"""Synthetic continuous GPS within-outside crossing, no bird locations."""
from datetime import date,datetime,timedelta
from scripts.qc_payoff_b_vulture_continuous_exit import (
    assessment,diagnostic,normalize_utc,DISTANCE_KM
)

def time(h,minutes=0):
    return datetime(2015,4,15,h,minutes)

def test_earlier_within_day_crossing_is_measured_not_fabricated_16h():
    anchor=date(2015,4,15)
    # Latitude ~0.5° north equals >30km from site at 20°N.
    fixes=[
        (time(7),20.,10.),(time(8),20.,10.),
        (time(10),20.5,10.),
        (time(11),20.6,10.),
        (time(19),21.1,10.),
        (datetime(2015,4,16,8),22.5,10.),
    ]
    a=assessment(fixes,(20.,10.),anchor)
    assert a["status"]=="AT_LEAST_ONE_SOURCE_GPS_THRESHOLD_CROSSING"
    assert a["raw"]["width_hours"]==2
    assert a["raw"]["early_on_anchor_day"]
    assert a["sustained"] is not None
    assert a["sustained"]["width_hours"]==2
    assert a["raw"]["status"]=="SAMPLED_12H_OUTSIDE"

def test_early_return_not_presented_as_sustained_stopover_departure():
    a=assessment([
        (time(7),20.,10.),(time(10),20.5,10.),
        (time(11),20.,10.),(time(19),20.,10.),
    ],(20.,10.),date(2015,4,15))
    assert a["raw"]["status"]=="OBSERVED_RETURN_WITHIN_12H"
    assert a["sustained"] is None
    assert a["n_candidates_with_sampled_return"]==1

def test_no_observed_crossing_is_not_a_decision_time():
    a=assessment([(time(7),20.,10.),(time(9),20.,10.)],
                 (20.,10.),date(2015,4,15))
    assert a["status"]=="NO_INSIDE_OUTSIDE_CROSSING_IN_LOCKED_48H_WINDOW"
    assert a["raw"] is None

def test_original_source_gate_only_aggregate_and_old_receipt_kept():
    anchor=date(2015,4,15)
    key=("Neophron percnopterus","private-id",2015)
    selected={key:(anchor,(20.,10.),None,None)}
    fixes={key:[(time(7),20.,10.),(time(10),20.5,10.),
                (time(18),20.7,10.),(time(19),21.,10.)]}
    original={key:{"status":"BRACKET_WITHIN_24H","hours":16.0}}
    d=diagnostic(selected,fixes,original)
    assert d["new_raw_fix_to_fix_brackets_under_hours"]["3"]==1
    assert d["old_bracket_under24h_width_summary"]["median"]==16
    assert d["GPS_position_crossing_equals_true_behavioral_departure"] is False
    assert "private-id" not in str(d)

def test_timestamp_timezone_normalization_is_consistent():
    out=normalize_utc("2015-04-15 11:00:00+02:00")
    assert out==datetime(2015,4,15,9)
    assert DISTANCE_KM==30.0
