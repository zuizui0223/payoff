"""Coalitional rescue from perfect-information coordination traps.

PAYOFF-B's perfect-information theorem shows that a network can remain in an
obsolete uninformed convention even when a perfect cue is available and the
fully informed state has higher joint payoff.

This module asks what coordinated seed is sufficient to escape that trap.

At q=1, let K be a coalition that simultaneously adopts the perfect cue while
all actors outside K retain the old prior-optimal action. For member i in K,

    G_i(K) = R_i - D_i - p I_i b_i(K),

where R_i is prior mismatch risk, D_i information/waiting cost, p is the
probability that perfect information requires the action opposite to the old
convention, I_i is interaction strength, and b_i(K) is the fraction of i's
interaction weight that still points outside K.

A coalition is self-financing when every member has G_i(K) >= 0.  This is a
coalitional accessibility result, not an assumption that species literally
negotiate.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import ceil, floor, isfinite
from typing import Iterable

from src.bayesian_timing_coordination import ALWAYS_EARLY, ALWAYS_LATE, FOLLOW_CUE
from src.endogenous_information_timing import prior_optimal_action
from src.shared_cue_deadline_network import (
    SharedCueGame,
    evaluate_shared_cue_profile,
    sequential_shared_cue_best_response,
)


@dataclass(frozen=True)
class CoalitionAdoption:
    members: tuple[int, ...]
    member_names: tuple[str, ...]
    outside_weight_fractions: tuple[float, ...]
    gains_vs_old: tuple[float, ...]
    weakly_self_financing: bool
    strictly_self_financing: bool
    joint_gain_vs_old: float
    final_profile_after_best_response: tuple[tuple[int, int], ...]
    reaches_fully_informed: bool


@dataclass(frozen=True)
class CompleteGraphCoalitionThreshold:
    n: int
    prior_risk: float
    information_cost: float
    switch_probability: float
    interaction_strength: float
    individual_first_move_gain: float
    full_coalition_gain_per_actor: float
    weak_minimum_size: int | None
    strict_minimum_size: int | None


def _perfect_information_components(game: SharedCueGame):
    if abs(game.cue_accuracy - 1.0) > 1e-12:
        raise ValueError("coalition rescue diagnostic requires cue accuracy q=1")

    prior_actions = tuple(
        prior_optimal_action(
            game.prior_early,
            player.false_early_cost,
            player.missed_early_cost,
        )
        for player in game.players
    )
    if len(set(prior_actions)) != 1:
        raise ValueError("players must share one prior-optimal constant action")
    prior_action = prior_actions[0]

    if prior_action == 0:
        switch_probability = game.prior_early
        risks = tuple(
            game.prior_early * player.missed_early_cost
            for player in game.players
        )
        old_policy = ALWAYS_LATE
    else:
        switch_probability = 1.0 - game.prior_early
        risks = tuple(
            (1.0 - game.prior_early) * player.false_early_cost
            for player in game.players
        )
        old_policy = ALWAYS_EARLY

    return prior_action, switch_probability, risks, old_policy


def _outside_fraction(
    game: SharedCueGame,
    member: int,
    coalition: set[int],
) -> float:
    n = len(game.players)
    if game.interaction_weights is None:
        if n <= 1:
            return 0.0
        outside = sum(
            1
            for j in range(n)
            if j != member and j not in coalition
        )
        return outside / (n - 1)

    weights = game.interaction_weights[member]
    total = sum(
        weights[j]
        for j in range(n)
        if j != member
    )
    if total <= 0.0:
        return 0.0
    outside = sum(
        weights[j]
        for j in range(n)
        if j != member and j not in coalition
    )
    return outside / total


def coalition_adoption(
    game: SharedCueGame,
    members: Iterable[int],
    *,
    tolerance: float = 1e-12,
) -> CoalitionAdoption:
    """Evaluate simultaneous perfect-information adoption by one coalition."""

    if tolerance < 0.0 or not isfinite(tolerance):
        raise ValueError("tolerance must be non-negative and finite")

    n = len(game.players)
    member_tuple = tuple(sorted(set(int(i) for i in members)))
    if not member_tuple:
        raise ValueError("coalition must contain at least one member")
    if any(i < 0 or i >= n for i in member_tuple):
        raise IndexError("coalition member index out of range")

    _, p, risks, old_policy = _perfect_information_components(game)
    coalition = set(member_tuple)

    fractions = tuple(
        _outside_fraction(game, i, coalition)
        for i in member_tuple
    )
    gains = tuple(
        risks[i]
        - game.players[i].information_cost
        - p * game.players[i].interaction_strength * fraction
        for i, fraction in zip(member_tuple, fractions)
    )

    old_profile = tuple(old_policy for _ in range(n))
    seed_profile = tuple(
        FOLLOW_CUE if i in coalition else old_policy
        for i in range(n)
    )
    old_eval = evaluate_shared_cue_profile(game, old_profile)
    seed_eval = evaluate_shared_cue_profile(game, seed_profile)

    path = sequential_shared_cue_best_response(
        game,
        seed_profile,
        tolerance=tolerance,
    )
    final_profile = path[-1].profile
    fully_informed = tuple(FOLLOW_CUE for _ in range(n))

    return CoalitionAdoption(
        members=member_tuple,
        member_names=tuple(game.players[i].name for i in member_tuple),
        outside_weight_fractions=fractions,
        gains_vs_old=gains,
        weakly_self_financing=all(
            gain >= -tolerance for gain in gains
        ),
        strictly_self_financing=all(
            gain > tolerance for gain in gains
        ),
        joint_gain_vs_old=seed_eval.joint_payoff - old_eval.joint_payoff,
        final_profile_after_best_response=final_profile,
        reaches_fully_informed=(final_profile == fully_informed),
    )


def minimum_self_financing_coalitions(
    game: SharedCueGame,
    *,
    strict: bool = False,
    tolerance: float = 1e-12,
) -> tuple[CoalitionAdoption, ...]:
    """Return all minimum-cardinality self-financing cue-adoption coalitions."""

    n = len(game.players)
    for size in range(1, n + 1):
        rows = []
        for members in combinations(range(n), size):
            result = coalition_adoption(
                game,
                members,
                tolerance=tolerance,
            )
            qualifies = (
                result.strictly_self_financing
                if strict
                else result.weakly_self_financing
            )
            if qualifies:
                rows.append(result)
        if rows:
            return tuple(rows)
    return ()


def minimum_cascading_rescue_coalitions(
    game: SharedCueGame,
    *,
    require_self_financing_seed: bool = True,
    strict_seed: bool = False,
    tolerance: float = 1e-12,
) -> tuple[CoalitionAdoption, ...]:
    """Return smallest coalitions whose seeding reaches all-informed equilibrium."""

    n = len(game.players)
    for size in range(1, n + 1):
        rows = []
        for members in combinations(range(n), size):
            result = coalition_adoption(
                game,
                members,
                tolerance=tolerance,
            )
            if require_self_financing_seed:
                seed_ok = (
                    result.strictly_self_financing
                    if strict_seed
                    else result.weakly_self_financing
                )
                if not seed_ok:
                    continue
            if result.reaches_fully_informed:
                rows.append(result)
        if rows:
            return tuple(rows)
    return ()


def minimum_temporary_subsidies(
    game: SharedCueGame,
    members: Iterable[int],
) -> tuple[float, ...]:
    """Per-member subsidy needed to make simultaneous adoption weakly profitable."""

    result = coalition_adoption(game, members)
    return tuple(max(0.0, -gain) for gain in result.gains_vs_old)


def complete_graph_minimum_coalition_size(
    *,
    n: int,
    prior_risk: float,
    information_cost: float,
    switch_probability: float,
    interaction_strength: float,
) -> CompleteGraphCoalitionThreshold:
    """Closed-form minimum self-financing coalition size for homogeneous K_N.

    For a coalition of size k in an unweighted complete graph,

        G(k) = R - D - p I (N-k)/(N-1).

    Weak adoption requires G(k) >= 0; strict adoption requires G(k) > 0.
    """

    if n < 2:
        raise ValueError("n must be at least 2")
    r = float(prior_risk)
    d = float(information_cost)
    p = float(switch_probability)
    interaction = float(interaction_strength)
    for name, value in (
        ("prior_risk", r),
        ("information_cost", d),
        ("switch_probability", p),
        ("interaction_strength", interaction),
    ):
        if not isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be non-negative and finite")
    if not 0.0 < p <= 1.0:
        raise ValueError("switch_probability must lie in (0,1]")

    first_gain = r - d - p * interaction
    full_gain = r - d

    if d > r:
        weak = None
        strict = None
    elif interaction == 0.0:
        weak = 1
        strict = 1 if r > d else None
    else:
        scale = p * interaction
        threshold = n - (n - 1) * (r - d) / scale

        # Weak: smallest integer k >= threshold.
        weak_candidate = max(1, ceil(threshold - 1e-12))
        weak = weak_candidate if weak_candidate <= n else None

        # Strict: smallest integer k > threshold.
        strict_candidate = max(1, floor(threshold + 1e-12) + 1)
        strict = strict_candidate if strict_candidate <= n else None

    return CompleteGraphCoalitionThreshold(
        n=n,
        prior_risk=r,
        information_cost=d,
        switch_probability=p,
        interaction_strength=interaction,
        individual_first_move_gain=first_gain,
        full_coalition_gain_per_actor=full_gain,
        weak_minimum_size=weak,
        strict_minimum_size=strict,
    )
