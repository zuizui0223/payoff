from math import isclose

from src.moving_climate_landscape_2d import (
    MovingLandscape2DScenario,
    bhattacharyya_overlap_2d,
    build_landscape_2d_geometry,
    corridor_persistence_frontier,
    gaussian_initial_distribution_2d,
    grid_dispersal_2d,
    multiple_vertical_barriers_habitat,
    optimize_matched_2d_strategy,
    phenology_only_capacity_velocity_ceiling,
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


def test_corridor_frontier_reports_gap_specific_brackets():
    rows = [
        {
            "gap_width": 1,
            "phenology_limit": 0.0,
            "climate_velocity": 0.02,
            "joint_persisted": 1,
            "migration_rate": 0.4,
            "phenology_rate": 0.0,
            "mean_fraction_beyond_barrier": 0.2,
            "phenology_limit_fraction": 0.0,
            "outcome": "migration",
        },
        {
            "gap_width": 1,
            "phenology_limit": 0.0,
            "climate_velocity": 0.03,
            "joint_persisted": 0,
            "migration_rate": 0.6,
            "phenology_rate": 0.0,
            "mean_fraction_beyond_barrier": 0.3,
            "phenology_limit_fraction": 0.0,
            "outcome": "failure",
        },
        {
            "gap_width": 5,
            "phenology_limit": 2.0,
            "climate_velocity": 0.02,
            "joint_persisted": 1,
            "migration_rate": 0.2,
            "phenology_rate": 0.2,
            "mean_fraction_beyond_barrier": 0.5,
            "phenology_limit_fraction": 0.4,
            "outcome": "mixed",
        },
        {
            "gap_width": 5,
            "phenology_limit": 2.0,
            "climate_velocity": 0.04,
            "joint_persisted": 1,
            "migration_rate": 0.4,
            "phenology_rate": 0.2,
            "mean_fraction_beyond_barrier": 0.7,
            "phenology_limit_fraction": 0.8,
            "outcome": "migration",
        },
    ]
    frontier = corridor_persistence_frontier(rows)
    narrow = frontier[0]
    wide = frontier[1]
    assert narrow["max_persisted_velocity"] == 0.02
    assert narrow["first_failed_velocity_above"] == 0.03
    assert narrow["monotone_persistence"] == 1
    assert wide["max_persisted_velocity"] == 0.04
    assert wide["first_failed_velocity_above"] is None
    assert wide["mean_crossing_at_frontier"] == 0.7


def test_zigzag_double_barrier_requires_transverse_route():
    width = 15
    height = 15
    center_y = height // 2
    straight = multiple_vertical_barriers_habitat(
        width,
        height,
        barriers=(
            (9, 1, center_y),
            (12, 1, center_y),
        ),
    )
    zigzag = multiple_vertical_barriers_habitat(
        width,
        height,
        barriers=(
            (9, 1, center_y + 5),
            (12, 1, center_y - 5),
        ),
    )
    straight_scenario = MovingLandscape2DScenario(
        width=width,
        height=height,
        climate_velocity=0.0,
        habitat_quality=straight,
        steps=20,
        burn_in=5,
    )
    zigzag_scenario = MovingLandscape2DScenario(
        width=width,
        height=height,
        climate_velocity=0.0,
        habitat_quality=zigzag,
        steps=20,
        burn_in=5,
    )

    initial = [0.0] * (width * height)
    initial[straight_scenario.index(8, center_y)] = 100.0
    straight_state = tuple(initial)
    zigzag_state = tuple(initial)

    for _ in range(80):
        straight_state = grid_dispersal_2d(
            straight_state,
            1.0,
            straight_scenario,
        )
        zigzag_state = grid_dispersal_2d(
            zigzag_state,
            1.0,
            zigzag_scenario,
        )

    def beyond_second_wall(state, scenario):
        return sum(
            value
            for index, value in enumerate(state)
            if scenario.coordinate_indices(index)[0] > 12
        )

    assert beyond_second_wall(
        straight_state,
        straight_scenario,
    ) > beyond_second_wall(
        zigzag_state,
        zigzag_scenario,
    )


def test_bhattacharyya_overlap_detects_identical_and_disjoint_distributions():
    identical_a = (1.0, 3.0, 0.0, 2.0)
    identical_b = (2.0, 6.0, 0.0, 4.0)
    disjoint_a = (1.0, 0.0, 2.0, 0.0)
    disjoint_b = (0.0, 3.0, 0.0, 4.0)

    assert isclose(
        bhattacharyya_overlap_2d(
            identical_a,
            identical_b,
        ),
        1.0,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    assert bhattacharyya_overlap_2d(
        disjoint_a,
        disjoint_b,
    ) == 0.0


def test_distribution_overlap_term_detects_same_centroid_spatial_segregation():
    width = 7
    height = 7
    center_x = width // 2
    center_y = height // 2
    parameters = SpeciesTrackingParameters(
        abiotic_strength=0.0,
        interaction_strength=1.0,
        migration_cost=0.0,
        phenology_cost=0.0,
        baseline_growth=0.30,
    )
    common = dict(
        width=width,
        height=height,
        climate_velocity=0.0,
        max_abs_phenology_shift=0.0,
        density_coefficient=0.0,
        steps=20,
        burn_in=5,
        species_a=parameters,
        species_b=parameters,
    )
    centroid_only = MovingLandscape2DScenario(
        distribution_overlap_scale=0.0,
        **common,
    )
    overlap_aware = MovingLandscape2DScenario(
        distribution_overlap_scale=1.0,
        **common,
    )

    abundance_a = [0.0] * (width * height)
    abundance_b = [0.0] * (width * height)
    for dy in (-1, 1):
        abundance_a[
            centroid_only.index(
                center_x,
                center_y + dy,
            )
        ] = 100.0
    for dy in (-2, 2):
        abundance_b[
            centroid_only.index(
                center_x,
                center_y + dy,
            )
        ] = 100.0

    strategy = TrackingStrategy(0.0, 0.0)
    baseline = simulate_moving_landscape_2d_pair(
        strategy,
        strategy,
        centroid_only,
        initial_abundance_a=tuple(abundance_a),
        initial_abundance_b=tuple(abundance_b),
    )
    aware = simulate_moving_landscape_2d_pair(
        strategy,
        strategy,
        overlap_aware,
        initial_abundance_a=tuple(abundance_a),
        initial_abundance_b=tuple(abundance_b),
    )

    # Both distributions have the same spatial centroid, so the legacy
    # centroid metric alone sees no mismatch.
    assert baseline.rms_interaction_mismatch < 1e-12
    assert baseline.mean_distribution_overlap == 0.0

    # The optional distribution term detects their disjoint support.
    assert aware.mean_distribution_overlap == 0.0
    assert aware.rms_interaction_mismatch > 0.99
    assert (
        aware.mean_joint_growth
        < baseline.mean_joint_growth - 0.49
    )


def test_temporal_bypass_capacity_ceiling_brackets_canonical_transition():
    width = 31
    height = 15
    center_x = width // 2
    barrier_x = center_x + 3
    parameters = SpeciesTrackingParameters(
        abiotic_strength=1.0,
        interaction_strength=0.25,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.30,
    )
    scenario = MovingLandscape2DScenario(
        width=width,
        height=height,
        climate_velocity=0.0,
        max_abs_phenology_shift=4.0,
        steps=100,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    accessible = tuple(
        scenario.index(x_index, y_index)
        for x_index in range(barrier_x)
        for y_index in range(height)
    )
    ceiling = phenology_only_capacity_velocity_ceiling(
        scenario,
        accessible,
        phenology_rate=1.0 / 3.0,
    )

    # Best-case terminal capacity predicts the observed canonical switch:
    # phenology-only is selected at v=0.05, while migration re-enters by v=0.06.
    assert 0.05 < ceiling < 0.06


def test_temporal_bypass_capacity_increases_with_phenology_limit():
    width = 15
    height = 9
    barrier_x = width // 2 + 2
    parameters = SpeciesTrackingParameters(
        abiotic_strength=1.0,
        interaction_strength=0.0,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.30,
    )

    ceilings = []
    for limit in (0.0, 2.0, 4.0):
        scenario = MovingLandscape2DScenario(
            width=width,
            height=height,
            climate_velocity=0.0,
            max_abs_phenology_shift=limit,
            steps=100,
            burn_in=20,
            species_a=parameters,
            species_b=parameters,
        )
        accessible = tuple(
            scenario.index(x_index, y_index)
            for x_index in range(barrier_x)
            for y_index in range(height)
        )
        ceilings.append(
            phenology_only_capacity_velocity_ceiling(
                scenario,
                accessible,
                phenology_rate=0.25,
            )
        )

    assert ceilings[0] < ceilings[1] < ceilings[2]
    assert isclose(
        ceilings[2] - ceilings[0],
        4.0 / 100.0,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
