"""Post-outcome S3 integrity: exact six fitted and spatial sensitivity outputs.

No biological mechanism or preregistered hypothesis is inferred. Re-run
outputs must numerically match the original immutable source-workflow CSVs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

SIX_FILES={
    "day_metric_to_bird_exploratory_slopes.csv":6,
    "day_metric_to_bird_exploratory_joined_rows.csv":150,
    "day_metric_to_bird_exploratory_bootstrap.csv":10000,
    "day_metric_to_bird_exploratory_status.csv":1,
}
SPATIAL_FILES={
    "spatial_sensitivity_all_24_intervals.csv":24,
    "spatial_sensitivity_scheme_status.csv":4,
    "leave_one_unit_out_all_564_slopes.csv":564,
    "leave_one_unit_out_summary.csv":12,
    "bootstrap_source_cell_10000.csv":10000,
    "bootstrap_target_cell_10000.csv":10000,
    "bootstrap_target_grid_5deg_10000.csv":10000,
    "bootstrap_target_grid_10deg_10000.csv":10000,
}


def rows(file:Path)->list[dict[str,str]]:
    with file.open(encoding="utf-8-sig",newline="") as handle:
        reader=csv.DictReader(handle)
        result=list(reader)
    if not result or reader.fieldnames is None:
        raise ValueError(f"Empty/missing original CSV: {file}")
    if len(set(reader.fieldnames))!=len(reader.fieldnames):
        raise ValueError(f"Duplicate CSV schema: {file}")
    return result


def same_value(a:str,b:str,name:str):
    if a==b or (a in ("NA","NaN","") and b in ("NA","NaN","")):
        return
    try:
        x=float(a);y=float(b)
    except (TypeError,ValueError):
        raise ValueError("Non-numeric source scientific field drift: "+name)
    if not (math.isfinite(x) and math.isfinite(y)) or abs(x-y)>1e-7:
        raise ValueError(f"Numerical source-vs-replay drift {name}: {a} vs {b}")


def compare_group(origin:Path,replay:Path,registered:dict[str,int])->dict:
    output={}
    for name,expected in registered.items():
        f1=origin/name
        f2=replay/name
        x=rows(f1);y=rows(f2)
        if len(x)!=expected or len(y)!=expected:
            raise ValueError(f"Original/replay row count drift for {name}")
        if tuple(x[0])!=tuple(y[0]):
            raise ValueError(f"Source schema drift in {name}")
        for j,(old,new) in enumerate(zip(x,y)):
            for k in old:
                same_value(old[k],new.get(k),f"{name}:{j}:{k}")
        output[name]={
            "source_sha256":hashlib.sha256(f1.read_bytes()).hexdigest(),
            "replay_sha256":hashlib.sha256(f2.read_bytes()).hexdigest(),
            "verified_rows":expected,
        }
    return output


def check(original_six:Path,original_spatial:Path,
          replay_six:Path,replay_spatial:Path)->dict:
    summary=compare_group(original_six,replay_six,SIX_FILES)
    geo=compare_group(original_spatial,replay_spatial,SPATIAL_FILES)
    sl=rows(replay_six/"day_metric_to_bird_exploratory_slopes.csv")
    assert len(sl)==6
    keys={(r["predictor"],r["response"]) for r in sl}
    if keys!={(p,y) for p in ("delta_loo_rmse","delta_loo_value_mse")
               for y in ("observed","fixed_arrival","bird_increment")}:
        raise ValueError("S3 original fixed six contrasts missing")
    for r in sl:
        if r["preregistered"]!="FALSE":
            raise ValueError("Post-outcome data falsely relabeled registered")
    statuses=rows(replay_spatial/"spatial_sensitivity_scheme_status.csv")
    if {(r["scheme"],int(r["n_clusters"])) for r in statuses}!={("source_cell",20),
        ("target_cell",19),("target_grid_5deg",9),("target_grid_10deg",4)}:
        raise ValueError("Original geographic cluster structure changed")
    if [r["status"] for r in statuses if r["scheme"]=="target_grid_10deg"]!=["NOT_ESTIMABLE"]:
        raise ValueError("Invalid 10-degree block uncertainty was invented")
    return {
        "status":"S3_ORIGINAL_POSTOUTCOME_TRANSFER_AND_SPATIAL_REPLAY_MATCH",
        "six_original_comparisons":6,
        "spatial_uncertainty_schemes":4,
        "spatial_scheme_CI_rows":24,
        "omission_slope_rows":564,
        "source_and_replay_csv_sha256":{"six":summary,"spatial":geo},
        "original_v8_preregistered_analysis_modified":False,
        "animal_cue_perception_or_fitness_identified":False,
        "journal_submitted":False,
    }


def main():
    p=argparse.ArgumentParser()
    for k in ("six-original","spatial-original","six-replay","spatial-replay","receipt"):
        p.add_argument("--"+k,type=Path,required=True)
    a=p.parse_args()
    result=check(a.six_original,a.spatial_original,a.six_replay,a.spatial_replay)
    a.receipt.parent.mkdir(parents=True,exist_ok=True)
    a.receipt.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({key:result[key] for key in ("status",
          "six_original_comparisons","spatial_uncertainty_schemes","journal_submitted")}))


if __name__=="__main__":
    main()
