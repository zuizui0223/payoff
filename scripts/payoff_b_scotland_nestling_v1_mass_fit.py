"""PAYOFF-B Scottish blue tit nestling early body mass vs actual sampled prey mass.

Original EIDC v1 nestling weight g (not biomass growth velocity).
Frozen design in docs/PAYOFF_B_SCOTLAND_NESTLING_V1MASS_RESOURCE_FREEZE_20261116.md
Source admission matches hatch, nest box, 5-9 day observation and 5-day
pre-visit food window, excluding manipulated nests and pre-2017 mass years.
No direct ingestion, causation or migration game effect is measured.
"""
import argparse
import json
import math
from collections import Counter
from pathlib import Path
import numpy as np
from scripts.payoff_b_2023_resource_fitness_loyo import fit_predict
from scripts.payoff_b_scotland_nestling_v1_mass_admission import (
    load_original, common_support
)

MIN_SITEYEARS=60
MIN_SITES=20
MIN_YEARS=3
MIN_NESTS=150
MIN_CHICKS=400

BASE=["year","latitude","elevation","hatch_doy","clutch_size",
      "v1_first_visit_age_proxy","spring_temperature","log_season_peak",
      "signed_peak_minus_hatch_days"]
MODELS={
    "A_climate_peak_gap_age":BASE,
    "B_plus_count5":BASE+["log_count_window5"],
    "C0_plus_mass_lower5":BASE+["log_mass_lower_window5"],
    "C1_plus_mass_upper5":BASE+["log_mass_upper_window5"],
    "D0_count_plus_mass_lower5":BASE+["log_count_window5",
                                     "log_mass_lower_window5"],
    "D1_count_plus_mass_upper5":BASE+["log_count_window5",
                                     "log_mass_upper_window5"],
}


def validate(rows,group):
    if not rows:
        raise ValueError("No admitted nestling mass site-years")
    ys=np.asarray([r["y_mean_v1mass_g"] for r in rows],float)
    groups=sorted({r[group] for r in rows})
    out={}
    for key,cols in MODELS.items():
        X=np.asarray([[r[c] for c in cols] for r in rows],dtype=float)
        squared=np.empty(len(rows),dtype=float)
        folds={}
        for g in groups:
            held=np.asarray([r[group]==g for r in rows],dtype=bool)
            train=~held
            if train.sum()<max(12,len(cols)+3):
                raise ValueError("Too few independent siteyears in training fold")
            pred=fit_predict(X[train],ys[train],X[held])
            err=(ys[held]-pred)**2
            squared[held]=err
            folds[str(g)]={"n_siteyears":int(held.sum()),
                           "mse_g_squared":float(err.mean())}
        out[key]={
            "equal_fold_mse_g_squared":float(np.mean([p["mse_g_squared"]
                                                    for p in folds.values()])),
            "pooled_equal_siteyear_mse_g_squared":float(squared.mean()),
            "heldout_folds":folds
        }
    return {"n_folds":len(groups),"source_siteyears":len(rows),"models":out}


