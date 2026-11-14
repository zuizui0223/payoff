"""Counterfactual seasonal adaptation deficits with interactions.

Source-free finite Bayesian example. Not a fit to any ecological data.

Perfect versus available information and full versus limited action capacity
are crossed under an identical *joint-loss* objective. Their two possible
nested decompositions are averaged (two-factor Shapley allocation).
A decentralized/private-optimal policy is evaluated on the SAME joint
loss scale, and its coordination excess is added last.

The result is an exact, nonnegative accounting identity for these declared
counterfactuals. It is NOT an identified causal allocation in nature.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping, Sequence


Losses = Mapping[str, tuple[float, float]]


@dataclass(frozen=True)
class CounterfactualDeficits:
    full_perfect: float
    limited_perfect: float
    full_cue: float
    limited_cue: float
    decentralized_cue: float
    information_deficit: float
    capacity_deficit: float
    coordination_deficit: float
    total_deficit: float
    information_capacity_interaction: float
    information_if_full_capacity: float
    information_if_limited_capacity: float
    capacity_if_perfect_information: float
    capacity_if_available_cue: float
    joint_policy_late_cue: str
    joint_policy_early_cue: str
    decentralized_policy_late_cue: str
    decentralized_policy_early_cue: str


def _weighted_action_loss(
    prior_early: float,
    cue_accuracy: float,
    cue: int,
    action: str,
    losses: Losses,
) -> float:
    """Unnormalized joint probability multiplied by action loss."""
    p = prior_early
    q = cue_accuracy
    p_cue_given_late = q if cue == 0 else 1 - q
    p_cue_given_early = 1 - q if cue == 0 else q
    loss_late, loss_early = losses[action]
    return (
        (1 - p) * p_cue_given_late * loss_late
        + p * p_cue_given_early * loss_early
    )


def _cue_optimal_policy(
    prior_early: float,
    cue_accuracy: float,
    actions: tuple[str, ...],
    losses: Losses,
) -> tuple[str, str]:
    # Stable first-action tie break; tie resolution may change the social
    # cost of a privately indifferent action.
    return tuple(
        min(
            actions,
            key=lambda action: _weighted_action_loss(
                prior_early, cue_accuracy, cue, action, losses
            ),
        )
        for cue in (0, 1)
    )


def _score_policy(
    prior_early: float,
    cue_accuracy: float,
    policy: tuple[str, str],
    losses: Losses,
) -> float:
    return sum(
        _weighted_action_loss(prior_early, cue_accuracy, cue, action, losses)
        for cue, action in enumerate(policy)
    )


def _perfect_information_risk(
    prior_early: float,
    actions: tuple[str, ...],
    losses: Losses,
) -> float:
    return (
        (1 - prior_early) * min(losses[a][0] for a in actions)
        + prior_early * min(losses[a][1] for a in actions)
    )


def decompose_seasonal_deficit(
    *,
    prior_early: float,
    cue_accuracy: float,
    joint_losses: Losses,
    private_losses: Losses,
    limited_actions: Sequence[str],
    full_actions: Sequence[str],
) -> CounterfactualDeficits:
    """Evaluate five counterfactual risks on a common expected-loss scale.

    There are two ecological states (late=0, early=1) and two cues.
    Cues correctly indicate the state with symmetric accuracy q.

    The decentralized policy minimizes private expected loss conditional on
    the cue, with the limited action set. The remaining four risks minimize
    *joint* loss under the crossed information/capacity scenarios.

    Full actions must contain all limited actions. No assumption that
    maximizing social welfare is individually evolutionarily accessible.
    """
    if (
        not isfinite(prior_early)
        or not 0 < prior_early < 1
        or not isfinite(cue_accuracy)
        or not 0.5 <= cue_accuracy <= 1
    ):
        raise ValueError("Need 0<prior_early<1 and 0.5<=cue_accuracy<=1")

    limited = tuple(limited_actions)
    full = tuple(full_actions)
    if not limited or not full:
        raise ValueError("Both action sets must be nonempty")
    if len(set(limited)) != len(limited) or len(set(full)) != len(full):
        raise ValueError("Actions must be unique within each set")
    if not set(limited).issubset(full):
        raise ValueError("The limited action set must be a subset of full actions")

    for action in full:
        for name, losses in (("joint", joint_losses), ("private", private_losses)):
            if action not in losses:
                raise ValueError(f"Missing {name} losses for action {action!r}")
            pair = losses[action]
            if len(pair) != 2 or any(
                not isfinite(value) or value < 0 for value in pair
            ):
                raise ValueError("Each action needs two finite nonnegative state losses")

    p = prior_early
    q = cue_accuracy
    joint_policy_limited = _cue_optimal_policy(p, q, limited, joint_losses)
    joint_policy_full = _cue_optimal_policy(p, q, full, joint_losses)
    private_policy = _cue_optimal_policy(p, q, limited, private_losses)

    lc = _score_policy(p, q, joint_policy_limited, joint_losses)
    fc = _score_policy(p, q, joint_policy_full, joint_losses)
    dc = _score_policy(p, q, private_policy, joint_losses)
    lp = _perfect_information_risk(p, limited, joint_losses)
    fp = _perfect_information_risk(p, full, joint_losses)

    information_full = fc - fp
    information_limited = lc - lp
    capacity_perfect = lp - fp
    capacity_cue = lc - fc
    information = (information_full + information_limited) / 2
    capacity = (capacity_perfect + capacity_cue) / 2
    coordination = dc - lc
    total = dc - fp
    interaction = information_limited - information_full

    values = (
        information_full, information_limited, capacity_perfect,
        capacity_cue, information, capacity, coordination, total,
    )
    if min(values) < -1e-9:
        raise ArithmeticError("Nested joint-risk monotonicity was violated")
    if abs((information + capacity + coordination) - total) > 1e-9:
        raise ArithmeticError("Counterfactual allocation does not telescope")

    return CounterfactualDeficits(
        full_perfect=fp,
        limited_perfect=lp,
        full_cue=fc,
        limited_cue=lc,
        decentralized_cue=dc,
        information_deficit=information,
        capacity_deficit=capacity,
        coordination_deficit=coordination,
        total_deficit=total,
        information_capacity_interaction=interaction,
        information_if_full_capacity=information_full,
        information_if_limited_capacity=information_limited,
        capacity_if_perfect_information=capacity_perfect,
        capacity_if_available_cue=capacity_cue,
        joint_policy_late_cue=joint_policy_limited[0],
        joint_policy_early_cue=joint_policy_limited[1],
        decentralized_policy_late_cue=private_policy[0],
        decentralized_policy_early_cue=private_policy[1],
    )
