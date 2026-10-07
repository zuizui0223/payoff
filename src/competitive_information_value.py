"""Competitive information value as a prospective PAYOFF-B extension.

The existing actionability-balance model is

    N(t) = r(t) V_A(q(t)) - C(t),

where q is cue quality and r is retained actionability.

This module adds a declared reduced-form retained-information-exclusivity
weight e(t):

    N(t) = r(t) e(t) V_A(q(t)) - C(t).

The mechanism is intentionally distinct from biological recourse loss.  In a
competitive prediction setting, e(t) can represent the fraction of focal
information advantage not yet absorbed by other decision makers or a market.

This is not claimed to be a universal market-microstructure model.  It is a
minimal bridge for testing whether improving predictive accuracy can coexist
with declining incremental decision value.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log

from src.actionability_balance import canonical_actionability_geometry


_TOL = 1e-12


def _positive_finite(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x) or x <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return x


def _nonnegative_finite(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x) or x < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return x


@dataclass(frozen=True)
class CompetitiveBalanceDerivative:
    """Derivative decomposition for r(t)e(t)V_A(q(t))-C(t)."""

    cue_accuracy: float
    cue_accuracy_rate: float
    retained_actionability: float
    actionability_rate: float
    retained_exclusivity: float
    exclusivity_rate: float
    marginal_wait_cost: float
    information_value: float
    information_gain_term: float
    actionability_change_term: float
    exclusivity_change_term: float
    net_derivative: float
    relative_information_gain: float | None
    relative_actionability_loss: float | None
    relative_exclusivity_loss: float | None


@dataclass(frozen=True)
class CompetitiveInformationPeak:
    """Closed-form peak under exponential learning and two value-loss hazards."""

    alpha_information_rate: float
    beta_actionability_decay: float
    gamma_exclusivity_decay: float
    total_value_decay: float
    cue_gain_amplitude: float
    total_loss_scale: float
    actionable_cue_accuracy: float
    optimal_time: float
    optimal_cue_accuracy: float
    retained_actionability_at_optimum: float
    retained_exclusivity_at_optimum: float
    maximum_gross_information_value: float


def competitive_balance_derivative(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    cue_accuracy: float,
    cue_accuracy_rate: float,
    retained_actionability: float,
    actionability_rate: float,
    retained_exclusivity: float,
    exclusivity_rate: float,
    marginal_wait_cost: float = 0.0,
) -> CompetitiveBalanceDerivative:
    """Evaluate the competitive-information balance above the PAYOFF-B q0.

    The reduced form is

        N(t)=r(t)e(t)[S q(t)-B]-C(t).

    With zero marginal waiting cost and positive r, e and V_A, a stationary
    point obeys

        S qdot / (S q-B) = -rdot/r - edot/e.
    """

    geom = canonical_actionability_geometry(
        prior_early,
        false_early_cost,
        missed_early_cost,
    )

    q = float(cue_accuracy)
    qdot = float(cue_accuracy_rate)
    r = float(retained_actionability)
    rdot = float(actionability_rate)
    e = float(retained_exclusivity)
    edot = float(exclusivity_rate)
    cdot = _nonnegative_finite("marginal_wait_cost", marginal_wait_cost)

    for name, value in (
        ("cue_accuracy", q),
        ("cue_accuracy_rate", qdot),
        ("retained_actionability", r),
        ("actionability_rate", rdot),
        ("retained_exclusivity", e),
        ("exclusivity_rate", edot),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")

    if q <= geom.actionable_cue_accuracy + _TOL:
        raise ValueError(
            "cue_accuracy must be strictly above the canonical actionability boundary"
        )
    if q > 1.0:
        raise ValueError("cue_accuracy must not exceed one")
    if not 0.0 <= r <= 1.0:
        raise ValueError("retained_actionability must lie in [0, 1]")
    if not 0.0 <= e <= 1.0:
        raise ValueError("retained_exclusivity must lie in [0, 1]")

    value = geom.total_loss_scale * q - geom.larger_prior_action_loss
    gain = r * e * geom.total_loss_scale * qdot
    actionability_change = rdot * e * value
    exclusivity_change = r * edot * value
    derivative = (
        gain
        + actionability_change
        + exclusivity_change
        - cdot
    )

    if value > _TOL and r > _TOL and e > _TOL:
        relative_gain = geom.total_loss_scale * qdot / value
        relative_actionability_loss = -rdot / r
        relative_exclusivity_loss = -edot / e
    else:
        relative_gain = None
        relative_actionability_loss = None
        relative_exclusivity_loss = None

    return CompetitiveBalanceDerivative(
        cue_accuracy=q,
        cue_accuracy_rate=qdot,
        retained_actionability=r,
        actionability_rate=rdot,
        retained_exclusivity=e,
        exclusivity_rate=edot,
        marginal_wait_cost=cdot,
        information_value=value,
        information_gain_term=gain,
        actionability_change_term=actionability_change,
        exclusivity_change_term=exclusivity_change,
        net_derivative=derivative,
        relative_information_gain=relative_gain,
        relative_actionability_loss=relative_actionability_loss,
        relative_exclusivity_loss=relative_exclusivity_loss,
    )


def exponential_competitive_information_peak(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    cue_gain_amplitude: float,
    alpha_information_rate: float,
    beta_actionability_decay: float,
    gamma_exclusivity_decay: float,
) -> CompetitiveInformationPeak:
    """Return the unique peak for exponential learning and value decay.

    Cue quality rises from the canonical PAYOFF-B actionability boundary:

        q(t)=q0+Delta_q(1-exp(-alpha t)).

    Retained actionability and retained exclusivity are

        r(t)=exp(-beta t)
        e(t)=exp(-gamma t).

    At least one of beta or gamma must be positive.  With zero direct waiting
    cost,

        N(t)=S Delta_q exp(-(beta+gamma)t)(1-exp(-alpha t))

    has the unique interior maximum

        t*=log(1+alpha/(beta+gamma))/alpha.
    """

    geom = canonical_actionability_geometry(
        prior_early,
        false_early_cost,
        missed_early_cost,
    )

    delta = _positive_finite("cue_gain_amplitude", cue_gain_amplitude)
    alpha = _positive_finite("alpha_information_rate", alpha_information_rate)
    beta = _nonnegative_finite(
        "beta_actionability_decay",
        beta_actionability_decay,
    )
    gamma = _nonnegative_finite(
        "gamma_exclusivity_decay",
        gamma_exclusivity_decay,
    )
    decay = beta + gamma
    if decay <= _TOL:
        raise ValueError(
            "at least one of actionability decay or exclusivity decay must be positive"
        )

    available = 1.0 - geom.actionable_cue_accuracy
    if delta > available + _TOL:
        raise ValueError(
            "cue_gain_amplitude exceeds the remaining cue-accuracy range"
        )

    t_star = log(1.0 + alpha / decay) / alpha
    exp_alpha = exp(-alpha * t_star)
    q_star = geom.actionable_cue_accuracy + delta * (1.0 - exp_alpha)
    r_star = exp(-beta * t_star)
    e_star = exp(-gamma * t_star)
    max_value = (
        geom.total_loss_scale
        * delta
        * r_star
        * e_star
        * (1.0 - exp_alpha)
    )

    return CompetitiveInformationPeak(
        alpha_information_rate=alpha,
        beta_actionability_decay=beta,
        gamma_exclusivity_decay=gamma,
        total_value_decay=decay,
        cue_gain_amplitude=delta,
        total_loss_scale=geom.total_loss_scale,
        actionable_cue_accuracy=geom.actionable_cue_accuracy,
        optimal_time=t_star,
        optimal_cue_accuracy=q_star,
        retained_actionability_at_optimum=r_star,
        retained_exclusivity_at_optimum=e_star,
        maximum_gross_information_value=max_value,
    )
