"""State-dependent information deadlines for PAYOFF-B.

The base information-deadline theorem assumes a fixed waiting cost D.  This
module allows the realised cost of delaying commitment to depend on a future
environmental state that may not yet be known when the wait/commit decision is
made.

Under risk-neutral additive expected loss, the exact ex-ante decision depends
on the conditional expected delay cost available at commitment, not on the
future realised cost.  This distinction prevents post-hoc environmental
conditions from being silently treated as information the actor possessed.
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
class HiddenDeadlineResult:
    expected_delay_cost: float
    wait_threshold: float | None
    ever_waits: bool
    cue_accuracy: float
    information_value: float
    ex_ante_decision: str
    probability_ex_post_reversal: float
    expected_ex_post_regret: float


def expected_delay_cost(
    probabilities: Iterable[float],
    delay_costs: Iterable[float],
) -> float:
    """Expected waiting cost under information available at commitment."""

    probs = [float(x) for x in probabilities]
    costs = [float(x) for x in delay_costs]
    if not probs or len(probs) != len(costs):
        raise ValueError("probabilities and delay_costs must be non-empty and aligned")
    if any((not isfinite(p)) or p < 0.0 for p in probs):
        raise ValueError("probabilities must be finite and non-negative")
    if any((not isfinite(d)) or d < 0.0 for d in costs):
        raise ValueError("delay costs must be finite and non-negative")
    total = sum(probs)
    if abs(total - 1.0) > 1e-10:
        raise ValueError("probabilities must sum to one")
    return sum(p * d for p, d in zip(probs, costs))


def state_dependent_deadline(
    prior_early: float,
    cue_accuracy: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    deadline_state_probabilities: Iterable[float],
    deadline_state_costs: Iterable[float],
) -> HiddenDeadlineResult:
    """Evaluate a wait/commit decision with an unresolved future deadline state.

    The future deadline state can modulate the realised cost of waiting.  The
    actor is assumed to know only the supplied probability distribution when it
    chooses whether to wait.  The later seasonal cue does not arrive until
    after this wait/commit choice.
    """

    probs = [float(x) for x in deadline_state_probabilities]
    costs = [float(x) for x in deadline_state_costs]
    dbar = expected_delay_cost(probs, costs)

    threshold = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=dbar,
    )
    value = information_value(
        prior_early,
        cue_accuracy,
        false_early_cost,
        missed_early_cost,
    )
    wait = value > dbar + 1e-12

    reversal_prob = 0.0
    regret = 0.0
    for p, realised_d in zip(probs, costs):
        if wait:
            state_regret = max(0.0, realised_d - value)
        else:
            state_regret = max(0.0, value - realised_d)
        if state_regret > 0.0:
            reversal_prob += p
        regret += p * state_regret

    return HiddenDeadlineResult(
        expected_delay_cost=dbar,
        wait_threshold=threshold.wait_cue_accuracy,
        ever_waits=threshold.ever_waits,
        cue_accuracy=float(cue_accuracy),
        information_value=value,
        ex_ante_decision="wait_for_information" if wait else "commit_now",
        probability_ex_post_reversal=reversal_prob,
        expected_ex_post_regret=regret,
    )


def conditional_threshold_shift(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    expected_delay_cost_before: float,
    expected_delay_cost_after: float,
) -> float:
    """Exact q-threshold shift when pre-commitment information changes E[D].

    This result is defined only when both expected delay costs remain below the
    maximum value of information, so both thresholds are finite.
    """

    before = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=expected_delay_cost_before,
    )
    after = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=expected_delay_cost_after,
    )
    if before.wait_cue_accuracy is None or after.wait_cue_accuracy is None:
        raise ValueError("both conditional thresholds must be finite")
    return after.wait_cue_accuracy - before.wait_cue_accuracy
