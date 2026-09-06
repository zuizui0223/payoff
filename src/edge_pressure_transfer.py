"""Edge-pressure transfer matrix for coupled architecture optimization.

For
    D(x;c)=sum_i a_i(x_i-theta_i)^2 + sum_e c_e(b_e^T x)^2,
let
    M=A+sum_e c_e b_e b_e^T,
    x*=M^-1 A theta,
    q_e=b_e^T x*.

Using decoupling coordinates d_e=c_e^0-c_e, the marginal recovery pressure is
    p_e=q_e^2.
Its transfer derivative is
    d p_f / d d_e = 2 q_f q_e b_f^T M^-1 b_e.

The full matrix is the Hessian of recovery R(d) and is positive semidefinite,
although individual cross-edge entries can be positive or negative.
"""

from __future__ import annotations

from math import sqrt
from typing import List, Sequence, Tuple

from src.edgewise_modularity import optimized_phenotype

Edge = Tuple[int, int]


def edge_incidence(node_count: int, edge: Edge) -> List[float]:
    """Return oriented incidence vector e_i-e_j for edge (i,j)."""

    i, j = edge
    if node_count <= 0:
        raise ValueError("node_count must be positive")
    if not (0 <= i < node_count and 0 <= j < node_count) or i == j:
        raise ValueError("edge endpoints must be distinct valid node indices")
    vector = [0.0] * node_count
    vector[i] = 1.0
    vector[j] = -1.0
    return vector


def architecture_matrix(
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    couplings: Sequence[float],
) -> List[List[float]]:
    """Return M=A+sum_e c_e b_e b_e^T."""

    if not trait_weights or len(edges) != len(couplings):
        raise ValueError("weights must be non-empty and one coupling is required per edge")
    if any(weight <= 0.0 for weight in trait_weights):
        raise ValueError("trait weights must be positive")
    if any(coupling < 0.0 for coupling in couplings):
        raise ValueError("couplings must be non-negative")
    n = len(trait_weights)
    matrix = [[0.0] * n for _ in range(n)]
    for i, weight in enumerate(trait_weights):
        matrix[i][i] = float(weight)
    for edge, coupling in zip(edges, couplings):
        b = edge_incidence(n, edge)
        for i in range(n):
            for j in range(n):
                matrix[i][j] += coupling * b[i] * b[j]
    return matrix


def edge_signed_disagreements(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    couplings: Sequence[float],
) -> Tuple[float, ...]:
    """Return q_e=b_e^T x* for each oriented edge."""

    phenotype = optimized_phenotype(optima, trait_weights, edges, couplings)
    return tuple(phenotype[i] - phenotype[j] for i, j in edges)


def edge_transfer_matrix(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    couplings: Sequence[float],
) -> Tuple[Tuple[float, ...], ...]:
    """Return Hessian H_fe=d pressure_f/d decoupling_e.

    H_fe = 2 q_f q_e b_f^T M^-1 b_e.
    """

    if not optima or len(optima) != len(trait_weights):
        raise ValueError("optima and trait_weights must have same non-zero length")
    if len(edges) != len(couplings):
        raise ValueError("one coupling is required per edge")
    n = len(optima)
    matrix = architecture_matrix(trait_weights, edges, couplings)
    inverse = _inverse_spd(matrix)
    incidence = [edge_incidence(n, edge) for edge in edges]
    q = edge_signed_disagreements(optima, trait_weights, edges, couplings)

    result = [[0.0] * len(edges) for _ in edges]
    for f in range(len(edges)):
        for e in range(len(edges)):
            transfer = _bilinear(incidence[f], inverse, incidence[e])
            result[f][e] = 2.0 * q[f] * q[e] * transfer
    return tuple(tuple(row) for row in result)


def strongest_positive_cross_transfer(
    transfer_matrix: Sequence[Sequence[float]],
    released_edge_index: int,
) -> Tuple[int, float] | None:
    """Return other edge with largest positive pressure response to releasing e."""

    m = len(transfer_matrix)
    if m == 0 or any(len(row) != m for row in transfer_matrix):
        raise ValueError("transfer_matrix must be non-empty and square")
    if not 0 <= released_edge_index < m:
        raise ValueError("released_edge_index out of range")
    candidates = [
        (f, float(transfer_matrix[f][released_edge_index]))
        for f in range(m)
        if f != released_edge_index and transfer_matrix[f][released_edge_index] > 0.0
    ]
    return max(candidates, key=lambda item: item[1]) if candidates else None


def minimum_quadratic_form_eigen_bound(
    matrix: Sequence[Sequence[float]],
    samples: Sequence[Sequence[float]],
) -> float:
    """Diagnostic minimum v^T H v over supplied vectors, not an eigen solver."""

    m = len(matrix)
    if m == 0 or any(len(row) != m for row in matrix):
        raise ValueError("matrix must be non-empty and square")
    minimum = float("inf")
    for vector in samples:
        if len(vector) != m:
            raise ValueError("sample vector dimension mismatch")
        value = sum(
            vector[i] * matrix[i][j] * vector[j]
            for i in range(m)
            for j in range(m)
        )
        minimum = min(minimum, value)
    return minimum


def _bilinear(left: Sequence[float], matrix, right: Sequence[float]) -> float:
    return sum(
        left[i] * matrix[i][j] * right[j]
        for i in range(len(left))
        for j in range(len(right))
    )


def _inverse_spd(matrix: Sequence[Sequence[float]]) -> List[List[float]]:
    """Gauss-Jordan inverse for small dense SPD matrices used in diagnostics."""

    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("matrix must be non-empty and square")
    augmented = [
        [float(value) for value in row]
        + [1.0 if i == j else 0.0 for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    width = 2 * n
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(augmented[row][col]))
        if abs(augmented[pivot][col]) < 1e-15:
            raise ValueError("matrix is singular")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        for j in range(width):
            augmented[col][j] /= scale
        for row in range(n):
            if row == col:
                continue
            factor = augmented[row][col]
            if factor == 0.0:
                continue
            for j in range(width):
                augmented[row][j] -= factor * augmented[col][j]
    return [row[n:] for row in augmented]
