"""Population games among hard module partitions.

A partition is represented by pairwise co-membership features. Weighted squared
co-membership distance supplies symmetric architecture feedback, while intrinsic
payoff comes from hard-module recovery minus architecture cost.
"""

from __future__ import annotations

from typing import Dict, Iterable, Mapping, Sequence, Tuple

from src.hard_module_partition import hard_partition_recovery

Partition = Tuple[Tuple[int, ...], ...]


def normalize_partition(n: int, partition: Sequence[Iterable[int]]) -> Partition:
    """Return a canonical partition with sorted members and sorted modules."""

    if n <= 0:
        raise ValueError("n must be positive")
    if not partition:
        raise ValueError("partition cannot be empty")
    modules = [tuple(sorted(int(i) for i in module)) for module in partition]
    if any(not module for module in modules):
        raise ValueError("modules cannot be empty")
    flat = [i for module in modules for i in module]
    if sorted(flat) != list(range(n)):
        raise ValueError("partition must contain every index exactly once")
    modules.sort(key=lambda module: (module[0], len(module), module))
    return tuple(modules)


def comembership_features(
    n: int, partition: Sequence[Iterable[int]]
) -> Tuple[int, ...]:
    """Return c_ij(P) for pairs ordered lexicographically by i<j."""

    modules = normalize_partition(n, partition)
    membership = {}
    for module_index, module in enumerate(modules):
        for i in module:
            membership[i] = module_index
    return tuple(
        int(membership[i] == membership[j])
        for i in range(n)
        for j in range(i + 1, n)
    )


def pair_labels(n: int) -> Tuple[Tuple[int, int], ...]:
    """Return pair order corresponding to comembership_features."""

    if n <= 0:
        raise ValueError("n must be positive")
    return tuple((i, j) for i in range(n) for j in range(i + 1, n))


def partition_distance(
    n: int,
    partition_a: Sequence[Iterable[int]],
    partition_b: Sequence[Iterable[int]],
    pair_weights: Sequence[float] | None = None,
) -> float:
    """Return weighted squared co-membership distance q(P,Q)."""

    left = comembership_features(n, partition_a)
    right = comembership_features(n, partition_b)
    if pair_weights is None:
        weights = [1.0] * len(left)
    else:
        if len(pair_weights) != len(left):
            raise ValueError("one pair weight is required per unordered function pair")
        if any(float(weight) <= 0.0 for weight in pair_weights):
            raise ValueError("pair_weights must be positive")
        weights = [float(weight) for weight in pair_weights]
    return sum(
        weight * (x - y) ** 2
        for weight, x, y in zip(weights, left, right)
    )


def intrinsic_partition_payoff(
    optima: Sequence[float],
    weights: Sequence[float],
    partition: Sequence[Iterable[int]],
    extra_module_cost: float,
) -> float:
    """Return b(P)=R(P)-kappa(|P|-1)."""

    if extra_module_cost < 0.0:
        raise ValueError("extra_module_cost must be non-negative")
    normalized = normalize_partition(len(optima), partition)
    recovery = hard_partition_recovery(optima, weights, normalized)
    return recovery - extra_module_cost * (len(normalized) - 1)


def pairwise_partition_payoff_parameters(
    intrinsic_a: float,
    intrinsic_b: float,
    n: int,
    partition_a: Sequence[Iterable[int]],
    partition_b: Sequence[Iterable[int]],
    gamma: float,
    pair_weights: Sequence[float] | None = None,
) -> Tuple[float, float]:
    """Return canonical (phi,eta) for B mutant against A resident."""

    q = partition_distance(n, partition_a, partition_b, pair_weights)
    return intrinsic_b - intrinsic_a, gamma * q


def partition_game_matrix(
    intrinsic_payoffs: Sequence[float],
    partitions: Sequence[Sequence[Iterable[int]]],
    n: int,
    gamma: float,
    pair_weights: Sequence[float] | None = None,
) -> Tuple[Tuple[float, ...], ...]:
    """Return symmetric A_ij=b_i+b_j-gamma*q(P_i,P_j)."""

    if len(intrinsic_payoffs) == 0 or len(intrinsic_payoffs) != len(partitions):
        raise ValueError("intrinsic_payoffs and partitions must have same non-zero length")
    normalized = [normalize_partition(n, partition) for partition in partitions]
    return tuple(
        tuple(
            float(intrinsic_payoffs[i])
            + float(intrinsic_payoffs[j])
            - gamma
            * partition_distance(n, normalized[i], normalized[j], pair_weights)
            for j in range(len(normalized))
        )
        for i in range(len(normalized))
    )


def population_potential(
    intrinsic_payoffs: Sequence[float],
    partitions: Sequence[Sequence[Iterable[int]]],
    frequencies: Sequence[float],
    n: int,
    gamma: float,
    pair_weights: Sequence[float] | None = None,
) -> float:
    """Return p^T A p for the symmetric hard-partition game."""

    if len(frequencies) != len(partitions):
        raise ValueError("frequencies must match partitions")
    if any(float(p) < 0.0 for p in frequencies):
        raise ValueError("frequencies must be non-negative")
    if abs(sum(float(p) for p in frequencies) - 1.0) > 1e-10:
        raise ValueError("frequencies must sum to one")
    matrix = partition_game_matrix(
        intrinsic_payoffs, partitions, n, gamma, pair_weights
    )
    return sum(
        float(frequencies[i]) * float(frequencies[j]) * matrix[i][j]
        for i in range(len(frequencies))
        for j in range(len(frequencies))
    )


