"""Synthetic high-frequency early/late windows, no bird locations."""
from datetime import datetime,timedelta
from collections import Counter
from scripts.qc_payoff_b_shearwater_two_window_source import (
    two_window_quality,source_summary,utc,MIN_ELIGIBLE_PER_ARM
)

def stamp(hours):
    return datetime(2012,6,10)+timedelta(hours=hours)

def test_continuous_5minute_trace_passes_both_windows():
    pts=[stamp(i/12) for i in range(24*12+1)]
    result=two_window_quality(pts)
    assert result["status"]=="BOTH_12H_WINDOWS_GPS_SOURCE_ADMITTED"
    assert result["cross_12h_boundary_gap_hours"]<1
    assert not result["initial_fix_equals_release_instant_verified"]

def test_sparse_gap_not_a_valid_second_stage():
    times=[stamp(t) for t in (0,1,2,3,4,5,7,8,9,10,11,12,22,23,24)]
    r=two_window_quality(times)
    assert r["status"]!="BOTH_12H_WINDOWS_GPS_SOURCE_ADMITTED"

def test_need_both_12h_windows():
    assert two_window_quality([stamp(i/12) for i in range(130)])["status"]!=\
        "BOTH_12H_WINDOWS_GPS_SOURCE_ADMITTED"

def test_original_sensor_allocation_denominator_preserved():
    assert MIN_ELIGIBLE_PER_ARM==5
    assert utc("2012-06-10T09:00:00+02:00")==datetime(2012,6,10,7)
    groups={"control":8,"magnetic_disruption":9,"olfactory_deprivation":6}
    arms={}
    tracks={}
    for g,n in groups.items():
        for i in range(n):
            identity=g+str(i)
            arms[identity]=g
            tracks[identity]=[stamp(k/12) for k in range(24*12+1)]
    report=source_summary(arms,tracks,Counter())
    assert report["source_gate"]["passed"]
    assert report["original_GPS_equipped"]==27
    assert report["two_observed_windows_total_valid_GPS_subjects"]==23
    assert not report["source_route_correction_or_fitness_effect_fitted"]
    assert "control0" not in str(report)
