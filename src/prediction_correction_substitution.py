"""Prediction-correction substitution in seasonal tracking.

Prospective PAYOFF-B extension. This module is explicitly post hoc relative to
the already-open barnacle-goose descriptive transition registry and the frozen
wigeon predictive-connectivity test. It must not be used to relabel those
results as confirmatory evidence.

The model asks a narrow mechanistic question:

    If better pre-commitment information lowers the mismatch risk that reaches
    a downstream stage, how much costly reactive correction should an optimal
    actor deploy?

Let R(q)>=0 be expected mismatch loss after using the best currently available
pre-commitment information. Let g in [0,1] be reactive correction gain, so
lambda=1-g is phase-error retention. Let correction cost be quadratic:

    L(g;q) = (1-g)^2 R(q) + (c/2) g^2,  c>0.

Then

    g*(q)      = 2 R(q) / [c + 2 R(q)]
    lambda*(q) = c / [c + 2 R(q)]
    L*(q)      = c R(q) / [c + 2 R(q)].

Therefore lower pre-correction risk implies weaker optimal feedback gain and
larger retention lambda. Prediction and reactive correction are substitutes in
this declared model.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from src.endogenous_information_timing import (
    closed_form_information_threshold,
    information_value,
)


@dataclass(frozen=True)
class OptimalCorrection:
    cue_accuracy: float
    pre_correction_risk: float
    correction_cost_curvature: float
    correction_gain: float
    phase_retention: float
    minimized_total_loss: float


def _positive_finite(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x) or x <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return x


def _unit_interval(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x) or x < 0.0 or x > 1.0:
        raise ValueError(f"{name} must lie in [0,1]")
    return x


def optimal_quadratic_correction(
    pre_correction_risk: float,
    *,
    correction_cost_curvature: float,
    cue_accuracy: float = 0.5,
) -> OptimalCorrection:
    """Return exact optimal feedback gain for a supplied pre-correction risk."""

    risk = float(pre_correction_risk)
    if not isfinite(risk) or risk < 0.0:
        raise ValueError("pre_correction_risk must be finite and non-negative")
    c = _positive_finite(
        "correction_cost_curvature",
        correction_cost_curvature,
    )
    q = _unit_interval("cue_accuracy", cue_accuracy)

    gain = 2.0 * risk / (c + 2.0 * risk)
    retention = c / (c + 2.0 * risk)
    minimized = c * risk / (c + 2.0 * risk)

    return OptimalCorrection(
        cue_accuracy=q,
        pre_correction_risk=risk,
        correction_cost_curvature=c,
        correction_gain=gain,
        phase_retention=retention,
        minimized_total_loss=minimized,
    )


def canonical_pre_correction_risk(
    prior_early: float,
    cue_accuracy: float,
    false_early_cost: float,
    missed_early_cost: float,
) -> float:
    """Return canonical mismatch risk after optimally using a cue.

    This is the no-cue Bayes risk minus the canonical value of information.
    Below the cue-actionability threshold, information value is zero and risk
    remains at the no-cue Bayes risk.
    """

    q = _unit_interval("cue_accuracy", cue_accuracy)
    base = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=0.0,
    )
    value = information_value(
        prior_early,
        q,
        false_early_cost,
        missed_early_cost,
    )
    risk = base.prior_bayes_risk - value
    if risk < -1e-12:
        raise AssertionError("information value exceeded prior Bayes risk")
    return max(0.0, risk)


def canonical_optimal_correction(
    prior_early: float,
    cue_accuracy: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    correction_cost_curvature: float,
) -> OptimalCorrection:
    """Map canonical cue accuracy to optimal downstream correction."""

    risk = canonical_pre_correction_risk(
        prior_early,
        cue_accuracy,
        false_early_cost,
        missed_early_cost,
    )
    return optimal_quadratic_correction(
        risk,
        correction_cost_curvature=correction_cost_curvature,
        cue_accuracy=cue_accuracy,
    )


def actionable_phase_retention_slope(
    prior_early: float,
    cue_accuracy: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    correction_cost_curvature: float,
) -> float:
    """Return d lambda*/dq above the canonical cue-actionability kink.

    Above q0, canonical post-cue risk has derivative -S, where

        S=(1-pi)C_F + pi C_M.

    Since lambda*=c/(c+2R),

        d lambda*/dq = 2 c S / (c+2R)^2 > 0.

    Below or at q0, the best action ignores the cue and this smooth derivative
    is not licensed.
    """

    q = _unit_interval("cue_accuracy", cue_accuracy)
    c = _positive_finite(
        "correction_cost_curvature",
        correction_cost_curvature,
    )
    base = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=0.0,
    )
    if q <= base.actionable_cue_accuracy + 1e-12:
        raise ValueError(
            "slope is defined only above the canonical cue-actionability kink"
        )

    risk = canonical_pre_correction_risk(
        prior_early,
        q,
        false_early_cost,
        missed_early_cost,
    )
    S = base.early_action_prior_loss + base.late_action_prior_loss
    return 2.0 * c * S / (c + 2.0 * risk) ** 2



@dataclass(frozen=True)
class PredictionCorrectionBalance:
    """Local balance between prediction benefit and cue-informed correction."""

    pre_correction_risk: float
    risk_derivative: float
    correction_cost_curvature: float
    correction_cost_derivative: float
    correction_gain: float
    phase_retention: float
    risk_log_derivative: float
    correction_cost_log_derivative: float
    correction_gain_logit_derivative: float
    correction_gain_derivative: float
    regime: str


def prediction_correction_balance(
    pre_correction_risk: float,
    risk_derivative: float,
    correction_cost_curvature: float,
    correction_cost_derivative: float,
    *,
    tolerance: float = 1e-12,
) -> PredictionCorrectionBalance:
    """Classify whether better information strengthens or weakens correction.

    Let both mismatch risk R(q)>0 and correction-cost curvature c(q)>0 vary with
    cue quality q. The optimal correction gain is

        g* = 2R/(c+2R).

    Exact differentiation gives

        dg*/dq
          = 2[c R' - R c']/(c+2R)^2,

    and, more transparently,

        d/dq log[g*/(1-g*)]
          = R'/R - c'/c.

    Therefore:
      - if R'/R < c'/c, prediction-risk reduction dominates and g falls;
      - if R'/R > c'/c, cue-informed cost reduction dominates and g rises;
      - equality is the local balance boundary.

    Note that both log derivatives may be negative.
    """

    R = float(pre_correction_risk)
    Rp = float(risk_derivative)
    c = float(correction_cost_curvature)
    cp = float(correction_cost_derivative)
    tol = float(tolerance)

    if not isfinite(R) or R <= 0.0:
        raise ValueError("pre_correction_risk must be finite and positive")
    if not isfinite(Rp):
        raise ValueError("risk_derivative must be finite")
    if not isfinite(c) or c <= 0.0:
        raise ValueError("correction_cost_curvature must be finite and positive")
    if not isfinite(cp):
        raise ValueError("correction_cost_derivative must be finite")
    if not isfinite(tol) or tol < 0.0:
        raise ValueError("tolerance must be finite and non-negative")

    gain = 2.0 * R / (c + 2.0 * R)
    retention = c / (c + 2.0 * R)
    risk_log = Rp / R
    cost_log = cp / c
    logit_derivative = risk_log - cost_log
    gain_derivative = gain * retention * logit_derivative

    if gain_derivative > tol:
        regime = "CUE_INFORMED_CORRECTION_DOMINANT"
    elif gain_derivative < -tol:
        regime = "PREDICTION_SUBSTITUTION_DOMINANT"
    else:
        regime = "LOCAL_BALANCE"

    return PredictionCorrectionBalance(
        pre_correction_risk=R,
        risk_derivative=Rp,
        correction_cost_curvature=c,
        correction_cost_derivative=cp,
        correction_gain=gain,
        phase_retention=retention,
        risk_log_derivative=risk_log,
        correction_cost_log_derivative=cost_log,
        correction_gain_logit_derivative=logit_derivative,
        correction_gain_derivative=gain_derivative,
        regime=regime,
    )
