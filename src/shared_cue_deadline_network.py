"""Shared-cue information-acquisition coordination for PAYOFF-B.

This module connects the information-deadline theorem to interaction-network
coordination.  Unlike the private-signal Bayesian game, all players here can
observe the same future cue if they pay their own acquisition / waiting cost.

The key exact q=1 result is a perfect-information coordination trap: coordinated
cue use can improve joint payoff even though no single player benefits from
being the first to use the information.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import isfinite
from typing import Iterable

from src.bayesian_timing_coordination import (
    ALWAYS_EARLY,
    ALWAYS_LATE,
    FOLLOW_CUE,
    INVERT_CUE,
    POLICIES,
    Policy,
)
from src.endogenous_information_timing import prior_optimal_action


@dataclass(frozen=True)
class SharedCuePlayer:
    name: str
    false_early_cost: float
    missed_early_cost: float
    interaction_strength: float
    information_cost: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("player name must be non-empty")
        for field in (
            "false_early_cost",
            "missed_early_cost",
            "interaction_strength",
            "information_cost",
        ):
            value = float(getattr(self, field))
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{field} must be non-negative and finite")
        if self.false_early_cost + self.missed_early_cost <= 0.0:
            raise ValueError("at least one state-mismatch cost is required")


@dataclass(frozen=True)
class SharedCueGame:
    prior_early: float
    cue_accuracy: float
    players: tuple[SharedCuePlayer, ...]
    interaction_weights: tuple[tuple[float, ...], ...] | None = None

    def __post_init__(self) -> None:
        if not isfinite(self.prior_early) or not 0.0 < self.prior_early < 1.0:
            raise ValueError("prior_early must lie strictly between 0 and 1")
        if not isfinite(self.cue_accuracy) or not 0.5 <= self.cue_accuracy <= 1.0:
            raise ValueError("cue_accuracy must lie in [0.5,1]")
        if len(self.players) < 2:
            raise ValueError("at least two players are required")
        if len({player.name for player in self.players}) != len(self.players):
            raise ValueError("player names must be unique")
        if self.interaction_weights is not None:
            n = len(self.players)
            if len(self.interaction_weights) != n:
                raise ValueError("interaction_weights must have one row per player")
            for i, row in enumerate(self.interaction_weights):
                if len(row) != n:
                    raise ValueError("interaction_weights must be square")
                for j, value in enumerate(row):
                    if not isfinite(value) or value < 0.0:
                        raise ValueError("interaction weights must be finite and non-negative")
                    if i == j and value != 0.0:
                        raise ValueError("interaction-weight diagonal must be zero")


@dataclass(frozen=True)
class SharedCueProfile:
    profile: tuple[Policy, ...]
    expected_payoffs: tuple[float, ...]

    @property
    def joint_payoff(self) -> float:
        return sum(self.expected_payoffs)


@dataclass(frozen=True)
class PerfectInformationTrap:
    common_prior_action: int
    prior_state_probability_opposite_action: float
    prior_risks: tuple[float, ...]
    information_costs: tuple[float, ...]
    interaction_penalties_for_first_mover: tuple[float, ...]
    unilateral_information_gains: tuple[float, ...]
    joint_information_gain: float
    old_profile_is_nash: bool
    old_profile_is_strict_nash: bool
    informed_profile_is_nash: bool
    informed_profile_is_strict_nash: bool
    coordinated_information_is_better: bool
    perfect_information_coordination_trap: bool


def _uses_information(policy: Policy) -> bool:
    return policy[0] != policy[1]


def _mismatch_fraction(
    game: SharedCueGame,
    actions: list[int],
    player_index: int,
) -> float:
    action = actions[player_index]
    n = len(actions)
    if game.interaction_weights is None:
        return (
            sum(
                actions[j] != action
                for j in range(n)
                if j != player_index
            )
            / (n - 1)
        )
    weights = game.interaction_weights[player_index]
    denominator = sum(
        weights[j]
        for j in range(n)
        if j != player_index
    )
    if denominator <= 0.0:
        return 0.0
    return (
        sum(
            weights[j]
            for j in range(n)
            if j != player_index and actions[j] != action
        )
        / denominator
    )


def evaluate_shared_cue_profile(
    game: SharedCueGame,
    profile: Iterable[Policy],
) -> SharedCueProfile:
    profile_tuple = tuple(profile)
    if len(profile_tuple) != len(game.players):
        raise ValueError("profile length must match players")
    if any(policy not in POLICIES for policy in profile_tuple):
        raise ValueError("unknown policy")

    expected = [0.0] * len(game.players)
    for state in (0, 1):
        state_probability = (
            game.prior_early
            if state == 1
            else 1.0 - game.prior_early
        )
        for signal in (0, 1):
            signal_probability = (
                game.cue_accuracy
                if signal == state
                else 1.0 - game.cue_accuracy
            )
            probability = state_probability * signal_probability
            actions = [
                policy[signal]
                for policy in profile_tuple
            ]
            for i, player in enumerate(game.players):
                if actions[i] == state:
                    state_loss = 0.0
                elif state == 1:
                    state_loss = player.missed_early_cost
                else:
                    state_loss = player.false_early_cost
                interaction_loss = (
                    player.interaction_strength
                    * _mismatch_fraction(game, actions, i)
                )
                expected[i] += probability * (
                    -state_loss - interaction_loss
                )

    for i, (player, policy) in enumerate(
        zip(game.players, profile_tuple)
    ):
        if _uses_information(policy):
            expected[i] -= player.information_cost

    return SharedCueProfile(
        profile=profile_tuple,
        expected_payoffs=tuple(expected),
    )


def is_shared_cue_nash(
    game: SharedCueGame,
    profile: Iterable[Policy],
    *,
    strict: bool = False,
    tolerance: float = 1e-12,
) -> bool:
    profile_tuple = tuple(profile)
    baseline = evaluate_shared_cue_profile(game, profile_tuple)
    for i in range(len(game.players)):
        current = baseline.expected_payoffs[i]
        alternatives = []
        for policy in POLICIES:
            if policy == profile_tuple[i]:
                continue
            candidate = list(profile_tuple)
            candidate[i] = policy
            alternatives.append(
                evaluate_shared_cue_profile(
                    game,
                    candidate,
                ).expected_payoffs[i]
            )
        best_alternative = max(alternatives)
        if strict:
            if current <= best_alternative + tolerance:
                return False
        elif current < best_alternative - tolerance:
            return False
    return True


def sequential_shared_cue_best_response(
    game: SharedCueGame,
    initial_profile: Iterable[Policy],
    *,
    max_cycles: int = 100,
    tolerance: float = 1e-12,
) -> tuple[SharedCueProfile, ...]:
    current = tuple(initial_profile)
    path = [evaluate_shared_cue_profile(game, current)]
    for _ in range(max_cycles):
        changed = False
        working = list(current)
        for i in range(len(game.players)):
            current_eval = evaluate_shared_cue_profile(game, working)
            current_payoff = current_eval.expected_payoffs[i]
            candidates = []
            for policy in POLICIES:
                candidate = list(working)
                candidate[i] = policy
                payoff = evaluate_shared_cue_profile(
                    game,
                    candidate,
                ).expected_payoffs[i]
                candidates.append((payoff, policy))
            best = max(value for value, _ in candidates)
            if current_payoff >= best - tolerance:
                continue
            best_policy = next(
                policy
                for value, policy in candidates
                if abs(value - best) <= tolerance
            )
            working[i] = best_policy
            current = tuple(working)
            path.append(evaluate_shared_cue_profile(game, current))
            changed = True
        current = tuple(working)
        if not changed:
            return tuple(path)
    raise RuntimeError("shared-cue best response did not converge")


def perfect_information_coordination_trap(
    game: SharedCueGame,
) -> PerfectInformationTrap:
    """Diagnose exact q=1 coordinated information use.

    This theorem diagnostic requires all players to share the same prior-optimal
    constant action.  It compares that uninformed profile with all players
    following a perfect shared cue.
    """

    if abs(game.cue_accuracy - 1.0) > 1e-12:
        raise ValueError("perfect-information trap diagnostic requires q=1")

    prior_actions = tuple(
        prior_optimal_action(
            game.prior_early,
            player.false_early_cost,
            player.missed_early_cost,
        )
        for player in game.players
    )
    if len(set(prior_actions)) != 1:
        raise ValueError("players must share one prior-optimal action")
    prior_action = prior_actions[0]
    old_policy = ALWAYS_LATE if prior_action == 0 else ALWAYS_EARLY
    old_profile = tuple(old_policy for _ in game.players)
    informed_profile = tuple(FOLLOW_CUE for _ in game.players)

    if prior_action == 0:
        switch_probability = game.prior_early
        prior_risks = tuple(
            game.prior_early * player.missed_early_cost
            for player in game.players
        )
    else:
        switch_probability = 1.0 - game.prior_early
        prior_risks = tuple(
            (1.0 - game.prior_early) * player.false_early_cost
            for player in game.players
        )

    first_mover_penalties = tuple(
        switch_probability * player.interaction_strength
        for player in game.players
    )
    information_costs = tuple(
        player.information_cost
        for player in game.players
    )
    unilateral_gains = tuple(
        risk - cost - penalty
        for risk, cost, penalty in zip(
            prior_risks,
            information_costs,
            first_mover_penalties,
        )
    )
    joint_gain = sum(prior_risks) - sum(information_costs)

    old_nash = is_shared_cue_nash(
        game,
        old_profile,
        strict=False,
    )
    old_strict = is_shared_cue_nash(
        game,
        old_profile,
        strict=True,
    )
    informed_nash = is_shared_cue_nash(
        game,
        informed_profile,
        strict=False,
    )
    informed_strict = is_shared_cue_nash(
        game,
        informed_profile,
        strict=True,
    )
    coordinated_better = joint_gain > 1e-12
    trap = old_nash and coordinated_better

    return PerfectInformationTrap(
        common_prior_action=prior_action,
        prior_state_probability_opposite_action=switch_probability,
        prior_risks=prior_risks,
        information_costs=information_costs,
        interaction_penalties_for_first_mover=first_mover_penalties,
        unilateral_information_gains=unilateral_gains,
        joint_information_gain=joint_gain,
        old_profile_is_nash=old_nash,
        old_profile_is_strict_nash=old_strict,
        informed_profile_is_nash=informed_nash,
        informed_profile_is_strict_nash=informed_strict,
        coordinated_information_is_better=coordinated_better,
        perfect_information_coordination_trap=trap,
    )


def canonical_shared_cue_deadline_game(
    cue_accuracy: float,
    *,
    interaction_topology: str = "chain",
) -> SharedCueGame:
    """Transparent three-player deadline-network witness."""

    if interaction_topology == "complete":
        weights = None
    elif interaction_topology == "chain":
        weights = (
            (0.0, 1.0, 0.0),
            (1.0, 0.0, 1.0),
            (0.0, 1.0, 0.0),
        )
    elif interaction_topology == "migrant_star":
        weights = (
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
            (1.0, 1.0, 0.0),
        )
    else:
        raise ValueError(
            "interaction_topology must be complete, chain, or migrant_star"
        )

    return SharedCueGame(
        prior_early=0.40,
        cue_accuracy=cue_accuracy,
        players=(
            SharedCuePlayer(
                name="flower",
                false_early_cost=1.0,
                missed_early_cost=0.25,
                interaction_strength=0.50,
                information_cost=0.05,
            ),
            SharedCuePlayer(
                name="local_pollinator",
                false_early_cost=1.0,
                missed_early_cost=0.25,
                interaction_strength=0.50,
                information_cost=0.10,
            ),
            SharedCuePlayer(
                name="migrant",
                false_early_cost=2.0,
                missed_early_cost=1.0,
                interaction_strength=0.50,
                information_cost=0.30,
            ),
        ),
        interaction_weights=weights,
    )
