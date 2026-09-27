"""Network consequences of asynchronous seasonal information uptake.

Actors share the same future cue but differ in opportunity costs of waiting for
it.  The information-deadline theorem determines which actors use the cue at a
given reliability.  This module maps those individual thresholds onto an
interaction network.

The central object is the weighted cut between informed and uninformed actors.
When the cue-contingent action differs from the prior convention, only edges
crossing that cut are temporally mismatched.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Sequence

from src.endogenous_information_timing import (
    closed_form_mismatch_probability_during_asynchrony,
    information_value,
)


@dataclass(frozen=True)
class NetworkUptakeState:
    cue_accuracy: float
    information_value: float
    informed: tuple[bool, ...]
    informed_count: int
    informed_fraction: float
    weighted_cut: float
    total_edge_weight: float
    cut_fraction: float
    conditional_action_mismatch_probability: float
    expected_edge_mismatch_fraction: float


def _validate_delays(delays: Iterable[float]) -> tuple[float, ...]:
    values = tuple(float(value) for value in delays)
    if len(values) < 2:
        raise ValueError("at least two actors are required")
    if any(not isfinite(value) or value < 0.0 for value in values):
        raise ValueError("delay costs must be non-negative and finite")
    return values


def _validate_symmetric_weights(
    weights: Sequence[Sequence[float]],
    n: int,
    *,
    tolerance: float = 1e-12,
) -> tuple[tuple[float, ...], ...]:
    if len(weights) != n:
        raise ValueError("weights must have one row per actor")
    rows = tuple(tuple(float(value) for value in row) for row in weights)
    if any(len(row) != n for row in rows):
        raise ValueError("weights must be square")
    for i in range(n):
        for j in range(n):
            value = rows[i][j]
            if not isfinite(value) or value < 0.0:
                raise ValueError("edge weights must be non-negative and finite")
            if i == j and abs(value) > tolerance:
                raise ValueError("weight diagonal must be zero")
            if abs(value - rows[j][i]) > tolerance:
                raise ValueError("weights must be symmetric")
    if sum(rows[i][j] for i in range(n) for j in range(i + 1, n)) <= 0.0:
        raise ValueError("network must contain positive edge weight")
    return rows


def complete_graph_weights(n: int) -> tuple[tuple[float, ...], ...]:
    if n < 2:
        raise ValueError("n must be at least 2")
    return tuple(
        tuple(0.0 if i == j else 1.0 for j in range(n))
        for i in range(n)
    )


def informed_mask(
    delay_costs: Iterable[float],
    *,
    information_value_amount: float,
) -> tuple[bool, ...]:
    """Actors use the cue only when its value strictly exceeds their delay cost."""

    delays = _validate_delays(delay_costs)
    value = float(information_value_amount)
    if not isfinite(value) or value < 0.0:
        raise ValueError("information value must be non-negative and finite")
    return tuple(value > delay for delay in delays)


def weighted_information_cut(
    informed: Sequence[bool],
    weights: Sequence[Sequence[float]],
) -> tuple[float, float, float]:
    """Return cut weight, total undirected edge weight, and cut fraction."""

    mask = tuple(bool(value) for value in informed)
    n = len(mask)
    if n < 2:
        raise ValueError("at least two actors are required")
    rows = _validate_symmetric_weights(weights, n)

    cut = 0.0
    total = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            weight = rows[i][j]
            total += weight
            if mask[i] != mask[j]:
                cut += weight
    return cut, total, cut / total


def complete_graph_cut_fraction(n: int, informed_count: int) -> float:
    """Exact fraction of undirected complete-graph edges crossing uptake states."""

    if n < 2:
        raise ValueError("n must be at least 2")
    k = int(informed_count)
    if not 0 <= k <= n:
        raise ValueError("informed_count must lie in [0,n]")
    cut_edges = k * (n - k)
    total_edges = n * (n - 1) / 2.0
    return cut_edges / total_edges


def complete_graph_maximum_cut_fraction(n: int) -> float:
    """Maximum asynchronous-uptake edge fraction, attained at half adoption."""

    if n < 2:
        raise ValueError("n must be at least 2")
    k = n // 2
    return complete_graph_cut_fraction(n, k)


def random_mixing_asynchronous_pair_fraction(
    informed_fraction: float,
) -> float:
    """Large-population / with-replacement asynchronous pair probability."""

    f = float(informed_fraction)
    if not isfinite(f) or not 0.0 <= f <= 1.0:
        raise ValueError("informed_fraction must lie in [0,1]")
    return 2.0 * f * (1.0 - f)


def adoption_cut_change(
    actor_index: int,
    informed_before: Sequence[bool],
    weights: Sequence[Sequence[float]],
) -> float:
    """Exact change in weighted informed/uninformed cut when one actor adopts.

    If actor i is currently uninformed, adoption changes the cut by

        weight(i, still-uninformed neighbours)
        - weight(i, already-informed neighbours).

    Positive values worsen network desynchronization; negative values repair it.
    """

    mask = list(bool(value) for value in informed_before)
    n = len(mask)
    if not 0 <= actor_index < n:
        raise IndexError("actor_index out of range")
    if mask[actor_index]:
        raise ValueError("actor must be uninformed before adoption")
    rows = _validate_symmetric_weights(weights, n)

    to_uninformed = 0.0
    to_informed = 0.0
    for j in range(n):
        if j == actor_index:
            continue
        if mask[j]:
            to_informed += rows[actor_index][j]
        else:
            to_uninformed += rows[actor_index][j]
    return to_uninformed - to_informed


def evaluate_network_uptake(
    *,
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    cue_accuracy: float,
    delay_costs: Iterable[float],
    weights: Sequence[Sequence[float]],
) -> NetworkUptakeState:
    """Evaluate network mismatch generated solely by asynchronous cue uptake."""

    delays = _validate_delays(delay_costs)
    q = float(cue_accuracy)
    value = information_value(
        prior_early,
        q,
        false_early_cost,
        missed_early_cost,
    )
    mask = informed_mask(
        delays,
        information_value_amount=value,
    )
    cut, total, cut_fraction = weighted_information_cut(mask, weights)
    conditional_mismatch = (
        closed_form_mismatch_probability_during_asynchrony(
            prior_early,
            false_early_cost,
            missed_early_cost,
            cue_accuracy=q,
        )
        if 0 < sum(mask) < len(mask)
        else 0.0
    )
    return NetworkUptakeState(
        cue_accuracy=q,
        information_value=value,
        informed=mask,
        informed_count=sum(mask),
        informed_fraction=sum(mask) / len(mask),
        weighted_cut=cut,
        total_edge_weight=total,
        cut_fraction=cut_fraction,
        conditional_action_mismatch_probability=conditional_mismatch,
        expected_edge_mismatch_fraction=(
            cut_fraction * conditional_mismatch
        ),
    )
