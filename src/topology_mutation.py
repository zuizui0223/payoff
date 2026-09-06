"""Rare-mutation substitution chain on discrete PAYOFF topologies."""

from __future__ import annotations

from heapq import heappop, heappush
from math import exp, log
from typing import Dict, Mapping, Sequence, Tuple

from src.topology_game import (
    Topology,
    pairwise_payoff_parameters,
    topology_distance,
    validate_topology,
)
from src.finite_population import moran_fixation_probability_d


def single_edge_neighbors(topology: Sequence[int]) -> Tuple[Topology, ...]:
    """Return all Hamming-distance-one binary topology neighbors."""

    state = validate_topology(topology)
    neighbors = []
    for index in range(len(state)):
        flipped = list(state)
        flipped[index] = 1 - flipped[index]
        neighbors.append(tuple(flipped))
    return tuple(neighbors)


def single_edge_mutation_graph(topologies: Sequence[Sequence[int]]) -> Dict[Topology, Tuple[Topology, ...]]:
    """Return induced single-edge mutation graph on supplied topology states."""

    states = tuple(validate_topology(state) for state in topologies)
    if len(set(states)) != len(states):
        raise ValueError("topologies must be unique")
    if not states:
        raise ValueError("topologies cannot be empty")
    lengths = {len(state) for state in states}
    if len(lengths) != 1:
        raise ValueError("all topologies must have equal length")
    state_set = set(states)
    return {
        state: tuple(neighbor for neighbor in single_edge_neighbors(state) if neighbor in state_set)
        for state in states
    }


def topology_substitution_rate(
    source: Sequence[int],
    target: Sequence[int],
    intrinsic_payoffs: Mapping[Topology, float],
    mutation_rate: float,
    n: int,
    beta: float,
    gamma: float,
    edge_weights: Sequence[float] | None = None,
) -> float:
    """Return mu_ST * rho(T|S) under exact pairwise Moran mapping."""

    s = validate_topology(source)
    t = validate_topology(target)
    if s == t:
        return 0.0
    if mutation_rate < 0.0:
        raise ValueError("mutation_rate must be non-negative")
    if s not in intrinsic_payoffs or t not in intrinsic_payoffs:
        raise ValueError("intrinsic payoff missing for source or target")
    phi, eta = pairwise_payoff_parameters(
        intrinsic_payoffs[s], intrinsic_payoffs[t], s, t, gamma, edge_weights
    )
    fixation = moran_fixation_probability_d(n, phi, eta, beta)
    return mutation_rate * fixation


def symmetric_single_edge_generator(
    intrinsic_payoffs: Mapping[Topology, float],
    mutation_rate: float,
    n: int,
    beta: float,
    gamma: float,
    edge_weights: Sequence[float] | None = None,
) -> Tuple[Tuple[Topology, ...], Tuple[Tuple[float, ...], ...]]:
    """Return CTMC generator for symmetric single-edge mutation among supplied states."""

    if mutation_rate <= 0.0:
        raise ValueError("mutation_rate must be positive")
    states = tuple(intrinsic_payoffs)
    graph = single_edge_mutation_graph(states)
    _require_connected(graph)
    matrix = [[0.0] * len(states) for _ in states]
    index = {state: i for i, state in enumerate(states)}
    for s in states:
        i = index[s]
        outgoing = 0.0
        for t in graph[s]:
            j = index[t]
            rate = topology_substitution_rate(
                s,
                t,
                intrinsic_payoffs,
                mutation_rate,
                n,
                beta,
                gamma,
                edge_weights,
            )
            matrix[i][j] = rate
            outgoing += rate
        matrix[i][i] = -outgoing
    return states, tuple(tuple(row) for row in matrix)


