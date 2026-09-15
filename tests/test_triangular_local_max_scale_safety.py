from math import isclose, isfinite

from src.triangular_kernel_barrier import (
    triangular_barrier_receipt,
    triangular_feedback_window,
)


def _scaled(q: float):
    return {
        "alpha": 0.5 / q,
        "kappa": 1.0 / q / q,
        "gamma": -2.0 / q / q,
        "epsilon": 0.3 * q,
        "length": 1.0 * q,
    }


def test_registered_triangular_local_max_is_coordinate_scale_covariant():
    base = triangular_barrier_receipt(
        alpha=0.5,
        kappa=1.0,
        gamma=-2.0,
        epsilon=0.3,
        length=1.0,
    )
    assert base.local_max_location is not None
    assert base.local_max_payoff is not None

    for q in (1e-100, 1.0, 1e100, 1e155):
        observed = triangular_barrier_receipt(**_scaled(q))
        assert observed.ridge_and_dip_exist == base.ridge_and_dip_exist
        assert observed.outside_global_better == base.outside_global_better
        assert observed.global_better_across_barrier == base.global_better_across_barrier
        assert observed.local_max_location is not None
        assert observed.local_max_payoff is not None
        assert isfinite(observed.local_max_location)
        assert isfinite(observed.local_max_payoff)
        assert isclose(
            observed.local_max_location / q,
            base.local_max_location,
            rel_tol=2e-11,
            abs_tol=0.0,
        )
        assert isclose(
            observed.local_max_payoff,
            base.local_max_payoff,
            rel_tol=2e-11,
            abs_tol=0.0,
        )
        assert isclose(
            observed.barrier_depth,
            base.barrier_depth,
            rel_tol=2e-11,
            abs_tol=0.0,
        )


def test_triangular_feedback_window_remains_covariant_at_extreme_coordinate_scales():
    base = triangular_feedback_window(alpha=0.5, kappa=1.0, epsilon=0.3, length=1.0)

    for q in (1e-100, 1.0, 1e100, 1e155):
        p = _scaled(q)
        observed = triangular_feedback_window(
            alpha=p["alpha"],
            kappa=p["kappa"],
            epsilon=p["epsilon"],
            length=p["length"],
        )
        assert isclose(
            observed.dimensionless_range,
            base.dimensionless_range,
            rel_tol=2e-11,
            abs_tol=0.0,
        )
        assert isclose(
            observed.upper_contact_location / q,
            base.upper_contact_location,
            rel_tol=2e-11,
            abs_tol=0.0,
        )
        assert isclose(
            observed.global_better_upper_G * q * q,
            base.global_better_upper_G,
            rel_tol=2e-11,
            abs_tol=0.0,
        )
        assert isclose(
            observed.ridge_onset_G * q * q,
            base.ridge_onset_G,
            rel_tol=2e-11,
            abs_tol=0.0,
        )
        assert isclose(
            observed.outside_optimum_payoff,
            base.outside_optimum_payoff,
            rel_tol=2e-11,
            abs_tol=0.0,
        )
