#!/usr/bin/env python3
"""Original-source radar station/year ecological association; NEVER a bird cue model.

Predeclared: site intercepts + linear calendar trend + full-season temperature
versus the same model + site/year MODIS greenup. Initial invocation is
--support-only and MUST NOT open the bird passage outcome.
After support is frozen separately, a --fit invocation may run one fixed
leave-entire-year-out retrospective comparison, not actual forecasts at choice.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np

SOURCE_SHA = "1751ca4cd523d632368ba7fbb27987c2d6c1cc4c1a9c75b8c67255476d799900"
DATA_COLS = ("site", "year", "spring_q50", "spring_mean_temp", "mean_greenup")
CONTRACT = Path(__file__).resolve().parents[1] / "data/payoff_b_radar_greenup_heldout_contract_20261122.json"


def source_rows(path):
    """Uncommitted original data must only exist in ephemeral runner memory/disk."""
    with Path(path).open(newline="") as stream:
        reader = csv.DictReader(stream)
        if not all(x in (reader.fieldnames or []) for x in DATA_COLS):
            raise ValueError("Original expected field missing")
        rows = []
        seen = set()
        for row in reader:
            site = (row.get("site") or "").strip()
            year_txt = (row.get("year") or "").strip()
            if not site or not year_txt or not year_txt.isdigit():
                raise ValueError("Original site or year invalid")
            year = int(year_txt)
            if not 2003 <= year <= 2018:
                raise ValueError("Original sample outside source years")
            key = (site, year)
            if key in seen:
                raise ValueError("Duplicate site-year")
            seen.add(key)
            values = {}
            for col in DATA_COLS[2:]:
                raw = (row.get(col) or "").strip()
                if raw.upper() in {"", "NA", "N/A", "NAN", "NULL"}:
                    values[col] = None
                    continue
                x = float(raw)
                values[col] = x if math.isfinite(x) else None
            rows.append({"site":site,"year":year,**values})
    return rows


def complete_rows(rows):
    return [x for x in rows if all(x.get(col) is not None for col in DATA_COLS[2:])]


def matrix(rows, augmented:bool, temperature:bool=True, holdout_sites=None):
    """Fixed site-dummy dictionary plus an explicit numeric year trend."""
    sites = holdout_sites if holdout_sites is not None else sorted({r["site"] for r in rows})
    ids = {name:i for i,name in enumerate(sites)}
    k = len(sites)+1 + int(temperature) + int(augmented)
    X = np.zeros((len(rows),k),dtype=float)
    for j,row in enumerate(rows):
        if row["site"] not in ids:
            raise ValueError("Holdout station absent from training")
        X[j,ids[row["site"]]] = 1
        X[j,len(sites)] = row["year"] - 2010
        if temperature:
            X[j,len(sites)+1] = row["spring_mean_temp"]
        if augmented:
            X[j,-1] = row["mean_greenup"]
    return X


def check_design(rows,contract):
    """Predictor-only support gate. Does not access spring_q50 values."""
    limits = contract["support_before_any_new_effect"]
    original_n = len(rows)
    complete = complete_rows(rows)
    if not complete:
        return {"status":"NOT_ESTIMABLE", "reason":"NO_COMPLETE_ROWS",
                "n_original":original_n,"n_complete":0}
    site_count = len({r["site"] for r in complete})
    years = sorted({r["year"] for r in complete})
    counts = {int(y):sum(r["year"]==y for r in complete) for y in years}
    missing_fraction = 1 - len(complete)/original_n
    base = matrix(complete,augmented=False)
    names = sorted({r["site"] for r in complete})
    site_year = np.asarray(matrix(complete,augmented=False,temperature=False))
    t = np.array([r["spring_mean_temp"] for r in complete])
    green = np.array([r["mean_greenup"] for r in complete])
    def resid(A,y):
        beta,*_ = np.linalg.lstsq(A,y,rcond=None)
        return y - A @ beta
    base_rank = int(np.linalg.matrix_rank(base))
    z1 = resid(site_year,green)
    z2 = resid(base,green)
    raw_ss = float(z1@z1)
    cond_ss = float(z2@z2)
    vif = raw_ss/cond_ss if cond_ss > 1e-12 else float("inf")
    residual_df=len(complete)-base_rank-1
    support = {
       "rows":len(complete)>=limits["min_complete_pairs"],
       "stations":site_count>=limits["min_stations"],
       "years":len(years)>=limits["min_years"],
       "all_heldout_year_support":all(v>=limits["min_site_years_per_heldout_year"] for v in counts.values()),
       "missing":missing_fraction<=limits["max_missing_focal_fraction"],
       "residual_df":residual_df>=limits["min_residual_df"],
       "greenup_independent":float(np.sqrt(cond_ss/len(complete)))>=limits["min_greenup_after_station_year_trend_temp_rms_days"],
       "vif":bool(np.isfinite(vif) and vif<=limits["max_greenup_partial_vif"]),
       "full_rank":base_rank+1 == int(np.linalg.matrix_rank(np.column_stack([base,green]))),
    }
    return {
       "status":"PASS" if all(support.values()) else "NOT_ESTIMABLE",
       "checks":support,"n_original":original_n,"n_complete":len(complete),
       "n_missing":original_n-len(complete),
       "n_sites":site_count,"n_years":len(years),
       "year_min":min(years),"year_max":max(years),
       "min_year_station_n":min(counts.values()),
       "max_year_station_n":max(counts.values()),
       "nuisance_rank":base_rank,
       "joint_df_residual":residual_df,
       "greenup_after_station_yeartrend_rms_days":float(np.sqrt(raw_ss/len(complete))),
       "greenup_after_temp_calendar_rms_days":float(np.sqrt(cond_ss/len(complete))),
       "greenup_partial_vif":float(vif) if np.isfinite(vif) else None,
       "new_bird_coefficient_opened":False,
    }


def estimate(rows, contract):
    """One fixed researcher-retrospective leave-calendar-year-out comparison."""
    design = check_design(rows,contract)
    result = {"status":"NOT_ESTIMABLE","prefit":design,
              "claim_limit":"Group radar ecology, not measured individual cue uptake, resource intake, or fitness.",
              "new_animal_info_mechanism_identified":False,
              "ecological_effect":None}
    if design["status"]!="PASS":
        return result
    data=complete_rows(rows)
    years=sorted({x["year"] for x in data})
    sites=sorted({x["site"] for x in data})
    folds=[]
    for year in years:
        tr=[x for x in data if x["year"]!=year]
        te=[x for x in data if x["year"]==year]
        if set(x["site"] for x in te)-set(x["site"] for x in tr):
            result["status"]="HOLDOUT_UNSEEN_STATION"
            return result
        yy=np.array([x["spring_q50"] for x in tr],dtype=float)
        y_test=np.array([x["spring_q50"] for x in te],dtype=float)
        a=matrix(tr,False,holdout_sites=sites)
        A=matrix(tr,True,holdout_sites=sites)
        ca,*_=np.linalg.lstsq(a,yy,rcond=None)
        cA,*_=np.linalg.lstsq(A,yy,rcond=None)
        pred_a=matrix(te,False,holdout_sites=sites)@ca
        pred_A=matrix(te,True,holdout_sites=sites)@cA
        mse_a=float(np.mean((pred_a-y_test)**2))
        mse_A=float(np.mean((pred_A-y_test)**2))
        folds.append({"heldout_year":year,"n":len(te),"mse_calendar_temperature":mse_a,
                      "mse_plus_greenup":mse_A,"mse_gain":mse_a-mse_A})
    deltas=np.array([f["mse_gain"] for f in folds],dtype=float)
    rand=np.random.default_rng(contract["uncertainty"]["seed"])
    ix=rand.integers(0,len(deltas),size=(contract["uncertainty"]["replicates"],len(deltas)))
    bs=np.mean(deltas[ix],axis=1)
    ci=np.quantile(bs,[0.025,0.975]).tolist()
    X=matrix(data,True,holdout_sites=sites)
    y=np.array([x["spring_q50"] for x in data],dtype=float)
    coef,*_=np.linalg.lstsq(X,y,rcond=None)
    avg_gain=float(np.mean(deltas))
    n_positive=int(np.sum(deltas>0))
    cond=avg_gain>0 and ci[0]>0 and n_positive>=10
    result.update({
       "status":"SUPPORT_PREDICTIVE_GAIN" if cond else "NO_ROBUST_PREDICTIVE_GAIN",
       "ecological_effect":{
          "primary_heldout_equal_year_mean_mse_gain":avg_gain,
          "ci95_bootstrap_years":ci,"n_heldout_years":len(folds),
          "n_years_positive":n_positive,
          "mean_baseline_mse":float(np.mean([f["mse_calendar_temperature"] for f in folds])),
          "mean_plus_greenup_mse":float(np.mean([f["mse_plus_greenup"] for f in folds])),
          "full_sample_descriptive_greenup_beta_day_per_greenup_day":float(coef[-1]),
          "folds":folds,
       }
    })
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--contract",type=Path,default=CONTRACT)
    p.add_argument("--support-only",action="store_true")
    p.add_argument("--fit",action="store_true")
    p.add_argument("--output",type=Path,required=True)
    x=p.parse_args()
    if bool(x.support_only)==bool(x.fit):
        p.error("Choose exactly one of --support-only or --fit")
    raw=x.contract.read_bytes()
    contract=json.loads(raw)
    rows=source_rows(x.input)
    if x.support_only:
        result={"status":"PREFIT_SUPPORT_ONLY","design":check_design(rows,contract),
                "outcome_opened":False,"new_bird_coefficient_fitted":False}
    else:
        result=estimate(rows,contract)
    result.update(date=contract["date"],contract_sha256=hashlib.sha256(raw).hexdigest(),
                  source_sha256=SOURCE_SHA,
                  provenance="Original Adams 2025 Figshare RDS read privately in CI; no original station/year rows published.",
                  no_ebird=True,publication_claim="POST_PUBLICATION_EXPLORATORY")
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print("RADAR_GREENUP_RESULT="+json.dumps(result,separators=(",",":"),allow_nan=False))


if __name__=="__main__":
    main()
