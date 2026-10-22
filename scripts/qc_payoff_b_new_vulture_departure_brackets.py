#!/usr/bin/env python3
"""Read-only original GPS timing-bracket admission on *new* Egyptian vulture.

Source independently catalogued before GPS/physical weather effects.
Select the first, original 7-day-separated northward candidate per
bird-calendar-year (18 pairs), not based on environmental effect sizes.
The original 3-day source-site center is from GPS only. A time bracket is
NOT an actual migratory decision or an observation of perceived cues.

No endangered-bird locations, animal IDs, case dates or individual
timestamp windows are ever written to output.
"""
from __future__ import annotations
import argparse,json,math,statistics,tempfile
from collections import Counter
from datetime import timedelta
from pathlib import Path

from scripts.qc_payoff_b_unopened_gps_source import SOURCES
from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_payoff_b_predecision_candidates import (
    daily_source_positions,detect_transfer_candidates
)
from scripts.qc_payoff_b_complete_stationary_riskset import site_three
from scripts.qc_payoff_b_stationary_case_controls import brackets,percentile

SOURCE=SOURCES["egyptian_vulture"]
EXACT_PRIOR_DEDUP_CANDIDATES=30
EXACT_ANIMAL_YEARS_WITH_CASE=18
MIN_DISTINCT_CASE_YEARS_WITH_24H_BRACKET=10
MAX_BRACKET_HOURS=24.0
BRACKET_TARGET_HOURS=(3.0,6.0,12.0,24.0)


def choose_first_per_animal_year(groups):
    chosen={}
    raw_count=0
    for key,days in sorted(groups.items()):
        daily=sorted(days)
        first_day_set=detect_transfer_candidates(daily)[1]
        raw_count+=len(first_day_set)
        if not first_day_set:continue
        day=min(first_day_set)
        index={x[0]:x for x in daily}
        prior=[index.get(day-timedelta(days=k)) for k in (2,1,0)]
        if any(x is None for x in prior):
            raise ValueError("Original candidate stationary site history absent")
        center=site_three(prior)
        chosen[key]=(day,center,None,None)
    return chosen,raw_count


def report_brackets(counts,widths,selected_n,total_candidates):
    if total_candidates!=EXACT_PRIOR_DEDUP_CANDIDATES:
        raise ValueError("Original 30 northward candidates changed")
    if selected_n!=EXACT_ANIMAL_YEARS_WITH_CASE:
        raise ValueError("Original 18 animal-years with northward candidate changed")
    # Helper 'brackets' accepts ONLY one source case per original animal-year.
    if sum(counts.values())!=selected_n:
        raise ValueError("Original case outcomes do not cover all selected animal-years")
    passed=len(widths)>=MIN_DISTINCT_CASE_YEARS_WITH_24H_BRACKET
    return {
        "original_stationary_then_northward_candidate_events":total_candidates,
        "first_event_per_original_bird_calendar_year":selected_n,
        "source_hour_bracket_outcome_counts":dict(sorted(counts.items())),
        "bracket_width_hours_quantiles_if_24h_or_narrower":{
            "min":min(widths) if widths else None,
            "q25":percentile(widths,.25) if widths else None,
            "median":percentile(widths,.5) if widths else None,
            "q75":percentile(widths,.75) if widths else None,
            "max":max(widths) if widths else None,
        },
        "brackets_narrower_than_h":{
            str(int(t)):sum(x<=t for x in widths) for t in BRACKET_TARGET_HOURS
        },
        "fixed_future_hourly_meteorology_source_gate":{
            "at_least_10_distinct_animal_year_brackets_under_24h":
                MIN_DISTINCT_CASE_YEARS_WITH_24H_BRACKET,
            "passed":passed,
        },
        "single_animal_year_counted_only_once":True,
        "true_behavioral_commitment_instant_identified":False,
        "no_raw_positions_source_identity_or_calendar_dates_exported":True,
    }


def run():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"original_published_GPS.csv"
        checksum=download_verified(SOURCE,p)
        groups,quality,idfield=daily_source_positions(p,SOURCE["taxon"])
        selected,n=choose_first_per_animal_year(groups)
        count,width=brackets(p,selected,SOURCE["taxon"])
        summary=report_brackets(count,width,len(selected),n)
        return {
            "status":"INDEPENDENT_TAXON_SOURCE_TIME_BRACKETS_COMPLETE",
            "source_doi":SOURCE["doi"],
            "original_checksum":checksum,
            "source_taxon":SOURCE["taxon"],
            "original_spring_geovalid_fix_counts":dict(sorted(quality.items())),
            "hour_bracket_source_admission":summary,
            "actual_stopover_exit_observed":False,
            "predecision_hourly_weather_joined":False,
            "future_remaining_migration_recourse_measured":False,
            "reproduction_survival_or_fitness_tested":False,
        }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,default=Path("outputs/payoff_b_new_vulture_time"))
    args=ap.parse_args()
    record={
        "schema":"payoff_b_new_vulture_original_GPS_hour_bracket_source_20261022",
        "analysis_type":"SOURCE_ONLY_TIMING_RESOLUTION_NOT_CUE_EFFECT",
    }
    try:record["result"]=run()
    except (OSError,ValueError,TypeError) as exc:
        record["result"]={"status":"SOURCE_OR_TIMING_QC_ERROR",
                          "error":type(exc).__name__+": "+str(exc)[:300]}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"egyptian_vulture.json").write_text(
        json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(record,ensure_ascii=False,indent=2))
    if record["result"]["status"]!="INDEPENDENT_TAXON_SOURCE_TIME_BRACKETS_COMPLETE":
        raise SystemExit("Original GPS time bracketing failed")

if __name__=="__main__":main()
