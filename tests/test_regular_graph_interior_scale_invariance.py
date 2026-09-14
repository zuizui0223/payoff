from math import isclose

from src.payoff_game import interior_equilibrium
from src.regular_graph_pair_approx import (
    graph_interior_equilibrium,
    transformed_parameters,
)


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)


def test_regular_graph_interior_matches_canonical_transformed_game_at_all_scales():
    degree = 3
    phi = 0.1
    eta = -1.0
    reference = graph_interior_equilibrium(phi, eta, degree)
    assert reference is not None

    for scale in SCALES:
        phi_scaled = scale * phi
        eta_scaled = scale * eta
        phi_k, eta_k = transformed_parameters(phi_scaled, eta_scaled, degree)
        expected = interior_equilibrium(phi_k, eta_k)
        observed = graph_interior_equilibrium(phi_scaled, eta_scaled, degree)
        assert expected is not None
        assert observed is not None
        assert isclose(observed, expected, rel_tol=0.0, abs_tol=1e-15)
        assert isclose(observed, reference, rel_tol=0.0, abs_tol=1e-15)


def test_tiny_valid_interior_equilibrium_is_not_lost_to_absolute_payoff_floor():
    observed = graph_interior_equilibrium(1e-17, -1e-16, 3)
    assert observed is not None
    assert isclose(observed, 0.65, rel_tol=0.0, abs_tol=1e-15)


def test_no_interior_case_remains_none_at_all_scales():
    degree = 4
    phi = 1.0
    eta = -0.1
    for scale in SCALES:
        assert graph_interior_equilibrium(scale * phi, scale * eta, degree) is None


def test_zero_feedback_remains_none_at_all_scales():
    for scale in SCALES:
        assert graph_interior_equilibrium(scale * 0.2, 0.0, 5) is None
