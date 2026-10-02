"""Continuous information-actionability balance for prospective PAYOFF-B theory.

This module extends the frozen Paper-2 information-deadline geometry without
retuning the submitted GEB manuscript.

Generic sequential value-of-information and optimal-stopping theory are prior
art. The purpose here is narrower: derive exact closed-form consequences of the
declared PAYOFF-B reduced model in which cue quality improves through time while
retained actionability decays.

Above the canonical actionability boundary q0=B/S,

    V_A(q) = S q - B.

If only a fraction r(t) of full state-contingent actionability remains and
cumulative waiting cost is C(t), the prospective net value of waiting until t is

    N(t) = r(t) [S q(t) - B] - C(t).

For differentiable paths, any interior stationary point above q0 obeys

    r S q_dot + r_dot (S q - B) = C_dot.

With zero marginal waiting cost,

    S q_dot / (S q - B) = - r_dot / r,

so the relative rate of information-value gain equals the relative rate of
optionality loss.

A canonical closed form follows when cue quality rises exponentially from the
actionability boundary while recourse decays exponentially:

    q(t) = q0 + Delta_q (1-exp(-alpha t)),
    r(t) = exp(-beta t).

Then

    N(t) = S Delta_q exp(-beta t)(1-exp(-alpha t))

has a unique interior maximum

    t* = log(1 + alpha/beta) / alpha.

Faster recourse decay beta therefore moves commitment earlier even when two
actors observe the same improving cue trajectory.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log

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
class CanonicalActionabilityGeometry:
    """Canonical Paper-2 loss geometry used by the continuous extension."""

    prior_early: float
    false_early_cost: float
    missed_early_cost: float
    early_action_prior_loss: float
    late_action_prior_loss: float
    total_loss_scale: float
    larger_prior_action_loss: float
    prior_bayes_risk: float
    actionable_cue_accuracy: float


@dataclass(frozen=True)
class ContinuousBalanceDerivative:
    """Derivative decomposition for N(t)=r(t)V_A(q(t))-C(t)."""

    cue_accuracy: float
    cue_accuracy_rate: float
    retained_actionability: float
    actionability_rate: float
    marginal_wait_cost: float
    information_value: float
    information_gain_term: float
    actionability_loss_term: float
    net_derivative: float
    zero_cost_relative_information_gain: float | None
    zero_cost_relative_actionability_loss: float | None


@dataclass(frozen=True)
class ExponentialActionabilityPeak:
    """Closed-form peak under exponential learning and recourse decay."""

    alpha_information_rate: float
    beta_actionability_decay: float
    cue_gain_amplitude: float
    total_loss_scale: float
    actionable_cue_accuracy: float
    optimal_time: float
    optimal_cue_accuracy: float
    retained_actionability_at_optimum: float
    maximum_gross_information_value: float


@dataclass(frozen=True)
class PairwiseExponentialCommitmentGap:
    """Two-actor commitment-time divergence under a shared cue trajectory."""

    alpha_information_rate: float
    actor_1_beta: float
    actor_2_beta: float
    actor_1_optimal_time: float
    actor_2_optimal_time: float
    absolute_time_gap: float
    earlier_committing_actor: int | None


@dataclass(frozen=True)
class LinearWaitCostPeak:
    """Optimal time when exponential actionability value pays a linear wait cost."""

    alpha_information_rate: float
    beta_actionability_decay: float
    gross_scale: float
    marginal_wait_cost: float
    zero_cost_peak_time: float
    optimal_time: float
    immediate_commitment: bool
    net_value_at_optimum: float


def canonical_actionability_geometry(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
) -> CanonicalActionabilityGeometry:
    """Return the canonical Paper-2 binary loss geometry."""

    base = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=0.0,
    )
    early = float(base.early_action_prior_loss)
    late = float(base.late_action_prior_loss)
    total = early + late
    if total <= 0.0:
        raise ValueError("canonical total loss scale must be positive")

    return CanonicalActionabilityGeometry(
        prior_early=float(prior_early),
        false_early_cost=float(false_early_cost),
        missed_early_cost=float(missed_early_cost),
        early_action_prior_loss=early,
        late_action_prior_loss=late,
        total_loss_scale=total,
        larger_prior_action_loss=max(early, late),
        prior_bayes_risk=float(base.prior_bayes_risk),
        actionable_cue_accuracy=float(base.actionable_cue_accuracy),
    )


def continuous_balance_derivative(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    cue_accuracy: float,
    cue_accuracy_rate: float,
    retained_actionability: float,
    actionability_rate: float,
    marginal_wait_cost: float = 0.0,
) -> ContinuousBalanceDerivative:
    """Evaluate d/dt of r(t)V_A(q(t))-C(t) above the actionability boundary.

    The function deliberately fails closed below q0 because the canonical
    Paper-2 information value is flat there. At q=q0, a one-sided derivative
    may be used externally if biologically justified.
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
    cdot = _nonnegative_finite("marginal_wait_cost", marginal_wait_cost)

    for name, value in (
        ("cue_accuracy", q),
        ("cue_accuracy_rate", qdot),
        ("retained_actionability", r),
        ("actionability_rate", rdot),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")

    if q <= geom.actionable_cue_accuracy + _TOL:
        raise ValueError(
            "cue_accuracy must be strictly above the canonical actionability boundary"
        )
    if q > 1.0:
        raise ValueError("cue_accuracy must not exceed one")
    if r < 0.0 or r > 1.0:
        raise ValueError("retained_actionability must lie in [0, 1]")

    value = (
        geom.total_loss_scale * q
        - geom.larger_prior_action_loss
    )
    gain = r * geom.total_loss_scale * qdot
    loss = rdot * value
    derivative = gain + loss - cdot

    if r > _TOL and value > _TOL:
        relative_gain = geom.total_loss_scale * qdot / value
        relative_loss = -rdot / r
    else:
        relative_gain = None
        relative_loss = None

    return ContinuousBalanceDerivative(
        cue_accuracy=q,
        cue_accuracy_rate=qdot,
        retained_actionability=r,
        actionability_rate=rdot,
        marginal_wait_cost=cdot,
        information_value=value,
        information_gain_term=gain,
        actionability_loss_term=loss,
        net_derivative=derivative,
        zero_cost_relative_information_gain=relative_gain,
        zero_cost_relative_actionability_loss=relative_loss,
    )


def exponential_actionability_peak(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    cue_gain_amplitude: float,
    alpha_information_rate: float,
    beta_actionability_decay: float,
) -> ExponentialActionabilityPeak:
    """Closed-form unique peak for exponential learning and recourse decay.

    The cue path starts exactly at the canonical actionability boundary:

        q(t)=q0+Delta_q(1-exp(-alpha t)).

    Delta_q must fit within the probability scale:
        0 < Delta_q <= 1-q0.

    Recourse is
        r(t)=exp(-beta t).

    With no additional waiting cost, the gross actionable-information value has
    the unique interior maximum

        t*=log(1+alpha/beta)/alpha.
    """

    geom = canonical_actionability_geometry(
        prior_early,
        false_early_cost,
        missed_early_cost,
    )
    delta = _positive_finite("cue_gain_amplitude", cue_gain_amplitude)
    alpha = _positive_finite("alpha_information_rate", alpha_information_rate)
    beta = _positive_finite(
        "beta_actionability_decay", beta_actionability_decay
    )

    available = 1.0 - geom.actionable_cue_accuracy
    if delta > available + _TOL:
        raise ValueError(
            "cue_gain_amplitude exceeds the remaining cue-accuracy range"
        )

    t_star = log(1.0 + alpha / beta) / alpha
    exp_alpha = exp(-alpha * t_star)
    q_star = geom.actionable_cue_accuracy + delta * (1.0 - exp_alpha)
    r_star = exp(-beta * t_star)
    max_value = (
        r_star
        * geom.total_loss_scale
        * delta
        * (1.0 - exp_alpha)
    )

    return ExponentialActionabilityPeak(
        alpha_information_rate=alpha,
        beta_actionability_decay=beta,
        cue_gain_amplitude=delta,
        total_loss_scale=geom.total_loss_scale,
        actionable_cue_accuracy=geom.actionable_cue_accuracy,
        optimal_time=t_star,
        optimal_cue_accuracy=q_star,
        retained_actionability_at_optimum=r_star,
        maximum_gross_information_value=max_value,
    )


def pairwise_exponential_commitment_gap(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    cue_gain_amplitude: float,
    alpha_information_rate: float,
    actor_1_beta: float,
    actor_2_beta: float,
) -> PairwiseExponentialCommitmentGap:
    """Exact commitment-time gap caused only by different recourse decay rates."""

    one = exponential_actionability_peak(
        prior_early,
        false_early_cost,
        missed_early_cost,
        cue_gain_amplitude=cue_gain_amplitude,
        alpha_information_rate=alpha_information_rate,
        beta_actionability_decay=actor_1_beta,
    )
    two = exponential_actionability_peak(
        prior_early,
        false_early_cost,
        missed_early_cost,
        cue_gain_amplitude=cue_gain_amplitude,
        alpha_information_rate=alpha_information_rate,
        beta_actionability_decay=actor_2_beta,
    )
    gap = abs(one.optimal_time - two.optimal_time)
    if gap <= _TOL:
        earlier = None
    elif one.optimal_time < two.optimal_time:
        earlier = 1
    else:
        earlier = 2

    return PairwiseExponentialCommitmentGap(
        alpha_information_rate=float(alpha_information_rate),
        actor_1_beta=float(actor_1_beta),
        actor_2_beta=float(actor_2_beta),
        actor_1_optimal_time=one.optimal_time,
        actor_2_optimal_time=two.optimal_time,
        absolute_time_gap=gap,
        earlier_committing_actor=earlier,
    )


def _exponential_gross_value(
    t: float,
    *,
    gross_scale: float,
    alpha: float,
    beta: float,
) -> float:
    return gross_scale * exp(-beta * t) * (1.0 - exp(-alpha * t))


def _exponential_gross_derivative(
    t: float,
    *,
    gross_scale: float,
    alpha: float,
    beta: float,
) -> float:
    return gross_scale * exp(-beta * t) * (
        (alpha + beta) * exp(-alpha * t) - beta
    )



@dataclass(frozen=True)
class ExponentialInformationUseWindow:
    """Time interval where actionable information exceeds a fixed deadline cost."""

    alpha_information_rate: float
    beta_actionability_decay: float
    gross_scale: float
    deadline_cost: float
    peak_time: float
    maximum_gross_value: float
    status: str
    start_time: float | None
    end_time: float | None


def exponential_information_use_window(
    *,
    gross_scale: float,
    alpha_information_rate: float,
    beta_actionability_decay: float,
    deadline_cost: float,
) -> ExponentialInformationUseWindow:
    """Return the exact qualitative time window where G(t)>D.

    Let

        G(t)=K exp(-beta t)[1-exp(-alpha t)],

    with K, alpha, beta > 0 and D >= 0.

    G(0)=0, G(infinity)=0, and G has one strict interior maximum. Therefore:

    - D > G_max: information is never worth using;
    - D = G_max: there is one tangency/indifference time;
    - 0 < D < G_max: there are exactly two crossings and information is worth
      using only on the finite interval (t_start, t_end);
    - D = 0: every finite t>0 has positive gross value, so the positive-value
      interval is (0, infinity).

    Roots are computed by deterministic bisection. The theorem itself follows
    from strict unimodality of G.
    """

    scale = _positive_finite("gross_scale", gross_scale)
    alpha = _positive_finite("alpha_information_rate", alpha_information_rate)
    beta = _positive_finite(
        "beta_actionability_decay", beta_actionability_decay
    )
    deadline = _nonnegative_finite("deadline_cost", deadline_cost)

    peak = log(1.0 + alpha / beta) / alpha
    gmax = _exponential_gross_value(
        peak,
        gross_scale=scale,
        alpha=alpha,
        beta=beta,
    )

    if deadline <= _TOL:
        return ExponentialInformationUseWindow(
            alpha_information_rate=alpha,
            beta_actionability_decay=beta,
            gross_scale=scale,
            deadline_cost=deadline,
            peak_time=peak,
            maximum_gross_value=gmax,
            status="POSITIVE_FOR_ALL_FINITE_T_AFTER_ZERO",
            start_time=0.0,
            end_time=None,
        )

    if deadline > gmax + _TOL:
        return ExponentialInformationUseWindow(
            alpha_information_rate=alpha,
            beta_actionability_decay=beta,
            gross_scale=scale,
            deadline_cost=deadline,
            peak_time=peak,
            maximum_gross_value=gmax,
            status="NEVER_USE",
            start_time=None,
            end_time=None,
        )

    if abs(deadline - gmax) <= _TOL:
        return ExponentialInformationUseWindow(
            alpha_information_rate=alpha,
            beta_actionability_decay=beta,
            gross_scale=scale,
            deadline_cost=deadline,
            peak_time=peak,
            maximum_gross_value=gmax,
            status="TANGENT_AT_PEAK",
            start_time=peak,
            end_time=peak,
        )

    def excess(t: float) -> float:
        return _exponential_gross_value(
            t,
            gross_scale=scale,
            alpha=alpha,
            beta=beta,
        ) - deadline

    lo, hi = 0.0, peak
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if excess(mid) > 0.0:
            hi = mid
        else:
            lo = mid
    start = 0.5 * (lo + hi)

    lo = peak
    hi = max(2.0 * peak, peak + 1.0 / min(alpha, beta))
    while excess(hi) > 0.0:
        hi *= 2.0
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if excess(mid) > 0.0:
            lo = mid
        else:
            hi = mid
    end = 0.5 * (lo + hi)

    return ExponentialInformationUseWindow(
        alpha_information_rate=alpha,
        beta_actionability_decay=beta,
        gross_scale=scale,
        deadline_cost=deadline,
        peak_time=peak,
        maximum_gross_value=gmax,
        status="FINITE_USE_WINDOW",
        start_time=start,
        end_time=end,
    )


def equal_rate_information_use_window_closed_form(
    *,
    gross_scale: float,
    common_rate: float,
    deadline_cost: float,
) -> tuple[float, float] | None:
    """Closed-form finite use window for alpha=beta=lambda.

    For x=exp(-lambda t),

        G/K=x(1-x).

    A finite strict-use window exists iff 0 < D/K < 1/4. The two crossings are

        x_early=(1+sqrt(1-4D/K))/2,
        x_late =(1-sqrt(1-4D/K))/2,

    with t=-log(x)/lambda.
    """

    from math import sqrt

    scale = _positive_finite("gross_scale", gross_scale)
    rate = _positive_finite("common_rate", common_rate)
    deadline = _nonnegative_finite("deadline_cost", deadline_cost)
    ratio = deadline / scale
    if ratio <= 0.0 or ratio >= 0.25:
        return None

    disc = sqrt(1.0 - 4.0 * ratio)
    x_early = 0.5 * (1.0 + disc)
    x_late = 0.5 * (1.0 - disc)
    return (
        -log(x_early) / rate,
        -log(x_late) / rate,
    )

def exponential_peak_with_linear_wait_cost(
    *,
    gross_scale: float,
    alpha_information_rate: float,
    beta_actionability_decay: float,
    marginal_wait_cost: float,
) -> LinearWaitCostPeak:
    """Peak of K e^-beta*t(1-e^-alpha*t) - c t.

    If c >= K alpha, the derivative at t=0 is non-positive and immediate
    commitment is optimal.

    Otherwise there is exactly one root of

        K e^-beta*t[(alpha+beta)e^-alpha*t-beta] = c

    in (0, t0), where t0 is the zero-cost peak. Bisection is deterministic
    because the gross derivative is strictly decreasing on that interval.
    """

    scale = _positive_finite("gross_scale", gross_scale)
    alpha = _positive_finite("alpha_information_rate", alpha_information_rate)
    beta = _positive_finite(
        "beta_actionability_decay", beta_actionability_decay
    )
    cost = _nonnegative_finite("marginal_wait_cost", marginal_wait_cost)

    t0 = log(1.0 + alpha / beta) / alpha
    if cost >= scale * alpha - _TOL:
        optimum = 0.0
        immediate = True
    elif cost <= _TOL:
        optimum = t0
        immediate = False
    else:
        lo, hi = 0.0, t0
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            slope = _exponential_gross_derivative(
                mid,
                gross_scale=scale,
                alpha=alpha,
                beta=beta,
            ) - cost
            if slope > 0.0:
                lo = mid
            else:
                hi = mid
        optimum = 0.5 * (lo + hi)
        immediate = False

    gross = _exponential_gross_value(
        optimum,
        gross_scale=scale,
        alpha=alpha,
        beta=beta,
    )
    net = gross - cost * optimum
    return LinearWaitCostPeak(
        alpha_information_rate=alpha,
        beta_actionability_decay=beta,
        gross_scale=scale,
        marginal_wait_cost=cost,
        zero_cost_peak_time=t0,
        optimal_time=optimum,
        immediate_commitment=immediate,
        net_value_at_optimum=net,
    )
