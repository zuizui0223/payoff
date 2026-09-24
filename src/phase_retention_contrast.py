"""Prospective within-system contrasts in PAYOFF-B phase retention.

A cross-system common coordinate does not imply lambda is constant. A strong
test is whether a predeclared forcing perturbation shifts lambda within the same
taxon while the phase coordinate and segment scale are held fixed.

This module evaluates source-model summaries of two registered forcing groups.
The statistical contrast itself is fit upstream; PAYOFF-B receives the frozen
lambda estimates and, when preregistered, the p-value for their difference.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal


ContrastDirection = Literal[
    "b_greater_than_a",
    "b_less_than_a",
    "different",
]


@dataclass(frozen=True)
class PhaseRetentionContrastRegistration:
    system_name: str
    independent_test_id: str
    phase_coordinate_id: str
    segment_scale_id: str
    group_a: str
    group_b: str
    expected_direction: ContrastDirection
    max_p_value: float | None = None
    min_abs_difference: float = 0.0

    def __post_init__(self) -> None:
        for name in (
            "system_name",
            "independent_test_id",
            "phase_coordinate_id",
            "segment_scale_id",
            "group_a",
            "group_b",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.group_a == self.group_b:
            raise ValueError("group_a and group_b must differ")
        if self.max_p_value is not None:
            if (
                not isfinite(self.max_p_value)
                or not 0.0 < self.max_p_value <= 1.0
            ):
                raise ValueError(
                    "max_p_value must lie in (0,1] when supplied"
                )
        if (
            not isfinite(self.min_abs_difference)
            or self.min_abs_difference < 0.0
        ):
            raise ValueError(
                "min_abs_difference must be non-negative and finite"
            )


@dataclass(frozen=True)
class PhaseRetentionContrastObservation:
    system_name: str
    independent_test_id: str
    phase_coordinate_id: str
    segment_scale_id: str
    group_a: str
    group_b: str
    lambda_a: float
    lambda_b: float
    p_difference: float | None = None
    fit_provenance: dict[str, object] | None = None

    def __post_init__(self) -> None:
        for name in (
            "system_name",
            "independent_test_id",
            "phase_coordinate_id",
            "segment_scale_id",
            "group_a",
            "group_b",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")
        for name in ("lambda_a", "lambda_b"):
            if not isfinite(getattr(self, name)):
                raise ValueError(f"{name} must be finite")
        if self.p_difference is not None:
            if (
                not isfinite(self.p_difference)
                or not 0.0 <= self.p_difference <= 1.0
            ):
                raise ValueError(
                    "p_difference must lie in [0,1] when supplied"
                )
        if (
            self.fit_provenance is not None
            and not isinstance(self.fit_provenance, dict)
        ):
            raise ValueError(
                "fit_provenance must be a mapping when supplied"
            )


@dataclass(frozen=True)
class PhaseRetentionContrastGate:
    passed: bool
    direction_passed: bool
    magnitude_passed: bool
    support_passed: bool
    lambda_difference_b_minus_a: float
    registration: PhaseRetentionContrastRegistration
    observation: PhaseRetentionContrastObservation
    reasons: tuple[str, ...]


def evaluate_phase_retention_contrast(
    registration: PhaseRetentionContrastRegistration,
    observation: PhaseRetentionContrastObservation,
) -> PhaseRetentionContrastGate:
    """Evaluate a preregistered within-system forcing effect on lambda."""

    identity_fields = (
        "system_name",
        "independent_test_id",
        "phase_coordinate_id",
        "segment_scale_id",
        "group_a",
        "group_b",
    )
    for name in identity_fields:
        if getattr(registration, name) != getattr(observation, name):
            raise ValueError(
                f"contrast observation {name} does not match registration"
            )

    delta = observation.lambda_b - observation.lambda_a

    if registration.expected_direction == "b_greater_than_a":
        direction_passed = delta > 0.0
    elif registration.expected_direction == "b_less_than_a":
        direction_passed = delta < 0.0
    else:
        direction_passed = abs(delta) > 0.0

    magnitude_passed = (
        abs(delta) >= registration.min_abs_difference
    )

    if registration.max_p_value is None:
        support_passed = True
    else:
        if observation.p_difference is None:
            support_passed = False
        else:
            support_passed = (
                observation.p_difference
                <= registration.max_p_value
            )

    reasons: list[str] = []
    if not direction_passed:
        reasons.append(
            "observed lambda contrast has the wrong preregistered direction"
        )
    if not magnitude_passed:
        reasons.append(
            "observed lambda contrast is below the preregistered magnitude"
        )
    if not support_passed:
        reasons.append(
            "observed lambda contrast lacks preregistered inferential support"
        )

    return PhaseRetentionContrastGate(
        passed=(
            direction_passed
            and magnitude_passed
            and support_passed
        ),
        direction_passed=direction_passed,
        magnitude_passed=magnitude_passed,
        support_passed=support_passed,
        lambda_difference_b_minus_a=delta,
        registration=registration,
        observation=observation,
        reasons=tuple(reasons),
    )
