"""Coevolutionary accessibility on the explicit moving-climate landscape."""

from __future__ import annotations

from dataclasses import dataclass

from src.moving_climate_landscape import (
    LandscapePairResult,
    MovingLandscapeScenario,
    optimize_matched_landscape_strategy,
    simulate_moving_landscape_pair,
)
from src.spatiotemporal_tracking import TrackingStrategy


@dataclass(frozen=True)
class LandscapeCoevolutionResult:
    path: tuple[LandscapePairResult, ...]
    converged: bool
    cycles: int

    @property
    def final(self) -> LandscapePairResult:
        return self.path[-1]


@dataclass(frozen=True)
class LandscapeCoordinationBarrier:
    local: LandscapeCoevolutionResult
    matched_optimum: LandscapePairResult
    accessibility_gap: float
    barrier: bool


def _neighbor_strategies(
    strategy: TrackingStrategy,
    mutation_step: float,
    max_migration_rate: float,
    max_phenology_rate: float,
) -> tuple[TrackingStrategy, ...]:
    if mutation_step <= 0.0:
        raise ValueError("mutation_step must be positive")
    if max_migration_rate < 0.0 or max_phenology_rate < 0.0:
        raise ValueError("maximum rates must be non-negative")

    neighbors: list[TrackingStrategy] = []
    seen: set[tuple[float, float]] = set()
    for dm in (-mutation_step, 0.0, mutation_step):
        for dh in (-mutation_step, 0.0, mutation_step):
            if dm == 0.0 and dh == 0.0:
                continue
            migration = min(
                max_migration_rate,
                max(0.0, strategy.migration_rate + dm),
            )
            phenology = min(
                max_phenology_rate,
                max(0.0, strategy.phenology_rate + dh),
            )
            key = (
                round(migration, 12),
                round(phenology, 12),
            )
            if key in seen:
                continue
            if (
                abs(migration - strategy.migration_rate) <= 1e-12
                and abs(phenology - strategy.phenology_rate) <= 1e-12
            ):
                continue
            seen.add(key)
            neighbors.append(
                TrackingStrategy(migration, phenology)
            )
    return tuple(neighbors)


