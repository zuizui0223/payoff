"""Fixed-interval empirical audit for PAYOFF-B tracking data.

This module converts projected interval-level observations into diagnostics for
the declared movement kernel and phase-error controller.

Important separation:
- movement displacement can test/parameterize the symmetric nearest-neighbor
  kernel only when directional drift is small on the declared decision interval;
- Days-From-Peak or other phase-error compression is a controller diagnostic;
  it identifies the PAYOFF-B phenology rate h only when the residual transition
  is independently known to isolate the timing axis from spatial movement.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import cos, isfinite, pi, sin, sqrt
from statistics import mean, median
from typing import Iterable

from src.tracking_empirical_parameterization import (
    DirectionalMovementKernelEstimate,
    MovementKernelEstimate,
    audit_residual_compression,
    deaggregate_directional_moments,
    infer_directional_movement_kernel_from_aggregated_moments,
    infer_movement_kernel_from_component_variances,
)


@dataclass(frozen=True)
class IntervalObservation:
    animal_id: str
    timestamp: datetime
    x_metric: float
    y_metric: float
    phase_residual: float | None = None


@dataclass(frozen=True)
class StepObservation:
    animal_id: str
    dt_seconds: float
    longitudinal_displacement: float
    transverse_displacement: float
    phase_before: float | None
    phase_after: float | None


@dataclass(frozen=True)
class MovementIntervalAudit:
    intervals: int
    latent_substeps: int
    mean_longitudinal_displacement: float
    mean_transverse_displacement: float
    rms_longitudinal_displacement: float
    rms_transverse_displacement: float
    per_step_mean_longitudinal: float
    per_step_mean_transverse: float
    per_step_second_longitudinal: float
    per_step_second_transverse: float
    longitudinal_mean_to_rms: float
    transverse_mean_to_rms: float
    symmetry_tolerance: float
    symmetric_kernel_compatible: bool
    direct_inverse_licensed: bool
    inverse_failure: str | None
    movement_kernel: MovementKernelEstimate | None
    directional_inverse_licensed: bool
    directional_inverse_failure: str | None
    directional_movement_kernel: DirectionalMovementKernelEstimate | None


@dataclass(frozen=True)
class PhaseCompressionAudit:
    intervals_with_phase: int
    latent_substeps: int
    monotone_compression_intervals: int
    sign_crossing_intervals: int
    amplification_intervals: int
    no_correction_intervals: int
    complete_correction_intervals: int
    mean_log_compression: float | None
    median_log_compression: float | None
    observation_interval_mean_log_compression: float | None
    observation_interval_median_log_compression: float | None
    timing_axis_isolated: bool
    phenology_rate_licensed: bool
    license_reason: str


@dataclass(frozen=True)
class IntervalCalibrationAudit:
    target_interval_seconds: float
    latent_substeps: int
    model_step_seconds: float
    interval_tolerance_fraction: float
    climate_axis_angle_degrees: float
    patch_spacing: float
    retained_intervals: int
    movement: MovementIntervalAudit
    phase: PhaseCompressionAudit


def parse_timestamp(value: str) -> datetime:
    text = value.strip()
    if not text:
        raise ValueError("timestamp is empty")
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(
            f"timestamp is not ISO-8601 compatible: {value!r}"
        ) from exc


def build_fixed_intervals(
    observations: Iterable[IntervalObservation],
    *,
    target_interval_seconds: float,
    interval_tolerance_fraction: float = 0.10,
    climate_axis_angle_degrees: float = 0.0,
) -> tuple[StepObservation, ...]:
    """Build consecutive within-animal steps near one declared interval."""

    if not isfinite(target_interval_seconds) or target_interval_seconds <= 0.0:
        raise ValueError("target_interval_seconds must be positive and finite")
    if (
        not isfinite(interval_tolerance_fraction)
        or interval_tolerance_fraction < 0.0
        or interval_tolerance_fraction >= 1.0
    ):
        raise ValueError(
            "interval_tolerance_fraction must lie in [0,1)"
        )
    if not isfinite(climate_axis_angle_degrees):
        raise ValueError("climate_axis_angle_degrees must be finite")

    grouped: dict[str, list[IntervalObservation]] = {}
    for observation in observations:
        if not observation.animal_id:
            raise ValueError("animal_id must be non-empty")
        for name, value in (
            ("x_metric", observation.x_metric),
            ("y_metric", observation.y_metric),
        ):
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
        if (
            observation.phase_residual is not None
            and not isfinite(observation.phase_residual)
        ):
            raise ValueError("phase_residual must be finite when supplied")
        grouped.setdefault(observation.animal_id, []).append(observation)

    angle = climate_axis_angle_degrees * pi / 180.0
    ux = cos(angle)
    uy = sin(angle)
    vx = -uy
    vy = ux
    low = target_interval_seconds * (1.0 - interval_tolerance_fraction)
    high = target_interval_seconds * (1.0 + interval_tolerance_fraction)

    steps: list[StepObservation] = []
    for animal_id, rows in grouped.items():
        rows.sort(key=lambda row: row.timestamp)
        for before, after in zip(rows, rows[1:]):
            dt = (after.timestamp - before.timestamp).total_seconds()
            if dt < low or dt > high:
                continue
            dx = after.x_metric - before.x_metric
            dy = after.y_metric - before.y_metric
            longitudinal = dx * ux + dy * uy
            transverse = dx * vx + dy * vy
            steps.append(
                StepObservation(
                    animal_id=animal_id,
                    dt_seconds=dt,
                    longitudinal_displacement=longitudinal,
                    transverse_displacement=transverse,
                    phase_before=before.phase_residual,
                    phase_after=after.phase_residual,
                )
            )

    return tuple(steps)


def _mean_square(values: list[float]) -> float:
    if not values:
        raise ValueError("cannot compute mean square of empty values")
    return sum(value * value for value in values) / len(values)


def _mean_to_rms(values: list[float]) -> tuple[float, float, float]:
    avg = mean(values)
    rms = sqrt(_mean_square(values))
    if rms == 0.0:
        ratio = 0.0
    else:
        ratio = abs(avg) / rms
    return avg, rms, ratio


def audit_movement_intervals(
    steps: Iterable[StepObservation],
    *,
    patch_spacing: float,
    symmetry_tolerance: float = 0.25,
    latent_substeps: int = 1,
) -> MovementIntervalAudit:
    """Audit compatibility with the symmetric one-step movement kernel."""

    rows = tuple(steps)
    if not rows:
        raise ValueError("no fixed-interval steps were retained")
    if not isfinite(patch_spacing) or patch_spacing <= 0.0:
        raise ValueError("patch_spacing must be positive and finite")
    if not isinstance(latent_substeps, int) or latent_substeps <= 0:
        raise ValueError("latent_substeps must be a positive integer")
    if (
        not isfinite(symmetry_tolerance)
        or symmetry_tolerance < 0.0
        or symmetry_tolerance >= 1.0
    ):
        raise ValueError("symmetry_tolerance must lie in [0,1)")

    longitudinal = [
        row.longitudinal_displacement for row in rows
    ]
    transverse = [
        row.transverse_displacement for row in rows
    ]
    mean_long, rms_long, _ = _mean_to_rms(longitudinal)
    mean_trans, rms_trans, _ = _mean_to_rms(transverse)

    second_long = _mean_square(longitudinal)
    second_trans = _mean_square(transverse)
    (
        step_mean_long,
        step_mean_trans,
        step_second_long,
        step_second_trans,
    ) = deaggregate_directional_moments(
        mean_long,
        mean_trans,
        second_long,
        second_trans,
        latent_substeps,
    )
    step_rms_long = sqrt(step_second_long)
    step_rms_trans = sqrt(step_second_trans)
    ratio_long = (
        0.0
        if step_rms_long == 0.0
        else abs(step_mean_long) / step_rms_long
    )
    ratio_trans = (
        0.0
        if step_rms_trans == 0.0
        else abs(step_mean_trans) / step_rms_trans
    )

    symmetric = (
        ratio_long <= symmetry_tolerance
        and ratio_trans <= symmetry_tolerance
    )

    kernel: MovementKernelEstimate | None = None
    failure: str | None = None
    licensed = False

    if not symmetric:
        failure = (
            "directional drift is too large for the declared symmetric "
            "nearest-neighbor kernel"
        )
    else:
        try:
            # For a mean-zero declared kernel, the expected squared component
            # displacement equals the component variance.
            kernel = infer_movement_kernel_from_component_variances(
                step_second_long,
                step_second_trans,
                patch_spacing,
            )
            licensed = True
        except ValueError as exc:
            failure = str(exc)

    directional_kernel: DirectionalMovementKernelEstimate | None = None
    directional_failure: str | None = None
    directional_licensed = False
    try:
        directional_kernel = (
            infer_directional_movement_kernel_from_aggregated_moments(
                mean_long,
                mean_trans,
                second_long,
                second_trans,
                patch_spacing,
                latent_substeps,
            )
        )
        directional_licensed = True
    except ValueError as exc:
        directional_failure = str(exc)

    return MovementIntervalAudit(
        intervals=len(rows),
        latent_substeps=latent_substeps,
        mean_longitudinal_displacement=mean_long,
        mean_transverse_displacement=mean_trans,
        rms_longitudinal_displacement=rms_long,
        rms_transverse_displacement=rms_trans,
        per_step_mean_longitudinal=step_mean_long,
        per_step_mean_transverse=step_mean_trans,
        per_step_second_longitudinal=step_second_long,
        per_step_second_transverse=step_second_trans,
        longitudinal_mean_to_rms=ratio_long,
        transverse_mean_to_rms=ratio_trans,
        symmetry_tolerance=symmetry_tolerance,
        symmetric_kernel_compatible=symmetric,
        direct_inverse_licensed=licensed,
        inverse_failure=failure,
        movement_kernel=kernel,
        directional_inverse_licensed=directional_licensed,
        directional_inverse_failure=directional_failure,
        directional_movement_kernel=directional_kernel,
    )


def audit_phase_intervals(
    steps: Iterable[StepObservation],
    *,
    timing_axis_isolated: bool = False,
    latent_substeps: int = 1,
) -> PhaseCompressionAudit:
    """Summarize fixed-interval phase-error compression.

    Even mathematically monotone phase-error compression is not licensed as the
    PAYOFF-B timing-axis rate h unless movement and other correction pathways
    have been removed or otherwise held fixed.
    """

    if not isinstance(latent_substeps, int) or latent_substeps <= 0:
        raise ValueError("latent_substeps must be a positive integer")

    rows = [
        row
        for row in steps
        if row.phase_before is not None
        and row.phase_after is not None
    ]
    counts = {
        "monotone_compression": 0,
        "sign_crossing_or_overshoot": 0,
        "mismatch_amplification": 0,
        "no_correction": 0,
        "complete_correction_boundary": 0,
        "zero_start_residual": 0,
    }
    logs: list[float] = []

    for row in rows:
        audit = audit_residual_compression(
            float(row.phase_before),
            float(row.phase_after),
        )
        counts[audit.status] = counts.get(audit.status, 0) + 1
        if audit.log_compression is not None:
            logs.append(audit.log_compression)

    observation_logs = list(logs)
    logs = [
        value / latent_substeps
        for value in observation_logs
    ]

    if not timing_axis_isolated:
        licensed = False
        reason = (
            "phase-error compression is not timing-axis specific; movement or "
            "other tracking pathways may contribute"
        )
    elif not rows:
        licensed = False
        reason = "no phase-residual transitions are available"
    elif counts["sign_crossing_or_overshoot"] > 0:
        licensed = False
        reason = "some residual transitions cross zero or overshoot"
    elif counts["mismatch_amplification"] > 0:
        licensed = False
        reason = "some residual transitions amplify mismatch"
    elif counts["complete_correction_boundary"] > 0:
        licensed = False
        reason = "complete correction implies an unbounded one-step rate"
    elif counts["zero_start_residual"] > 0:
        licensed = False
        reason = "some transitions begin at zero residual"
    elif not logs:
        licensed = False
        reason = "no positive finite log-compression values are available"
    else:
        licensed = True
        reason = (
            "timing axis declared isolated and all retained transitions are "
            "compatible with finite monotone first-order correction"
        )

    return PhaseCompressionAudit(
        intervals_with_phase=len(rows),
        latent_substeps=latent_substeps,
        monotone_compression_intervals=counts["monotone_compression"],
        sign_crossing_intervals=counts["sign_crossing_or_overshoot"],
        amplification_intervals=counts["mismatch_amplification"],
        no_correction_intervals=counts["no_correction"],
        complete_correction_intervals=counts[
            "complete_correction_boundary"
        ],
        mean_log_compression=mean(logs) if logs else None,
        median_log_compression=median(logs) if logs else None,
        observation_interval_mean_log_compression=(
            mean(observation_logs) if observation_logs else None
        ),
        observation_interval_median_log_compression=(
            median(observation_logs) if observation_logs else None
        ),
        timing_axis_isolated=timing_axis_isolated,
        phenology_rate_licensed=licensed,
        license_reason=reason,
    )


def audit_interval_calibration(
    observations: Iterable[IntervalObservation],
    *,
    target_interval_seconds: float,
    patch_spacing: float,
    interval_tolerance_fraction: float = 0.10,
    climate_axis_angle_degrees: float = 0.0,
    symmetry_tolerance: float = 0.25,
    timing_axis_isolated: bool = False,
    latent_substeps: int = 1,
) -> IntervalCalibrationAudit:
    if not isinstance(latent_substeps, int) or latent_substeps <= 0:
        raise ValueError("latent_substeps must be a positive integer")

    steps = build_fixed_intervals(
        observations,
        target_interval_seconds=target_interval_seconds,
        interval_tolerance_fraction=interval_tolerance_fraction,
        climate_axis_angle_degrees=climate_axis_angle_degrees,
    )
    movement = audit_movement_intervals(
        steps,
        patch_spacing=patch_spacing,
        symmetry_tolerance=symmetry_tolerance,
        latent_substeps=latent_substeps,
    )
    phase = audit_phase_intervals(
        steps,
        timing_axis_isolated=timing_axis_isolated,
        latent_substeps=latent_substeps,
    )
    return IntervalCalibrationAudit(
        target_interval_seconds=target_interval_seconds,
        latent_substeps=latent_substeps,
        model_step_seconds=(
            target_interval_seconds / latent_substeps
        ),
        interval_tolerance_fraction=interval_tolerance_fraction,
        climate_axis_angle_degrees=climate_axis_angle_degrees,
        patch_spacing=patch_spacing,
        retained_intervals=len(steps),
        movement=movement,
        phase=phase,
    )
