from math import exp

import pytest

from src.phase_retention_recovery import (
    LambdaRecoveryDesign,
    corrected_lambda_from_known_error,
    expected_naive_lambda,
    fit_naive_lambda,
    lambda_from_tracking_rates,
    lower_tail_null_probability,
    simulate_lambda_recovery,
)


def design(
    *,
    true_lambda=0.5,
    latent_phase_sd=10.0,
    error_sd=0.0,
    error_correlation=0.0,
    n_pairs=200,
):
    return LambdaRecoveryDesign(
        true_lambda=true_lambda,
        latent_phase_sd=latent_phase_sd,
        predictor_error_sd=error_sd,
        outcome_error_sd=error_sd,
        error_correlation=error_correlation,
        process_noise_sd=0.0,
        n_pairs=n_pairs,
    )


def test_tracking_rates_map_exactly_to_retained_phase_fraction():
    assert lambda_from_tracking_rates(
        0.2, 0.3
    ) == pytest.approx(exp(-0.5))
    assert lambda_from_tracking_rates(
        0.0, 0.0
    ) == pytest.approx(1.0)


@pytest.mark.parametrize(
    ("true_lambda", "error_sd", "expected"),
    [
        (0.10, 0.0, 0.10),
        (0.10, 3.0, 0.0917431193),
        (0.10, 6.0, 0.0735294118),
        (0.10, 10.0, 0.05),
        (0.50, 0.0, 0.50),
        (0.50, 3.0, 0.4587155963),
        (0.50, 6.0, 0.3676470588),
        (0.50, 10.0, 0.25),
        (0.86, 0.0, 0.86),
        (0.86, 3.0, 0.7889908257),
        (0.86, 6.0, 0.6323529412),
        (0.86, 10.0, 0.43),
    ],
)
def test_analytic_regression_dilution_reproduces_reference_grid(
    true_lambda,
    error_sd,
    expected,
):
    row = design(
        true_lambda=true_lambda,
        error_sd=error_sd,
    )
    assert expected_naive_lambda(
        row
    ) == pytest.approx(expected)


def test_lambda_one_null_can_look_like_strong_contraction():
    row = design(
        true_lambda=1.0,
        error_sd=10.0,
    )
    assert expected_naive_lambda(
        row
    ) == pytest.approx(0.5)


def test_positive_consecutive_error_correlation_can_remove_attenuation():
    row = design(
        true_lambda=1.0,
        error_sd=10.0,
        error_correlation=1.0,
    )
    assert expected_naive_lambda(
        row
    ) == pytest.approx(1.0)


def test_monte_carlo_mean_tracks_analytic_expectation():
    row = LambdaRecoveryDesign(
        true_lambda=0.86,
        latent_phase_sd=10.0,
        predictor_error_sd=6.0,
        outcome_error_sd=6.0,
        error_correlation=0.0,
        process_noise_sd=2.0,
        n_pairs=400,
    )
    summary = simulate_lambda_recovery(
        row,
        replicates=300,
        seed=20260922,
    )
    assert summary.mean_naive_lambda == pytest.approx(
        summary.expected_naive_lambda,
        abs=0.02,
    )
    assert summary.mean_naive_lambda < row.true_lambda
    assert summary.q025 < summary.q50 < summary.q975


def test_naive_slope_is_exact_without_noise():
    x = (-2.0, -1.0, 0.0, 1.0, 2.0)
    y = tuple(3.0 + 0.4 * value for value in x)
    assert fit_naive_lambda(x, y) == pytest.approx(0.4)


def test_known_error_correction_recovers_true_lambda_in_reference_case():
    # Latent Var(X)=100, predictor error Var=36, so observed Var=136.
    # Independent measurement error attenuates lambda=0.5 to 0.367647...
    corrected = corrected_lambda_from_known_error(
        naive_lambda=0.36764705882352944,
        observed_predictor_variance=136.0,
        predictor_error_variance=36.0,
    )
    assert corrected == pytest.approx(0.5)


def test_known_error_correction_handles_correlated_measurement_error():
    # lambda=0.5, latent predictor variance=100, error covariance=18,
    # observed predictor variance=136 -> naive covariance=68.
    naive = 68.0 / 136.0
    corrected = corrected_lambda_from_known_error(
        naive_lambda=naive,
        observed_predictor_variance=136.0,
        predictor_error_variance=36.0,
        predictor_outcome_error_covariance=18.0,
    )
    assert corrected == pytest.approx(0.5)


def test_lower_tail_null_probability_uses_plus_one_correction():
    p = lower_tail_null_probability(
        0.5,
        (0.4, 0.6, 0.7, 0.8),
    )
    assert p == pytest.approx(2 / 5)


def test_correction_refuses_error_variance_that_exhausts_predictor_variance():
    with pytest.raises(ValueError, match="positive latent variance"):
        corrected_lambda_from_known_error(
            naive_lambda=0.5,
            observed_predictor_variance=25.0,
            predictor_error_variance=25.0,
        )


def test_invalid_error_correlation_is_rejected():
    with pytest.raises(ValueError, match="correlation"):
        design(error_correlation=1.1)
