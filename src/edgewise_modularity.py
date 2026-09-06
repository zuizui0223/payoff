"""Edgewise coupling and modular-topology utilities for PAYOFF.

For trait coordinates x and function optima theta,
    D(x;c)=sum_i a_i(x_i-theta_i)^2 + sum_e c_e(x_i-x_j)^2.

The optimized edge pressure is exactly
    dD*/dc_e=(x_i*-x_j*)^2.

Relative to reference couplings c0, decoupling d=c0-c has recovery
    R(d)=D*(c0)-D*(c0-d).
Under linear decoupling costs a globally optimal representative exists at a
box vertex, so small graphs can be audited by enumerating released-edge sets.
"""

from __future__ import annotations

from itertools import product
from typing import Dict, List, Sequence, Tuple

Edge = Tuple[int, int]


def optimized_phenotype(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    couplings: Sequence[float],
) -> List[float]:
    """Return unique optimized phenotype x* for edgewise quadratic coupling."""

    _validate_problem(optima, trait_weights, edges, couplings)
    n = len(optima)
    matrix = [[0.0] * n for _ in range(n)]
    rhs = [0.0] * n
    for i, (theta, weight) in enumerate(zip(optima, trait_weights)):
        matrix[i][i] = float(weight)
        rhs[i] = weight * theta

    for (i, j), coupling in zip(edges, couplings):
        matrix[i][i] += coupling
        matrix[j][j] += coupling
        matrix[i][j] -= coupling
        matrix[j][i] -= coupling

    return _solve_linear_system(matrix, rhs)


def optimized_loss(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    couplings: Sequence[float],
) -> float:
    """Return minimized quadratic loss D*(c)."""

    x = optimized_phenotype(optima, trait_weights, edges, couplings)
    base = sum(
        weight * (value - theta) ** 2
        for value, theta, weight in zip(x, optima, trait_weights)
    )
    coupling_loss = sum(
        coupling * (x[i] - x[j]) ** 2
        for (i, j), coupling in zip(edges, couplings)
    )
    return base + coupling_loss


def edge_pressures(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    couplings: Sequence[float],
) -> List[float]:
    """Return exact marginal coupling penalties (x_i*-x_j*)^2 for each edge."""

    x = optimized_phenotype(optima, trait_weights, edges, couplings)
    return [(x[i] - x[j]) ** 2 for i, j in edges]


def recovery_from_decoupling(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    reference_couplings: Sequence[float],
    decouplings: Sequence[float],
) -> float:
    """Return R(d)=D*(c0)-D*(c0-d)."""

    current = _current_couplings(reference_couplings, decouplings)
    reference = optimized_loss(optima, trait_weights, edges, reference_couplings)
    released = optimized_loss(optima, trait_weights, edges, current)
    return reference - released


def recovery_gradient(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    reference_couplings: Sequence[float],
    decouplings: Sequence[float],
) -> List[float]:
    """Return exact gradient dR/dd_e=(x_i*-x_j*)^2 at current decoupling."""

    current = _current_couplings(reference_couplings, decouplings)
    return edge_pressures(optima, trait_weights, edges, current)


def linear_decoupling_cost(decouplings: Sequence[float], costs: Sequence[float]) -> float:
    """Return sum_e k_e d_e."""

    if len(decouplings) != len(costs):
        raise ValueError("decouplings and costs must have same length")
    if any(d < 0.0 for d in decouplings):
        raise ValueError("decouplings must be non-negative")
    if any(k < 0.0 for k in costs):
        raise ValueError("linear costs must be non-negative")
    return sum(d * k for d, k in zip(decouplings, costs))


def net_gain_linear_cost(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    reference_couplings: Sequence[float],
    decouplings: Sequence[float],
    linear_costs: Sequence[float],
) -> float:
    """Return Phi(d)=R(d)-sum k_e d_e."""

    return recovery_from_decoupling(
        optima,
        trait_weights,
        edges,
        reference_couplings,
        decouplings,
    ) - linear_decoupling_cost(decouplings, linear_costs)


