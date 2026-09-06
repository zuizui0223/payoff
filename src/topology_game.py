"""Population game among discrete modular coupling topologies.

A topology is a binary edge-release vector. Intrinsic payoff b_s is supplied by
edgewise phenotype optimization. Pairwise feedback uses weighted Hamming
feature distance q(s,t), producing an exact canonical PAYOFF pair with
    phi=b_t-b_s,
    eta=gamma*q(s,t).
"""

from __future__ import annotations

from typing import Dict, Mapping, Sequence, Tuple

from src.finite_population import (
    moran_fixation_probability_d,
    moran_fixation_probability_s,
)

Topology = Tuple[int, ...]


def validate_topology(topology: Sequence[int]) -> Topology:
    """Return a normalized binary topology tuple."""

    if not topology:
        raise ValueError("topology cannot be empty")
    result = tuple(int(value) for value in topology)
    if any(value not in (0, 1) for value in result):
        raise ValueError("topology entries must be 0 or 1")
    return result


def topology_distance(
    topology_a: Sequence[int],
    topology_b: Sequence[int],
    edge_weights: Sequence[float] | None = None,
) -> float:
    """Return weighted squared feature distance / weighted Hamming distance."""

    a = validate_topology(topology_a)
    b = validate_topology(topology_b)
    if len(a) != len(b):
        raise ValueError("topologies must have equal length")
    if edge_weights is None:
        weights = [1.0] * len(a)
    else:
        if len(edge_weights) != len(a):
            raise ValueError("one edge weight is required per topology coordinate")
        if any(weight <= 0.0 for weight in edge_weights):
            raise ValueError("edge weights must be positive")
        weights = edge_weights
    return sum(
        weight * (left - right) ** 2
        for left, right, weight in zip(a, b, weights)
    )


def pairwise_payoff_parameters(
    resident_payoff: float,
    mutant_payoff: float,
    resident_topology: Sequence[int],
    mutant_topology: Sequence[int],
    gamma: float,
    edge_weights: Sequence[float] | None = None,
) -> Tuple[float, float]:
    """Return exact canonical pair parameters (phi,eta)."""

    q = topology_distance(resident_topology, mutant_topology, edge_weights)
    return mutant_payoff - resident_payoff, gamma * q


def pairwise_payoff_gap(
    mutant_frequency: float,
    resident_payoff: float,
    mutant_payoff: float,
    resident_topology: Sequence[int],
    mutant_topology: Sequence[int],
    gamma: float,
    edge_weights: Sequence[float] | None = None,
) -> float:
    """Return pi_mutant-pi_resident at mutant frequency p."""

    if not 0.0 <= mutant_frequency <= 1.0:
        raise ValueError("mutant_frequency must lie in [0,1]")
    phi, eta = pairwise_payoff_parameters(
        resident_payoff,
        mutant_payoff,
        resident_topology,
        mutant_topology,
        gamma,
        edge_weights,
    )
    return phi + eta * (2.0 * mutant_frequency - 1.0)


def reciprocal_invasion_margins(
    payoff_s: float,
    payoff_t: float,
    topology_s: Sequence[int],
    topology_t: Sequence[int],
    gamma: float,
    edge_weights: Sequence[float] | None = None,
) -> Tuple[float, float]:
    """Return (T_into_S, S_into_T) deterministic rare-invasion margins."""

    phi, eta = pairwise_payoff_parameters(
        payoff_s, payoff_t, topology_s, topology_t, gamma, edge_weights
    )
    return phi - eta, -phi - eta


def classify_pairwise_topology_game(
    payoff_s: float,
    payoff_t: float,
    topology_s: Sequence[int],
    topology_t: Sequence[int],
    gamma: float,
    edge_weights: Sequence[float] | None = None,
    tol: float = 1e-12,
) -> str:
    """Classify pairwise topology dominance/coexistence/coordination."""

    t_margin, s_margin = reciprocal_invasion_margins(
        payoff_s, payoff_t, topology_s, topology_t, gamma, edge_weights
    )
    t_invades = t_margin > tol
    s_invades = s_margin > tol
    if t_invades and s_invades:
        return "stable_pairwise_coexistence"
    if t_invades:
        return "t_dominance"
    if s_invades:
        return "s_dominance"
    if abs(t_margin) <= tol or abs(s_margin) <= tol:
        return "boundary"
    return "coordination_bistability"


