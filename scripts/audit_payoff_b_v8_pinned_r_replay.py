#!/usr/bin/env python3
"""Compare fresh frozen-code R replay with separately restored 2026-10-05 rows.

A success proves that the original deterministic pair mapping, species-target
eligibility and key registered row values were independently reproduced using
the pinned raw RDS. Unchanged R source, same data, and different execution
are NOT independent biological validation or a newly proposed hypothesis.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
from pathlib import Path

from scripts.audit_payoff_b_v8_restored_rows import (
    MANIFEST, FILES, audit, load_rows
)


KEYS={
    "environment_pairs":("pair_key",),
    "environment_species":("species",),
    "environment_incidence":("species","pair_key"),
    "transfer_rows":("species","target_cell","pair_key"),
    "structural_rows":("species","target_cell","pair_key"),
}

CRITICAL_NUMERIC={
    "environment_pairs":("rho_early","rho_late","delta_rho"),
    "environment_species":("delta_rho",),
    "transfer_rows":("delta_rho","delta_mismatch","z_delta_rho",
                     "mean_mismatch_early","mean_mismatch_late"),
    "structural_rows":("delta_rho","delta_mismatch","z_delta_rho",
                       "delta_pseudo_mismatch"),
}


def snapshot(rows,keys,role):
    bykey={}
    for r in rows:
        k=tuple(r.get(f) for f in keys)
        if k in bykey:
            raise ValueError(f"Duplicate key in {role}: {k}")
        bykey[k]=r
    return bykey


def compare_archived_rows(original:Path,replay:Path,manifest:dict)->dict:
    # First, independently compare both complete sets to predeclared frozen
    # numerical targets (including three original bootstrap/permutation CIs).
    old_audit=audit(original,manifest)
    new_audit=audit(replay,manifest)
    per_role={}
    for role,keys in KEYS.items():
        subdir,name=FILES[role]
        old=snapshot(load_rows(original/subdir/name),keys,role+"/frozen")
        new=snapshot(load_rows(replay/subdir/name),keys,role+"/replay")
        if set(old)!=set(new):
            missing=sorted(set(old)-set(new))[:3]
            extra=sorted(set(new)-set(old))[:3]
            raise ValueError(
                f"Frozen/replay row membership differs for {role}: missing={missing},extra={extra}"
            )
        max_diff=0.0
        ncomp=0
        for k in old:
            for field in CRITICAL_NUMERIC.get(role,()):
                a=float(old[k][field]);b=float(new[k][field])
                if not all(map(math.isfinite,(a,b))):
                    raise ValueError("Nonfinite replay row")
                max_diff=max(max_diff,abs(a-b))
                ncomp+=1
                if abs(a-b)>1e-8:
                    raise ValueError(f"Replay coefficient row drift in {role}, {k}, {field}: {a} vs {b}")
        per_role[role]={"n_rows":len(old),"compared_numeric_fields":ncomp,
                        "max_abs_numeric_difference":max_diff,
                        "frozen_csv_sha256":hashlib.sha256((original/subdir/name).read_bytes()).hexdigest(),
                        "replay_csv_sha256":hashlib.sha256((replay/subdir/name).read_bytes()).hexdigest()}
    # Bootstraps are checked independently against frozen numerical targets,
    # not required byte-equal across R versions/RNG environments.
    return {
       "status":"FROZEN_V8_PINNED_SOURCE_INDEPENDENT_R_REPLAY_MATCHED",
       "original_20261005_output_status":old_audit["status"],
       "replayed_R_output_status":new_audit["status"],
       "matched_row_results":per_role,
       "environment_replay":new_audit["environment"],
       "transfer_replay":new_audit["transfer"],
       "structural_null_replay":new_audit["structural_null"],
       "original_R_scripts_modified":False,
       "new_hypothesis_fitted":False,
       "independently_ran_original_frozen_R_scripts_from_pinned_source":True,
       "causal_information_use_or_fitness_identified":False,
       "anonymous_reviewer_archive_approved":False,
       "submission_ready":False,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original",type=Path,required=True)
    p.add_argument("--replay",type=Path,required=True)
    p.add_argument("--manifest",type=Path,default=MANIFEST)
    p.add_argument("--receipt",type=Path,required=True)
    args=p.parse_args()
    result=compare_archived_rows(
      args.original,args.replay,json.loads(args.manifest.read_text(encoding="utf-8")))
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
       "status":result["status"],
       "matched_row_results":result["matched_row_results"],
       "submission_ready":False
    },ensure_ascii=False))


if __name__=="__main__":
    main()
