#!/usr/bin/env python3
"""Weather API batching feasibility for all 5,509 source at-risk GPS dates.

Original bird GPS is read privately; 0.5-degree grid identifiers, original
source locations, IDs and dates NEVER leave this process. Only grouped
counts, source-unit numbers and weather-request cost estimates are emitted.

A weather batch is a (year, month, 0.5-degree cell) with a requested
historical window from month-start minus eight days to month-end inclusive.
"""
from __future__ import annotations
import argparse,json,statistics,tempfile
from collections import Counter,defaultdict
from datetime import date,timedelta
from pathlib import Path
from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_predecision_candidates import SYSTEMS,daily_source_positions
from scripts.qc_payoff_b_complete_stationary_riskset import collect

EXPECTED={
    "stork":(1633,156,941,352,184),
    "white_fronted_goose":(2008,111,1456,285,156),
    "curlew":(1868,66,1632,90,80)
}
GRID_DEGREES=0.5
WEATHER_PRIOR_DAYS=8
MAX_MONTH_GRID_REQUESTS_WITHOUT_MANUAL_REVIEW=500


def month_end(year,month):
    next_month=date(year+1,1,1) if month==12 else date(year,month+1,1)
    return next_month-timedelta(days=1)


def plan_batch_queries(rows):
    by_month=defaultdict(Counter)
    year_cells=defaultdict(Counter)
    original_ids=set()
    allrisk=len(rows)
    for key,day,site,label in rows:
        original_ids.add(key)
        grid=(round(site[0]*2)/2,round(site[1]*2)/2)
        group=(day.year,day.month,grid)
        by_month[group][label]+=1
        year_cells[(day.year,grid)][label]+=1
    per_month_group_sizes=[sum(x.values()) for x in by_month.values()]
    case_stay_overlap=[
        x for x in by_month.values()
        if x.get("NORTHWARD_CANDIDATE",0)>0 and
           x.get("STAYED_TWO_DAYS",0)>0
    ]
    total_case=sum(x.get("NORTHWARD_CANDIDATE",0) for x in by_month.values())
    cases_inside_overlap=sum(x.get("NORTHWARD_CANDIDATE",0)
                             for x in case_stay_overlap)
    # These counts never export any source spatial grid identifier.
    return {
        "at_risk_source_days":allrisk,
        "individual_source_calendar_years":len(original_ids),
        "grid_resolution_degrees":GRID_DEGREES,
        "unique_grid_years":len(year_cells),
        "unique_grid_calendar_months":len(by_month),
        "estimated_monthly_hourly_NASA_requests":len(by_month),
        "prior_weather_context_days":WEATHER_PRIOR_DAYS,
        "raw_one_query_per_riskday_request_count":allrisk,
        "best_case_batched_vs_daily_query_reduction_fraction":
            1-len(by_month)/allrisk if allrisk else None,
        "riskdays_per_gridmonth_summary":{
            "min":min(per_month_group_sizes) if per_month_group_sizes else None,
            "median":statistics.median(per_month_group_sizes)
                     if per_month_group_sizes else None,
            "max":max(per_month_group_sizes) if per_month_group_sizes else None,
        },
        "grid_months_with_both_northward_and_stay_observations":len(case_stay_overlap),
        "northward_case_days_in_overlap_gridmonths":cases_inside_overlap,
        "fraction_case_days_in_within_gridmonth_overlap":
            cases_inside_overlap/total_case if total_case else None,
        "independence_of_weather_grid_months":False,
        "grid_month_weather_is_climatological_forecast":False,
        "GPS_source_coordinates_or_batch_cells_exported":False,
        "batch_cost_under_predeclared_500_query_gate":
            len(by_month)<=MAX_MONTH_GRID_REQUESTS_WITHOUT_MANUAL_REVIEW,
    }


def source_plan(system):
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"source.csv"
        doi,taxon,sensor,source=origin_source(system,path)
        tracks,quality,idcol=daily_source_positions(path,taxon)
        allrows,count,_,_=collect(tracks)
        keys=("all_at_risk_stationary_days","NORTHWARD_CANDIDATE",
              "STAYED_TWO_DAYS","OTHER_MOVEMENT","CENSORED")
        if tuple(count[k] for k in keys)!=EXPECTED[system]:
            raise ValueError("Frozen all-riskset source changed")
        return {
          "source_doi":doi,
          "source_name":taxon,
          "original_source_checksum":source,
          "source_label_counts":{k:count[k] for k in keys},
          "batch_cost_and_overlap":plan_batch_queries(allrows),
          "weather_effect_fitted":False,
          "animal_cue_and_fitness_not_measured":True,
        }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--system",choices=SYSTEMS,required=True)
    ap.add_argument("--out",type=Path,
        default=Path("outputs/payoff_b_batched_weather_plan"))
    args=ap.parse_args()
    result={
      "schema":"payoff_b_original_riskday_weather_grid_cost_plan_20261022",
      "system":args.system,
      "source_only":True,
      "status":"NOT_OPENED",
    }
    try:
        result["result"]=source_plan(args.system)
        result["status"]="SOURCE_BATCHING_PLAN_COMPLETE"
    except (ValueError,OSError,TypeError) as e:
        result["status"]="SOURCE_BATCH_COST_GATE_FAILED"
        result["error"]=type(e).__name__+": "+str(e)[:260]
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/(args.system+".json")).write_text(
        json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    if result["status"]!="SOURCE_BATCHING_PLAN_COMPLETE":
        raise SystemExit("Monthly weather batching plan could not be verified")


if __name__=="__main__":main()
