"""State-dependent information deadlines for PAYOFF-B.

The original information-deadline theorem uses a fixed waiting cost D.
This extension allows the cost paid by waiting to depend on an unobserved
future state or ecological context.

Under risk-neutral additive expected loss, the ex-ante decision depends on the
conditional expected waiting cost available at commitment, not on the
subsequently realised cost.  This distinction prevents post-hoc environmental
conditions from being silently treated as information the actor possessed.

This is an exact extension of the declared binary-cue model, not an empirical
claim about any particular species.
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
class StateDependentDeadline:
    prior_early: float
    delay_cost_normal: float
    delay_cost_early: float
    expected_delay_cost: float
    wait_threshold: float | None
    ever_waits: bool


@dataclass(frozen=True)
class HiddenDeadlineDecision:
    expected_delay_cost: float
    cue_accuracy: float
    information_value: float
    wait_threshold: float | None
    ever_waits: bool
    ex_ante_decision: str
    probability_ex_post_reversal: float
    expected_ex_post_regret: float


def _validate_context_distribution(
    probabilities: Iterable[float],
    delay_costs: Iterable[float],
) -> tuple[list[float], list[float]]:
    probs = [float(x) for x in probabilities]
    costs = [float(x) for x in delay_costs]
    if not probs or len(probs) != len(costs):
        raise ValueError(
            "probabilities and delay_costs must be non-empty and aligned"
        )
    if any((not isfinite(p)) or p < 0.0 for p in probs):
        raise ValueError("probabilities must be finite and non-negative")
    if any((not isfinite(d)) or d < 0.0 for d in costs):
        raise ValueError("delay costs must be finite and non-negative")
    if abs(sum(probs) - 1.0) > 1e-10:
        raise ValueError("probabilities must sum to one")
    return probs, costs


def expected_context_delay_cost(
    probabilities: Iterable[float],
    delay_costs: Iterable[float],
) -> float:
    """Expected waiting cost under information available at commitment."""

    probs, costs = _validate_context_distribution(
        probabilities,
        delay_costs,
    )
    return sum(p * d for p, d in zip(probs, costs))


def expected_state_dependent_delay_cost(
    prior_early: float,
    delay_cost_normal: float,
    delay_cost_early: float,
) -> float:
    """Expected waiting cost before the future seasonal state is observed."""

    pi = float(prior_early)
    dn = float(delay_cost_normal)
    de = float(delay_cost_early)
    if not isfinite(pi) or not 0.0 < pi < 1.0:
        raise ValueError("prior_early must lie strictly between 0 and 1")
    if not all(isfinite(x) and x >= 0.0 for x in (dn, de)):
        raise ValueError("state-dependent delay costs must be non-negative")
    return expected_context_delay_cost(
        [1.0 - pi, pi],
        [dn, de],
    )


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
    return (
        abs(two.expected_delay_cost - one.expected_delay_cost)
        / total_loss
    )


def hidden_deadline_decision(
    prior_early: float,
    cue_accuracy: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    deadline_state_probabilities: Iterable[float],
    deadline_state_costs: Iterable[float],
) -> HiddenDeadlineDecision:
    """Decision and ex-post reversal risk under an unresolved deadline state.

    The actor chooses whether to wait before the deadline state is revealed.
    Ex ante it uses E[D | information at commitment].  Ex post, the realised
    D can make the opposite choice look better without implying irrationality.
    """

    probs, costs = _validate_context_distribution(
        deadline_state_probabilities,
        deadline_state_costs,
    )
    expected = sum(p * d for p, d in zip(probs, costs))

    base = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=expected,
    )
    value = information_value(
        prior_early,
        cue_accuracy,
        false_early_cost,
        missed_early_cost,
    )
    waits = value > expected + 1e-12

    reversal_probability = 0.0
    expected_regret = 0.0
    for p, realised_cost in zip(probs, costs):
        if waits:
            regret = max(0.0, realised_cost - value)
        else:
            regret = max(0.0, value - realised_cost)
        if regret > 0.0:
            reversal_probability += p
        expected_regret += p * regret

    return HiddenDeadlineDecision(
        expected_delay_cost=expected,
        cue_accuracy=float(cue_accuracy),
        information_value=value,
        wait_threshold=base.wait_cue_accuracy,
        ever_waits=base.ever_waits,
        ex_ante_decision=(
            "wait_for_information" if waits else "commit_now"
        ),
        probability_ex_post_reversal=reversal_probability,
        expected_ex_post_regret=expected_regret,
    )


def conditional_threshold_shift(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    expected_delay_cost_before: float,
    expected_delay_cost_after: float,
) -> float:
    """Exact threshold shift when pre-commitment information changes E[D]."""

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
