"""Cross-system phase-retention coordinate and independent actuator gates.

PAYOFF-B should not require different taxa to share the same physical actuator.

The common cross-system coordinate is the signed phase-retention coefficient
lambda in

    e_out = r + lambda * e_in,

where e is signed phase mismatch and r is an interval-specific residual forcing
/intercept.

The actuator layer is deliberately separate. Speed, stopover duration, route
reset, movement direction, or other mechanisms are tested as prospective
system-specific predictions. Failing an actuator prediction does not erase a
successful lambda prediction; it rejects that actuator hypothesis for that
system.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Iterable, Literal


ActuatorDirection = Literal["increase", "decrease", "no_change"]
RetentionClass = Literal[
    "sign_reversing",
    "restoring",
    "neutral_retention",
    "amplifying",
]


@dataclass(frozen=True)
class PhaseRetentionEstimate:
    pairs: int
    lambda_retention: float
    residual_forcing: float
    rmse: float
    r_squared: float | None
    retention_class: RetentionClass


@dataclass(frozen=True)
class PhaseRetentionPrediction:
    lambda_low: float
    lambda_high: float
    min_pairs: int = 3
    require_retention_class: RetentionClass | None = None

    def __post_init__(self) -> None:
        if not isfinite(self.lambda_low) or not isfinite(self.lambda_high):
            raise ValueError("lambda bounds must be finite")
        if self.lambda_low > self.lambda_high:
            raise ValueError("lambda_low must be <= lambda_high")
        if self.min_pairs < 3:
            raise ValueError("min_pairs must be at least 3")


@dataclass(frozen=True)
class PhaseRetentionGate:
    passed: bool
    estimate: PhaseRetentionEstimate
    prediction: PhaseRetentionPrediction
    interval_passed: bool
    class_passed: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class ActuatorPrediction:
    name: str
    expected_direction: ActuatorDirection
    observed_effect: float
    zero_tolerance: float = 0.0
    prospective: bool = True

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("actuator name must be non-empty")
        if not isfinite(self.observed_effect):
            raise ValueError("observed_effect must be finite")
        if not isfinite(self.zero_tolerance) or self.zero_tolerance < 0.0:
            raise ValueError(
                "zero_tolerance must be non-negative and finite"
            )


@dataclass(frozen=True)
class ActuatorPredictionResult:
    name: str
    expected_direction: ActuatorDirection
    observed_effect: float
    passed: bool
    prospective: bool


@dataclass(frozen=True)
class ActuatorGate:
    system_name: str
    predictions: tuple[ActuatorPredictionResult, ...]
    prospective_predictions: int
    passed_predictions: int
    failed_predictions: int
    all_prospective_passed: bool


def classify_phase_retention(
    lambda_retention: float,
    *,
    equality_tolerance: float = 1e-12,
) -> RetentionClass:
    if not isfinite(lambda_retention):
        raise ValueError("lambda_retention must be finite")
    if equality_tolerance < 0.0 or not isfinite(equality_tolerance):
        raise ValueError(
            "equality_tolerance must be non-negative and finite"
        )
    if lambda_retention < -equality_tolerance:
        return "sign_reversing"
    if lambda_retention < 1.0 - equality_tolerance:
        return "restoring"
    if lambda_retention <= 1.0 + equality_tolerance:
        return "neutral_retention"
    return "amplifying"


def estimate_phase_retention(
    pairs: Iterable[tuple[float, float]],
) -> PhaseRetentionEstimate:
    """Fit e_out = r + lambda*e_in by ordinary least squares.

    This is the common coordinate layer. It does not infer which actuator
    produced the observed retention.
    """

    rows = tuple(pairs)
    if len(rows) < 3:
        raise ValueError("at least three phase-error pairs are required")
    for before, after in rows:
        if not isfinite(before) or not isfinite(after):
            raise ValueError("phase-error pairs must be finite")

    xbar = sum(before for before, _ in rows) / len(rows)
    ybar = sum(after for _, after in rows) / len(rows)
    sxx = sum((before - xbar) ** 2 for before, _ in rows)
    if sxx <= 0.0:
        raise ValueError(
            "phase-retention slope is unidentified because e_in has no variance"
        )
    sxy = sum(
        (before - xbar) * (after - ybar)
        for before, after in rows
    )
    lam = sxy / sxx
    intercept = ybar - lam * xbar

    residuals = [
        after - (intercept + lam * before)
        for before, after in rows
    ]
    sse = sum(value * value for value in residuals)
    rmse = sqrt(sse / len(rows))
    syy = sum((after - ybar) ** 2 for _, after in rows)
    r_squared = None if syy <= 0.0 else 1.0 - sse / syy

    return PhaseRetentionEstimate(
        pairs=len(rows),
        lambda_retention=lam,
        residual_forcing=intercept,
        rmse=rmse,
        r_squared=r_squared,
        retention_class=classify_phase_retention(lam),
    )


def evaluate_phase_retention_gate(
    estimate: PhaseRetentionEstimate,
    prediction: PhaseRetentionPrediction,
) -> PhaseRetentionGate:
    """Evaluate only the common lambda prediction.

    No actuator observations enter this gate.
    """

    reasons: list[str] = []
    enough_pairs = estimate.pairs >= prediction.min_pairs
    if not enough_pairs:
        reasons.append("phase-error pair count below predeclared minimum")

    interval_passed = (
        prediction.lambda_low
        <= estimate.lambda_retention
        <= prediction.lambda_high
    )
    if not interval_passed:
        reasons.append(
            "observed lambda lies outside the predeclared prediction interval"
        )

    class_passed = (
        prediction.require_retention_class is None
        or estimate.retention_class
        == prediction.require_retention_class
    )
    if not class_passed:
        reasons.append(
            "observed lambda retention class differs from prediction"
        )

    return PhaseRetentionGate(
        passed=enough_pairs and interval_passed and class_passed,
        estimate=estimate,
        prediction=prediction,
        interval_passed=interval_passed,
        class_passed=class_passed,
        reasons=tuple(reasons),
    )


def _actuator_prediction_passes(
    prediction: ActuatorPrediction,
) -> bool:
    value = prediction.observed_effect
    tolerance = prediction.zero_tolerance
    if prediction.expected_direction == "increase":
        return value > tolerance
    if prediction.expected_direction == "decrease":
        return value < -tolerance
    return abs(value) <= tolerance


def evaluate_actuator_gate(
    system_name: str,
    predictions: Iterable[ActuatorPrediction],
) -> ActuatorGate:
    """Evaluate system-specific actuator predictions independently of lambda."""

    if not system_name.strip():
        raise ValueError("system_name must be non-empty")
    rows = tuple(predictions)
    if not rows:
        raise ValueError("at least one actuator prediction is required")

    results = tuple(
        ActuatorPredictionResult(
            name=row.name,
            expected_direction=row.expected_direction,
            observed_effect=row.observed_effect,
            passed=_actuator_prediction_passes(row),
            prospective=row.prospective,
        )
        for row in rows
    )
    prospective = tuple(row for row in results if row.prospective)
    passed = sum(row.passed for row in prospective)
    failed = len(prospective) - passed

    return ActuatorGate(
        system_name=system_name,
        predictions=results,
        prospective_predictions=len(prospective),
        passed_predictions=passed,
        failed_predictions=failed,
        all_prospective_passed=(len(prospective) > 0 and failed == 0),
    )


def total_feedback_from_lambda(
    lambda_retention: float,
) -> float:
    """Map the common retention coordinate to total local restoring gain.

    Under the declared local recurrence

        e_(t+1) = lambda*e_t + r
                = (1-K)*e_t + r,

    K = 1-lambda.

    This does not identify the actuator decomposition of K.
    """

    if not isfinite(lambda_retention):
        raise ValueError("lambda_retention must be finite")
    return 1.0 - lambda_retention
