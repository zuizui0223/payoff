"""Chronology gate uses original UTC issue timestamps, not later analyses."""
from copy import deepcopy

import pytest

from scripts.payoff_b_ruppel_GFS_issued_forecast_gate import (
    admission, utc_instant, test_future_issue_time_record as check_issued
)


def sample():
    return {
        "decision_utc":"2020-09-16T19:00:00Z",
        "forecast_issue_utc":"2020-09-16T12:00:00Z",
        "forecast_valid_utc":"2020-09-17T00:00:00Z",
        "original_forecast_product":"operational_issue_time_forecast",
        "original_operational_archive":"d084001",
        "original_GRIB2_file_sha256":"a"*64,
    }


def test_genuine_prior_issue_and_future_valid_time_are_distinct():
    result=check_issued(sample())
    assert result["issued_at_least_1h_predecision"]
    assert result["valid_after_decision"]
    assert result["positive_model_forecast_lead"]
    assert result["decision_to_target_near_primary_plus6h"]
    assert result["animal_subjective_access_verified"] is False


def test_future_issued_forecast_fails_decision_access_not_reclassified():
    r=sample()
    # GFS initializations occur at fixed UTC hours. To check the 1-hour
    # buffer, change the bird's decision time instead of inventing a GFS run
    # initialized at 18:30 UTC.
    r["decision_utc"]="2020-09-16T18:30:00Z"
    r["forecast_issue_utc"]="2020-09-16T18:00:00Z"
    x=check_issued(r)
    assert x["issued_at_least_1h_predecision"] is False
    r["forecast_issue_utc"]="2020-09-16T12:00:00Z"
    assert check_issued(r)["issued_at_least_1h_predecision"] is True


def test_nowcast_or_weather_after_decision_cannot_fake_future_cue():
    r=sample()
    r["original_forecast_product"]="ERA5_hindcast"
    with pytest.raises(ValueError,match="not eligible"):
        check_issued(r)
    r=sample()
    r["forecast_valid_utc"]="2020-09-16T18:00:00Z"
    assert not check_issued(r)["valid_after_decision"]
    assert not check_issued(r)["decision_to_target_near_primary_plus6h"]


def test_naive_local_datetime_or_other_year_or_source_is_not_admitted():
    r=sample()
    r["forecast_issue_utc"]="2020-09-16T12:00"
    with pytest.raises(ValueError,match="UTC"):
        check_issued(r)
    r=sample()
    r["decision_utc"]="2026-09-16T19:00:00Z"
    with pytest.raises(ValueError,match="study years"):
        check_issued(r)
    r=sample()
    r["original_operational_archive"]="ERA5"
    with pytest.raises(ValueError,match="original historical GFS"):
        check_issued(r)


def test_metadata_gate_does_not_fake_user_login_or_original_bytes():
    import json
    from scripts.payoff_b_ruppel_GFS_issued_forecast_gate import CONTRACT
    manifest=json.loads(CONTRACT.read_text(encoding="utf-8"))
    x=admission(manifest)
    assert x["original_forecast_issued_values_obtained"] is False
    assert x["future_user_authorized_GRIB2_admission_needed"] is True
    assert x["bird_cue_vs_landing_biological_effect_fitted"] is False
    bad=deepcopy(manifest)
    bad["external_forecast_archive"]["original_file_sha256_checked"]=True
    with pytest.raises(ValueError,match="source access"):
        admission(bad)
