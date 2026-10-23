#!/usr/bin/env python3
"""Independent-source Egyptian-vulture *geometry* before external weather.

Use the same original February-May 3-day stationary GPS risk opportunity
definitions and 0.5-degree monthly NASA request planner as earlier PAYOFF.
No public meteorology or animal behavior effect is opened in this gate.
For a threatened taxon, never export routes, IDs, days or source grid cells.
"""
from __future__ import annotations
import argparse,json,tempfile
from collections import Counter
from pathlib import Path

from scripts.qc_payoff_b_unopened_gps_source import SOURCES
from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_payoff_b_predecision_candidates import (
    daily_source_positions, source_audit,
)
from scripts.qc_payoff_b_complete_stationary_riskset import collect
from scripts.plan_payoff_b_batch_weather_requests import plan_batch_queries

SOURCE="egyptian_vulture"
EXPECTED_ORIGINAL_CANDIDATES=30
EXPECTED_SPRING_SOURCE_ANIMAL_YEARS_WITH_CANDIDATES=18
MIN_WEATHER_CASES_IN_MATCHING_GRIDMONTH=10
MIN_WEATHER_GRIDMONTH_OVERLAP_STRATA=5
MAX_NASA_MONTHLY_BATCHES=500


def read_original():
    data=SOURCES[SOURCE]
    with tempfile.TemporaryDirectory() as directory:
        p=Path(directory)/"published_original_CC0.csv"
        checksum=download_verified(data,p)
        groups,quality,idcol=daily_source_positions(p,data["taxon"])
        audit=source_audit(groups,quality,idcol)
        if audit["total_candidate_events"]!=EXPECTED_ORIGINAL_CANDIDATES:
            raise ValueError("Original published source candidate count changed")
        years=audit["classified_source_taxa"][data["taxon"]]["animal_years_with_one_or_more_candidates"]
        if years!=EXPECTED_SPRING_SOURCE_ANIMAL_YEARS_WITH_CANDIDATES:
            raise ValueError("Original source departure cohort changed")
        rows,source_counts,by_month,by_year=collect(groups)
        if source_counts["deduplicated_frozen_cases"]!=EXPECTED_ORIGINAL_CANDIDATES:
            raise ValueError("Full riskset failed to reproduce exactly 30 frozen vulture cases")
        plan=plan_batch_queries(rows)
        n=plan["northward_case_days_in_overlap_gridmonths"]
        overlaps=plan["grid_months_with_both_northward_and_stay_observations"]
        admissible=(n>=MIN_WEATHER_CASES_IN_MATCHING_GRIDMONTH
                    and overlaps>=MIN_WEATHER_GRIDMONTH_OVERLAP_STRATA
                    and plan["estimated_monthly_hourly_NASA_requests"]<=MAX_NASA_MONTHLY_BATCHES)
        return {
            "source_original_doi":data["doi"],
            "source_taxon":data["taxon"],
            "source_original_file_checksum":checksum,
            "original_fixed_source_candidates":audit["total_candidate_events"],
            "fixed_source_candidate_animal_years":years,
            "all_3day_stationary_riskday_counts":dict(sorted(source_counts.items())),
            "source_counts_by_month_no_location":{
                f"{tax}|{m:02d}":dict(sorted(x.items()))
                for (tax,m),x in sorted(by_month.items())},
            "source_counts_by_year_no_location":{
                f"{tax}|{year}":dict(sorted(x.items()))
                for (tax,year),x in sorted(by_year.items())},
            "weather_gridmonth_query_cost_no_geolocation":plan,
            "followup_weather_source_gate":{
                "min_northward_cases_with_same_gridmonth_stays":
                    MIN_WEATHER_CASES_IN_MATCHING_GRIDMONTH,
                "min_grid_year_months_with_case_stay_overlap":
                    MIN_WEATHER_GRIDMONTH_OVERLAP_STRATA,
                "max_public_weather_API_requests":
                    MAX_NASA_MONTHLY_BATCHES,
                "passed":admissible
            },
            "source_admission":"READY_FOR_FIXED_EXPLORATORY_WEATHER_JOIN"
                        if admissible else "NOT_ESTIMABLE_FIXED_SOURCE_OVERLAP_OR_API_GATE",
            "known_actual_departure_decisions":False,
            "weather_or_fitness_analyzed":False,
            "source_animal_IDs_locations_or_dates_exported":False
        }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=Path("outputs/payoff_b_new_vulture_riskday"))
    args=p.parse_args()
    result={"schema":"payoff_b_new_vulture_independent_GPS_riskset_source_gate_v1",
            "analysis_class":"ORIGINAL_SOURCE_GEOMETRY_AND_API_COST_ONLY"}
    try:
        result["result"]=read_original()
        result["status"]="ORIGINAL_PUBLIC_GPS_RISKSET_QC_COMPLETE"
    except (ValueError,OSError,TypeError) as e:
        result["status"]="SOURCE_GATE_FAILED"
        result["error"]=type(e).__name__+": "+str(e)[:240]
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"egyptian_vulture.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if result["status"]!="ORIGINAL_PUBLIC_GPS_RISKSET_QC_COMPLETE":
        raise SystemExit("Original threatened-vulture source integrity gate failed")


if __name__=="__main__":main()