def normalized_intrinsic_slope(
    payoff_s: float,
    payoff_t: float,
    topology_s: Sequence[int],
    topology_t: Sequence[int],
    edge_weights: Sequence[float] | None = None,
) -> float:
    """Return |b_t-b_s| / q(s,t), requiring distinct topologies."""

    q = topology_distance(topology_s, topology_t, edge_weights)
    if q <= 0.0:
        raise ValueError("distinct topology distance must be positive")
    return abs(payoff_t - payoff_s) / q


def reciprocal_fixation_probabilities(
    n: int,
    beta: float,
    payoff_s: float,
    payoff_t: float,
    topology_s: Sequence[int],
    topology_t: Sequence[int],
    gamma: float,
    edge_weights: Sequence[float] | None = None,
) -> Tuple[float, float]:
    """Return (rho_T_into_S,rho_S_into_T) under exact Moran mapping."""

    phi, eta = pairwise_payoff_parameters(
        payoff_s, payoff_t, topology_s, topology_t, gamma, edge_weights
    )
    return (
        moran_fixation_probability_d(n, phi, eta, beta),
        moran_fixation_probability_s(n, phi, eta, beta),
    )


def mean_topology_game_payoff(
    intrinsic_payoffs: Mapping[Topology, float],
    frequencies: Mapping[Topology, float],
    gamma: float,
    edge_weights: Sequence[float] | None = None,
) -> float:
    """Return V=E[b_s+b_t-gamma*q(s,t)] for a topology distribution."""

    _validate_distribution(intrinsic_payoffs, frequencies)
    topologies = list(frequencies)
    total = 0.0
    for s in topologies:
        for t in topologies:
            total += frequencies[s] * frequencies[t] * (
                intrinsic_payoffs[s]
                + intrinsic_payoffs[t]
                - gamma * topology_distance(s, t, edge_weights)
            )
    return total


def topology_marginal_release_frequencies(
    frequencies: Mapping[Topology, float],
) -> Tuple[float, ...]:
    """Return edgewise marginal release frequencies m_e."""

    if not frequencies:
        raise ValueError("frequencies cannot be empty")
    normalized = {validate_topology(topology): freq for topology, freq in frequencies.items()}
    lengths = {len(topology) for topology in normalized}
    if len(lengths) != 1:
        raise ValueError("all topologies must have equal length")
    if any(freq < 0.0 for freq in normalized.values()):
        raise ValueError("frequencies must be non-negative")
    if abs(sum(normalized.values()) - 1.0) > 1e-10:
        raise ValueError("frequencies must sum to one")
    edge_count = next(iter(lengths))
    return tuple(
        sum(freq * topology[edge] for topology, freq in normalized.items())
        for edge in range(edge_count)
    )


def expected_topology_distance(
    frequencies: Mapping[Topology, float],
    edge_weights: Sequence[float] | None = None,
) -> float:
    """Return E[q(S,T)] for independent topology draws."""

    marginals = topology_marginal_release_frequencies(frequencies)
    if edge_weights is None:
        weights = [1.0] * len(marginals)
    else:
        if len(edge_weights) != len(marginals):
            raise ValueError("one edge weight is required per topology coordinate")
        if any(weight <= 0.0 for weight in edge_weights):
            raise ValueError("edge weights must be positive")
        weights = edge_weights
    return 2.0 * sum(
        weight * marginal * (1.0 - marginal)
        for weight, marginal in zip(weights, marginals)
    )


def _validate_distribution(
    intrinsic_payoffs: Mapping[Topology, float],
    frequencies: Mapping[Topology, float],
) -> None:
    if not frequencies:
        raise ValueError("frequencies cannot be empty")
    if set(intrinsic_payoffs) != set(frequencies):
        raise ValueError("intrinsic_payoffs and frequencies must have identical topology keys")
    topology_marginal_release_frequencies(frequencies)