def coevolve_moving_landscape_pair(
    scenario: MovingLandscapeScenario,
    initial_a: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    initial_b: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    *,
    mutation_step: float = 0.1,
    max_migration_rate: float = 1.0,
    max_phenology_rate: float = 1.0,
    max_cycles: int = 100,
    improvement_tolerance: float = 1e-10,
) -> LandscapeCoevolutionResult:
    """Alternating strictly improving substitutions on the explicit landscape."""

    if max_cycles <= 0:
        raise ValueError("max_cycles must be positive")
    if improvement_tolerance < 0.0:
        raise ValueError("improvement_tolerance must be non-negative")

    cache: dict[
        tuple[float, float, float, float],
        LandscapePairResult,
    ] = {}

    def evaluate(
        strategy_a: TrackingStrategy,
        strategy_b: TrackingStrategy,
    ) -> LandscapePairResult:
        key = (
            round(strategy_a.migration_rate, 12),
            round(strategy_a.phenology_rate, 12),
            round(strategy_b.migration_rate, 12),
            round(strategy_b.phenology_rate, 12),
        )
        if key not in cache:
            cache[key] = simulate_moving_landscape_pair(
                strategy_a,
                strategy_b,
                scenario,
            )
        return cache[key]

    current = evaluate(initial_a, initial_b)
    path = [current]

    for cycle in range(1, max_cycles + 1):
        changed = False

        candidates_a = [
            evaluate(mutant, current.strategy_b)
            for mutant in _neighbor_strategies(
                current.strategy_a,
                mutation_step,
                max_migration_rate,
                max_phenology_rate,
            )
        ]
        if candidates_a:
            best_a = max(
                candidates_a,
                key=lambda row: row.mean_log_growth_a,
            )
            if (
                best_a.mean_log_growth_a
                > current.mean_log_growth_a + improvement_tolerance
            ):
                current = best_a
                path.append(current)
                changed = True

        candidates_b = [
            evaluate(current.strategy_a, mutant)
            for mutant in _neighbor_strategies(
                current.strategy_b,
                mutation_step,
                max_migration_rate,
                max_phenology_rate,
            )
        ]
        if candidates_b:
            best_b = max(
                candidates_b,
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
            return LandscapeCoevolutionResult(
                path=tuple(path),
                converged=True,
                cycles=cycle,
            )

    return LandscapeCoevolutionResult(
        path=tuple(path),
        converged=False,
        cycles=max_cycles,
    )


def landscape_coordination_barrier_diagnostic(
    scenario: MovingLandscapeScenario,
    *,
    initial_a: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    initial_b: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    mutation_step: float = 0.1,
    max_migration_rate: float = 1.0,
    max_phenology_rate: float = 1.0,
    max_cycles: int = 100,
    matched_migration_points: int | None = None,
    matched_phenology_points: int | None = None,
    gap_tolerance: float = 1e-10,
) -> LandscapeCoordinationBarrier:
    """Compare local unilateral evolution with coordinated matched optimization."""

    if gap_tolerance < 0.0:
        raise ValueError("gap_tolerance must be non-negative")

    local = coevolve_moving_landscape_pair(
        scenario,
        initial_a,
        initial_b,
        mutation_step=mutation_step,
        max_migration_rate=max_migration_rate,
        max_phenology_rate=max_phenology_rate,
        max_cycles=max_cycles,
    )
    if matched_migration_points is None:
        matched_migration_points = (
            int(round(max_migration_rate / mutation_step)) + 1
        )
    if matched_phenology_points is None:
        matched_phenology_points = (
            int(round(max_phenology_rate / mutation_step)) + 1
        )

    matched = optimize_matched_landscape_strategy(
        scenario,
        max_migration_rate=max_migration_rate,
        max_phenology_rate=max_phenology_rate,
        migration_points=matched_migration_points,
        phenology_points=matched_phenology_points,
    )

    gap = max(
        0.0,
        matched.mean_joint_growth
        - local.final.mean_joint_growth,
    )
    return LandscapeCoordinationBarrier(
        local=local,
        matched_optimum=matched,
        accessibility_gap=gap,
        barrier=gap > gap_tolerance,
    )



@dataclass(frozen=True)
class LandscapeLocalCoordinationGate:
    resident: TrackingStrategy
    coordinated_neighbor: TrackingStrategy
    coordinated_gain: float
    unilateral_gain_a: float
    unilateral_gain_b: float
    unilateral_mismatch_a: float
    unilateral_mismatch_b: float
    blocked: bool


def landscape_local_coordination_gate(
    scenario: MovingLandscapeScenario,
    resident: TrackingStrategy,
    *,
    mutation_step: float = 0.1,
    max_migration_rate: float = 1.0,
    max_phenology_rate: float = 1.0,
    tolerance: float = 1e-10,
) -> LandscapeLocalCoordinationGate:
    """Audit whether a beneficial coordinated step is blocked unilaterally.

    Starting from a matched resident pair (resident,resident), enumerate all
    one-step neighboring tracking strategies. For each neighbor compare:

    - the gain if both species move together to the neighbor;
    - the gain to species A if only A moves;
    - the gain to species B if only B moves.

    A local coordination gate is blocked when the best coordinated one-step
    move is beneficial but neither unilateral move is individually beneficial.
    """

    if tolerance < 0.0:
        raise ValueError("tolerance must be non-negative")

    baseline = simulate_moving_landscape_pair(
        resident,
        resident,
        scenario,
    )
    neighbors = _neighbor_strategies(
        resident,
        mutation_step,
        max_migration_rate,
        max_phenology_rate,
    )
    if not neighbors:
        return LandscapeLocalCoordinationGate(
            resident=resident,
            coordinated_neighbor=resident,
            coordinated_gain=0.0,
            unilateral_gain_a=0.0,
            unilateral_gain_b=0.0,
            unilateral_mismatch_a=0.0,
            unilateral_mismatch_b=0.0,
            blocked=False,
        )

    best_neighbor = neighbors[0]
    best_coordinated = simulate_moving_landscape_pair(
        best_neighbor,
        best_neighbor,
        scenario,
    )
    best_gain = (
        best_coordinated.mean_joint_growth
        - baseline.mean_joint_growth
    )

    for neighbor in neighbors[1:]:
        coordinated = simulate_moving_landscape_pair(
            neighbor,
            neighbor,
            scenario,
        )
        gain = (
            coordinated.mean_joint_growth
            - baseline.mean_joint_growth
        )
        if gain > best_gain:
            best_gain = gain
            best_neighbor = neighbor
            best_coordinated = coordinated

    unilateral_a = simulate_moving_landscape_pair(
        best_neighbor,
        resident,
        scenario,
    )
    unilateral_b = simulate_moving_landscape_pair(
        resident,
        best_neighbor,
        scenario,
    )
    gain_a = (
        unilateral_a.mean_log_growth_a
        - baseline.mean_log_growth_a
    )
    gain_b = (
        unilateral_b.mean_log_growth_b
        - baseline.mean_log_growth_b
    )
    blocked = (
        best_gain > tolerance
        and gain_a <= tolerance
        and gain_b <= tolerance
    )

    return LandscapeLocalCoordinationGate(
        resident=resident,
        coordinated_neighbor=best_neighbor,
        coordinated_gain=best_gain,
        unilateral_gain_a=gain_a,
        unilateral_gain_b=gain_b,
        unilateral_mismatch_a=unilateral_a.rms_interaction_mismatch,
        unilateral_mismatch_b=unilateral_b.rms_interaction_mismatch,
        blocked=blocked,
    )
