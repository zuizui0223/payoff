"""Hidden-state coordination game for climate-tracking decisions.

This module formalizes a partial-information version of PAYOFF-B.

Species choose whether to advance a seasonal action (1) or retain the baseline
timing (0) before the shared environmental state is fully revealed. Each
species receives a private binary cue with species-specific accuracy. Payoff
combines abiotic mismatch, mismatch with interaction partners, and an
asymmetric cost of advancing.

The model is intentionally minimal and dependency-free. It separates:

1. a state-contingent coordinated optimum under perfect information;
2. full-information decentralized Nash equilibria;
3. pure Bayesian Nash equilibria under heterogeneous cue reliability.

That decomposition allows a clean "information-only trap": a viable
state-contingent solution exists and is a full-information equilibrium, yet
partial information makes a different policy rational before the state is
known.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import isfinite
from typing import Literal


Action = Literal[0, 1]
Signal = Literal[0, 1]
Policy = tuple[Action, Action]

ALWAYS_BASELINE: Policy = (0, 0)
FOLLOW_CUE: Policy = (0, 1)
REVERSE_CUE: Policy = (1, 0)
ALWAYS_ADVANCE: Policy = (1, 1)
PURE_POLICIES: tuple[Policy, ...] = (
    ALWAYS_BASELINE,
    FOLLOW_CUE,
    REVERSE_CUE,
    ALWAYS_ADVANCE,
)


@dataclass(frozen=True)
class SpeciesCueParameters:
    """Payoff and information parameters for one interacting species.

    `cue_accuracy` is P(signal == environmental_state), constrained to [0.5,1].
    State 0 denotes the baseline/normal seasonal state and state 1 an advanced
    seasonal state.

    Realized low-density growth is

        baseline_growth
        - abiotic_mismatch_cost * 1[action != state]
        - interaction_mismatch_cost * partner_mismatch_fraction
        - advance_cost * action.

    Interaction mismatch is averaged across the other species, keeping the
    interaction term comparable as network size changes.
    """

    name: str
    cue_accuracy: float
    baseline_growth: float
    abiotic_mismatch_cost: float
    interaction_mismatch_cost: float
    advance_cost: float = 0.0

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("species name must be non-empty")
        if (
            not isfinite(self.cue_accuracy)
            or not 0.5 <= self.cue_accuracy <= 1.0
        ):
            raise ValueError("cue_accuracy must lie in [0.5,1]")
        for name in (
            "baseline_growth",
            "abiotic_mismatch_cost",
            "interaction_mismatch_cost",
            "advance_cost",
        ):
            value = float(getattr(self, name))
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
        for name in (
            "abiotic_mismatch_cost",
            "interaction_mismatch_cost",
            "advance_cost",
        ):
            if getattr(self, name) < 0.0:
                raise ValueError(f"{name} must be non-negative")


@dataclass(frozen=True)
class HiddenStateGame:
    """Binary hidden-state coordination game with heterogeneous private cues."""

    species: tuple[SpeciesCueParameters, ...]
    prior_advanced: float = 0.5

    def __post_init__(self) -> None:
        if len(self.species) < 2:
            raise ValueError("at least two interacting species are required")
        if (
            not isfinite(self.prior_advanced)
            or not 0.0 < self.prior_advanced < 1.0
        ):
            raise ValueError("prior_advanced must lie strictly in (0,1)")


@dataclass(frozen=True)
class BayesianEquilibrium:
    policies: tuple[Policy, ...]
    expected_growths: tuple[float, ...]

    @property
    def mean_expected_growth(self) -> float:
        return sum(self.expected_growths) / len(self.expected_growths)


@dataclass(frozen=True)
class InformationDeficitDiagnostic:
    oracle_expected_mean_growth: float
    full_information_equilibrium_expected_mean_growth: float
    partial_information_equilibrium_expected_mean_growth: float
    coordination_deficit: float
    information_deficit: float
    total_deficit: float
    partial_equilibria: tuple[BayesianEquilibrium, ...]
    selected_partial_equilibrium: BayesianEquilibrium

    @property
    def information_only_trap(self) -> bool:
        return (
            abs(self.coordination_deficit) <= 1e-10
            and self.information_deficit > 1e-10
        )


@dataclass(frozen=True)
class FocalInformationThreshold:
    species_name: str
    critical_posterior_advanced: float | None
    critical_positive_cue_accuracy: float | None
    posterior_after_baseline_cue: float
    posterior_after_advanced_cue: float
    best_response_policy: Policy
    advances_after_positive_cue: bool


def signal_probability(
    signal: Signal,
    state: Action,
    cue_accuracy: float,
) -> float:
    if signal not in (0, 1) or state not in (0, 1):
        raise ValueError("signal and state must be binary")
    if not isfinite(cue_accuracy) or not 0.5 <= cue_accuracy <= 1.0:
        raise ValueError("cue_accuracy must lie in [0.5,1]")
    return cue_accuracy if signal == state else 1.0 - cue_accuracy


def posterior_advanced(
    prior_advanced: float,
    cue_accuracy: float,
    signal: Signal,
) -> float:
    """Posterior P(state=1 | private signal) under a symmetric binary cue."""

    if not isfinite(prior_advanced) or not 0.0 < prior_advanced < 1.0:
        raise ValueError("prior_advanced must lie strictly in (0,1)")
    if not isfinite(cue_accuracy) or not 0.5 <= cue_accuracy <= 1.0:
        raise ValueError("cue_accuracy must lie in [0.5,1]")
    if signal not in (0, 1):
        raise ValueError("signal must be binary")

    likelihood_advanced = (
        cue_accuracy if signal == 1 else 1.0 - cue_accuracy
    )
    likelihood_baseline = (
        1.0 - cue_accuracy if signal == 1 else cue_accuracy
    )
    numerator = prior_advanced * likelihood_advanced
    denominator = numerator + (1.0 - prior_advanced) * likelihood_baseline
    if denominator <= 0.0:
        raise ValueError(
            "posterior is undefined for a zero-probability signal"
        )
    return numerator / denominator


def realized_growths(
    game: HiddenStateGame,
    state: Action,
    actions: tuple[Action, ...],
) -> tuple[float, ...]:
    """Realized low-density growth after the true environmental state is known."""

    if state not in (0, 1):
        raise ValueError("state must be binary")
    if len(actions) != len(game.species):
        raise ValueError("one action is required for each species")
    if any(action not in (0, 1) for action in actions):
        raise ValueError("actions must be binary")

    n = len(game.species)
    growths: list[float] = []
    for i, params in enumerate(game.species):
        mismatched_partners = sum(
            actions[j] != actions[i]
            for j in range(n)
            if j != i
        )
        partner_mismatch_fraction = mismatched_partners / (n - 1)
        growths.append(
            params.baseline_growth
            - params.abiotic_mismatch_cost * (actions[i] != state)
            - params.interaction_mismatch_cost
            * partner_mismatch_fraction
            - params.advance_cost * actions[i]
        )
    return tuple(growths)


def expected_growths(
    game: HiddenStateGame,
    policies: tuple[Policy, ...],
) -> tuple[float, ...]:
    """Ex-ante expected growth under a profile of signal-contingent policies."""

    if len(policies) != len(game.species):
        raise ValueError("one policy is required for each species")
    if any(policy not in PURE_POLICIES for policy in policies):
        raise ValueError("policies must be binary pure policies")

    n = len(game.species)
    totals = [0.0] * n
    for state in (0, 1):
        state_probability = (
            game.prior_advanced
            if state == 1
            else 1.0 - game.prior_advanced
        )
        for signals in product((0, 1), repeat=n):
            probability = state_probability
            for index, signal in enumerate(signals):
                probability *= signal_probability(
                    signal,
                    state,
                    game.species[index].cue_accuracy,
                )
            if probability <= 0.0:
                continue
            actions = tuple(
                policies[index][signals[index]]
                for index in range(n)
            )
            growth = realized_growths(game, state, actions)
            for index in range(n):
                totals[index] += probability * growth[index]
    return tuple(totals)


def pure_bayesian_nash_equilibria(
    game: HiddenStateGame,
    *,
    tolerance: float = 1e-12,
) -> tuple[BayesianEquilibrium, ...]:
    """Enumerate all pure-strategy Bayesian Nash equilibria.

    A pure strategy is a complete mapping from private signal {0,1} to action
    {0,1}. This is exact for the finite game and intentionally does not impose
    an equilibrium-selection rule.
    """

    if tolerance < 0.0 or not isfinite(tolerance):
        raise ValueError("tolerance must be non-negative and finite")

    n = len(game.species)
    equilibria: list[BayesianEquilibrium] = []
    for profile in product(PURE_POLICIES, repeat=n):
        profile_tuple = tuple(profile)
        current = expected_growths(game, profile_tuple)
        is_equilibrium = True
        for focal in range(n):
            for alternative in PURE_POLICIES:
                if alternative == profile_tuple[focal]:
                    continue
                deviated = list(profile_tuple)
                deviated[focal] = alternative
                alternative_growth = expected_growths(
                    game,
                    tuple(deviated),
                )[focal]
                if alternative_growth > current[focal] + tolerance:
                    is_equilibrium = False
                    break
            if not is_equilibrium:
                break
        if is_equilibrium:
            equilibria.append(
                BayesianEquilibrium(
                    policies=profile_tuple,
                    expected_growths=current,
                )
            )
    return tuple(equilibria)


def _mean(values: tuple[float, ...]) -> float:
    return sum(values) / len(values)


def oracle_action_profile(
    game: HiddenStateGame,
    state: Action,
) -> tuple[Action, ...]:
    """Joint-payoff maximizing action profile after observing the true state."""

    n = len(game.species)
    best_actions: tuple[Action, ...] | None = None
    best_value = float("-inf")
    for actions in product((0, 1), repeat=n):
        actions_tuple = tuple(actions)
        value = _mean(realized_growths(game, state, actions_tuple))
        if value > best_value + 1e-12:
            best_value = value
            best_actions = actions_tuple
        elif abs(value - best_value) <= 1e-12:
            assert best_actions is not None
            if sum(actions_tuple) < sum(best_actions):
                best_actions = actions_tuple
    assert best_actions is not None
    return best_actions


def full_information_nash_equilibria(
    game: HiddenStateGame,
    state: Action,
    *,
    tolerance: float = 1e-12,
) -> tuple[tuple[Action, ...], ...]:
    """Pure Nash equilibria when every species observes the true state."""

    if tolerance < 0.0 or not isfinite(tolerance):
        raise ValueError("tolerance must be non-negative and finite")

    n = len(game.species)
    equilibria: list[tuple[Action, ...]] = []
    for actions in product((0, 1), repeat=n):
        actions_tuple = tuple(actions)
        current = realized_growths(game, state, actions_tuple)
        is_equilibrium = True
        for focal in range(n):
            deviated = list(actions_tuple)
            deviated[focal] = 1 - deviated[focal]
            alternative = realized_growths(
                game,
                state,
                tuple(deviated),
            )[focal]
            if alternative > current[focal] + tolerance:
                is_equilibrium = False
                break
        if is_equilibrium:
            equilibria.append(actions_tuple)
    return tuple(equilibria)


def _best_full_information_equilibrium_value(
    game: HiddenStateGame,
    state: Action,
) -> float:
    equilibria = full_information_nash_equilibria(game, state)
    if not equilibria:
        raise RuntimeError(
            "finite binary game has no pure full-information equilibrium"
        )
    return max(
        _mean(realized_growths(game, state, actions))
        for actions in equilibria
    )


def information_deficit_diagnostic(
    game: HiddenStateGame,
) -> InformationDeficitDiagnostic:
    """Separate full-information coordination loss from information loss.

    Values use mean low-density growth across species.

    oracle:
        state is known and actions are coordinated to maximize joint growth.

    full-information equilibrium:
        state is known but species choose individually; the highest-welfare
        pure Nash equilibrium is used to avoid injecting an equilibrium
        selection penalty into the information term.

    partial-information equilibrium:
        species act on private cues; the highest-welfare pure Bayesian Nash
        equilibrium is used for the same reason.

    The resulting information deficit is conservative: it asks whether
    information loss persists even under favorable equilibrium selection.
    """

    prior = game.prior_advanced
    oracle_values = {}
    full_eq_values = {}
    for state in (0, 1):
        oracle_actions = oracle_action_profile(game, state)
        oracle_values[state] = _mean(
            realized_growths(game, state, oracle_actions)
        )
        full_eq_values[state] = _best_full_information_equilibrium_value(
            game,
            state,
        )

    oracle_expected = (
        (1.0 - prior) * oracle_values[0]
        + prior * oracle_values[1]
    )
    full_info_expected = (
        (1.0 - prior) * full_eq_values[0]
        + prior * full_eq_values[1]
    )

    partial = pure_bayesian_nash_equilibria(game)
    if not partial:
        raise RuntimeError(
            "no pure Bayesian Nash equilibrium; mixed-strategy analysis required"
        )
    selected = max(
        partial,
        key=lambda row: row.mean_expected_growth,
    )
    partial_value = selected.mean_expected_growth

    return InformationDeficitDiagnostic(
        oracle_expected_mean_growth=oracle_expected,
        full_information_equilibrium_expected_mean_growth=full_info_expected,
        partial_information_equilibrium_expected_mean_growth=partial_value,
        coordination_deficit=oracle_expected - full_info_expected,
        information_deficit=full_info_expected - partial_value,
        total_deficit=oracle_expected - partial_value,
        partial_equilibria=partial,
        selected_partial_equilibrium=selected,
    )


def critical_posterior_against_state_followers(
    species: SpeciesCueParameters,
) -> float | None:
    """Posterior threshold for advancing when all partners follow true state.

    If every partner uses action == state, advancing rather than retaining the
    baseline timing has conditional expected-growth difference

        (2q - 1) * (A + I) - C,

    where q=P(state=advanced | cue), A is abiotic mismatch cost, I is the
    interaction mismatch cost, and C is the advance cost.

    Hence advancing is optimal when

        q > 0.5 * [1 + C/(A+I)].

    None means advancing is never strictly optimal, even with perfect
    information, because the advance cost is at least the total mismatch cost.
    """

    mismatch_cost = (
        species.abiotic_mismatch_cost
        + species.interaction_mismatch_cost
    )
    if mismatch_cost <= 0.0:
        return None
    threshold = 0.5 * (
        1.0 + species.advance_cost / mismatch_cost
    )
    if threshold >= 1.0:
        return None
    return threshold


def critical_positive_cue_accuracy(
    prior_advanced: float,
    species: SpeciesCueParameters,
) -> float | None:
    """Cue accuracy needed for a positive cue to cross the advance threshold."""

    threshold = critical_posterior_against_state_followers(species)
    if threshold is None:
        return None
    if not isfinite(prior_advanced) or not 0.0 < prior_advanced < 1.0:
        raise ValueError("prior_advanced must lie strictly in (0,1)")

    denominator = (
        prior_advanced * (1.0 - threshold)
        + threshold * (1.0 - prior_advanced)
    )
    if denominator <= 0.0:
        return None
    accuracy = (
        threshold * (1.0 - prior_advanced) / denominator
    )
    return min(1.0, max(0.5, accuracy))


def focal_threshold_diagnostic(
    game: HiddenStateGame,
    focal_index: int,
) -> FocalInformationThreshold:
    """Exact focal best response if all other species observe and follow state."""

    if not 0 <= focal_index < len(game.species):
        raise IndexError("focal_index out of range")
    species = game.species[focal_index]
    threshold = critical_posterior_against_state_followers(species)
    q0 = posterior_advanced(
        game.prior_advanced,
        species.cue_accuracy,
        0,
    )
    q1 = posterior_advanced(
        game.prior_advanced,
        species.cue_accuracy,
        1,
    )

    def best_action(q: float) -> Action:
        if threshold is None:
            return 0
        return 1 if q > threshold else 0

    policy: Policy = (best_action(q0), best_action(q1))
    return FocalInformationThreshold(
        species_name=species.name,
        critical_posterior_advanced=threshold,
        critical_positive_cue_accuracy=critical_positive_cue_accuracy(
            game.prior_advanced,
            species,
        ),
        posterior_after_baseline_cue=q0,
        posterior_after_advanced_cue=q1,
        best_response_policy=policy,
        advances_after_positive_cue=(policy[1] == 1),
    )
