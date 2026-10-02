"""Continuous information-actionability tradeoff for PAYOFF-B.

Prospective extension only. This module does not alter the frozen GEB Paper 2
submission.

Inside the actionable region of the canonical binary information model,

    V_A(q) = S q - B,

where S=A+L and B=max(A,L). If only a reduced-form fraction r(t) of the later
cue remains behaviorally actionable and cumulative waiting cost is D(t), define

    F(t) = r(t) [S q(t) - B] - D(t).

At an interior optimum with q above the actionability kink and r>0,

    F'(t)
      = r'(t)[S q(t)-B] + r(t) S q'(t) - D'(t)
      = 0.

Equivalently,

    S q'(t) / [S q(t)-B]
      = -r'(t)/r(t)
        + D'(t) / {r(t)[S q(t)-B]}.

Thus the relative rate of information improvement must balance recourse
attrition plus the marginal waiting-cost burden.

For the canonical exponential witness

    q(t)=q0+(1-q0)(1-exp(-alpha t)),
    r(t)=exp(-beta t),
    D(t)=0,

the unique finite optimum for alpha,beta>0 is

    t* = log(1 + alpha/beta) / alpha.

This is a closed-form ecological specialization of standard optimal-stopping /
value-of-information logic, not a generic novelty claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log1p

from src.endogenous_information_timing import (
    closed_form_information_threshold,
)


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
class ContinuousActionabilityBalance:
    """One continuous-time point in the active information region."""

    cue_accuracy: float
    retained_actionability: float
    cumulative_wait_cost: float
    canonical_information_value: float
    actionable_information_value: float
    net_value: float
    net_derivative: float
    relative_information_gain_rate: float
    recourse_attrition_rate: float
    marginal_wait_cost_rate: float
    marginal_wait_cost_burden: float
    balance_residual: float


@dataclass(frozen=True)
class ExponentialActionabilityOptimum:
    """Closed-form optimum for exponential information gain and recourse loss."""

    information_rate: float
    recourse_decay_rate: float
    actionable_cue_accuracy: float
    optimal_time: float
    optimal_cue_accuracy: float
    optimal_recourse: float
    maximum_actionable_information_value: float
    relative_information_gain_rate: float
    recourse_attrition_rate: float


def continuous_actionability_balance(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    cue_accuracy: float,
    retained_actionability: float,
    cue_accuracy_rate: float,
    actionability_rate: float,
    cumulative_wait_cost: float = 0.0,
    marginal_wait_cost_rate: float = 0.0,
) -> ContinuousActionabilityBalance:
    """Evaluate the exact first-order balance in the actionable region.

    Parameters
    ----------
    cue_accuracy_rate
        dq/dt.
    actionability_rate
        dr/dt. This is usually non-positive under increasing irreversibility.
    marginal_wait_cost_rate
        dD/dt.

    Notes
    -----
    The formula is smooth only above the canonical information-actionability
    kink q0=B/S. At or below q0 this function fails closed rather than assigning
    an arbitrary derivative through the max(0,.) kink.
    """

    q = float(cue_accuracy)
    r = float(retained_actionability)
    qdot = float(cue_accuracy_rate)
    rdot = float(actionability_rate)
    D = _nonnegative_finite("cumulative_wait_cost", cumulative_wait_cost)
    Ddot = _nonnegative_finite(
        "marginal_wait_cost_rate",
        marginal_wait_cost_rate,
    )
    if not isfinite(q) or q < 0.5 or q > 1.0:
        raise ValueError("cue_accuracy must lie in [0.5, 1]")
    if not isfinite(r) or r <= 0.0 or r > 1.0:
        raise ValueError("retained_actionability must lie in (0, 1]")
    if not isfinite(qdot):
        raise ValueError("cue_accuracy_rate must be finite")
    if not isfinite(rdot):
        raise ValueError("actionability_rate must be finite")

    base = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=0.0,
    )
    q0 = base.actionable_cue_accuracy
    if q <= q0 + _TOL:
        raise ValueError(
            "continuous balance is defined only above the actionable cue kink"
        )

    S = base.early_action_prior_loss + base.late_action_prior_loss
    B = max(
        base.early_action_prior_loss,
        base.late_action_prior_loss,
    )
    canonical = S * q - B
    actionable = r * canonical
    net = actionable - D

    derivative = rdot * canonical + r * S * qdot - Ddot
    relative_info = S * qdot / canonical
    attrition = -rdot / r
    marginal_burden = Ddot / actionable
    residual = relative_info - attrition - marginal_burden

    # Algebraic consistency guard.
    if abs(derivative - actionable * residual) > 1e-9:
        raise AssertionError("continuous first-order decomposition mismatch")

    return ContinuousActionabilityBalance(
        cue_accuracy=q,
        retained_actionability=r,
        cumulative_wait_cost=D,
        canonical_information_value=canonical,
        actionable_information_value=actionable,
        net_value=net,
        net_derivative=derivative,
        relative_information_gain_rate=relative_info,
        recourse_attrition_rate=attrition,
        marginal_wait_cost_rate=Ddot,
        marginal_wait_cost_burden=marginal_burden,
        balance_residual=residual,
    )


def exponential_information_actionability_optimum(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    information_rate: float,
    recourse_decay_rate: float,
) -> ExponentialActionabilityOptimum:
    """Closed-form zero-wait-cost optimum for exponential q gain and r loss.

    The declared trajectories are

        q(t) = q0 + (1-q0)(1-exp(-alpha t))
        r(t) = exp(-beta t),

    with alpha>0 and beta>0.

    The actionable information value is

        r(t) S [q(t)-q0],

    which is strictly zero at t=0, rises, then falls to zero as t->infinity.
    Its unique maximizer is

        t* = log(1+alpha/beta)/alpha.
    """

    alpha = _positive_finite("information_rate", information_rate)
    beta = _positive_finite("recourse_decay_rate", recourse_decay_rate)

    base = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=0.0,
    )
    q0 = base.actionable_cue_accuracy
    S = base.early_action_prior_loss + base.late_action_prior_loss

    t_star = log1p(alpha / beta) / alpha
    exp_alpha = beta / (alpha + beta)
    q_star = q0 + (1.0 - q0) * (1.0 - exp_alpha)
    r_star = exp(-beta * t_star)
    max_value = r_star * S * (q_star - q0)

    qdot_star = (1.0 - q0) * alpha * exp_alpha
    relative_info = S * qdot_star / (S * (q_star - q0))

    return ExponentialActionabilityOptimum(
        information_rate=alpha,
        recourse_decay_rate=beta,
        actionable_cue_accuracy=q0,
        optimal_time=t_star,
        optimal_cue_accuracy=q_star,
        optimal_recourse=r_star,
        maximum_actionable_information_value=max_value,
        relative_information_gain_rate=relative_info,
        recourse_attrition_rate=beta,
    )


def exponential_actionability_value(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    information_rate: float,
    recourse_decay_rate: float,
    time: float,
) -> float:
    """Evaluate the exponential-witness actionable information value at time t."""

    alpha = _positive_finite("information_rate", information_rate)
    beta = _positive_finite("recourse_decay_rate", recourse_decay_rate)
    t = _nonnegative_finite("time", time)

    base = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=0.0,
    )
    q0 = base.actionable_cue_accuracy
    S = base.early_action_prior_loss + base.late_action_prior_loss

    q = q0 + (1.0 - q0) * (1.0 - exp(-alpha * t))
    r = exp(-beta * t)
    return r * S * max(0.0, q - q0)
