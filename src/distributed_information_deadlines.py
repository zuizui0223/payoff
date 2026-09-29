"""Population-level uptake implied by heterogeneous PAYOFF-B deadlines.

The individual information-deadline theorem says an actor waits iff

    D < V(q),

with strict inequality under the implemented tie rule.  If D varies among
individuals, the population uptake curve is therefore the CDF of D evaluated at
the information value.  This module keeps that observation exact and
distribution-free.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable

from src.endogenous_information_timing import (
    closed_form_information_threshold,
    information_value,
)


@dataclass(frozen=True)
class DistributedDeadlineSummary:
    cue_accuracy: float
    information_value: float
    uptake_probability: float
    never_wait_fraction: float
    individuals: int


def _validate_delays(delays: Iterable[float]) -> list[float]:
    values = [float(x) for x in delays]
    if not values:
        raise ValueError("at least one delay cost is required")
    if any((not isfinite(x)) or x < 0.0 for x in values):
        raise ValueError("delay costs must be finite and non-negative")
    return values


def population_information_uptake(
    prior_early: float,
    cue_accuracy: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    delay_costs: Iterable[float],
) -> DistributedDeadlineSummary:
    """Exact empirical-CDF uptake for heterogeneous delay costs.

    With the PAYOFF-B tie rule, an individual waits only when V(q) > D.
    """

    delays = _validate_delays(delay_costs)
    value = information_value(
        prior_early,
        cue_accuracy,
        false_early_cost,
        missed_early_cost,
    )
    uptake = sum(d < value for d in delays) / len(delays)

    zero_delay = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=0.0,
    )
    r0 = zero_delay.maximum_information_value
    never_wait = sum(d >= r0 for d in delays) / len(delays)

    return DistributedDeadlineSummary(
        cue_accuracy=float(cue_accuracy),
        information_value=value,
        uptake_probability=uptake,
        never_wait_fraction=never_wait,
        individuals=len(delays),
    )


def wait_threshold_from_delay_cost(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    delay_cost: float,
) -> float | None:
    """Affine individual threshold; None means the actor never waits."""

    result = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=delay_cost,
    )
    return result.wait_cue_accuracy


def delay_cost_from_finite_wait_threshold(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    wait_threshold: float,
) -> float:
    """Invert a finite q_wait to its delay cost under the exact model."""

    q = float(wait_threshold)
    if not isfinite(q) or not 0.5 <= q <= 1.0:
        raise ValueError("wait_threshold must lie in [0.5, 1]")

    zero = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=0.0,
    )
    q0 = zero.actionable_cue_accuracy
    if q < q0:
        raise ValueError("finite wait threshold cannot lie below actionable q0")

    total = (
        zero.early_action_prior_loss
        + zero.late_action_prior_loss
    )
    delay = total * (q - q0)
    if delay >= zero.prior_bayes_risk + 1e-12:
        raise ValueError(
            "threshold implies D >= R0; such an actor never waits under "
            "the implemented strict rule"
        )
    return max(0.0, delay)


def independent_pair_asynchrony(
    uptake_probability_1: float,
    uptake_probability_2: float,
) -> float:
    """P(exactly one waits) for conditionally independent actors."""

    p1 = float(uptake_probability_1)
    p2 = float(uptake_probability_2)
    if not all(isfinite(p) and 0.0 <= p <= 1.0 for p in (p1, p2)):
        raise ValueError("uptake probabilities must lie in [0,1]")
    return p1 * (1.0 - p2) + (1.0 - p1) * p2


def pair_asynchrony_from_joint_uptake(
    uptake_probability_1: float,
    uptake_probability_2: float,
    joint_wait_probability: float,
) -> float:
    """General P(exactly one waits), allowing correlated deadlines."""

    p1 = float(uptake_probability_1)
    p2 = float(uptake_probability_2)
    p12 = float(joint_wait_probability)
    if not all(isfinite(p) for p in (p1, p2, p12)):
        raise ValueError("probabilities must be finite")
    if not (0.0 <= p1 <= 1.0 and 0.0 <= p2 <= 1.0):
        raise ValueError("marginal probabilities must lie in [0,1]")
    lower = max(0.0, p1 + p2 - 1.0)
    upper = min(p1, p2)
    if not lower - 1e-12 <= p12 <= upper + 1e-12:
        raise ValueError("joint probability violates Fréchet bounds")
    return p1 + p2 - 2.0 * p12
