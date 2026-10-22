#!/usr/bin/env python3
"""Held-out-year incremental physical-weather prediction from strict bird GPS.

Frozen pre-fit exploratory protocol: season/geography/stationary-run baseline
vs same baseline + source-day -1 and days -2..-8 NASA POWER weather.

Uses *original* published CC0 and MD5, true all-original-GPS-fixes-within-
30-km strict source-state sensitivity, and unchanged day4/5 labels. Entire
calendar years are held out: no split of overlapping animal-days within year.
Secondary held-out-animal check accounts for repeated individuals, but neither
can identify weather cues actually perceived by a migrating bird.

OUTCOME-OPENED: weather group contrasts and source cohort details were
previously examined; this is a prospective *model workflow* on previously
opened data, NOT independent preregistered species-wide confirmation.

No GPS, identities, event dates, or weather-grid coordinates exported.
"""
from __future__ import annotations
import argparse
import json
import math
import tempfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_predecision_candidates import SYSTEMS, daily_source_positions
from scripts.qc_payoff_b_complete_stationary_riskset import collect
from scripts.qc_payoff_b_riskday_fix_integrity import audit_fixes
from scripts.qc_payoff_b_strict_fix_source_overlap import (
    ORIGINAL_CLEAN_COUNT, filtered_source_gate,
)
from scripts.run_payoff_b_full_riskday_daily_weather import (
    batch_key, download_batch, event_prior_weather,
)

SOURCE_LIST=("stork","white_fronted_goose","curlew")
CASE="NORTHWARD_CANDIDATE"
STAY="STAYED_TWO_DAYS"
WEATHER=("T2M_last","T2M_anomaly","WS10M_last","WS10M_anomaly",
         "V10M_last","V10M_anomaly",
         "ALLSKY_SFC_SW_DWN_last","ALLSKY_SFC_SW_DWN_anomaly")
MIN_COMPLETE_FRACTION=.95
MIN_TRAIN_POSITIVES=12
MIN_TRAIN_STAYS=60
MIN_TEST_ROWS=20
MIN_TEST_POSITIVES=1
MIN_HOLDOUT_YEARS=3
MIN_TESTED_POSITIVES=15
MIN_TESTED_STAYS=100
MODEL_C=1.0
METRIC_EPS=1e-9
MAX_PUBLIC_BATCHES=500


def site_time_features(date,site,run_length):
    """Only quantities known before future day4/5 outcome is scored."""
    doy=date.timetuple().tm_yday
    lat,lon=site
    radians=math.radians(lon)
    angle=2*math.pi*doy/365.25
    return [
        math.sin(angle),math.cos(angle),
        lat/90,math.sin(radians),math.cos(radians),
        math.log1p(run_length),
    ]


def make_risk_features(risk,mask):
    """Run-age must not depend on which earlier days later became cases/stays.

    First traverse every GPS-defined source opportunity, even OTHER/CENSORED,
    with original strict fix flags. Count consecutive strict source days
    using only the observation history through each anchor day; ONLY THEN
    decide which rows have the two observed future GPS outcome classes.
    """
    from datetime import timedelta
    if len(risk)!=len(mask):
        raise ValueError("Source and GPS mask disagree")
    originals=sorted(zip(risk,mask),key=lambda pair:(pair[0][0],pair[0][1]))
    last={}
    run=defaultdict(int)
    result=[]
    for ((tax,animal,year),day,site,label),strict in originals:
        group=(tax,animal,year)
        if not strict:
            run[group]=0
            last.pop(group,None)
            continue
        old=last.get(group)
        run[group]=(run[group]+1 if old is not None and
                    day-old==timedelta(days=1) else 1)
        last[group]=day
        if label not in (CASE,STAY):
            continue
        result.append({
            "source_group":group,"animal":animal,"year":year,
            "source_day":day,"site":site,"label":label,
            "base":site_time_features(day,site,run[group]),
        })
    return result


def private_complete_weather(rows,cache):
    good=[]
    absent=Counter()
    for r in rows:
        source=cache.get(batch_key(r["source_day"],r["site"]))
        if source is None:
            absent["MISSING_SOURCE_BATCH"]+=1
            continue
        met=event_prior_weather(source,r["source_day"])
        if met is None:
            absent["INSUFFICIENT_PREDECISION_HISTORY"]+=1
            continue
        if not all(math.isfinite(met[v]) for v in WEATHER):
            absent["NONFINITE_SOURCE_METEOROLOGY"]+=1
            continue
        good.append({
           "base":r["base"],
           "weather":[met[v] for v in WEATHER],
           "y":int(r["label"]==CASE),
           "animal":r["animal"],
           "year":r["year"],
        })
    return good,dict(sorted(absent.items()))


