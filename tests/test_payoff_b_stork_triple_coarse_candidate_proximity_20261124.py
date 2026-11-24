"""Synthetic original-GPS triplet-only proximity gates, no source animal rows."""
from datetime import date
import csv
import io
from math import isclose
import pytest

from scripts import payoff_b_stork_triple_coarse_candidate_proximity_20261124 as g
from scripts.payoff_b_stork_gps_coarse_hour_cell_20261124 import cell_hour_key

def v(t,lat=50.0,lon=10.0):
    return (float(t),lat,lon)

def cfg():
    return {"privacy":{
        "max_stored_candidate_event_fixes_per_cohort":50000,
        "max_fixes_per_candidate_key_per_cohort":10000
    }}

def fake_stream(rows):
    headers=("timestamp","tag-local-identifier","location-lat","location-long")
    out=io.StringIO()
    writer=csv.DictWriter(out,fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
    out.seek(0)
    return out, list(headers)


def test_three_source_actual_fix_candidates_not_merely_coarse_bins():
    a=v(1000.0,50.0000,10.0000)
    b=v(1010.0,50.0010,10.0000)
    c=v(1200.0,50.0002,10.0010)
    assert g.exactly_one_triplet([[a],[b],[c]],300,1000) is True
    assert g.exactly_one_triplet([[a],[b],[v(1350.0,50.0002,10.0010)]],300,1000) is False
    assert g.exactly_one_triplet([[a],[b],[v(1200.0,50.15,10.0010)]],300,1000) is False
    assert g.exactly_one_triplet([[a],[b],[v(1600.0,50.15,10.0010)]],900,5000) is False
    assert g.exactly_one_triplet([[a],[b],[]],300,1000) is False


def test_global_triplet_time_span_not_only_pairwise_distance():
    # A-B are 300 s apart, C is within 300 s of each separately only if
    # C resides between them. A point 100 s before A is 400 s before B.
    a=v(0)
    b=v(300)
    c=v(-100)
    assert g.exactly_one_triplet([[a],[b],[c]],300,1000) is False


def test_haversine_spatial_distance_true_metric_not_angular_width():
    assert isclose(g.haversine_meters(v(0,0,0),v(0,0,0)),0.0)
    assert 1000 < g.haversine_meters(v(0,0,0),v(0,0.01,0)) < 1200
    assert g.haversine_meters(v(0,52,0),v(0,52,0.01)) < 1000


def test_UTC_hour_coarse_candidate_collection_drops_noncandidate_values_and_ids():
    stamp="2020-06-01 12:03:00"
    fake,outnames=fake_stream([
        {"timestamp":stamp,"tag-local-identifier":"PRIVATE_STORK_ONE",
         "location-lat":"50.0001","location-long":"10.0001"},
        {"timestamp":"2020-06-01 12:04:00","tag-local-identifier":"PRIVATE_STORK_TWO",
         "location-lat":"50.0002","location-long":"10.0002"},
        {"timestamp":"2020-06-01 14:00:00","tag-local-identifier":"PRIVATE_STORK_THREE",
         "location-lat":"50.0001","location-long":"10.0001"},
    ])
    from scripts.payoff_b_stork_gps_coarse_hour_cell_20261124 import parse_UTC_dt
    dt=parse_UTC_dt(stamp,date(2026,11,24))
    hour=dt.date().toordinal()*24+dt.hour
    candidates={
      10:{cell_hour_key(hour,50.0001,10.0001,10)},
      5:{cell_hour_key(hour,50.0001,10.0001,5)}
    }
    ret=g.collect_fixes(fake,outnames,date(2026,11,24),candidates,cfg())
    assert sum(map(len,ret[10].values()))==2
    assert sum(map(len,ret[5].values()))==2
    assert "PRIVATE_STORK" not in str(ret)
    # Point values stay only inside test process, NEVER in aggregate output.


def test_frozen_candidate_privacy_cap_fail_closed():
    stamp="2020-06-01 12:03:00"
    fake,header=fake_stream([{
      "timestamp":stamp,"tag-local-identifier":"TAG",
      "location-lat":"50.1","location-long":"10.1"
    }])
    from scripts.payoff_b_stork_gps_coarse_hour_cell_20261124 import parse_UTC_dt
    dt=parse_UTC_dt(stamp,date(2026,11,24))
    h=dt.date().toordinal()*24+dt.hour
    keys={10:{cell_hour_key(h,50.1,10.1,10)},5:{cell_hour_key(h,50.1,10.1,5)}}
    strict={"privacy":{
       "max_stored_candidate_event_fixes_per_cohort":1,
       "max_fixes_per_candidate_key_per_cohort":10000
    }}
    with pytest.raises(ValueError,match="privacy cap"):
        g.collect_fixes(fake,header,date(2026,11,24),keys,strict)


def test_source_claim_contract_is_postopen_and_not_information_effect():
    import json
    c=json.loads(g.CONTRACT.read_text())
    assert c["stage"].startswith("POST_OPEN")
    assert c["candidate_expected_counts"]=={"0p1_degree":11,"0p2_degree":16}
    assert c["estimands"][0]["max_three_fix_time_span_seconds"]==300
    assert c["estimands"][0]["max_three_pairwise_haversine_metres"]==1000
    assert c["privacy"]["no_source_event_rows_export"] is True
    assert c["no_biological_causal_model"] is True
    assert c["no_ebird"] is True
