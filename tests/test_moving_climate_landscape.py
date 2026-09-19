from math import isclose

from src.moving_climate_landscape import (
    MovingLandscapeScenario,
    gaussian_initial_distribution,
    geometric_tracking_capacity,
    landscape_persistence_frontier,
    nearest_neighbor_dispersal,
    optimize_matched_landscape_strategy,
    reflect_nearest_neighbor_dispersal,
    simulate_moving_landscape_pair,
    terminal_nonnegative_growth_velocity_ceiling,
    zero_mismatch_velocity_ceiling,
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
    # With zero dispersal, selection can still reweight the small spatial
    # tails already present in the initial Gaussian. The key prediction is
    # that phenology carries almost all tracking while range movement stays
    # small.
    assert abs(result.final_centroid_a) < 0.5
    assert result.final_phenology_a > 1.0
    assert (
        scenario.phenology_scale * result.final_phenology_a
        > scenario.spatial_gradient * abs(result.final_centroid_a)
    )
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
    # The population is compressed against the leading landscape edge before
    # it collapses. Once extinct, the final centroid is intentionally reported
    # as zero, so edge occupancy and persistence are the relevant diagnostics.
    assert result.right_edge_mass_fraction_a > 0.30
    assert result.rms_abiotic_mismatch_a > 0.5
    assert not result.joint_persisted


def test_landscape_persistence_frontier_reports_bracket_without_assuming_monotonicity():
    rows = [
        {
            "phenology_limit": 0.0,
            "climate_velocity": 0.01,
            "joint_persisted": 1,
            "outcome": "migration",
            "migration_rate": 0.4,
            "phenology_rate": 0.0,
            "right_edge_mass_fraction": 0.01,
            "phenology_limit_fraction": 0.0,
        },
        {
            "phenology_limit": 0.0,
            "climate_velocity": 0.03,
            "joint_persisted": 1,
            "outcome": "migration",
            "migration_rate": 0.6,
            "phenology_rate": 0.0,
            "right_edge_mass_fraction": 0.10,
            "phenology_limit_fraction": 0.0,
        },
        {
            "phenology_limit": 0.0,
            "climate_velocity": 0.05,
            "joint_persisted": 0,
            "outcome": "failure",
            "migration_rate": 0.8,
            "phenology_rate": 0.0,
            "right_edge_mass_fraction": 0.45,
            "phenology_limit_fraction": 0.0,
        },
        {
            "phenology_limit": 2.0,
            "climate_velocity": 0.01,
            "joint_persisted": 1,
            "outcome": "phenology",
            "migration_rate": 0.0,
            "phenology_rate": 0.5,
            "right_edge_mass_fraction": 0.0,
            "phenology_limit_fraction": 0.0,
        },
        {
            "phenology_limit": 2.0,
            "climate_velocity": 0.03,
            "joint_persisted": 0,
            "outcome": "failure",
            "migration_rate": 0.2,
            "phenology_rate": 0.5,
            "right_edge_mass_fraction": 0.2,
            "phenology_limit_fraction": 1.0,
        },
        {
            "phenology_limit": 2.0,
            "climate_velocity": 0.05,
            "joint_persisted": 1,
            "outcome": "mixed",
            "migration_rate": 0.4,
            "phenology_rate": 0.4,
            "right_edge_mass_fraction": 0.3,
            "phenology_limit_fraction": 1.0,
        },
    ]
    frontier = landscape_persistence_frontier(rows)
    first = frontier[0]
    second = frontier[1]

    assert first["max_persisted_velocity"] == 0.03
    assert first["first_failed_velocity_above"] == 0.05
    assert first["monotone_persistence"] == 1

    assert second["max_persisted_velocity"] == 0.05
    assert second["first_failed_velocity_above"] is None
    assert second["monotone_persistence"] == 0


def test_static_landscape_low_density_fitness_penalizes_costly_tracking():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.0,
        migration_cost=0.05,
        phenology_cost=0.05,
        baseline_growth=0.30,
    )
    scenario = MovingLandscapeScenario(
        patches=21,
        climate_velocity=0.0,
        max_abs_phenology_shift=2.0,
        carrying_capacity=400.0,
        density_coefficient=0.30,
        steps=50,
        burn_in=10,
        species_a=parameters,
        species_b=parameters,
    )
    zero = simulate_moving_landscape_pair(
        TrackingStrategy(0.0, 0.0),
        TrackingStrategy(0.0, 0.0),
        scenario,
    )
    costly = simulate_moving_landscape_pair(
        TrackingStrategy(0.0, 0.8),
        TrackingStrategy(0.0, 0.8),
        scenario,
    )

    assert zero.mean_log_growth_a > costly.mean_log_growth_a
    assert zero.mean_log_growth_b > costly.mean_log_growth_b
    assert (
        costly.mean_realized_log_growth_a
        != costly.mean_log_growth_a
    )


