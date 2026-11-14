import datetime as dt

import pytest

from src.japan_phenology_environment_gate import ClimateJoinNotAdmitted, validate_environment_panel


def example(year):
    event = dt.date(year, 4, 15)
    return {
        "source_file": "001.csv", "station_id": "401", "year": year,
        "event_date": event.isoformat(), "day_of_year": event.timetuple().tm_yday,
        "rm_original_code": "8", "lat": 45.4, "lon": 141.7,
        "station_location_valid_for_year": True,
        "temperature_window_start": f"{year}-03-01",
        "temperature_window_end": f"{year}-03-30",
        "temperature_mean_c": 2.5, "temperature_valid_days": 30,
        "temperature_expected_days": 30,
        "ndvi_window_start": f"{year}-03-01",
        "ndvi_window_end": f"{year}-03-30",
        "ndvi_qa_valid_fraction": 0.95, "ndvi_value": 0.31,
        "ndvi_product_version": "TEST_ONLY",
        "ndvi_pixel_area_m2": 250000,
        "source_station_metadata_id": "TEST_ONLY",
        "source_temperature_id": "TEST_ONLY",
        "source_ndvi_id": "TEST_ONLY",
    }


def test_admission_is_predictive_only_not_causal():
    rows = [example(y) for y in range(2010, 2015)]
    result = validate_environment_panel(rows)
    assert result["joined_rows"] == 5
    assert result["site_event_series_with_min_years"] == 1
    assert result["causal_information_use_identified"] is False


@pytest.mark.parametrize("field,value", [
    ("station_location_valid_for_year", False),
    ("lat", 10),
    ("source_station_metadata_id", ""),
    ("ndvi_product_version", ""),
    ("ndvi_qa_valid_fraction", 0.4),
    ("ndvi_value", 1.2),
    ("temperature_valid_days", 2),
    ("temperature_window_end", "2010-05-01"),
    ("ndvi_window_end", "2010-05-01"),
    ("temperature_mean_c", float("nan")),
    ("event_date", "2011-04-15"),
    ("temperature_expected_days", 31),
])
def test_invalid_source_or_future_predictors_fail(field, value):
    rows = [example(y) for y in range(2010, 2015)]
    rows[0][field] = value
    with pytest.raises(ClimateJoinNotAdmitted):
        validate_environment_panel(rows)


def test_duplicate_event_key_fails():
    rows = [example(y) for y in range(2010, 2015)]
    rows.append(dict(rows[0]))
    with pytest.raises(ClimateJoinNotAdmitted, match="duplicate"):
        validate_environment_panel(rows)
