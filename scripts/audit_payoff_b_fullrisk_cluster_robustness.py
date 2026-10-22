#!/usr/bin/env python3
"""Post-outcome robustness audit of full GPS riskday weather contrasts.

Uses exactly the original 5509 stationary-day observations and 809 original
daily weather batches. Estimates coarse grid-year-month case-stay anomaly
contrasts under whole-animal resampling and leave-one-year-out perturbations.

NOT a registered confirmatory test. Does not identify actual cue uptake,
flight-height winds, decision recourse, reproductive benefits or causality.
All animal IDs, source sites and event dates remain internal to the runner.
"""
from __future__ import annotations
import argparse,json,random,tempfile
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path

from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_predecision_candidates import SYSTEMS,daily_source_positions
from scripts.qc_payoff_b_complete_stationary_riskset import collect
from scripts.run_payoff_b_full_riskday_daily_weather import (
    batch_key,download_batch,event_prior_weather,EXPECTED,WORKERS,
)
from scripts.run_payoff_b_stork_stage_handoff_pilot import percentile

VARS=("T2M_anomaly","WS10M_anomaly","V10M_anomaly",
      "ALLSKY_SFC_SW_DWN_anomaly")
CASE="NORTHWARD_CANDIDATE"
STAY="STAYED_TWO_DAYS"
BOOT=1000
SEED=20261022
MIN_SOURCE_COMPLETENESS=.90
MIN_OVERLAP_CASES=25
MIN_OVERLAP_STRATA=10


def cell_key(day,site):
    from scripts.run_payoff_b_full_riskday_daily_weather import grid_cell
    return (day.year,day.month,grid_cell(site))


def weighted_gridmonth_contrast(observations,multiplicity=None):
    """Original days are in-memory (taxon, individual, year, day, grid, label, weather)."""
    m=defaultdict(lambda:defaultdict(
        lambda:{"sum":Counter(),"n":0}))
    for ident,day,cell,label,weather in observations:
        if label not in (CASE,STAY):continue
        weight=multiplicity.get(ident,0) if multiplicity is not None else 1
        if weight<=0:continue
        stratum=(day.year,day.month,cell)
        e=m[stratum][label]
        e["n"]+=weight
        for v in VARS:e["sum"][v]+=weight*weather[v]
    effects=Counter()
    matched_cases=0
    nstrata=0
    for v in m.values():
        if v[CASE]["n"]==0 or v[STAY]["n"]==0:
            continue
        nstrata+=1
        ncase=v[CASE]["n"]
        matched_cases+=ncase
        for name in VARS:
            diff=v[CASE]["sum"][name]/ncase-v[STAY]["sum"][name]/v[STAY]["n"]
            effects[name]+=ncase*diff
    return {
       "n_gridmonth_strata_with_both_labels":nstrata,
       "n_original_case_day_weights_in_overlap":matched_cases,
       "source_case_weighted_contrasts":{
           name:effects[name]/matched_cases if matched_cases else None
           for name in VARS
       },
    }


def uncertainty(original,bootstrap=BOOT,seed=SEED):
    base=weighted_gridmonth_contrast(original)
    identities=sorted({key for key,*_ in original})
    rng=random.Random(seed)
    boots=defaultdict(list)
    failed=0
    n_overlap=[]
    for _ in range(bootstrap):
        frequency=Counter(rng.choices(identities,k=len(identities)))
        result=weighted_gridmonth_contrast(original,frequency)
        if (result["n_gridmonth_strata_with_both_labels"]<MIN_OVERLAP_STRATA
                or result["n_original_case_day_weights_in_overlap"]<
                MIN_OVERLAP_CASES):
            failed+=1
            continue
        n_overlap.append(result["n_original_case_day_weights_in_overlap"])
        for var,val in result["source_case_weighted_contrasts"].items():
            boots[var].append(val)
    interval={}
    if bootstrap-failed>=.9*bootstrap:
        for var,values in boots.items():
            interval[var]=[percentile(values,.025),percentile(values,.975)]
        status="DESCRIPTIVE_CLUSTER_BOOTSTRAP_ESTIMABLE"
    else:
        status="BOOTSTRAP_NOT_ESTIMABLE_EXCESSIVE_SOURCE_OVERLAP_LOSS"
        interval={}
    by_year=defaultdict(list)
    for row in original:by_year[row[1].year].append(row)
    year_sensitivity={}
    for year in sorted(by_year):
        subset=[row for row in original if row[1].year!=year]
        out=weighted_gridmonth_contrast(subset)
        year_sensitivity[str(year)]={
            "remaining_gridmonth_overlap":out["n_gridmonth_strata_with_both_labels"],
            "remaining_case_weight_in_overlap":
                out["n_original_case_day_weights_in_overlap"],
            "case_weighted_contrasts":out["source_case_weighted_contrasts"],
        }
    return {
        "status":status,"original_effect":base,
        "animal_cluster_units":len(identities),
        "animal_history_resampled_across_all_years":True,
        "bootstrap_replicates_requested":bootstrap,
        "bootstrap_valid":bootstrap-failed,
        "bootstrap_lost_or_underrepresented_source_overlap":failed,
        "cluster_bootstrap_95pct_descriptive_intervals":interval,
        "leave_one_source_year_out_descriptive":year_sensitivity,
        "bootstrap_accounts_for_shared_weather_grid_between_animals":False,
        "bootstrap_estimates_biological_causal_effect":False,
    }


