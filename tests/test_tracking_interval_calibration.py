from datetime import datetime, timedelta

import pytest

from src.tracking_interval_calibration import (
    IntervalObservation,
    audit_interval_calibration,
    audit_movement_intervals,
    audit_phase_intervals,
    build_fixed_intervals,
)


def make_observations(displacements, phase_values=None):
    start = datetime(2020, 4, 1, 0, 0, 0)
    x = 0.0
    y = 0.0
    observations = [
        IntervalObservation(
            animal_id="A",
            timestamp=start,
            x_metric=x,
            y_metric=y,
            phase_residual=(
                None if phase_values is None else phase_values[0]
            ),
        )
    ]
    for index, (dx, dy) in enumerate(displacements, start=1):
        x += dx
        y += dy
        observations.append(
            IntervalObservation(
                animal_id="A",
                timestamp=start + timedelta(hours=index),
                x_metric=x,
                y_metric=y,
                phase_residual=(
                    None
                    if phase_values is None
                    else phase_values[index]
                ),
            )
        )
    return observations


def test_symmetric_fixed_interval_steps_license_declared_kernel_inverse():
    displacements = [
        (1.0, 0.0),
        (-1.0, 0.0),
        (0.0, 1.0),
        (0.0, -1.0),
    ] * 5
    observations = make_observations(displacements)

    audit = audit_interval_calibration(
        observations,
        target_interval_seconds=3600.0,
        patch_spacing=2.0,
        symmetry_tolerance=0.05,
    )

    assert audit.retained_intervals == len(displacements)
    assert audit.movement.symmetric_kernel_compatible
    assert audit.movement.direct_inverse_licensed
    assert audit.movement.movement_kernel is not None
    assert audit.movement.movement_kernel.migration_rate > 0.0


def test_directional_migration_fails_symmetric_kernel_gate():
    # Valid biased nearest-neighbor kernel realization:
    # 60% move +1 along x, 40% stay.
    displacements = (
        [(1.0, 0.0)] * 12
        + [(0.0, 0.0)] * 8
    )
    observations = make_observations(displacements)
    steps = build_fixed_intervals(
        observations,
        target_interval_seconds=3600.0,
    )
    movement = audit_movement_intervals(
        steps,
        patch_spacing=1.0,
        symmetry_tolerance=0.25,
    )

    assert not movement.symmetric_kernel_compatible
    assert not movement.direct_inverse_licensed
    assert movement.movement_kernel is None
    assert "directional drift" in movement.inverse_failure
    assert movement.directional_inverse_licensed
    assert movement.directional_movement_kernel is not None
    assert movement.directional_movement_kernel.x_bias > 0.9


def test_interval_tolerance_filters_nonmatching_steps():
    start = datetime(2020, 4, 1, 0, 0, 0)
    observations = [
        IntervalObservation("A", start, 0.0, 0.0, None),
        IntervalObservation(
            "A",
            start + timedelta(hours=1),
            1.0,
            0.0,
            None,
        ),
        IntervalObservation(
            "A",
            start + timedelta(hours=3),
            2.0,
            0.0,
            None,
        ),
    ]
    steps = build_fixed_intervals(
        observations,
        target_interval_seconds=3600.0,
        interval_tolerance_fraction=0.1,
    )
    assert len(steps) == 1


def test_phase_compression_is_not_h_without_timing_axis_isolation():
    displacements = [
        (1.0, 0.0),
        (-1.0, 0.0),
        (1.0, 0.0),
        (-1.0, 0.0),
    ]
    phase = [16.0, 12.0, 9.0, 6.75, 5.0625]
    observations = make_observations(displacements, phase)
    steps = build_fixed_intervals(
        observations,
        target_interval_seconds=3600.0,
    )
    audit = audit_phase_intervals(
        steps,
        timing_axis_isolated=False,
    )

    assert audit.monotone_compression_intervals == 4
    assert audit.mean_log_compression is not None
    assert not audit.phenology_rate_licensed
    assert "not timing-axis specific" in audit.license_reason


def test_isolated_monotone_phase_compression_can_license_candidate_h():
    displacements = [
        (1.0, 0.0),
        (-1.0, 0.0),
        (1.0, 0.0),
        (-1.0, 0.0),
    ]
    phase = [16.0, 8.0, 4.0, 2.0, 1.0]
    observations = make_observations(displacements, phase)
    steps = build_fixed_intervals(
        observations,
        target_interval_seconds=3600.0,
    )
    audit = audit_phase_intervals(
        steps,
        timing_axis_isolated=True,
    )

    assert audit.phenology_rate_licensed
    assert audit.mean_log_compression == pytest.approx(
        0.6931471805599453
    )


def test_sign_crossing_blocks_isolated_h_license():
    displacements = [
        (1.0, 0.0),
        (-1.0, 0.0),
    ]
    phase = [4.0, 2.0, -1.0]
    observations = make_observations(displacements, phase)
    steps = build_fixed_intervals(
        observations,
        target_interval_seconds=3600.0,
    )
    audit = audit_phase_intervals(
        steps,
        timing_axis_isolated=True,
    )

    assert not audit.phenology_rate_licensed
    assert audit.sign_crossing_intervals == 1


def test_directional_interval_inverse_recovers_known_biased_kernel_moments():
    # Deterministic empirical moments matching a biased one-step kernel:
    # x second moment dominates and mean x is positive.
    displacements = (
        [(2.0, 0.0)] * 6
        + [(-2.0, 0.0)] * 2
        + [(0.0, 2.0)] * 1
        + [(0.0, -2.0)] * 1
        + [(0.0, 0.0)] * 10
    )
    observations = make_observations(displacements)
    steps = build_fixed_intervals(
        observations,
        target_interval_seconds=3600.0,
    )
    movement = audit_movement_intervals(
        steps,
        patch_spacing=3.0,
        symmetry_tolerance=0.1,
    )

    assert not movement.symmetric_kernel_compatible
    assert movement.directional_inverse_licensed
    kernel = movement.directional_movement_kernel
    assert kernel is not None
    assert kernel.x_bias > 0.0
    assert abs(kernel.y_bias) < 1e-12
    assert kernel.x_weight > kernel.y_weight
