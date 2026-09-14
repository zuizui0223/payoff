from math import isclose

from src.spatial_environment_gradient import (
    common_eta_window_switch_rate,
    two_patch_coordination_switch_rate,
)


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)
BASE_PHIS = (0.6, -0.6)
ETA = 0.1
UNIT_ADJACENCY = ((0.0, 1.0), (1.0, 0.0))
EXPECTED = two_patch_coordination_switch_rate(BASE_PHIS[0], BASE_PHIS[1], ETA)


def test_general_window_switch_matches_exact_two_patch_result():
    observed = common_eta_window_switch_rate(
        BASE_PHIS,
        ETA,
        UNIT_ADJACENCY,
        tol=1e-12,
    )
    assert isclose(observed, EXPECTED, rel_tol=1e-10, abs_tol=0.0)


def test_window_switch_covaries_with_common_rate_scale():
    for scale in SCALES:
        observed = common_eta_window_switch_rate(
            tuple(scale * value for value in BASE_PHIS),
            scale * ETA,
            UNIT_ADJACENCY,
            tol=1e-12,
        )
        assert isclose(
            observed / scale,
            EXPECTED,
            rel_tol=1e-10,
            abs_tol=0.0,
        )


def test_window_switch_covaries_inversely_with_graph_weight_scale():
    for scale in SCALES:
        adjacency = ((0.0, scale), (scale, 0.0))
        observed = common_eta_window_switch_rate(
            BASE_PHIS,
            ETA,
            adjacency,
            tol=1e-12,
        )
        assert isclose(
            observed * scale,
            EXPECTED,
            rel_tol=1e-10,
            abs_tol=0.0,
        )


def test_large_physical_window_switch_above_old_cutoff_solves_normally():
    graph_scale = 1e-16
    observed = common_eta_window_switch_rate(
        BASE_PHIS,
        ETA,
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


def test_tiny_rate_problem_remains_resolvable():
    scale = 1e-16
    observed = common_eta_window_switch_rate(
        tuple(scale * value for value in BASE_PHIS),
        scale * ETA,
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
