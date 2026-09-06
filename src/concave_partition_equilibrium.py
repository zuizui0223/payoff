"""Stable mixtures for concave hard-partition distance games.

For gamma<0, the symmetric co-membership squared-distance kernel makes the
population potential concave on the simplex. For a modest number of candidate
partition strategies, support enumeration plus KKT conditions recovers a global
stable mixture.
"""

from __future__ import annotations

from itertools import combinations
from typing import Dict, Iterable, Sequence, Tuple

from src.hard_partition_game import partition_game_matrix, population_potential


def stable_negative_feedback_mixture(
    intrinsic_payoffs: Sequence[float],
    partitions: Sequence[Sequence[Iterable[int]]],
    n: int,
    gamma: float,
    pair_weights: Sequence[float] | None = None,
    tol: float = 1e-10,
    max_strategies: int = 12,
) -> Dict[str, object]:
    """Return one global KKT maximizer for a gamma<0 partition game.

    The method enumerates candidate supports. It is intended for a modest,
    preregistered candidate architecture set, not all Bell-number partitions.
    """

    m = len(partitions)
    if m == 0 or len(intrinsic_payoffs) != m:
        raise ValueError("intrinsic_payoffs and partitions must have same non-zero length")
    if gamma >= 0.0:
        raise ValueError("stable_negative_feedback_mixture requires gamma<0")
    if m > max_strategies:
        raise ValueError("candidate strategy count exceeds support-enumeration limit")
    if tol <= 0.0:
        raise ValueError("tol must be positive")

    matrix = partition_game_matrix(
        intrinsic_payoffs, partitions, n, gamma, pair_weights
    )
    candidates = []

    for support_size in range(1, m + 1):
        for support in combinations(range(m), support_size):
            solved = _solve_support_kkt(matrix, support, tol)
            if solved is None:
                continue
            frequencies, lagrange = solved
            payoffs = _matrix_vector(matrix, frequencies)
            if any(
                payoffs[index] > lagrange + 10.0 * tol
                for index in range(m)
                if index not in support
            ):
                continue
            potential = population_potential(
                intrinsic_payoffs,
                partitions,
                frequencies,
                n,
                gamma,
                pair_weights,
            )
            candidates.append(
                {
                    "support": support,
                    "frequencies": frequencies,
                    "lagrange_payoff": lagrange,
                    "strategy_payoffs": payoffs,
                    "potential": potential,
                }
            )

    if not candidates:
        raise RuntimeError(
            "no nonsingular KKT support found; candidate game may be degenerate"
        )

    candidates.sort(
        key=lambda row: (
            -float(row["potential"]),
            len(row["support"]),
            tuple(row["support"]),
        )
    )
    best = candidates[0]
    tied = sum(
        abs(float(row["potential"]) - float(best["potential"])) <= 100.0 * tol
        for row in candidates
    )
    return {
        **best,
        "candidate_kkt_count": len(candidates),
        "tied_global_kkt_count": tied,
    }


def _solve_support_kkt(matrix, support: Tuple[int, ...], tol: float):
    size = len(support)
    # Solve A_SS p - lambda*1 = 0, 1^T p = 1.
    augmented_matrix = [[0.0] * (size + 1) for _ in range(size + 1)]
    rhs = [0.0] * size + [1.0]
    for row_local, row_global in enumerate(support):
        for col_local, col_global in enumerate(support):
            augmented_matrix[row_local][col_local] = float(
                matrix[row_global][col_global]
            )
        augmented_matrix[row_local][size] = -1.0
    for col_local in range(size):
        augmented_matrix[size][col_local] = 1.0

    try:
        solution = _solve_linear_system(augmented_matrix, rhs)
    except ValueError:
        return None

    local_frequencies = solution[:size]
    lagrange = solution[size]
    if any(value <= tol for value in local_frequencies):
        return None

    frequencies = [0.0] * len(matrix)
    for index, value in zip(support, local_frequencies):
        frequencies[index] = value
    if abs(sum(frequencies) - 1.0) > 100.0 * tol:
        return None
    return tuple(frequencies), lagrange


def _matrix_vector(matrix, vector):
    return tuple(
        sum(float(value) * float(weight) for value, weight in zip(row, vector))
        for row in matrix
    )


def _solve_linear_system(matrix, rhs):
    n = len(rhs)
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("matrix must be square and match rhs")
    augmented = [
        [float(value) for value in row] + [float(target)]
        for row, target in zip(matrix, rhs)
    ]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(augmented[row][col]))
        if abs(augmented[pivot][col]) < 1e-13:
            raise ValueError("singular linear system")
        if pivot != col:
            augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        divisor = augmented[col][col]
        for j in range(col, n + 1):
            augmented[col][j] /= divisor
        for row in range(n):
            if row == col:
                continue
            factor = augmented[row][col]
            if abs(factor) < 1e-18:
                continue
            for j in range(col, n + 1):
                augmented[row][j] -= factor * augmented[col][j]
    return [augmented[row][n] for row in range(n)]
