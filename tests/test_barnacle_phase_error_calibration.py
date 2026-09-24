import math

import numpy as np
import pandas as pd
import pytest

from src.barnacle_phase_error_calibration import (
    EARLY_JERK_LOGIT,
    fit_fixed_transition_controller,
    fit_gdd_jerk,
    latitude_base_temperature,
    summarize_replicate_differences,
)


def test_gdd_jerk_recovers_exact_logistic_accumulation():
    latitude = 60.0
    t_base = latitude_base_temperature(latitude)
    asymptote = 1200.0
    rate = 0.045
    midpoint = 150.0
    days = np.arange(1, 366, dtype=float)
    cumulative = asymptote / (
        1.0 + np.exp(-rate * (days - midpoint))
    )
    increments = np.diff(
        np.concatenate([[0.0], cumulative])
    )
    assert np.all(increments >= 0.0)
    temperature = t_base + increments

    fit = fit_gdd_jerk(
        temperature,
        latitude,
        min_r_squared=0.999,
    )
    expected_onset = midpoint + EARLY_JERK_LOGIT / rate
    assert fit.r_squared > 0.999999
    assert fit.onset_day == pytest.approx(
        expected_onset,
        abs=0.05,
    )


def test_fixed_transition_controller_recovers_phase_slope_and_stopover_sign():
    rows = []
    for i in range(12):
        x = float(i - 6)
        residual = ((i % 3) - 1) * 0.01
        rows.append(
            {
                "individual_id": f"A{i:02d}",
                "origin_phase": x,
                "destination_phase": 3.0 + 0.4 * x + residual,
                "origin_stopover_days": 8.0 - 0.5 * x + residual,
            }
        )
    frame = pd.DataFrame(rows)
    fit = fit_fixed_transition_controller(
        frame,
        origin_phase_column="origin_phase",
        destination_phase_column="destination_phase",
    )
    assert fit.n == 12
    assert fit.n_individuals == 12
    assert fit.lambda_hat == pytest.approx(0.4, abs=0.01)
    assert fit.stopover_slope < 0.0
    assert fit.origin_phase_sd > 0.0


def test_replicate_difference_summary_uses_sqrt_two_sensitivity_scale():
    summary = summarize_replicate_differences(
        [-2.0, 0.0, 2.0, 4.0]
    )
    assert summary.n == 4
    assert summary.mean == pytest.approx(1.0)
    assert summary.median == pytest.approx(1.0)
    assert summary.equal_independent_replicate_error_sd == pytest.approx(
        summary.sample_sd / math.sqrt(2.0)
    )


@pytest.mark.parametrize("latitude", [-91.0, 91.0, float("nan")])
def test_invalid_latitude_is_rejected(latitude):
    with pytest.raises(ValueError):
        latitude_base_temperature(latitude)
