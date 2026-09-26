"""Endogenous information acquisition embedded in a timing network.

This module unifies two PAYOFF-B layers that were previously separate:

1. whether an actor commits before a cue or waits to use it;
2. whether interaction-dependent timing payoffs make information uptake
   strategically accessible.

Policies use the same binary representation as the finite Bayesian timing game:

    ALWAYS_LATE  = commit late before observing the cue
    FOLLOW_CUE   = wait, pay the delay cost, then follow the cue
    INVERT_CUE   = wait, pay the delay cost, then invert the cue
    ALWAYS_EARLY = commit early before observing the cue

Cue-contingent policies incur the player's delay cost. Constant policies do not.
The model is exact for the declared finite strategy space.
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
    policy_label,
)


WAIT_POLICIES: tuple[Policy, Policy] = (
    FOLLOW_CUE,
    INVERT_CUE,
)


@dataclass(frozen=True)
class InformationNetworkPlayer:
    name: str
    cue_accuracy: float
    false_early_cost: float
    missed_early_cost: float
    interaction_strength: float
    delay_cost: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("player name must be non-empty")
        if (
            not isfinite(self.cue_accuracy)
            or not 0.5 <= self.cue_accuracy <= 1.0
        ):
            raise ValueError("cue_accuracy must lie in [0.5, 1]")
        for name in (
            "false_early_cost",
            "missed_early_cost",
            "interaction_strength",
            "delay_cost",
        ):
            value = float(getattr(self, name))
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be non-negative and finite")
        if self.false_early_cost + self.missed_early_cost <= 0.0:
            raise ValueError("at least one state-mismatch cost is required")


@dataclass(frozen=True)
class EndogenousInformationNetworkGame:
    prior_early: float
    players: tuple[InformationNetworkPlayer, ...]
    interaction_weights: tuple[tuple[float, ...], ...] | None = None

    def __post_init__(self) -> None:
        if (
            not isfinite(self.prior_early)
            or not 0.0 < self.prior_early < 1.0
        ):
            raise ValueError("prior_early must lie strictly between 0 and 1")
        if len(self.players) < 2:
            raise ValueError("at least two players are required")
        if len({player.name for player in self.players}) != len(self.players):
            raise ValueError("player names must be unique")
        if self.interaction_weights is not None:
            n = len(self.players)
            if len(self.interaction_weights) != n:
                raise ValueError(
                    "interaction_weights must have one row per player"
                )
            for i, row in enumerate(self.interaction_weights):
                if len(row) != n:
                    raise ValueError(
                        "interaction_weights must be a square matrix"
                    )
                for j, value in enumerate(row):
                    if not isfinite(value) or value < 0.0:
                        raise ValueError(
                            "interaction weights must be non-negative and finite"
                        )
                    if i == j and value != 0.0:
                        raise ValueError(
                            "interaction-weight diagonal must be zero"
                        )


@dataclass(frozen=True)
class InformationNetworkEvaluation:
    profile: tuple[Policy, ...]
    expected_payoffs: tuple[float, ...]

    @property
    def joint_payoff(self) -> float:
        return sum(self.expected_payoffs)


@dataclass(frozen=True)
class InformationNetworkBestResponse:
    path: tuple[InformationNetworkEvaluation, ...]
    converged: bool
    cycles: int

    @property
    def final(self) -> InformationNetworkEvaluation:
        return self.path[-1]


def _signal_probability(signal: int, state: int, accuracy: float) -> float:
    return accuracy if signal == state else 1.0 - accuracy


def _mismatch_fraction(
    game: EndogenousInformationNetworkGame,
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

    row = game.interaction_weights[player_index]
    total_weight = sum(
        value
        for j, value in enumerate(row)
        if j != player_index
    )
    if total_weight <= 0.0:
        return 0.0
    mismatch_weight = sum(
        row[j]
        for j in range(n)
        if j != player_index and actions[j] != action
    )
    return mismatch_weight / total_weight


def evaluate_information_network(
    game: EndogenousInformationNetworkGame,
    profile: Iterable[Policy],
) -> InformationNetworkEvaluation:
    profile_tuple = tuple(profile)
    n_players = len(game.players)
    if len(profile_tuple) != n_players:
        raise ValueError("profile length must match number of players")
    if any(policy not in POLICIES for policy in profile_tuple):
        raise ValueError("profile contains an unknown policy")

    expected = [0.0 for _ in game.players]

    for state in (0, 1):
        state_probability = (
            game.prior_early if state == 1
            else 1.0 - game.prior_early
        )
        for signals in product((0, 1), repeat=n_players):
            probability = state_probability
            for player, signal in zip(game.players, signals):
                probability *= _signal_probability(
                    signal,
                    state,
                    player.cue_accuracy,
                )

            actions = [
                profile_tuple[i][signals[i]]
                for i in range(n_players)
            ]

            for i, player in enumerate(game.players):
                action = actions[i]
                state_loss = 0.0
                if action != state:
                    state_loss = (
                        player.missed_early_cost
                        if state == 1
                        else player.false_early_cost
                    )
                interaction_loss = (
                    player.interaction_strength
                    * _mismatch_fraction(game, actions, i)
                )
                delay_loss = (
                    player.delay_cost
                    if profile_tuple[i] in WAIT_POLICIES
                    else 0.0
                )
                expected[i] += probability * (
                    -state_loss
                    - interaction_loss
                    - delay_loss
                )

    return InformationNetworkEvaluation(
        profile=profile_tuple,
        expected_payoffs=tuple(expected),
    )


def information_network_best_response_margins(
    game: EndogenousInformationNetworkGame,
    profile: Iterable[Policy],
) -> tuple[float, ...]:
    profile_tuple = tuple(profile)
    baseline = evaluate_information_network(game, profile_tuple)
    margins: list[float] = []

    for i in range(len(game.players)):
        alternatives: list[float] = []
        for policy in POLICIES:
            if policy == profile_tuple[i]:
                continue
            candidate = list(profile_tuple)
            candidate[i] = policy
            alternatives.append(
                evaluate_information_network(
                    game,
                    candidate,
                ).expected_payoffs[i]
            )
        margins.append(
            baseline.expected_payoffs[i] - max(alternatives)
        )
    return tuple(margins)


def is_strict_information_network_equilibrium(
    game: EndogenousInformationNetworkGame,
    profile: Iterable[Policy],
    *,
    minimum_margin: float = 1e-9,
) -> bool:
    if not isfinite(minimum_margin) or minimum_margin <= 0.0:
        raise ValueError("minimum_margin must be positive and finite")
    return (
        min(
            information_network_best_response_margins(
                game,
                profile,
            )
        )
        > minimum_margin
    )


def sequential_information_network_best_response(
    game: EndogenousInformationNetworkGame,
    initial_profile: Iterable[Policy],
    *,
    max_cycles: int = 100,
    improvement_tolerance: float = 1e-12,
) -> InformationNetworkBestResponse:
    if max_cycles <= 0:
        raise ValueError("max_cycles must be positive")
    if improvement_tolerance < 0.0:
        raise ValueError("improvement_tolerance must be non-negative")

    current = tuple(initial_profile)
    if len(current) != len(game.players):
        raise ValueError("initial profile length must match number of players")

    path = [evaluate_information_network(game, current)]

    for cycle in range(1, max_cycles + 1):
        changed = False
        working = list(current)

        for i in range(len(game.players)):
            baseline = evaluate_information_network(game, working)
            current_payoff = baseline.expected_payoffs[i]

            candidates: list[tuple[float, Policy]] = []
            for policy in POLICIES:
                candidate = list(working)
                candidate[i] = policy
                payoff = evaluate_information_network(
                    game,
                    candidate,
                ).expected_payoffs[i]
                candidates.append((payoff, policy))

            best_payoff = max(payoff for payoff, _ in candidates)
            if current_payoff >= best_payoff - improvement_tolerance:
                continue

            best_policy = next(
                policy
                for payoff, policy in candidates
                if abs(payoff - best_payoff) <= improvement_tolerance
            )
            working[i] = best_policy
            current = tuple(working)
            path.append(evaluate_information_network(game, current))
            changed = True

        current = tuple(working)
        if not changed:
            return InformationNetworkBestResponse(
                path=tuple(path),
                converged=True,
                cycles=cycle,
            )

    return InformationNetworkBestResponse(
        path=tuple(path),
        converged=False,
        cycles=max_cycles,
    )


def canonical_endogenous_information_network(
    cue_accuracy: float,
    *,
    interaction_strength: float = 0.50,
    prior_early: float = 0.40,
    interaction_topology: str = "complete",
) -> EndogenousInformationNetworkGame:
    """Three-player witness with heterogeneous opportunity costs of waiting.

    Delay costs are illustrative mechanism-probe values:
      migrant = 0.30
      resident_partner = 0.10
      resource = 0.20

    All players observe cues of the same reliability.  Information asymmetry is
    therefore endogenous to their different incentives to wait, rather than
    imposed through different sensory accuracy.
    """

    if interaction_topology == "complete":
        interaction_weights = None
    elif interaction_topology == "chain":
        interaction_weights = (
            (0.0, 1.0, 0.0),
            (1.0, 0.0, 1.0),
            (0.0, 1.0, 0.0),
        )
    elif interaction_topology == "migrant_star":
        interaction_weights = (
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
            (1.0, 1.0, 0.0),
        )
    else:
        raise ValueError(
            "interaction_topology must be complete, chain, or migrant_star"
        )

    return EndogenousInformationNetworkGame(
        prior_early=prior_early,
        players=(
            InformationNetworkPlayer(
                name="migrant",
                cue_accuracy=cue_accuracy,
                false_early_cost=2.0,
                missed_early_cost=1.0,
                interaction_strength=interaction_strength,
                delay_cost=0.30,
            ),
            InformationNetworkPlayer(
                name="resident_partner",
                cue_accuracy=cue_accuracy,
                false_early_cost=2.0,
                missed_early_cost=1.0,
                interaction_strength=interaction_strength,
                delay_cost=0.10,
            ),
            InformationNetworkPlayer(
                name="resource",
                cue_accuracy=cue_accuracy,
                false_early_cost=2.0,
                missed_early_cost=1.0,
                interaction_strength=interaction_strength,
                delay_cost=0.20,
            ),
        ),
        interaction_weights=interaction_weights,
    )


def profile_labels(profile: Iterable[Policy]) -> tuple[str, ...]:
    return tuple(policy_label(policy) for policy in profile)


def all_commit_late_profile(n_players: int = 3) -> tuple[Policy, ...]:
    return tuple(ALWAYS_LATE for _ in range(n_players))


def all_wait_follow_profile(n_players: int = 3) -> tuple[Policy, ...]:
    return tuple(FOLLOW_CUE for _ in range(n_players))
