"""Two-species coevolution on the migration--phenology tracking plane."""

from __future__ import annotations

from dataclasses import dataclass
from math import expm1, isfinite, sqrt

from src.spatiotemporal_tracking import (
    TrackingStrategy,
    classify_tracking_outcome,
)


_EPS = 1e-12


@dataclass(frozen=True)
class SpeciesTrackingParameters:
    abiotic_strength: float = 1.0
    interaction_strength: float = 0.25
    migration_cost: float = 0.05
    phenology_cost: float = 0.05
    joint_cost: float = 0.0
    baseline_growth: float = 0.2

    def __post_init__(self) -> None:
        for name in (
            "abiotic_strength",
            "interaction_strength",
            "migration_cost",
            "phenology_cost",
            "joint_cost",
            "baseline_growth",
        ):
            value = float(getattr(self, name))
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
        for name in (
            "abiotic_strength",
            "interaction_strength",
            "migration_cost",
            "phenology_cost",
            "joint_cost",
        ):
            if getattr(self, name) < 0.0:
                raise ValueError(f"{name} must be non-negative")


@dataclass(frozen=True)
class CoevolutionScenario:
    climate_velocity: float = 0.05
    phenology_scale: float = 1.0
    steps: int = 240
    burn_in: int = 60
    species_a: SpeciesTrackingParameters = SpeciesTrackingParameters()
    species_b: SpeciesTrackingParameters = SpeciesTrackingParameters()

    def __post_init__(self) -> None:
        if not isfinite(self.climate_velocity):
            raise ValueError("climate_velocity must be finite")
        if not isfinite(self.phenology_scale) or self.phenology_scale <= 0.0:
            raise ValueError("phenology_scale must be positive and finite")
        if self.steps <= 0:
            raise ValueError("steps must be positive")
        if not 0 <= self.burn_in < self.steps:
            raise ValueError("burn_in must satisfy 0 <= burn_in < steps")


@dataclass(frozen=True)
class PairSimulationResult:
    strategy_a: TrackingStrategy
    strategy_b: TrackingStrategy
    mean_log_growth_a: float
    mean_log_growth_b: float
    abiotic_only_mean_log_growth_a: float
    abiotic_only_mean_log_growth_b: float
    rms_abiotic_mismatch_a: float
    rms_abiotic_mismatch_b: float
    rms_interaction_mismatch: float
    outcome_a: str
    outcome_b: str

    @property
    def both_viable(self) -> bool:
        return (
            self.mean_log_growth_a >= 0.0
            and self.mean_log_growth_b >= 0.0
        )


@dataclass(frozen=True)
class CoevolutionResult:
    path: tuple[PairSimulationResult, ...]
    converged: bool
    cycles: int

    @property
    def final(self) -> PairSimulationResult:
        return self.path[-1]


def _correction_fraction(total_rate: float) -> float:
    if total_rate <= 0.0:
        return 0.0
    return -expm1(-total_rate)


def _step_tracking(
    strategy: TrackingStrategy,
    spatial_position: float,
    phenology_shift: float,
    demand: float,
    phenology_scale: float,
) -> tuple[float, float, float]:
    total = strategy.total_rate
    mismatch = demand - (
        spatial_position + phenology_scale * phenology_shift
    )
    if total <= _EPS:
        return spatial_position, phenology_shift, mismatch

    correction = _correction_fraction(total) * mismatch
    migration_share = strategy.migration_rate / total
    phenology_share = strategy.phenology_rate / total
    spatial_position += migration_share * correction
    phenology_shift += (
        phenology_share * correction / phenology_scale
    )
    mismatch_after = demand - (
        spatial_position + phenology_scale * phenology_shift
    )
    return spatial_position, phenology_shift, mismatch_after


def _architecture_cost(
    strategy: TrackingStrategy,
    parameters: SpeciesTrackingParameters,
) -> float:
    m = strategy.migration_rate
    h = strategy.phenology_rate
    return (
        parameters.migration_cost * m * m
        + parameters.phenology_cost * h * h
        + parameters.joint_cost * m * h
    )


