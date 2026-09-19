from math import isclose

from src.moving_climate_landscape import (
    MovingLandscapeScenario,
    gaussian_initial_distribution,
    optimize_matched_landscape_strategy,
    reflect_nearest_neighbor_dispersal,
    simulate_moving_landscape_pair,
)
from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import SpeciesTrackingParameters


def test_reflecting_dispersal_conserves_total_abundance():
    abundance = (1.0, 2.0, 3.0, 4.0, 5.0)
    for migration_rate in (0.0, 0.1, 0.7, 3.0):
        dispersed = reflect_nearest_neighbor_dispersal(
            abundance,
            migration_rate,
        )
        assert isclose(
            sum(dispersed),
            sum(abundance),
            rel_tol=1e-12,
            abs_tol=1e-12,
        )
        assert all(value >= 0.0 for value in dispersed)


def test_initial_distribution_is_centered_and_normalized():
    scenario = MovingLandscapeScenario(
        patches=21,
        carrying_capacity=500.0,
        steps=40,
        burn_in=10,
    )
    abundance = gaussian_initial_distribution(scenario)
    assert isclose(sum(abundance), 500.0, abs_tol=1e-10)
    centroid = sum(
        value * position
        for value, position in zip(
            abundance,
            scenario.positions,
        )
    ) / sum(abundance)
    assert abs(centroid) < 1e-12


def test_identical_species_strategies_have_zero_interaction_mismatch():
    parameters = SpeciesTrackingParameters(
        interaction_strength=1.0,
        migration_cost=0.02,
        phenology_cost=0.02,
        baseline_growth=0.30,
    )
    scenario = MovingLandscapeScenario(
        patches=31,
        climate_velocity=0.04,
        max_abs_phenology_shift=3.0,
        steps=80,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    strategy = TrackingStrategy(0.4, 0.3)
    result = simulate_moving_landscape_pair(
        strategy,
        strategy,
        scenario,
    )
    assert result.rms_interaction_mismatch < 1e-12


def test_migration_only_tracking_moves_centroid_with_climate():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.0,
        migration_cost=0.01,
        phenology_cost=0.05,
        baseline_growth=0.35,
    )
    scenario = MovingLandscapeScenario(
        patches=41,
        spatial_gradient=0.20,
        climate_velocity=0.03,
        max_abs_phenology_shift=0.0,
        carrying_capacity=800.0,
        density_coefficient=0.35,
        steps=100,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    result = simulate_moving_landscape_pair(
        TrackingStrategy(0.8, 0.0),
        TrackingStrategy(0.8, 0.0),
        scenario,
    )
    assert result.final_centroid_a > 2.0
    assert result.final_centroid_b > 2.0
    assert result.final_phenology_a == 0.0
    assert result.final_phenology_b == 0.0


def test_phenology_only_tracking_can_follow_slow_change_without_range_shift():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.0,
        migration_cost=0.08,
        phenology_cost=0.01,
        baseline_growth=0.35,
    )
    scenario = MovingLandscapeScenario(
        patches=31,
        spatial_gradient=0.20,
        climate_velocity=0.02,
        max_abs_phenology_shift=5.0,
        carrying_capacity=800.0,
        density_coefficient=0.35,
        steps=80,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    result = simulate_moving_landscape_pair(
        TrackingStrategy(0.0, 0.8),
        TrackingStrategy(0.0, 0.8),
        scenario,
    )
    assert abs(result.final_centroid_a) < 1e-10
    assert result.final_phenology_a > 1.0
    assert result.rms_abiotic_mismatch_a < 0.5
    assert result.joint_persisted


def test_axis_mismatch_reduces_growth_on_explicit_landscape():
    parameters = SpeciesTrackingParameters(
        interaction_strength=1.0,
        migration_cost=0.01,
        phenology_cost=0.01,
        baseline_growth=0.35,
    )
    scenario = MovingLandscapeScenario(
        patches=41,
        spatial_gradient=0.20,
        climate_velocity=0.03,
        max_abs_phenology_shift=4.0,
        carrying_capacity=800.0,
        density_coefficient=0.35,
        steps=100,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    matched = simulate_moving_landscape_pair(
        TrackingStrategy(0.7, 0.0),
        TrackingStrategy(0.7, 0.0),
        scenario,
    )
    mismatched = simulate_moving_landscape_pair(
        TrackingStrategy(0.7, 0.0),
        TrackingStrategy(0.0, 0.7),
        scenario,
    )
    assert mismatched.rms_interaction_mismatch > 0.0
    assert mismatched.mean_joint_growth < matched.mean_joint_growth


def test_zero_phenology_limit_makes_positive_phenology_rate_wasteful():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.0,
        migration_cost=0.02,
        phenology_cost=0.05,
        baseline_growth=0.35,
    )
    scenario = MovingLandscapeScenario(
        patches=31,
        climate_velocity=0.03,
        max_abs_phenology_shift=0.0,
        carrying_capacity=600.0,
        density_coefficient=0.35,
        steps=70,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    best = optimize_matched_landscape_strategy(
        scenario,
        max_migration_rate=0.8,
        max_phenology_rate=0.8,
        migration_points=5,
        phenology_points=5,
    )
    assert best.strategy_a.phenology_rate == 0.0
    assert best.strategy_a.migration_rate > 0.0


def test_fast_climate_with_no_phenology_pushes_population_to_right_edge():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.0,
        migration_cost=0.01,
        phenology_cost=0.05,
        baseline_growth=0.35,
    )
    scenario = MovingLandscapeScenario(
        patches=21,
        spatial_gradient=0.20,
        climate_velocity=0.10,
        max_abs_phenology_shift=0.0,
        carrying_capacity=500.0,
        density_coefficient=0.35,
        steps=100,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    result = simulate_moving_landscape_pair(
        TrackingStrategy(1.0, 0.0),
        TrackingStrategy(1.0, 0.0),
        scenario,
    )
    assert result.final_centroid_a > 0.0
    assert result.right_edge_mass_fraction_a > 0.01
    assert result.rms_abiotic_mismatch_a > 0.5
