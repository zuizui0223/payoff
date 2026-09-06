from math import isclose

from src.temporal_common_environment import (
    finite_time_log_multiplier,
    linear_environment_shifts,
    linear_environment_temporal_exponents,
    mean_shift,
    temporal_environment_summary,
    temporal_invasion_exponents,
    zero_mean_fluctuation_residual,
)


def test_weighted_mean_shift():
    assert isclose(mean_shift([1.0, -1.0]), 0.0, abs_tol=1e-12)
    assert isclose(mean_shift([1.0, -1.0], [3.0, 1.0]), 0.5, abs_tol=1e-12)


def test_temporal_exponents_shift_reciprocally():
    lambda_d0 = 0.2
    lambda_s0 = -0.4
    shifts = [0.6, -0.2, 0.1]
    q_bar = sum(shifts) / len(shifts)
    d, s = temporal_invasion_exponents(lambda_d0, lambda_s0, shifts)
    assert isclose(d, lambda_d0 + q_bar, abs_tol=1e-12)
    assert isclose(s, lambda_s0 - q_bar, abs_tol=1e-12)


def test_zero_mean_fluctuations_have_zero_long_run_effect():
    baseline = 0.37
    sequences = [
        [1.0, -1.0],
        [10.0, -10.0],
        [3.0, -1.0, -2.0],
        [0.0, 0.0, 0.0],
    ]
    for shifts in sequences:
        assert abs(zero_mean_fluctuation_residual(baseline, shifts)) < 1e-12


def test_season_order_does_not_change_finite_time_log_multiplier():
    baseline = -0.15
    shifts_a = [0.8, -0.3, 0.1]
    durations_a = [2.0, 1.0, 4.0]
    shifts_b = [0.1, 0.8, -0.3]
    durations_b = [4.0, 2.0, 1.0]
    log_a = finite_time_log_multiplier(baseline, shifts_a, durations_a)
    log_b = finite_time_log_multiplier(baseline, shifts_b, durations_b)
    assert isclose(log_a, log_b, abs_tol=1e-12)


def test_linear_environment_depends_only_on_weighted_mean_environment():
    environments_a = [0.0, 2.0]
    durations_a = [1.0, 1.0]
    environments_b = [1.0, 1.0]
    durations_b = [1.0, 1.0]
    e0 = 0.5
    alpha = 0.7
    lambda_d0 = -0.2
    lambda_s0 = 0.1
    a = linear_environment_temporal_exponents(
        lambda_d0, lambda_s0, environments_a, e0, alpha, durations_a
    )
    b = linear_environment_temporal_exponents(
        lambda_d0, lambda_s0, environments_b, e0, alpha, durations_b
    )
    assert all(isclose(x, y, abs_tol=1e-12) for x, y in zip(a, b))


def test_linear_environment_shifts():
    shifts = linear_environment_shifts([1.0, 2.0, 4.0], reference_environment=2.0, slope=0.5)
    assert shifts == [-0.5, 0.0, 1.0]


def test_reciprocal_exponent_sum_is_temporally_invariant():
    lambda_d0 = 0.5
    lambda_s0 = -0.1
    shifts = [2.0, -1.0, 0.4]
    d, s = temporal_invasion_exponents(lambda_d0, lambda_s0, shifts)
    assert isclose(d + s, lambda_d0 + lambda_s0, abs_tol=1e-12)


def test_temporal_summary_consistent():
    summary = temporal_environment_summary(
        lambda_d_baseline=0.2,
        lambda_s_baseline=-0.3,
        environments=[0.0, 2.0, 1.0],
        reference_environment=1.0,
        slope=0.5,
    )
    assert isclose(summary["mean_environment_shift"], 0.0, abs_tol=1e-12)
    assert isclose(summary["lambda_d_temporal"], 0.2, abs_tol=1e-12)
    assert isclose(summary["lambda_s_temporal"], -0.3, abs_tol=1e-12)
    assert isclose(summary["signed_reciprocal_exponent_sum"], -0.1, abs_tol=1e-12)
