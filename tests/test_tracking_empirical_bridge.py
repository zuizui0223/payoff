from datetime import datetime, timedelta
from math import log

import pytest

from src.tracking_empirical_bridge import (
    controls_from_interval_audit,
)
from src.tracking_interval_calibration import (
    IntervalObservation,
    audit_interval_calibration,
)


def build_observations(displacements, phases=None):
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


def test_symmetric_interval_audit_builds_full_tracking_controls():
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
        build_observations(displacements, phases),
        target_interval_seconds=3600.0,
        patch_spacing=2.0,
        symmetry_tolerance=0.05,
        timing_axis_isolated=True,
    )
    controls = controls_from_interval_audit(
        audit,
        spatial_gradient=0.2,
        wave_speed=0.3,
        phenology_scale=0.1,
        max_abs_phenology_shift=20.0,
    )

    assert controls.movement_kernel_kind == "symmetric_nearest_neighbor"
    assert controls.dispersal_x_bias == 0.0
    assert controls.dispersal_y_bias == 0.0
    assert controls.climate_velocity == pytest.approx(0.06)
    assert controls.phenology_rate == pytest.approx(log(2.0))
    assert controls.full_tracking_controls_ready


def test_directional_interval_audit_builds_directional_controls():
    displacements = (
        [(1.0, 0.0)] * 12
        + [(0.0, 0.0)] * 8
    )
    audit = audit_interval_calibration(
        build_observations(displacements),
        target_interval_seconds=3600.0,
        patch_spacing=1.0,
        symmetry_tolerance=0.25,
        timing_axis_isolated=False,
    )
    controls = controls_from_interval_audit(
        audit,
        spatial_gradient=0.2,
        wave_speed=0.3,
        phenology_scale=0.1,
        max_abs_phenology_shift=20.0,
    )

    assert controls.movement_kernel_kind == "directional_nearest_neighbor"
    assert controls.dispersal_x_bias > 0.9
    assert abs(controls.dispersal_y_bias) < 1e-12
    assert not controls.phenology_rate_licensed
    assert controls.phenology_rate is None
    assert not controls.full_tracking_controls_ready


def test_phase_compression_without_isolation_does_not_populate_h():
    displacements = [
        (1.0, 0.0),
        (-1.0, 0.0),
        (1.0, 0.0),
        (-1.0, 0.0),
    ]
    phases = [16.0, 8.0, 4.0, 2.0, 1.0]
    audit = audit_interval_calibration(
        build_observations(displacements, phases),
        target_interval_seconds=3600.0,
        patch_spacing=2.0,
        symmetry_tolerance=0.05,
        timing_axis_isolated=False,
    )
    controls = controls_from_interval_audit(
        audit,
        spatial_gradient=0.2,
        wave_speed=0.3,
        phenology_scale=0.1,
        max_abs_phenology_shift=20.0,
    )

    assert audit.phase.mean_log_compression is not None
    assert controls.phenology_rate is None
    assert not controls.full_tracking_controls_ready


def test_controls_refuse_when_no_declared_movement_kernel_fits():
    # Every step is two patch spacings, outside the one-step support.
    displacements = [
        (2.0, 0.0),
        (-2.0, 0.0),
    ] * 4
    audit = audit_interval_calibration(
        build_observations(displacements),
        target_interval_seconds=3600.0,
        patch_spacing=1.0,
        symmetry_tolerance=0.05,
    )

    assert not audit.movement.direct_inverse_licensed
    assert not audit.movement.directional_inverse_licensed

    with pytest.raises(ValueError):
        controls_from_interval_audit(
            audit,
            spatial_gradient=0.2,
            wave_speed=0.3,
            phenology_scale=0.1,
            max_abs_phenology_shift=20.0,
        )
