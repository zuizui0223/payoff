from math import isclose

from src.symmetric_pair_canonical import (
    architecture_pair_parameters,
    canonical_parameters,
    canonical_shifted_matrix,
    endpoint_margins,
    symmetric_pair_gap,
)


def direct_gap(p: float, a: float, b: float, d: float) -> float:
    pi_s = (1.0 - p) * a + p * b
    pi_t = (1.0 - p) * b + p * d
    return pi_t - pi_s


def test_canonical_coordinates_reconstruct_any_symmetric_pair():
    examples = [
        (0.0, 1.0, 2.0),
        (2.5, -0.7, 4.1),
        (-3.0, 0.2, -1.4),
        (5.0, 5.0, 5.0),
    ]
    for a, b, d in examples:
        phi, eta = canonical_parameters(a, b, d)
        shifted = canonical_shifted_matrix(a, b, d)
        assert isclose(shifted[0][0], 0.0)
        assert isclose(shifted[0][1], b - a)
        assert isclose(shifted[1][0], b - a)
        assert isclose(shifted[1][1], d - a)
        assert isclose(shifted[0][1], phi - eta)
        assert isclose(shifted[1][1], 2.0 * phi)


def test_canonical_gap_matches_direct_symmetric_game():
    a, b, d = 1.7, -0.4, 3.2
    for p in [0.0, 0.1, 0.5, 0.9, 1.0]:
        assert isclose(
            symmetric_pair_gap(p, a, b, d),
            direct_gap(p, a, b, d),
            rel_tol=1e-12,
            abs_tol=1e-12,
        )


def test_endpoint_margins_match_phi_eta_endpoints():
    a, b, d = 1.7, -0.4, 3.2
    phi, eta = canonical_parameters(a, b, d)
    t_into_s, s_into_t = endpoint_margins(a, b, d)
    assert isclose(t_into_s, phi - eta)
    assert isclose(s_into_t, -phi - eta)


def test_architecture_decomposition_formulas():
    b_s = 0.3
    b_t = 0.9
    h_ss = 0.2
    h_st = -0.5
    h_tt = 0.8
    phi, eta = architecture_pair_parameters(b_s, b_t, h_ss, h_st, h_tt)
    assert isclose(phi, b_t - b_s + 0.5 * (h_tt - h_ss))
    assert isclose(eta, 0.5 * (h_ss + h_tt - 2.0 * h_st))


def test_equal_diagonal_feedback_preserves_intrinsic_gap():
    b_s = -0.2
    b_t = 0.7
    phi, eta = architecture_pair_parameters(
        b_s, b_t, h_ss=1.2, h_st=-0.3, h_tt=1.2
    )
    assert isclose(phi, b_t - b_s)
    assert isclose(eta, 1.5)


def test_zero_diagonal_distance_kernel_reduces_to_topology_mapping():
    b_s = 0.1
    b_t = 0.8
    gamma = -0.4
    q = 3.5
    phi, eta = architecture_pair_parameters(
        b_s, b_t, h_ss=0.0, h_st=-gamma * q, h_tt=0.0
    )
    assert isclose(phi, b_t - b_s)
    assert isclose(eta, gamma * q)
