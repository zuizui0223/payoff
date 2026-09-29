"""Compensated information deadlines for PAYOFF-B.

Raw waiting time is not necessarily the fitness cost that enters the
information-deadline theorem. An actor may compensate after waiting (for
example by faster migration or reduced stopover time). Under additive
separability, the original theorem uses the total effective waiting cost: a
non-recoverable direct waiting cost plus optimally compensated downstream cost.

For the linear specialization:
    raw delay = delta
    compensation c in [0, min(C, delta)]
    compensation cost K(c) = kappa * c
    residual timing loss M(delta-c) = mu * (delta-c)

the exact optimum is piecewise:
    c* = 0                     if kappa >= mu
    c* = min(C, delta)         if kappa < mu

and D_eff = J(delta) + K(c*) + M(delta-c*).
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
    direct_wait_cost_per_unit: float
    optimal_compensation: float
    residual_delay: float
    direct_wait_cost: float
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
    direct_wait_cost_per_unit: float = 0.0,
) -> tuple[float, float, float]:
    """Return c*, residual delay, and total D_eff for the linear model.

    D_eff includes a direct, non-recoverable waiting cost omega * delta plus
    the optimized downstream compensation/residual-timing cost.
    """

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
    omega = _nonnegative_finite(
        "direct_wait_cost_per_unit",
        direct_wait_cost_per_unit,
    )

    usable = min(capacity, delta)
    if kappa < mu:
        compensated = usable
    else:
        # At the exact tie kappa == mu every feasible c has the same cost.
        # Choose zero compensation deterministically.
        compensated = 0.0

    residual = delta - compensated
    direct = omega * delta
    effective = direct + kappa * compensated + mu * residual
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
    direct_wait_cost_per_unit: float = 0.0,
) -> LinearCompensatedDeadline:
    """Exact information-use threshold after optimal linear compensation."""

    compensated, residual, effective = linear_effective_deadline_cost(
        raw_delay,
        compensation_capacity=compensation_capacity,
        compensation_cost_per_unit=compensation_cost_per_unit,
        residual_loss_per_unit=residual_loss_per_unit,
        direct_wait_cost_per_unit=direct_wait_cost_per_unit,
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
        direct_wait_cost_per_unit=float(direct_wait_cost_per_unit),
        optimal_compensation=compensated,
        residual_delay=residual,
        direct_wait_cost=float(direct_wait_cost_per_unit) * float(raw_delay),
        effective_delay_cost=effective,
        wait_threshold=base.wait_cue_accuracy,
        ever_waits=base.ever_waits,
    )


def _unpack_actor(actor):
    """Accept legacy 4-tuples or general 5-tuples including direct wait cost.

    Order:
      (raw_delay, capacity, compensation_cost, residual_loss[, direct_wait_cost])
    """

    if len(actor) == 4:
        return (*actor, 0.0)
    if len(actor) == 5:
        return actor
    raise ValueError("actor must contain 4 or 5 values")


def compensated_pair_window_width(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    actor_1: tuple[float, ...],
    actor_2: tuple[float, ...],
) -> float | None:
    """Exact pairwise q-window width using actor-specific D_eff.

    Actor tuple order:
        (raw_delay, compensation_capacity,
         compensation_cost_per_unit, residual_loss_per_unit
         [, direct_wait_cost_per_unit])

    Returns None when at least one actor never waits even at perfect
    information.
    """

    a1 = _unpack_actor(actor_1)
    a2 = _unpack_actor(actor_2)
    one = linear_compensated_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        raw_delay=a1[0],
        compensation_capacity=a1[1],
        compensation_cost_per_unit=a1[2],
        residual_loss_per_unit=a1[3],
        direct_wait_cost_per_unit=a1[4],
    )
    two = linear_compensated_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        raw_delay=a2[0],
        compensation_capacity=a2[1],
        compensation_cost_per_unit=a2[2],
        residual_loss_per_unit=a2[3],
        direct_wait_cost_per_unit=a2[4],
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
    direct_wait_cost_per_unit: float = 0.0,
    total_prior_loss: float,
    raw_delay: float,
) -> float:
    """Piecewise dq_wait/d(delta) away from the capacity kink.

    When compensation is cheaper than residual timing loss, the threshold
    initially rises with slope (omega+kappa)/S while compensation capacity
    remains, then with slope (omega+mu)/S after capacity is exhausted. If
    compensation is not worthwhile, the slope is (omega+mu)/S throughout.
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
    omega = _nonnegative_finite(
        "direct_wait_cost_per_unit",
        direct_wait_cost_per_unit,
    )
    scale = float(total_prior_loss)
    delta = _nonnegative_finite("raw_delay", raw_delay)
    if not isfinite(scale) or scale <= 0.0:
        raise ValueError("total_prior_loss must be finite and positive")

    if kappa >= mu:
        return (omega + mu) / scale
    if abs(delta - capacity) <= 1e-12:
        raise ValueError("slope is not unique at the capacity kink")
    return (omega + (kappa if delta < capacity else mu)) / scale


