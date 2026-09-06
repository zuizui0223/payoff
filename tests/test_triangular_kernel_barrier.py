from src.triangular_kernel_barrier import (
    triangular_barrier_receipt,
    triangular_feedback_window,
)


def test_registered_triangular_witness_has_exact_local_ridge_and_global_better_state():
    result = triangular_barrier_receipt(
        alpha=0.5,
        kappa=1.0,
        gamma=-2.0,
        epsilon=0.3,
    )
    assert result.ridge_and_dip_exist
    assert result.global_better_across_barrier
    assert abs(result.local_max_location - 0.25) < 1e-12
    assert abs(result.local_max_payoff - 0.11458333333333333) < 1e-12
    assert abs(result.boundary_payoff - 0.105) < 1e-12
    assert abs(result.barrier_depth - 0.00958333333333333) < 1e-12
    assert abs(result.outside_optimum_payoff - 0.125) < 1e-12


def test_weak_feedback_fails_to_create_ridge_before_kernel_boundary():
    result = triangular_barrier_receipt(
        alpha=0.5,
        kappa=1.0,
        gamma=-0.5,
        epsilon=0.3,
    )
    assert not result.ridge_and_dip_exist
    assert not result.global_better_across_barrier


def test_very_strong_feedback_makes_local_ridge_itself_better_than_outside_optimum():
    result = triangular_barrier_receipt(
        alpha=0.5,
        kappa=1.0,
        gamma=-5.0,
        epsilon=0.3,
    )
    assert result.ridge_and_dip_exist
    assert result.local_max_payoff > result.outside_optimum_payoff
    assert not result.outside_global_better
    assert not result.global_better_across_barrier


def test_exact_ridge_onset_condition_is_feedback_strength_greater_than_alpha_over_epsilon_minus_kappa():
    threshold_G = 0.5 / 0.3 - 1.0
    below = triangular_barrier_receipt(
        alpha=0.5,
        kappa=1.0,
        gamma=-(threshold_G - 1e-4),
        epsilon=0.3,
    )
    above = triangular_barrier_receipt(
        alpha=0.5,
        kappa=1.0,
        gamma=-(threshold_G + 1e-4),
        epsilon=0.3,
    )
    assert not below.ridge_and_dip_exist
    assert above.ridge_and_dip_exist


def test_registered_global_better_barrier_has_unique_finite_feedback_window():
    window = triangular_feedback_window(
        alpha=0.5,
        kappa=1.0,
        epsilon=0.3,
    )
    assert abs(window.ridge_onset_G - (2.0 / 3.0)) < 1e-12
    assert abs(window.global_better_upper_G - 2.93184698670244) < 1e-9
    assert abs(window.gamma_window_lower + 2.93184698670244) < 1e-9
    assert abs(window.gamma_window_upper + 2.0 / 3.0) < 1e-12

    inside = triangular_barrier_receipt(
        alpha=0.5,
        kappa=1.0,
        gamma=-2.0,
        epsilon=0.3,
    )
    below_onset = triangular_barrier_receipt(
        alpha=0.5,
        kappa=1.0,
        gamma=-0.6,
        epsilon=0.3,
    )
    above_upper = triangular_barrier_receipt(
        alpha=0.5,
        kappa=1.0,
        gamma=-3.2,
        epsilon=0.3,
    )
    assert inside.global_better_across_barrier
    assert not below_onset.global_better_across_barrier
    assert not above_upper.global_better_across_barrier
