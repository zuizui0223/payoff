from math import isclose

from src.spatial_environment_gradient import (
    common_eta_window_switch_rate,
    common_eta_zero_migration_signed_width,
    signed_reciprocal_environment_width,
    two_patch_coordination_switch_rate,
)


def test_zero_migration_common_eta_width_is_range_minus_two_eta():
    phis = [0.9, -0.4, 0.2]
    eta = 0.3
    alpha = 0.5
    expected = (max(phis) - min(phis) - 2.0 * eta) / alpha
    assert isclose(
        common_eta_zero_migration_signed_width(phis, eta, alpha),
        expected,
        abs_tol=1e-12,
    )


def test_general_graph_switch_matches_two_patch_closed_form():
    phis = [1.2, -0.4]
    eta = 0.5
    adjacency = [[0.0, 1.0], [1.0, 0.0]]
    numeric = common_eta_window_switch_rate(phis, eta, adjacency)
    exact = two_patch_coordination_switch_rate(phis[0], phis[1], eta)
    assert isclose(numeric, exact, rel_tol=1e-8, abs_tol=1e-8)


def test_connected_three_patch_window_switch_changes_sign_once():
    phis = [1.0, 0.1, -0.8]
    eta = 0.4
    adjacency = [
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ]
    m_switch = common_eta_window_switch_rate(phis, eta, adjacency)
    etas = [eta] * len(phis)
    alpha = 1.0
    assert signed_reciprocal_environment_width(phis, etas, adjacency, 0.5 * m_switch, alpha) > 0.0
    assert abs(signed_reciprocal_environment_width(phis, etas, adjacency, m_switch, alpha)) < 1e-8
    assert signed_reciprocal_environment_width(phis, etas, adjacency, 2.0 * m_switch, alpha) < 0.0


def test_no_switch_when_patch_contrast_does_not_beat_coordination():
    phis = [0.5, 0.0, -0.2]
    eta = 0.4
    adjacency = [
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ]
    assert max(phis) - min(phis) <= 2.0 * eta
    try:
        common_eta_window_switch_rate(phis, eta, adjacency)
    except ValueError:
        pass
    else:
        raise AssertionError("expected no positive window-collapse threshold")