def fold_score(data,groups,*,scheme):
    """Both models trained on identical rows, scaler fit on training ONLY."""
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    from sklearn.model_selection import GroupKFold

    y=np.asarray([int(r["y"]) for r in data],dtype=int)
    X0=np.asarray([r["base"] for r in data],dtype=float)
    X1=np.asarray([r["base"]+r["weather"] for r in data],dtype=float)
    years=np.asarray([r["year"] for r in data],dtype=int)
    animals=np.asarray([r["animal"] for r in data])
    folds=[]
    if scheme=="calendar_year":
        for yr in sorted(set(years)):
            test=np.flatnonzero(years==yr)
            train=np.flatnonzero(years!=yr)
            folds.append((train,test))
    elif scheme=="whole_animal":
        groups_unique=len(set(animals))
        if groups_unique<5:
            return {"status":"INSUFFICIENT_ANIMAL_IDENTITIES",
                    "available_animal_identifiers":groups_unique}
        folds=list(GroupKFold(n_splits=5).split(X0,y,groups=animals))
    else:raise ValueError("Invalid CV block scheme")

    outcomes=[]
    totals=Counter()
    for tr,te in folds:
        if (sum(y[tr])<MIN_TRAIN_POSITIVES or
            sum(1-y[tr])<MIN_TRAIN_STAYS or
            len(te)<MIN_TEST_ROWS or
            sum(y[te])<MIN_TEST_POSITIVES):
            totals["unadmitted_folds"]+=1
            continue
        if scheme=="calendar_year" and set(years[tr])&set(years[te]):
            raise ValueError("Source-year leakage detected")
        if scheme=="whole_animal" and set(animals[tr])&set(animals[te]):
            raise ValueError("Source-individual leakage detected")
        predictions=[]
        for feature in (X0,X1):
            model=make_pipeline(
                StandardScaler(),
                LogisticRegression(C=MODEL_C,penalty="l2",
                                   solver="lbfgs",max_iter=1600)
            )
            model.fit(feature[tr],y[tr])
            prob=np.clip(model.predict_proba(feature[te])[:,1],
                         METRIC_EPS,1-METRIC_EPS)
            predictions.append(prob)
        outcomes.append((te,predictions))
        totals["admitted_folds"]+=1

    indices=[index for test,_ in outcomes for index in test]
    if len(set(indices))!=len(indices):
        raise ValueError("Overlapping CV test slices")
    if (len(outcomes)<MIN_HOLDOUT_YEARS or
        sum(y[indices])<MIN_TESTED_POSITIVES or
        sum(1-y[indices])<MIN_TESTED_STAYS):
        return {
            "status":"NOT_ESTIMABLE_PRESET_HELDOUT_SOURCE_GATES",
            "split_scheme":scheme,
            "n_folds_admitted":len(outcomes),
            "n_folds_excluded":totals["unadmitted_folds"],
            "heldout_original_source_cases":int(sum(y[indices])),
            "heldout_original_source_stays":int(sum(1-y[indices])),
        }

    p0=np.concatenate([p[0] for _,p in outcomes])
    p1=np.concatenate([p[1] for _,p in outcomes])
    actual=y[indices]
    def logloss(prob):
        return float(np.mean(-actual*np.log(prob)-(1-actual)*np.log(1-prob)))
    def brier(prob):
        return float(np.mean((actual-prob)**2))
    loss0,loss1=logloss(p0),logloss(p1)
    brier0,brier1=brier(p0),brier(p1)
    return {
        "status":"OUT_OF_FOLD_OBSERVATIONAL_PREDICTION_ESTIMABLE",
        "split_scheme":scheme,
        "n_folds_admitted":len(outcomes),
        "n_folds_excluded":totals["unadmitted_folds"],
        "heldout_original_source_days":len(indices),
        "heldout_original_source_cases":int(sum(actual)),
        "heldout_original_source_stays":int(sum(1-actual)),
        "baseline_log_loss":loss0,
        "baseline_plus_weather_log_loss":loss1,
        "incremental_lag_weather_log_loss_gain":loss0-loss1,
        "baseline_Brier_score":brier0,
        "baseline_plus_weather_Brier_score":brier1,
        "incremental_lag_weather_Brier_gain":brier0-brier1,
        "positive_gain_means_better_heldout_prediction":True,
        "fixed_model":"L2 regularized logistic C=1, standardized within train only",
        "baseline":"DOY sin/cos, latitude, circular longitude, past eligible run-age",
        "additional_predictors":"predecision last-day & 7-day anomalies: T2M,WS10M,V10M,solar",
        "no_individual_predictions_or_animal_ids_exported":True,
    }


