from math import isclose

from src.moving_climate_landscape_2d import (
    MovingLandscape2DScenario,
    build_landscape_2d_geometry,
    gaussian_initial_distribution_2d,
    grid_dispersal_2d,
    optimize_matched_2d_strategy,
    simulate_moving_landscape_2d_pair,
    vertical_barrier_habitat,
)
from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import SpeciesTrackingParameters


def test_open_2d_dispersal_conserves_total_mass():
    scenario = MovingLandscape2DScenario(
        width=9,
        height=7,
        climate_velocity=0.0,
        steps=20,
        burn_in=5,
    )
    abundance = tuple(
        float(index + 1)
        for index in range(scenario.width * scenario.height)
    )
    for migration_rate in (0.0, 0.2, 1.0, 3.0):
        dispersed = grid_dispersal_2d(
            abundance,
            migration_rate,
            scenario,
        )
        assert isclose(
            sum(dispersed),
            sum(abundance),
            rel_tol=1e-12,
            abs_tol=1e-12,
        )
        assert all(value >= 0.0 for value in dispersed)


def test_closed_vertical_barrier_blocks_crossing():
    width = 9
    height = 7
    barrier_x = 5
    quality = vertical_barrier_habitat(
        width,
        height,
        barrier_x_index=barrier_x,
        gap_width=0,
    )
    scenario = MovingLandscape2DScenario(
        width=width,
        height=height,
        climate_velocity=0.0,
        habitat_quality=quality,
        steps=20,
        burn_in=5,
    )
    abundance = [0.0] * (width * height)
    abundance[scenario.index(barrier_x - 1, height // 2)] = 100.0

    state = tuple(abundance)
    for _ in range(30):
        state = grid_dispersal_2d(
            state,
            1.0,
            scenario,
        )

    mass_beyond = sum(
        value
        for index, value in enumerate(state)
        if scenario.coordinate_indices(index)[0] > barrier_x
    )
    assert mass_beyond == 0.0
    assert isclose(sum(state), 100.0, abs_tol=1e-10)


def test_centered_gap_allows_crossing():
    width = 9
    height = 7
    barrier_x = 5
    quality = vertical_barrier_habitat(
        width,
        height,
        barrier_x_index=barrier_x,
        gap_width=1,
    )
    scenario = MovingLandscape2DScenario(
        width=width,
        height=height,
        climate_velocity=0.0,
        habitat_quality=quality,
        steps=20,
        burn_in=5,
    )
    abundance = [0.0] * (width * height)
    abundance[scenario.index(barrier_x - 1, height // 2)] = 100.0

    state = tuple(abundance)
    for _ in range(30):
        state = grid_dispersal_2d(
            state,
            1.0,
            scenario,
        )

    mass_beyond = sum(
        value
        for index, value in enumerate(state)
        if scenario.coordinate_indices(index)[0] > barrier_x
    )
    assert mass_beyond > 0.0
    assert isclose(sum(state), 100.0, abs_tol=1e-10)


def test_narrow_corridor_reduces_flux_relative_to_open_landscape():
    width = 15
    height = 11
    barrier_x = 9
    narrow_quality = vertical_barrier_habitat(
        width,
        height,
        barrier_x_index=barrier_x,
        gap_width=1,
    )
    open_quality = vertical_barrier_habitat(
        width,
        height,
        barrier_x_index=barrier_x,
        gap_width=height,
    )
    common = dict(
        width=width,
        height=height,
        climate_velocity=0.0,
        steps=20,
        burn_in=5,
    )
    narrow = MovingLandscape2DScenario(
        habitat_quality=narrow_quality,
        **common,
    )
    open_scenario = MovingLandscape2DScenario(
        habitat_quality=open_quality,
        **common,
    )

    initial = gaussian_initial_distribution_2d(open_scenario)
    narrow_state = initial
    open_state = initial
    for _ in range(25):
        narrow_state = grid_dispersal_2d(
            narrow_state,
            0.8,
            narrow,
        )
        open_state = grid_dispersal_2d(
            open_state,
            0.8,
            open_scenario,
        )

    def beyond(state, scenario):
        return sum(
            value
            for index, value in enumerate(state)
            if scenario.coordinate_indices(index)[0] > barrier_x
        )

    assert beyond(narrow_state, narrow) < beyond(
        open_state,
        open_scenario,
    )


def test_identical_2d_strategies_have_zero_interaction_mismatch():
    parameters = SpeciesTrackingParameters(
        interaction_strength=1.0,
        migration_cost=0.02,
        phenology_cost=0.02,
        baseline_growth=0.30,
    )
    scenario = MovingLandscape2DScenario(
        width=21,
        height=11,
        climate_velocity=0.025,
        max_abs_phenology_shift=2.0,
        steps=70,
        burn_in=15,
        species_a=parameters,
        species_b=parameters,
    )
    strategy = TrackingStrategy(0.5, 0.3)
    result = simulate_moving_landscape_2d_pair(
        strategy,
        strategy,
        scenario,
    )
    assert result.rms_interaction_mismatch < 1e-12


def test_static_2d_environment_penalizes_costly_tracking_in_low_density_fitness():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.0,
        migration_cost=0.05,
        phenology_cost=0.05,
        baseline_growth=0.30,
    )
    scenario = MovingLandscape2DScenario(
        width=15,
        height=9,
        climate_velocity=0.0,
        max_abs_phenology_shift=2.0,
        steps=50,
        burn_in=10,
        species_a=parameters,
        species_b=parameters,
    )
    zero = simulate_moving_landscape_2d_pair(
        TrackingStrategy(0.0, 0.0),
        TrackingStrategy(0.0, 0.0),
        scenario,
    )
    costly = simulate_moving_landscape_2d_pair(
        TrackingStrategy(0.0, 0.8),
        TrackingStrategy(0.0, 0.8),
        scenario,
    )
    assert zero.mean_log_growth_a > costly.mean_log_growth_a


def test_open_2d_climate_tracking_moves_centroid_along_climate_axis():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.0,
        migration_cost=0.01,
        phenology_cost=0.05,
        baseline_growth=0.35,
    )
    scenario = MovingLandscape2DScenario(
        width=31,
        height=15,
        climate_velocity=0.02,
        max_abs_phenology_shift=0.0,
        steps=80,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    result = simulate_moving_landscape_2d_pair(
        TrackingStrategy(0.8, 0.0),
        TrackingStrategy(0.8, 0.0),
        scenario,
    )
    assert result.final_climate_centroid_a > 1.0
    assert result.final_climate_centroid_b > 1.0


def test_zero_phenology_limit_makes_phenology_rate_wasteful_in_2d():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.0,
        migration_cost=0.02,
        phenology_cost=0.05,
        baseline_growth=0.35,
    )
    scenario = MovingLandscape2DScenario(
        width=21,
        height=11,
        climate_velocity=0.02,
        max_abs_phenology_shift=0.0,
        steps=60,
        burn_in=15,
        species_a=parameters,
        species_b=parameters,
    )
    best = optimize_matched_2d_strategy(
        scenario,
        max_migration_rate=0.8,
        max_phenology_rate=0.8,
        migration_points=5,
        phenology_points=5,
    )
    assert best.strategy_a.phenology_rate == 0.0


def test_offset_gap_places_passage_away_from_climate_axis():
    width = 9
    height = 9
    barrier_x = 6
    center = height // 2
    offset_center = center + 2
    quality = vertical_barrier_habitat(
        width,
        height,
        barrier_x_index=barrier_x,
        gap_width=1,
        gap_center_y_index=offset_center,
    )
    scenario = MovingLandscape2DScenario(
        width=width,
        height=height,
        climate_velocity=0.0,
        habitat_quality=quality,
        steps=20,
        burn_in=5,
    )
    assert quality[scenario.index(barrier_x, center)] == 0.0
    assert quality[
        scenario.index(barrier_x, offset_center)
    ] > 0.0


def test_cached_2d_geometry_is_numerically_identical():
    scenario = MovingLandscape2DScenario(
        width=15,
        height=9,
        climate_velocity=0.02,
        max_abs_phenology_shift=2.0,
        steps=40,
        burn_in=10,
    )
    strategy = TrackingStrategy(0.4, 0.2)
    direct = simulate_moving_landscape_2d_pair(
        strategy,
        strategy,
        scenario,
    )
    geometry = build_landscape_2d_geometry(scenario)
    cached = simulate_moving_landscape_2d_pair(
        strategy,
        strategy,
        scenario,
        _geometry=geometry,
    )
    assert cached == direct
