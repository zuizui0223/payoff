"""Synthetic tests only. Real animal positions are not fixture data."""
from datetime import date
from scripts.qc_public_movebank_stork_spring_progress_2018 import (
    classify_progression, quantile, summarise_progress,
)


def test_percentile_and_northward_progress_from_synthetic_dates():
    rows = [(date(2014,1,d),10.0) for d in range(1,7)]
    rows += [(date(2014,3,d),10.0+(d-1)*2) for d in range(1,17)]
    r=classify_progression(rows)
    assert r["status"]=="NORTHWARD_PROGRESS_OBSERVED"
    assert r["first_20_percent_doy"] < r["first_80_percent_doy"]
    assert r["twenty_to_eighty_day_span"] > 0
    assert not r["has_breeding_arrival_proof"]


def test_left_censor_is_reported_not_hidden():
    rows=[(date(2014,1,d),10) for d in range(1,7)]
    rows += [(date(2014,3,d),25+d) for d in range(1,17)]
    r=classify_progression(rows)
    assert r["status"]=="SPRING_LEFT_CENSORED"


def test_winter_missing_fails_coverage():
    rows=[(date(2014,3,d),10+d) for d in range(1,14)]
    assert classify_progression(rows)["status"]=="WINTER_DAYS_INSUFFICIENT"


def test_results_aggregate_without_identity_leakage():
    records={
        ("secret-id-A",2014):{
            "status":"NORTHWARD_PROGRESS_OBSERVED",
            "first_20_percent_doy":72,
            "first_80_percent_doy":89,
            "twenty_to_eighty_day_span":17,
            "northing_deg":20,
        },
        ("secret-id-A",2015):{"status":"WINTER_DAYS_INSUFFICIENT"},
    }
    r=summarise_progress(records,{},{"identity_method":"individual-local-identifier"},
                         {("secret-id-A",2014)})
    assert r["success_unique_animal_years"]==1
    assert r["success_with_numeric_fledgling_outcome_available"]==1
    assert "secret-id-A" not in str(r)
    assert not r["reproductive_regression_fitted"]
