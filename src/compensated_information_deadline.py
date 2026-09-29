"""Compensated information deadlines for PAYOFF-B.

Raw waiting time is not necessarily the fitness cost that enters the
information-deadline theorem. An actor may compensate after waiting (for
example by faster migration or reduced stopover time). Under additive
separability, the original theorem uses the optimally compensated downstream
cost D_eff.

For the linear specialization:
    raw delay = delta
    compensation c in [0, min(C, delta)]
    compensation cost K(c) = kappa * c
    residual timing loss M(delta-c) = mu * (delta-c)

the exact optimum is piecewise:
    c* = 0                     if kappa >= mu
    c* = min(C, delta)         if kappa < mu

and D_eff = K(c*) + M(delta-c*).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from src.endogenous_information_timing import (
    closed_form_information_threshold,
)


@dataclass(frozen=True)
class LinearCompensatedDeadline:
    raw_delay: float
    compensation_capacity: float
    compensation_cost_per_unit: float
    residual_loss_per_unit: float
    optimal_compensation: float
    residual_delay: float
    effective_delay_cost: float
    wait_threshold: float | None
    ever_waits: bool


def _nonnegative_finite(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x) or x < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return x


def linear_effective_deadline_cost(
    raw_delay: float,
    *,
    compensation_capacity: float,
    compensation_cost_per_unit: float,
    residual_loss_per_unit: float,
) -> tuple[float, float, float]:
    """Return c*, residual delay, and D_eff for the linear model."""

    delta = _nonnegative_finite("raw_delay", raw_delay)
    capacity = _nonnegative_finite(
        "compensation_capacity", compensation_capacity
    )
    kappa = _nonnegative_finite(
        "compensation_cost_per_unit",
        compensation_cost_per_unit,
    )
    mu = _nonnegative_finite(
        "residual_loss_per_unit",
        residual_loss_per_unit,
    )

    usable = min(capacity, delta)
    if kappa < mu:
        compensated = usable
    else:
        # At the exact tie kappa == mu every feasible c has the same cost.
        # Choose zero compensation deterministically.
        compensated = 0.0

    residual = delta - compensated
    effective = kappa * compensated + mu * residual
    return compensated, residual, effective


def linear_compensated_information_threshold(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    raw_delay: float,
    compensation_capacity: float,
    compensation_cost_per_unit: float,
    residual_loss_per_unit: float,
) -> LinearCompensatedDeadline:
    """Exact information-use threshold after optimal linear compensation."""

    compensated, residual, effective = linear_effective_deadline_cost(
        raw_delay,
        compensation_capacity=compensation_capacity,
        compensation_cost_per_unit=compensation_cost_per_unit,
        residual_loss_per_unit=residual_loss_per_unit,
    )
    base = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=effective,
    )
    return LinearCompensatedDeadline(
        raw_delay=float(raw_delay),
        compensation_capacity=float(compensation_capacity),
        compensation_cost_per_unit=float(compensation_cost_per_unit),
        residual_loss_per_unit=float(residual_loss_per_unit),
        optimal_compensation=compensated,
        residual_delay=residual,
        effective_delay_cost=effective,
        wait_threshold=base.wait_cue_accuracy,
        ever_waits=base.ever_waits,
    )


def compensated_pair_window_width(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    actor_1: tuple[float, float, float, float],
    actor_2: tuple[float, float, float, float],
) -> float | None:
    """Exact pairwise q-window width using actor-specific D_eff.

    Actor tuple order:
        (raw_delay, compensation_capacity,
         compensation_cost_per_unit, residual_loss_per_unit)

    Returns None when at least one actor never waits even at perfect
    information.
    """

    one = linear_compensated_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        raw_delay=actor_1[0],
        compensation_capacity=actor_1[1],
        compensation_cost_per_unit=actor_1[2],
        residual_loss_per_unit=actor_1[3],
    )
    two = linear_compensated_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        raw_delay=actor_2[0],
        compensation_capacity=actor_2[1],
        compensation_cost_per_unit=actor_2[2],
        residual_loss_per_unit=actor_2[3],
    )
    if not one.ever_waits or not two.ever_waits:
        return None

    pi = float(prior_early)
    total_loss = (
        (1.0 - pi) * float(false_early_cost)
        + pi * float(missed_early_cost)
    )
    if total_loss <= 0.0:
        raise ValueError("prior-weighted total mismatch loss must be positive")

    return abs(
        two.effective_delay_cost - one.effective_delay_cost
    ) / total_loss


def threshold_slope_with_raw_delay(
    *,
    compensation_capacity: float,
    compensation_cost_per_unit: float,
    residual_loss_per_unit: float,
    total_prior_loss: float,
    raw_delay: float,
) -> float:
    """Piecewise dq_wait/d(delta) away from the capacity kink.

    When compensation is cheaper than residual timing loss, the threshold
    initially rises with slope kappa/S while compensation capacity remains,
    then with slope mu/S after capacity is exhausted. If compensation is not
    worthwhile, the slope is mu/S throughout.
    """

    capacity = _nonnegative_finite(
        "compensation_capacity", compensation_capacity
    )
    kappa = _nonnegative_finite(
        "compensation_cost_per_unit",
        compensation_cost_per_unit,
    )
    mu = _nonnegative_finite(
        "residual_loss_per_unit",
        residual_loss_per_unit,
    )
    scale = float(total_prior_loss)
    delta = _nonnegative_finite("raw_delay", raw_delay)
    if not isfinite(scale) or scale <= 0.0:
        raise ValueError("total_prior_loss must be finite and positive")

    if kappa >= mu:
        return mu / scale
    if abs(delta - capacity) <= 1e-12:
        raise ValueError("slope is not unique at the capacity kink")
    return (kappa if delta < capacity else mu) / scale
