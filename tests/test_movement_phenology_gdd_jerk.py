import math

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("scipy")

from analysis.movement_phenology.gdd_jerk import (
    EARLY_JERK_FRACTION,
    early_jerk_peak_day,
    fit_gdd_jerk,
    growing_degree_days,
    latitude_base_temperature,
    logistic_gdd,
    logistic_third_derivative,
)


def test_latitude_base_temperature_matches_declared_endpoints():
    assert latitude_base_temperature(52) == pytest.approx(0.0)
    assert latitude_base_temperature(72) == pytest.approx(-5.0)


def test_gdu_is_truncated_at_zero():
    gdd = growing_degree_days([-10, 0, 1, 2, 3, 4, 5, 6, 7, 8], 52)
    assert gdd[0] == pytest.approx(0)
    assert np.all(np.diff(gdd) >= 0)


def test_analytic_early_jerk_is_actual_positive_maximum_before_midpoint():
    L, k, t0 = 1000.0, 0.05, 160.0
    t_peak = early_jerk_peak_day(k, t0)
    grid = np.linspace(1, t0, 20000)
    jerk = logistic_third_derivative(grid, L, k, t0)
    t_numeric = float(grid[np.argmax(jerk)])
    assert t_peak == pytest.approx(t_numeric, abs=0.02)

    fitted_fraction = 1 / (1 + math.exp(-k * (t_peak - t0)))
    assert fitted_fraction == pytest.approx(EARLY_JERK_FRACTION)


def test_fit_recovers_synthetic_onset_from_temperature_generated_gdd():
    # Construct daily GDU as differences of an exact logistic cumulative GDD,
    # then convert to temperature by adding the latitude-specific base.
    lat = 65.0
    L, k, t0 = 1400.0, 0.035, 175.0
    days = np.arange(0, 366, dtype=float)
    curve = logistic_gdd(days, L, k, t0)
    increments = np.diff(curve)
    tbase = latitude_base_temperature(lat)
    temp = increments + tbase

    fit = fit_gdd_jerk(temp, lat, min_r_squared=0.999)
    expected = early_jerk_peak_day(k, t0)
    assert fit.onset_day == pytest.approx(expected, abs=0.5)
    assert fit.r_squared > 0.999


def test_low_accumulation_fails_closed():
    with pytest.raises(ValueError):
        fit_gdd_jerk([-20.0] * 365, 78.0)
