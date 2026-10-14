#!/usr/bin/env python3
"""Validate independent mule-deer SOURCE-DATA reanalysis against frozen results.

The Ortega et al. 2023 source XLSX is a published-source benchmark, not new
biological discovery. No test here identifies latent animal information,
causal fitness costs, or a readiness-gated timing controller.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

EXPECTED_SHA="2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364"
FILES={
    "phase":("frozen_variance.json","reproduced_variance.json"),
    "readiness":("frozen_readiness.json","reproduced_readiness.json"),
    "channels":("frozen_channels.json","reproduced_channels.json"),
}
CHECKS={
    "phase":[
        "phase.n","phase.variance_ratio_end_over_start",
        "phase.within_year_variance_ratio","phase.mean_abs_start","phase.mean_abs_end",
        "phase.closer_to_peak_n","bootstrap.unique_animals",
        "bootstrap.variance_ratio_ci95","bootstrap.within_year_variance_ratio_ci95",
        "actuators.movement_rate_slope_per_DFP_day",
        "actuators.stopover_slope_days_per_DFP_day",
        "actuators.movement_rate_within_year_slope",
        "actuators.stopover_within_year_slope",
        "bootstrap.movement_rate_slope_ci95",
        "bootstrap.stopover_slope_ci95",
    ],
    "readiness":[
        "schema.readiness_rows_with_joinable_fat_and_timing",
        "schema.temporally_safe_rows","safe_primary.n",
        "safe_primary.animals","safe_primary.slope_std_start_per_scaledIFBFat",
        "safe_cluster_bootstrap.unique_animals",
        "safe_cluster_bootstrap.slope_ci95",
    ],
    "channels":[
        "safe_joined_rows","safe_animals","movement_rate.n",
        "movement_rate.raw.beta_DFP_Start",
        "movement_rate.raw.beta_scaledIFBFat",
        "movement_rate.raw_ci95.beta_DFP_Start",
        "stopover.n","stopover.animals",
        "stopover.raw.beta_DFP_Start",
        "stopover.raw_ci95.beta_DFP_Start",
    ],
}


def path_value(obj:dict,path:str):
    for segment in path.split("."):
        obj=obj[segment]
    return obj


def close_value(a,b,key):
    if isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b):
            raise ValueError("List length mismatch "+key)
        for i,(x,y) in enumerate(zip(a,b)):
            close_value(x,y,key+"["+str(i)+"]")
    elif isinstance(a,(int,float)) and isinstance(b,(int,float)):
        if not (math.isfinite(float(a)) and math.isfinite(float(b))):
            raise ValueError("Nonfinite source value "+key)
        if abs(float(a)-float(b))>max(1e-6,abs(float(a))*1e-7):
            raise ValueError(f"Original paper source reproduction differs at {key}: {a} vs {b}")
    elif a!=b:
        raise ValueError(f"Frozen source value mismatch: {key}: {a} vs {b}")


def audit(source:Path,freeze:Path,replayed:Path)->dict:
    raw=source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA:
        raise ValueError("2023 published Source Data XLSX SHA256 drift")
    result={"status":"MULE_DEER_PUBLISHED_SOURCE_REPRODUCTION_PASS",
            "source_sha256":EXPECTED_SHA,"checks":{},
            "frozen_result_support_changed":False,
            "new_hypothesis_fitted":False,
            "causal_fitness_inference":False,
            "molecular_clock_identified":False,
            "journal_submission_ready":False}
    for group,(baseline_name,new_name) in FILES.items():
        a=json.loads((freeze/baseline_name).read_text(encoding="utf-8"))
        b=json.loads((replayed/new_name).read_text(encoding="utf-8"))
        for path in CHECKS[group]:
            close_value(path_value(a,path),path_value(b,path),group+"."+path)
        result["checks"][group]=len(CHECKS[group])
    # A temporary-safe March body-fat measure is NOT a molecular clock.
    channels=json.loads((replayed/FILES["channels"][1]).read_text(encoding="utf-8"))
    if int(channels["safe_joined_rows"])!=62:
        raise ValueError("Unsafe March-migration sample drift")
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--frozen",type=Path,required=True)
    p.add_argument("--replayed",type=Path,required=True)
    p.add_argument("--receipt",type=Path,required=True)
    x=p.parse_args()
    r=audit(x.source,x.frozen,x.replayed)
    x.receipt.parent.mkdir(parents=True,exist_ok=True)
    x.receipt.write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(r))


if __name__=="__main__":
    main()
