"""Synthetic within-track progress and unknown-outcome bound tests."""
from datetime import datetime,timedelta
from scripts.audit_payoff_b_shearwater_stagewise_progress import (
    km,bound,segment,evaluate
)

def test_geo_and_missing_bounds():
    assert 100<km((42,10),(43,10))<115
    assert km((42,10),(42,10))==0
    assert bound(3,6,14)==[3/14,11/14]
    assert bound(0,0,9)==[0,1]

def test_synthetic_northward_track_progress_within_unit_bound():
    start=datetime(2012,6,1)
    pts=[(start+timedelta(minutes=i*20),(30+i*.06,10)) for i in range(36)]
    r=segment(pts,start,(0,12))
    assert r["status"]=="PROGRESS_CALCULATED"
    assert .9<r["efficiency"]<=1

def test_no_travel_kept_missing_not_binary_nonimprovement():
    start=datetime(2012,6,1)
    pts={start+timedelta(hours=i):(40.,10.) for i in range(25)}
    assert evaluate(pts)["status"]!="BOTH_STAGE_PROGRESS_ESTIMABLE"
