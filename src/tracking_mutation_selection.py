"""Mutation-selection occupancy on the migration--phenology strategy lattice.

The v0.1 tracking model returns the payoff of one fixed heritable strategy.
This module promotes that landscape to a population-level distribution using a
replicator-mutator map.

Mutation proposals are symmetric on the four axial lattice directions. Invalid
boundary proposals remain at the parental state, which makes the neutral
mutation kernel doubly stochastic and therefore gives an exact uniform neutral
stationary distribution.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log
from typing import Sequence

from src.spatiotemporal_tracking import (
    TrackingScenario,
    TrackingSimulationResult,
    TrackingStrategy,
    simulate_tracking,
)


@dataclass(frozen=True)
class StrategyLattice:
    max_rate: float = 1.5
    points: int = 31

    def __post_init__(self) -> None:
        if self.max_rate <= 0.0:
            raise ValueError("max_rate must be positive")
        if self.points < 2:
            raise ValueError("points must be at least 2")

    @property
    def step(self) -> float:
        return self.max_rate / (self.points - 1)

    @property
    def size(self) -> int:
        return self.points * self.points

    def strategy(self, migration_index: int, phenology_index: int) -> TrackingStrategy:
        self._validate_coordinate(migration_index, phenology_index)
        return TrackingStrategy(
            migration_index * self.step,
            phenology_index * self.step,
        )

    def index(self, migration_index: int, phenology_index: int) -> int:
        self._validate_coordinate(migration_index, phenology_index)
        return migration_index * self.points + phenology_index

    def coordinate(self, index: int) -> tuple[int, int]:
        if not 0 <= index < self.size:
            raise ValueError("strategy index out of bounds")
        return divmod(index, self.points)

    def strategies(self) -> tuple[TrackingStrategy, ...]:
        return tuple(
            self.strategy(i, j)
            for i in range(self.points)
            for j in range(self.points)
        )

    def axial_neighbors(self, index: int) -> tuple[int, ...]:
        i, j = self.coordinate(index)
        neighbors: list[int] = []
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ii = i + di
            jj = j + dj
            if 0 <= ii < self.points and 0 <= jj < self.points:
                neighbors.append(self.index(ii, jj))
        return tuple(neighbors)

    def _validate_coordinate(self, i: int, j: int) -> None:
        if not (0 <= i < self.points and 0 <= j < self.points):
            raise ValueError("lattice coordinate out of bounds")


@dataclass(frozen=True)
class OccupancyResult:
    lattice: StrategyLattice
    probabilities: tuple[float, ...]
    landscape: tuple[TrackingSimulationResult, ...]
    iterations: int
    converged: bool
    l1_residual: float

    def summary(self) -> dict[str, float | str | int | bool]:
        probs = self.probabilities
        strategies = tuple(item.strategy for item in self.landscape)
        mean_migration = sum(
            p * strategy.migration_rate
            for p, strategy in zip(probs, strategies)
        )
        mean_phenology = sum(
            p * strategy.phenology_rate
            for p, strategy in zip(probs, strategies)
        )
        mean_total = mean_migration + mean_phenology
        mean_share = (
            mean_migration / mean_total if mean_total > 0.0 else 0.5
        )
        mean_growth = sum(
            p * item.mean_log_growth
            for p, item in zip(probs, self.landscape)
        )
        mean_abiotic_growth = sum(
            p * item.abiotic_only_mean_log_growth
            for p, item in zip(probs, self.landscape)
        )
        entropy = -sum(p * log(p) for p in probs if p > 0.0)
        top_index = max(range(len(probs)), key=probs.__getitem__)
        top = self.landscape[top_index]
        outcome_mass: dict[str, float] = {}
        for probability, item in zip(probs, self.landscape):
            outcome_mass[item.outcome] = (
                outcome_mass.get(item.outcome, 0.0) + probability
            )
        dominant_outcome = max(
            outcome_mass, key=outcome_mass.__getitem__
        )
        return {
            "mean_migration_rate": mean_migration,
            "mean_phenology_rate": mean_phenology,
            "mean_migration_share": mean_share,
            "mean_log_growth": mean_growth,
            "mean_abiotic_only_log_growth": mean_abiotic_growth,
            "entropy": entropy,
            "effective_strategy_count": exp(entropy),
            "top_probability": probs[top_index],
            "top_migration_rate": top.strategy.migration_rate,
            "top_phenology_rate": top.strategy.phenology_rate,
            "top_outcome": top.outcome,
            "dominant_outcome_mass": dominant_outcome,
            "interaction_failure_mass": outcome_mass.get(
                "interaction_failure", 0.0
            ),
            "failure_mass": outcome_mass.get("failure", 0.0),
            "iterations": self.iterations,
            "converged": self.converged,
            "l1_residual": self.l1_residual,
        }


def tracking_growth_landscape(
    scenario: TrackingScenario,
    lattice: StrategyLattice,
) -> tuple[TrackingSimulationResult, ...]:
    return tuple(
        simulate_tracking(strategy, scenario)
        for strategy in lattice.strategies()
    )


def symmetric_mutation_step(
    probabilities: Sequence[float],
    lattice: StrategyLattice,
    mutation_rate: float,
) -> tuple[float, ...]:
    """Apply symmetric axial mutation.

    Each of the four directional proposals has probability mutation_rate/4.
    Boundary proposals that would leave the lattice stay in the parental state.
    """

    _validate_probabilities(probabilities, lattice.size)
    if not 0.0 <= mutation_rate <= 1.0:
        raise ValueError("mutation_rate must lie in [0, 1]")

    proposal = mutation_rate / 4.0
    out = [0.0] * lattice.size
    for index, mass in enumerate(probabilities):
        neighbors = lattice.axial_neighbors(index)
        moved = proposal * len(neighbors)
        out[index] += mass * (1.0 - moved)
        for neighbor in neighbors:
            out[neighbor] += mass * proposal
    return tuple(out)


def replicator_mutator_step(
    probabilities: Sequence[float],
    growth_values: Sequence[float],
    lattice: StrategyLattice,
    *,
    selection_strength: float,
    mutation_rate: float,
) -> tuple[float, ...]:
    """One selection-then-mutation generation."""

    _validate_probabilities(probabilities, lattice.size)
    if len(growth_values) != lattice.size:
        raise ValueError("growth_values length must equal lattice size")
    if selection_strength < 0.0:
        raise ValueError("selection_strength must be non-negative")

    max_growth = max(growth_values)
    weighted = [
        p * exp(selection_strength * (growth - max_growth))
        for p, growth in zip(probabilities, growth_values)
    ]
    total = sum(weighted)
    if total <= 0.0:
        raise ValueError("selected population has non-positive total mass")
    selected = tuple(value / total for value in weighted)
    return symmetric_mutation_step(
        selected, lattice, mutation_rate
    )


def stationary_tracking_occupancy(
    scenario: TrackingScenario,
    lattice: StrategyLattice = StrategyLattice(),
    *,
    selection_strength: float = 20.0,
    mutation_rate: float = 0.02,
    tolerance: float = 1e-12,
    max_iterations: int = 100_000,
    initial_probabilities: Sequence[float] | None = None,
) -> OccupancyResult:
    """Iterate the replicator-mutator map to stationary occupancy."""

    if selection_strength < 0.0:
        raise ValueError("selection_strength must be non-negative")
    if not 0.0 < mutation_rate < 1.0:
        raise ValueError(
            "stationary occupancy requires 0 < mutation_rate < 1"
        )
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")

    landscape = tracking_growth_landscape(scenario, lattice)
    growth = tuple(item.mean_log_growth for item in landscape)

    if initial_probabilities is None:
        probabilities = tuple(
            1.0 / lattice.size for _ in range(lattice.size)
        )
    else:
        _validate_probabilities(
            initial_probabilities, lattice.size
        )
        total = sum(initial_probabilities)
        probabilities = tuple(
            value / total for value in initial_probabilities
        )

    residual = float("inf")
    for iteration in range(1, max_iterations + 1):
        updated = replicator_mutator_step(
            probabilities,
            growth,
            lattice,
            selection_strength=selection_strength,
            mutation_rate=mutation_rate,
        )
        residual = sum(
            abs(a - b)
            for a, b in zip(probabilities, updated)
        )
        probabilities = updated
        if residual <= tolerance:
            return OccupancyResult(
                lattice=lattice,
                probabilities=probabilities,
                landscape=landscape,
                iterations=iteration,
                converged=True,
                l1_residual=residual,
            )

    return OccupancyResult(
        lattice=lattice,
        probabilities=probabilities,
        landscape=landscape,
        iterations=max_iterations,
        converged=False,
        l1_residual=residual,
    )


def _validate_probabilities(
    probabilities: Sequence[float],
    expected_length: int,
) -> None:
    if len(probabilities) != expected_length:
        raise ValueError(
            "probability vector length must equal lattice size"
        )
    if any(value < 0.0 for value in probabilities):
        raise ValueError("probabilities must be non-negative")
    if sum(probabilities) <= 0.0:
        raise ValueError("probabilities must have positive mass")
