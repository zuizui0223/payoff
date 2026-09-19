"""Stochastic integer metapopulation on the moving-climate landscape.

The deterministic moving-landscape model produces expected abundance after
local density-regulated reproduction and dispersal. This layer samples each
destination patch from a Poisson distribution with that expectation, creating
explicit local demographic noise while preserving the same low-density fitness,
tracking geometry, dispersal, and boundary conditions.

The simulation stops at the first species extinction because post-partner-loss
fitness is not yet specified in the interaction model.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from statistics import mean, pstdev

from src.moving_climate_landscape import (
    MovingLandscapeScenario,
    _one_species_generation,
    _update_phenology,
    gaussian_initial_distribution,
    spatial_centroid,
)
from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_population import poisson_sample


@dataclass(frozen=True)
class StochasticLandscapeResult:
    strategy_a: TrackingStrategy
    strategy_b: TrackingStrategy
    seed: int
    joint_persisted: bool
    first_extinction_step: int | None
    extinct_species: str | None
    final_abundance_a: int
    final_abundance_b: int
    minimum_abundance_a: int
    minimum_abundance_b: int
    mean_abundance_a: float
    mean_abundance_b: float
    mean_low_density_growth_a: float
    mean_low_density_growth_b: float
    mean_realized_growth_a: float
    mean_realized_growth_b: float
    mean_interaction_mismatch: float
    mean_centroid_gap: float
    mean_phenology_gap: float


@dataclass(frozen=True)
class StochasticLandscapeEnsemble:
    replicates: tuple[StochasticLandscapeResult, ...]

    def summary(self) -> dict[str, float | int]:
        if not self.replicates:
            raise ValueError("replicates cannot be empty")
        persistence = [
            row.joint_persisted for row in self.replicates
        ]
        final_a = [
            row.final_abundance_a for row in self.replicates
        ]
        final_b = [
            row.final_abundance_b for row in self.replicates
        ]
        extinction_steps = [
            row.first_extinction_step
            for row in self.replicates
            if row.first_extinction_step is not None
        ]
        return {
            "replicates": len(self.replicates),
            "joint_persistence_fraction": (
                sum(persistence) / len(persistence)
            ),
            "joint_extinction_fraction": (
                1.0 - sum(persistence) / len(persistence)
            ),
            "mean_final_abundance_a": mean(final_a),
            "mean_final_abundance_b": mean(final_b),
            "sd_final_abundance_a": (
                pstdev(final_a) if len(final_a) > 1 else 0.0
            ),
            "sd_final_abundance_b": (
                pstdev(final_b) if len(final_b) > 1 else 0.0
            ),
            "mean_minimum_abundance_a": mean(
                row.minimum_abundance_a
                for row in self.replicates
            ),
            "mean_minimum_abundance_b": mean(
                row.minimum_abundance_b
                for row in self.replicates
            ),
            "mean_low_density_growth_a": mean(
                row.mean_low_density_growth_a
                for row in self.replicates
            ),
            "mean_low_density_growth_b": mean(
                row.mean_low_density_growth_b
                for row in self.replicates
            ),
            "mean_interaction_mismatch": mean(
                row.mean_interaction_mismatch
                for row in self.replicates
            ),
            "mean_extinction_step_conditional": (
                mean(extinction_steps)
                if extinction_steps
                else float("nan")
            ),
        }


def _integer_initial_distribution(
    scenario: MovingLandscapeScenario,
    rng: Random,
) -> tuple[int, ...]:
    """Poisson-sample the declared Gaussian initial abundance profile."""

    expected = gaussian_initial_distribution(scenario)
    return tuple(
        poisson_sample(value, rng)
        for value in expected
    )


def _poisson_patch_sample(
    expected: tuple[float, ...],
    rng: Random,
) -> tuple[int, ...]:
    return tuple(
        poisson_sample(max(0.0, value), rng)
        for value in expected
    )


def simulate_stochastic_moving_landscape_pair(
    strategy_a: TrackingStrategy,
    strategy_b: TrackingStrategy,
    scenario: MovingLandscapeScenario,
    *,
    seed: int,
) -> StochasticLandscapeResult:
    """Simulate one stochastic two-species patch realization."""

    rng_a = Random(seed + 11_000_003)
    rng_b = Random(seed + 29_000_011)
    abundance_a = _integer_initial_distribution(
        scenario,
        rng_a,
    )
    abundance_b = _integer_initial_distribution(
        scenario,
        rng_b,
    )

    total_a = sum(abundance_a)
    total_b = sum(abundance_b)
    minimum_a = total_a
    minimum_b = total_b

    if total_a <= 0:
        return StochasticLandscapeResult(
            strategy_a=strategy_a,
            strategy_b=strategy_b,
            seed=seed,
            joint_persisted=False,
            first_extinction_step=0,
            extinct_species="A",
            final_abundance_a=0,
            final_abundance_b=total_b,
            minimum_abundance_a=0,
            minimum_abundance_b=total_b,
            mean_abundance_a=0.0,
            mean_abundance_b=float(total_b),
            mean_low_density_growth_a=0.0,
            mean_low_density_growth_b=0.0,
            mean_realized_growth_a=0.0,
            mean_realized_growth_b=0.0,
            mean_interaction_mismatch=0.0,
            mean_centroid_gap=0.0,
            mean_phenology_gap=0.0,
        )
    if total_b <= 0:
        return StochasticLandscapeResult(
            strategy_a=strategy_a,
            strategy_b=strategy_b,
            seed=seed,
            joint_persisted=False,
            first_extinction_step=0,
            extinct_species="B",
            final_abundance_a=total_a,
            final_abundance_b=0,
            minimum_abundance_a=total_a,
            minimum_abundance_b=0,
            mean_abundance_a=float(total_a),
            mean_abundance_b=0.0,
            mean_low_density_growth_a=0.0,
            mean_low_density_growth_b=0.0,
            mean_realized_growth_a=0.0,
            mean_realized_growth_b=0.0,
            mean_interaction_mismatch=0.0,
            mean_centroid_gap=0.0,
            mean_phenology_gap=0.0,
        )

    phenology_a = 0.0
    phenology_b = 0.0
    abundance_sum_a = 0.0
    abundance_sum_b = 0.0
    low_growth_sum_a = 0.0
    low_growth_sum_b = 0.0
    realized_growth_sum_a = 0.0
    realized_growth_sum_b = 0.0
    interaction_sum = 0.0
    centroid_gap_sum = 0.0
    phenology_gap_sum = 0.0
    observed = 0

    for step in range(1, scenario.steps + 1):
        demand = scenario.climate_velocity * step

        phenology_a, _ = _update_phenology(
            tuple(float(value) for value in abundance_a),
            strategy_a,
            phenology_a,
            demand,
            scenario,
        )
        phenology_b, _ = _update_phenology(
            tuple(float(value) for value in abundance_b),
            strategy_b,
            phenology_b,
            demand,
            scenario,
        )

        centroid_a = spatial_centroid(
            abundance_a,
            scenario.positions,
        )
        centroid_b = spatial_centroid(
            abundance_b,
            scenario.positions,
        )
        climate_centroid_gap = (
            scenario.spatial_gradient
            * (centroid_a - centroid_b)
        )
        climate_phenology_gap = (
            scenario.phenology_scale
            * (phenology_a - phenology_b)
        )
        interaction_sq = (
            climate_centroid_gap * climate_centroid_gap
            + climate_phenology_gap * climate_phenology_gap
        )

        expected_a, low_a, realized_a = _one_species_generation(
            tuple(float(value) for value in abundance_a),
            strategy_a,
            scenario.species_a,
            phenology_a,
            demand,
            interaction_sq,
            scenario,
        )
        expected_b, low_b, realized_b = _one_species_generation(
            tuple(float(value) for value in abundance_b),
            strategy_b,
            scenario.species_b,
            phenology_b,
            demand,
            interaction_sq,
            scenario,
        )

        abundance_a = _poisson_patch_sample(
            expected_a,
            rng_a,
        )
        abundance_b = _poisson_patch_sample(
            expected_b,
            rng_b,
        )
        total_a = sum(abundance_a)
        total_b = sum(abundance_b)
        minimum_a = min(minimum_a, total_a)
        minimum_b = min(minimum_b, total_b)

        if step > scenario.burn_in:
            observed += 1
            abundance_sum_a += total_a
            abundance_sum_b += total_b
            low_growth_sum_a += low_a
            low_growth_sum_b += low_b
            realized_growth_sum_a += realized_a
            realized_growth_sum_b += realized_b
            interaction_sum += interaction_sq ** 0.5
            centroid_gap_sum += abs(climate_centroid_gap)
            phenology_gap_sum += abs(climate_phenology_gap)

        if (
            total_a <= scenario.extinction_threshold
            or total_b <= scenario.extinction_threshold
        ):
            if total_a <= scenario.extinction_threshold:
                abundance_a = tuple(0 for _ in abundance_a)
                total_a = 0
            if total_b <= scenario.extinction_threshold:
                abundance_b = tuple(0 for _ in abundance_b)
                total_b = 0
            if total_a == 0 and total_b == 0:
                extinct_species = "both"
            elif total_a == 0:
                extinct_species = "A"
            else:
                extinct_species = "B"

            divisor = max(1, observed)
            return StochasticLandscapeResult(
                strategy_a=strategy_a,
                strategy_b=strategy_b,
                seed=seed,
                joint_persisted=False,
                first_extinction_step=step,
                extinct_species=extinct_species,
                final_abundance_a=total_a,
                final_abundance_b=total_b,
                minimum_abundance_a=minimum_a,
                minimum_abundance_b=minimum_b,
                mean_abundance_a=abundance_sum_a / divisor,
                mean_abundance_b=abundance_sum_b / divisor,
                mean_low_density_growth_a=(
                    low_growth_sum_a / divisor
                ),
                mean_low_density_growth_b=(
                    low_growth_sum_b / divisor
                ),
                mean_realized_growth_a=(
                    realized_growth_sum_a / divisor
                ),
                mean_realized_growth_b=(
                    realized_growth_sum_b / divisor
                ),
                mean_interaction_mismatch=(
                    interaction_sum / divisor
                ),
                mean_centroid_gap=(
                    centroid_gap_sum / divisor
                ),
                mean_phenology_gap=(
                    phenology_gap_sum / divisor
                ),
            )

    divisor = max(1, observed)
    return StochasticLandscapeResult(
        strategy_a=strategy_a,
        strategy_b=strategy_b,
        seed=seed,
        joint_persisted=True,
        first_extinction_step=None,
        extinct_species=None,
        final_abundance_a=total_a,
        final_abundance_b=total_b,
        minimum_abundance_a=minimum_a,
        minimum_abundance_b=minimum_b,
        mean_abundance_a=abundance_sum_a / divisor,
        mean_abundance_b=abundance_sum_b / divisor,
        mean_low_density_growth_a=(
            low_growth_sum_a / divisor
        ),
        mean_low_density_growth_b=(
            low_growth_sum_b / divisor
        ),
        mean_realized_growth_a=(
            realized_growth_sum_a / divisor
        ),
        mean_realized_growth_b=(
            realized_growth_sum_b / divisor
        ),
        mean_interaction_mismatch=(
            interaction_sum / divisor
        ),
        mean_centroid_gap=centroid_gap_sum / divisor,
        mean_phenology_gap=phenology_gap_sum / divisor,
    )


def stochastic_moving_landscape_ensemble(
    strategy_a: TrackingStrategy,
    strategy_b: TrackingStrategy,
    scenario: MovingLandscapeScenario,
    *,
    replicates: int,
    seed: int,
) -> StochasticLandscapeEnsemble:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    rows = tuple(
        simulate_stochastic_moving_landscape_pair(
            strategy_a,
            strategy_b,
            scenario,
            seed=seed + replicate * 1_000_003,
        )
        for replicate in range(replicates)
    )
    return StochasticLandscapeEnsemble(
        replicates=rows,
    )