def simulate_coevolving_pair(
    strategy_a: TrackingStrategy,
    strategy_b: TrackingStrategy,
    scenario: CoevolutionScenario,
) -> PairSimulationResult:
    """Simulate two interacting lineages tracking the same moving environment."""

    x_a = 0.0
    z_a = 0.0
    x_b = 0.0
    z_b = 0.0

    growth_a = 0.0
    growth_b = 0.0
    abiotic_growth_a = 0.0
    abiotic_growth_b = 0.0
    abiotic_sq_a = 0.0
    abiotic_sq_b = 0.0
    interaction_sq_sum = 0.0
    observed = 0

    cost_a = _architecture_cost(strategy_a, scenario.species_a)
    cost_b = _architecture_cost(strategy_b, scenario.species_b)

    for step in range(1, scenario.steps + 1):
        demand = scenario.climate_velocity * step

        x_a, z_a, mismatch_a = _step_tracking(
            strategy_a,
            x_a,
            z_a,
            demand,
            scenario.phenology_scale,
        )
        x_b, z_b, mismatch_b = _step_tracking(
            strategy_b,
            x_b,
            z_b,
            demand,
            scenario.phenology_scale,
        )

        spatial_gap = x_a - x_b
        phenology_gap = scenario.phenology_scale * (z_a - z_b)
        interaction_sq = (
            spatial_gap * spatial_gap + phenology_gap * phenology_gap
        )

        abiotic_a = (
            scenario.species_a.baseline_growth
            - cost_a
            - 0.5
            * scenario.species_a.abiotic_strength
            * mismatch_a
            * mismatch_a
        )
        abiotic_b = (
            scenario.species_b.baseline_growth
            - cost_b
            - 0.5
            * scenario.species_b.abiotic_strength
            * mismatch_b
            * mismatch_b
        )

        current_a = (
            abiotic_a
            - 0.5
            * scenario.species_a.interaction_strength
            * interaction_sq
        )
        current_b = (
            abiotic_b
            - 0.5
            * scenario.species_b.interaction_strength
            * interaction_sq
        )

        if step > scenario.burn_in:
            observed += 1
            growth_a += current_a
            growth_b += current_b
            abiotic_growth_a += abiotic_a
            abiotic_growth_b += abiotic_b
            abiotic_sq_a += mismatch_a * mismatch_a
            abiotic_sq_b += mismatch_b * mismatch_b
            interaction_sq_sum += interaction_sq

    mean_a = growth_a / observed
    mean_b = growth_b / observed
    abiotic_mean_a = abiotic_growth_a / observed
    abiotic_mean_b = abiotic_growth_b / observed

    return PairSimulationResult(
        strategy_a=strategy_a,
        strategy_b=strategy_b,
        mean_log_growth_a=mean_a,
        mean_log_growth_b=mean_b,
        abiotic_only_mean_log_growth_a=abiotic_mean_a,
        abiotic_only_mean_log_growth_b=abiotic_mean_b,
        rms_abiotic_mismatch_a=sqrt(abiotic_sq_a / observed),
        rms_abiotic_mismatch_b=sqrt(abiotic_sq_b / observed),
        rms_interaction_mismatch=sqrt(
            interaction_sq_sum / observed
        ),
        outcome_a=classify_tracking_outcome(
            strategy_a,
            mean_a,
            abiotic_mean_a,
        ),
        outcome_b=classify_tracking_outcome(
            strategy_b,
            mean_b,
            abiotic_mean_b,
        ),
    )


def _neighbor_strategies(
    strategy: TrackingStrategy,
    mutation_step: float,
    max_rate: float,
) -> tuple[TrackingStrategy, ...]:
    if mutation_step <= 0.0:
        raise ValueError("mutation_step must be positive")
    if max_rate <= 0.0:
        raise ValueError("max_rate must be positive")
    if (
        strategy.migration_rate > max_rate + _EPS
        or strategy.phenology_rate > max_rate + _EPS
    ):
        raise ValueError("strategy exceeds max_rate")

    neighbors: list[TrackingStrategy] = []
    seen: set[tuple[float, float]] = set()
    for dm in (-mutation_step, 0.0, mutation_step):
        for dh in (-mutation_step, 0.0, mutation_step):
            if dm == 0.0 and dh == 0.0:
                continue
            m = min(max_rate, max(0.0, strategy.migration_rate + dm))
            h = min(max_rate, max(0.0, strategy.phenology_rate + dh))
            key = (round(m, 12), round(h, 12))
            if key in seen:
                continue
            if (
                abs(m - strategy.migration_rate) <= _EPS
                and abs(h - strategy.phenology_rate) <= _EPS
            ):
                continue
            seen.add(key)
            neighbors.append(TrackingStrategy(m, h))
    return tuple(neighbors)


