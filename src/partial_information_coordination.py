"""Partial-information coordination game for PAYOFF-B phenological tracking.

A destination-resident guild (for example, a flowering resource and local
pollinator) can condition timing on the realized destination state. A migrant
must commit before observing that state and instead receives a noisy remote cue.

The migrant's private decision threshold need not equal the threshold that
maximizes joint payoff once mismatch costs imposed on resident partners are
counted. This creates an information--coordination wedge in which advancing is
jointly optimal under the available information but not privately optimal for
the migrant.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal


Action = Literal["late", "early"]
Cue = Literal["late", "early"]
Regime = Literal[
    "aligned_early",
    "information_coordination_wedge",
    "information_limited",
    "private_early_joint_late",
]


@dataclass(frozen=True)
class PartialInformationTimingGame:
    """Binary hidden-state timing game with an informed resident guild.

    State:
        early spring (1) or normal/late spring (0).

    Resident partners observe the realized destination state and match it.
    The migrant sees a symmetric binary cue whose accuracy is cue_accuracy,
    then commits to early or late timing.

    false_early_cost:
        Migrant loss from advancing when spring is not early.

    missed_early_cost:
        Migrant loss from staying late when spring is early.

    migrant_interaction_mismatch_cost:
        Aggregate interaction loss borne privately by the migrant whenever its
        action differs from the destination-resident guild.

    resident_interaction_mismatch_cost_per_partner:
        Loss borne by each resident partner when migrant and resident timing
        differ. This is an externality from the migrant's private perspective.
    """

    prior_early: float = 0.55
    cue_accuracy: float = 0.55
    false_early_cost: float = 2.0
    missed_early_cost: float = 1.0
    migrant_interaction_mismatch_cost: float = 0.5
    resident_interaction_mismatch_cost_per_partner: float = 1.0
    resident_partners: int = 2

    def __post_init__(self) -> None:
        if not isfinite(self.prior_early) or not 0.0 < self.prior_early < 1.0:
            raise ValueError("prior_early must lie strictly between 0 and 1")
        if (
            not isfinite(self.cue_accuracy)
            or not 0.5 <= self.cue_accuracy <= 1.0
        ):
            raise ValueError("cue_accuracy must lie in [0.5, 1]")
        for name in (
            "false_early_cost",
            "missed_early_cost",
            "migrant_interaction_mismatch_cost",
            "resident_interaction_mismatch_cost_per_partner",
        ):
            value = float(getattr(self, name))
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be non-negative and finite")
        if self.false_early_cost + self.missed_early_cost <= 0.0:
            raise ValueError("at least one state-mismatch cost must be positive")
        if self.resident_partners < 0:
            raise ValueError("resident_partners must be non-negative")


@dataclass(frozen=True)
class TimingGameDiagnostic:
    posterior_early_after_late_cue: float
    posterior_early_after_early_cue: float
    private_threshold: float
    joint_threshold: float
    private_critical_accuracy: float
    joint_critical_accuracy: float
    early_cue_private_action: Action
    early_cue_joint_action: Action
    late_cue_private_action: Action
    late_cue_joint_action: Action
    early_cue_regime: Regime
    expected_joint_loss_private_policy: float
    expected_joint_loss_joint_policy: float
    capacity_deficit: float
    information_deficit: float
    coordination_deficit: float
    total_adaptation_deficit: float
    accuracy_wedge_width: float


def posterior_early(
    game: PartialInformationTimingGame,
    cue: Cue,
) -> float:
    """Posterior P(early spring | cue) under a symmetric binary cue."""

    prior = game.prior_early
    q = game.cue_accuracy
    if cue == "early":
        early_weight = prior * q
        late_weight = (1.0 - prior) * (1.0 - q)
    elif cue == "late":
        early_weight = prior * (1.0 - q)
        late_weight = (1.0 - prior) * q
    else:
        raise ValueError("cue must be 'late' or 'early'")
    return early_weight / (early_weight + late_weight)


def private_action_threshold(game: PartialInformationTimingGame) -> float:
    """Posterior threshold above which early departure is privately optimal."""

    false_loss = (
        game.false_early_cost + game.migrant_interaction_mismatch_cost
    )
    missed_loss = (
        game.missed_early_cost + game.migrant_interaction_mismatch_cost
    )
    return false_loss / (false_loss + missed_loss)


def joint_action_threshold(game: PartialInformationTimingGame) -> float:
    """Posterior threshold above which early departure maximizes joint payoff."""

    externality = (
        game.resident_partners
        * game.resident_interaction_mismatch_cost_per_partner
    )
    false_loss = (
        game.false_early_cost
        + game.migrant_interaction_mismatch_cost
        + externality
    )
    missed_loss = (
        game.missed_early_cost
        + game.migrant_interaction_mismatch_cost
        + externality
    )
    return false_loss / (false_loss + missed_loss)


def critical_early_cue_accuracy(
    prior_early: float,
    action_threshold: float,
) -> float:
    """Cue accuracy at which an early cue puts the posterior on the threshold."""

    if not isfinite(prior_early) or not 0.0 < prior_early < 1.0:
        raise ValueError("prior_early must lie strictly between 0 and 1")
    if (
        not isfinite(action_threshold)
        or not 0.0 < action_threshold < 1.0
    ):
        raise ValueError("action_threshold must lie strictly between 0 and 1")

    numerator = action_threshold * (1.0 - prior_early)
    denominator = (
        prior_early * (1.0 - action_threshold)
        + action_threshold * (1.0 - prior_early)
    )
    return numerator / denominator


def _action_from_posterior(
    posterior: float,
    threshold: float,
) -> Action:
    # Ties are conservatively assigned to late. The strict threshold makes
    # boundary behavior deterministic and leaves all open-interval results
    # unchanged.
    return "early" if posterior > threshold else "late"


def _cue_probability(
    game: PartialInformationTimingGame,
    cue: Cue,
) -> float:
    prior = game.prior_early
    q = game.cue_accuracy
    if cue == "early":
        return prior * q + (1.0 - prior) * (1.0 - q)
    if cue == "late":
        return prior * (1.0 - q) + (1.0 - prior) * q
    raise ValueError("cue must be 'late' or 'early'")


def _conditional_joint_loss(
    game: PartialInformationTimingGame,
    cue: Cue,
    action: Action,
) -> float:
    posterior = posterior_early(game, cue)
    externality = (
        game.resident_partners
        * game.resident_interaction_mismatch_cost_per_partner
    )
    false_loss = (
        game.false_early_cost
        + game.migrant_interaction_mismatch_cost
        + externality
    )
    missed_loss = (
        game.missed_early_cost
        + game.migrant_interaction_mismatch_cost
        + externality
    )
    if action == "early":
        return (1.0 - posterior) * false_loss
    return posterior * missed_loss


def evaluate_partial_information_game(
    game: PartialInformationTimingGame,
) -> TimingGameDiagnostic:
    """Evaluate private versus joint policies under the same noisy cue.

    With adequate timing capacity, perfect information has zero loss. The total
    joint adaptation deficit therefore decomposes exactly into:

        information deficit
        + coordination deficit,

    with capacity deficit fixed at zero in this minimal game.

    information deficit:
        loss remaining under the joint-optimal signal-contingent policy.

    coordination deficit:
        extra joint loss from the migrant following its private optimum rather
        than the joint optimum.
    """

    private_threshold = private_action_threshold(game)
    joint_threshold = joint_action_threshold(game)
    post_late = posterior_early(game, "late")
    post_early = posterior_early(game, "early")

    private_actions = {
        "late": _action_from_posterior(post_late, private_threshold),
        "early": _action_from_posterior(post_early, private_threshold),
    }
    joint_actions = {
        "late": _action_from_posterior(post_late, joint_threshold),
        "early": _action_from_posterior(post_early, joint_threshold),
    }

    if private_actions["early"] == "early" and joint_actions["early"] == "early":
        regime: Regime = "aligned_early"
    elif (
        private_actions["early"] == "late"
        and joint_actions["early"] == "early"
    ):
        regime = "information_coordination_wedge"
    elif (
        private_actions["early"] == "late"
        and joint_actions["early"] == "late"
    ):
        regime = "information_limited"
    else:
        regime = "private_early_joint_late"

    private_policy_joint_loss = 0.0
    joint_policy_joint_loss = 0.0
    for cue in ("late", "early"):
        cue_probability = _cue_probability(game, cue)
        private_policy_joint_loss += cue_probability * _conditional_joint_loss(
            game,
            cue,
            private_actions[cue],
        )
        joint_policy_joint_loss += cue_probability * _conditional_joint_loss(
            game,
            cue,
            joint_actions[cue],
        )

    information_deficit = joint_policy_joint_loss
    coordination_deficit = (
        private_policy_joint_loss - joint_policy_joint_loss
    )
    if coordination_deficit < 0.0 and abs(coordination_deficit) < 1e-12:
        coordination_deficit = 0.0

    private_critical = critical_early_cue_accuracy(
        game.prior_early,
        private_threshold,
    )
    joint_critical = critical_early_cue_accuracy(
        game.prior_early,
        joint_threshold,
    )

    capacity_deficit = 0.0
    total_deficit = (
        capacity_deficit + information_deficit + coordination_deficit
    )

    return TimingGameDiagnostic(
        posterior_early_after_late_cue=post_late,
        posterior_early_after_early_cue=post_early,
        private_threshold=private_threshold,
        joint_threshold=joint_threshold,
        private_critical_accuracy=private_critical,
        joint_critical_accuracy=joint_critical,
        early_cue_private_action=private_actions["early"],
        early_cue_joint_action=joint_actions["early"],
        late_cue_private_action=private_actions["late"],
        late_cue_joint_action=joint_actions["late"],
        early_cue_regime=regime,
        expected_joint_loss_private_policy=private_policy_joint_loss,
        expected_joint_loss_joint_policy=joint_policy_joint_loss,
        capacity_deficit=capacity_deficit,
        information_deficit=information_deficit,
        coordination_deficit=coordination_deficit,
        total_adaptation_deficit=total_deficit,
        accuracy_wedge_width=max(0.0, private_critical - joint_critical),
    )
