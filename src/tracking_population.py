"""Density-regulated demographic dynamics for migration--phenology tracking.

The existing tracking modules produce per-generation low-density Malthusian
growth. This module transports that quantity into integer population dynamics:

    E[N_(t+1) | N_t]
    = N_t * exp(g_t - d * N_t / K)

followed by Poisson demographic sampling. Population size zero is absorbing.

The default density coefficient can be chosen equal to baseline low-density
growth so that a perfectly matched zero-cost strategy has deterministic
equilibrium near K.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, expm1, floor, lgamma, log, sqrt
from random import Random
from statistics import mean, median, pstdev

from src.spatiotemporal_tracking import (
    TrackingScenario,
    TrackingStrategy,
)
from src.stochastic_tracking import StochasticForcing


_EPS = 1e-12


@dataclass(frozen=True)
class PopulationDynamics:
    initial_population: int = 250
    carrying_capacity: float = 500.0
    density_coefficient: float = 0.2
    extinction_threshold: int = 0

    def __post_init__(self) -> None:
        if self.initial_population < 0:
            raise ValueError("initial_population must be non-negative")
        if self.carrying_capacity <= 0.0:
            raise ValueError("carrying_capacity must be positive")
        if self.density_coefficient < 0.0:
            raise ValueError("density_coefficient must be non-negative")
        if self.extinction_threshold < 0:
            raise ValueError("extinction_threshold must be non-negative")


@dataclass(frozen=True)
class PopulationTrackingResult:
    strategy: TrackingStrategy
    seed: int
    extinct: bool
    extinction_step: int | None
    final_population: int
    minimum_population: int
    mean_population: float
    mean_low_density_log_growth: float
    mean_realized_log_growth: float
    rms_abiotic_mismatch: float
    rms_interaction_mismatch: float

    @property
    def persistence_fraction(self) -> float:
        return 0.0 if self.extinct else 1.0


@dataclass(frozen=True)
class PopulationEnsembleResult:
    strategy: TrackingStrategy
    replicates: tuple[PopulationTrackingResult, ...]

    def summary(self) -> dict[str, float | int]:
        extinction_times = [
            row.extinction_step
            for row in self.replicates
            if row.extinction_step is not None
        ]
        final = [row.final_population for row in self.replicates]
        return {
            "replicates": len(self.replicates),
            "extinction_fraction": (
                sum(row.extinct for row in self.replicates)
                / len(self.replicates)
            ),
            "persistence_fraction": (
                sum(not row.extinct for row in self.replicates)
                / len(self.replicates)
            ),
            "mean_final_population": mean(final),
            "sd_final_population": (
                pstdev(final) if len(final) > 1 else 0.0
            ),
            "mean_population": mean(
                row.mean_population
                for row in self.replicates
            ),
            "mean_minimum_population": mean(
                row.minimum_population
                for row in self.replicates
            ),
            "mean_low_density_log_growth": mean(
                row.mean_low_density_log_growth
                for row in self.replicates
            ),
            "mean_realized_log_growth": mean(
                row.mean_realized_log_growth
                for row in self.replicates
            ),
            "mean_extinction_step_conditional": (
                mean(extinction_times)
                if extinction_times
                else float("nan")
            ),
            "median_extinction_step_conditional": (
                median(extinction_times)
                if extinction_times
                else float("nan")
            ),
        }


def poisson_sample(rate: float, rng: Random) -> int:
    """Draw a Poisson variate without third-party dependencies.

    Small rates use Knuth's product method. Larger rates use the PTRS
    transformed-rejection algorithm of Hoermann (1993).
    """

    if rate < 0.0:
        raise ValueError("Poisson rate must be non-negative")
    if rate == 0.0:
        return 0
    if rate < 30.0:
        threshold = exp(-rate)
        product = 1.0
        count = 0
        while product > threshold:
            count += 1
            product *= rng.random()
        return count - 1

    root = sqrt(rate)
    b = 0.931 + 2.53 * root
    a = -0.059 + 0.02483 * b
    inverse_alpha = 1.1239 + 1.1328 / (b - 3.4)
    squeeze = 0.9277 - 3.6224 / (b - 2.0)

    while True:
        u = rng.random() - 0.5
        v = rng.random()
        us = 0.5 - abs(u)
        if us <= 0.0:
            continue
        k = floor((2.0 * a / us + b) * u + rate + 0.43)
        if us >= 0.07 and v <= squeeze:
            return int(k)
        if k < 0 or (us < 0.013 and v > us):
            continue
        lhs = log(
            v
            * inverse_alpha
            / (a / (us * us) + b)
        )
        rhs = (
            -rate
            + k * log(rate)
            - lgamma(k + 1.0)
        )
        if lhs <= rhs:
            return int(k)


def _clip01(value: float) -> float:
    return min(1.0, max(0.0, value))


def _tracking_fraction(total_rate: float) -> float:
    if total_rate <= 0.0:
        return 0.0
    return -expm1(-total_rate)


def simulate_population_tracking(
    strategy: TrackingStrategy,
    scenario: TrackingScenario,
    population: PopulationDynamics,
    forcing: StochasticForcing = StochasticForcing(),
    *,
    seed: int,
) -> PopulationTrackingResult:
    """Simulate one integer population under tracking mismatch and density."""

    rng = Random(seed)
    abundance = population.initial_population
    minimum = abundance
    extinction_step: int | None = (
        0 if abundance <= population.extinction_threshold else None
    )

    total_rate = strategy.total_rate
    correction_fraction = _tracking_fraction(total_rate)
    if total_rate > _EPS:
        migration_share = strategy.migration_rate / total_rate
        phenology_share = strategy.phenology_rate / total_rate
    else:
        migration_share = 0.0
        phenology_share = 0.0

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

    demand = 0.0
    spatial_position = 0.0
    phenology_shift = 0.0
    population_sum = 0.0
    low_density_growth_sum = 0.0
    realized_growth_sum = 0.0
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
                    0.0,
                    forcing.partner_spatial_share_sd,
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
        partner_x = partner_share * partner_demand
        partner_z = (
            (1.0 - partner_share)
            * partner_demand
            / scenario.phenology_scale
        )

        spatial_gap = spatial_position - partner_x
        phenology_gap = scenario.phenology_scale * (
            phenology_shift - partner_z
        )
        interaction_sq = (
            spatial_gap * spatial_gap
            + phenology_gap * phenology_gap
        )
        low_density_growth = (
            scenario.baseline_growth
            - architecture_cost
            - 0.5
            * scenario.abiotic_strength
            * abiotic_mismatch
            * abiotic_mismatch
            - 0.5
            * scenario.interaction_strength
            * interaction_sq
        )

        density_penalty = (
            population.density_coefficient
            * abundance
            / population.carrying_capacity
        )
        realized_growth = (
            low_density_growth - density_penalty
        )

        if extinction_step is None:
            expected = abundance * exp(realized_growth)
            abundance = poisson_sample(expected, rng)
            if abundance <= population.extinction_threshold:
                abundance = 0
                extinction_step = step
        else:
            abundance = 0

        minimum = min(minimum, abundance)

        if step > scenario.burn_in:
            observed += 1
            population_sum += abundance
            low_density_growth_sum += low_density_growth
            realized_growth_sum += realized_growth
            abiotic_sq_sum += (
                abiotic_mismatch * abiotic_mismatch
            )
            interaction_sq_sum += interaction_sq

    if observed <= 0:
        raise RuntimeError("no post-burn-in observations")

    return PopulationTrackingResult(
        strategy=strategy,
        seed=seed,
        extinct=extinction_step is not None,
        extinction_step=extinction_step,
        final_population=abundance,
        minimum_population=minimum,
        mean_population=population_sum / observed,
        mean_low_density_log_growth=(
            low_density_growth_sum / observed
        ),
        mean_realized_log_growth=(
            realized_growth_sum / observed
        ),
        rms_abiotic_mismatch=sqrt(
            abiotic_sq_sum / observed
        ),
        rms_interaction_mismatch=sqrt(
            interaction_sq_sum / observed
        ),
    )


def population_tracking_ensemble(
    strategy: TrackingStrategy,
    scenario: TrackingScenario,
    population: PopulationDynamics,
    forcing: StochasticForcing = StochasticForcing(),
    *,
    replicates: int,
    seed: int,
) -> PopulationEnsembleResult:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    rows = tuple(
        simulate_population_tracking(
            strategy,
            scenario,
            population,
            forcing,
            seed=seed + replicate * 1_000_003,
        )
        for replicate in range(replicates)
    )
    return PopulationEnsembleResult(
        strategy=strategy,
        replicates=rows,
    )