def run_system(system,fetch=download_batch):
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"original.csv"
        doi,taxon,sensor,checks=origin_source(system,path)
        tracks,quality,idcol=daily_source_positions(path,taxon)
        allrisk,source_counts,_,_=collect(tracks)
        keynames=("all_at_risk_stationary_days","NORTHWARD_CANDIDATE",
                  "STAYED_TWO_DAYS","OTHER_MOVEMENT","CENSORED")
        observed=tuple(source_counts[k] for k in keynames)
        if observed!=EXPECTED[system][:5]:
            raise ValueError("Original source riskday population changed")
        keys={batch_key(day,site) for group,day,site,label in allrisk}
        if len(keys)!=EXPECTED[system][5]:
            raise ValueError("Original fixed gridmonth source count changed")
        cached={}
        failed=Counter()
        with ThreadPoolExecutor(max_workers=WORKERS) as executor:
            futures={executor.submit(fetch,k):k for k in sorted(keys)}
            for fut in as_completed(futures):
                key=futures[fut]
                try:cached[key]=fut.result()
                except Exception as e:failed[type(e).__name__]+=1
        values=[]
        coverage=Counter()
        for (tax,individual,year),day,site,label in allrisk:
            original=cached.get(batch_key(day,site))
            if original is None:
                coverage[label+"_FAILED_BATCH"]+=1
                continue
            weather=event_prior_weather(original,day)
            if weather is None:
                coverage[label+"_INCOMPLETE_PRIOR_WEATHER"]+=1
                continue
            coverage[label]+=1
            if label in (CASE,STAY):
                values.append((individual,day,cell_key(day,site)[2],label,weather))
        if any(coverage[class_name]<source_counts[class_name]*MIN_SOURCE_COMPLETENESS
               for class_name in (CASE,STAY)):
            return {"status":"NOT_ESTIMABLE_SOURCE_MISSINGNESS",
                    "weather_batches":len(keys),
                    "error_groups":dict(sorted(failed.items()))}
        result=uncertainty(values)
        if (result["original_effect"]["n_gridmonth_strata_with_both_labels"]<
               MIN_OVERLAP_STRATA or
            result["original_effect"]["n_original_case_day_weights_in_overlap"]<
               MIN_OVERLAP_CASES):
            return {"status":"NOT_ESTIMABLE_SOURCE_OVERLAP"}
        return {
            "status":"SOURCE_SOURCE_YEAR_ROBUSTNESS_DESCRIPTIVES_COMPLETE",
            "source_doi":doi,"source_taxon":taxon,
            "original_source_checksum":checks,
            "source_riskday_observations":len(allrisk),
            "weather_complete_classes":dict(sorted(coverage.items())),
            "retrieved_month_grid_year_batches":len(keys),
            "failed_batches":dict(sorted(failed.items())),
            "sensitivity":result,
            "pvalue_or_causal_claim":False,
            "raw_individual_date_grid_exported":False,
        }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--system",choices=SYSTEMS,required=True)
    parser.add_argument("--out",type=Path,
                        default=Path("outputs/payoff_b_fullrisk_robustness"))
    a=parser.parse_args()
    receipt={
        "schema":"payoff_b_fullrisk_postoutcome_animal_cluster_robustness_20261022",
        "system":a.system,
        "classification":"POST_OUTCOME_SENSITIVITY_NOT_CONFIRMATORY",
    }
    try:receipt["result"]=run_system(a.system)
    except Exception as e:
        receipt["result"]={"status":"SOURCE_OR_CLUSTER_INFERENCE_FAILED",
                           "error":type(e).__name__+": "+str(e)[:250]}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/(a.system+".json")).write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(receipt,indent=2,ensure_ascii=False))
    if receipt["result"]["status"]!="SOURCE_SOURCE_YEAR_ROBUSTNESS_DESCRIPTIVES_COMPLETE":
        raise SystemExit("Original cluster/year source robustness gate failed")


if __name__=="__main__":main()
