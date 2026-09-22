from datetime import date, timedelta
from statistics import stdev

import pytest

from src.wigeon_phase_error_calibration import (
    simulate_true_lambda_one_null,
    summarize_replicate_disagreement,
    tgs_onset_from_daily_mean,
)


def dates_2020(n):
    start = date(2020, 1, 1)
    return [
        start + timedelta(days=index)
        for index in range(n)
    ]


def test_tgs_helper_matches_published_cumulative_minimum_rule():
    dates = dates_2020(120)
    temperatures = [0.0] * 60 + [10.0] * 60
    assert tgs_onset_from_daily_mean(
        dates,
        temperatures,
    ) == 60


def test_tgs_helper_refuses_august_input():
    dates = dates_2020(220)
    temperatures = [5.0] * len(dates)
    with pytest.raises(ValueError, match="January-July"):
        tgs_onset_from_daily_mean(
            dates,
            temperatures,
        )


def test_replicate_disagreement_keeps_equal_replicate_assumption_explicit():
    values = (-4.0, -1.0, 1.0, 4.0)
    summary = summarize_replicate_disagreement(values)
    assert summary.n == 4
    assert summary.sample_sd == pytest.approx(stdev(values))
    assert summary.equal_independent_replicate_error_sd == pytest.approx(
        stdev(values) / (2.0 ** 0.5)
    )


def test_true_lambda_one_null_is_exact_without_measurement_or_process_noise():
    result = simulate_true_lambda_one_null(
        name="zero_noise",
        observed_lambda_hat=1.0,
        observed_residualized_predictor_sd=10.0,
        predictor_error_sd=0.0,
        error_correlation=0.0,
        process_noise_sd=0.0,
        n_pairs=50,
        replicates=20,
        seed=123,
    )
    assert result.status == "COMPLETE"
    assert result.expected_naive_lambda_under_true_one == pytest.approx(1.0)
    assert result.null_mean_lambda_hat == pytest.approx(1.0)
    assert result.null_sd_lambda_hat == pytest.approx(0.0)
    assert result.eiv_corrected_observed_lambda == pytest.approx(1.0)


def test_true_lambda_one_null_fails_closed_if_error_exceeds_observed_signal():
    result = simulate_true_lambda_one_null(
        name="unidentified",
        observed_lambda_hat=0.75,
        observed_residualized_predictor_sd=5.0,
        predictor_error_sd=5.0,
        error_correlation=0.0,
        process_noise_sd=1.0,
        n_pairs=50,
        replicates=20,
        seed=123,
    )
    assert result.status == "NOT_IDENTIFIABLE"
    assert result.inferred_latent_predictor_sd is None
    assert "positive latent phase variance" in result.reason


def test_controller_helper_matches_frozen_formula_on_synthetic_fixture():
    pd = pytest.importorskip("pandas")
    pytest.importorskip("statsmodels")
    pytest.importorskip("scipy")

    rows = []
    for group in range(12):
        individual = f"A{group:02d}"
        year = 2018 + group % 3
        endpoint = 1000.0 + 20.0 * group
        for index in range(20):
            origin_phase = float(index - 10) + group * 0.1
            progress = 50.0 * index + group
            destination_phase = (
                2.0
                + 0.6 * origin_phase
                + 0.01 * (index % 3 - 1)
            )
            rows.append(
                {
                    "individual_id": individual,
                    "year": year,
                    "origin_progress_km": progress,
                    "endpoint_distance_km": endpoint,
                    "origin_stopover_days": 10.0 - 0.2 * origin_phase,
                    "travel_speed_km_day": 50.0,
                    "x": origin_phase,
                    "y": destination_phase,
                }
            )
    from src.wigeon_phase_error_calibration import (
        fit_source_faithful_controller,
    )

    result = fit_source_faithful_controller(
        pd.DataFrame(rows),
        origin_phase_column="x",
        destination_phase_column="y",
    )
    assert result.n_pairs == 240
    assert result.n_individuals == 12
    assert result.lambda_hat == pytest.approx(0.6, abs=0.01)
    assert result.stopover_slope == pytest.approx(-0.2, abs=0.01)
