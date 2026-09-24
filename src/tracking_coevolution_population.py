"""Population consequences of migration--phenology coevolution.

This module couples the two-species tracking geometry to integer demographic
dynamics. It is designed to compare a locally accessible coevolution endpoint
with the coordinated matched optimum under the same demographic design.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp
from random import Random
from statistics import mean

from src.tracking_coevolution import (
    CoevolutionScenario,
    PairSimulationResult,
    coordination_barrier_diagnostic,
    _architecture_cost,
    _step_tracking,
)
from src.tracking_population import (
    PopulationDynamics,
    poisson_sample,
)
from src.spatiotemporal_tracking import TrackingStrategy


@dataclass(frozen=True)
class PairPopulationResult:
    strategy_a: TrackingStrategy
    strategy_b: TrackingStrategy
    seed: int
    joint_persisted: bool
    first_extinction_step: int | None
    extinct_species: str | None
    final_population_a: int
    final_population_b: int
    minimum_population_a: int
    minimum_population_b: int


@dataclass(frozen=True)
class PairPopulationEnsemble:
    replicates: tuple[PairPopulationResult, ...]

    def summary(self) -> dict[str, float | int]:
        extinction_steps = [
            row.first_extinction_step
            for row in self.replicates
            if row.first_extinction_step is not None
        ]
        return {
            "replicates": len(self.replicates),
            "joint_persistence_fraction": (
                sum(row.joint_persisted for row in self.replicates)
                / len(self.replicates)
            ),
            "joint_extinction_fraction": (
                sum(not row.joint_persisted for row in self.replicates)
                / len(self.replicates)
            ),
            "mean_final_population_a": mean(
                row.final_population_a
                for row in self.replicates
            ),
            "mean_final_population_b": mean(
                row.final_population_b
                for row in self.replicates
            ),
            "mean_minimum_population_a": mean(
                row.minimum_population_a
                for row in self.replicates
            ),
            "mean_minimum_population_b": mean(
                row.minimum_population_b
                for row in self.replicates
            ),
            "mean_first_extinction_step_conditional": (
                mean(extinction_steps)
                if extinction_steps
                else float("nan")
            ),
        }


@dataclass(frozen=True)
class BarrierPopulationConsequence:
    accessibility_gap: float
    barrier: bool
    local_endpoint: PairSimulationResult
    matched_optimum: PairSimulationResult
    local_population: PairPopulationEnsemble
    matched_population: PairPopulationEnsemble

    @property
    def persistence_gain(self) -> float:
        return (
            float(
                self.matched_population.summary()[
                    "joint_persistence_fraction"
                ]
            )
            - float(
                self.local_population.summary()[
                    "joint_persistence_fraction"
                ]
            )
        )


def simulate_pair_population(
    strategy_a: TrackingStrategy,
    strategy_b: TrackingStrategy,
    scenario: CoevolutionScenario,
    population_a: PopulationDynamics,
    population_b: PopulationDynamics,
    *,
    seed: int,
) -> PairPopulationResult:
    """Simulate joint persistence until either interacting population is lost.

    The low-density growth terms are exactly those used by the deterministic
    coevolution model. Density regulation is species-specific. The simulation
    stops at the first extinction because the current interaction model does
    not yet specify post-partner-loss growth.
    """

    rng_a = Random(seed + 11_000_003)
    rng_b = Random(seed + 29_000_011)

    abundance_a = population_a.initial_population
    abundance_b = population_b.initial_population
    minimum_a = abundance_a
    minimum_b = abundance_b

    if abundance_a <= population_a.extinction_threshold:
        return PairPopulationResult(
            strategy_a=strategy_a,
            strategy_b=strategy_b,
            seed=seed,
            joint_persisted=False,
            first_extinction_step=0,
            extinct_species="A",
            final_population_a=0,
            final_population_b=abundance_b,
            minimum_population_a=0,
            minimum_population_b=abundance_b,
        )
    if abundance_b <= population_b.extinction_threshold:
        return PairPopulationResult(
            strategy_a=strategy_a,
            strategy_b=strategy_b,
            seed=seed,
            joint_persisted=False,
            first_extinction_step=0,
            extinct_species="B",
            final_population_a=abundance_a,
            final_population_b=0,
            minimum_population_a=abundance_a,
            minimum_population_b=0,
        )

    x_a = z_a = x_b = z_b = 0.0
    cost_a = _architecture_cost(
        strategy_a,
        scenario.species_a,
    )
    cost_b = _architecture_cost(
        strategy_b,
        scenario.species_b,
    )

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
        phenology_gap = scenario.phenology_scale * (
            z_a - z_b
        )
        interaction_sq = (
            spatial_gap * spatial_gap
            + phenology_gap * phenology_gap
        )

        low_density_a = (
            scenario.species_a.baseline_growth
            - cost_a
            - 0.5
            * scenario.species_a.abiotic_strength
            * mismatch_a
            * mismatch_a
            - 0.5
            * scenario.species_a.interaction_strength
            * interaction_sq
        )
        low_density_b = (
            scenario.species_b.baseline_growth
            - cost_b
            - 0.5
            * scenario.species_b.abiotic_strength
            * mismatch_b
            * mismatch_b
            - 0.5
            * scenario.species_b.interaction_strength
            * interaction_sq
        )

        realized_a = (
            low_density_a
            - population_a.density_coefficient
            * abundance_a
            / population_a.carrying_capacity
        )
        realized_b = (
            low_density_b
            - population_b.density_coefficient
            * abundance_b
            / population_b.carrying_capacity
        )

        abundance_a = poisson_sample(
            abundance_a * exp(realized_a),
            rng_a,
        )
        abundance_b = poisson_sample(
            abundance_b * exp(realized_b),
            rng_b,
        )
        if abundance_a <= population_a.extinction_threshold:
            abundance_a = 0
        if abundance_b <= population_b.extinction_threshold:
            abundance_b = 0

        minimum_a = min(minimum_a, abundance_a)
        minimum_b = min(minimum_b, abundance_b)

        if abundance_a == 0 or abundance_b == 0:
            if abundance_a == 0 and abundance_b == 0:
                extinct_species = "both"
            elif abundance_a == 0:
                extinct_species = "A"
            else:
                extinct_species = "B"
            return PairPopulationResult(
                strategy_a=strategy_a,
                strategy_b=strategy_b,
                seed=seed,
                joint_persisted=False,
                first_extinction_step=step,
                extinct_species=extinct_species,
                final_population_a=abundance_a,
                final_population_b=abundance_b,
                minimum_population_a=minimum_a,
                minimum_population_b=minimum_b,
            )

    return PairPopulationResult(
        strategy_a=strategy_a,
        strategy_b=strategy_b,
        seed=seed,
        joint_persisted=True,
        first_extinction_step=None,
        extinct_species=None,
        final_population_a=abundance_a,
        final_population_b=abundance_b,
        minimum_population_a=minimum_a,
        minimum_population_b=minimum_b,
    )


def pair_population_ensemble(
    strategy_a: TrackingStrategy,
    strategy_b: TrackingStrategy,
    scenario: CoevolutionScenario,
    population_a: PopulationDynamics,
    population_b: PopulationDynamics,
    *,
    replicates: int,
    seed: int,
) -> PairPopulationEnsemble:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    rows = tuple(
        simulate_pair_population(
            strategy_a,
            strategy_b,
            scenario,
            population_a,
            population_b,
            seed=seed + replicate * 1_000_003,
        )
        for replicate in range(replicates)
    )
    return PairPopulationEnsemble(replicates=rows)


def coordination_barrier_population_consequence(
    scenario: CoevolutionScenario,
    population_a: PopulationDynamics,
    population_b: PopulationDynamics,
    *,
    replicates: int,
    seed: int,
    mutation_step: float = 0.1,
    max_rate: float = 1.5,
    max_cycles: int = 100,
) -> BarrierPopulationConsequence:
    """Compare demographic persistence of local versus coordinated solutions."""

    diagnostic = coordination_barrier_diagnostic(
        scenario,
        mutation_step=mutation_step,
        max_rate=max_rate,
        max_cycles=max_cycles,
    )
    local = diagnostic.local.final
    matched = diagnostic.matched_optimum

    local_population = pair_population_ensemble(
        local.strategy_a,
        local.strategy_b,
        scenario,
        population_a,
        population_b,
        replicates=replicates,
        seed=seed,
    )
    matched_population = pair_population_ensemble(
        matched.strategy_a,
        matched.strategy_b,
        scenario,
        population_a,
        population_b,
        replicates=replicates,
        seed=seed,
    )

    return BarrierPopulationConsequence(
        accessibility_gap=diagnostic.accessibility_gap,
        barrier=diagnostic.barrier,
        local_endpoint=local,
        matched_optimum=matched,
        local_population=local_population,
        matched_population=matched_population,
    )
