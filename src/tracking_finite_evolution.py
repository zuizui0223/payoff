"""Finite-population weak-mutation evolution on the tracking strategy lattice.

This layer separates deterministic accessibility from finite-N substitution.
Populations are monomorphic between mutation events. A proposed one-step
migration/phenology mutant fixes according to the exact Moran probability for
frequency-independent relative fitness

    r = exp(beta * (g_mutant - g_resident)).

For symmetric mutation proposals, the exact weak-mutation stationary law on
the connected strategy lattice is

    Pi_i proportional to exp[beta * (N-1) * g_i].
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, expm1, isfinite, log
from random import Random
from typing import Sequence

from src.spatiotemporal_tracking import (
    TrackingScenario,
    TrackingSimulationResult,
)
from src.tracking_mutation_selection import (
    StrategyLattice,
    tracking_growth_landscape,
)


@dataclass(frozen=True)
class FiniteEvolutionResult:
    lattice: StrategyLattice
    landscape: tuple[TrackingSimulationResult, ...]
    state_path: tuple[int, ...]
    accepted_substitutions: int
    mutation_proposals: int

    @property
    def final_index(self) -> int:
        return self.state_path[-1]

    @property
    def final(self) -> TrackingSimulationResult:
        return self.landscape[self.final_index]

    def empirical_occupancy(self) -> tuple[float, ...]:
        counts = [0] * self.lattice.size
        for index in self.state_path:
            counts[index] += 1
        total = len(self.state_path)
        return tuple(count / total for count in counts)


def moran_fixation_probability_from_growth_difference(
    growth_difference: float,
    population_size: int,
    selection_strength: float,
) -> float:
    """Exact one-mutant Moran fixation probability under constant fitness."""

    if population_size < 2:
        raise ValueError("population_size must be at least 2")
    if selection_strength < 0.0 or not isfinite(selection_strength):
        raise ValueError(
            "selection_strength must be non-negative and finite"
        )
    if not isfinite(growth_difference):
        raise ValueError("growth_difference must be finite")

    s = selection_strength * growth_difference
    if abs(s) < 1e-12:
        return 1.0 / population_size

    if s > 0.0:
        numerator = -expm1(-s)
        denominator = -expm1(-population_size * s)
        return numerator / denominator

    # Algebraically identical to
    # (1-exp(-s))/(1-exp(-N*s)), but stable for negative s.
    numerator = exp((population_size - 1) * s) * expm1(s)
    denominator = expm1(population_size * s)
    if denominator == 0.0:
        return 1.0 / population_size
    return numerator / denominator


def weak_mutation_stationary_distribution(
    growth_values: Sequence[float],
    population_size: int,
    selection_strength: float,
) -> tuple[float, ...]:
    """Exact stationary law for symmetric mutation on a connected lattice."""

    if not growth_values:
        raise ValueError("growth_values cannot be empty")
    if population_size < 2:
        raise ValueError("population_size must be at least 2")
    if selection_strength < 0.0:
        raise ValueError("selection_strength must be non-negative")
    if any(not isfinite(value) for value in growth_values):
        raise ValueError("growth_values must be finite")

    scale = selection_strength * (population_size - 1)
    logs = [scale * value for value in growth_values]
    maximum = max(logs)
    weights = [exp(value - maximum) for value in logs]
    total = sum(weights)
    return tuple(weight / total for weight in weights)


def simulate_finite_tracking_evolution(
    scenario: TrackingScenario,
    lattice: StrategyLattice = StrategyLattice(),
    *,
    population_size: int = 100,
    selection_strength: float = 10.0,
    mutation_events: int = 10_000,
    seed: int = 20260920,
    initial_index: int | None = None,
) -> FiniteEvolutionResult:
    """Simulate a monomorphic weak-mutation substitution chain."""

    if population_size < 2:
        raise ValueError("population_size must be at least 2")
    if selection_strength < 0.0:
        raise ValueError("selection_strength must be non-negative")
    if mutation_events <= 0:
        raise ValueError("mutation_events must be positive")

    landscape = tracking_growth_landscape(scenario, lattice)
    growth = tuple(item.mean_log_growth for item in landscape)

    if initial_index is None:
        initial_index = lattice.index(0, 0)
    if not 0 <= initial_index < lattice.size:
        raise ValueError("initial_index out of bounds")

    rng = Random(seed)
    resident = initial_index
    path = [resident]
    accepted = 0

    for _ in range(mutation_events):
        neighbors = lattice.axial_neighbors(resident)
        if not neighbors:
            raise RuntimeError("strategy lattice contains isolated state")
        mutant = neighbors[rng.randrange(len(neighbors))]
        fixation = moran_fixation_probability_from_growth_difference(
            growth[mutant] - growth[resident],
            population_size,
            selection_strength,
        )
        if rng.random() < fixation:
            resident = mutant
            accepted += 1
        path.append(resident)

    return FiniteEvolutionResult(
        lattice=lattice,
        landscape=landscape,
        state_path=tuple(path),
        accepted_substitutions=accepted,
        mutation_proposals=mutation_events,
    )



def finite_stationary_tracking_summary(
    scenario: TrackingScenario,
    lattice: StrategyLattice = StrategyLattice(),
    *,
    population_size: int = 100,
    selection_strength: float = 10.0,
) -> dict[str, float | str | int]:
    """Summarize exact weak-mutation occupancy on the tracking lattice."""

    landscape = tracking_growth_landscape(scenario, lattice)
    growth = tuple(item.mean_log_growth for item in landscape)
    probabilities = weak_mutation_stationary_distribution(
        growth,
        population_size,
        selection_strength,
    )

    mean_migration = sum(
        probability * item.strategy.migration_rate
        for probability, item in zip(probabilities, landscape)
    )
    mean_phenology = sum(
        probability * item.strategy.phenology_rate
        for probability, item in zip(probabilities, landscape)
    )
    total_rate = mean_migration + mean_phenology
    mean_share = (
        mean_migration / total_rate if total_rate > 0.0 else 0.5
    )

    entropy = -sum(
        probability * log(probability)
        for probability in probabilities
        if probability > 0.0
    )
    top_index = max(
        range(len(probabilities)),
        key=probabilities.__getitem__,
    )
    top = landscape[top_index]
    outcome_mass: dict[str, float] = {}
    for probability, item in zip(probabilities, landscape):
        outcome_mass[item.outcome] = (
            outcome_mass.get(item.outcome, 0.0)
            + probability
        )

    return {
        "population_size": population_size,
        "selection_strength": selection_strength,
        "mean_migration_rate": mean_migration,
        "mean_phenology_rate": mean_phenology,
        "mean_migration_share": mean_share,
        "entropy": entropy,
        "effective_strategy_count": exp(entropy),
        "top_probability": probabilities[top_index],
        "top_migration_rate": top.strategy.migration_rate,
        "top_phenology_rate": top.strategy.phenology_rate,
        "top_outcome": top.outcome,
        "interaction_failure_mass": outcome_mass.get(
            "interaction_failure", 0.0
        ),
        "failure_mass": outcome_mass.get("failure", 0.0),
    }
