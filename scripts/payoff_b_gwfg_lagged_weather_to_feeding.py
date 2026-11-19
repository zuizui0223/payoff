#!/usr/bin/env python3
"""Original 2024 Greenland white-fronted goose stage-ordered weather test.

Exploratory original-paper-source reanalysis, never an independent q/D_eff/r_t
test. The code reads a public source, verifies exact original Git blob SHA,
fits a pre-declared stage3-freezing -> stage4-feeding model and downstream
prediction-stress tests. It emits ONLY aggregates, never bird identifiers.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t as student_t
import statsmodels.api as sm
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.metrics import mean_squared_error, log_loss, brier_score_loss
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SOURCE_REPO = "aschindler23/Schindler_etal_2024_ProcB"
SOURCE_FILE = "spring_data.csv"
SOURCE_GIT_BLOB_SHA1 = "ca3736a281dfd2465921efc940dd985499c71a4f"
SOURCE_YEAR_MAP = {1: 2018, 2: 2019, 3: 2020, 4: 2021, 5: 2022}
REQUIRED = {
    "id", "year", "sub_season", "breeding_outcome", "breeding_success",
    "first_day", "log_ODBA", "num_feed_fixes", "num_ACC_fixes",
    "mean_precip", "prop_days_below_freezing", "prop_storm_days",
}
SOURCE_STAGES = {1, 2, 3, 4, 5, 6}
EXPECTED = {
    "rows":642, "bird_years":107, "birds":49,
    "years":5, "successes":28, "non_successes":79,
    "repeated_birds":30, "three_plus_years":18,
}
RIDGE_ALPHA = 1.0
LOGIT_C = 1.0
CONTROLS = ["feed3","precip3","storm3","first_day3","precip4","storm4"]
PREDICTION_BASE = CONTROLS + ["year_index"]
PREDICTION_WITH_EARLY_FREEZE = PREDICTION_BASE + ["freeze3_10pp"]
SUCCESS_BASE = [
    "feed3", "freeze3_10pp", "precip3", "storm3",
    "precip4", "storm4", "first_day4", "year_index",
]
SUCCESS_LATE = SUCCESS_BASE + ["feed4","log_ODBA4"]


def original_source_digest(source_path:Path)->dict:
    source=source_path.read_bytes()
    sha1=hashlib.sha1(
        f"blob {len(source)}\0".encode("ascii")+source
    ).hexdigest()
    sha256=hashlib.sha256(source).hexdigest()
    if sha1!=SOURCE_GIT_BLOB_SHA1:
        raise ValueError("Original 2024 source Git blob SHA1 mismatch")
    return {
        "source_original_public_git_blob_SHA1":sha1,
        "source_original_public_file_SHA256":sha256,
        "source_file_size_bytes":len(source),
        "source_public_repository":SOURCE_REPO,
        "original_individual_or_annual_records_committed":False,
    }


def make_bird_years(source:pd.DataFrame, strict:bool=True)->pd.DataFrame:
    if not REQUIRED.issubset(source.columns):
        raise ValueError("Original source required columns missing")
    d=source.copy()
    if d[["id","year","sub_season"]].isnull().any().any():
        raise ValueError("Original bird-year-stage identifier missing")
    if d.duplicated(["id","year","sub_season"]).any():
        raise ValueError("Original duplicate bird-year-stage record")
    if not set(d.sub_season.unique()).issubset(SOURCE_STAGES):
        raise ValueError("Unknown original source stage")
    wide=[]
    for (bird,year), g in d.groupby(["id","year"],sort=True):
        gg={int(row.sub_season):row for row in g.itertuples(index=False)}
        if set(gg)!=SOURCE_STAGES:
            raise ValueError("Missing original source stage within bird-year")
        stages=[gg[i] for i in range(1,7)]
        if any(float(stages[i].first_day)>=float(stages[i+1].first_day)
               for i in range(5)):
            raise ValueError("Original source time ordering violation")
        outcats=set(int(x.breeding_outcome) for x in stages)
        success=set(int(x.breeding_success) for x in stages)
        if len(outcats)!=1 or len(success)!=1 or not outcats.issubset({1,2,3}):
            raise ValueError("Original breeding outcome inconsistency")
        yy=next(iter(outcats)); yy_success=next(iter(success))
        if yy_success not in (0,1) or (yy==1)!=(yy_success==1):
            raise ValueError("Original breeding outcome status invalid")
        for row in stages:
            for field in ("num_feed_fixes","num_ACC_fixes","log_ODBA",
                          "mean_precip","prop_days_below_freezing",
                          "prop_storm_days","first_day"):
                if not math.isfinite(float(getattr(row,field))):
                    raise ValueError("Nonfinite source stage measurement")
            if not (0<=row.num_feed_fixes<=row.num_ACC_fixes and row.num_ACC_fixes>0):
                raise ValueError("Invalid original ACC denominator or feed count")
            if not (0<=row.prop_days_below_freezing<=1
                    and 0<=row.prop_storm_days<=1):
                raise ValueError("Invalid source fraction")
            if row.mean_precip<0:
                raise ValueError("Negative source mean precipitation")
        v3,v4=gg[3],gg[4]
        wide.append({
            "bird_id":bird,
            "year_index":int(year),
            "first_day3":float(v3.first_day),
            "first_day4":float(v4.first_day),
            "feed3":float(v3.num_feed_fixes)/float(v3.num_ACC_fixes),
            "feed4":float(v4.num_feed_fixes)/float(v4.num_ACC_fixes),
            "freeze3_10pp":float(v3.prop_days_below_freezing)/0.1,
            "freeze4":float(v4.prop_days_below_freezing),
            "precip3":float(v3.mean_precip),
            "precip4":float(v4.mean_precip),
            "storm3":float(v3.prop_storm_days),
            "storm4":float(v4.prop_storm_days),
            "log_ODBA4":float(v4.log_ODBA),
            "breeding_success":yy_success,
            "breeding_outcome":yy,
        })
    x=pd.DataFrame(wide)
    if x.empty:
        raise ValueError("No original bird-year groups")
    if strict:
        counts=x.groupby("bird_id")["year_index"].nunique()
        actual={
            "rows":len(d),
            "bird_years":len(x),
            "birds":x.bird_id.nunique(),
            "years":x.year_index.nunique(),
            "successes":int(x.breeding_success.sum()),
            "non_successes":int((x.breeding_success==0).sum()),
            "repeated_birds":int((counts>=2).sum()),
            "three_plus_years":int((counts>=3).sum()),
        }
        if actual!=EXPECTED or set(x.year_index)!=set(SOURCE_YEAR_MAP):
            raise ValueError(f"Original published source grain drift: {actual}")
        sufficient_years=sum(
            x.loc[x.year_index==y,"freeze3_10pp"].nunique()>=3
            for y in SOURCE_YEAR_MAP
        )
        if sufficient_years<3:
            raise ValueError("Stage3 freezing within-year support gate failed")
        if x[["bird_id","year_index"]].duplicated().any():
            raise ValueError("Duplicate bird-year record")
    return x


def study_design(df:pd.DataFrame, include_freeze:bool=True)->pd.DataFrame:
    columns=["feed3","precip3","storm3","first_day3","precip4","storm4"]
    base=pd.DataFrame({"intercept":np.ones(len(df))},index=df.index)
    for c in columns:
        base[c]=df[c].astype(float)
    if include_freeze:
        base["freeze3_10pp"]=df["freeze3_10pp"].astype(float)
    # Rebuild year dummies using the earliest *observed training year* as
    # baseline, so omitting 2018 does not make intercept = sum(year dummies).
    for year in sorted(df.year_index.unique())[1:]:
        base[f"year_{int(year)}"]=df.year_index.eq(year).astype(float)
    return base


def regress(df:pd.DataFrame, include_freeze:bool=True)->dict:
    X=study_design(df,include_freeze)
    if int(np.linalg.matrix_rank(X.to_numpy()))!=len(X.columns):
        raise ValueError("Primary source design rank deficient")
    m=sm.OLS(df["feed4"].astype(float),X).fit(
        cov_type="cluster",
        cov_kwds={"groups":df.bird_id.to_numpy(),"use_correction":True},
    )
    if len(df)<50 or df.bird_id.nunique()<30:
        raise ValueError("Independent bird support insufficient")
    value={
        "n_bird_years":int(len(df)),
        "n_individual_birds":int(df.bird_id.nunique()),
        "n_calendar_years":int(df.year_index.nunique()),
        "design_columns":int(len(X.columns)),
        "design_rank":int(np.linalg.matrix_rank(X.to_numpy())),
        "sum_squared_residuals":float(np.sum(m.resid**2)),
        "fitted_ordinary_R2":float(m.rsquared),
        "bird_cluster_covariance":True,
    }
    if include_freeze:
        coef=float(m.params["freeze3_10pp"])
        se=float(m.bse["freeze3_10pp"])
        df_study=int(df.bird_id.nunique()-1)
        crit=float(student_t.ppf(0.975,df_study))
        p=2*float(student_t.sf(abs(coef/se),df_study)) if se>0 else None
        value.update({
            "focal_early_freezing_beta_per_10pp":coef,
            "bird_cluster_SE":se,
            "bird_t_df":df_study,
            "focal_ci95":[coef-crit*se,coef+crit*se],
            "focal_two_sided_p":p,
        })
    return value


def _predictive_group_cv(df:pd.DataFrame,
                         baseline_cols:list[str],
                         updated_cols:list[str],
                         grouping:str,
                         is_binary:bool=False)->dict:
    if grouping not in ("bird_id","year_index"):
        raise ValueError("Only original independent bird/year folds")
    y=df["breeding_success"].to_numpy(int) if is_binary else df["feed4"].to_numpy(float)
    fold_ids=df[grouping].to_numpy()
    base_pred=np.zeros(len(df),float)
    with_pred=np.zeros(len(df),float)
    outcome_records=[]
    for train_idx,test_idx in LeaveOneGroupOut().split(df,y,fold_ids):
        if is_binary:
            if len(set(y[train_idx]))<2:
                raise ValueError("Binary training sample lacks success/failure")
            m0=make_pipeline(StandardScaler(),LogisticRegression(
                C=LOGIT_C,penalty="l2",max_iter=5000,solver="lbfgs"))
            m1=make_pipeline(StandardScaler(),LogisticRegression(
                C=LOGIT_C,penalty="l2",max_iter=5000,solver="lbfgs"))
        else:
            m0=make_pipeline(StandardScaler(),Ridge(alpha=RIDGE_ALPHA))
            m1=make_pipeline(StandardScaler(),Ridge(alpha=RIDGE_ALPHA))
        m0.fit(df.iloc[train_idx][baseline_cols],y[train_idx])
        m1.fit(df.iloc[train_idx][updated_cols],y[train_idx])
        if is_binary:
            pred0=m0.predict_proba(df.iloc[test_idx][baseline_cols])[:,1]
            pred1=m1.predict_proba(df.iloc[test_idx][updated_cols])[:,1]
        else:
            pred0=m0.predict(df.iloc[test_idx][baseline_cols])
            pred1=m1.predict(df.iloc[test_idx][updated_cols])
        base_pred[test_idx]=pred0
        with_pred[test_idx]=pred1
        # No individual bird IDs ever enter the output artifact.
        if grouping=="year_index":
            if is_binary:
                ll0=float(log_loss(y[test_idx],pred0,labels=[0,1]))
                ll1=float(log_loss(y[test_idx],pred1,labels=[0,1]))
            else:
                ll0=float(mean_squared_error(y[test_idx],pred0))
                ll1=float(mean_squared_error(y[test_idx],pred1))
            outcome_records.append({
                "calendar_year":int(2017+int(fold_ids[test_idx][0])),
                "n_bird_years":len(test_idx),
                "baseline_loss":ll0,
                "augmented_loss":ll1,
            })
    if is_binary:
        score0=float(log_loss(y,base_pred,labels=[0,1]))
        score1=float(log_loss(y,with_pred,labels=[0,1]))
        metric="heldout_pooled_log_loss"
        extra={
            "baseline_heldout_brier":float(brier_score_loss(y,base_pred)),
            "augmented_heldout_brier":float(brier_score_loss(y,with_pred)),
        }
    else:
        score0=float(mean_squared_error(y,base_pred))
        score1=float(mean_squared_error(y,with_pred))
        metric="heldout_pooled_MSE_feeding_fraction_squared"
        extra={}
    return {
        "holdout_unit":grouping,
        "n_holdout_folds":int(np.unique(fold_ids).size),
        "same_time_window_baseline":True,
        "train_only_standardization":True,
        "ridge_alpha_not_tuned":RIDGE_ALPHA if not is_binary else None,
        "logistic_C_not_tuned":LOGIT_C if is_binary else None,
        "metric":metric,
        "baseline_loss":score0,
        "augmented_loss":score1,
        "augmented_minus_baseline":score1-score0,
        "per_year_metrics":outcome_records if grouping=="year_index" else "NOT_EMITTED_TO_PROTECT_BIRD_ID",
        **extra,
    }


def run(df:pd.DataFrame, source_info:dict)->dict:
    if (len(df),df.bird_id.nunique(),df.year_index.nunique())!=(107,49,5):
        raise ValueError("Independent original bird/year source insufficient")
    primary=regress(df,True)
    null=regress(df,False)
    partial=(
        (null["sum_squared_residuals"]-primary["sum_squared_residuals"])
        /null["sum_squared_residuals"]
    )
    omitted=[]
    for year in sorted(df.year_index.unique()):
        subset=df[df.year_index!=year].copy()
        fit=regress(subset,True)
        omitted.append({
            "original_heldout_year":2017+int(year),
            "estimate":fit["focal_early_freezing_beta_per_10pp"],
            "CI95":fit["focal_ci95"],
            "n_remaining_bird_years":fit["n_bird_years"],
        })
    return {
        "result_id":"PAYOFF_B_SCHINDLER_2024_LAGGED_STAGE3_STAGE4_20261119",
        "as_of":"2026-11-19",
        "scientific_status":"POST_OPEN_SOURCE_REANALYSIS_NO_CUE_CAUSAL_IDENTIFICATION",
        "frozen_contract":"docs/PAYOFF_B_GWFG_STAGE3_TO_STAGE4_FREEZE_20261119.md",
        "original_source":source_info,
        "unit":"individual bird-year",
        "source_metadata":{
            "source_staging_rows":642,
            "original_individual_bird_years":107,
            "original_birds":49,
            "birds_with_2plus_years":30,
            "birds_with_3plus_years":18,
            "calendar_years":[2018,2019,2020,2021,2022],
            "original_breeding_success":28,
            "original_breeding_failed_attempt":72,
            "original_breeding_deferral":7,
            "all_original_stages_1_to_6_present_and_ordered":True,
        },
        "stage3_early_freezing_association":{
            "full_source_fixed_year_clustered_OLS":primary,
            "otherwise_identical_no_freeze_SSE":null["sum_squared_residuals"],
            "freeze3_partial_SSE_reduction_fraction":float(partial),
            "leave_one_year_out_coefficient_stress":omitted,
            "no_original_study_year_independent_replications_claimed":True,
        },
        "stage4_feeding_heldout_prediction":{
            "baseline_weather_earlier_feeding_no_freeze_vs_added_early_freeze":{
                "leave_one_entire_bird_out":_predictive_group_cv(
                    df,PREDICTION_BASE,PREDICTION_WITH_EARLY_FREEZE,"bird_id"),
                "leave_one_entire_year_out":_predictive_group_cv(
                    df,PREDICTION_BASE,PREDICTION_WITH_EARLY_FREEZE,"year_index"),
            },
        },
        "stage4_behavior_to_later_breeding_success_prediction":{
            "already_published_feeding_fitness_association_prior_art":True,
            "leave_one_entire_bird_out":_predictive_group_cv(
                df,SUCCESS_BASE,SUCCESS_LATE,"bird_id",is_binary=True),
            "leave_one_entire_year_out":_predictive_group_cv(
                df,SUCCESS_BASE,SUCCESS_LATE,"year_index",is_binary=True),
        },
        "claims":{
            "new_independent_natural_study":False,
            "source_original_was_published_and_analyzed_in_2024":True,
            "direct_organism_observed_future_state_credibility":False,
            "actual_cue_observed_before_departure":False,
            "original_weather_measure_in_stage3_is_animal_belief":False,
            "correlation_or_prediction_is_causal_compensation":False,
            "measured_downstream_actuator_budget":False,
            "individual_payoff_q_wait_or_D_eff_identified":False,
            "v7_goose_geographic_q_times_U_opened":False,
            "source_eBird_occurrences_used":False,
            "new_paper_claim_ceiling":"Temporal-source lagged association/predictive update only, not the PAYOFF mechanism",
        },
    }


def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    source_info=original_source_digest(args.source)
    raw=pd.read_csv(args.source)
    wide=make_bird_years(raw,strict=True)
    result=run(wide,source_info)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    primary=result["stage3_early_freezing_association"]["full_source_fixed_year_clustered_OLS"]
    print(json.dumps({
        "primary_early_freezing_coefficient":primary["focal_early_freezing_beta_per_10pp"],
        "primary_ci95":primary["focal_ci95"],
        "year_CV_freeze_extra_MSE":result["stage4_feeding_heldout_prediction"][
            "baseline_weather_earlier_feeding_no_freeze_vs_added_early_freeze"
        ]["leave_one_entire_year_out"]["augmented_minus_baseline"],
        "success_year_CV_late_behavior_extra_logloss":result[
            "stage4_behavior_to_later_breeding_success_prediction"
        ]["leave_one_entire_year_out"]["augmented_minus_baseline"],
        "source_verified":True,
        "causal_information_theory_mechanism":False,
    },ensure_ascii=False))

if __name__=="__main__":
    main()
