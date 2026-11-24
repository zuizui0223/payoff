#!/usr/bin/env python3
"""Post-open source semantic correction: future deploy-off cannot be observed.

Retains raw 2023 author CC0 reference data privately, preserves original first
receipt, quarantines all end dates later than the fixed 2026-11-24 reference.
This is a source-data diagnostic, NOT a biological intervention/cue analysis.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))
from payoff_b_stork_deployment_time_gate_20261124 import (
    bounded_cc0_csv, read_tag_intervals, compute
)

DEFAULT_CONTRACT=HERE.parent/"data/payoff_b_stork_future_end_date_diagnosis_contract_20261124.json"
ORIGINAL_CONTRACT=HERE.parent/"data/payoff_b_stork_deployment_time_contract_20261124.json"

def quarantine_future_ends(rows,asof):
    changed=[]
    quarantined=0
    for r in rows:
        x=dict(r)
        if x["end"] is not None and x["end"]>asof:
            x["end"]=None
            quarantined+=1
        changed.append(x)
    return changed,quarantined

def source_quality(datasets,original_contract,diagnostic):
    asof=date.fromisoformat(diagnostic["classification"]["reference_day"])
    corrected={}
    counts={}
    for k,raw in datasets.items():
        updated,n=quarantine_future_ends(raw,asof)
        corrected[k]=updated
        counts[k]={"n_original_reference_rows":len(raw),
                   "n_end_dates_after_reference_day":n,
                   "n_end_dates_missing_or_unparseable":sum(r["end"] is None for r in raw),
                   "n_ends_calendar_plausible_after_quarantine":sum(r["end"] is not None for r in updated)}
    if sum(x["n_end_dates_after_reference_day"] for x in counts.values())!=1:
        return {"status":"ORIGINAL_FUTURE_END_SOURCE_SHAPE_CHANGED", "source_quality_by_cohort":counts,
                "overlap_counts":None,
                "original_source_rows_or_tag_ids_exported":False}
    z=compute(corrected,original_contract)
    if z["status"] not in ("TIME_METADATA_BOUNDED_SUPPORT_ONLY","TIME_WINDOW_ENDS_UNOBSERVED"):
        raise ValueError("Corrected source support calculation unexpectedly changed")
    return {
      "status":"POSTOPEN_FUTURE_END_QUARANTINE_COMPLETED_SOURCE_ONLY",
      "original_date_source_status":"TIME_OVERLAP_COUNTS_QUARANTINED_PENDING_FUTURE_END_SEMANTICS",
      "reference_day":asof.isoformat(),
      "source_quality_by_cohort":counts,
      "source_support_after_quarantine":z,
      "total_original_source_rows":sum(len(x) for x in datasets.values()),
      "future_end_is_not_observed":True,
      "even_earlier_end_may_be_scheduled_not_observed":True,
      "actual_spatiotemporal_co_presence_identified":False,
      "same_bird_cross_cohort_tag_join_identified":False,
      "GPS_event_data_opened":False,
      "biological_q_times_recourse_or_fitness_fitted":False,
      "raw_original_tag_ids_or_dates_committed":False,
      "no_ebird":True,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--diagnostic-contract",type=Path,default=DEFAULT_CONTRACT)
    p.add_argument("--original-contract",type=Path,default=ORIGINAL_CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    raw_c=a.diagnostic_contract.read_bytes()
    diagnosis=json.loads(raw_c)
    original=json.loads(a.original_contract.read_text())
    datasets={}
    for cohort,info in original["original_archives"].items():
        payload=bounded_cc0_csv(info,cohort,original)
        datasets[cohort]=read_tag_intervals(payload,info["rows"])
    result=source_quality(datasets,original,diagnosis)
    result.update({
      "original_contract_sha256":sha256(a.original_contract.read_bytes()).hexdigest(),
      "new_postopen_diagnostic_contract_sha256":sha256(raw_c).hexdigest(),
      "source_doi":"10.1098/rspb.2023.1268"
    })
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n")
    print("STORK_FUTURE_END_SOURCE_DIAG="+json.dumps(result,separators=(",",":")))

if __name__=="__main__":
    main()
