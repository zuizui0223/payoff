from datetime import date, timedelta
from scripts.qc_payoff_b_predecision_candidates import (
    detect_transfer_candidates,source_audit,haversine,
)

def synthetic_track(moving_north=True):
    t=date(2015,3,1)
    coords=[(20,10),(20.02,10.02),(20.01,10.01),
            (20.5,10.5),(21.6,11.2)] if moving_north else [
            (20,10),(20.02,10.02),(20.01,10.01),
            (19.5,10.5),(18.6,11.2)]
    return [(t+timedelta(days=i),a,b) for i,(a,b) in enumerate(coords)]

def test_five_day_departs_north_from_stationary_position():
    windows,d=detect_transfer_candidates(synthetic_track())
    assert windows==1
    assert d==[date(2015,3,3)]
    assert haversine(20,10,21.6,11.2)>120

def test_southward_motion_is_not_northward_departure():
    windows,d=detect_transfer_candidates(synthetic_track(False))
    assert windows==1
    assert not d

def test_sampling_gaps_prevent_fabricating_departure():
    d=synthetic_track()
    d[3]=(d[3][0]+timedelta(days=1),d[3][1],d[3][2])
    n,c=detect_transfer_candidates(d)
    assert n==0 and not c

def test_only_aggregate_results_no_source_coordinates():
    groups={("Bird","secret-identifier",2015):synthetic_track()}
    r=source_audit(groups,{},"individual-local-identifier")
    assert r["total_candidate_events"]==1
    assert r["classified_source_taxa"]["Bird"]["candidate_stationary_to_northward_events"]==1
    assert "secret-identifier" not in str(r)
    assert not r["predecision_weather_joined"]
