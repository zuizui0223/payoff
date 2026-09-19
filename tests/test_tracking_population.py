from math import isclose
from random import Random
from statistics import mean, pvariance

from src.spatiotemporal_tracking import (
    TrackingScenario,
    TrackingStrategy,
)
from src.stochastic_tracking import StochasticForcing
from src.tracking_population import (
    PopulationDynamics,
    poisson_sample,
    population_tracking_ensemble,
    simulate_population_tracking,
)


def test_poisson_sampler_has_correct_large_rate_moments():
    rng = Random(12345)
    rate = 50.0
    draws = [poisson_sample(rate, rng) for _ in range(6000)]
    observed_mean = mean(draws)
    observed_variance = pvariance(draws)

    assert abs(observed_mean - rate) / rate < 0.03
    assert abs(observed_variance - rate) / rate < 0.06


def test_poisson_sampler_handles_zero_and_small_rates():
    rng = Random(7)
    assert poisson_sample(0.0, rng) == 0
    draws = [poisson_sample(2.0, rng) for _ in range(4000)]
    assert abs(mean(draws) - 2.0) < 0.12


def test_zero_initial_population_is_absorbing():
    scenario = TrackingScenario(
        climate_velocity=0.0,
        interaction_strength=0.0,
        steps=40,
        burn_in=10,
    )
    population = PopulationDynamics(
        initial_population=0,
        carrying_capacity=100.0,
        density_coefficient=0.2,
    )
    result = simulate_population_tracking(
        TrackingStrategy(0.0, 0.0),
        scenario,
        population,
        seed=1,
    )
    assert result.extinct
    assert result.extinction_step == 0
    assert result.final_population == 0


def test_density_regulation_keeps_matched_population_near_carrying_capacity():
    scenario = TrackingScenario(
        climate_velocity=0.0,
        interaction_strength=0.0,
        migration_cost=0.0,
        phenology_cost=0.0,
        baseline_growth=0.2,
        steps=160,
        burn_in=40,
    )
    population = PopulationDynamics(
        initial_population=500,
        carrying_capacity=500.0,
        density_coefficient=0.2,
    )
    ensemble = population_tracking_ensemble(
        TrackingStrategy(0.0, 0.0),
        scenario,
        population,
        replicates=24,
        seed=100,
    )
    summary = ensemble.summary()

    assert summary["extinction_fraction"] == 0.0
    assert 420.0 < summary["mean_final_population"] < 580.0
    assert 420.0 < summary["mean_population"] < 580.0


def test_partner_axis_mismatch_increases_extinction_despite_abiotic_tracking():
    scenario = TrackingScenario(
        climate_velocity=0.04,
        partner_spatial_share=1.0,
        interaction_strength=0.8,
        migration_cost=0.01,
        phenology_cost=0.01,
        baseline_growth=0.28,
        steps=120,
        burn_in=20,
    )
    population = PopulationDynamics(
        initial_population=120,
        carrying_capacity=250.0,
        density_coefficient=0.28,
    )
    forcing = StochasticForcing(
        climate_increment_sd=0.005,
    )

    matched = population_tracking_ensemble(
        TrackingStrategy(0.5, 0.0),
        scenario,
        population,
        forcing,
        replicates=32,
        seed=700,
    ).summary()
    mismatched = population_tracking_ensemble(
        TrackingStrategy(0.0, 0.5),
        scenario,
        population,
        forcing,
        replicates=32,
        seed=700,
    ).summary()

    assert matched["persistence_fraction"] > 0.8
    assert mismatched["extinction_fraction"] > 0.8
    assert (
        mismatched["extinction_fraction"]
        > matched["extinction_fraction"]
    )


def test_ensemble_is_seed_reproducible():
    scenario = TrackingScenario(
        climate_velocity=0.03,
        steps=60,
        burn_in=10,
    )
    population = PopulationDynamics(
        initial_population=80,
        carrying_capacity=150.0,
        density_coefficient=0.2,
    )
    forcing = StochasticForcing(
        climate_increment_sd=0.01,
        partner_spatial_share_sd=0.05,
    )
    first = population_tracking_ensemble(
        TrackingStrategy(0.3, 0.2),
        scenario,
        population,
        forcing,
        replicates=5,
        seed=99,
    )
    second = population_tracking_ensemble(
        TrackingStrategy(0.3, 0.2),
        scenario,
        population,
        forcing,
        replicates=5,
        seed=99,
    )
    assert first == second
