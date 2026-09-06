from math import isclose

from src.environment_mosaic import invasion_exponent
from src.source_topology import (
    initial_migration_slope,
    low_migration_linear_approximation,
    source_topology_summary,
    unique_best_source_index,
)


def test_unique_best_source_index():
    assert unique_best_source_index([-0.2, 0.7, 0.1]) == 1


def test_initial_slope_is_minus_weighted_degree():
    margins = [0.9, -0.2, -0.5]
    adjacency = [
        [0.0, 2.0, 0.5],
        [2.0, 0.0, 1.0],
        [0.5, 1.0, 0.0],
    ]
    assert isclose(initial_migration_slope(margins, adjacency), -2.5, abs_tol=1e-12)


def test_finite_difference_matches_initial_slope():
    margins = [1.1, 0.2, -0.8]
    adjacency = [
        [0.0, 1.5, 0.4],
        [1.5, 0.0, 0.2],
        [0.4, 0.2, 0.0],
    ]
    eps = 1e-6
    lambda0 = invasion_exponent(margins, adjacency, 0.0)
    lambda1 = invasion_exponent(margins, adjacency, eps)
    numerical = (lambda1 - lambda0) / eps
    analytic = initial_migration_slope(margins, adjacency)
    assert isclose(numerical, analytic, rel_tol=1e-5, abs_tol=1e-5)


def test_low_migration_linear_approximation():
    margins = [0.8, -0.3]
    adjacency = [[0.0, 1.0], [1.0, 0.0]]
    m = 1e-5
    approx = low_migration_linear_approximation(margins, adjacency, m)
    exact = invasion_exponent(margins, adjacency, m)
    assert abs(approx - exact) < 1e-9


def test_more_connected_source_has_faster_initial_dilution():
    margins = [1.0, -0.4, -0.6]
    weak_source_connection = [
        [0.0, 0.2, 0.2],
        [0.2, 0.0, 1.0],
        [0.2, 1.0, 0.0],
    ]
    strong_source_connection = [
        [0.0, 1.2, 1.2],
        [1.2, 0.0, 1.0],
        [1.2, 1.0, 0.0],
    ]
    slope_weak = initial_migration_slope(margins, weak_source_connection)
    slope_strong = initial_migration_slope(margins, strong_source_connection)
    assert slope_strong < slope_weak


def test_source_topology_summary():
    margins = [-0.1, 0.6, -0.9]
    adjacency = [
        [0.0, 0.5, 0.0],
        [0.5, 0.0, 1.25],
        [0.0, 1.25, 0.0],
    ]
    summary = source_topology_summary(margins, adjacency)
    assert summary["source_index"] == 1.0
    assert summary["source_margin"] == 0.6
    assert isclose(summary["source_weighted_degree"], 1.75, abs_tol=1e-12)
    assert isclose(summary["initial_migration_slope"], -1.75, abs_tol=1e-12)
