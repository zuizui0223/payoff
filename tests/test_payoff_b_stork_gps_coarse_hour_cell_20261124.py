"""Pure synthetic GPS coarse hour/cell support tests. No original event rows."""
from datetime import date,datetime,timezone
import io
import json
import pytest

from scripts import payoff_b_stork_gps_coarse_hour_cell_20261124 as s


COLS=["timestamp","location-lat","location-long",
      "tag-local-identifier","individual-local-identifier","visible"]


def csv_stream(rows):
    import csv
    dst=io.StringIO()
    w=csv.writer(dst)
    w.writerow(COLS)
    w.writerows(rows)
    dst.seek(0)
    return dst


def sample_rows():
    return [
        ["2020-09-10 10:05:00","47.701","8.101","PRIVATE_TAG_A","PRIVATE_BIRD_A","true"],
        ["2020-09-10 10:09:00","47.705","8.102","PRIVATE_TAG_B","PRIVATE_BIRD_B","true"],
        ["2020-09-10 10:11:00","47.704","8.102","PRIVATE_TAG_A","PRIVATE_BIRD_A","true"],
        ["2020-09-10 10:12:00","49.100","9.300","PRIVATE_TAG_C","PRIVATE_BIRD_C","true"],
        ["2020-09-10 11:01:00","47.700","8.100","PRIVATE_TAG_B","PRIVATE_BIRD_B","true"],
        ["2020-09-10 10:13:00","999","9.300","PRIVATE_TAG_C","PRIVATE_BIRD_C","true"],
        ["bad-time","47.700","8.100","PRIVATE_TAG_B","PRIVATE_BIRD_B","true"],
    ]


def test_event_time_UTC_and_fixed_grid_bins_without_distance_claim():
    dt=s.parse_UTC_dt("2020-09-10T23:30:00-02:00",date(2026,11,24))
    assert dt.date()==date(2020,9,11)
    assert dt.hour==1
    assert s.parse_UTC_dt("2040-09-10 08:00:00",date(2026,11,24)) is None
    hour=date(2020,9,10).toordinal()*24+10
    assert s.cell_hour_key(hour,47.701,8.101,10)==s.cell_hour_key(hour,47.705,8.102,10)
    assert s.cell_hour_key(hour,47.701,8.101,10)!=s.cell_hour_key(hour,49.1,9.3,10)
    assert s.cell_hour_key(hour,47.701,8.101,10)!=s.cell_hour_key(hour+1,47.701,8.101,10)


def test_stream_reads_all_synthetic_events_and_retains_only_internal_keys():
    scan=s.source_scan_main_csv(csv_stream(sample_rows()),COLS,date(2026,11,24))
    assert scan["n_raw_rows"]==7
    assert scan["n_valid_georeferenced_rows"]==5
    assert scan["n_unusable_time"]==1
    assert scan["n_unusable_coordinate"]==1
    assert len(scan["day_ordinals"])==1
    assert len(scan["hour_ordinals"])==2
    assert len(scan["cell_hour_keys"][10])==3
    assert len(scan["cell_hour_two_distinct_tag_keys"][10])==1
    assert len(scan["cell_hour_two_distinct_tag_keys"][5])==1
    aggregated=s.one_cohort(scan,"control")
    assert aggregated["n_UTC_hour_0p1_cells_with_at_least_two_tag_strings"]==1
    assert aggregated["no_original_tag_or_coordinate_exported"] is True
    assert "PRIVATE_TAG_A" not in json.dumps(aggregated)
    assert "PRIVATE_BIRD_A" not in json.dumps(aggregated)


def test_cross_cohort_grid_hour_intersection_does_not_claim_contact():
    base=s.source_scan_main_csv(csv_stream(sample_rows()),COLS,date(2026,11,24))
    good=[
        ["2020-09-10 10:07:00","47.704","8.102","PRIVATE_COHORT_D","PRIVATE_D","true"],
    ]
    same=s.source_scan_main_csv(csv_stream(good),COLS,date(2026,11,24))
    other=s.source_scan_main_csv(csv_stream(good),COLS,date(2026,11,24))
    out=s.cross_cohort_support({"control":base,"delayed":same,"naturally_timed":other})
    assert out["three_cohort_aggregate"]["n_common_UTC_hours"]==1
    assert out["three_cohort_aggregate"]["n_same_UTC_hour_and_0p1_degree_cell_keys"]==1
    assert out["three_cohort_aggregate"]["n_same_UTC_hour_and_0p2_degree_cell_keys"]==1
    assert len(out["pairwise_aggregate"])==3
    assert out["pairwise_aggregate"][0]["n_same_UTC_hour_and_0p1_degree_cell_keys"]==1
    assert "PRIVATE" not in json.dumps(out)


def test_source_original_full_scan_counts_must_match_previous_CRC_gate():
    scan=s.source_scan_main_csv(csv_stream(sample_rows()),COLS,date(2026,11,24))
    prev={"n_original_main_member_GPS_CSV_rows":7,
          "n_valid_georeferenced_event_rows":5,
          "n_unusable_timestamp_rows":1,
          "n_unusable_coordinate_rows":1,
          "n_unusable_tag_rows":0,
          "n_distinct_UTC_dates_with_valid_events":1,
          "full_original_zip_md5_source_verified":True,
          "not_full_study_coverage":True}
    s.verify_against_first_pass(scan,prev)
    prev["n_valid_georeferenced_event_rows"]=6
    with pytest.raises(ValueError,match="Original GPS support"):
        s.verify_against_first_pass(scan,prev)


def test_bad_coordinates_and_missing_timestamp_not_promoted():
    stream=csv_stream([
       ["","47.7","8.1","TAG","ANIMAL","true"],
       ["2020-09-10 10:00:00","-95","8.1","TAG","ANIMAL","true"],
       ["2020-09-10 10:00:00","47.7","8.1","TAG","ANIMAL","true"],
    ])
    z=s.source_scan_main_csv(stream,COLS,date(2026,11,24))
    assert z["n_raw_rows"]==3
    assert z["n_unusable_time"]==1
    assert z["n_unusable_coordinate"]==1
    assert z["n_valid_georeferenced_rows"]==1
    assert len(z["cell_hour_keys"][10])==1


def test_unregistered_source_cohort_cannot_gain_fake_cross_cohort_support():
    base=s.source_scan_main_csv(csv_stream(sample_rows()),COLS,date(2026,11,24))
    with pytest.raises(ValueError,match="Exactly three"):
        s.cross_cohort_support({"control":base,"delayed":base})