def summarize(rows):
    results={}
    for key in ("year","site"):
        a=validate(rows,key)
        m=a["models"]
        score=lambda n:m[n]["equal_fold_mse_g_squared"]
        results[key]={
            "n_folds":a["n_folds"],
            "n_siteyears":len(rows),
            "models":m,
            "extra_mass_lower_over_count":score("B_plus_count5")-
                                          score("D0_count_plus_mass_lower5"),
            "extra_mass_upper_over_count":score("B_plus_count5")-
                                          score("D1_count_plus_mass_upper5"),
            "mass_count_lower_over_climate":score("A_climate_peak_gap_age")-
                                            score("D0_count_plus_mass_lower5"),
            "mass_count_upper_over_climate":score("A_climate_peak_gap_age")-
                                            score("D1_count_plus_mass_upper5"),
        }
    yrs=sorted({r["year"] for r in rows})
    y=results["year"]["models"]
    each_year=[]
    for yr in yrs:
        m=lambda k:y[k]["heldout_folds"][str(yr)]["mse_g_squared"]
        d0=m("B_plus_count5")-m("D0_count_plus_mass_lower5")
        d1=m("B_plus_count5")-m("D1_count_plus_mass_upper5")
        a0=m("A_climate_peak_gap_age")-m("D0_count_plus_mass_lower5")
        a1=m("A_climate_peak_gap_age")-m("D1_count_plus_mass_upper5")
        each_year.append({"year":yr,"siteyears":
            y["B_plus_count5"]["heldout_folds"][str(yr)]["n_siteyears"],
            "extra_mass_low":d0,"extra_mass_high":d1,
            "above_climate_low":a0,"above_climate_high":a1,
            "all_four_positive":all(v>0 for v in (d0,d1,a0,a1))})
    result={
        "results":results,
        "yearly_lower_upper":each_year,
        "required_successful_year_folds":math.ceil(0.8*len(yrs)),
        "observed_all_four_positive_years":sum(v["all_four_positive"] for v in each_year)
    }
    fullgate=(
        all(results[k][field]>0
            for k in ("year","site")
            for field in ("extra_mass_lower_over_count",
                          "extra_mass_upper_over_count",
                          "mass_count_lower_over_climate",
                          "mass_count_upper_over_climate"))
        and result["observed_all_four_positive_years"] >=
             result["required_successful_year_folds"])
    result["gate"]="EXPLORATORY_NESTLING_CONDITION_INCREMENT" if fullgate \
                   else "HOLD_NO_GENERAL_NESTLING_BODY_MASS_PREDICTIVE_INCREMENT"
    return result


def run(rows,qa):
    years=sorted({r["year"] for r in rows})
    sites=sorted({r["site"] for r in rows})
    nests=sum(r["n_nests"] for r in rows)
    chicks=sum(r["n_chicks"] for r in rows)
    admitted=(qa["source_gate_pass"] and len(rows)>=MIN_SITEYEARS and
              len(sites)>=MIN_SITES and len(years)>=MIN_YEARS and
              nests>=MIN_NESTS and chicks>=MIN_CHICKS)
    out={
      "status":"PAYOFF_B_EIDC_NESTLING_V1_BODY_MASS_ORIGINAL_LOYO_LOSO",
      "frozen_before_new_body_mass_fit":
          "docs/PAYOFF_B_SCOTLAND_NESTLING_V1MASS_RESOURCE_FREEZE_20261116.md",
      "original_EIDC_csv_content_verified":True,
      "source":"10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3",
      "siteyears":len(rows),"sites":len(sites),"years":years,
      "nest_boxes":nests,"individual_first_visit_weight_rows":chicks,
      "source_qa":qa,
      "outcome":"siteyear average nest mean first-visit nestling mass in g",
      "previsit_food_source":"5 days from first recorded hatch, no future food",
      "food_mass":"source g per standardized beating, left censor bounds 0..0.02g",
      "independent_unit":"siteyear; independent entire calendar year/site held out",
      "not_caused_by_food_or_direct_feeding":True,
      "does_not_test_information_or_recourse":True,
      "post_prior_outcome_exploratory":True,
      "admitted_for_prediction":admitted
    }
    if not admitted:
        out["gate"]="NO_GO_EARLY_MASS_SOURCE_PANEL"
        return out
    out["primary"]=summarize(rows)
    out["gate"]=out["primary"]["gate"]
    no20=[r for r in rows if r["year"]!=2020]
    if len(no20)>=MIN_SITEYEARS and len({r["year"] for r in no20})>=MIN_YEARS and len({r["site"] for r in no20})>=MIN_SITES and sum(r["n_nests"] for r in no20)>=MIN_NESTS:
        out["exclude_2020_sensitivity"]={
           "admitted":True,"siteyears":len(no20),
           "nests":sum(r["n_nests"] for r in no20),
           "results":summarize(no20),
           "does_not_replace_main_result":True}
    else:
        out["exclude_2020_sensitivity"]={
           "admitted":False,"siteyears":len(no20)}
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    qa,rows=common_support(load_original(),return_panel=True)
    out=run(rows,qa)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(out,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
