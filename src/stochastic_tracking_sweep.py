"""Reproducible sharded stochastic sweeps for PAYOFF-B tracking."""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import isfinite

from src.spatiotemporal_tracking import (
    TrackingScenario,
    TrackingStrategy,
    classify_tracking_outcome,
)
from src.stochastic_tracking import (
    StochasticForcing,
    stochastic_tracking_ensemble,
)


@dataclass(frozen=True)
class UniformRange:
    low: float
    high: float

    def __post_init__(self) -> None:
        if not isfinite(self.low) or not isfinite(self.high):
            raise ValueError("range bounds must be finite")
        if self.high < self.low:
            raise ValueError("range high must be >= low")

    def draw(self, u: float) -> float:
        if not 0.0 <= u <= 1.0:
            raise ValueError("u must lie in [0, 1]")
        return self.low + u * (self.high - self.low)


@dataclass(frozen=True)
class StochasticSweepRanges:
    climate_velocity: UniformRange = UniformRange(0.01, 0.10)
    partner_spatial_share: UniformRange = UniformRange(0.0, 1.0)
    interaction_strength: UniformRange = UniformRange(0.0, 1.5)
    migration_cost: UniformRange = UniformRange(0.01, 0.15)
    phenology_cost: UniformRange = UniformRange(0.01, 0.15)
    climate_increment_sd: UniformRange = UniformRange(0.0, 0.04)
    partner_spatial_share_sd: UniformRange = UniformRange(0.0, 0.20)
    partner_demand_noise_sd: UniformRange = UniformRange(0.0, 0.10)


@dataclass(frozen=True)
class StochasticSweepPoint:
    sample_index: int
    scenario: TrackingScenario
    forcing: StochasticForcing


@dataclass(frozen=True)
class StochasticOptimizationResult:
    strategy: TrackingStrategy
    mean_log_growth: float
    sd_log_growth: float
    mean_abiotic_only_log_growth: float
    viability_fraction: float
    interaction_failure_fraction: float
    mean_rms_abiotic_mismatch: float
    mean_rms_interaction_mismatch: float
    outcome: str


def _index_uniforms(sample_index: int, seed: int, count: int) -> tuple[float, ...]:
    """Generate deterministic per-index pseudo-uniforms without shared RNG state."""

    if sample_index < 0:
        raise ValueError("sample_index must be non-negative")
    if count <= 0:
        raise ValueError("count must be positive")

    # SplitMix64: fast deterministic integer mixing with good bit diffusion.
    mask = (1 << 64) - 1
    state = (
        int(seed)
        + 0x9E3779B97F4A7C15 * (sample_index + 1)
    ) & mask
    values: list[float] = []
    for _ in range(count):
        state = (state + 0x9E3779B97F4A7C15) & mask
        z = state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & mask
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & mask
        z = z ^ (z >> 31)
        # Use the high 53 bits to map exactly into [0,1).
        values.append(((z >> 11) & ((1 << 53) - 1)) / float(1 << 53))
    return tuple(values)


def draw_stochastic_sweep_point(
    sample_index: int,
    *,
    seed: int,
    base_scenario: TrackingScenario,
    ranges: StochasticSweepRanges = StochasticSweepRanges(),
) -> StochasticSweepPoint:
    u = _index_uniforms(sample_index, seed, 8)
    scenario = replace(
        base_scenario,
        climate_velocity=ranges.climate_velocity.draw(u[0]),
        partner_spatial_share=ranges.partner_spatial_share.draw(u[1]),
        interaction_strength=ranges.interaction_strength.draw(u[2]),
        migration_cost=ranges.migration_cost.draw(u[3]),
        phenology_cost=ranges.phenology_cost.draw(u[4]),
    )
    forcing = StochasticForcing(
        climate_increment_sd=ranges.climate_increment_sd.draw(u[5]),
        partner_spatial_share_sd=(
            ranges.partner_spatial_share_sd.draw(u[6])
        ),
        partner_demand_noise_sd=(
            ranges.partner_demand_noise_sd.draw(u[7])
        ),
    )
    return StochasticSweepPoint(
        sample_index=sample_index,
        scenario=scenario,
        forcing=forcing,
    )