def test_geometric_tracking_capacity_and_zero_mismatch_velocity_ceiling():
    scenario = MovingLandscapeScenario(
        patches=41,
        patch_spacing=1.0,
        spatial_gradient=0.20,
        max_abs_phenology_shift=2.0,
        phenology_scale=1.0,
        steps=160,
        burn_in=20,
    )
    # Edge position is +/-20, so spatial capacity is 4 and phenology adds 2.
    assert isclose(
        geometric_tracking_capacity(scenario),
        6.0,
        abs_tol=1e-12,
    )
    assert isclose(
        zero_mismatch_velocity_ceiling(scenario),
        6.0 / 160.0,
        abs_tol=1e-12,
    )


def test_terminal_growth_ceiling_exceeds_perfect_tracking_ceiling():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.0,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.30,
        abiotic_strength=1.0,
    )
    scenario = MovingLandscapeScenario(
        patches=41,
        spatial_gradient=0.20,
        max_abs_phenology_shift=2.0,
        steps=160,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    strategy = TrackingStrategy(1.0 / 3.0, 1.0 / 6.0)
    terminal = terminal_nonnegative_growth_velocity_ceiling(
        scenario,
        strategy,
        parameters,
    )
    assert terminal is not None
    assert terminal > zero_mismatch_velocity_ceiling(scenario)


def test_leaky_boundary_loses_only_outward_edge_mass():
    abundance = (10.0, 0.0, 0.0)
    migration_rate = 0.7
    fraction = 1.0 - __import__("math").exp(-migration_rate)

    absorbing = nearest_neighbor_dispersal(
        abundance,
        migration_rate,
        boundary_retention=0.0,
    )
    half_retained = nearest_neighbor_dispersal(
        abundance,
        migration_rate,
        boundary_retention=0.5,
    )
    reflecting = nearest_neighbor_dispersal(
        abundance,
        migration_rate,
        boundary_retention=1.0,
    )

    assert isclose(
        sum(absorbing),
        10.0 * (1.0 - 0.5 * fraction),
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    assert isclose(
        sum(half_retained),
        10.0 * (1.0 - 0.25 * fraction),
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    assert isclose(sum(reflecting), 10.0, abs_tol=1e-12)


def test_boundary_retention_validation():
    import pytest

    with pytest.raises(ValueError):
        MovingLandscapeScenario(boundary_retention=-0.1)
    with pytest.raises(ValueError):
        MovingLandscapeScenario(boundary_retention=1.1)

    with pytest.raises(ValueError):
        nearest_neighbor_dispersal(
            (1.0, 2.0, 3.0),
            0.2,
            boundary_retention=1.1,
        )


def test_reflect_wrapper_matches_general_boundary_retention_one():
    abundance = (1.0, 3.0, 2.0, 4.0)
    for migration_rate in (0.0, 0.2, 1.0):
        assert reflect_nearest_neighbor_dispersal(
            abundance,
            migration_rate,
        ) == nearest_neighbor_dispersal(
            abundance,
            migration_rate,
            boundary_retention=1.0,
        )
