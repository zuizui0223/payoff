"""Fail-closed helpers for the greater-snow-goose dual-use cue screen."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class CompensationScreenGate:
    estimable: bool
    reasons: tuple[str, ...]
    individuals: int
    years: int
    origin_contexts: int
    transitions: int
    predictive_connectivity_sd: float
    wait_days_sd: float


@dataclass(frozen=True)
class DualUseScreenClassification:
    status: str
    estimate: float | None
    se: float | None
    ci_low_95: float | None
    ci_high_95: float | None
    interpretation: str


def evaluate_compensation_screen_estimability(
    *,
    individuals: int,
    years: int,
    origin_contexts: int,
    transitions: int,
    predictive_connectivity_sd: float,
    wait_days_sd: float,
) -> CompensationScreenGate:
    rho_sd = float(predictive_connectivity_sd)
    wait_sd = float(wait_days_sd)
    if not isfinite(rho_sd) or rho_sd < 0:
        raise ValueError("predictive_connectivity_sd must be finite and non-negative")
    if not isfinite(wait_sd) or wait_sd < 0:
        raise ValueError("wait_days_sd must be finite and non-negative")

    reasons = []
    if int(individuals) < 30:
        reasons.append("FEWER_THAN_30_INDIVIDUALS")
    if int(years) < 4:
        reasons.append("FEWER_THAN_4_YEARS")
    if int(origin_contexts) < 3:
        reasons.append("FEWER_THAN_3_ORIGIN_CONTEXTS")
    if int(transitions) < 100:
        reasons.append("FEWER_THAN_100_TRANSITIONS")
    if rho_sd < 0.03:
        reasons.append("PREDICTIVE_CONNECTIVITY_SD_BELOW_0_03")
    if wait_sd <= 1e-12:
        reasons.append("NO_WAIT_DAYS_VARIATION")

    return CompensationScreenGate(
        estimable=not reasons,
        reasons=tuple(reasons),
        individuals=int(individuals),
        years=int(years),
        origin_contexts=int(origin_contexts),
        transitions=int(transitions),
        predictive_connectivity_sd=rho_sd,
        wait_days_sd=wait_sd,
    )


def classify_dual_use_compensation_signal(
    *,
    estimable: bool,
    interaction_estimate: float | None,
    interaction_se: float | None,
) -> DualUseScreenClassification:
    """Classify the registered negative transit-duration interaction.

    A supported negative interaction blocks promotion of a cue-independent
    fixed-D_eff interpretation. A null result does not prove exogeneity.
    """

    if not estimable:
        return DualUseScreenClassification(
            status="NOT_ESTIMABLE",
            estimate=None,
            se=None,
            ci_low_95=None,
            ci_high_95=None,
            interpretation=(
                "Compensation screen not estimable; fixed-D_eff exogeneity "
                "remains unresolved."
            ),
        )

    if interaction_estimate is None or interaction_se is None:
        raise ValueError("estimate and se are required when estimable=True")

    estimate = float(interaction_estimate)
    se = float(interaction_se)
    if not isfinite(estimate) or not isfinite(se) or se < 0:
        raise ValueError("estimate and se must be finite; se must be non-negative")

    low = estimate - 1.96 * se
    high = estimate + 1.96 * se

    if estimate < 0.0 and high < 0.0:
        return DualUseScreenClassification(
            status="DUAL_USE_BEHAVIORAL_SIGNAL_SUPPORTED",
            estimate=estimate,
            se=se,
            ci_low_95=low,
            ci_high_95=high,
            interpretation=(
                "Warmer locally predictive cues are associated with shorter "
                "subsequent transit duration. Fixed-D_eff cue exogeneity is "
                "not licensed for this focal cue; use a dual-use model for "
                "any theorem-level promotion."
            ),
        )

    return DualUseScreenClassification(
        status="DUAL_USE_NOT_DEMONSTRATED_EXOGENEITY_UNRESOLVED",
        estimate=estimate,
        se=se,
        ci_low_95=low,
        ci_high_95=high,
        interpretation=(
            "Registered dual-use behavioral signal not supported, but a null "
            "association is not an equivalence test. Fixed-D_eff cue "
            "exogeneity remains unresolved."
        ),
    )
