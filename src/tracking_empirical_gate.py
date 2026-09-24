"""Predeclared held-out validation gates for empirical tracking controls."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from src.tracking_empirical_validation import HeldOutTrackingValidation


@dataclass(frozen=True)
class TrackingValidationThresholds:
    max_movement_moment_rmse: float
    min_held_out_intervals: int = 1
    require_phase_validation: bool = False
    max_abs_phase_log_error: float | None = None
    min_phase_intervals: int = 1

    def __post_init__(self) -> None:
        if (
            not isfinite(self.max_movement_moment_rmse)
            or self.max_movement_moment_rmse < 0.0
        ):
            raise ValueError(
                "max_movement_moment_rmse must be non-negative and finite"
            )
        if self.min_held_out_intervals <= 0:
            raise ValueError("min_held_out_intervals must be positive")
        if self.min_phase_intervals <= 0:
            raise ValueError("min_phase_intervals must be positive")
        if self.require_phase_validation:
            if (
                self.max_abs_phase_log_error is None
                or not isfinite(self.max_abs_phase_log_error)
                or self.max_abs_phase_log_error < 0.0
            ):
                raise ValueError(
                    "require_phase_validation needs a non-negative finite "
                    "max_abs_phase_log_error"
                )
        elif self.max_abs_phase_log_error is not None:
            if (
                not isfinite(self.max_abs_phase_log_error)
                or self.max_abs_phase_log_error < 0.0
            ):
                raise ValueError(
                    "max_abs_phase_log_error must be non-negative and finite"
                )


@dataclass(frozen=True)
class TrackingValidationGate:
    passed: bool
    movement_passed: bool
    phase_passed: bool
    thresholds: TrackingValidationThresholds
    movement_rmse: float
    held_out_intervals: int
    phase_validation_licensed: bool
    phase_intervals: int
    abs_phase_log_error: float | None
    reasons: tuple[str, ...]


def evaluate_tracking_validation_gate(
    validation: HeldOutTrackingValidation,
    thresholds: TrackingValidationThresholds,
) -> TrackingValidationGate:
    """Evaluate frozen controls against predeclared held-out criteria.

    The threshold values are external scientific design choices. This function
    deliberately does not infer or optimize them from the held-out data.
    """

    reasons: list[str] = []
    movement = validation.movement

    movement_passed = True
    if movement.intervals < thresholds.min_held_out_intervals:
        movement_passed = False
        reasons.append(
            "held-out movement interval count below predeclared minimum"
        )
    if (
        movement.dimensionless_moment_rmse
        > thresholds.max_movement_moment_rmse
    ):
        movement_passed = False
        reasons.append(
            "held-out movement moment RMSE exceeds predeclared maximum"
        )

    phase = validation.phase
    phase_intervals = phase.intervals_with_phase
    phase_abs_error = (
        None
        if phase.mean_log_compression_error is None
        else abs(phase.mean_log_compression_error)
    )

    if thresholds.require_phase_validation:
        phase_passed = True
        if not phase.validation_licensed:
            phase_passed = False
            reasons.append(
                "held-out timing-axis validation is not licensed"
            )
        if phase_intervals < thresholds.min_phase_intervals:
            phase_passed = False
            reasons.append(
                "held-out phase interval count below predeclared minimum"
            )
        if phase_abs_error is None:
            phase_passed = False
            reasons.append(
                "held-out phase log-compression error is unavailable"
            )
        elif (
            phase_abs_error
            > float(thresholds.max_abs_phase_log_error)
        ):
            phase_passed = False
            reasons.append(
                "held-out phase log-compression error exceeds predeclared maximum"
            )
    else:
        phase_passed = True

    return TrackingValidationGate(
        passed=movement_passed and phase_passed,
        movement_passed=movement_passed,
        phase_passed=phase_passed,
        thresholds=thresholds,
        movement_rmse=movement.dimensionless_moment_rmse,
        held_out_intervals=movement.intervals,
        phase_validation_licensed=phase.validation_licensed,
        phase_intervals=phase_intervals,
        abs_phase_log_error=phase_abs_error,
        reasons=tuple(reasons),
    )
