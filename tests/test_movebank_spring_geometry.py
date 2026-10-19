"""Fixed synthetic northward geometry gates: no natural movement outcomes."""
from datetime import date
from scripts.qc_public_movebank_spring_geometry import analyze_one,summarize

def test_observable_synthetic_northing():
    data=[(date(2020,3,i),5.0+2*i) for i in range(1,21)]
    r=analyze_one(data)
    assert r["status"]=="TWO_NORTHWARD_CHECKPOINTS"
    assert r["interval_days"]>0

def test_left_censor_when_track_starts_after_progress():
    data=[(date(2020,3,i),25.0) for i in range(1,7)]
    data += [(date(2020,3,i),5.0+2*i) for i in range(7,21)]
    result=analyze_one(data)
    assert result["status"] in (
        "LEFT_CENSORED_AT_FIRST_SPRING_OBSERVATION",
        "NET_NORTHWARD_CHANGE_UNRESOLVED")

def test_northing_not_inferred_from_wide_but_round_trip_track():
    data=[(date(2020,3,i),5.0+2*(11-abs(i-11))) for i in range(1,21)]
    r=analyze_one(data)
    assert r["status"]=="NET_NORTHWARD_CHANGE_UNRESOLVED"

def test_all_exclusions_are_reported_no_identity_output():
    p={("Somebird","secretid",2019):
         [(date(2019,3,i),i*2.0) for i in range(1,21)],
       ("Somebird","secretid",2020):
         [(date(2020,3,i),1.0) for i in range(1,21)]}
    r=summarize(p,{}, {}, "individual-local-identifier")
    assert r["all_status_counts"]["LATITUDINAL_RANGE_UNRESOLVED"]==1
    assert r["complete_two_checkpoint_identity_years"]==1
    assert "secretid" not in str(r)
    assert not r["cue_or_actionability_measured"]
