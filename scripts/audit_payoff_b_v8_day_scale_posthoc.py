#!/usr/bin/env python3
"""Fail-closed restoration of the 2026-10-05 POSTHOC day-scale V8 audit.

This checks the original, already executed diagnostic on the same 166
environmental pairs and 150 bird exposures. Its estimates are NOT registered
confirmatory hypotheses; LOYO RMSE is not a bird's decision-time forecast.

Expected values and claims are locked independently in Table S2 before this
run. The original R scientific script and preregistered V8 results are unchanged.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

SOURCES=(
    "payoff_b_v8_metric_scale_pairs.csv",
    "payoff_b_v8_metric_scale_summary.csv",
    "payoff_b_v8_metric_scale_forecast_skill_summary.csv",
    "payoff_b_v8_metric_scale_forecast_value_exact_complete.csv",
    "payoff_b_v8_metric_scale_bird_rows.csv",
    "payoff_b_v8_metric_scale_bird_summary.csv",
    "payoff_b_v8_metric_scale_status.csv",
)
EXPECTED={
 "target_sd":(2.412,4.662,2.250,1.946,2.549),
 "slope":(.399,.640,.241,.142,.339),
 "r2":(.290,.572,.282,.234,.330),
 "rmse_in":(1.821,2.494,.673,.460,.891),
 "loo_rmse":(4.113,4.168,.055,-.591,.632),
 "loo_null_rmse":(3.182,5.865,2.683,2.342,3.013),
}
PAIRS=166
BIRD_ROWS=150
BIRD_ENV_PAIRS=72
BIRD_SPECIES=22
SCRIPT_BLOB_SHA="a42b4d9f1a1792d647d6091e980754c428009ce1"


def read_csv(path:Path)->list[dict]:
    with path.open(encoding="utf-8-sig",newline="") as inp:
        z=list(csv.DictReader(inp))
    if not z:
        raise ValueError("Original posthoc output missing or empty: "+str(path))
    return z


def fl(row:dict,key:str)->float:
    try:
        v=float(row[key])
    except (KeyError,ValueError,TypeError) as exc:
        raise ValueError("Missing/non-numeric "+key) from exc
    if not math.isfinite(v):
        raise ValueError("Nonfinite "+key)
    return v


def approx(x:float,expected:float,metric:str,tol:float=.004)->None:
    if abs(x-expected)>tol:
        raise ValueError(f"Historical posthoc {metric} drift: {x} vs {expected}")


def unique(rows,field,count,tag):
    keys=[r[field] for r in rows]
    if len(set(keys))!=count:
        raise ValueError(f"{tag}: expected {count} distinct {field}")
    return keys


def record_key(row,name):
    if name.endswith("_pairs.csv"):
        return row["pair_key"]
    if name.endswith("_bird_rows.csv"):
        return (row["species"],row["target_cell"],row["pair_key"])
    if name.endswith("_summary.csv") and "forecast" not in name:
        return row.get("metric","only_row")
    return "only_row"


def compare_historical(original:Path,replay:Path)->dict:
    hashes={}
    for name in SOURCES:
        a=original/name
        b=replay/name
        old=read_csv(a)
        new=read_csv(b)
        if len(old)!=len(new):
            raise ValueError("Historical day-diagnostic row count drift: "+name)
        if tuple(old[0])!=tuple(new[0]):
            raise ValueError("Historical day-diagnostic schema drift: "+name)
        # Paired row files: compare scientific keys, not CSV row order.
        ok={record_key(r,name):r for r in old}
        nk={record_key(r,name):r for r in new}
        if len(ok)!=len(old) or len(nk)!=len(new) or set(ok)!=set(nk):
            raise ValueError("Historical identity/key membership drift: "+name)
        for k in ok:
            for field in ok[k]:
                av=ok[k][field]
                bv=nk[k][field]
                if av==bv:continue
                if av in ("NA","NaN","") and bv in ("NA","NaN",""):
                    continue
                try:
                    xx=float(av);yy=float(bv)
                    if math.isfinite(xx) and math.isfinite(yy) and abs(xx-yy)<=1e-7:
                        continue
                except (ValueError,TypeError):
                    pass
                raise ValueError(f"Historical output field drift: {name}/{k}/{field}")
        hashes[name]={
            "original_sha256":hashlib.sha256(a.read_bytes()).hexdigest(),
            "rerun_sha256":hashlib.sha256(b.read_bytes()).hexdigest(),
            "rows":len(old),
        }
    return hashes


def audit(original:Path,replay:Path,supplement:Path)->dict:
    original_files=compare_historical(original,replay)
    rows=read_csv(replay/"payoff_b_v8_metric_scale_pairs.csv")
    bird=read_csv(replay/"payoff_b_v8_metric_scale_bird_rows.csv")
    if len(rows)!=PAIRS or len(bird)!=BIRD_ROWS:
        raise ValueError("Registered environmental/bird unit drift")
    unique(rows,"pair_key",PAIRS,"environment")
    unique(bird,"pair_key",BIRD_ENV_PAIRS,"birds")
    unique(bird,"species",BIRD_SPECIES,"birds")
    if max(abs(fl(r,"rho_late")-fl(r,"rho_early")-fl(r,"delta_rho")) for r in rows)>1e-8:
        raise ValueError("Frozen rho arithmetic changed")
    rho_early=sum(fl(r,"rho_early") for r in rows)/PAIRS
    rho_late=sum(fl(r,"rho_late") for r in rows)/PAIRS
    approx(rho_early,.2838,"rho_early")
    approx(rho_late,.6528,"rho_late")

    bymetric={r["metric"]:r for r in read_csv(replay/"payoff_b_v8_metric_scale_summary.csv")}
    if not set(EXPECTED).issubset(bymetric):
        raise ValueError("Old posthoc schema missing SD/slope/RMSE")
    for metric,reference in EXPECTED.items():
        r=bymetric[metric]
        if int(fl(r,"n_pairs"))!=166:
            raise ValueError("Historical scale-summary sampling drift: "+metric)
        cols=("early_pair_mean","late_pair_mean","late_minus_early",
              "pair_ci_low_95","pair_ci_high_95")
        for name,want in zip(cols,reference):
            approx(fl(r,name),want,metric+"."+name)

    skill=read_csv(replay/"payoff_b_v8_metric_scale_forecast_skill_summary.csv")[0]
    for col,want in (
        ("n_pairs",166),("loo_skill_rmse_early_mean",-.931),
        ("loo_skill_rmse_late_mean",1.697),("delta_loo_skill_rmse_mean",2.628),
        ("rmse_pair_ci_low_95",2.134),("rmse_pair_ci_high_95",3.202),
        ("loo_value_mse_early_mean",-16.094),
        ("loo_value_mse_late_mean",15.987),
        ("delta_loo_value_mse_mean",32.082),
        ("value_pair_ci_low_95",21.040),("value_pair_ci_high_95",46.796)
    ):
        approx(fl(skill,col),want,"skill."+col,.005)

    bc=read_csv(replay/"payoff_b_v8_metric_scale_bird_summary.csv")[0]
    for col,want in (
        ("n_rows",150),("n_pairs",72),("n_species",22),
        ("abs_days_early_unweighted",8.418),
        ("abs_days_late_unweighted",8.066),
        ("delta_abs_days_unweighted",-.352),
        ("delta_abs_days_unweighted_ci_low_95",-.890),
        ("delta_abs_days_unweighted_ci_high_95",.200),
        ("delta_abs_days_equal_species",-.627),
        ("delta_abs_days_equal_species_ci_low_95",-1.147),
        ("delta_abs_days_equal_species_ci_high_95",-.018),
    ):
        approx(fl(bc,col),want,"bird."+col,.005)

    status=read_csv(replay/"payoff_b_v8_metric_scale_status.csv")[0]
    if status.get("diagnostic_status")!="POSTHOC_OUTCOME_INFORMED":
        raise ValueError("Missing explicit nonconfirmatory analysis status")
    if abs(fl(status,"rho_reconstruction_max_abs_diff_early"))>1e-10 or abs(fl(status,"rho_reconstruction_max_abs_diff_late"))>1e-10:
        raise ValueError("Registered rho reconstruction changed")

    text=supplement.read_text(encoding="utf-8")
    if "POST HOC" not in text or "LOYO" not in text or "−0.591" not in text or "2.628" not in text:
        raise ValueError("Missing transparent posthoc or negative-outcome text from supplement")
    if "A negative direct RMSE-to-mismatch transfer has not been established" not in text:
        raise ValueError("Supplement falsely promotes untested transfer")

    return {
        "status":"ORIGINAL_V8_DAY_SCALE_POSTHOC_REEXECUTED_AND_SOURCE_MATCHED",
        "original_diagnostic_script_git_blob_sha":SCRIPT_BLOB_SHA,
        "source_early_rho":rho_early,
        "source_late_rho":rho_late,
        "pairs":PAIRS,
        "bird_rows":BIRD_ROWS,
        "bird_unique_pairs":BIRD_ENV_PAIRS,
        "bird_species":BIRD_SPECIES,
        "original_vs_new_file_checksums":original_files,
        "summary_results":{metric:{
            "early":fl(bymetric[metric],"early_pair_mean"),
            "late":fl(bymetric[metric],"late_pair_mean"),
            "change":fl(bymetric[metric],"late_minus_early"),
            "pair_boot_ci95":[fl(bymetric[metric],"pair_ci_low_95"),
                              fl(bymetric[metric],"pair_ci_high_95")],
        } for metric in EXPECTED},
        "loo_rmse_skill_change":fl(skill,"delta_loo_skill_rmse_mean"),
        "loo_squared_value_change":fl(skill,"delta_loo_value_mse_mean"),
        "bird_absolute_mismatch_change_days":fl(bc,"delta_abs_days_unweighted"),
        "classification":"POSTHOC_OUTCOME_INFORMED_ONLY",
        "rmse_change_to_bird_mismatch_direct_transfer_tested":False,
        "registered_primary_v8_modified":False,
        "animal_perception_fitness_identified":False,
        "manuscript_submission_ready":False,
    }


def main()->None:
    p=argparse.ArgumentParser()
    p.add_argument("--historical",type=Path,required=True)
    p.add_argument("--rerun",type=Path,required=True)
    p.add_argument("--supplement",type=Path,required=True)
    p.add_argument("--receipt",type=Path,required=True)
    args=p.parse_args()
    value=audit(args.historical,args.rerun,args.supplement)
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:value[k] for k in ("status","pairs","bird_rows",
                "loo_rmse_skill_change","loo_squared_value_change",
                "rmse_change_to_bird_mismatch_direct_transfer_tested")},
                ensure_ascii=False))


if __name__=="__main__":
    main()
