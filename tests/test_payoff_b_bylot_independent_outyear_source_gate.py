"""Source calendar overlap and terms access gate, not observed goose results."""
import json
from copy import deepcopy
from scripts.payoff_b_bylot_independent_outyear_source_gate import (
    MANIFEST, source_calendar_gate
)

def original():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))

def test_nominal_year_overlap_and_historical_prior_art():
    x=source_calendar_gate(original())
    assert x["historical_calendar_overlap_n"]==22
    assert x["historical_calendar_overlap_years"]==list(range(1994,2016))
    assert x["post_2015_calendar_overlap_years"]==[2016,2017,2018,2019,2022,2023]
    assert x["post_2015_nominal_max_n"]==6
    assert x["registered_strong_outyear_gate"]=="FAIL_MAX_6_YEARS_LESS_THAN_10"
    assert x["new_focal_biological_effect"]=="NOT_FITTED"

def test_year_overlap_cannot_be_represented_as_individual_data():
    x=source_calendar_gate(original())
    assert x["original_nest_visits_vs_GPS_overlap_years_only"]==[2019]
    assert x["original_nest_summary_vs_GPS_overlap_years_only"]==[2019,2022,2023]
    assert x["individual_GPS_to_nest_join_admitted"] is False
    assert x["actual_annual_laying_outcomes_opened"] is False
    assert x["actual_predecision_weather_data_opened"] is False
    assert x["breeding_temperature_observed_by_migrants_before_decision"] is False

def test_missing_observations_are_not_imputed():
    x=source_calendar_gate(original())
    for y in (2020,2021,2024,2025):
        assert y not in x["post_2015_calendar_overlap_years"]

def test_source_identity_or_analysis_threshold_cannot_be_retuned():
    base=original()
    from pytest import raises
    invalid=deepcopy(base)
    invalid["source_roles"][0]["version"]="1.1"
    with raises(ValueError,match="Frozen source identity"):
        source_calendar_gate(invalid)
    invalid=deepcopy(base)
    invalid["eligibility_contract"]["minimum_independent_post_2015_holdout_years"]=5
    with raises(ValueError,match="threshold"):
        source_calendar_gate(invalid)
    invalid=deepcopy(base)
    invalid["eligibility_contract"]["fixed_pre_egg_temperature_window"]="June 1–15"
    with raises(ValueError,match="Temporal cue"):
        source_calendar_gate(invalid)

def test_access_receipt_and_SHA_cannot_be_fabricated():
    from pytest import raises
    d=original()
    d["source_roles"][0]["original_bytes_sha256"]="f"*64
    with raises(ValueError,match="SHA256"):
        source_calendar_gate(d)
    d=original()
    d["source_admission"]["gps_original_bytes_permission_confirmed"]=True
    with raises(ValueError,match="Access"):
        source_calendar_gate(d)
