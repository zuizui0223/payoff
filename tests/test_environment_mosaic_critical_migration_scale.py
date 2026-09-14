from math import isclose

from src.environment_mosaic import (
    critical_migration_rate,
    two_patch_rescue_threshold,
)


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)
BASE_MARGINS = (0.5, -1.5)
UNIT_ADJACENCY = ((0.0, 1.0), (1.0, 0.0))
EXPECTED = two_patch_rescue_threshold(*BASE_MARGINS)


def test_general_solver_matches_exact_two_patch_threshold():
    observed = critical_migration_rate(
        BASE_MARGINS,
        UNIT_ADJACENCY,
        tol=1e-12,
    )
    assert isclose(observed, EXPECTED, rel_tol=1e-10, abs_tol=0.0)


def test_threshold_covaries_with_common_margin_rate_scale():
    for scale in SCALES:
        observed = critical_migration_rate(
            tuple(scale * value for value in BASE_MARGINS),
            UNIT_ADJACENCY,
            tol=1e-12,
        )
        assert isclose(
            observed / scale,
            EXPECTED,
            rel_tol=1e-10,
            abs_tol=0.0,
        )


def test_threshold_covaries_inversely_with_graph_weight_scale():
    for scale in SCALES:
        adjacency = ((0.0, scale), (scale, 0.0))
        observed = critical_migration_rate(
            BASE_MARGINS,
            adjacency,
            tol=1e-12,
        )
        assert isclose(
            observed * scale,
            EXPECTED,
            rel_tol=1e-10,
            abs_tol=0.0,
        )


def test_large_physical_threshold_above_old_cutoff_solves_normally():
    graph_scale = 1e-16
    observed = critical_migration_rate(
        BASE_MARGINS,
        ((0.0, graph_scale), (graph_scale, 0.0)),
        tol=1e-12,
    )
    assert observed > 1e15
    assert isclose(
        observed * graph_scale,
        EXPECTED,
        rel_tol=1e-10,
        abs_tol=0.0,
    )


def test_tiny_heterogeneous_margins_are_not_rounded_to_homogeneous():
    scale = 1e-16
    observed = critical_migration_rate(
        tuple(scale * value for value in BASE_MARGINS),
        UNIT_ADJACENCY,
        tol=1e-12,
    )
    assert observed > 0.0
    assert isclose(
        observed / scale,
        EXPECTED,
        rel_tol=1e-10,
        abs_tol=0.0,
    )
