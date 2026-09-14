import math

import pytest

from src.source_topology import (
    initial_migration_slope,
    low_migration_linear_approximation,
    source_topology_summary,
)


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)
MARGINS = (2.0, 1.0)


def test_source_degree_and_slope_covary_with_graph_weight_scale():
    for scale in SCALES:
        adjacency = ((0.0, scale), (scale, 0.0))
        slope = initial_migration_slope(MARGINS, adjacency)
        assert math.isclose(slope / scale, -1.0, rel_tol=1e-12)

        summary = source_topology_summary(MARGINS, adjacency)
        assert summary["source_index"] == 0.0
        assert math.isclose(
            summary["source_weighted_degree"] / scale,
            1.0,
            rel_tol=1e-12,
        )
        assert math.isclose(
            summary["initial_migration_slope"] / scale,
            -1.0,
            rel_tol=1e-12,
        )

        # Inverse migration-rate rescaling preserves the first-order correction.
        approx = low_migration_linear_approximation(
            MARGINS,
            adjacency,
            migration_rate=0.25 / scale,
        )
        assert math.isclose(approx, 1.75, rel_tol=1e-12)


def test_materially_asymmetric_graph_is_rejected_at_every_scale():
    for scale in SCALES:
        adjacency = ((0.0, scale), (2.0 * scale, 0.0))
        with pytest.raises(ValueError, match="symmetric"):
            initial_migration_slope(MARGINS, adjacency)


def test_nonfinite_adjacency_fails_closed():
    with pytest.raises(ValueError):
        initial_migration_slope(
            MARGINS,
            ((0.0, float("nan")), (float("nan"), 0.0)),
        )
