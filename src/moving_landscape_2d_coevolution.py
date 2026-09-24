"""Coevolutionary accessibility on heterogeneous 2D moving landscapes."""

from __future__ import annotations

from dataclasses import dataclass

from src.moving_climate_landscape_2d import (
    Landscape2DGeometry,
    Landscape2DPairResult,
    MovingLandscape2DScenario,
    build_landscape_2d_geometry,
    optimize_matched_2d_strategy,
    simulate_moving_landscape_2d_pair,
)
from src.spatiotemporal_tracking import TrackingStrategy


@dataclass(frozen=True)
class Landscape2DCoevolutionResult:
    path: tuple[Landscape2DPairResult, ...]
    converged: bool
    cycles: int

    @property
    def final(self) -> Landscape2DPairResult:
        return self.path[-1]


@dataclass(frozen=True)
class Landscape2DCoordinationBarrier:
    local: Landscape2DCoevolutionResult
    matched_optimum: Landscape2DPairResult
    accessibility_gap: float
    barrier: bool
    persistence_rescue: bool


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


def coevolve_moving_landscape_2d_pair(
    scenario: MovingLandscape2DScenario,
    initial_a: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    initial_b: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    *,
    mutation_step: float = 0.2,
    max_migration_rate: float = 1.0,
    max_phenology_rate: float = 1.0,
    max_cycles: int = 60,
    improvement_tolerance: float = 1e-10,
    _geometry: Landscape2DGeometry | None = None,
) -> Landscape2DCoevolutionResult:
    """Alternating strictly improving substitutions in 2D."""

    if max_cycles <= 0:
        raise ValueError("max_cycles must be positive")
    if improvement_tolerance < 0.0:
        raise ValueError("improvement_tolerance must be non-negative")

    geometry = (
        build_landscape_2d_geometry(scenario)
        if _geometry is None
        else _geometry
    )
    cache: dict[
        tuple[float, float, float, float],
        Landscape2DPairResult,
    ] = {}

    def evaluate(
        strategy_a: TrackingStrategy,
        strategy_b: TrackingStrategy,
    ) -> Landscape2DPairResult:
        key = (
            round(strategy_a.migration_rate, 12),
            round(strategy_a.phenology_rate, 12),
            round(strategy_b.migration_rate, 12),
            round(strategy_b.phenology_rate, 12),
        )
        if key not in cache:
            cache[key] = simulate_moving_landscape_2d_pair(
                strategy_a,
                strategy_b,
                scenario,
                _geometry=geometry,
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
            return Landscape2DCoevolutionResult(
                path=tuple(path),
                converged=True,
                cycles=cycle,
            )

    return Landscape2DCoevolutionResult(
        path=tuple(path),
        converged=False,
        cycles=max_cycles,
    )


def landscape_2d_coordination_barrier_diagnostic(
    scenario: MovingLandscape2DScenario,
    *,
    initial_a: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    initial_b: TrackingStrategy = TrackingStrategy(0.0, 0.0),
    mutation_step: float = 0.2,
    max_migration_rate: float = 1.0,
    max_phenology_rate: float = 1.0,
    max_cycles: int = 60,
    matched_migration_points: int | None = None,
    matched_phenology_points: int | None = None,
    gap_tolerance: float = 1e-10,
) -> Landscape2DCoordinationBarrier:
    """Compare local 2D unilateral evolution with coordinated optimization."""

    if gap_tolerance < 0.0:
        raise ValueError("gap_tolerance must be non-negative")

    geometry = build_landscape_2d_geometry(scenario)
    local = coevolve_moving_landscape_2d_pair(
        scenario,
        initial_a,
        initial_b,
        mutation_step=mutation_step,
        max_migration_rate=max_migration_rate,
        max_phenology_rate=max_phenology_rate,
        max_cycles=max_cycles,
        _geometry=geometry,
    )
    if matched_migration_points is None:
        matched_migration_points = (
            int(round(max_migration_rate / mutation_step)) + 1
        )
    if matched_phenology_points is None:
        matched_phenology_points = (
            int(round(max_phenology_rate / mutation_step)) + 1
        )

    matched = optimize_matched_2d_strategy(
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
    return Landscape2DCoordinationBarrier(
        local=local,
        matched_optimum=matched,
        accessibility_gap=gap,
        barrier=gap > gap_tolerance,
        persistence_rescue=(
            (not local.final.joint_persisted)
            and matched.joint_persisted
        ),
    )


@dataclass(frozen=True)
class Landscape2DGateAudit:
    resident: Landscape2DPairResult
    coordinated: Landscape2DPairResult
    unilateral_a: Landscape2DPairResult
    unilateral_b: Landscape2DPairResult
    coordinated_joint_gain: float
    unilateral_gain_a: float
    unilateral_gain_b: float

    @property
    def coordination_gate(self) -> bool:
        return (
            self.coordinated_joint_gain > 0.0
            and self.unilateral_gain_a < 0.0
            and self.unilateral_gain_b < 0.0
        )


def audit_landscape_2d_coordination_gate(
    scenario: MovingLandscape2DScenario,
    resident_strategy: TrackingStrategy,
    coordinated_neighbor: TrackingStrategy,
) -> Landscape2DGateAudit:
    """Audit one coordinated step versus the two corresponding unilateral steps."""

    geometry = build_landscape_2d_geometry(scenario)
    resident = simulate_moving_landscape_2d_pair(
        resident_strategy,
        resident_strategy,
        scenario,
        _geometry=geometry,
    )
    coordinated = simulate_moving_landscape_2d_pair(
        coordinated_neighbor,
        coordinated_neighbor,
        scenario,
        _geometry=geometry,
    )
    unilateral_a = simulate_moving_landscape_2d_pair(
        coordinated_neighbor,
        resident_strategy,
        scenario,
        _geometry=geometry,
    )
    unilateral_b = simulate_moving_landscape_2d_pair(
        resident_strategy,
        coordinated_neighbor,
        scenario,
        _geometry=geometry,
    )

    return Landscape2DGateAudit(
        resident=resident,
        coordinated=coordinated,
        unilateral_a=unilateral_a,
        unilateral_b=unilateral_b,
        coordinated_joint_gain=(
            coordinated.mean_joint_growth
            - resident.mean_joint_growth
        ),
        unilateral_gain_a=(
            unilateral_a.mean_log_growth_a
            - resident.mean_log_growth_a
        ),
        unilateral_gain_b=(
            unilateral_b.mean_log_growth_b
            - resident.mean_log_growth_b
        ),
    )
