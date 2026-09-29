import pytest

from src.greater_snow_goose_climate import (
    CONTEXT_ORDER,
    initial_bearing_deg,
    seasonal_window,
    target_window,
    training_years,
    wind_support_ms,
)


def test_training_window_is_strictly_preoutcome():
    years = training_years(2019)
    assert years[0] == 1999
    assert years[-1] == 2018
    assert len(years) == 20
    assert 2019 not in years


def test_frozen_context_windows():
    assert seasonal_window("southern_staging", 2020)[0].isoformat() == "2020-04-01"
    assert seasonal_window("southern_staging", 2020)[1].isoformat() == "2020-05-15"
    assert seasonal_window("mid_arctic_staging", 2020)[0].isoformat() == "2020-05-10"
    assert seasonal_window("northern_arctic_staging", 2020)[1].isoformat() == "2020-06-05"
    assert target_window(2020)[0].isoformat() == "2020-05-30"
    assert target_window(2020)[1].isoformat() == "2020-06-15"
    assert CONTEXT_ORDER == (
        "southern_staging",
        "mid_arctic_staging",
        "northern_arctic_staging",
    )


def test_initial_bearing_cardinal_cases():
    assert initial_bearing_deg(0, 0, 0, 10) == pytest.approx(0.0)
    assert initial_bearing_deg(0, 0, 10, 0) == pytest.approx(90.0)


def test_wind_support_uses_meteorological_from_direction():
    # Southerly wind blows northward and supports a northbound route.
    assert wind_support_ms(5.0, 180.0, 0.0) == pytest.approx(5.0)
    # Northerly wind opposes the same route.
    assert wind_support_ms(5.0, 0.0, 0.0) == pytest.approx(-5.0)
