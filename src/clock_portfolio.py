"""Optimal allocation between entry-clock precision and downstream feedback.

Post-freeze PAYOFF-B extension.

Let baseline entry-phase variance be V_ref.  Investment x>=0 in the
developmental/physiological entry clock reduces that variance to

    V0 = V_ref * exp(-x).

Let y>=0 denote per-checkpoint feedback effort, parameterized so that

    |lambda| = exp(-y).

After n equivalent post-entry correction checkpoints and no new process
innovation,

    Vn = V_ref * exp[-(x + 2 n y)].

For a target V_target < V_ref, define required log-precision

    P = log(V_ref / V_target).

Under convex effort costs

    C = (a/2) x^2 + (b/2) y^2,

the unique minimum-cost portfolio on x + 2 n y = P is

    x* = b P / (b + 4 n^2 a),
    y* = 2 n a P / (b + 4 n^2 a).

This formalizes partial substitution between a precise entry clock and repeated
post-entry correction.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log


@dataclass(frozen=True)
class ClockPortfolio:
    baseline_variance: float
    target_variance: float
    checkpoints: int
    timer_cost_curvature: float
    feedback_cost_curvature: float
    required_log_precision: float
    timer_effort: float
    feedback_effort_per_checkpoint: float
    timer_precision_share: float
    feedback_precision_share: float
    achieved_variance: float
    minimum_cost: float
    absolute_phase_retention: float


def _finite_positive(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x) or x <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return x


def _nonnegative_int(name: str, value: int) -> int:
    x = int(value)
    if x < 0 or x != value:
        raise ValueError(f"{name} must be a non-negative integer")
    return x


def final_variance_from_portfolio(
    baseline_variance: float,
    *,
    timer_effort: float,
    feedback_effort_per_checkpoint: float,
    checkpoints: int,
) -> float:
    """Return Vn = Vref exp[-x - 2ny]."""

    vref = _finite_positive("baseline_variance", baseline_variance)
    x = float(timer_effort)
    y = float(feedback_effort_per_checkpoint)
    if not isfinite(x) or x < 0.0:
        raise ValueError("timer_effort must be finite and non-negative")
    if not isfinite(y) or y < 0.0:
        raise ValueError(
            "feedback_effort_per_checkpoint must be finite and non-negative"
        )
    n = _nonnegative_int("checkpoints", checkpoints)
    return vref * exp(-(x + 2.0 * n * y))


def optimal_clock_portfolio(
    baseline_variance: float,
    target_variance: float,
    *,
    checkpoints: int,
    timer_cost_curvature: float,
    feedback_cost_curvature: float,
) -> ClockPortfolio:
    """Return the minimum-cost timer/feedback precision portfolio.

    If n=0 there is no downstream feedback route and all required precision must
    be supplied by the entry clock.

    For n>0, the interior quadratic optimum is exact.
    """

    vref = _finite_positive("baseline_variance", baseline_variance)
    vt = _finite_positive("target_variance", target_variance)
    if vt > vref:
        raise ValueError("target_variance must not exceed baseline_variance")

    n = _nonnegative_int("checkpoints", checkpoints)
    a = _finite_positive("timer_cost_curvature", timer_cost_curvature)
    b = _finite_positive("feedback_cost_curvature", feedback_cost_curvature)

    P = log(vref / vt)
    if P == 0.0:
        return ClockPortfolio(
            baseline_variance=vref,
            target_variance=vt,
            checkpoints=n,
            timer_cost_curvature=a,
            feedback_cost_curvature=b,
            required_log_precision=0.0,
            timer_effort=0.0,
            feedback_effort_per_checkpoint=0.0,
            timer_precision_share=0.0,
            feedback_precision_share=0.0,
            achieved_variance=vref,
            minimum_cost=0.0,
            absolute_phase_retention=1.0,
        )

    if n == 0:
        x = P
        y = 0.0
        timer_share = 1.0
        feedback_share = 0.0
    else:
        denom = b + 4.0 * n * n * a
        x = b * P / denom
        y = 2.0 * n * a * P / denom
        timer_share = x / P
        feedback_share = 2.0 * n * y / P

    achieved = final_variance_from_portfolio(
        vref,
        timer_effort=x,
        feedback_effort_per_checkpoint=y,
        checkpoints=n,
    )
    cost = 0.5 * a * x * x + 0.5 * b * y * y
    lam_abs = exp(-y)

    return ClockPortfolio(
        baseline_variance=vref,
        target_variance=vt,
        checkpoints=n,
        timer_cost_curvature=a,
        feedback_cost_curvature=b,
        required_log_precision=P,
        timer_effort=x,
        feedback_effort_per_checkpoint=y,
        timer_precision_share=timer_share,
        feedback_precision_share=feedback_share,
        achieved_variance=achieved,
        minimum_cost=cost,
        absolute_phase_retention=lam_abs,
    )


def clock_portfolio_precision_shares(
    *,
    checkpoints: int,
    timer_cost_curvature: float,
    feedback_cost_curvature: float,
) -> tuple[float, float]:
    """Return timer and feedback shares of required log-precision.

    For n>0,

        s_timer = b / (b + 4 n^2 a),
        s_feedback = 4 n^2 a / (b + 4 n^2 a).

    The shares do not depend on the target precision under quadratic costs.
    """

    n = _nonnegative_int("checkpoints", checkpoints)
    a = _finite_positive("timer_cost_curvature", timer_cost_curvature)
    b = _finite_positive("feedback_cost_curvature", feedback_cost_curvature)

    if n == 0:
        return 1.0, 0.0
    denom = b + 4.0 * n * n * a
    return b / denom, 4.0 * n * n * a / denom