def comembership_marginals(
    n: int,
    partitions: Sequence[Sequence[Iterable[int]]],
    frequencies: Sequence[float],
) -> Tuple[float, ...]:
    """Return m_ij=population frequency that each pair shares a module."""

    if len(partitions) == 0 or len(partitions) != len(frequencies):
        raise ValueError("partitions and frequencies must have same non-zero length")
    if any(float(p) < 0.0 for p in frequencies):
        raise ValueError("frequencies must be non-negative")
    if abs(sum(float(p) for p in frequencies) - 1.0) > 1e-10:
        raise ValueError("frequencies must sum to one")
    features = [comembership_features(n, partition) for partition in partitions]
    return tuple(
        sum(float(p) * features[state][feature] for state, p in enumerate(frequencies))
        for feature in range(len(features[0]))
    )


def potential_from_comembership_marginals(
    intrinsic_payoffs: Sequence[float],
    frequencies: Sequence[float],
    marginals: Sequence[float],
    gamma: float,
    pair_weights: Sequence[float] | None = None,
) -> float:
    """Return V=2E[b]-2gamma sum w*m(1-m)."""

    if len(intrinsic_payoffs) != len(frequencies):
        raise ValueError("intrinsic_payoffs and frequencies must have same length")
    if any(float(p) < 0.0 for p in frequencies):
        raise ValueError("frequencies must be non-negative")
    if abs(sum(float(p) for p in frequencies) - 1.0) > 1e-10:
        raise ValueError("frequencies must sum to one")
    if any(not 0.0 <= float(m) <= 1.0 for m in marginals):
        raise ValueError("marginals must lie in [0,1]")
    if pair_weights is None:
        weights = [1.0] * len(marginals)
    else:
        if len(pair_weights) != len(marginals):
            raise ValueError("pair_weights must match marginals")
        if any(float(weight) <= 0.0 for weight in pair_weights):
            raise ValueError("pair_weights must be positive")
        weights = [float(weight) for weight in pair_weights]
    mean_intrinsic = sum(float(p) * float(b) for p, b in zip(frequencies, intrinsic_payoffs))
    diversity = sum(
        weight * float(m) * (1.0 - float(m))
        for weight, m in zip(weights, marginals)
    )
    return 2.0 * mean_intrinsic - 2.0 * gamma * diversity


def registered_three_function_architectures():
    """Return named S,M,F partitions and intrinsic payoffs for kappa=1 fixture."""

    partitions = {
        "S": ((0, 1, 2),),
        "M": ((0, 1), (2,)),
        "F": ((0,), (1,), (2,)),
    }
    payoffs = {
        "S": 0.0,
        "M": 19.0 / 6.0,
        "F": 8.0 / 3.0,
    }
    return partitions, payoffs


def registered_three_function_phase(h: float, tol: float = 1e-12) -> Dict[str, float | str]:
    """Return exact stable phase/equilibrium for gamma=-h in registered S,M,F game."""

    if h < 0.0:
        raise ValueError("h must be non-negative")
    if h <= 0.5 + tol:
        return {
            "phase": "M_monomorphic",
            "p_S": 0.0,
            "p_M": 1.0,
            "p_F": 0.0,
        }
    if h <= 19.0 / 12.0 + tol:
        p_f = (2.0 * h - 1.0) / (4.0 * h)
        return {
            "phase": "M_F_coexistence",
            "p_S": 0.0,
            "p_M": 1.0 - p_f,
            "p_F": p_f,
        }
    return {
        "phase": "S_M_F_coexistence",
        "p_S": (12.0 * h - 19.0) / (24.0 * h),
        "p_M": 25.0 / (24.0 * h),
        "p_F": (2.0 * h - 1.0) / (4.0 * h),
    }


def registered_three_function_effective_payoffs(
    h: float, frequencies: Mapping[str, float]
) -> Dict[str, float]:
    """Return relative effective payoffs u_S,u_M,u_F for gamma=-h fixture."""

    if h < 0.0:
        raise ValueError("h must be non-negative")
    if set(frequencies) != {"S", "M", "F"}:
        raise ValueError("frequencies must have S,M,F keys")
    if any(float(value) < 0.0 for value in frequencies.values()):
        raise ValueError("frequencies must be non-negative")
    if abs(sum(float(value) for value in frequencies.values()) - 1.0) > 1e-10:
        raise ValueError("frequencies must sum to one")
    p_s = float(frequencies["S"])
    p_m = float(frequencies["M"])
    p_f = float(frequencies["F"])
    return {
        "S": 2.0 * h * p_m + 3.0 * h * p_f,
        "M": 19.0 / 6.0 + 2.0 * h * p_s + h * p_f,
        "F": 8.0 / 3.0 + 3.0 * h * p_s + h * p_m,
    }
