from src.moving_climate_landscape import MovingLandscapeScenario
from src.spatiotemporal_tracking import TrackingStrategy
from src.stochastic_moving_landscape import (
    simulate_stochastic_moving_landscape_pair,
    stochastic_moving_landscape_ensemble,
)
from src.tracking_coevolution import SpeciesTrackingParameters


def test_stochastic_landscape_is_seed_reproducible():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.3,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.30,
    )
    scenario = MovingLandscapeScenario(
        patches=21,
        climate_velocity=0.03,
        max_abs_phenology_shift=2.0,
        carrying_capacity=300.0,
        density_coefficient=0.30,
        steps=60,
        burn_in=10,
        species_a=parameters,
        species_b=parameters,
    )
    strategy = TrackingStrategy(0.3, 0.1)
    first = simulate_stochastic_moving_landscape_pair(
        strategy,
        strategy,
        scenario,
        seed=123,
    )
    second = simulate_stochastic_moving_landscape_pair(
        strategy,
        strategy,
        scenario,
        seed=123,
    )
    assert first == second


def test_benign_static_landscape_persists_under_local_demographic_noise():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.2,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.35,
    )
    scenario = MovingLandscapeScenario(
        patches=21,
        climate_velocity=0.0,
        max_abs_phenology_shift=2.0,
        carrying_capacity=500.0,
        density_coefficient=0.35,
        steps=80,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    ensemble = stochastic_moving_landscape_ensemble(
        TrackingStrategy(0.0, 0.0),
        TrackingStrategy(0.0, 0.0),
        scenario,
        replicates=12,
        seed=10,
    )
    summary = ensemble.summary()
    assert summary["joint_persistence_fraction"] > 0.9


def test_known_spatial_coordination_rescue_survives_demographic_noise():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.5,
        migration_cost=0.10,
        phenology_cost=0.02,
        baseline_growth=0.30,
    )
    scenario = MovingLandscapeScenario(
        patches=31,
        spatial_gradient=0.20,
        climate_velocity=0.05,
        max_abs_phenology_shift=4.0,
        carrying_capacity=800.0,
        density_coefficient=0.30,
        steps=120,
        burn_in=30,
        species_a=parameters,
        species_b=parameters,
    )

    local = stochastic_moving_landscape_ensemble(
        TrackingStrategy(0.2, 0.0),
        TrackingStrategy(0.2, 0.0),
        scenario,
        replicates=16,
        seed=500,
    ).summary()
    matched = stochastic_moving_landscape_ensemble(
        TrackingStrategy(0.1, 0.2),
        TrackingStrategy(0.1, 0.2),
        scenario,
        replicates=16,
        seed=500,
    ).summary()

    assert local["joint_persistence_fraction"] < 0.2
    assert matched["joint_persistence_fraction"] > 0.8
    assert (
        matched["joint_persistence_fraction"]
        > local["joint_persistence_fraction"]
    )


def test_absorbing_boundary_can_be_simulated_stochastically():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.0,
        migration_cost=0.01,
        phenology_cost=0.03,
        baseline_growth=0.30,
    )
    scenario = MovingLandscapeScenario(
        patches=21,
        climate_velocity=0.04,
        max_abs_phenology_shift=2.0,
        boundary_retention=0.0,
        carrying_capacity=300.0,
        density_coefficient=0.30,
        steps=60,
        burn_in=10,
        species_a=parameters,
        species_b=parameters,
    )
    result = simulate_stochastic_moving_landscape_pair(
        TrackingStrategy(0.4, 0.1),
        TrackingStrategy(0.4, 0.1),
        scenario,
        seed=77,
    )
    assert result.final_abundance_a >= 0
    assert result.final_abundance_b >= 0
