#!/usr/bin/env python3
"""Post-open Usui E6 within-study migration-distance robustness only.

- SHA256-verified original 944-row published E6 effect archive.
- Known eBird-derived study excluded; Lithuanian 4-row source unresolved.
- 676 described-original-source rows, 26 original studies.
- PRIMARY: 13 crossed studies, 444 effects, fixed study intercepts.
- No animal decision-time cue, causal information access, or novelty claim.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from scripts.payoff_b_e6_known_ebird_exclusion import read_verified_artifact
from scripts.payoff_b_e6_source_origin_inventory import inventory
from scripts.payoff_b_cross_system_information import (
    two_way_cluster_wls,
    term_summary,
)


def source_only_crossed_studies(original: pd.DataFrame) -> pd.DataFrame:
    provenance = inventory(original)
    origins = {v["study"] for v in provenance["source_specific_evidence"]}
    x = original.loc[original["Study"].isin(origins)].copy()
    if (len(x),x["Study"].nunique(),x["Species"].nunique())!=(676,26,279):
        raise ValueError("Source-described original E6 panel changed")
    groups = pd.crosstab(x["Study"],x["Migration_distance"])
    if not {"short","long"}.issubset(groups.columns):
        raise ValueError("No short/long source categories")
    both = groups.index[(groups["short"]>0)&(groups["long"]>0)]
    d = x.loc[x["Study"].isin(both)].copy()
    if (len(both),len(d),d["Species"].nunique())!=(13,444,269):
        raise ValueError("Source-only within-study crossed support drifted")
    return d


def fixed_study_design(df: pd.DataFrame) -> tuple[np.ndarray,list[str]]:
    studies = sorted(df["Study"].astype(str).unique().tolist())
    if len(studies)<2:
        raise ValueError("At least two source studies required")
    cols=["intercept","long_minus_short"] + ["study:"+v for v in studies[1:]]
    study = pd.get_dummies(df["Study"].astype(str),dtype=float).reindex(
        columns=studies[1:],fill_value=0.)
    x = np.column_stack([
        np.ones(len(df),dtype=float),
        df["Migration_distance"].eq("long").astype(float).to_numpy(),
        study.to_numpy(dtype=float),
    ])
    rank=int(np.linalg.matrix_rank(x))
    if rank!=x.shape[1]:
        raise ValueError("Study FE model not full rank")
    return x,cols


def fit(df: pd.DataFrame, method: str) -> dict:
    x,names = fixed_study_design(df)
    w = 1.0 / np.square(df["SE"].to_numpy(float))
    if method=="cap99":
        w=np.minimum(w,float(np.quantile(w,0.99)))
    elif method=="unweighted":
        w=np.ones_like(w)
    elif method!="ivw":
        raise ValueError("Unknown predeclared weighting method")
    obj=two_way_cluster_wls(
        df["Slope"].to_numpy(float),
        x,w,
        df["Study"].astype(str).to_numpy(),
        df["Species"].astype(str).to_numpy(),
    )
    coef=term_summary(obj,names,"long_minus_short")
    if (
        obj["clusters_study"] != len(df.Study.unique())
        or coef["df"] != len(df.Study.unique())-1
    ):
        raise ValueError("Two-way clustered study degrees of freedom drifted")
    if not np.isfinite(coef["estimate"]) or not np.isfinite(coef["se"]):
        raise ValueError("Invalid fitted coefficient or clustered SE")
    return {
        "method":method,
        "n_effect_rows":int(len(df)),
        "n_independent_source_studies":int(obj["clusters_study"]),
        "n_source_species":int(obj["clusters_species"]),
        "design_columns":len(names),
        "design_rank":int(np.linalg.matrix_rank(x)),
        "study_cluster_df":int(coef["df"]),
        "beta_long_minus_short_days_per_C":float(coef["estimate"]),
        "cluster_se":float(coef["se"]),
        "ci95":[float(a) for a in coef["ci95"]],
        "p_two_sided":float(coef["p"]),
    }


def descriptive_study_contrasts(df: pd.DataFrame) -> list[dict]:
    out=[]
    for name,g in sorted(df.groupby("Study"),key=lambda x:str(x[0])):
        numbers={}
        for distance in ("short","long"):
            v=g.loc[g.Migration_distance.eq(distance)]
            if v.empty:
                raise ValueError("Crossed study missing one distance class")
            w=1.0/np.square(v.SE.to_numpy(float))
            numbers[distance]=float(np.average(v.Slope.to_numpy(float),weights=w))
        out.append({
            "original_source_study":str(name),
            "rows":len(g),
            "short_rows":int((g.Migration_distance=="short").sum()),
            "long_rows":int((g.Migration_distance=="long").sum()),
            "descriptive_IVW_long_minus_short":numbers["long"]-numbers["short"],
            "per_study_significance_calculated":False,
        })
    return out


def run(original: pd.DataFrame) -> dict:
    d=source_only_crossed_studies(original)
    primary=fit(d,"ivw")
    if (
        primary["design_columns"]!=14
        or primary["study_cluster_df"]!=12
        or primary["n_effect_rows"]!=444
    ):
        raise ValueError("Original primary design identity changed")
    cap=fit(d,"cap99")
    unweighted=fit(d,"unweighted")
    LOO=[]
    for name in sorted(d.Study.astype(str).unique()):
        sub=d.loc[~d.Study.eq(name)]
        o=fit(sub,"ivw")
        LOO.append({
            "excluded_original_source_study":name,
            "beta":o["beta_long_minus_short_days_per_C"],
            "ci95":o["ci95"],
            "n_remaining_studies":o["n_independent_source_studies"],
            "n_remaining_effect_rows":o["n_effect_rows"],
        })
    individual=descriptive_study_contrasts(d)
    positive=sum(v["descriptive_IVW_long_minus_short"]>0 for v in individual)
    negative=sum(v["descriptive_IVW_long_minus_short"]<0 for v in individual)
    if positive+negative!=13:
        raise ValueError("Descriptive original source contrasts include zero")
    return {
        "status":"POST_OPEN_WITHIN_STUDY_SOURCE_ASSOCIATION_NOT_CAUSAL_INFORMATION_USE",
        "as_of":"2026-11-19",
        "source":"Usui 2017 original GitHub E6 archived derived effect rows; exact SHA verified by shared loader",
        "source_provenance":"known eBird study excluded, original Lithuanian source unverified, no complete auxiliary-source eBird-free certification",
        "frozen_model_contract":"docs/PAYOFF_B_E6_WITHIN_STUDY_FIXED_EFFECT_FREEZE_20261119.md",
        "registered_after_original_prior_E6_outcome_opened":True,
        "n_original_source_described_usable_rows":676,
        "n_original_source_described_studies":26,
        "n_source_studies_with_both_migration_classes":13,
        "n_source_effects_in_crossed_studies":444,
        "primary_study_fixed_effect_ivw":primary,
        "weight_capped_99_sensitivity":cap,
        "unweighted_sensitivity":unweighted,
        "leave_one_original_study_out":{
            "n_repeats":len(LOO),
            "all_positive_estimates":all(r["beta"]>0 for r in LOO),
            "min_beta":float(min(r["beta"] for r in LOO)),
            "max_beta":float(max(r["beta"] for r in LOO)),
            "all_CI_lower_positive":all(r["ci95"][0]>0 for r in LOO),
            "per_original_study":LOO,
        },
        "study_descriptive_unadjusted_signs":{
            "positive":positive,
            "negative":negative,
            "per_study":individual,
        },
        "no_new_source_independent_replication":True,
        "no_biological_fitness_or_cue_exposure_fitted":True,
        "no_information_distance_causal_mechanism_identified":True,
        "frozen_V7_individual_q_times_geography_urgency":"NOT_ESTIMABLE",
        "result_interpretation":"Within-source study intercepts do not remove the published migration-distance temperature response gradient in this pre-declared study-crossed source subset. No animal cue, actionability or causal information-distance effect is identified.",
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifact-zip",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    result=run(read_verified_artifact(args.artifact_zip))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "primary":result["primary_study_fixed_effect_ivw"],
        "LOO_range":[result["leave_one_original_study_out"]["min_beta"],
                     result["leave_one_original_study_out"]["max_beta"]],
        "study_contrast_signs":result["study_descriptive_unadjusted_signs"]["positive"],
        "n_studies":13,
        "cause_identified":False,
    },ensure_ascii=False))


if __name__=="__main__":
    main()