def optimize_stochastic_strategy(
    scenario: TrackingScenario,
    forcing: StochasticForcing,
    *,
    replicates: int,
    seed: int,
    max_rate: float = 1.5,
    points: int = 11,
) -> StochasticOptimizationResult:
    """Grid-optimize expected growth under common random environmental draws."""

    if replicates <= 0:
        raise ValueError("replicates must be positive")
    if max_rate <= 0.0:
        raise ValueError("max_rate must be positive")
    if points < 2:
        raise ValueError("points must be at least 2")

    values = [
        max_rate * index / (points - 1)
        for index in range(points)
    ]
    best: StochasticOptimizationResult | None = None

    for migration in values:
        for phenology in values:
            strategy = TrackingStrategy(migration, phenology)
            ensemble = stochastic_tracking_ensemble(
                strategy,
                scenario,
                forcing,
                replicates=replicates,
                seed=seed,
            )
            summary = ensemble.summary()
            outcome = classify_tracking_outcome(
                strategy,
                float(summary["mean_log_growth"]),
                float(summary["mean_abiotic_only_log_growth"]),
            )
            candidate = StochasticOptimizationResult(
                strategy=strategy,
                mean_log_growth=float(summary["mean_log_growth"]),
                sd_log_growth=float(summary["sd_log_growth"]),
                mean_abiotic_only_log_growth=float(
                    summary["mean_abiotic_only_log_growth"]
                ),
                viability_fraction=float(summary["viability_fraction"]),
                interaction_failure_fraction=float(
                    summary["interaction_failure_fraction"]
                ),
                mean_rms_abiotic_mismatch=float(
                    summary["mean_rms_abiotic_mismatch"]
                ),
                mean_rms_interaction_mismatch=float(
                    summary["mean_rms_interaction_mismatch"]
                ),
                outcome=outcome,
            )
            if best is None:
                best = candidate
                continue
            if candidate.mean_log_growth > best.mean_log_growth:
                best = candidate
                continue
            if candidate.mean_log_growth == best.mean_log_growth:
                if (
                    candidate.strategy.total_rate
                    < best.strategy.total_rate
                ):
                    best = candidate

    assert best is not None
    return best


def shard_sample_indices(
    samples: int,
    shard_index: int,
    shard_count: int,
) -> tuple[int, ...]:
    if samples < 0:
        raise ValueError("samples must be non-negative")
    if shard_count <= 0:
        raise ValueError("shard_count must be positive")
    if not 0 <= shard_index < shard_count:
        raise ValueError(
            "shard_index must satisfy 0 <= shard_index < shard_count"
        )
    return tuple(
        index
        for index in range(samples)
        if index % shard_count == shard_index
    )


def planned_tracking_steps(
    samples: int,
    strategy_points: int,
    replicates: int,
    ecological_steps: int,
) -> int:
    if min(samples, strategy_points, replicates, ecological_steps) < 0:
        raise ValueError("workload inputs must be non-negative")
    return (
        samples
        * strategy_points
        * strategy_points
        * replicates
        * ecological_steps
    )


def stochastic_sweep_row(
    point: StochasticSweepPoint,
    optimum: StochasticOptimizationResult,
    *,
    replicates: int,
    strategy_points: int,
) -> dict[str, float | int | str]:
    scenario = point.scenario
    forcing = point.forcing
    return {
        "sample_index": point.sample_index,
        "climate_velocity": scenario.climate_velocity,
        "partner_spatial_share": scenario.partner_spatial_share,
        "interaction_strength": scenario.interaction_strength,
        "migration_cost": scenario.migration_cost,
        "phenology_cost": scenario.phenology_cost,
        "climate_increment_sd": forcing.climate_increment_sd,
        "partner_spatial_share_sd": forcing.partner_spatial_share_sd,
        "partner_demand_noise_sd": forcing.partner_demand_noise_sd,
        "replicates": replicates,
        "strategy_points": strategy_points,
        "best_migration_rate": optimum.strategy.migration_rate,
        "best_phenology_rate": optimum.strategy.phenology_rate,
        "best_migration_share": optimum.strategy.migration_share,
        "mean_log_growth": optimum.mean_log_growth,
        "sd_log_growth": optimum.sd_log_growth,
        "mean_abiotic_only_log_growth": (
            optimum.mean_abiotic_only_log_growth
        ),
        "viability_fraction": optimum.viability_fraction,
        "interaction_failure_fraction": (
            optimum.interaction_failure_fraction
        ),
        "mean_rms_abiotic_mismatch": (
            optimum.mean_rms_abiotic_mismatch
        ),
        "mean_rms_interaction_mismatch": (
            optimum.mean_rms_interaction_mismatch
        ),
        "outcome": optimum.outcome,
    }
