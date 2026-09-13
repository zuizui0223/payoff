import math

import pytest

from src.source_topology import (
    initial_migration_slope,
    low_migration_linear_approximation,
    source_topology_summary,
    unique_best_source_index,
)


ADJACENCY = [
    [0.0, 0.5, 0.0],
    [0.5, 0.0, 1.25],
    [0.0, 1.25, 0.0],
]


def test_best_source_and_initial_slope_are_invariant_to_margin_units():
    base = [-0.2, 1.0, 0.1]
    for scale in (1e-16, 1e-13, 1.0, 1e16):
        margins = [scale * value for value in base]
        assert unique_best_source_index(margins) == 1
        assert initial_migration_slope(margins, ADJACENCY) == -1.75

        summary = source_topology_summary(margins, ADJACENCY)
        assert summary["source_index"] == 1.0
        assert summary["source_margin"] == margins[1]
        assert summary["source_weighted_degree"] == 1.75
        assert summary["initial_migration_slope"] == -1.75


def test_low_migration_approximation_transforms_with_rate_units():
    base_margins = [-0.2, 1.0, 0.1]
    base_migration = 0.03
    reference = low_migration_linear_approximation(
        base_margins, ADJACENCY, base_migration
    )

    for scale in (1e-16, 1e-13, 1e16):
        observed = low_migration_linear_approximation(
            [scale * value for value in base_margins],
            ADJACENCY,
            scale * base_migration,
        )
        assert math.isclose(observed, scale * reference, rel_tol=2e-15, abs_tol=0.0)


def test_exact_equal_maxima_remain_non_unique_at_all_scales():
    for scale in (1e-16, 1.0, 1e16):
        with pytest.raises(ValueError, match="must be unique"):
            unique_best_source_index([scale, scale, -scale])


def test_nonfinite_margins_fail_closed():
    for bad in (math.nan, math.inf, -math.inf):
        with pytest.raises(ValueError, match="finite"):
            unique_best_source_index([0.0, bad])
