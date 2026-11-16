"""Post-open source-measurement and calendar selection audit for Scottish mass.

The original data documentation explicitly states caterpillars were weighed
ONLY FROM 2017. Earlier years must not be represented as measured mass; their
potential structural zero is not a measured seasonal mass curve. Run fixed
models unchanged on all named subpanels, including null outcomes, with full
year and site holdouts. Not a confirmatory pre-registered second test.
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from scripts.payoff_b_scotland_measured_mass_window import (
    panel_from_original, cv, source_data, original_mass_bounds,
    MIN_SITEYEARS, MIN_SITES, MIN_YEARS, MIN_NESTS
)
from scripts.payoff_b_scotland_hatch_resource_admission import numeric


def mass_reporting_by_year(rows):
    by=defaultdict(Counter)
    for row in rows:
        yr=numeric(row.get("year"))
        if yr is None:
            continue
        yr=int(yr)
        stats=by[yr]
        stats["source_branch_rows"]+=1
        tmp=Counter()
        mass=original_mass_bounds(row,tmp)
        stats.update(tmp)
        if mass is not None:
            stats["mass_bound_accepted_branch_rows"]+=1
            if str(row.get("caterpillars") or "").strip() not in ("0","0.0"):
                stats["mass_bound_accepted_positive_caterpillar_branches"]+=1
    return {str(y):dict(v) for y,v in sorted(by.items())}


def summarize_cv(rows):
    out={}
    for group in ("year","site"):
        a=cv(rows,group)
        s={name:value["equal_fold_mse"] for name,value in a["models"].items()}
        out[group]={
            "n_folds":a["n_folds"],
            "mse_by_model":s,
            "extra_mass_lower_vs_count":s["B_plus_count"]-s["D0_count_mass_lower"],
            "extra_mass_upper_vs_count":s["B_plus_count"]-s["D1_count_mass_upper"],
            "mass_lower_vs_peak":s["A_climate_peak_gap"]-s["C0_mass_lower"],
            "mass_upper_vs_peak":s["A_climate_peak_gap"]-s["C1_mass_upper"],
            "heldout":{
                label:{
                    "n_siteyears":v["siteyears"],
                    "mass_lower_minus_count":
                        a["models"]["B_plus_count"]["heldout_folds"][label]["mse"]-
                        a["models"]["D0_count_mass_lower"]["heldout_folds"][label]["mse"],
                    "mass_upper_minus_count":
                        a["models"]["B_plus_count"]["heldout_folds"][label]["mse"]-
                        a["models"]["D1_count_mass_upper"]["heldout_folds"][label]["mse"]
                }
                for label,v in a["models"]["B_plus_count"]["heldout_folds"].items()
            },
        }
    return out


def evaluate(rows):
    distinct_years=sorted({r["year"] for r in rows})
    n_sites=len({r["site"] for r in rows})
    n_nests=sum(r["n_nests"] for r in rows)
    status={
        "siteyears":len(rows),
        "sites":n_sites,
        "years":distinct_years,
        "nests":n_nests,
        "n_siteyears_by_year":dict(Counter(str(r["year"]) for r in rows))
    }
    if (len(rows)<MIN_SITEYEARS or n_sites<MIN_SITES
        or len(distinct_years)<MIN_YEARS or n_nests<MIN_NESTS):
        return {**status, "admission":"NO_GO_SAMPLE_SUPPORT", "fitted":False}
    return {**status,
        "admission":"ADMITTED_POST_OPEN_SENSITIVITY",
        "fitted":True,
        "metrics":summarize_cv(rows)
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    data=source_data()
    rows,qa=panel_from_original(data)
    variants={
        "all_original_prior_opened":rows,
        "weighed_since_2017_no_2014":[r for r in rows if r["year"]>=2017],
        "covid_2020_excluded":[r for r in rows if r["year"]!=2020],
        "weighed_since_2017_and_2020_excluded":[
            r for r in rows if r["year"]>=2017 and r["year"]!=2020],
    }
    report={
        "status":"PAYOFF_B_SCOTLAND_MEASURED_MASS_SOURCE_YEAR_POSTOPEN_AUDIT",
        "year_weight_source":"Official EIDC supporting data description: samples weighed from 2017",
        "previous_primary_result_was_opened":True,
        "posthoc_source_measurement_validity_check_not_confirmation":True,
        "no_outcome_model_or_hyperparameter_modified":True,
        "source_original": "EIDC 10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3",
        "mass_source_status_by_year":mass_reporting_by_year(data["data/branch_beating.csv"]),
        "subpanels":{name:evaluate(x) for name,x in variants.items()},
        "evidence_not_actual_diet_or_game_payoff":True,
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(report,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
