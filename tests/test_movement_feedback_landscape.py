import pytest

from src.movement_feedback_landscape import (
    MovementRateFeedbackController,
    simulate_controlled_moving_landscape_2d,
)
from src.moving_climate_landscape_2d import (
    MovingLandscape2DScenario,
    simulate_moving_landscape_2d_pair,
)
from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import SpeciesTrackingParameters


def base_scenario(**overrides):
    parameters = SpeciesTrackingParameters(
        abiotic_strength=1.0,
        interaction_strength=0.0,
        migration_cost=0.0,
        phenology_cost=0.0,
        joint_cost=0.0,
        baseline_growth=0.35,
    )
    common = dict(
        width=21,
        height=11,
        climate_velocity=0.025,
        spatial_gradient=0.20,
        max_abs_phenology_shift=4.0,
        initial_total_abundance=300.0,
        local_carrying_capacity=80.0,
        density_coefficient=0.35,
        dispersal_x_weight=1.0,
        dispersal_y_weight=0.0,
        dispersal_x_bias=1.0,
        dispersal_y_bias=0.0,
        steps=80,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    common.update(overrides)
    return MovingLandscape2DScenario(**common)


def test_zero_feedback_matches_fixed_rate_single_species_projection():
    scenario = base_scenario()
    strategy = TrackingStrategy(0.3, 0.2)

    controlled = simulate_controlled_moving_landscape_2d(
        strategy,
        scenario,
        MovementRateFeedbackController(gain=0.0),
    )
    fixed = simulate_moving_landscape_2d_pair(
        strategy,
        strategy,
        scenario,
    )

    assert controlled.mean_low_density_growth == pytest.approx(
        fixed.mean_log_growth_a,
        rel=1e-12,
        abs=1e-12,
    )
    assert controlled.mean_realized_growth == pytest.approx(
        fixed.mean_realized_log_growth_a,
        rel=1e-12,
        abs=1e-12,
    )
    assert controlled.final_abundance == pytest.approx(
        fixed.final_abundance_a,
        rel=1e-12,
        abs=1e-12,
    )
    assert controlled.final_climate_centroid == pytest.approx(
        fixed.final_climate_centroid_a,
        rel=1e-12,
        abs=1e-12,
    )
    assert controlled.final_phenology_shift == pytest.approx(
        fixed.final_phenology_a,
        rel=1e-12,
        abs=1e-12,
    )
    assert controlled.rms_abiotic_mismatch == pytest.approx(
        fixed.rms_abiotic_mismatch_a,
        rel=1e-12,
        abs=1e-12,
    )


def test_positive_feedback_speeds_movement_and_reduces_lag_mismatch():
    scenario = base_scenario(
        climate_velocity=0.03,
        max_abs_phenology_shift=0.0,
    )
    strategy = TrackingStrategy(0.1, 0.0)

    fixed = simulate_controlled_moving_landscape_2d(
        strategy,
        scenario,
        MovementRateFeedbackController(gain=0.0),
    )
    controlled = simulate_controlled_moving_landscape_2d(
        strategy,
        scenario,
        MovementRateFeedbackController(
            gain=0.5,
            max_migration_rate=1.5,
        ),
    )

    assert controlled.mean_effective_migration_rate > strategy.migration_rate
    assert controlled.final_climate_centroid > fixed.final_climate_centroid
    assert controlled.rms_abiotic_mismatch < fixed.rms_abiotic_mismatch


def test_phenology_reduces_controller_movement_demand():
    scenario = base_scenario(
        climate_velocity=0.03,
        max_abs_phenology_shift=4.0,
    )
    controller = MovementRateFeedbackController(
        gain=0.5,
        max_migration_rate=1.5,
    )

    movement_only = simulate_controlled_moving_landscape_2d(
        TrackingStrategy(0.1, 0.0),
        scenario,
        controller,
    )
    with_phenology = simulate_controlled_moving_landscape_2d(
        TrackingStrategy(0.1, 0.5),
        scenario,
        controller,
    )

    assert (
        with_phenology.mean_effective_migration_rate
        < movement_only.mean_effective_migration_rate
    )
    assert with_phenology.final_phenology_shift > 0.0


def test_controller_ceiling_is_respected_and_reported():
    scenario = base_scenario(
        climate_velocity=0.05,
        max_abs_phenology_shift=0.0,
    )
    strategy = TrackingStrategy(0.1, 0.0)
    controlled = simulate_controlled_moving_landscape_2d(
        strategy,
        scenario,
        MovementRateFeedbackController(
            gain=2.0,
            max_migration_rate=0.4,
        ),
    )

    assert controlled.maximum_effective_migration_rate <= 0.4 + 1e-12
    assert controlled.controller_ceiling_fraction > 0.0


def test_negative_mismatch_can_slow_movement_to_floor():
    controller = MovementRateFeedbackController(
        gain=0.5,
        min_migration_rate=0.1,
        max_migration_rate=1.0,
    )
    rate, floor_hit, ceiling_hit = controller.effective_rate(
        baseline_rate=0.3,
        mismatch=-1.0,
    )
    assert rate == pytest.approx(0.1)
    assert floor_hit
    assert not ceiling_hit
