"""Bridge interval-level empirical audits into PAYOFF-B tracking controls.

This module intentionally returns only the control parameters identified by the
declared observation model. It does not fabricate ecological fitness terms.

Movement is accepted from either:
- the symmetric one-step nearest-neighbor inverse; or
- the directional one-step nearest-neighbor inverse.

Phenology rate h is included only when the fixed-interval phase audit licenses
a timing-axis-specific first-order correction.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from src.tracking_empirical_parameterization import (
    climate_velocity_from_wave_speed,
)
from src.tracking_interval_calibration import (
    IntervalCalibrationAudit,
)


@dataclass(frozen=True)
class EmpiricalTrackingControls:
    decision_interval_seconds: float
    calibration_patch_spacing: float
    climate_axis_angle_degrees: float
    spatial_gradient: float
    environmental_wave_speed: float
    climate_velocity: float
    migration_rate: float
    dispersal_x_weight: float
    dispersal_y_weight: float
    dispersal_x_bias: float
    dispersal_y_bias: float
    movement_kernel_kind: str
    phenology_rate: float | None
    phenology_rate_licensed: bool
    phenology_scale: float
    max_abs_phenology_shift: float

    @property
    def full_tracking_controls_ready(self) -> bool:
        return self.phenology_rate_licensed and self.phenology_rate is not None


def controls_from_interval_audit(
    audit: IntervalCalibrationAudit,
    *,
    spatial_gradient: float,
    wave_speed: float,
    phenology_scale: float,
    max_abs_phenology_shift: float,
) -> EmpiricalTrackingControls:
    """Construct the directly identified tracking-control subset.

    Preference order:
    1. if the symmetric kernel is licensed, use it with zero directional bias;
    2. otherwise, use the directional kernel when licensed;
    3. otherwise refuse.

    The symmetric route is preferred when both are mathematically available
    because it is the more parsimonious declared kernel.
    """

    for name, value in (
        ("spatial_gradient", spatial_gradient),
        ("wave_speed", wave_speed),
        ("phenology_scale", phenology_scale),
        ("max_abs_phenology_shift", max_abs_phenology_shift),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")

    if phenology_scale <= 0.0:
        raise ValueError("phenology_scale must be positive")
    if max_abs_phenology_shift < 0.0:
        raise ValueError(
            "max_abs_phenology_shift must be non-negative"
        )

    movement = audit.movement
    if (
        movement.direct_inverse_licensed
        and movement.movement_kernel is not None
    ):
        kernel = movement.movement_kernel
        migration_rate = kernel.migration_rate
        x_weight = kernel.x_weight
        y_weight = kernel.y_weight
        x_bias = 0.0
        y_bias = 0.0
        kernel_kind = "symmetric_nearest_neighbor"
    elif (
        movement.directional_inverse_licensed
        and movement.directional_movement_kernel is not None
    ):
        kernel = movement.directional_movement_kernel
        migration_rate = kernel.migration_rate
        x_weight = kernel.x_weight
        y_weight = kernel.y_weight
        x_bias = kernel.x_bias
        y_bias = kernel.y_bias
        kernel_kind = "directional_nearest_neighbor"
    else:
        failures = [
            value
            for value in (
                movement.inverse_failure,
                movement.directional_inverse_failure,
            )
            if value
        ]
        detail = "; ".join(failures) if failures else "no licensed movement inverse"
        raise ValueError(
            "interval audit does not license a movement kernel: "
            + detail
        )

    phase = audit.phase
    if phase.phenology_rate_licensed:
        if phase.mean_log_compression is None:
            raise ValueError(
                "phase audit is licensed but has no finite mean log compression"
            )
        phenology_rate: float | None = phase.mean_log_compression
        phenology_licensed = True
    else:
        phenology_rate = None
        phenology_licensed = False

    return EmpiricalTrackingControls(
        decision_interval_seconds=audit.target_interval_seconds,
        calibration_patch_spacing=audit.patch_spacing,
        climate_axis_angle_degrees=audit.climate_axis_angle_degrees,
        spatial_gradient=spatial_gradient,
        environmental_wave_speed=wave_speed,
        climate_velocity=climate_velocity_from_wave_speed(
            spatial_gradient,
            wave_speed,
        ),
        migration_rate=migration_rate,
        dispersal_x_weight=x_weight,
        dispersal_y_weight=y_weight,
        dispersal_x_bias=x_bias,
        dispersal_y_bias=y_bias,
        movement_kernel_kind=kernel_kind,
        phenology_rate=phenology_rate,
        phenology_rate_licensed=phenology_licensed,
        phenology_scale=phenology_scale,
        max_abs_phenology_shift=max_abs_phenology_shift,
    )
