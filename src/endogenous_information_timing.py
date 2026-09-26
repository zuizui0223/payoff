"""Endogenous information timing for PAYOFF-B seasonal decisions.

The partial-information game treats cue quality as given.  This module adds a
second decision: commit before a seasonal cue becomes observable, or wait and
act with better information.

The ecological quantity is the value of waiting for information relative to
the opportunity cost of delay.  This separates:

    early action under uncertainty
    versus
    later action with more information.

The model is intentionally small and exact.  It is a decision-theory layer that
can be embedded in the larger interaction game.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal


TimingDecision = Literal["commit_now", "wait_for_information"]


@dataclass(frozen=True)
class InformationTimingScenario:
    prior_early: float = 0.40
    cue_accuracy_after_wait: float = 0.90
    false_early_cost: float = 2.0
    missed_early_cost: float = 1.0
    partner_false_early_externality: float = 0.0
    partner_missed_early_externality: float = 0.0

    def __post_init__(self) -> None:
        if (
            not isfinite(self.prior_early)
            or not 0.0 < self.prior_early < 1.0
        ):
            raise ValueError("prior_early must lie strictly between 0 and 1")
        if (
            not isfinite(self.cue_accuracy_after_wait)
            or not 0.5 <= self.cue_accuracy_after_wait <= 1.0
        ):
            raise ValueError(
                "cue_accuracy_after_wait must lie in [0.5, 1]"
            )
        for name in (
            "false_early_cost",
            "missed_early_cost",
            "partner_false_early_externality",
            "partner_missed_early_externality",
        ):
            value = float(getattr(self, name))
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be non-negative and finite")
        if self.false_early_cost + self.missed_early_cost <= 0.0:
            raise ValueError("at least one private state-mismatch cost is required")


@dataclass(frozen=True)
class InformationTimingDiagnostic:
    prior_bayes_risk_private: float
    post_cue_bayes_risk_private: float
    private_information_value: float
    prior_bayes_risk_joint: float
    post_cue_bayes_risk_joint: float
    joint_information_value: float
    delay_cost: float
    private_decision: TimingDecision
    joint_decision: TimingDecision
    information_timing_wedge: bool


def _validate_cost(value: float, name: str) -> float:
    value = float(value)
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be non-negative and finite")
    return value


def prior_bayes_risk(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
) -> float:
    """Minimum expected state-mismatch loss before observing a cue."""

    pi = float(prior_early)
    cf = _validate_cost(false_early_cost, "false_early_cost")
    cm = _validate_cost(missed_early_cost, "missed_early_cost")
    if not isfinite(pi) or not 0.0 < pi < 1.0:
        raise ValueError("prior_early must lie strictly between 0 and 1")
    return min((1.0 - pi) * cf, pi * cm)


def posterior_cue_bayes_risk(
    prior_early: float,
    cue_accuracy: float,
    false_early_cost: float,
    missed_early_cost: float,
) -> float:
    """Expected Bayes risk after observing a symmetric binary cue.

    The calculation uses joint state-signal probabilities directly, so no
    posterior division is required.
    """

    pi = float(prior_early)
    q = float(cue_accuracy)
    cf = _validate_cost(false_early_cost, "false_early_cost")
    cm = _validate_cost(missed_early_cost, "missed_early_cost")
    if not isfinite(pi) or not 0.0 < pi < 1.0:
        raise ValueError("prior_early must lie strictly between 0 and 1")
    if not isfinite(q) or not 0.5 <= q <= 1.0:
        raise ValueError("cue_accuracy must lie in [0.5, 1]")

    # Signal says early.
    late_state_early_signal = (1.0 - pi) * (1.0 - q)
    early_state_early_signal = pi * q
    risk_early_signal = min(
        late_state_early_signal * cf,
        early_state_early_signal * cm,
    )

    # Signal says late.
    late_state_late_signal = (1.0 - pi) * q
    early_state_late_signal = pi * (1.0 - q)
    risk_late_signal = min(
        late_state_late_signal * cf,
        early_state_late_signal * cm,
    )
    return risk_early_signal + risk_late_signal


def information_value(
    prior_early: float,
    cue_accuracy: float,
    false_early_cost: float,
    missed_early_cost: float,
) -> float:
    """Expected reduction in decision loss from waiting for the cue."""

    before = prior_bayes_risk(
        prior_early,
        false_early_cost,
        missed_early_cost,
    )
    after = posterior_cue_bayes_risk(
        prior_early,
        cue_accuracy,
        false_early_cost,
        missed_early_cost,
    )
    value = before - after
    if value < -1e-12:
        raise AssertionError("Bayes information value cannot be negative")
    return max(0.0, value)


def decision_for_delay_cost(
    information_value_amount: float,
    delay_cost: float,
    *,
    tolerance: float = 1e-12,
) -> TimingDecision:
    """Wait only when information gain strictly exceeds the delay cost."""

    value = _validate_cost(
        information_value_amount,
        "information_value_amount",
    )
    delay = _validate_cost(delay_cost, "delay_cost")
    if not isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("tolerance must be non-negative and finite")
    if value > delay + tolerance:
        return "wait_for_information"
    return "commit_now"


def evaluate_information_timing(
    scenario: InformationTimingScenario,
    *,
    delay_cost: float,
) -> InformationTimingDiagnostic:
    """Compare private and system-level incentives to wait for information."""

    delay = _validate_cost(delay_cost, "delay_cost")

    private_before = prior_bayes_risk(
        scenario.prior_early,
        scenario.false_early_cost,
        scenario.missed_early_cost,
    )
    private_after = posterior_cue_bayes_risk(
        scenario.prior_early,
        scenario.cue_accuracy_after_wait,
        scenario.false_early_cost,
        scenario.missed_early_cost,
    )
    private_value = private_before - private_after

    joint_cf = (
        scenario.false_early_cost
        + scenario.partner_false_early_externality
    )
    joint_cm = (
        scenario.missed_early_cost
        + scenario.partner_missed_early_externality
    )
    joint_before = prior_bayes_risk(
        scenario.prior_early,
        joint_cf,
        joint_cm,
    )
    joint_after = posterior_cue_bayes_risk(
        scenario.prior_early,
        scenario.cue_accuracy_after_wait,
        joint_cf,
        joint_cm,
    )
    joint_value = joint_before - joint_after

    private_decision = decision_for_delay_cost(
        private_value,
        delay,
    )
    joint_decision = decision_for_delay_cost(
        joint_value,
        delay,
    )
    return InformationTimingDiagnostic(
        prior_bayes_risk_private=private_before,
        post_cue_bayes_risk_private=private_after,
        private_information_value=private_value,
        prior_bayes_risk_joint=joint_before,
        post_cue_bayes_risk_joint=joint_after,
        joint_information_value=joint_value,
        delay_cost=delay,
        private_decision=private_decision,
        joint_decision=joint_decision,
        information_timing_wedge=(
            private_decision == "commit_now"
            and joint_decision == "wait_for_information"
        ),
    )


def sex_specific_information_access(
    scenario: InformationTimingScenario,
    *,
    early_sex_delay_cost: float,
    late_sex_delay_cost: float,
) -> tuple[TimingDecision, TimingDecision]:
    """Evaluate timing decisions under sex-specific opportunity costs.

    This does not infer sex-specific biology from first principles.  It is a
    compact representation of a system in which one sex pays a larger cost for
    delaying commitment than the other.
    """

    value = information_value(
        scenario.prior_early,
        scenario.cue_accuracy_after_wait,
        scenario.false_early_cost,
        scenario.missed_early_cost,
    )
    return (
        decision_for_delay_cost(value, early_sex_delay_cost),
        decision_for_delay_cost(value, late_sex_delay_cost),
    )


def maximum_affordable_wait_days(
    information_value_amount: float,
    *,
    delay_cost_per_day: float,
) -> float:
    """Maximum linear waiting time before opportunity cost exceeds information."""

    value = _validate_cost(
        information_value_amount,
        "information_value_amount",
    )
    daily = float(delay_cost_per_day)
    if not isfinite(daily) or daily <= 0.0:
        raise ValueError("delay_cost_per_day must be positive and finite")
    return value / daily



def prior_optimal_action(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
) -> int:
    """Return 0=late or 1=early before the cue; ties retain late."""

    pi = float(prior_early)
    early_loss = (1.0 - pi) * _validate_cost(
        false_early_cost,
        "false_early_cost",
    )
    late_loss = pi * _validate_cost(
        missed_early_cost,
        "missed_early_cost",
    )
    return 1 if early_loss < late_loss else 0


def cue_optimal_action(
    prior_early: float,
    cue_accuracy: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    signal: int,
) -> int:
    """Return the Bayes-optimal action after one binary signal."""

    if signal not in (0, 1):
        raise ValueError("signal must be 0 or 1")
    pi = float(prior_early)
    q = float(cue_accuracy)
    if not isfinite(pi) or not 0.0 < pi < 1.0:
        raise ValueError("prior_early must lie strictly between 0 and 1")
    if not isfinite(q) or not 0.5 <= q <= 1.0:
        raise ValueError("cue_accuracy must lie in [0.5, 1]")
    cf = _validate_cost(false_early_cost, "false_early_cost")
    cm = _validate_cost(missed_early_cost, "missed_early_cost")

    if signal == 1:
        p_late_and_signal = (1.0 - pi) * (1.0 - q)
        p_early_and_signal = pi * q
    else:
        p_late_and_signal = (1.0 - pi) * q
        p_early_and_signal = pi * (1.0 - q)

    early_loss = p_late_and_signal * cf
    late_loss = p_early_and_signal * cm
    return 1 if early_loss < late_loss else 0


def expected_shared_cue_action_mismatch(
    scenario: InformationTimingScenario,
    *,
    actor_a_delay_cost: float,
    actor_b_delay_cost: float,
) -> float:
    """Expected timing disagreement for two actors sharing the same later cue.

    Both actors have the same state-loss structure and cue.  They differ only
    in the opportunity cost of waiting.  If both commit, they take the same
    prior-optimal action.  If both wait, they condition on the same signal and
    again take the same action.  Mismatch can therefore arise only when one
    actor waits and the other commits.
    """

    value = information_value(
        scenario.prior_early,
        scenario.cue_accuracy_after_wait,
        scenario.false_early_cost,
        scenario.missed_early_cost,
    )
    decision_a = decision_for_delay_cost(value, actor_a_delay_cost)
    decision_b = decision_for_delay_cost(value, actor_b_delay_cost)
    if decision_a == decision_b:
        return 0.0

    committed_action = prior_optimal_action(
        scenario.prior_early,
        scenario.false_early_cost,
        scenario.missed_early_cost,
    )

    q = scenario.cue_accuracy_after_wait
    pi = scenario.prior_early
    p_signal_early = pi * q + (1.0 - pi) * (1.0 - q)
    p_signal_late = 1.0 - p_signal_early

    mismatch = 0.0
    for signal, probability in (
        (1, p_signal_early),
        (0, p_signal_late),
    ):
        informed_action = cue_optimal_action(
            pi,
            q,
            scenario.false_early_cost,
            scenario.missed_early_cost,
            signal=signal,
        )
        if informed_action != committed_action:
            mismatch += probability

    return mismatch
