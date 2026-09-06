"""Low-migration topology diagnostics for heterogeneous PAYOFF source patches."""

from __future__ import annotations

from typing import Dict, Sequence


def unique_best_source_index(margins: Sequence[float], tol: float = 1e-12) -> int:
    """Return the unique index attaining the largest local invasion margin."""

    if not margins:
        raise ValueError("margins cannot be empty")
    maximum = max(margins)
    winners = [i for i, value in enumerate(margins) if abs(value - maximum) <= tol]
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
    for i in range(n):
        for j in range(n):
            if adjacency[i][j] < 0.0:
                raise ValueError("adjacency weights must be non-negative")
            if abs(adjacency[i][j] - adjacency[j][i]) > 1e-12:
                raise ValueError("adjacency must be symmetric")