def symmetric_mutation_stationary_distribution(
    intrinsic_payoffs: Mapping[Topology, float],
    n: int,
    beta: float,
) -> Dict[Topology, float]:
    """Return exact rare-mutation stationary Pi_s ∝ exp[beta(N-2)b_s]."""

    if n < 2:
        raise ValueError("n must be at least 2")
    if beta < 0.0:
        raise ValueError("beta must be non-negative")
    if not intrinsic_payoffs:
        raise ValueError("intrinsic_payoffs cannot be empty")
    scale = beta * (n - 2)
    logs = {state: scale * payoff for state, payoff in intrinsic_payoffs.items()}
    maximum = max(logs.values())
    weights = {state: exp(value - maximum) for state, value in logs.items()}
    total = sum(weights.values())
    return {state: weight / total for state, weight in weights.items()}


def detailed_balance_max_residual(
    states: Sequence[Topology],
    generator: Sequence[Sequence[float]],
    stationary: Mapping[Topology, float],
) -> float:
    """Return max |Pi_i Q_ij-Pi_j Q_ji| over distinct state pairs."""

    if len(states) != len(generator) or any(len(row) != len(states) for row in generator):
        raise ValueError("generator shape must match states")
    maximum = 0.0
    for i, s in enumerate(states):
        for j in range(i + 1, len(states)):
            t = states[j]
            residual = abs(
                stationary[s] * generator[i][j]
                - stationary[t] * generator[j][i]
            )
            maximum = max(maximum, residual)
    return maximum


def is_single_edge_local_optimum(
    topology: Sequence[int], intrinsic_payoffs: Mapping[Topology, float], tol: float = 1e-12
) -> bool:
    """Return whether no supplied one-edge neighbor has higher intrinsic payoff."""

    state = validate_topology(topology)
    if state not in intrinsic_payoffs:
        raise ValueError("topology missing from intrinsic_payoffs")
    value = intrinsic_payoffs[state]
    for neighbor in single_edge_neighbors(state):
        if neighbor in intrinsic_payoffs and intrinsic_payoffs[neighbor] > value + tol:
            return False
    return True


def best_bottleneck_payoff(
    source: Sequence[int],
    target: Sequence[int],
    intrinsic_payoffs: Mapping[Topology, float],
) -> float:
    """Return max over single-edge paths of the minimum intrinsic payoff on path.

    This is the widest-path problem with node capacities equal to intrinsic payoff.
    """

    s = validate_topology(source)
    t = validate_topology(target)
    if s not in intrinsic_payoffs or t not in intrinsic_payoffs:
        raise ValueError("source and target must be present")
    graph = single_edge_mutation_graph(tuple(intrinsic_payoffs))
    _require_connected(graph)

    capacity: Dict[Topology, float] = {state: float("-inf") for state in graph}
    capacity[s] = intrinsic_payoffs[s]
    heap = [(-capacity[s], s)]
    visited = set()
    while heap:
        negative_cap, state = heappop(heap)
        current = -negative_cap
        if state in visited:
            continue
        visited.add(state)
        if state == t:
            return current
        for neighbor in graph[state]:
            candidate = min(current, intrinsic_payoffs[neighbor])
            if candidate > capacity[neighbor]:
                capacity[neighbor] = candidate
                heappush(heap, (-candidate, neighbor))
    raise ValueError("target is unreachable from source")


def intrinsic_valley_depth(
    source: Sequence[int],
    target: Sequence[int],
    intrinsic_payoffs: Mapping[Topology, float],
) -> float:
    """Return B=max(0,b_source-best_path_bottleneck)."""

    s = validate_topology(source)
    bottleneck = best_bottleneck_payoff(s, target, intrinsic_payoffs)
    return max(0.0, intrinsic_payoffs[s] - bottleneck)


def transition_resistance(rate: float) -> float:
    """Return -log(rate) as a kinetic edge diagnostic."""

    if rate <= 0.0:
        return float("inf")
    return -log(rate)


def _require_connected(graph: Mapping[Topology, Sequence[Topology]]) -> None:
    if not graph:
        raise ValueError("mutation graph cannot be empty")
    start = next(iter(graph))
    seen = {start}
    stack = [start]
    while stack:
        state = stack.pop()
        for neighbor in graph[state]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    if len(seen) != len(graph):
        raise ValueError("supplied topology mutation graph must be connected")
