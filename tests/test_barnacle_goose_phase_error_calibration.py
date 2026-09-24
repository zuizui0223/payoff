from math import sin, pi

import pytest

pd = pytest.importorskip("pandas")

from src.barnacle_goose_phase_error_calibration import (
    fit_fixed_route_lambda,
    fit_gdd_jerk,
    latitude_base_temperature,
)


def test_latitude_base_temperature_matches_frozen_goose_transform():
    assert latitude_base_temperature(60.0) == pytest.approx(-2.0)


def test_gdd_jerk_fit_returns_finite_spring_onset_for_complete_year():
    # Smooth synthetic seasonal cycle with enough summer heat to accumulate GDD.
    temp = [
        2.0 + 12.0 * sin(2.0 * pi * (day - 90.0) / 365.0)
        for day in range(1, 366)
    ]
    fit = fit_gdd_jerk(
        temp,
        latitude_deg=55.0,
        min_r_squared=0.90,
    )
    assert 1.0 <= fit.onset_day <= 365.0
    assert fit.r_squared >= 0.90


def test_fixed_route_lambda_recovers_exact_slope_with_intercept():
    rows = []
    for animal in range(8):
        for year in (2008, 2009):
            x = float(animal - 4) + (year - 2008) * 0.25
            rows.append(
                {
                    "individual_id": f"A{animal}",
                    "origin": x,
                    "destination": 3.0 + 0.4 * x,
                }
            )
    frame = pd.DataFrame(rows)
    fit = fit_fixed_route_lambda(
        frame,
        origin_phase_column="origin",
        destination_phase_column="destination",
    )
    assert fit.n_pairs == 16
    assert fit.n_individuals == 8
    assert fit.lambda_hat == pytest.approx(0.4)
    assert fit.p_vs_one < 0.05


def test_fixed_route_lambda_rejects_missing_columns():
    with pytest.raises(ValueError, match="missing"):
        fit_fixed_route_lambda(
            pd.DataFrame(
                {
                    "individual_id": ["A", "B", "C"],
                    "origin": [1.0, 2.0, 3.0],
                }
            ),
            origin_phase_column="origin",
            destination_phase_column="destination",
        )
