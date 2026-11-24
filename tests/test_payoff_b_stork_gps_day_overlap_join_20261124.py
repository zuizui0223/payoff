"""Pure synthetic day-coverage joins; no raw original bird/location data."""
from copy import deepcopy
import json
import pytest

from scripts import payoff_b_stork_gps_day_overlap_join_20261124 as j

COHORTS=["control","delayed","naturally_timed"]


def c():
    return {"expected_cohorts":COHORTS,"verified_source_required":{
        "status":"ORIGINAL_CC0_GPS_SINGLE_ARCHIVE_UTC_DATE_SUPPORT_VERIFIED",
        "full_original_zip_md5_source_verified":True,
        "original_main_zip_member_CRC_read_through_EOF":True,
        "n_valid_georeferenced_event_rows_min":1,
        "source_GPS_raw_file_committed":False,
        "source_event_values_exported":False,
        "not_full_study_coverage":True,
        "no_ebird":True
    }}


def fake(cohort,day_specs):
    # tuples (UTC day, n valid rows, distinct tags)
    summary={}
    for day,count,tags in day_specs:
        year=int(day[:4])
        x=summary.setdefault(year,{"events":0,"days":0,"two_tags":0})
        x["events"]+=count;x["days"]+=1;x["two_tags"]+=int(tags>=2)
    return {
      "cohort":cohort,
      "status":"ORIGINAL_CC0_GPS_SINGLE_ARCHIVE_UTC_DATE_SUPPORT_VERIFIED",
      "full_original_zip_md5_source_verified":True,
      "original_main_zip_member_CRC_read_through_EOF":True,
      "source_GPS_raw_file_committed":False,
      "source_event_values_exported":False,
      "not_full_study_coverage":True,
      "no_ebird":True,
      "source_contract_sha256":"f"*64,
      "header_source_receipt_sha256":"b"*64,
      "n_valid_georeferenced_event_rows":sum(v[1] for v in day_specs),
      "n_distinct_UTC_dates_with_valid_events":len(day_specs),
      "daily_aggregate_only":[{"UTC_date":d,"n_valid_georeferenced_event_rows":n,
                                "n_distinct_observed_tag_strings":k}
                              for d,n,k in day_specs],
      "yearly_aggregate":[
        {"year":yr,
         "n_valid_georeferenced_events":v["events"],
         "n_UTC_dates_with_georeferenced_events":v["days"],
         "n_UTC_dates_with_at_least_two_tag_strings":v["two_tags"]}
         for yr,v in sorted(summary.items())
      ],
    }


def fixture():
    return {
      "control":fake("control",[("2020-09-01",3,2),("2020-09-02",2,1)]),
      "delayed":fake("delayed",[("2020-09-01",2,1),("2020-09-03",2,2)]),
      "naturally_timed":fake("naturally_timed",[("2020-09-01",10,3),
                                             ("2021-09-01",8,4)]),
    }


def test_triple_and_pairwise_same_day_coverage_not_cue_or_colocation():
    r=j.derived_overlap(fixture(),c())
    assert r["status"]=="DERIVED_COHORT_UTC_DAY_SOURCE_OVERLAP_NOT_COLOCATION"
    assert r["n_UTC_days_in_all_three_selected_ZIPs"]==1
    assert r["n_UTC_days_with_any_selected_ZIP_data"]==4
    assert all(x["n_exact_UTC_days_with_observations_in_both_selected_archives"]==1
               for x in r["pairwise_same_day_observation_support"])
    assert r["within_group_same_day_two_tag_support"]=={
        "control":1,"delayed":1,"naturally_timed":2
    }
    assert r["UTC_day_only_no_hour_or_spatial_colocation"] is True
    assert r["animal_id_or_original_event_location_exported"] is False
    assert r["social_contact_information_q_or_recourse_r_estimated"] is False
    assert r["outcome_or_fitness_model_fitted"] is False


def test_date_duplicate_or_invalid_day_fails_closed():
    data=fixture()
    data["control"]["daily_aggregate_only"].append({
        "UTC_date":"2020-09-01","n_valid_georeferenced_event_rows":1,
        "n_distinct_observed_tag_strings":1
    })
    data["control"]["n_distinct_UTC_dates_with_valid_events"]=3
    with pytest.raises(ValueError,match="Noncanonical or repeated"):
        j.derived_overlap(data,c())
    data=fixture()
    data["control"]["daily_aggregate_only"][0]["UTC_date"]="2020-99-01"
    with pytest.raises(ValueError,match="Invalid source UTC date"):
        j.derived_overlap(data,c())


def test_zip_source_identity_or_same_header_drift_fails_before_join():
    data=fixture()
    data["delayed"]["source_contract_sha256"]="different"
    with pytest.raises(ValueError,match="provenance mismatched"):
        j.derived_overlap(data,c())


def test_reject_daily_year_sum_mismatch():
    data=fixture()
    data["control"]["daily_aggregate_only"][0]["n_valid_georeferenced_event_rows"]=4
    with pytest.raises(ValueError,match="source-event sum"):
        j.derived_overlap(data,c())


def test_missing_a_cohort_is_not_a_negative_observation():
    data=fixture()
    del data["control"]
    with pytest.raises(ValueError,match="Three exact original cohorts"):
        j.derived_overlap(data,c())


def test_source_not_full_archive_collection_remains_explicit():
    data=fixture()
    data["control"]["not_full_study_coverage"]=False
    with pytest.raises(ValueError,match="source gate mismatch"):
        j.derived_overlap(data,c())
