"""Heterogeneous correction opportunities in seasonal clock portfolios.

Post-freeze PAYOFF-B theory.

The canonical clock-portfolio model treats downstream correction opportunity
through a checkpoint count n or a single retained fraction omega.  Natural
routes are heterogeneous: one stopover can be much more useful for phase
correction than another, and substitutes can preserve effective opportunity
even when named sites are lost.

This module gives an exact weighted generalization.

Independent checkpoint-capacity model
-------------------------------------
Let checkpoint j have correction leverage c_j >= 0 and quadratic effort-cost
curvature b_j > 0.  Timer effort x has cost curvature a > 0.

Required log-precision P is supplied by

    x + 2 sum_j c_j y_j = P

at cost

    C = (a/2) x^2 + sum_j (b_j/2) y_j^2.

Define weighted route leverage

    L = sum_j c_j^2 / b_j.

The exact optimum is

    x* = P / (1 + 4 a L)

    y_j* = 2 a P c_j / [b_j (1 + 4 a L)]

and feedback precision share is

    s_F = 4 a L / (1 + 4 a L).

If disruption retains fraction o_j of checkpoint j's usable correction
opportunity, the effective opportunity-retention fraction under the historical
allocation is

    omega_eff =
        [sum_j o_j c_j^2/b_j] /
        [sum_j c_j^2/b_j].

Immediate variance inflation is therefore

    F = exp[(1-omega_eff) s_F P].

Thus named-site loss is not the relevant quantity.  The relevant loss is
weighted by each checkpoint's historical precision contribution.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log
from typing import Sequence


_TOL = 1e-12


@dataclass(frozen=True)
class WeightedClockPortfolio:
    baseline_variance: float
    target_variance: float
    required_log_precision: float
    timer_cost_curvature: float
    checkpoint_leverages: tuple[float, ...]
    checkpoint_cost_curvatures: tuple[float, ...]
    route_leverage: float
    timer_effort: float
    checkpoint_efforts: tuple[float, ...]
    timer_precision_share: float
    feedback_precision_share: float
    checkpoint_feedback_shares: tuple[float, ...]
    minimum_cost: float
    achieved_variance: float


@dataclass(frozen=True)
class WeightedOpportunityLoss:
    historical_feedback_precision_share: float
    required_log_precision: float
    checkpoint_retention: tuple[float, ...]
    checkpoint_feedback_shares: tuple[float, ...]
    effective_opportunity_retention: float
    effective_opportunity_loss: float
    variance_inflation_factor: float
    disrupted_variance: float


@dataclass(frozen=True)
class SharedCapacityPortfolio:
    baseline_variance: float
    target_variance: float
    required_log_precision: float
    timer_cost_curvature: float
    feedback_capacity_cost_curvature: float
    total_leverage: float
    timer_precision_share: float
    feedback_precision_share: float
    timer_effort: float
    shared_feedback_effort: float
    minimum_cost: float


def _finite(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _positive(name: str, value: float) -> float:
    x = _finite(name, value)
    if x <= 0.0:
        raise ValueError(f"{name} must be positive")
    return x


def _nonnegative(name: str, value: float) -> float:
    x = _finite(name, value)
    if x < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return x


def _unit(name: str, value: float) -> float:
    x = _finite(name, value)
    if x < 0.0 or x > 1.0:
        raise ValueError(f"{name} must lie in [0,1]")
    return x


def _validated_vectors(
    checkpoint_leverages: Sequence[float],
    checkpoint_cost_curvatures: Sequence[float],
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    c = tuple(_nonnegative("checkpoint_leverage", x) for x in checkpoint_leverages)
    b = tuple(
        _positive("checkpoint_cost_curvature", x)
        for x in checkpoint_cost_curvatures
    )
    if len(c) != len(b):
        raise ValueError("leverage and cost vectors must have equal length")
    if not c:
        raise ValueError("at least one checkpoint is required")
    return c, b


def weighted_route_leverage(
    checkpoint_leverages: Sequence[float],
    checkpoint_cost_curvatures: Sequence[float],
) -> float:
    """Return L = sum c_j^2 / b_j."""

    c, b = _validated_vectors(checkpoint_leverages, checkpoint_cost_curvatures)
    return sum(x * x / cost for x, cost in zip(c, b))


def optimal_weighted_clock_portfolio(
    baseline_variance: float,
    target_variance: float,
    *,
    timer_cost_curvature: float,
    checkpoint_leverages: Sequence[float],
    checkpoint_cost_curvatures: Sequence[float],
) -> WeightedClockPortfolio:
    """Return the exact minimum-cost heterogeneous checkpoint portfolio."""

    vref = _positive("baseline_variance", baseline_variance)
    vt = _positive("target_variance", target_variance)
    if vt > vref:
        raise ValueError("target_variance must not exceed baseline_variance")

    a = _positive("timer_cost_curvature", timer_cost_curvature)
    c, b = _validated_vectors(checkpoint_leverages, checkpoint_cost_curvatures)
    P = log(vref / vt)

    L = sum(x * x / cost for x, cost in zip(c, b))
    if P == 0.0:
        zero_efforts = tuple(0.0 for _ in c)
        zero_shares = tuple(0.0 for _ in c)
        return WeightedClockPortfolio(
            baseline_variance=vref,
            target_variance=vt,
            required_log_precision=0.0,
            timer_cost_curvature=a,
            checkpoint_leverages=c,
            checkpoint_cost_curvatures=b,
            route_leverage=L,
            timer_effort=0.0,
            checkpoint_efforts=zero_efforts,
            timer_precision_share=0.0,
            feedback_precision_share=0.0,
            checkpoint_feedback_shares=zero_shares,
            minimum_cost=0.0,
            achieved_variance=vref,
        )

    denom = 1.0 + 4.0 * a * L
    x = P / denom
    ys = tuple(
        2.0 * a * P * cj / (bj * denom)
        for cj, bj in zip(c, b)
    )

    downstream_log_precision = tuple(
        2.0 * cj * yj for cj, yj in zip(c, ys)
    )
    feedback_total = sum(downstream_log_precision)
    timer_share = x / P
    feedback_share = feedback_total / P
    checkpoint_shares = tuple(v / P for v in downstream_log_precision)

    achieved = vref * exp(-(x + feedback_total))
    cost = 0.5 * a * x * x + sum(
        0.5 * bj * yj * yj for bj, yj in zip(b, ys)
    )

    if abs(timer_share + feedback_share - 1.0) > 1e-10:
        raise AssertionError("precision shares do not sum to one")
    if abs(feedback_share - 4.0 * a * L / denom) > 1e-10:
        raise AssertionError("weighted feedback-share identity failed")
    if abs(cost - a * P * P / (2.0 * denom)) > 1e-10:
        raise AssertionError("weighted minimum-cost identity failed")

    return WeightedClockPortfolio(
        baseline_variance=vref,
        target_variance=vt,
        required_log_precision=P,
        timer_cost_curvature=a,
        checkpoint_leverages=c,
        checkpoint_cost_curvatures=b,
        route_leverage=L,
        timer_effort=x,
        checkpoint_efforts=ys,
        timer_precision_share=timer_share,
        feedback_precision_share=feedback_share,
        checkpoint_feedback_shares=checkpoint_shares,
        minimum_cost=cost,
        achieved_variance=achieved,
    )


def effective_opportunity_retention(
    checkpoint_leverages: Sequence[float],
    checkpoint_cost_curvatures: Sequence[float],
    checkpoint_retention: Sequence[float],
) -> float:
    """Return cost-adjusted retained opportunity under the optimal allocation.

    At the heterogeneous optimum, checkpoint j's historical downstream
    precision contribution is proportional to c_j^2/b_j.  Therefore

        omega_eff =
          sum o_j c_j^2/b_j / sum c_j^2/b_j.

    If all checkpoint leverages/costs are equal, this reduces to the arithmetic
    mean retention fraction.
    """

    c, b = _validated_vectors(checkpoint_leverages, checkpoint_cost_curvatures)
    o = tuple(_unit("checkpoint_retention", x) for x in checkpoint_retention)
    if len(o) != len(c):
        raise ValueError("retention and checkpoint vectors must have equal length")

    weights = tuple(cj * cj / bj for cj, bj in zip(c, b))
    total = sum(weights)
    if total <= _TOL:
        return 1.0
    return sum(oj * w for oj, w in zip(o, weights)) / total


def disrupted_weighted_portfolio(
    portfolio: WeightedClockPortfolio,
    *,
    checkpoint_retention: Sequence[float],
) -> WeightedOpportunityLoss:
    """Return immediate variance inflation under heterogeneous opportunity loss.

    Historical efforts are held fixed during the immediate perturbation.
    """

    o = tuple(_unit("checkpoint_retention", x) for x in checkpoint_retention)
    if len(o) != len(portfolio.checkpoint_efforts):
        raise ValueError("retention vector must match portfolio checkpoints")

    P = portfolio.required_log_precision
    if P == 0.0 or portfolio.feedback_precision_share == 0.0:
        return WeightedOpportunityLoss(
            historical_feedback_precision_share=portfolio.feedback_precision_share,
            required_log_precision=P,
            checkpoint_retention=o,
            checkpoint_feedback_shares=portfolio.checkpoint_feedback_shares,
            effective_opportunity_retention=1.0,
            effective_opportunity_loss=0.0,
            variance_inflation_factor=1.0,
            disrupted_variance=portfolio.target_variance,
        )

    feedback_total = portfolio.feedback_precision_share * P
    retained_feedback = sum(
        oj * share * P
        for oj, share in zip(o, portfolio.checkpoint_feedback_shares)
    )
    omega = retained_feedback / feedback_total
    loss = 1.0 - omega
    factor = exp(loss * feedback_total)

    direct_disrupted = portfolio.baseline_variance * exp(
        -(
            portfolio.timer_effort
            + retained_feedback
        )
    )
    if abs(direct_disrupted / portfolio.target_variance - factor) > 1e-10:
        raise AssertionError("heterogeneous opportunity-loss identity failed")

    return WeightedOpportunityLoss(
        historical_feedback_precision_share=portfolio.feedback_precision_share,
        required_log_precision=P,
        checkpoint_retention=o,
        checkpoint_feedback_shares=portfolio.checkpoint_feedback_shares,
        effective_opportunity_retention=omega,
        effective_opportunity_loss=loss,
        variance_inflation_factor=factor,
        disrupted_variance=direct_disrupted,
    )


def shared_capacity_clock_portfolio(
    baseline_variance: float,
    target_variance: float,
    *,
    timer_cost_curvature: float,
    feedback_capacity_cost_curvature: float,
    checkpoint_leverages: Sequence[float],
) -> SharedCapacityPortfolio:
    """Return the shared-capacity analogue.

    One feedback-capacity effort y is reused across all checkpoints:

        x + 2 y sum_j c_j = P

        C = (a/2)x^2 + (b/2)y^2.

    With total leverage C_route = sum c_j,

        s_F = 4 a C_route^2 / [b + 4 a C_route^2].

    Equal c_j=1 recovers the canonical n^2 scaling.
    """

    vref = _positive("baseline_variance", baseline_variance)
    vt = _positive("target_variance", target_variance)
    if vt > vref:
        raise ValueError("target_variance must not exceed baseline_variance")
    a = _positive("timer_cost_curvature", timer_cost_curvature)
    b = _positive(
        "feedback_capacity_cost_curvature",
        feedback_capacity_cost_curvature,
    )
    c = tuple(_nonnegative("checkpoint_leverage", x) for x in checkpoint_leverages)
    if not c:
        raise ValueError("at least one checkpoint is required")

    P = log(vref / vt)
    Croute = sum(c)
    if P == 0.0:
        return SharedCapacityPortfolio(
            baseline_variance=vref,
            target_variance=vt,
            required_log_precision=0.0,
            timer_cost_curvature=a,
            feedback_capacity_cost_curvature=b,
            total_leverage=Croute,
            timer_precision_share=0.0,
            feedback_precision_share=0.0,
            timer_effort=0.0,
            shared_feedback_effort=0.0,
            minimum_cost=0.0,
        )

    denom = b + 4.0 * a * Croute * Croute
    x = b * P / denom
    y = 2.0 * a * Croute * P / denom
    s_timer = x / P
    s_feedback = 2.0 * Croute * y / P
    cost = 0.5 * a * x * x + 0.5 * b * y * y

    return SharedCapacityPortfolio(
        baseline_variance=vref,
        target_variance=vt,
        required_log_precision=P,
        timer_cost_curvature=a,
        feedback_capacity_cost_curvature=b,
        total_leverage=Croute,
        timer_precision_share=s_timer,
        feedback_precision_share=s_feedback,
        timer_effort=x,
        shared_feedback_effort=y,
        minimum_cost=cost,
    )
