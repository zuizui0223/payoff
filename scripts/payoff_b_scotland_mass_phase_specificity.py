"""PAYOFF-B source-verified Scotland: hatch-window mass vs season mean mass.

Exploratory falsification of time-specific food availability rather than generic
resource magnitude. Freeze document:
docs/PAYOFF_B_SCOTLAND_MASS_PHASE_SPECIFICITY_FREEZE_20261116.md

Source from upstream SHA256-verified original UKCEH/EIDC CSVs.
No nest-level pseudo replication; no causal diet, intake or information game.
"""
import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from scripts.payoff_b_2023_resource_fitness_loyo import fit_predict
from scripts.payoff_b_scotland_measured_mass_window import (
    panel_from_original, source_mass
)
from scripts.payoff_b_scotland_hatch_window_fitness_loyo import source_data
from src.payoff_b_resource_contact import daily_resource_rates

SAMPLE_EXPECTED_SITEYEARS=138
SAMPLE_EXPECTED_NESTS=427
SAMPLE_EXPECTED_SITES=44
SAMPLE_EXPECTED_YEARS=(2018,2019,2020,2021)

BASE=["year","latitude","elevation","hatch_doy","clutch_size",
      "spring_temperature","log_season_peak","signed_peak_minus_hatch_days"]
COUNT=BASE+["log_hatch_window"]
MODELS={
    "A_climate_peak_gap":BASE,
    "B_plus_count":COUNT,
    "H0_count_plus_hatch_mass_lower":COUNT+["log_mass_window_lower"],
    "H1_count_plus_hatch_mass_upper":COUNT+["log_mass_window_upper"],
    "S0_count_plus_season_mass_lower":COUNT+["log_season_mass_lower"],
    "S1_count_plus_season_mass_upper":COUNT+["log_season_mass_upper"],
    "HS0_count_plus_hatch_and_season_lower":
        COUNT+["log_mass_window_lower","log_season_mass_lower"],
    "HS1_count_plus_hatch_and_season_upper":
        COUNT+["log_mass_window_upper","log_season_mass_upper"],
}


def season_means(source_data_rows):
    """Equal-weight mean of observed source sampling DATE mass rates.

    Uses the original site-year source mass data, no hatch date or fitness data,
    no filling missing observation dates. Original grams returned, not biomass/m2.
    """
    low,high,qa=source_mass(source_data_rows)
    if set(low)!=set(high):
        raise ValueError("Censor bounds have different original source siteyears")
    out={}
    days=[]
    for key in sorted(low):
        l,currency=daily_resource_rates(low[key])
        h,currency2=daily_resource_rates(high[key])
        if currency!="measured_mg_per_beating" or currency2!=currency:
            raise ValueError("Source resource currency changed")
        if [d for d,v in l]!=[d for d,v in h]:
            raise ValueError("Source observation dates differ across censor bounds")
        if len(l)<2:
            continue
        v0=sum(x for date,x in l)/(len(l)*1000)
        v1=sum(x for date,x in h)/(len(h)*1000)
        if v0>v1:
            raise ValueError("Source mass detection intervals reversed")
        out[key]={
            "log_season_mass_lower":math.log1p(v0),
            "log_season_mass_upper":math.log1p(v1),
            "n_observed_mass_dates":len(l),
            "season_mass_mean_lower_g_per_beat":v0,
            "season_mass_mean_upper_g_per_beat":v1,
            "first_mass_source_date_ordinal":l[0][0],
            "last_mass_source_date_ordinal":l[-1][0],
        }
        days.append(len(l))
    summary={
        "mass_source_date_qa":qa,
        "siteyears_with_two_or_more_mass_dates":len(out),
        "source_mass_dates_min":min(days) if days else None,
        "source_mass_dates_max":max(days) if days else None,
        "source_mass_dates_median":float(np.median(days)) if days else None,
        "source_mass_control":"arithmetic mean of directly observed sampled-date g per beat",
        "mass_source_season_not_time_integrated":True,
    }
    return out,summary


def build_panel(data):
    original,source_qa=panel_from_original(data)
    measured=[r.copy() for r in original if r["year"]>=2017]
    seasons,season_qa=season_means(data["data/branch_beating.csv"])
    missing=[]
    for row in measured:
        k=(row["site"],row["year"])
        if k not in seasons:
            missing.append(k)
        else:
            row.update(seasons[k])
    years=tuple(sorted({r["year"] for r in measured}))
    sites=len({r["site"] for r in measured})
    n_nests=sum(r["n_nests"] for r in measured)
    samples_ok=(len(measured)==SAMPLE_EXPECTED_SITEYEARS
                and n_nests==SAMPLE_EXPECTED_NESTS
                and sites==SAMPLE_EXPECTED_SITES
                and years==SAMPLE_EXPECTED_YEARS
                and not missing)
    support={
        "post_original_measured_years_only":list(SAMPLE_EXPECTED_YEARS),
        "n_siteyears":len(measured),"n_sites":sites,
        "n_nests":n_nests,"years":list(years),
        "siteyear_nest_set_matches_frozen_measurement_era":samples_ok,
        "missing_season_mass_siteyears":len(missing),
        "source_qa":source_qa,
        "season_mass_qa":season_qa,
    }
    return measured,support


