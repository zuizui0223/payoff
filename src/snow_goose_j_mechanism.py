"""Fail-closed helpers for the public 2009 snow-goose J-mechanism lane.

This lane is mechanistic only. It asks whether prolonged captivity under fed
conditions produces a direct physiological/body-condition burden after
conditioning on pre-treatment state. It does not identify natural information-
waiting cost J, D_eff, or q_wait.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class JMechanismGate:
    estimable: bool
    reasons: tuple[str, ...]
    females: int
    capture_groups: int
    duration_levels: int
    min_group_size: int


@dataclass(frozen=True)
class JMechanismClassification:
    status: str
    estimate: float | None
    se: float | None
    ci_low_95: float | None
    ci_high_95: float | None
    interpretation: str


def evaluate_j_mechanism_gate(
    *,
    females: int,
    capture_groups: int,
    duration_levels: int,
    min_group_size: int,
) -> JMechanismGate:
    reasons = []
    if int(females) < 30:
        reasons.append("FEWER_THAN_30_FED_FEMALES")
    if int(capture_groups) < 6:
        reasons.append("FEWER_THAN_6_FED_CAPTURE_GROUPS")
    if int(duration_levels) < 2:
        reasons.append("FEWER_THAN_2_NONZERO_DURATION_LEVELS")
    if int(min_group_size) < 2:
        reasons.append("CAPTURE_GROUP_WITH_FEWER_THAN_2_FEMALES")
    return JMechanismGate(
        estimable=not reasons,
        reasons=tuple(reasons),
        females=int(females),
        capture_groups=int(capture_groups),
        duration_levels=int(duration_levels),
        min_group_size=int(min_group_size),
    )


def classify_j_mechanism(
    *,
    estimable: bool,
    days_estimate: float | None,
    days_se: float | None,
) -> JMechanismClassification:
    if not estimable:
        return JMechanismClassification(
            status="NOT_ESTIMABLE",
            estimate=None,
            se=None,
            ci_low_95=None,
            ci_high_95=None,
            interpretation=(
                "Fed-only captivity-duration mechanism lane is not estimable; "
                "no inference about a J-like physiological cost is licensed."
            ),
        )
    if days_estimate is None or days_se is None:
        raise ValueError("estimate and se are required when estimable=True")
    estimate = float(days_estimate)
    se = float(days_se)
    if not isfinite(estimate) or not isfinite(se) or se < 0.0:
        raise ValueError("estimate and se must be finite; se non-negative")
    low = estimate - 1.96 * se
    high = estimate + 1.96 * se

    if estimate < 0.0 and high < 0.0:
        status = "FED_CAPTIVITY_PHYSIOLOGICAL_J_SIGNAL_SUPPORTED"
        interpretation = (
            "Among fed captive females, longer captivity predicts lower "
            "post-treatment body condition after baseline adjustment. This "
            "supports a direct physiological burden consistent with a J(delta) "
            "component, but does not identify natural J or D_eff."
        )
    else:
        status = "FED_CAPTIVITY_PHYSIOLOGICAL_J_SIGNAL_NOT_SUPPORTED"
        interpretation = (
            "The registered fed-only body-condition signal is not supported. "
            "This does not establish J=0 because non-energetic stress and other "
            "direct waiting costs remain untested."
        )

    return JMechanismClassification(
        status=status,
        estimate=estimate,
        se=se,
        ci_low_95=low,
        ci_high_95=high,
        interpretation=interpretation,
    )