def enumerate_vertex_topologies(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    reference_couplings: Sequence[float],
    linear_costs: Sequence[float],
) -> List[Dict[str, object]]:
    """Enumerate all retain/release vertices for small edge sets."""

    _validate_problem(optima, trait_weights, edges, reference_couplings)
    if len(linear_costs) != len(edges):
        raise ValueError("one linear cost is required per edge")
    if any(k < 0.0 for k in linear_costs):
        raise ValueError("linear costs must be non-negative")

    rows: List[Dict[str, object]] = []
    for bits in product((0, 1), repeat=len(edges)):
        decouplings = [
            float(bit) * reference
            for bit, reference in zip(bits, reference_couplings)
        ]
        current = _current_couplings(reference_couplings, decouplings)
        rows.append(
            {
                "released": tuple(bool(bit) for bit in bits),
                "decouplings": tuple(decouplings),
                "couplings": tuple(current),
                "recovery": recovery_from_decoupling(
                    optima,
                    trait_weights,
                    edges,
                    reference_couplings,
                    decouplings,
                ),
                "architecture_cost": linear_decoupling_cost(
                    decouplings, linear_costs
                ),
                "net_gain": net_gain_linear_cost(
                    optima,
                    trait_weights,
                    edges,
                    reference_couplings,
                    decouplings,
                    linear_costs,
                ),
            }
        )
    return rows


def best_vertex_topology(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    reference_couplings: Sequence[float],
    linear_costs: Sequence[float],
) -> Dict[str, object]:
    """Return one maximum-net-gain vertex architecture."""

    rows = enumerate_vertex_topologies(
        optima, trait_weights, edges, reference_couplings, linear_costs
    )
    return max(rows, key=lambda row: float(row["net_gain"]))


def edge_release_receipt(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    reference_couplings: Sequence[float],
    decouplings: Sequence[float],
    marginal_costs: Sequence[float],
) -> List[Dict[str, float | str]]:
    """Compare exact marginal recovery pressure with supplied marginal costs."""

    if len(marginal_costs) != len(edges):
        raise ValueError("one marginal cost is required per edge")
    pressures = recovery_gradient(
        optima, trait_weights, edges, reference_couplings, decouplings
    )
    rows: List[Dict[str, float | str]] = []
    for index, (pressure, cost) in enumerate(zip(pressures, marginal_costs)):
        if cost < 0.0:
            raise ValueError("marginal costs must be non-negative")
        margin = pressure - cost
        if margin > 1e-12:
            direction = "favor_more_decoupling"
        elif margin < -1e-12:
            direction = "favor_more_coupling"
        else:
            direction = "marginal_balance"
        rows.append(
            {
                "edge_index": float(index),
                "pressure": pressure,
                "marginal_cost": cost,
                "margin": margin,
                "direction": direction,
            }
        )
    return rows


def _current_couplings(
    reference_couplings: Sequence[float], decouplings: Sequence[float]
) -> List[float]:
    if len(reference_couplings) != len(decouplings):
        raise ValueError("reference_couplings and decouplings must have same length")
    current = []
    for reference, release in zip(reference_couplings, decouplings):
        if reference < 0.0:
            raise ValueError("reference couplings must be non-negative")
        if release < 0.0 or release > reference + 1e-12:
            raise ValueError("decoupling must lie in [0,reference coupling]")
        current.append(max(0.0, reference - release))
    return current


def _validate_problem(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    couplings: Sequence[float],
) -> None:
    n = len(optima)
    if n == 0 or len(trait_weights) != n:
        raise ValueError("optima and trait_weights must have same non-zero length")
    if any(weight <= 0.0 for weight in trait_weights):
        raise ValueError("trait_weights must be positive")
    if len(edges) != len(couplings):
        raise ValueError("one coupling is required per edge")
    if any(c < 0.0 for c in couplings):
        raise ValueError("couplings must be non-negative")
    for i, j in edges:
        if i == j or i < 0 or j < 0 or i >= n or j >= n:
            raise ValueError("edges must connect distinct valid node indices")


def _solve_linear_system(matrix: Sequence[Sequence[float]], rhs: Sequence[float]) -> List[float]:
    """Solve a dense positive-definite linear system with pivoted Gauss-Jordan."""

    n = len(rhs)
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("matrix must be square and match rhs")
    augmented = [
        [float(value) for value in row] + [float(rhs_i)]
        for row, rhs_i in zip(matrix, rhs)
    ]

    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(augmented[row][col]))
        if abs(augmented[pivot][col]) < 1e-15:
            raise ValueError("singular linear system")
        if pivot != col:
            augmented[col], augmented[pivot] = augmented[pivot], augmented[col]

        pivot_value = augmented[col][col]
        for j in range(col, n + 1):
            augmented[col][j] /= pivot_value

        for row in range(n):
            if row == col:
                continue
            factor = augmented[row][col]
            if factor == 0.0:
                continue
            for j in range(col, n + 1):
                augmented[row][j] -= factor * augmented[col][j]

    return [augmented[i][n] for i in range(n)]
