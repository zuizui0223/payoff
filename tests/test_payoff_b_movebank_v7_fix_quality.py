"""Only source-format tests; no route metrics or V7 effects."""
from scripts.payoff_b_movebank_v7_fix_quality import (
    date_utc,parse_coord,audit_gps_rows
)


def test_timezone_aware_utc_and_invalid_dates():
    assert date_utc("2009-04-03T12:04:00Z").year==2009
    assert date_utc("invalid") is None
    assert parse_coord("91",90) is None
    assert parse_coord("11.5",180)==11.5


def test_one_bird_same_time_is_not_independent_fix():
    rows=[
      {"individual-local-identifier":"A","timestamp":"2009-05-01T00:00:00Z",
       "location-long":"1","location-lat":"55","sensor-type":"GPS"},
      {"individual-local-identifier":"A","timestamp":"2009-05-01T00:00:00Z",
       "location-long":"1.1","location-lat":"55.1","sensor-type":"GPS"},
      {"individual-local-identifier":"B","timestamp":"2009-05-02T00:00:00Z",
       "location-long":"2","location-lat":"56","sensor-type":"GPS"},
    ]
    x=audit_gps_rows(rows,"synthetic")
    assert x["source_all_rows"]==3
    assert x["individual_ids_unique_n"]==2
    assert x["source_valid_unique_gps_fix_n"]==2
    assert x["bad_source_counts"]["duplicate_same_individual_utc_timestamp"]==1
    assert x["independent_30year_predictability_q_from_supplement"] is False