def run_one(system,fetch=download_batch):
    with tempfile.TemporaryDirectory() as d:
        original=Path(d)/"original_CC0_GPS.csv"
        doi,taxon,sensor,digest=origin_source(system,original)
        groups,source_quality,idcol=daily_source_positions(original,taxon)
        allrisk,orig,_,_=collect(groups)
        _,mask=audit_fixes(original,allrisk,taxon,return_private_mask=True)
        stage=filtered_source_gate(allrisk,mask)
        n=stage["strict_all_3days_fix_within_30km_source_riskdays"]
        c=stage["strict_all_3days_source_label_counts"]
        if (n,c.get(CASE,0),c.get(STAY,0))!=ORIGINAL_CLEAN_COUNT[system]:
            raise ValueError("Original strict published source eligibility changed")
        if not stage["source_overlap_preweather_admission"]["passed"]:
            return {"status":"NOT_ADMITTED_SOURCE_ORIGINAL_OVERLAP_GATE"}
        rows=make_risk_features(allrisk,mask)
        batches=sorted({batch_key(r["source_day"],r["site"]) for r in rows})
        if len(batches)>MAX_PUBLIC_BATCHES:
            return {"status":"NOT_ADMITTED_PUBLIC_API_REQUEST_CAP",
                    "source_batch_count":len(batches)}
        response={};errors=Counter()
        with ThreadPoolExecutor(max_workers=3) as pool:
            fs={pool.submit(fetch,key):key for key in batches}
            for fut in as_completed(fs):
                key=fs[fut]
                try:response[key]=fut.result()
                except Exception as exc:errors[type(exc).__name__]+=1
        complete,missing=private_complete_weather(rows,response)
        if len(complete)<len(rows)*MIN_COMPLETE_FRACTION:
            return {
                "status":"NOT_ESTIMABLE_WEATHER_SOURCE_COMPLETENESS",
                "original_source_case_stay_days":len(rows),
                "complete_days":len(complete),
                "source_batch_failures":dict(sorted(errors.items())),
                "row_missing_categories":missing,
            }
        return {
            "status":"PHYSICAL_WEATHER_PREDICTION_CV_COMPLETED",
            "source_doi":doi,"taxon":taxon,
            "source_GPS_MD5_and_bytes_verified":digest,
            "original_strict_source_riskdays":n,
            "original_strict_case_stay_riskdays":len(rows),
            "original_source_cases":c.get(CASE,0),
            "original_source_stays":c.get(STAY,0),
            "unique_month_weather_API_batches":len(batches),
            "weather_batches_failed":dict(sorted(errors.items())),
            "original_complete_weather_rows":len(complete),
            "weather_missing":missing,
            "heldout_whole_source_calendar_year":fold_score(complete, None,scheme="calendar_year"),
            "heldout_whole_animal_IDs":fold_score(complete,None,scheme="whole_animal"),
            "biological_weather_cue_received_by_bird_proven":False,
            "animal_actionability_or_fitness_measured":False,
            "causal_hazard_effect_estimated":False,
            "actual_migration_intention_verified":False,
            "original_sensitive_positions_dates_ids_exported":False,
        }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--system",choices=SOURCE_LIST,required=True)
    p.add_argument("--out",type=Path,default=Path("outputs/payoff_b_strict_cv_weather"))
    a=p.parse_args()
    record={
       "schema":"payoff_b_strict_source_weather_incremental_predictive_value_v1",
       "source_system":a.system,
       "analysis_class":"POST_OUTCOME_EXPLORATORY_PREDICTIVE_NECESSARY_CONDITION_ONLY",
       "model_protocol":"docs/PAYOFF_B_STRICT_WEATHER_CV_PROTOCOL_20261022.md",
    }
    try:record["result"]=run_one(a.system)
    except Exception as e:
        record["result"]={
            "status":"PUBLISHED_SOURCE_OR_CV_MODEL_FAILED",
            "error":type(e).__name__+": "+str(e)[:240],
        }
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/(a.system+".json")).write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps(record,indent=2))
    if record["result"]["status"]!="PHYSICAL_WEATHER_PREDICTION_CV_COMPLETED":
        raise SystemExit("Incremental weather value source-CV gate failed")

if __name__=="__main__":main()
