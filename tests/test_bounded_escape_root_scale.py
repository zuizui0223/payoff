from math import isclose

from src.bounded_interaction_theory import (
    negative_feedback_interface_escape_infimum,
    shared_resident_inside_payoff,
    shared_resident_outside_payoff,
)


BASE = dict(alpha=0.5, kappa=1.0, gamma=-1.0, epsilon=0.1)


def test_escape_distances_covary_under_architecture_coordinate_units():
    reference = negative_feedback_interface_escape_infimum(**BASE)
    for scale in (1e-8, 1.0, 1e8):
        result = negative_feedback_interface_escape_infimum(
            alpha=BASE["alpha"] / scale,
            kappa=BASE["kappa"] / (scale * scale),
            gamma=BASE["gamma"] / (scale * scale),
            epsilon=BASE["epsilon"] * scale,
        )
        assert isclose(
            result.equal_payoff_origin_side,
            reference.equal_payoff_origin_side * scale,
            rel_tol=2e-13,
            abs_tol=0.0,
        )
        assert isclose(
            result.escape_jump_infimum,
            reference.escape_jump_infimum * scale,
            rel_tol=2e-13,
            abs_tol=0.0,
        )
        assert isclose(
            result.inside_boundary_payoff,
            reference.inside_boundary_payoff,
            rel_tol=2e-13,
            abs_tol=0.0,
        )
        assert isclose(
            result.outside_boundary_payoff,
            reference.outside_boundary_payoff,
            rel_tol=2e-13,
            abs_tol=0.0,
        )


def test_escape_geometry_is_invariant_to_common_payoff_scaling():
    reference = negative_feedback_interface_escape_infimum(**BASE)
    for scale in (1e-16, 1.0, 1e16):
        result = negative_feedback_interface_escape_infimum(
            alpha=BASE["alpha"] * scale,
            kappa=BASE["kappa"] * scale,
            gamma=BASE["gamma"] * scale,
            epsilon=BASE["epsilon"],
        )
        assert isclose(
            result.equal_payoff_origin_side,
            reference.equal_payoff_origin_side,
            rel_tol=2e-13,
            abs_tol=0.0,
        )
        assert isclose(
            result.escape_jump_infimum,
            reference.escape_jump_infimum,
            rel_tol=2e-13,
            abs_tol=0.0,
        )
        assert isclose(
            result.interface_jump,
            reference.interface_jump * scale,
            rel_tol=2e-13,
            abs_tol=0.0,
        )


def test_near_linear_root_uses_cancellation_safe_continuous_formula():
    params = dict(
        alpha=0.5,
        kappa=1.0,
        gamma=-0.4999999999,
        epsilon=0.1,
    )
    result = negative_feedback_interface_escape_infimum(**params)
    inside_at_root = shared_resident_inside_payoff(
        result.equal_payoff_origin_side,
        alpha=params["alpha"],
        kappa=params["kappa"],
        gamma=params["gamma"],
    )
    outside_boundary = shared_resident_outside_payoff(
        params["epsilon"],
        alpha=params["alpha"],
        kappa=params["kappa"],
    )
    assert isclose(inside_at_root, outside_boundary, rel_tol=2e-14, abs_tol=0.0)

    coordinate_scale = 1e3
    scaled = negative_feedback_interface_escape_infimum(
        alpha=params["alpha"] / coordinate_scale,
        kappa=params["kappa"] / (coordinate_scale * coordinate_scale),
        gamma=params["gamma"] / (coordinate_scale * coordinate_scale),
        epsilon=params["epsilon"] * coordinate_scale,
    )
    assert isclose(
        scaled.equal_payoff_origin_side / coordinate_scale,
        result.equal_payoff_origin_side,
        rel_tol=2e-13,
        abs_tol=0.0,
    )