def _validated_state_vectors(
    probabilities,
    compensation_costs_per_unit,
    residual_losses_per_unit,
):
    probs = [float(x) for x in probabilities]
    kappas = [float(x) for x in compensation_costs_per_unit]
    mus = [float(x) for x in residual_losses_per_unit]
    if not probs or not (len(probs) == len(kappas) == len(mus)):
        raise ValueError("state vectors must be non-empty and aligned")
    if any((not isfinite(p)) or p < 0.0 for p in probs):
        raise ValueError("state probabilities must be finite and non-negative")
    if abs(sum(probs) - 1.0) > 1e-10:
        raise ValueError("state probabilities must sum to one")
    if any((not isfinite(x)) or x < 0.0 for x in kappas + mus):
        raise ValueError("state-specific cost rates must be finite and non-negative")
    return probs, kappas, mus


def adaptive_state_expected_effective_cost(
    probabilities,
    *,
    raw_delay: float,
    compensation_capacity: float,
    compensation_costs_per_unit,
    residual_losses_per_unit,
    direct_wait_costs_per_unit=None,
) -> float:
    """E[min_c L(c,H)] when compensation may adapt after H is known."""

    probs, kappas, mus = _validated_state_vectors(
        probabilities,
        compensation_costs_per_unit,
        residual_losses_per_unit,
    )
    if direct_wait_costs_per_unit is None:
        omegas = [0.0] * len(probs)
    else:
        omegas = [float(x) for x in direct_wait_costs_per_unit]
        if len(omegas) != len(probs) or any(
            (not isfinite(x)) or x < 0.0 for x in omegas
        ):
            raise ValueError("direct wait cost rates must align and be non-negative")

    total = 0.0
    for p, kappa, mu, omega in zip(probs, kappas, mus, omegas):
        _, _, cost = linear_effective_deadline_cost(
            raw_delay,
            compensation_capacity=compensation_capacity,
            compensation_cost_per_unit=kappa,
            residual_loss_per_unit=mu,
            direct_wait_cost_per_unit=omega,
        )
        total += p * cost
    return total


def precommitted_state_expected_effective_cost(
    probabilities,
    *,
    raw_delay: float,
    compensation_capacity: float,
    compensation_costs_per_unit,
    residual_losses_per_unit,
    direct_wait_costs_per_unit=None,
) -> float:
    """min_c E[L(c,H)] when one compensation plan must be chosen before H."""

    probs, kappas, mus = _validated_state_vectors(
        probabilities,
        compensation_costs_per_unit,
        residual_losses_per_unit,
    )
    if direct_wait_costs_per_unit is None:
        omegas = [0.0] * len(probs)
    else:
        omegas = [float(x) for x in direct_wait_costs_per_unit]
        if len(omegas) != len(probs) or any(
            (not isfinite(x)) or x < 0.0 for x in omegas
        ):
            raise ValueError("direct wait cost rates must align and be non-negative")

    mean_kappa = sum(p * k for p, k in zip(probs, kappas))
    mean_mu = sum(p * mu for p, mu in zip(probs, mus))
    mean_omega = sum(p * w for p, w in zip(probs, omegas))
    _, _, cost = linear_effective_deadline_cost(
        raw_delay,
        compensation_capacity=compensation_capacity,
        compensation_cost_per_unit=mean_kappa,
        residual_loss_per_unit=mean_mu,
        direct_wait_cost_per_unit=mean_omega,
    )
    return cost
