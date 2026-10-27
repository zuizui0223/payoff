"""Original source daily-centroid fixed-anchor position integrity controls."""
from datetime import date,timedelta
from pathlib import Path
import csv
from scripts.qc_payoff_b_riskday_fix_integrity import audit_fixes

def test_daily_centroid_hides_original_boundary_crossing(tmp_path:Path):
    day=date(2015,3,11)
    risk=[
       (("Bird","private",2015),day,(20.,10.),"NORTHWARD_CANDIDATE"),
       (("Bird","private",2015),day-timedelta(days=1),(20.,10.),
        "STAYED_TWO_DAYS")
    ]
    path=tmp_path/"mock.csv"
    fields=["timestamp","individual-local-identifier",
            "individual-taxon-canonical-name","location-lat","location-long"]
    rows=[]
    for d in (day-timedelta(days=3),day-timedelta(days=2),
              day-timedelta(days=1),day):
        rows.extend([
            {"timestamp":d.isoformat()+" 08:00:00",
             "individual-local-identifier":"private","individual-taxon-canonical-name":"Bird",
             "location-lat":"20","location-long":"10"},
            {"timestamp":d.isoformat()+" 13:00:00",
             "individual-local-identifier":"private","individual-taxon-canonical-name":"Bird",
             "location-lat":"20","location-long":"10"}
        ])
    rows.append({"timestamp":day.isoformat()+" 15:00:00",
         "individual-local-identifier":"private","individual-taxon-canonical-name":"Bird",
         "location-lat":"21.0","location-long":"10.0"})
    with path.open("w",newline="") as h:
        w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows)
    result=audit_fixes(path,risk,"Bird")
    src=result["per_prior_riskday_outcome_fix_level_integrity"]
    assert src["NORTHWARD_CANDIDATE"]["final_anchor_day_any_fix_outside"]==1
    assert src["NORTHWARD_CANDIDATE"]["final_anchor_day_last_fix_outside"]==1
    assert src["STAYED_TWO_DAYS"]["final_anchor_day_last_fix_outside"]==0
    assert "private" not in str(result)
    assert result["anchor_fix_level_stable_is_verified_true_stopover"] is False

def test_missing_anchor_day_is_fatal(tmp_path:Path):
    p=tmp_path/"miss.csv"
    p.write_text("timestamp,individual-local-identifier,location-lat,location-long\n"
                 "2015-03-11 12:00:00,p,20,10\n")
    try:
        audit_fixes(p,[(("Bird","p",2015),date(2015,3,11),(20,10),"CENSORED")],"Bird")
        raise AssertionError("Should fail without source geometry")
    except ValueError:pass
