"""Stochastic forcing for migration--phenology tracking.

Environmental demand follows a noisy random walk with drift. The interaction
partner can also vary its spatial-versus-phenological allocation through time.
This layer is intentionally seed-explicit so large sweeps are reproducible and
shardable.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import expm1, isfinite, sqrt
from random import Random
from statistics import mean, pstdev

from src.spatiotemporal_tracking import (
    TrackingScenario,
    TrackingStrategy,
    classify_tracking_outcome,
)


_EPS = 1e-12


@dataclass(frozen=True)
class StochasticForcing:
    climate_increment_sd: float = 0.0
    partner_spatial_share_sd: float = 0.0
    partner_demand_noise_sd: float = 0.0

    def __post_init__(self) -> None:
        for name in (
            "climate_increment_sd",
            "partner_spatial_share_sd",
            "partner_demand_noise_sd",
        ):
            value = float(getattr(self, name))
            if not isfinite(value) or value < 0.0:
                raise ValueError(
                    f"{name} must be non-negative and finite"
                )


@dataclass(frozen=True)
class StochasticTrackingResult:
    strategy: TrackingStrategy
    seed: int
    mean_log_growth: float
    abiotic_only_mean_log_growth: float
    rms_abiotic_mismatch: float
    rms_interaction_mismatch: float
    final_environmental_demand: float
    realized_mean_climate_increment: float
    outcome: str

    @property
    def viable(self) -> bool:
        return self.mean_log_growth >= 0.0

    @property
    def interaction_limited(self) -> bool:
        return (
            self.mean_log_growth < 0.0
            and self.abiotic_only_mean_log_growth >= 0.0
        )


@dataclass(frozen=True)
class StochasticEnsembleResult:
    strategy: TrackingStrategy
    replicates: tuple[StochasticTrackingResult, ...]

    def summary(self) -> dict[str, float | int]:
        growth = [row.mean_log_growth for row in self.replicates]
        abiotic = [
            row.abiotic_only_mean_log_growth
            for row in self.replicates
        ]
        return {
            "replicates": len(self.replicates),
            "mean_log_growth": mean(growth),
            "sd_log_growth": pstdev(growth) if len(growth) > 1 else 0.0,
            "mean_abiotic_only_log_growth": mean(abiotic),
            "viability_fraction": (
                sum(row.viable for row in self.replicates)
                / len(self.replicates)
            ),
            "interaction_failure_fraction": (
                sum(
                    row.interaction_limited
                    for row in self.replicates
                )
                / len(self.replicates)
            ),
            "mean_rms_abiotic_mismatch": mean(
                row.rms_abiotic_mismatch
                for row in self.replicates
            ),
            "mean_rms_interaction_mismatch": mean(
                row.rms_interaction_mismatch
                for row in self.replicates
            ),
        }


def _clip01(value: float) -> float:
    return min(1.0, max(0.0, value))


def _correction_fraction(total_rate: float) -> float:
    if total_rate <= 0.0:
        return 0.0
    return -expm1(-total_rate)


def simulate_stochastic_tracking(
    strategy: TrackingStrategy,
    scenario: TrackingScenario,
    forcing: StochasticForcing,
    *,
    seed: int,
) -> StochasticTrackingResult:
    """Simulate one explicit stochastic environmental realization."""

    rng = Random(seed)
    total_rate = strategy.total_rate
    correction_fraction = _correction_fraction(total_rate)
    if total_rate > _EPS:
        migration_share = strategy.migration_rate / total_rate
        phenology_share = strategy.phenology_rate / total_rate
    else:
        migration_share = 0.0
        phenology_share = 0.0

    spatial_position = 0.0
    phenology_shift = 0.0
    demand = 0.0
    increment_sum = 0.0

    architecture_cost = (
        scenario.migration_cost
        * strategy.migration_rate
        * strategy.migration_rate
        + scenario.phenology_cost
        * strategy.phenology_rate
        * strategy.phenology_rate
        + scenario.joint_cost
        * strategy.migration_rate
        * strategy.phenology_rate
    )

    growth_sum = 0.0
    abiotic_growth_sum = 0.0
    abiotic_sq_sum = 0.0
    interaction_sq_sum = 0.0
    observed = 0

    for step in range(1, scenario.steps + 1):
        increment = scenario.climate_velocity
        if forcing.climate_increment_sd > 0.0:
            increment += rng.gauss(
                0.0, forcing.climate_increment_sd
            )
        demand += increment
        increment_sum += increment

        residual = demand - (
            spatial_position
            + scenario.phenology_scale * phenology_shift
        )
        correction = correction_fraction * residual
        spatial_position += migration_share * correction
        phenology_shift += (
            phenology_share
            * correction
            / scenario.phenology_scale
        )

        abiotic_mismatch = demand - (
            spatial_position
            + scenario.phenology_scale * phenology_shift
        )

        partner_share = scenario.partner_spatial_share
        if forcing.partner_spatial_share_sd > 0.0:
            partner_share = _clip01(
                partner_share
                + rng.gauss(
                    0.0, forcing.partner_spatial_share_sd
                )
            )

        partner_demand = (
            scenario.partner_tracking_fraction * demand
            - scenario.partner_lag
        )
        if forcing.partner_demand_noise_sd > 0.0:
            partner_demand += rng.gauss(
                0.0, forcing.partner_demand_noise_sd
            )

        partner_spatial_position = (
            partner_share * partner_demand
        )
        partner_phenology_shift = (
            (1.0 - partner_share)
            * partner_demand
            / scenario.phenology_scale
        )

        spatial_gap = (
            spatial_position - partner_spatial_position
        )
        phenology_gap = scenario.phenology_scale * (
            phenology_shift - partner_phenology_shift
        )
        interaction_sq = (
            spatial_gap * spatial_gap
            + phenology_gap * phenology_gap
        )

        abiotic_penalty = (
            0.5
            * scenario.abiotic_strength
            * abiotic_mismatch
            * abiotic_mismatch
        )
        interaction_penalty = (
            0.5
            * scenario.interaction_strength
            * interaction_sq
        )
        abiotic_growth = (
            scenario.baseline_growth
            - architecture_cost
            - abiotic_penalty
        )
        full_growth = (
            abiotic_growth - interaction_penalty
        )

        if step > scenario.burn_in:
            observed += 1
            growth_sum += full_growth
            abiotic_growth_sum += abiotic_growth
            abiotic_sq_sum += (
                abiotic_mismatch * abiotic_mismatch
            )
            interaction_sq_sum += interaction_sq

    mean_growth = growth_sum / observed
    mean_abiotic = abiotic_growth_sum / observed
    return StochasticTrackingResult(
        strategy=strategy,
        seed=seed,
        mean_log_growth=mean_growth,
        abiotic_only_mean_log_growth=mean_abiotic,
        rms_abiotic_mismatch=sqrt(
            abiotic_sq_sum / observed
        ),
        rms_interaction_mismatch=sqrt(
            interaction_sq_sum / observed
        ),
        final_environmental_demand=demand,
        realized_mean_climate_increment=(
            increment_sum / scenario.steps
        ),
        outcome=classify_tracking_outcome(
            strategy,
            mean_growth,
            mean_abiotic,
        ),
    )


def stochastic_tracking_ensemble(
    strategy: TrackingStrategy,
    scenario: TrackingScenario,
    forcing: StochasticForcing,
    *,
    replicates: int,
    seed: int,
) -> StochasticEnsembleResult:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    rows = tuple(
        simulate_stochastic_tracking(
            strategy,
            scenario,
            forcing,
            seed=seed + replicate * 1_000_003,
        )
        for replicate in range(replicates)
    )
    return StochasticEnsembleResult(
        strategy=strategy,
        replicates=rows,
    )
