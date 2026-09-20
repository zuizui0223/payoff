"""Empirical phase-error controller diagnostics for migration tracking.

This layer is deliberately distinct from the PAYOFF-B timing-axis phenology
rate h. A controller can reduce phase mismatch through spatial movement,
stopover behavior, route choice, timing, or combinations of these processes.

For a local linear phase profile along route distance,

    e(x) = beta0 + beta1 x,

the derivative of half squared phase error is

    d[e(x)^2/2]/dx = e(x) * beta1.

At the reference point x=0, a controller is locally restoring when

    beta0 * beta1 < 0.

When beta0 is known and nonzero, the local fractional relaxation coefficient is

    kappa = -beta1 / beta0,

with units inverse route-distance. Positive kappa means local restoration.

These diagnostics do not identify the independent timing-axis rate h.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal


PhaseState = Literal["early", "late", "matched", "unknown"]
ControllerClass = Literal[
    "restoring",
    "diverging",
    "no_detected_change",
    "matched_reference",
    "insufficient_information",
]


@dataclass(frozen=True)
class PhaseControllerAudit:
    phase_state: PhaseState
    slope: float | None
    slope_detected: bool
    intercept: float | None
    controller_class: ControllerClass
    restoring: bool | None
    local_squared_error_recovery: float | None
    local_fractional_relaxation: float | None
    linear_zero_crossing_distance: float | None
    linear_half_error_distance: float | None


def phase_state_from_intercept(
    intercept: float,
    *,
    zero_tolerance: float = 0.0,
) -> PhaseState:
    if not isfinite(intercept):
        raise ValueError("intercept must be finite")
    if zero_tolerance < 0.0 or not isfinite(zero_tolerance):
        raise ValueError("zero_tolerance must be non-negative and finite")
    if intercept < -zero_tolerance:
        return "early"
    if intercept > zero_tolerance:
        return "late"
    return "matched"


def audit_phase_controller(
    *,
    phase_state: PhaseState | None = None,
    slope: float | None,
    slope_detected: bool,
    intercept: float | None = None,
) -> PhaseControllerAudit:
    """Classify a route-distance phase controller.

    slope_detected=False means the published/statistical evidence does not
    establish a nonzero route-distance slope. In that case the result is
    no_detected_change, even if a point estimate was reported.

    phase_state can be supplied when only the sign of the intercept is
    published. If both phase_state and intercept are supplied, they must agree.
    """

    if phase_state is not None and phase_state not in {
        "early",
        "late",
        "matched",
        "unknown",
    }:
        raise ValueError("invalid phase_state")
    if slope is not None and not isfinite(slope):
        raise ValueError("slope must be finite when supplied")
    if intercept is not None and not isfinite(intercept):
        raise ValueError("intercept must be finite when supplied")

    inferred_state: PhaseState | None = None
    if intercept is not None:
        inferred_state = phase_state_from_intercept(intercept)

    if phase_state is None:
        state: PhaseState = inferred_state or "unknown"
    else:
        state = phase_state
        if (
            inferred_state is not None
            and state != "unknown"
            and state != inferred_state
        ):
            raise ValueError(
                "phase_state conflicts with the sign of intercept"
            )

    if not slope_detected:
        return PhaseControllerAudit(
            phase_state=state,
            slope=slope,
            slope_detected=False,
            intercept=intercept,
            controller_class="no_detected_change",
            restoring=False,
            local_squared_error_recovery=(
                0.0 if intercept is not None else None
            ),
            local_fractional_relaxation=None,
            linear_zero_crossing_distance=None,
            linear_half_error_distance=None,
        )

    if slope is None:
        raise ValueError(
            "slope must be supplied when slope_detected=True"
        )

    if state == "matched":
        return PhaseControllerAudit(
            phase_state=state,
            slope=slope,
            slope_detected=True,
            intercept=intercept,
            controller_class="matched_reference",
            restoring=None,
            local_squared_error_recovery=None,
            local_fractional_relaxation=None,
            linear_zero_crossing_distance=None,
            linear_half_error_distance=None,
        )

    if state == "unknown":
        return PhaseControllerAudit(
            phase_state=state,
            slope=slope,
            slope_detected=True,
            intercept=intercept,
            controller_class="insufficient_information",
            restoring=None,
            local_squared_error_recovery=None,
            local_fractional_relaxation=None,
            linear_zero_crossing_distance=None,
            linear_half_error_distance=None,
        )

    restoring_flag = (
        (state == "early" and slope > 0.0)
        or (state == "late" and slope < 0.0)
    )
    diverging = (
        (state == "early" and slope < 0.0)
        or (state == "late" and slope > 0.0)
    )

    if slope == 0.0:
        controller_class: ControllerClass = "no_detected_change"
        restoring_value: bool | None = False
    elif restoring_flag:
        controller_class = "restoring"
        restoring_value = True
    elif diverging:
        controller_class = "diverging"
        restoring_value = False
    else:
        controller_class = "insufficient_information"
        restoring_value = None

    squared_recovery = None
    fractional = None
    zero_distance = None
    half_distance = None

    if intercept is not None:
        squared_recovery = -intercept * slope
        if intercept != 0.0:
            fractional = -slope / intercept
        if restoring_flag and slope != 0.0:
            candidate_zero = -intercept / slope
            if candidate_zero > 0.0:
                zero_distance = candidate_zero
                half_distance = 0.5 * candidate_zero

    return PhaseControllerAudit(
        phase_state=state,
        slope=slope,
        slope_detected=True,
        intercept=intercept,
        controller_class=controller_class,
        restoring=restoring_value,
        local_squared_error_recovery=squared_recovery,
        local_fractional_relaxation=fractional,
        linear_zero_crossing_distance=zero_distance,
        linear_half_error_distance=half_distance,
    )
