"""Migration--phenology tracking model for PAYOFF-B.

This module adds a minimal eco-evolutionary tracking layer in which spatial
movement and phenological change are alternative ways to close the same moving
environmental mismatch. An exogenous interaction partner can track the same
environmental demand through a different mixture of the two axes.

The baseline is deliberately deterministic and dependency-free. It is a
benchmark that can later be embedded in stochastic population, network, and
large parameter-sweep simulations.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import expm1, isfinite, sqrt
from typing import Iterable


_EPS = 1e-12


def _finite(name: str, value: float) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


@dataclass(frozen=True)
class TrackingStrategy:
    """Heritable rates of spatial and phenological tracking."""

    migration_rate: float
    phenology_rate: float

    def __post_init__(self) -> None:
        for name, value in (
            ("migration_rate", self.migration_rate),
            ("phenology_rate", self.phenology_rate),
        ):
            _finite(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be non-negative")

    @property
    def total_rate(self) -> float:
        return self.migration_rate + self.phenology_rate

    @property
    def migration_share(self) -> float:
        if self.total_rate <= _EPS:
            return 0.5
        return self.migration_rate / self.total_rate


@dataclass(frozen=True)
class TrackingScenario:
    """Ecological forcing, partner tracking, and costs for one simulation."""

    climate_velocity: float = 0.05
    partner_tracking_fraction: float = 1.0
    partner_spatial_share: float = 0.5
    partner_lag: float = 0.0
    phenology_scale: float = 1.0
    abiotic_strength: float = 1.0
    interaction_strength: float = 0.25
    migration_cost: float = 0.05
    phenology_cost: float = 0.05
    joint_cost: float = 0.0
    baseline_growth: float = 0.2
    steps: int = 240
    burn_in: int = 60

    def __post_init__(self) -> None:
        for name in (
            "climate_velocity",
            "partner_tracking_fraction",
            "partner_spatial_share",
            "partner_lag",
            "phenology_scale",
            "abiotic_strength",
            "interaction_strength",
            "migration_cost",
            "phenology_cost",
            "joint_cost",
            "baseline_growth",
        ):
            _finite(name, float(getattr(self, name)))
        if self.partner_tracking_fraction < 0.0:
            raise ValueError("partner_tracking_fraction must be non-negative")
        if not 0.0 <= self.partner_spatial_share <= 1.0:
            raise ValueError("partner_spatial_share must lie in [0, 1]")
        if self.phenology_scale <= 0.0:
            raise ValueError("phenology_scale must be positive")
        for name in (
            "abiotic_strength",
            "interaction_strength",
            "migration_cost",
            "phenology_cost",
            "joint_cost",
        ):
            if getattr(self, name) < 0.0:
                raise ValueError(f"{name} must be non-negative")
        if self.steps <= 0:
            raise ValueError("steps must be positive")
        if not 0 <= self.burn_in < self.steps:
            raise ValueError("burn_in must satisfy 0 <= burn_in < steps")


@dataclass(frozen=True)
class TrackingSimulationResult:
    strategy: TrackingStrategy
    mean_log_growth: float
    abiotic_only_mean_log_growth: float
    rms_abiotic_mismatch: float
    rms_interaction_mismatch: float
    final_spatial_position: float
    final_phenology_shift: float
    final_environmental_demand: float
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
class EvolutionResult:
    """Rare-mutation adaptive walk over migration/phenology strategy space."""

    path: tuple[TrackingSimulationResult, ...]
    converged: bool

    @property
    def final(self) -> TrackingSimulationResult:
        return self.path[-1]


def classify_tracking_outcome(
    strategy: TrackingStrategy,
    mean_log_growth: float,
    abiotic_only_mean_log_growth: float,
    dominance_threshold: float = 2.0 / 3.0,
) -> str:
    """Classify survival and the dominant adaptive axis."""

    if not 0.5 < dominance_threshold < 1.0:
        raise ValueError("dominance_threshold must lie in (0.5, 1)")
    if mean_log_growth < 0.0:
        if abiotic_only_mean_log_growth >= 0.0:
            return "interaction_failure"
        return "failure"
    if strategy.total_rate <= _EPS:
        return "stasis"
    share = strategy.migration_share
    if share >= dominance_threshold:
        return "migration"
    if share <= 1.0 - dominance_threshold:
        return "phenology"
    return "mixed"


def _tracking_correction_fraction(total_rate: float) -> float:
    """Fraction of current environmental mismatch closed in one generation."""

    if total_rate <= 0.0:
        return 0.0
    return -expm1(-total_rate)


def simulate_tracking(
    strategy: TrackingStrategy,
    scenario: TrackingScenario,
) -> TrackingSimulationResult:
    """Simulate one fixed heritable tracking strategy.

    The moving environmental demand is D_t = climate_velocity * t in a common
    climate-equivalent coordinate. Spatial displacement x and scaled
    phenological displacement s*z close the same mismatch:

        mismatch = D_t - (x + s*z).

    The two adaptive axes are therefore substitutable in abiotic tracking.
    Their allocation matters because the interaction partner can partition its
    own tracking differently between space and phenology.
    """

    migration = strategy.migration_rate
    phenology = strategy.phenology_rate
    total_rate = strategy.total_rate
    correction_fraction = _tracking_correction_fraction(total_rate)

    if total_rate > _EPS:
        migration_share = migration / total_rate
        phenology_share = phenology / total_rate
    else:
        migration_share = 0.0
        phenology_share = 0.0

    spatial_position = 0.0
    phenology_shift = 0.0
    growth_sum = 0.0
    abiotic_only_sum = 0.0
    abiotic_sq_sum = 0.0
    interaction_sq_sum = 0.0
    observed = 0

    architecture_cost = (
        scenario.migration_cost * migration * migration
        + scenario.phenology_cost * phenology * phenology
        + scenario.joint_cost * migration * phenology
    )

    for step in range(1, scenario.steps + 1):
        demand = scenario.climate_velocity * step
        residual = demand - (
            spatial_position + scenario.phenology_scale * phenology_shift
        )

        correction = correction_fraction * residual
        spatial_position += migration_share * correction
        phenology_shift += (
            phenology_share * correction / scenario.phenology_scale
        )

        abiotic_mismatch = demand - (
            spatial_position + scenario.phenology_scale * phenology_shift
        )

        partner_demand = (
            scenario.partner_tracking_fraction * demand - scenario.partner_lag
        )
        partner_spatial_position = (
            scenario.partner_spatial_share * partner_demand
        )
        partner_phenology_shift = (
            (1.0 - scenario.partner_spatial_share)
            * partner_demand
            / scenario.phenology_scale
        )

        spatial_gap = spatial_position - partner_spatial_position
        phenology_gap = scenario.phenology_scale * (
            phenology_shift - partner_phenology_shift
        )
        interaction_sq = (
            spatial_gap * spatial_gap + phenology_gap * phenology_gap
        )

        abiotic_penalty = (
            0.5
            * scenario.abiotic_strength
            * abiotic_mismatch
            * abiotic_mismatch
        )
        interaction_penalty = (
            0.5 * scenario.interaction_strength * interaction_sq
        )

        abiotic_only_growth = (
            scenario.baseline_growth - architecture_cost - abiotic_penalty
        )
        log_growth = abiotic_only_growth - interaction_penalty

        if step > scenario.burn_in:
            observed += 1
            growth_sum += log_growth
            abiotic_only_sum += abiotic_only_growth
            abiotic_sq_sum += abiotic_mismatch * abiotic_mismatch
            interaction_sq_sum += interaction_sq

    mean_growth = growth_sum / observed
    abiotic_only_mean = abiotic_only_sum / observed
    outcome = classify_tracking_outcome(
        strategy, mean_growth, abiotic_only_mean
    )
    return TrackingSimulationResult(
        strategy=strategy,
        mean_log_growth=mean_growth,
        abiotic_only_mean_log_growth=abiotic_only_mean,
        rms_abiotic_mismatch=sqrt(abiotic_sq_sum / observed),
        rms_interaction_mismatch=sqrt(interaction_sq_sum / observed),
        final_spatial_position=spatial_position,
        final_phenology_shift=phenology_shift,
        final_environmental_demand=(
            scenario.climate_velocity * scenario.steps
        ),
        outcome=outcome,
    )


def _grid_values(max_rate: float, points: int) -> list[float]:
    _finite("max_rate", max_rate)
    if max_rate <= 0.0:
        raise ValueError("max_rate must be positive")
    if points < 2:
        raise ValueError("points must be at least 2")
    return [max_rate * i / (points - 1) for i in range(points)]


def _result_rank(
    result: TrackingSimulationResult,
) -> tuple[float, float, float]:
    """Rank by growth, then prefer parsimonious strategies on exact ties."""

    strategy = result.strategy
    return (
        result.mean_log_growth,
        -strategy.total_rate,
        -abs(strategy.migration_share - 0.5),
    )


def optimize_tracking_strategy(
    scenario: TrackingScenario,
    *,
    max_rate: float = 1.5,
    points: int = 31,
) -> TrackingSimulationResult:
    """Return the best strategy on a migration/phenology grid."""

    values = _grid_values(max_rate, points)
    best: TrackingSimulationResult | None = None
    for migration in values:
        for phenology in values:
            result = simulate_tracking(
                TrackingStrategy(migration, phenology), scenario
            )
            if best is None or _result_rank(result) > _result_rank(best):
                best = result
    assert best is not None
    return best


def evolve_tracking_strategy(
    scenario: TrackingScenario,
    initial: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    *,
    mutation_step: float = 0.1,
    max_rate: float = 1.5,
    max_evolution_steps: int = 100,
    improvement_tolerance: float = 1e-10,
) -> EvolutionResult:
    """Rare-mutation adaptive walk on the two-dimensional strategy surface.

    At each evolutionary step, the resident is compared with all one-step
    axis and diagonal mutants. The best strictly improving mutant fixes.
    This is a deterministic accessibility benchmark, not a finite-population
    fixation model.
    """

    for name, value in (
        ("mutation_step", mutation_step),
        ("max_rate", max_rate),
        ("improvement_tolerance", improvement_tolerance),
    ):
        _finite(name, value)
    if mutation_step <= 0.0:
        raise ValueError("mutation_step must be positive")
    if max_rate <= 0.0:
        raise ValueError("max_rate must be positive")
    if max_evolution_steps <= 0:
        raise ValueError("max_evolution_steps must be positive")
    if improvement_tolerance < 0.0:
        raise ValueError("improvement_tolerance must be non-negative")
    if (
        initial.migration_rate > max_rate
        or initial.phenology_rate > max_rate
    ):
        raise ValueError("initial strategy exceeds max_rate")

    current = simulate_tracking(initial, scenario)
    path = [current]
    offsets = (-mutation_step, 0.0, mutation_step)

    for _ in range(max_evolution_steps):
        candidates: list[TrackingSimulationResult] = []
        seen: set[tuple[float, float]] = set()
        for dm in offsets:
            for dp in offsets:
                if dm == 0.0 and dp == 0.0:
                    continue
                migration = min(
                    max_rate,
                    max(0.0, current.strategy.migration_rate + dm),
                )
                phenology = min(
                    max_rate,
                    max(0.0, current.strategy.phenology_rate + dp),
                )
                key = (round(migration, 12), round(phenology, 12))
                if key in seen:
                    continue
                if (
                    abs(
                        migration - current.strategy.migration_rate
                    )
                    <= _EPS
                    and abs(
                        phenology - current.strategy.phenology_rate
                    )
                    <= _EPS
                ):
                    continue
                seen.add(key)
                candidates.append(
                    simulate_tracking(
                        TrackingStrategy(migration, phenology),
                        scenario,
                    )
                )

        if not candidates:
            return EvolutionResult(tuple(path), True)

        best = max(candidates, key=_result_rank)
        if (
            best.mean_log_growth
            <= current.mean_log_growth + improvement_tolerance
        ):
            return EvolutionResult(tuple(path), True)
        current = best
        path.append(current)

    return EvolutionResult(tuple(path), False)


def tracking_phase_diagram(
    base_scenario: TrackingScenario,
    climate_velocities: Iterable[float],
    partner_spatial_shares: Iterable[float],
    *,
    max_rate: float = 1.5,
    points: int = 31,
) -> list[dict[str, float | str]]:
    """Optimize over a climate-speed x partner-axis design."""

    rows: list[dict[str, float | str]] = []
    for velocity in climate_velocities:
        _finite("climate_velocity", velocity)
        for share in partner_spatial_shares:
            _finite("partner_spatial_share", share)
            if not 0.0 <= share <= 1.0:
                raise ValueError(
                    "partner spatial shares must lie in [0, 1]"
                )
            scenario = replace(
                base_scenario,
                climate_velocity=velocity,
                partner_spatial_share=share,
            )
            best = optimize_tracking_strategy(
                scenario,
                max_rate=max_rate,
                points=points,
            )
            rows.append(
                {
                    "climate_velocity": velocity,
                    "partner_spatial_share": share,
                    "migration_rate": best.strategy.migration_rate,
                    "phenology_rate": best.strategy.phenology_rate,
                    "migration_share": best.strategy.migration_share,
                    "mean_log_growth": best.mean_log_growth,
                    "abiotic_only_mean_log_growth": (
                        best.abiotic_only_mean_log_growth
                    ),
                    "rms_abiotic_mismatch": (
                        best.rms_abiotic_mismatch
                    ),
                    "rms_interaction_mismatch": (
                        best.rms_interaction_mismatch
                    ),
                    "outcome": best.outcome,
                }
            )
    return rows
