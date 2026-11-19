#!/usr/bin/env python3
"""Post-open original Greenland goose within-year weather assignment control.

Keep year-specific freezing distribution, all outcomes, bird IDs, original
weather and dates fixed; shuffle only the mapping of stage3 freezing values
to bird-years WITHIN each year. Never a randomized ecological experiment.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from scripts.payoff_b_gwfg_lagged_weather_to_feeding import (
    original_source_digest, make_bird_years,
    _predictive_group_cv, PREDICTION_BASE,
    PREDICTION_WITH_EARLY_FREEZE, RIDGE_ALPHA
)

SEED=20261119
PERMUTATIONS=99
FROZEN_YEARS=(1,2,3,4,5)


def within_year_shuffle(x:pd.DataFrame,rng)->pd.DataFrame:
    q=x.copy()
    if tuple(sorted(q.year_index.unique())) != FROZEN_YEARS:
        raise ValueError("Original five published calendar years changed")
    for year in FROZEN_YEARS:
        idx=q.index[q.year_index.eq(year)]
        original=x.loc[idx,"freeze3_10pp"].to_numpy(float)
        shuffled=rng.permutation(original)
        q.loc[idx,"freeze3_10pp"]=shuffled
        # Exact original weather marginal distribution preserved per year.
        if not np.array_equal(np.sort(original),np.sort(shuffled)):
            raise ValueError("Within-year source weather distribution drifted")
    # No outcome or other predictor should have changed.
    for col in x.columns:
        if col=="freeze3_10pp":
            continue
        if not x[col].equals(q[col]):
            raise ValueError("Permutation altered unrelated original source column")
    return q


def updated_ridge_mse(x:pd.DataFrame,grouping:str)->float:
    if grouping not in ("bird_id","year_index"):
        raise ValueError("Only declared independent group folds")
    groups=x[grouping].to_numpy()
    target=x.feed4.to_numpy(float)
    predicted=np.empty(len(x),float)
    for train,test in LeaveOneGroupOut().split(x,target,groups):
        model=make_pipeline(StandardScaler(),Ridge(alpha=RIDGE_ALPHA))
        model.fit(x.iloc[train][PREDICTION_WITH_EARLY_FREEZE],target[train])
        predicted[test]=model.predict(x.iloc[test][PREDICTION_WITH_EARLY_FREEZE])
    return float(mean_squared_error(target,predicted))


def run(x:pd.DataFrame)->dict:
    if (len(x),x.bird_id.nunique(),x.year_index.nunique())!=(107,49,5):
        raise ValueError("Frozen original source support changed")
    baseline={}
    for grouping in ("bird_id","year_index"):
        declared=_predictive_group_cv(
            x,PREDICTION_BASE,PREDICTION_WITH_EARLY_FREEZE,grouping)
        independently_repeated=updated_ridge_mse(x,grouping)
        if abs(independently_repeated-declared["augmented_loss"])>1e-11:
            raise ValueError("Frozen prior ridge forecast was not reproduced")
        baseline[grouping]={
            "baseline_MSE":declared["baseline_loss"],
            "augmented_MSE":declared["augmented_loss"],
            "observed_early_freezing_gain":(
                declared["baseline_loss"]-declared["augmented_loss"]
            ),
            "n_independent_original_holdout_units":declared["n_holdout_folds"],
        }
    rng=np.random.default_rng(SEED)
    null={key:[] for key in baseline}
    for _ in range(PERMUTATIONS):
        perm=within_year_shuffle(x,rng)
        for grouping in null:
            mse=updated_ridge_mse(perm,grouping)
            null[grouping].append(baseline[grouping]["baseline_MSE"]-mse)
    outputs={}
    for key in baseline:
        vals=np.asarray(null[key],float)
        obs=baseline[key]["observed_early_freezing_gain"]
        outputs[key]={
            **baseline[key],
            "n_within_year_shuffles":PERMUTATIONS,
            "null_gain_median":float(np.median(vals)),
            "null_gain_mean":float(np.mean(vals)),
            "null_gain_quantiles_05_95":[float(k) for k in np.quantile(vals,[.05,.95])],
            "n_null_shuffles_with_nonnegative_gain":int(np.sum(vals>=0)),
            "n_null_shuffles_at_least_as_large_as_observed":int(np.sum(vals>=obs)),
            "post_open_randomization_tail_fraction":float((1+np.sum(vals>=obs))/(PERMUTATIONS+1)),
            "source_year_distributions_preserved":True,
            "individual_and_weather_outcome_not_permuted":True,
            "observational_permutation_not_causal_p_value":True,
        }
    return {
        "result_id":"PAYOFF_B_GWFG_WITHIN_YEAR_SOURCE_WEATHER_PERMUTATION_20261119",
        "status":"POST_OPEN_EXPLORATORY_NONEXCHANGEABLE_PERMUTATION_DIAGNOSTIC",
        "original_source":"Schindler et al 2024 Proc R Soc B original stage CSV",
        "source_frozen_stage3_to_stage4_model":"docs/PAYOFF_B_GWFG_STAGE3_TO_STAGE4_FREEZE_20261119.md",
        "fixed_postopen_permutation_design":"docs/PAYOFF_B_GWFG_WITHIN_YEAR_FREEZE_PERMUTATION_FREEZE_20261119.md",
        "source_years":[2018,2019,2020,2021,2022],
        "n_bird_years":len(x),
        "n_original_birds":int(x.bird_id.nunique()),
        "n_permutations":PERMUTATIONS,
        "fixed_seed":SEED,
        "heldout_diagnostics":outputs,
        "claims":{
            "stage3_freeze_weather_is_actual_forecast_belief":False,
            "shuffled_weather_is_randomized_natural_experiment":False,
            "permutation_preserves_unobserved_individual_habitat":False,
            "new_independent_natural_system":False,
            "causal_downstream_feedback_identified":False,
            "theoretical_information_deadline_estimated":False,
            "original_goose_V7_qxU_unlocked":False,
            "original_paper_prior_art_unchanged":True,
            "new_breeding_success_effect_fitted":False,
            "raw_animal_IDs_exported":False
        }
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    source=original_source_digest(args.source)
    d=make_bird_years(pd.read_csv(args.source),strict=True)
    result=run(d)
    result["original_source_provenance"]=source
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "bird_holdout":result["heldout_diagnostics"]["bird_id"],
        "year_holdout":result["heldout_diagnostics"]["year_index"],
        "real_information_deadline_estimated":False
    },ensure_ascii=False))


if __name__=="__main__":
    main()
