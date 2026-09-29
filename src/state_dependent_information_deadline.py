"""State-dependent information deadlines for PAYOFF-B.

The original information-deadline theorem uses a fixed waiting cost D.
This extension allows the cost paid by waiting to depend on an unobserved
future state or ecological context.  Under risk-neutral expected loss, the
decision depends on the pre-commitment expected waiting cost.

This is an exact extension of the declared binary-cue model, not an empirical
claim about any particular species.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from src.endogenous_information_timing import (
    closed_form_information_threshold,
)


@dataclass(frozen=True)
class StateDependentDeadline:
    prior_early: float
    delay_cost_normal: float
    delay_cost_early: float
    expected_delay_cost: float
    wait_threshold: float | None
    ever_waits: bool


def expected_state_dependent_delay_cost(
    prior_early: float,
    delay_cost_normal: float,
    delay_cost_early: float,
) -> float:
    """Expected waiting cost before the future state is observed."""

    pi = float(prior_early)
    dn = float(delay_cost_normal)
    de = float(delay_cost_early)
    if not isfinite(pi) or not 0.0 < pi < 1.0:
        raise ValueError("prior_early must lie strictly between 0 and 1")
    if not all(isfinite(x) and x >= 0.0 for x in (dn, de)):
        raise ValueError("state-dependent delay costs must be non-negative")
    return (1.0 - pi) * dn + pi * de


def state_dependent_information_threshold(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    delay_cost_normal: float,
    delay_cost_early: float,
) -> StateDependentDeadline:
    """Exact wait threshold when waiting cost depends on the hidden state.

    Waiting occurs before the later cue is observed.  Therefore, under linear
    expected loss, the fixed D in the original theorem is replaced by

        E[D(theta)] = (1-pi) D_normal + pi D_early.

    All other threshold results then follow unchanged.
    """

    expected = expected_state_dependent_delay_cost(
        prior_early,
        delay_cost_normal,
        delay_cost_early,
    )
    base = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=expected,
    )
    return StateDependentDeadline(
        prior_early=float(prior_early),
        delay_cost_normal=float(delay_cost_normal),
        delay_cost_early=float(delay_cost_early),
        expected_delay_cost=expected,
        wait_threshold=base.wait_cue_accuracy,
        ever_waits=base.ever_waits,
    )


def state_dependent_pair_window_width(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    actor_1_delay_normal: float,
    actor_1_delay_early: float,
    actor_2_delay_normal: float,
    actor_2_delay_early: float,
) -> float | None:
    """Exact asynchronous-window width for two state-dependent deadlines.

    Returns None if at least one actor never waits even at perfect information.
    """

    one = state_dependent_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost_normal=actor_1_delay_normal,
        delay_cost_early=actor_1_delay_early,
    )
    two = state_dependent_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost_normal=actor_2_delay_normal,
        delay_cost_early=actor_2_delay_early,
    )
    if not one.ever_waits or not two.ever_waits:
        return None

    pi = float(prior_early)
    total_loss = (
        (1.0 - pi) * float(false_early_cost)
        + pi * float(missed_early_cost)
    )
    return abs(two.expected_delay_cost - one.expected_delay_cost) / total_loss
