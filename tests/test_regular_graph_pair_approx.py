from math import isclose

from src.regular_graph_pair_approx import (
    graph_bridge_summary,
    graph_cost_boundaries,
    graph_interior_equilibrium,
    graph_payoff_gap,
    graph_phi_boundaries,
    ohtsuki_h,
    payoff_matrix,
    transformed_matrix,
    transformed_parameters,
)


def _gap_from_matrix(matrix, p):
    pi_s = matrix[0][0] * (1.0 - p) + matrix[0][1] * p
    pi_d = matrix[1][0] * (1.0 - p) + matrix[1][1] * p
    return pi_d - pi_s


def test_ohtsuki_correction_is_rule_independent_for_payoff_matrix():
    for degree in [3, 4, 7, 20]:
        for phi, eta in [(-0.7, 0.2), (0.0, 1.3), (0.45, -0.8)]:
            values = [ohtsuki_h(phi, eta, degree, rule) for rule in ["bd", "pc", "db", "im"]]
            expected = -2.0 * phi / (degree - 2.0)
            for value in values:
                assert isclose(value, expected, rel_tol=1e-12, abs_tol=1e-12)
            assert max(values) - min(values) < 1e-12


def test_transformed_matrix_gap_matches_scaled_parameters_all_rules():
    phi = 0.37
    eta = -0.91
    for degree in [3, 5, 12]:
        for rule in ["bd", "pc", "db", "im"]:
            matrix = transformed_matrix(phi, eta, degree, rule)
            for p in [0.0, 0.17, 0.5, 0.83, 1.0]:
                assert isclose(
                    _gap_from_matrix(matrix, p),
                    graph_payoff_gap(p, phi, eta, degree),
                    rel_tol=1e-12,
                    abs_tol=1e-12,
                )


def test_graph_transform_scales_phi_and_preserves_eta():
    phi = 0.6
    eta = 1.1
    for degree in [3, 4, 6, 20]:
        phi_k, eta_k = transformed_parameters(phi, eta, degree)
        assert isclose(phi_k, degree * phi / (degree - 2.0), abs_tol=1e-12)
        assert isclose(eta_k, eta, abs_tol=1e-12)
        assert (phi_k > 0) == (phi > 0)


def test_zero_static_gap_is_fixed_point_of_graph_transform():
    for degree in [3, 4, 10, 100]:
        phi_k, eta_k = transformed_parameters(0.0, -2.3, degree)
        assert phi_k == 0.0
        assert eta_k == -2.3
        assert payoff_matrix(0.0, -2.3) == transformed_matrix(0.0, -2.3, degree, "db")


def test_graph_middle_width_shrinks_with_sparse_degree():
    eta = 1.5
    well_mixed_width = 2.0 * abs(eta)
    previous = None
    for degree in [3, 4, 6, 10, 50, 1000]:
        lower, upper = graph_phi_boundaries(eta, degree)
        width = upper - lower
        expected = well_mixed_width * (degree - 2.0) / degree
        assert isclose(width, expected, rel_tol=1e-12, abs_tol=1e-12)
        assert width < well_mixed_width
        if previous is not None:
            assert width > previous
        previous = width


def test_graph_cost_boundaries_keep_static_midpoint():
    recovery = 2.4
    eta = -0.9
    for degree in [3, 4, 8, 30]:
        k_low, k_high = graph_cost_boundaries(recovery, eta, degree)
        assert isclose((k_low + k_high) / 2.0, recovery, abs_tol=1e-12)
        assert isclose(
            k_high - k_low,
            2.0 * abs(eta) * (degree - 2.0) / degree,
            abs_tol=1e-12,
        )


def test_graph_interior_threshold_moves_away_from_half_when_phi_nonzero():
    phi = 0.1
    eta = 1.0
    p_well = 0.5 * (1.0 - phi / eta)
    for degree in [3, 4, 8]:
        p_graph = graph_interior_equilibrium(phi, eta, degree)
        assert p_graph is not None
        assert p_graph < p_well
    assert graph_interior_equilibrium(0.0, eta, 3) == 0.5


def test_large_degree_recovers_well_mixed_gap():
    phi = -0.42
    eta = 0.77
    p = 0.63
    well_mixed = phi + eta * (2.0 * p - 1.0)
    graph = graph_payoff_gap(p, phi, eta, degree=1_000_000)
    assert abs(graph - well_mixed) < 1e-6


def test_graph_bridge_summary_is_self_consistent():
    summary = graph_bridge_summary(phi=0.25, eta=-0.6, degree=5)
    assert isclose(summary["phi_graph"], summary["phi"] * summary["phi_amplification"], abs_tol=1e-12)
    assert isclose(summary["eta_graph"], summary["eta"], abs_tol=1e-12)
    assert isclose(
        summary["middle_phi_width"],
        summary["middle_phi_upper"] - summary["middle_phi_lower"],
        abs_tol=1e-12,
    )
