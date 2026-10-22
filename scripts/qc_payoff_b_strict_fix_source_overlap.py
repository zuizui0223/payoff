#!/usr/bin/env python3
"""Original GPS all-fix 3-day stationary riskset: overlap/source gate.

Measurement method introduced after the original weather associations.
No new climate outcomes, ecological effects, animal IDs, GPS positions,
fine-grid identifiers or original sensitive event dates are exported.

All original three-day source means and future day4/5 labels unchanged;
the only sensitivity restriction is every original GPS fix in ALL THREE
anchor days within the 30-km published centroid-source circle.
This may exclude valid short foraging excursions, so it is a deliberately
strict sensitivity population, NOT proof of actual site residence.
"""
from __future__ import annotations
import argparse,json,tempfile
from collections import Counter
from pathlib import Path

from scripts.qc_payoff_b_riskday_fix_integrity import (
    audit_fixes,EXPECTED as SOURCE_EXPECTED,
)
from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_unopened_gps_source import SOURCES
from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_payoff_b_predecision_candidates import daily_source_positions
from scripts.qc_payoff_b_complete_stationary_riskset import collect
from scripts.plan_payoff_b_batch_weather_requests import plan_batch_queries

SOURCE_LIST=("stork","white_fronted_goose","curlew","egyptian_vulture")
CASE="NORTHWARD_CANDIDATE"
STAY="STAYED_TWO_DAYS"
ORIGINAL_CLEAN_COUNT={
    "stork":(1110,85,716),
    "white_fronted_goose":(1790,93,1324),
    "curlew":(1778,42,1585),
    "egyptian_vulture":(1257,13,1029),
}
MIN_CASES_SAME_GRIDYEAR_MONTH=10
MIN_BOTH_OUTCOME_GRIDMONTH_STRATA=5
MAX_PUBLIC_NASA_REQUESTS=500


def filtered_source_gate(risk,stable):
    if len(risk)!=len(stable):
        raise ValueError("Source and fixed fix-level mask lengths differ")
    clean=[r for r,good in zip(risk,stable) if good]
    valid_cases_stays=[r for r in clean if r[3] in (CASE,STAY)]
    c=Counter(r[3] for r in clean)
    original=Counter(r[3] for r in risk)
    plan=plan_batch_queries(valid_cases_stays) if valid_cases_stays else None
    can=(plan is not None and
         plan["northward_case_days_in_overlap_gridmonths"]>=MIN_CASES_SAME_GRIDYEAR_MONTH
         and plan["grid_months_with_both_northward_and_stay_observations"]>=MIN_BOTH_OUTCOME_GRIDMONTH_STRATA
         and plan["estimated_monthly_hourly_NASA_requests"]<=MAX_PUBLIC_NASA_REQUESTS)
    return {
        "original_all_source_stationary_anchor_days":len(risk),
        "strict_all_3days_fix_within_30km_source_riskdays":len(clean),
        "strict_all_3days_source_label_counts":dict(sorted(c.items())),
        "original_daily_centroid_source_label_counts":dict(sorted(original.items())),
        "strict_risk_days_case_or_stay":len(valid_cases_stays),
        "strict_case_and_stay_weather_source_query_plan":plan,
        "source_overlap_preweather_admission":{
            "min_case_days_with_matching_stay_grid_year_month":MIN_CASES_SAME_GRIDYEAR_MONTH,
            "min_distinct_same_grid_year_month_strata":MIN_BOTH_OUTCOME_GRIDMONTH_STRATA,
            "max_distinct_public_NASA_requests":MAX_PUBLIC_NASA_REQUESTS,
            "passed":bool(can)
        },
        "original_weather_association_refitted":False,
        "direct_perceived_migratory_cue_or_fitness_tested":False,
        "all_fixes_inside_circle_proves_biological_stationary":False,
        "GPS_source_IDs_locations_and_grid_cells_exported":False,
    }


def run_one(system):
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"published_original_GPS.csv"
        if system=="egyptian_vulture":
            src=SOURCES[system]
            checksum=download_verified(src,path)
            doi,taxon=src["doi"],src["taxon"]
        else:
            doi,taxon,sensor,checksum=origin_source(system,path)
        groups,quality,identity=daily_source_positions(path,taxon)
        risk,counts,_,_=collect(groups)
        label_order=(CASE,STAY,"OTHER_MOVEMENT","CENSORED")
        observed=(len(risk),)+tuple(counts[label] for label in label_order)
        if observed!=SOURCE_EXPECTED[system]:
            raise ValueError("Original riskday population changed")
        aggregate,private_mask=audit_fixes(path,risk,taxon,return_private_mask=True)
        result=filtered_source_gate(risk,private_mask)
        c=result["strict_all_3days_source_label_counts"]
        baseline=(result["strict_all_3days_fix_within_30km_source_riskdays"],
                  c.get(CASE,0),c.get(STAY,0))
        if baseline!=ORIGINAL_CLEAN_COUNT[system]:
            raise ValueError("Strict fix-level source QA census does not reproduce")
        return {
            "status":"STRICT_FIX_SOURCE_OVERLAP_GATE_REPRODUCED",
            "system":system,"source_doi":doi,"source_taxon":taxon,
            "original_checksum":checksum,
            "original_all_fix_stationarity_diagnostic":aggregate,
            "strict_fix_level_source_overlap_admission":result,
            "no_local_weather_downloaded":True,
            "no_behavioral_or_Payoff_B_effect_estimated":True,
        }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--system",choices=SOURCE_LIST,required=True)
    ap.add_argument("--out",type=Path,
                    default=Path("outputs/payoff_b_strict_fix_source_overlap"))
    args=ap.parse_args()
    report={
        "schema":"payoff_b_strict_GPS_fixed_stationary_source_overlap_20261022",
        "classification":"POST_OUTCOME_QC_SOURCE_GEOMETRY_ONLY",
        "system":args.system,
    }
    try:report["result"]=run_one(args.system)
    except (OSError,ValueError,OverflowError,TypeError) as e:
        report["result"]={
            "status":"SOURCE_FIX_FILTER_OR_OVERLAP_QC_FAILED",
            "error":type(e).__name__+": "+str(e)[:280],
        }
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/(args.system+".json")).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    if report["result"]["status"]!="STRICT_FIX_SOURCE_OVERLAP_GATE_REPRODUCED":
        raise SystemExit("Strict original fix source overlap audit failed")

if __name__=="__main__":main()
