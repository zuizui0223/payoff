from datetime import datetime, timedelta

import pytest

from src.tracking_empirical_bridge import controls_from_interval_audit
from src.tracking_empirical_validation import (
    validate_tracking_controls,
)
from src.tracking_interval_calibration import (
    IntervalObservation,
    audit_interval_calibration,
    build_fixed_intervals,
)


def make_observations(displacements, phases=None):
    start = datetime(2020, 4, 1, 0, 0, 0)
    x = 0.0
    y = 0.0
    rows = [
        IntervalObservation(
            "A",
            start,
            x,
            y,
            None if phases is None else phases[0],
        )
    ]
    for index, (dx, dy) in enumerate(displacements, start=1):
        x += dx
        y += dy
        rows.append(
            IntervalObservation(
                "A",
                start + timedelta(hours=index),
                x,
                y,
                None if phases is None else phases[index],
            )
        )
    return rows


def directional_controls():
    displacements = (
        [(1.0, 0.0)] * 12
        + [(0.0, 0.0)] * 8
    )
    audit = audit_interval_calibration(
        make_observations(displacements),
        target_interval_seconds=3600.0,
        patch_spacing=1.0,
        symmetry_tolerance=0.25,
        timing_axis_isolated=False,
    )
    return controls_from_interval_audit(
        audit,
        spatial_gradient=0.2,
        wave_speed=0.3,
        phenology_scale=0.1,
        max_abs_phenology_shift=20.0,
    )


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


def test_held_out_same_directional_kernel_has_zero_moment_error():
    controls = directional_controls()
    held_out_displacements = (
        [(1.0, 0.0)] * 12
        + [(0.0, 0.0)] * 8
    )
    steps = build_fixed_intervals(
        make_observations(held_out_displacements),
        target_interval_seconds=3600.0,
    )
    validation = validate_tracking_controls(
        steps,
        controls,
    )

    assert validation.movement.dimensionless_moment_rmse == pytest.approx(
        0.0,
        abs=1e-12,
    )


def test_held_out_different_kernel_has_positive_moment_error():
    controls = directional_controls()
    held_out_displacements = (
        [(-1.0, 0.0)] * 12
        + [(0.0, 0.0)] * 8
    )
    steps = build_fixed_intervals(
        make_observations(held_out_displacements),
        target_interval_seconds=3600.0,
    )
    validation = validate_tracking_controls(
        steps,
        controls,
    )

    assert validation.movement.dimensionless_moment_rmse > 0.1


def test_held_out_isolated_phase_matches_frozen_h():
    controls = full_controls()
    displacements = [
        (1.0, 0.0),
        (-1.0, 0.0),
        (0.0, 1.0),
        (0.0, -1.0),
    ]
    phases = [8.0, 4.0, 2.0, 1.0, 0.5]
    steps = build_fixed_intervals(
        make_observations(displacements, phases),
        target_interval_seconds=3600.0,
    )
    validation = validate_tracking_controls(
        steps,
        controls,
        timing_axis_isolated=True,
    )

    assert validation.phase.validation_licensed
    assert validation.phase.mean_log_compression_error == pytest.approx(
        0.0,
        abs=1e-12,
    )


def test_held_out_phase_refuses_validation_without_axis_isolation():
    controls = full_controls()
    displacements = [
        (1.0, 0.0),
        (-1.0, 0.0),
    ]
    phases = [8.0, 4.0, 2.0]
    steps = build_fixed_intervals(
        make_observations(displacements, phases),
        target_interval_seconds=3600.0,
    )
    validation = validate_tracking_controls(
        steps,
        controls,
        timing_axis_isolated=False,
    )

    assert not validation.phase.validation_licensed
    assert validation.phase.mean_log_compression_error is None


def test_movement_only_calibration_cannot_validate_h():
    controls = directional_controls()
    displacements = [
        (1.0, 0.0),
        (0.0, 0.0),
    ]
    phases = [8.0, 4.0, 2.0]
    steps = build_fixed_intervals(
        make_observations(displacements, phases),
        target_interval_seconds=3600.0,
    )
    validation = validate_tracking_controls(
        steps,
        controls,
        timing_axis_isolated=True,
    )

    assert not controls.phenology_rate_licensed
    assert not validation.phase.validation_licensed
    assert validation.phase.predicted_log_compression is None
