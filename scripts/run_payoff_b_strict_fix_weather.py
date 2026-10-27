#!/usr/bin/env python3
"""Post-outcome strict original GPS fix-level weather sensitivity.

The source filter requires all original GPS fixes in all three original
stationary anchor days to lie inside the original 30km center. Same
northward/stay labels and original NASA daily prior-day weather.
This is NOT confirmatory cue/behavior/fitness inference. Threatened
species identities, places and real dates are never exported.
"""
from __future__ import annotations
import argparse,json,tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path

from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_unopened_gps_source import SOURCES
from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_payoff_b_predecision_candidates import daily_source_positions
from scripts.qc_payoff_b_complete_stationary_riskset import collect
from scripts.qc_payoff_b_riskday_fix_integrity import audit_fixes
from scripts.qc_payoff_b_strict_fix_source_overlap import (
    filtered_source_gate,ORIGINAL_CLEAN_COUNT,SOURCE_LIST
)
from scripts.run_payoff_b_full_riskday_daily_weather import (
    batch_key,event_prior_weather,download_batch,grid_cell
)
from scripts.audit_payoff_b_weather_block_dependence import (
    complete_matched_strata,estimate_from_strata,block_sensitivity
)

CASE="NORTHWARD_CANDIDATE"
STAY="STAYED_TWO_DAYS"
COMPLETE_THRESHOLD=.95
MAX_REQUESTS=500
BOOT_DRAWS=3000


def read_source(system,path):
    if system=="egyptian_vulture":
        src=SOURCES[system]
        return src["doi"],src["taxon"],download_verified(src,path)
    doi,taxon,sensor,checksum=origin_source(system,path)
    return doi,taxon,checksum


def run(system,fetch=download_batch):
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"original_source.csv"
        doi,taxon,checksum=read_source(system,path)
        groups,_,_=daily_source_positions(path,taxon)
        source,_,_,_=collect(groups)
        aggregate,mask=audit_fixes(path,source,taxon,return_private_mask=True)
        plan=filtered_source_gate(source,mask)
        counts=plan["strict_all_3days_source_label_counts"]
        baseline=(plan["strict_all_3days_fix_within_30km_source_riskdays"],
                  counts.get(CASE,0),counts.get(STAY,0))
        if baseline!=ORIGINAL_CLEAN_COUNT[system]:
            raise ValueError("Original strict GPS source has drifted")
        selection=[r for r,good in zip(source,mask)
                   if good and r[3] in (CASE,STAY)]
        if not plan["source_overlap_preweather_admission"]["passed"]:
            return {
                "status":"NOT_ESTIMABLE_STRICT_SOURCE_OVERLAP",
                "source_doi":doi,"original_source_checksum":checksum,
                "source_gate":plan,
                "public_meteorology_queries_made":0,
                "environmental_effect_fitted":False,
            }
        keys=sorted({batch_key(day,site) for _,day,site,_ in selection})
        if (len(keys)>MAX_REQUESTS or len(keys)!=
                plan["strict_case_and_stay_weather_source_query_plan"]["unique_grid_calendar_months"]):
            raise ValueError("Weather batch source inventory changed")
        values={};errors=Counter()
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures={pool.submit(fetch,key):key for key in keys}
            for fut in as_completed(futures):
                k=futures[fut]
                try:values[k]=fut.result()
                except Exception as e:errors[type(e).__name__]+=1
        complete=[];n=Counter();missing=Counter()
        for (tax,ident,year),day,site,label in selection:
            batch=values.get(batch_key(day,site))
            met=event_prior_weather(batch,day) if batch is not None else None
            if met is None:
                missing[label]+=1
                continue
            complete.append((ident,day,grid_cell(site),label,met))
            n[label]+=1
        if any(n[k]<COMPLETE_THRESHOLD*counts.get(k,0) for k in (CASE,STAY)):
            return {"status":"NOT_ESTIMABLE_WEATHER_MISSING",
                    "source_doi":doi,"source_gate":plan,
                    "completed_source_classes":dict(n),
                    "missing_source_classes":dict(missing),
                    "failed_requests":dict(errors)}
        strata,info=complete_matched_strata(complete)
        required=plan["strict_case_and_stay_weather_source_query_plan"]
        if (info["matched_strata_count"]!=
               required["grid_months_with_both_northward_and_stay_observations"]
            or info["case_risk_days_in_matched_strata"]!=
               required["northward_case_days_in_overlap_gridmonths"]):
            raise ValueError("Source cases changed during weather matching")
        result=estimate_from_strata(strata)
        sensitivity={
            scale:block_sensitivity(strata,scale,draws=BOOT_DRAWS,seed=20261022)
            for scale in ("grid_half_degree","weather_block_2_degree",
                          "weather_episode_year_month")
        }
        return {
            "status":"STRICT_SOURCE_WEATHER_SENSITIVITY_COMPLETE",
            "source_doi":doi,"source_taxon":taxon,
            "original_CC0_checksum":checksum,
            "original_source_riskday_n":len(source),
            "strict_all_fix_stable_riskday_n":baseline[0],
            "strict_source_case_stay_counts":dict(sorted(counts.items())),
            "weather_complete_by_class":dict(sorted(n.items())),
            "public_weather_batch_n":len(keys),
            "public_weather_errors":dict(sorted(errors.items())),
            "matched_source_strata":info,
            "strict_fix_source_case_weighted_weather_contrasts":
                result["case_weighted_difference"],
            "post_outcome_weather_block_sensitivity":sensitivity,
            "selection_policy":"All original prior-3day GPS fixes <=30km; no source outcome reclassification",
            "individual_perceived_weather_or_fitness_observed":False,
            "causal_migration_effect_estimated":False,
            "raw_animal_dates_sites_or_IDs_exported":False,
        }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--system",choices=SOURCE_LIST,required=True)
    ap.add_argument("--out",type=Path,
                    default=Path("outputs/payoff_b_strict_fix_weather"))
    a=ap.parse_args()
    o={"schema":"payoff_b_4guild_strict_fix_source_weather_sensitivity_v1",
       "system":a.system,
       "science":"POST_OUTCOME_MEASUREMENT_SENSITIVITY_NOT_CONFIRMATORY"}
    try:o["result"]=run(a.system)
    except (OSError,ValueError,TypeError) as e:
        o["result"]={"status":"SOURCE_OR_API_GATE_FAILED",
                     "error":type(e).__name__+": "+str(e)[:280]}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/(a.system+".json")).write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(o,ensure_ascii=False,indent=2))
    if o["result"]["status"] not in (
        "NOT_ESTIMABLE_STRICT_SOURCE_OVERLAP",
        "NOT_ESTIMABLE_WEATHER_MISSING",
        "STRICT_SOURCE_WEATHER_SENSITIVITY_COMPLETE"):
        raise SystemExit("Original strict source weather audit failed")
if __name__=="__main__":main()