def grouped_prediction(rows,fold_key):
    if not rows:
        raise ValueError("No verified source site-year panel")
    y=np.asarray([r["y_fledged_fraction"] for r in rows],float)
    groups=sorted({r[fold_key] for r in rows})
    folds={g:np.asarray([r[fold_key]==g for r in rows],bool) for g in groups}
    models={}
    for name,features in MODELS.items():
        X=np.asarray([[r[k] for k in features] for r in rows],float)
        errors=np.empty(len(rows))
        groupscores={}
        for label,mask in folds.items():
            train=~mask
            if train.sum()<max(12,len(features)+3):
                raise ValueError("Insufficient independent training siteyears")
            predicted=fit_predict(X[train],y[train],X[mask])
            sq=(y[mask]-predicted)**2
            errors[mask]=sq
            groupscores[str(label)]={"n_siteyears":int(mask.sum()),
                "mse":float(sq.mean())}
        models[name]={
            "equal_fold_mse":float(np.mean([x["mse"] for x in groupscores.values()])),
            "equal_siteyear_mse":float(errors.mean()),
            "heldout_folds":groupscores,
        }
    return {"n_folds":len(groups),"n_siteyears":len(rows),"model_results":models}


def interpret(rows):
    lo=grouped_prediction(rows,"year")
    so=grouped_prediction(rows,"site")
    contrasts={}
    for key,obj in (("loyo",lo),("loso",so)):
        m=obj["model_results"]
        mse=lambda name:m[name]["equal_fold_mse"]
        contrasts[key]={
            "phase_conditional_lower":mse("S0_count_plus_season_mass_lower")-
                                      mse("HS0_count_plus_hatch_and_season_lower"),
            "phase_conditional_upper":mse("S1_count_plus_season_mass_upper")-
                                      mse("HS1_count_plus_hatch_and_season_upper"),
            "hatch_vs_season_lower":mse("S0_count_plus_season_mass_lower")-
                                     mse("H0_count_plus_hatch_mass_lower"),
            "hatch_vs_season_upper":mse("S1_count_plus_season_mass_upper")-
                                     mse("H1_count_plus_hatch_mass_upper"),
            "season_mass_extra_lower":mse("B_plus_count")-
                                       mse("S0_count_plus_season_mass_lower"),
            "season_mass_extra_upper":mse("B_plus_count")-
                                       mse("S1_count_plus_season_mass_upper"),
        }
    years=sorted({r["year"] for r in rows})
    yearly=[]
    for year in years:
        label=str(year)
        m=lo["model_results"]
        dev=lambda key:m[key]["heldout_folds"][label]["mse"]
        low=dev("S0_count_plus_season_mass_lower")-dev(
                    "HS0_count_plus_hatch_and_season_lower")
        high=dev("S1_count_plus_season_mass_upper")-dev(
                    "HS1_count_plus_hatch_and_season_upper")
        yearly.append({"year":year,"n_siteyears":
            m["B_plus_count"]["heldout_folds"][label]["n_siteyears"],
            "phase_conditional_lower":low,
            "phase_conditional_upper":high,
            "both_positive":low>0 and high>0})
    required=math.ceil(.75*len(years))
    success=(all(contrasts[k][v]>0 for k in ("loyo","loso")
                 for v in ("phase_conditional_lower","phase_conditional_upper",
                           "hatch_vs_season_lower","hatch_vs_season_upper"))
             and sum(x["both_positive"] for x in yearly)>=required)
    return {
        "loyo":lo,"loso":so,"contrasts":contrasts,
        "heldout_year_phase_specificity":yearly,
        "years_both_censor_bounds_positive":sum(x["both_positive"] for x in yearly),
        "required_year_folds_positive":required,
        "gate":"EXPLORATORY_PHASE_SPECIFIC_PREDICTIVE_INCREMENT" if success
               else "HOLD_PHASE_SPECIFICITY_NOT_ESTABLISHED",
    }


def run(rows,support):
    admitted=bool(support["siteyear_nest_set_matches_frozen_measurement_era"])
    out={
        "status":"PAYOFF_B_SCOTLAND_ORIGINAL_PREY_MASS_PHASE_NEGATIVE_CONTROL",
        "freeze":"docs/PAYOFF_B_SCOTLAND_MASS_PHASE_SPECIFICITY_FREEZE_20261116.md",
        "previous_count_mass_result":"EXPLORATORY_RESTRICTED_INCREMENT",
        "previous_nestling_first_mass_result":"HOLD",
        "source_content_sha256_verified_by_import":True,
        "same_siteyear_nest_outcome_required":True,
        "analysis_after_prior_outcome_exploratory":True,
        "source_mass_g_per_standardized_beating_not_consumption":True,
        "phase_specificity_not_causal_information_game":True,
        "admitted":admitted,
        "source_audit":support,
    }
    if not admitted:
        out["gate"]="NO_GO_FROZEN_SOURCE_SAMPLE_MISMATCH"
        return out
    out["primary"]=interpret(rows)
    out["gate"]=out["primary"]["gate"]
    without20=[r for r in rows if r["year"]!=2020]
    if len(without20)>=60 and len({r["year"] for r in without20})>=3:
        out["exclude_2020_sensitivity"]={
            "n_siteyears":len(without20),
            "n_years":len({r["year"] for r in without20}),
            "results":interpret(without20),
            "does_not_replace_primary":True}
    else:
        out["exclude_2020_sensitivity"]={"gate":"NO_GO"}
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True,type=Path)
    args=parser.parse_args()
    rows,support=build_panel(source_data())
    o=run(rows,support)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(o,ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
