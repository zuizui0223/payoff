"""Low-migration topology diagnostics for heterogeneous PAYOFF source patches."""

from __future__ import annotations

from math import isclose, isfinite
from sys import float_info
from typing import Dict, Sequence

from src.numerical_tolerance import relative_band


def unique_best_source_index(
    margins: Sequence[float], tol: float = 64.0 * float_info.epsilon
) -> int:
    """Return the unique index attaining the largest local invasion margin.

    ``tol`` is a dimensionless relative numerical tolerance.  No fixed
    rate-unit band is used, so common positive rescaling of all local margins
    preserves source uniqueness.
    """

    if not margins:
        raise ValueError("margins cannot be empty")
    numeric = [float(value) for value in margins]
    if not all(isfinite(value) for value in numeric):
        raise ValueError("margins must be finite")
    tol = float(tol)
    if not isfinite(tol) or tol < 0.0:
        raise ValueError("tol must be finite and non-negative")

    maximum = max(numeric)
    winners = [
        i
        for i, value in enumerate(numeric)
        if isclose(value, maximum, rel_tol=tol, abs_tol=0.0)
    ]
    if len(winners) != 1:
        raise ValueError("the largest local margin must be unique")
    return winners[0]


def initial_migration_slope(
    margins: Sequence[float], adjacency: Sequence[Sequence[float]]
) -> float:
    """Return d Lambda/dm at m=0 when the best source is unique.

    For A(m)=diag(r)-mL and a simple largest eigenvalue r_s at m=0,
    first-order symmetric eigenvalue perturbation gives

        Lambda'(0) = - e_s^T L e_s = -degree_s.
    """

    _validate_adjacency(adjacency)
    if len(margins) != len(adjacency):
        raise ValueError("one margin is required per patch")
    source = unique_best_source_index(margins)
    weighted_degree = sum(adjacency[source])
    return -weighted_degree


def low_migration_linear_approximation(
    margins: Sequence[float], adjacency: Sequence[Sequence[float]], migration_rate: float
) -> float:
    """Return max(r)+m Lambda'(0), the first-order low-migration approximation."""

    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    slope = initial_migration_slope(margins, adjacency)
    return max(margins) + migration_rate * slope


def source_topology_summary(
    margins: Sequence[float], adjacency: Sequence[Sequence[float]]
) -> Dict[str, float]:
    """Return best-source strength, degree, and initial dilution slope."""

    _validate_adjacency(adjacency)
    source = unique_best_source_index(margins)
    degree = sum(adjacency[source])
    return {
        "source_index": float(source),
        "source_margin": margins[source],
        "source_weighted_degree": degree,
        "initial_migration_slope": -degree,
    }


def _validate_adjacency(adjacency: Sequence[Sequence[float]]) -> None:
    n = len(adjacency)
    if n == 0 or any(len(row) != n for row in adjacency):
        raise ValueError("adjacency must be non-empty and square")

    numeric = [[float(adjacency[i][j]) for j in range(n)] for i in range(n)]
    for row in numeric:
        for value in row:
            relative_band((value,))
            if value < 0.0:
                raise ValueError("adjacency weights must be non-negative")

    for i in range(n):
        for j in range(i + 1, n):
            left = numeric[i][j]
            right = numeric[j][i]
            if abs(left - right) > relative_band((left, right)):
                raise ValueError("adjacency must be symmetric")
