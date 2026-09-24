from datetime import datetime, timedelta
from math import log

import pytest

from src.tracking_empirical_bridge import controls_from_interval_audit
from src.tracking_empirical_parameterization import TrackingFitnessEstimate
from src.tracking_empirical_prediction import (
    build_empirical_landscape_bundle,
    simulate_empirical_landscape_prediction,
)
from src.tracking_interval_calibration import (
    IntervalObservation,
    audit_interval_calibration,
)


def make_observations(displacements, phases=None):
    start = datetime(2020, 4, 1, 0, 0, 0)
    x = 0.0
    y = 0.0
    rows = [
        IntervalObservation(
            animal_id="A",
            timestamp=start,
            x_metric=x,
            y_metric=y,
            phase_residual=(
                None if phases is None else phases[0]
            ),
        )
    ]
    for index, (dx, dy) in enumerate(displacements, start=1):
        x += dx
        y += dy
        rows.append(
            IntervalObservation(
                animal_id="A",
                timestamp=start + timedelta(hours=index),
                x_metric=x,
                y_metric=y,
                phase_residual=(
                    None if phases is None else phases[index]
                ),
            )
        )
    return rows


def full_controls():
    displacements = [
        (1.0, 0.0),
        (-1.0, 0.0),
        (0.0, 1.0),
        (0.0, -1.0),
    ] * 5
    phases = [16.0]
    for _ in displacements:
        phases.append(phases[-1] * 0.5)

    audit = audit_interval_calibration(
        make_observations(displacements, phases),
        target_interval_seconds=3600.0,
        patch_spacing=2.0,
        symmetry_tolerance=0.05,
        timing_axis_isolated=True,
    )
    return controls_from_interval_audit(
        audit,
        spatial_gradient=0.2,
        wave_speed=0.3,
        phenology_scale=0.1,
        max_abs_phenology_shift=20.0,
    )


def fitness():
    return TrackingFitnessEstimate(
        baseline_growth=0.4,
        abiotic_strength=1.0,
        interaction_strength=0.5,
        migration_cost=0.05,
        phenology_cost=0.03,
        joint_cost=0.01,
    )


def test_calibration_environment_bundle_preserves_control_scales():
    controls = full_controls()
    bundle = build_empirical_landscape_bundle(
        controls,
        fitness(),
        width=15,
        height=9,
        steps=40,
        burn_in=10,
    )

    assert bundle.prediction_is_calibration_environment
    assert bundle.decision_interval_seconds == 3600.0
    assert bundle.scenario.patch_spacing == 2.0
    assert bundle.scenario.spatial_gradient == 0.2
    assert bundle.scenario.climate_velocity == pytest.approx(0.06)
    assert bundle.strategy.migration_rate == controls.migration_rate
    assert bundle.strategy.phenology_rate == pytest.approx(log(2.0))
    assert bundle.scenario.dispersal_x_weight == controls.dispersal_x_weight
    assert bundle.scenario.dispersal_y_weight == controls.dispersal_y_weight


def test_held_out_wave_speed_changes_forcing_not_strategy():
    controls = full_controls()
    calibration = build_empirical_landscape_bundle(
        controls,
        fitness(),
        width=15,
        height=9,
        steps=40,
        burn_in=10,
    )
    held_out = build_empirical_landscape_bundle(
        controls,
        fitness(),
        width=15,
        height=9,
        prediction_wave_speed=0.6,
        steps=40,
        burn_in=10,
    )

    assert calibration.strategy == held_out.strategy
    assert calibration.scenario.dispersal_x_weight == (
        held_out.scenario.dispersal_x_weight
    )
    assert calibration.scenario.dispersal_x_bias == (
        held_out.scenario.dispersal_x_bias
    )
    assert calibration.scenario.climate_velocity == pytest.approx(0.06)
    assert held_out.scenario.climate_velocity == pytest.approx(0.12)
    assert not held_out.prediction_is_calibration_environment


def test_prediction_uses_zero_interaction_mismatch_matched_duplicate():
    bundle = build_empirical_landscape_bundle(
        full_controls(),
        fitness(),
        width=15,
        height=9,
        steps=40,
        burn_in=10,
    )
    prediction = simulate_empirical_landscape_prediction(bundle)

    assert prediction.pair_result.rms_interaction_mismatch < 1e-12
    assert prediction.final_abundance >= 0.0
    assert prediction.rms_abiotic_mismatch >= 0.0


def test_movement_only_controls_refuse_full_empirical_prediction():
    displacements = (
        [(1.0, 0.0)] * 12
        + [(0.0, 0.0)] * 8
    )
    audit = audit_interval_calibration(
        make_observations(displacements),
        target_interval_seconds=3600.0,
        patch_spacing=1.0,
        timing_axis_isolated=False,
    )
    controls = controls_from_interval_audit(
        audit,
        spatial_gradient=0.2,
        wave_speed=0.3,
        phenology_scale=0.1,
        max_abs_phenology_shift=20.0,
    )
    assert not controls.full_tracking_controls_ready

    with pytest.raises(ValueError):
        build_empirical_landscape_bundle(
            controls,
            fitness(),
            width=15,
            height=9,
            steps=40,
            burn_in=10,
        )


def test_directional_controls_propagate_bias_into_prediction_scenario():
    displacements = (
        [(1.0, 0.0)] * 12
        + [(0.0, 0.0)] * 8
    )
    # Isolate a mathematically valid timing signal separately so full controls
    # are available while movement remains directional.
    phases = [16.0]
    for _ in displacements:
        phases.append(phases[-1] * 0.9)

    audit = audit_interval_calibration(
        make_observations(displacements, phases),
        target_interval_seconds=3600.0,
        patch_spacing=1.0,
        symmetry_tolerance=0.25,
        timing_axis_isolated=True,
    )
    controls = controls_from_interval_audit(
        audit,
        spatial_gradient=0.2,
        wave_speed=0.3,
        phenology_scale=0.1,
        max_abs_phenology_shift=20.0,
    )
    bundle = build_empirical_landscape_bundle(
        controls,
        fitness(),
        width=15,
        height=9,
        steps=30,
        burn_in=5,
    )

    assert controls.movement_kernel_kind == "directional_nearest_neighbor"
    assert bundle.scenario.dispersal_x_bias > 0.9
    assert abs(bundle.scenario.dispersal_y_bias) < 1e-12
