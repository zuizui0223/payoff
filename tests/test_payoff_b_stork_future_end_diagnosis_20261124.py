"""Source-specific post-open future deployment-off correction is separate from original."""
from datetime import date
from scripts import payoff_b_stork_future_end_diagnosis_20261124 as q

def original():
    return {
      "control":[{"tag":"PRIVATE_C1","start":date(2019,9,1),"end":date(2019,11,1)},
                 {"tag":"PRIVATE_C2","start":date(2019,9,10),"end":None}],
      "delayed":[{"tag":"PRIVATE_D1","start":date(2019,9,10),"end":date(2030,1,1)},
                 {"tag":"PRIVATE_D2","start":date(2019,9,1),"end":date(2020,1,1)}],
      "naturally_timed":[{"tag":"PRIVATE_N1","start":date(2020,9,1),"end":date(2021,9,1)},
                        {"tag":"PRIVATE_N2","start":date(2020,9,1),"end":date(2020,10,1)}],
    }

def contract():
    return {
      "original_archives":{"control":{"rows":2},"delayed":{"rows":2},"naturally_timed":{"rows":2}},
    }

def diagnosis():
    return {"classification":{"reference_day":"2026-11-24"}}

def test_only_future_end_is_unbounded_not_imputed_to_today():
    rows=original()["delayed"]
    corrected,n=q.quarantine_future_ends(rows,date(2026,11,24))
    assert n==1
    assert corrected[0]["end"] is None
    assert corrected[1]["end"]==date(2020,1,1)
    assert rows[0]["end"]==date(2030,1,1)

def test_future_end_detection_and_no_raw_ids():
    z=q.source_quality(original(),contract(),diagnosis())
    assert z["status"]=="POSTOPEN_FUTURE_END_QUARANTINE_COMPLETED_SOURCE_ONLY"
    assert z["source_quality_by_cohort"]["delayed"]["n_end_dates_after_reference_day"]==1
    assert z["source_quality_by_cohort"]["delayed"]["n_ends_calendar_plausible_after_quarantine"]==1
    assert z["future_end_is_not_observed"] is True
    assert z["actual_spatiotemporal_co_presence_identified"] is False
    assert "PRIVATE_C1" not in str(z)
    assert "PRIVATE_D1" not in str(z)
    assert z["no_ebird"] is True

def test_source_shape_change_closes_overlap_gate():
    rows=original()
    rows["control"][0]["end"]=date(2030,1,1)
    z=q.source_quality(rows,contract(),diagnosis())
    assert z["status"]=="ORIGINAL_FUTURE_END_SOURCE_SHAPE_CHANGED"
    assert z["overlap_counts"] is None
