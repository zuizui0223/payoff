"""Finite Bayesian timing-coordination game for PAYOFF-B.

Players choose early/late timing as a function of a private binary cue about a
shared hidden spring state. Payoffs combine state mismatch and pairwise timing
mismatch. The finite strategy space allows exact enumeration of pure Bayesian
Nash equilibria and deterministic sequential best-response dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product
from math import isfinite
from typing import Iterable


Policy = tuple[int, int]
ALWAYS_LATE: Policy = (0, 0)
FOLLOW_CUE: Policy = (0, 1)
INVERT_CUE: Policy = (1, 0)
ALWAYS_EARLY: Policy = (1, 1)
POLICIES: tuple[Policy, ...] = (
    ALWAYS_LATE,
    FOLLOW_CUE,
    INVERT_CUE,
    ALWAYS_EARLY,
)


@dataclass(frozen=True)
class TimingPlayer:
    name: str
    cue_accuracy: float
    false_early_cost: float
    missed_early_cost: float
    interaction_strength: float

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
        ):
            value = float(getattr(self, name))
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be non-negative and finite")
        if self.false_early_cost + self.missed_early_cost <= 0.0:
            raise ValueError("at least one state-mismatch cost must be positive")


@dataclass(frozen=True)
class BayesianTimingGame:
    prior_early: float
    players: tuple[TimingPlayer, ...]
    interaction_weights: tuple[tuple[float, ...], ...] | None = None

    def __post_init__(self) -> None:
        if not isfinite(self.prior_early) or not 0.0 < self.prior_early < 1.0:
            raise ValueError("prior_early must lie strictly between 0 and 1")
        if len(self.players) < 2:
            raise ValueError("at least two players are required")
        if len({player.name for player in self.players}) != len(self.players):
            raise ValueError("player names must be unique")
        if self.interaction_weights is not None:
            if len(self.interaction_weights) != len(self.players):
                raise ValueError(
                    "interaction_weights must have one row per player"
                )
            for index, row in enumerate(self.interaction_weights):
                if len(row) != len(self.players):
                    raise ValueError(
                        "interaction_weights must be a square matrix"
                    )
                for other_index, value in enumerate(row):
                    if not isfinite(value) or value < 0.0:
                        raise ValueError(
                            "interaction weights must be non-negative and finite"
                        )
                    if index == other_index and value != 0.0:
                        raise ValueError(
                            "interaction-weight diagonal must be zero"
                        )


@dataclass(frozen=True)
class ProfileEvaluation:
    profile: tuple[Policy, ...]
    expected_payoffs: tuple[float, ...]

    @property
    def joint_payoff(self) -> float:
        return sum(self.expected_payoffs)


@dataclass(frozen=True)
class BestResponseResult:
    path: tuple[ProfileEvaluation, ...]
    converged: bool
    cycles: int

    @property
    def final(self) -> ProfileEvaluation:
        return self.path[-1]


def policy_label(policy: Policy) -> str:
    if policy == ALWAYS_LATE:
        return "always_late"
    if policy == FOLLOW_CUE:
        return "follow_cue"
    if policy == INVERT_CUE:
        return "invert_cue"
    if policy == ALWAYS_EARLY:
        return "always_early"
    raise ValueError("unknown policy")


def with_player_accuracy(
    game: BayesianTimingGame,
    player_index: int,
    cue_accuracy: float,
) -> BayesianTimingGame:
    if not 0 <= player_index < len(game.players):
        raise IndexError("player_index out of range")
    players = list(game.players)
    players[player_index] = replace(
        players[player_index],
        cue_accuracy=cue_accuracy,
    )
    return replace(game, players=tuple(players))


def _signal_probability(signal: int, state: int, accuracy: float) -> float:
    return accuracy if signal == state else 1.0 - accuracy


def evaluate_profile(
    game: BayesianTimingGame,
    profile: Iterable[Policy],
) -> ProfileEvaluation:
    profile_tuple = tuple(profile)
    n_players = len(game.players)
    if len(profile_tuple) != n_players:
        raise ValueError("profile length must match number of players")
    if any(policy not in POLICIES for policy in profile_tuple):
        raise ValueError("profile contains an unknown policy")

    expected = [0.0 for _ in game.players]

    for state in (0, 1):
        state_probability = (
            game.prior_early if state == 1 else 1.0 - game.prior_early
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
                profile_tuple[index][signals[index]]
                for index in range(n_players)
            ]

            for index, player in enumerate(game.players):
                action = actions[index]
                state_loss = 0.0
                if action != state:
                    state_loss = (
                        player.missed_early_cost
                        if state == 1
                        else player.false_early_cost
                    )

                if game.interaction_weights is None:
                    mismatch_fraction = (
                        sum(
                            1
                            for other_index, other_action
                            in enumerate(actions)
                            if (
                                other_index != index
                                and other_action != action
                            )
                        )
                        / (n_players - 1)
                    )
                else:
                    weights = game.interaction_weights[index]
                    weight_sum = sum(
                        weight
                        for other_index, weight in enumerate(weights)
                        if other_index != index
                    )
                    if weight_sum <= 0.0:
                        mismatch_fraction = 0.0
                    else:
                        mismatch_fraction = (
                            sum(
                                weights[other_index]
                                for other_index, other_action
                                in enumerate(actions)
                                if (
                                    other_index != index
                                    and other_action != action
                                )
                            )
                            / weight_sum
                        )
                interaction_loss = (
                    player.interaction_strength
                    * mismatch_fraction
                )
                expected[index] += probability * (
                    -state_loss - interaction_loss
                )

    return ProfileEvaluation(
        profile=profile_tuple,
        expected_payoffs=tuple(expected),
    )


def is_pure_bayesian_nash(
    game: BayesianTimingGame,
    profile: Iterable[Policy],
    *,
    tolerance: float = 1e-12,
) -> bool:
    if tolerance < 0.0:
        raise ValueError("tolerance must be non-negative")
    profile_tuple = tuple(profile)
    baseline = evaluate_profile(game, profile_tuple)

    for player_index in range(len(game.players)):
        baseline_payoff = baseline.expected_payoffs[player_index]
        for alternative in POLICIES:
            if alternative == profile_tuple[player_index]:
                continue
            candidate = list(profile_tuple)
            candidate[player_index] = alternative
            candidate_payoff = evaluate_profile(
                game,
                candidate,
            ).expected_payoffs[player_index]
            if candidate_payoff > baseline_payoff + tolerance:
                return False
    return True


def pure_bayesian_nash_equilibria(
    game: BayesianTimingGame,
    *,
    tolerance: float = 1e-12,
) -> tuple[ProfileEvaluation, ...]:
    """Enumerate all pure Bayesian Nash equilibria.

    The state space is 4^N policy profiles, so this exact enumerator is intended
    for the small interaction systems used in PAYOFF-B, not large communities.
    """

    if len(game.players) > 6:
        raise ValueError("exact equilibrium enumeration is limited to <= 6 players")

    equilibria: list[ProfileEvaluation] = []
    for profile in product(POLICIES, repeat=len(game.players)):
        if is_pure_bayesian_nash(
            game,
            profile,
            tolerance=tolerance,
        ):
            equilibria.append(evaluate_profile(game, profile))
    equilibria.sort(key=lambda row: row.joint_payoff, reverse=True)
    return tuple(equilibria)


def sequential_best_response(
    game: BayesianTimingGame,
    initial_profile: Iterable[Policy],
    *,
    max_cycles: int = 100,
    improvement_tolerance: float = 1e-12,
) -> BestResponseResult:
    """Sequential best-response dynamics with path-preserving tie handling.

    Players update in declared order. If the current policy is already tied for
    best response, it is retained. This makes historical state explicit rather
    than resolving ties by arbitrary policy replacement.
    """

    if max_cycles <= 0:
        raise ValueError("max_cycles must be positive")
    if improvement_tolerance < 0.0:
        raise ValueError("improvement_tolerance must be non-negative")

    current = tuple(initial_profile)
    if len(current) != len(game.players):
        raise ValueError("initial profile length must match number of players")

    path = [evaluate_profile(game, current)]

    for cycle in range(1, max_cycles + 1):
        changed = False
        working = list(current)

        for player_index in range(len(game.players)):
            current_evaluation = evaluate_profile(game, working)
            current_payoff = current_evaluation.expected_payoffs[player_index]

            candidates: list[tuple[float, Policy]] = []
            for policy in POLICIES:
                candidate = list(working)
                candidate[player_index] = policy
                payoff = evaluate_profile(
                    game,
                    candidate,
                ).expected_payoffs[player_index]
                candidates.append((payoff, policy))

            best_payoff = max(payoff for payoff, _ in candidates)
            if current_payoff >= best_payoff - improvement_tolerance:
                continue

            best_policy = next(
                policy
                for payoff, policy in candidates
                if abs(payoff - best_payoff) <= improvement_tolerance
            )
            working[player_index] = best_policy
            current = tuple(working)
            path.append(evaluate_profile(game, current))
            changed = True

        current = tuple(working)
        if not changed:
            return BestResponseResult(
                path=tuple(path),
                converged=True,
                cycles=cycle,
            )

    return BestResponseResult(
        path=tuple(path),
        converged=False,
        cycles=max_cycles,
    )


def canonical_three_player_game(
    migrant_accuracy: float,
    *,
    interaction_strength: float = 0.50,
    local_accuracy: float = 0.90,
    prior_early: float = 0.40,
    interaction_topology: str = "complete",
) -> BayesianTimingGame:
    """Transparent resident--resident--migrant hysteresis witness.

    The numbers are mechanism probes, not empirical parameter estimates.
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

    return BayesianTimingGame(
        prior_early=prior_early,
        players=(
            TimingPlayer(
                name="flower",
                cue_accuracy=local_accuracy,
                false_early_cost=1.0,
                missed_early_cost=0.25,
                interaction_strength=interaction_strength,
            ),
            TimingPlayer(
                name="local_pollinator",
                cue_accuracy=local_accuracy,
                false_early_cost=1.0,
                missed_early_cost=0.25,
                interaction_strength=interaction_strength,
            ),
            TimingPlayer(
                name="migrant",
                cue_accuracy=migrant_accuracy,
                false_early_cost=2.0,
                missed_early_cost=1.0,
                interaction_strength=interaction_strength,
            ),
        ),
        interaction_weights=interaction_weights,
    )