def coevolve_tracking_pair(
    scenario: CoevolutionScenario,
    initial_a: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    initial_b: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    *,
    mutation_step: float = 0.1,
    max_rate: float = 1.5,
    max_cycles: int = 100,
    improvement_tolerance: float = 1e-10,
) -> CoevolutionResult:
    """Alternating rare-mutation adaptive walk for two interacting lineages.

    Species A is offered all one-step axial/diagonal mutants while B is fixed;
    the best strictly improving mutant fixes. Species B is then updated against
    the new A strategy. A full A+B cycle with no substitution is convergence.
    """

    if max_cycles <= 0:
        raise ValueError("max_cycles must be positive")
    if improvement_tolerance < 0.0:
        raise ValueError("improvement_tolerance must be non-negative")

    current = simulate_coevolving_pair(
        initial_a,
        initial_b,
        scenario,
    )
    path = [current]

    for cycle in range(1, max_cycles + 1):
        changed = False

        a_candidates = [
            simulate_coevolving_pair(
                mutant,
                current.strategy_b,
                scenario,
            )
            for mutant in _neighbor_strategies(
                current.strategy_a,
                mutation_step,
                max_rate,
            )
        ]
        if a_candidates:
            best_a = max(
                a_candidates,
                key=lambda row: row.mean_log_growth_a,
            )
            if (
                best_a.mean_log_growth_a
                > current.mean_log_growth_a + improvement_tolerance
            ):
                current = best_a
                path.append(current)
                changed = True

        b_candidates = [
            simulate_coevolving_pair(
                current.strategy_a,
                mutant,
                scenario,
            )
            for mutant in _neighbor_strategies(
                current.strategy_b,
                mutation_step,
                max_rate,
            )
        ]
        if b_candidates:
            best_b = max(
                b_candidates,
                key=lambda row: row.mean_log_growth_b,
            )
            if (
                best_b.mean_log_growth_b
                > current.mean_log_growth_b + improvement_tolerance
            ):
                current = best_b
                path.append(current)
                changed = True

        if not changed:
            return CoevolutionResult(
                path=tuple(path),
                converged=True,
                cycles=cycle,
            )

    return CoevolutionResult(
        path=tuple(path),
        converged=False,
        cycles=max_cycles,
    )



@dataclass(frozen=True)
class CoordinationBarrierDiagnostic:
    local: CoevolutionResult
    matched_optimum: PairSimulationResult
    accessibility_gap: float
    barrier: bool


def optimize_matched_pair(
    scenario: CoevolutionScenario,
    *,
    max_rate: float = 1.5,
    points: int = 16,
) -> PairSimulationResult:
    """Optimize a constrained matched pair with strategy_a == strategy_b.

    This is a coordinated benchmark, not an evolutionary path. Because both
    lineages move together, the interaction mismatch is exactly zero at every
    candidate strategy.
    """

    if max_rate <= 0.0:
        raise ValueError("max_rate must be positive")
    if points < 2:
        raise ValueError("points must be at least 2")
    values = [
        max_rate * index / (points - 1)
        for index in range(points)
    ]
    best: PairSimulationResult | None = None
    for migration in values:
        for phenology in values:
            strategy = TrackingStrategy(
                migration,
                phenology,
            )
            candidate = simulate_coevolving_pair(
                strategy,
                strategy,
                scenario,
            )
            candidate_score = 0.5 * (
                candidate.mean_log_growth_a
                + candidate.mean_log_growth_b
            )
            if best is None:
                best = candidate
                continue
            best_score = 0.5 * (
                best.mean_log_growth_a
                + best.mean_log_growth_b
            )
            if candidate_score > best_score:
                best = candidate
            elif candidate_score == best_score:
                if (
                    strategy.total_rate
                    < best.strategy_a.total_rate
                ):
                    best = candidate
    assert best is not None
    return best


def coordination_barrier_diagnostic(
    scenario: CoevolutionScenario,
    *,
    initial_a: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    initial_b: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    mutation_step: float = 0.1,
    max_rate: float = 1.5,
    max_cycles: int = 100,
    matched_points: int | None = None,
    gap_tolerance: float = 1e-10,
) -> CoordinationBarrierDiagnostic:
    """Compare local unilateral accessibility with a coordinated benchmark."""

    if gap_tolerance < 0.0:
        raise ValueError("gap_tolerance must be non-negative")
    local = coevolve_tracking_pair(
        scenario,
        initial_a,
        initial_b,
        mutation_step=mutation_step,
        max_rate=max_rate,
        max_cycles=max_cycles,
    )
    if matched_points is None:
        # Align the benchmark grid with the mutation lattice whenever possible.
        matched_points = int(round(max_rate / mutation_step)) + 1
    matched = optimize_matched_pair(
        scenario,
        max_rate=max_rate,
        points=matched_points,
    )
    local_score = 0.5 * (
        local.final.mean_log_growth_a
        + local.final.mean_log_growth_b
    )
    matched_score = 0.5 * (
        matched.mean_log_growth_a
        + matched.mean_log_growth_b
    )
    gap = max(0.0, matched_score - local_score)
    return CoordinationBarrierDiagnostic(
        local=local,
        matched_optimum=matched,
        accessibility_gap=gap,
        barrier=gap > gap_tolerance,
    )
