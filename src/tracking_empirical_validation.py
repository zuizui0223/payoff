"""Held-out validation for calibrated PAYOFF-B tracking controls."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from statistics import mean, median
from typing import Iterable

from src.tracking_empirical_bridge import EmpiricalTrackingControls
from src.tracking_empirical_parameterization import (
    audit_residual_compression,
    implied_directional_movement_moments,
)
from src.tracking_interval_calibration import StepObservation


@dataclass(frozen=True)
class HeldOutMovementValidation:
    intervals: int
    observed_mean_longitudinal: float
    observed_mean_transverse: float
    observed_second_longitudinal: float
    observed_second_transverse: float
    predicted_mean_longitudinal: float
    predicted_mean_transverse: float
    predicted_second_longitudinal: float
    predicted_second_transverse: float
    error_mean_longitudinal: float
    error_mean_transverse: float
    error_second_longitudinal: float
    error_second_transverse: float
    dimensionless_moment_rmse: float


@dataclass(frozen=True)
class HeldOutPhaseValidation:
    intervals_with_phase: int
    compatible_intervals: int
    incompatible_intervals: int
    observed_mean_log_compression: float | None
    observed_median_log_compression: float | None
    predicted_log_compression: float | None
    mean_log_compression_error: float | None
    validation_licensed: bool
    license_reason: str


@dataclass(frozen=True)
class HeldOutTrackingValidation:
    movement: HeldOutMovementValidation
    phase: HeldOutPhaseValidation


def _movement_moments(
    steps: tuple[StepObservation, ...],
) -> tuple[float, float, float, float]:
    if not steps:
        raise ValueError("no held-out intervals supplied")
    longitudinal = [
        row.longitudinal_displacement for row in steps
    ]
    transverse = [
        row.transverse_displacement for row in steps
    ]
    return (
        mean(longitudinal),
        mean(transverse),
        mean(value * value for value in longitudinal),
        mean(value * value for value in transverse),
    )


def validate_movement_controls(
    steps: Iterable[StepObservation],
    controls: EmpiricalTrackingControls,
) -> HeldOutMovementValidation:
    """Compare frozen movement controls with held-out step moments."""

    rows = tuple(steps)
    (
        observed_mean_x,
        observed_mean_y,
        observed_second_x,
        observed_second_y,
    ) = _movement_moments(rows)

    (
        predicted_mean_x,
        predicted_mean_y,
        predicted_second_x,
        predicted_second_y,
    ) = implied_directional_movement_moments(
        controls.migration_rate,
        controls.dispersal_x_weight,
        controls.dispersal_y_weight,
        controls.dispersal_x_bias,
        controls.dispersal_y_bias,
        controls.calibration_patch_spacing,
    )

    error_mean_x = observed_mean_x - predicted_mean_x
    error_mean_y = observed_mean_y - predicted_mean_y
    error_second_x = observed_second_x - predicted_second_x
    error_second_y = observed_second_y - predicted_second_y

    d = controls.calibration_patch_spacing
    scaled = (
        error_mean_x / d,
        error_mean_y / d,
        error_second_x / (d * d),
        error_second_y / (d * d),
    )
    rmse = sqrt(
        sum(value * value for value in scaled) / len(scaled)
    )

    return HeldOutMovementValidation(
        intervals=len(rows),
        observed_mean_longitudinal=observed_mean_x,
        observed_mean_transverse=observed_mean_y,
        observed_second_longitudinal=observed_second_x,
        observed_second_transverse=observed_second_y,
        predicted_mean_longitudinal=predicted_mean_x,
        predicted_mean_transverse=predicted_mean_y,
        predicted_second_longitudinal=predicted_second_x,
        predicted_second_transverse=predicted_second_y,
        error_mean_longitudinal=error_mean_x,
        error_mean_transverse=error_mean_y,
        error_second_longitudinal=error_second_x,
        error_second_transverse=error_second_y,
        dimensionless_moment_rmse=rmse,
    )


def validate_phase_controls(
    steps: Iterable[StepObservation],
    controls: EmpiricalTrackingControls,
    *,
    timing_axis_isolated: bool,
) -> HeldOutPhaseValidation:
    """Validate frozen h only under an independently isolated timing axis."""

    rows = [
        row
        for row in steps
        if row.phase_before is not None
        and row.phase_after is not None
    ]

    if not controls.phenology_rate_licensed or controls.phenology_rate is None:
        return HeldOutPhaseValidation(
            intervals_with_phase=len(rows),
            compatible_intervals=0,
            incompatible_intervals=len(rows),
            observed_mean_log_compression=None,
            observed_median_log_compression=None,
            predicted_log_compression=None,
            mean_log_compression_error=None,
            validation_licensed=False,
            license_reason=(
                "calibration receipt does not license a timing-axis h"
            ),
        )

    if not timing_axis_isolated:
        return HeldOutPhaseValidation(
            intervals_with_phase=len(rows),
            compatible_intervals=0,
            incompatible_intervals=len(rows),
            observed_mean_log_compression=None,
            observed_median_log_compression=None,
            predicted_log_compression=controls.phenology_rate,
            mean_log_compression_error=None,
            validation_licensed=False,
            license_reason=(
                "held-out phase transitions are not declared timing-axis "
                "isolated"
            ),
        )

    logs: list[float] = []
    incompatible = 0
    for row in rows:
        audit = audit_residual_compression(
            float(row.phase_before),
            float(row.phase_after),
        )
        if (
            audit.monotone_first_order_compatible
            and audit.log_compression is not None
        ):
            logs.append(audit.log_compression)
        else:
            incompatible += 1

    if not rows:
        reason = "no held-out phase transitions"
        licensed = False
    elif incompatible > 0:
        reason = (
            "held-out phase transitions include sign crossing, amplification, "
            "zero-start or complete-correction boundary"
        )
        licensed = False
    elif not logs:
        reason = "no finite compatible held-out log-compression values"
        licensed = False
    else:
        reason = (
            "held-out timing axis is isolated and all transitions are "
            "compatible with the frozen first-order h"
        )
        licensed = True

    observed_mean = mean(logs) if logs else None
    return HeldOutPhaseValidation(
        intervals_with_phase=len(rows),
        compatible_intervals=len(logs),
        incompatible_intervals=incompatible,
        observed_mean_log_compression=observed_mean,
        observed_median_log_compression=(
            median(logs) if logs else None
        ),
        predicted_log_compression=controls.phenology_rate,
        mean_log_compression_error=(
            None
            if observed_mean is None
            else observed_mean - controls.phenology_rate
        ),
        validation_licensed=licensed,
        license_reason=reason,
    )


def validate_tracking_controls(
    steps: Iterable[StepObservation],
    controls: EmpiricalTrackingControls,
    *,
    timing_axis_isolated: bool = False,
) -> HeldOutTrackingValidation:
    rows = tuple(steps)
    return HeldOutTrackingValidation(
        movement=validate_movement_controls(
            rows,
            controls,
        ),
        phase=validate_phase_controls(
            rows,
            controls,
            timing_axis_isolated=timing_axis_isolated,
        ),
    )
