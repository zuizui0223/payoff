from math import isclose

import pytest

from src.triangular_kernel_barrier import (
    triangular_barrier_receipt,
    triangular_feedback_window,
)


BASE = dict(alpha=0.5, kappa=1.0, gamma=-2.0, epsilon=0.3, length=1.0)


def test_barrier_receipt_is_invariant_to_architecture_coordinate_units():
    reference = triangular_barrier_receipt(**BASE)
    assert reference.global_better_across_barrier

    for scale in (1e-16, 1.0, 1e16):
        result = triangular_barrier_receipt(
            alpha=BASE["alpha"] / scale,
            kappa=BASE["kappa"] / (scale * scale),
            gamma=BASE["gamma"] / (scale * scale),
            epsilon=BASE["epsilon"] * scale,
            length=BASE["length"] * scale,
        )
        assert result.ridge_and_dip_exist == reference.ridge_and_dip_exist
        assert result.outside_global_better == reference.outside_global_better
        assert result.global_better_across_barrier == reference.global_better_across_barrier
        assert isclose(
            result.local_max_location,
            reference.local_max_location * scale,
            rel_tol=2e-13,
            abs_tol=0.0,
        )
        assert isclose(
            result.intrinsic_optimum,
            reference.intrinsic_optimum * scale,
            rel_tol=2e-13,
            abs_tol=0.0,
        )
        assert isclose(
            result.local_max_payoff,
            reference.local_max_payoff,
            rel_tol=2e-13,
            abs_tol=0.0,
        )
        assert isclose(
            result.outside_optimum_payoff,
            reference.outside_optimum_payoff,
            rel_tol=2e-13,
            abs_tol=0.0,
        )


def test_barrier_receipt_is_invariant_to_common_payoff_scaling():
    reference = triangular_barrier_receipt(**BASE)
    for scale in (1e-16, 1.0, 1e16):
        result = triangular_barrier_receipt(
            alpha=BASE["alpha"] * scale,
            kappa=BASE["kappa"] * scale,
            gamma=BASE["gamma"] * scale,
            epsilon=BASE["epsilon"],
            length=BASE["length"],
        )
        assert result.ridge_and_dip_exist == reference.ridge_and_dip_exist
        assert result.outside_global_better == reference.outside_global_better
        assert result.global_better_across_barrier == reference.global_better_across_barrier
        assert isclose(result.local_max_location, reference.local_max_location, rel_tol=2e-13)
        assert isclose(
            result.local_max_payoff,
            reference.local_max_payoff * scale,
            rel_tol=2e-13,
            abs_tol=0.0,
        )
        assert isclose(
            result.barrier_depth,
            reference.barrier_depth * scale,
            rel_tol=3e-13,
            abs_tol=0.0,
        )


def test_feedback_window_covaries_under_coordinate_and_payoff_units():
    reference = triangular_feedback_window(
        alpha=0.5, kappa=1.0, epsilon=0.3, length=1.0
    )

    for scale in (1e-16, 1.0, 1e16):
        coordinate = triangular_feedback_window(
            alpha=0.5 / scale,
            kappa=1.0 / (scale * scale),
            epsilon=0.3 * scale,
            length=1.0 * scale,
        )
        assert isclose(coordinate.dimensionless_range, reference.dimensionless_range, rel_tol=2e-13)
        assert isclose(
            coordinate.upper_contact_location,
            reference.upper_contact_location * scale,
            rel_tol=2e-13,
            abs_tol=0.0,
        )
        assert isclose(
            coordinate.ridge_onset_G,
            reference.ridge_onset_G / (scale * scale),
            rel_tol=3e-13,
            abs_tol=0.0,
        )
        assert isclose(
            coordinate.global_better_upper_G,
            reference.global_better_upper_G / (scale * scale),
            rel_tol=3e-13,
            abs_tol=0.0,
        )
        assert isclose(
            coordinate.outside_optimum_payoff,
            reference.outside_optimum_payoff,
            rel_tol=2e-13,
            abs_tol=0.0,
        )

    for scale in (1e-16, 1.0, 1e16):
        payoff = triangular_feedback_window(
            alpha=0.5 * scale,
            kappa=1.0 * scale,
            epsilon=0.3,
            length=1.0,
        )
        assert isclose(payoff.dimensionless_range, reference.dimensionless_range, rel_tol=2e-13)
        assert isclose(payoff.upper_contact_location, reference.upper_contact_location, rel_tol=2e-13)
        assert isclose(
            payoff.ridge_onset_G,
            reference.ridge_onset_G * scale,
            rel_tol=3e-13,
            abs_tol=0.0,
        )
        assert isclose(
            payoff.global_better_upper_G,
            reference.global_better_upper_G * scale,
            rel_tol=3e-13,
            abs_tol=0.0,
        )
        assert isclose(
            payoff.outside_optimum_payoff,
            reference.outside_optimum_payoff * scale,
            rel_tol=2e-13,
            abs_tol=0.0,
        )


def test_feedback_window_rejects_out_of_domain_optimum_at_tiny_coordinate_scale():
    with pytest.raises(ValueError, match="alpha/kappa <= length"):
        triangular_feedback_window(alpha=1.0001, kappa=1.0, epsilon=0.3, length=1.0)

    scale = 1e-16
    with pytest.raises(ValueError, match="alpha/kappa <= length"):
        triangular_feedback_window(
            alpha=1.0001 / scale,
            kappa=1.0 / (scale * scale),
            epsilon=0.3 * scale,
            length=1.0 * scale,
        )
