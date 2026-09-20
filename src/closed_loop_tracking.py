"""Closed-loop movement--phenology tracking around a moving environment.

This local linear control model is intentionally simpler than the explicit
landscape. It asks what happens when movement and timing are *feedback
channels* that respond to current phase/environment mismatch.

Let e_t be climate-equivalent mismatch. After any baseline spatial tracking,
let r be the residual environmental displacement per decision interval.

Movement-mediated feedback corrects fraction q_m of current mismatch and
phenology-mediated feedback corrects fraction q_h. Then

    e_(t+1) = (1 - q_m - q_h) e_t + r.

For the existing PAYOFF-B phenology rate h,

    q_h = 1 - exp(-h).

The model therefore separates:
- baseline tracking of the moving environment, and
- closed-loop correction of accumulated mismatch.

It provides an exact local bridge to empirical phase-error controller evidence
without relabeling route-distance controller slopes as the intrinsic timing
rate h.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, sqrt


_EPS = 1e-12


@dataclass(frozen=True)
class ClosedLoopTrackingResult:
    residual_forcing: float
    movement_feedback_gain: float
    phenology_feedback_gain: float
    total_feedback_gain: float
    multiplier: float
    stable: bool
    stability_class: str
    theoretical_equilibrium_mismatch: float | None
    final_mismatch: float
    mean_mismatch: float
    rms_mismatch: float


@dataclass(frozen=True)
class FeedbackAllocation:
    total_feedback_gain: float
    movement_feedback_gain: float
    phenology_feedback_gain: float
    movement_cost: float
    phenology_cost: float
    total_quadratic_cost: float


@dataclass(frozen=True)
class UnconstrainedFeedbackOptimum:
    residual_forcing: float
    mismatch_strength: float
    movement_cost: float
    phenology_cost: float
    effective_feedback_cost: float
    total_feedback_gain: float
    movement_feedback_gain: float
    phenology_feedback_gain: float
    equilibrium_mismatch: float
    objective_value: float
    stability_feasible: bool
    phenology_fraction_feasible: bool


def phenology_rate_to_feedback_gain(
    phenology_rate: float,
) -> float:
    """Convert existing PAYOFF-B h into first-order correction fraction q_h."""

    if not isfinite(phenology_rate) or phenology_rate < 0.0:
        raise ValueError(
            "phenology_rate must be non-negative and finite"
        )
    return 1.0 - exp(-phenology_rate)


def feedback_gain_to_phenology_rate(
    feedback_gain: float,
) -> float:
    """Invert q_h=1-exp(-h) for 0<=q_h<1."""

    if not isfinite(feedback_gain):
        raise ValueError("feedback_gain must be finite")
    if not 0.0 <= feedback_gain < 1.0:
        raise ValueError(
            "phenology feedback gain must lie in [0,1)"
        )
    if feedback_gain == 0.0:
        return 0.0
    return -__import__("math").log1p(-feedback_gain)


def classify_closed_loop_stability(
    total_feedback_gain: float,
) -> str:
    """Classify e_(t+1)=(1-K)e_t+r by total feedback gain K."""

    if not isfinite(total_feedback_gain):
        raise ValueError("total_feedback_gain must be finite")
    if total_feedback_gain < 0.0:
        return "anti_restoring_unstable"
    if total_feedback_gain == 0.0:
        return "no_feedback"
    if total_feedback_gain < 1.0:
        return "stable_monotone"
    if total_feedback_gain == 1.0:
        return "deadbeat_one_step"
    if total_feedback_gain < 2.0:
        return "stable_oscillatory"
    if total_feedback_gain == 2.0:
        return "neutral_two_cycle"
    return "oscillatory_unstable"


def closed_loop_equilibrium_mismatch(
    residual_forcing: float,
    movement_feedback_gain: float,
    phenology_feedback_gain: float,
) -> float | None:
    """Exact equilibrium mismatch when total restoring gain is positive."""

    for name, value in (
        ("residual_forcing", residual_forcing),
        ("movement_feedback_gain", movement_feedback_gain),
        ("phenology_feedback_gain", phenology_feedback_gain),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    total = movement_feedback_gain + phenology_feedback_gain
    if total <= 0.0:
        return None
    return residual_forcing / total


def simulate_closed_loop_tracking(
    *,
    residual_forcing: float,
    movement_feedback_gain: float,
    phenology_feedback_gain: float,
    initial_mismatch: float = 0.0,
    steps: int = 200,
    burn_in: int = 50,
) -> ClosedLoopTrackingResult:
    """Simulate the exact scalar closed-loop recurrence."""

    for name, value in (
        ("residual_forcing", residual_forcing),
        ("movement_feedback_gain", movement_feedback_gain),
        ("phenology_feedback_gain", phenology_feedback_gain),
        ("initial_mismatch", initial_mismatch),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if movement_feedback_gain < 0.0:
        raise ValueError(
            "movement_feedback_gain must be non-negative"
        )
    if phenology_feedback_gain < 0.0:
        raise ValueError(
            "phenology_feedback_gain must be non-negative"
        )
    if steps <= 0:
        raise ValueError("steps must be positive")
    if not 0 <= burn_in < steps:
        raise ValueError(
            "burn_in must satisfy 0 <= burn_in < steps"
        )

    total = movement_feedback_gain + phenology_feedback_gain
    multiplier = 1.0 - total
    stability_class = classify_closed_loop_stability(total)
    stable = abs(multiplier) < 1.0
    equilibrium = (
        closed_loop_equilibrium_mismatch(
            residual_forcing,
            movement_feedback_gain,
            phenology_feedback_gain,
        )
        if stable
        else None
    )

    mismatch = initial_mismatch
    values: list[float] = []
    for step in range(1, steps + 1):
        mismatch = (
            multiplier * mismatch + residual_forcing
        )
        if step > burn_in:
            values.append(mismatch)

    mean_mismatch = sum(values) / len(values)
    rms = sqrt(
        sum(value * value for value in values)
        / len(values)
    )
    return ClosedLoopTrackingResult(
        residual_forcing=residual_forcing,
        movement_feedback_gain=movement_feedback_gain,
        phenology_feedback_gain=phenology_feedback_gain,
        total_feedback_gain=total,
        multiplier=multiplier,
        stable=stable,
        stability_class=stability_class,
        theoretical_equilibrium_mismatch=equilibrium,
        final_mismatch=mismatch,
        mean_mismatch=mean_mismatch,
        rms_mismatch=rms,
    )


def minimum_cost_feedback_allocation(
    total_feedback_gain: float,
    *,
    movement_cost: float,
    phenology_cost: float,
) -> FeedbackAllocation:
    """Allocate fixed total feedback K between movement and phenology.

    Minimize

        0.5*c_m*q_m^2 + 0.5*c_h*q_h^2

    subject to

        q_m + q_h = K.

    The unconstrained solution is

        q_m = K*c_h/(c_m+c_h)
        q_h = K*c_m/(c_m+c_h).

    This function does not impose q_h<1. Use the returned value to check
    whether the existing finite-rate phenology channel can realize the optimum.
    """

    for name, value in (
        ("total_feedback_gain", total_feedback_gain),
        ("movement_cost", movement_cost),
        ("phenology_cost", phenology_cost),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if total_feedback_gain < 0.0:
        raise ValueError(
            "total_feedback_gain must be non-negative"
        )
    if movement_cost <= 0.0 or phenology_cost <= 0.0:
        raise ValueError(
            "movement_cost and phenology_cost must be positive"
        )

    denominator = movement_cost + phenology_cost
    q_m = (
        total_feedback_gain
        * phenology_cost
        / denominator
    )
    q_h = (
        total_feedback_gain
        * movement_cost
        / denominator
    )
    cost = 0.5 * (
        movement_cost * q_m * q_m
        + phenology_cost * q_h * q_h
    )
    return FeedbackAllocation(
        total_feedback_gain=total_feedback_gain,
        movement_feedback_gain=q_m,
        phenology_feedback_gain=q_h,
        movement_cost=movement_cost,
        phenology_cost=phenology_cost,
        total_quadratic_cost=cost,
    )


def unconstrained_optimal_feedback(
    *,
    residual_forcing: float,
    mismatch_strength: float,
    movement_cost: float,
    phenology_cost: float,
) -> UnconstrainedFeedbackOptimum:
    """Closed-form interior optimum for steady mismatch plus feedback cost.

    The steady-state objective is

        J
        = 0.5*A*(r/K)^2
          + 0.5*c_m*q_m^2
          + 0.5*c_h*q_h^2,

    with K=q_m+q_h.

    For fixed K, the minimum feedback cost has effective coefficient

        c_eff = c_m*c_h/(c_m+c_h).

    Therefore

        K* = [A*r^2/c_eff]^(1/4).

    This is an unconstrained local optimum. It is dynamically admissible only
    when K*<2, and the phenology component is representable by finite h only
    when q_h*<1.
    """

    for name, value in (
        ("residual_forcing", residual_forcing),
        ("mismatch_strength", mismatch_strength),
        ("movement_cost", movement_cost),
        ("phenology_cost", phenology_cost),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if mismatch_strength <= 0.0:
        raise ValueError("mismatch_strength must be positive")
    if movement_cost <= 0.0 or phenology_cost <= 0.0:
        raise ValueError(
            "movement_cost and phenology_cost must be positive"
        )

    c_eff = (
        movement_cost
        * phenology_cost
        / (movement_cost + phenology_cost)
    )
    forcing_sq = residual_forcing * residual_forcing

    if forcing_sq == 0.0:
        total = 0.0
        allocation = minimum_cost_feedback_allocation(
            total,
            movement_cost=movement_cost,
            phenology_cost=phenology_cost,
        )
        equilibrium = 0.0
        objective = 0.0
    else:
        total = (
            mismatch_strength
            * forcing_sq
            / c_eff
        ) ** 0.25
        allocation = minimum_cost_feedback_allocation(
            total,
            movement_cost=movement_cost,
            phenology_cost=phenology_cost,
        )
        equilibrium = residual_forcing / total
        objective = (
            0.5
            * mismatch_strength
            * equilibrium
            * equilibrium
            + allocation.total_quadratic_cost
        )

    return UnconstrainedFeedbackOptimum(
        residual_forcing=residual_forcing,
        mismatch_strength=mismatch_strength,
        movement_cost=movement_cost,
        phenology_cost=phenology_cost,
        effective_feedback_cost=c_eff,
        total_feedback_gain=total,
        movement_feedback_gain=(
            allocation.movement_feedback_gain
        ),
        phenology_feedback_gain=(
            allocation.phenology_feedback_gain
        ),
        equilibrium_mismatch=equilibrium,
        objective_value=objective,
        stability_feasible=(0.0 <= total < 2.0),
        phenology_fraction_feasible=(
            allocation.phenology_feedback_gain < 1.0
        ),
    )


def route_relaxation_to_step_feedback(
    local_fractional_relaxation_per_distance: float,
    forward_distance_per_step: float,
) -> float:
    """Convert a local route-distance restoring coefficient to step feedback.

    Under the local exponential approximation

        de/dx = -kappa_x e,

    traversing distance Delta x gives

        e_after/e_before = exp(-kappa_x Delta x),

    so the equivalent one-step feedback fraction is

        q = 1 - exp(-kappa_x Delta x).

    This is a local model bridge. A published linear route regression supplies
    evidence for the sign and local restoring tendency, but this conversion
    requires confirmed distance units and a declared forward distance per model
    step.
    """

    for name, value in (
        (
            "local_fractional_relaxation_per_distance",
            local_fractional_relaxation_per_distance,
        ),
        ("forward_distance_per_step", forward_distance_per_step),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if local_fractional_relaxation_per_distance < 0.0:
        raise ValueError(
            "local fractional relaxation must be non-negative"
        )
    if forward_distance_per_step < 0.0:
        raise ValueError(
            "forward_distance_per_step must be non-negative"
        )
    return 1.0 - exp(
        -local_fractional_relaxation_per_distance
        * forward_distance_per_step
    )
