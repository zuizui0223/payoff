#!/usr/bin/env python3
"""Source-only continuous GPS 30-km exit-bracket audit for Egyptian vultures.

Re-examines the same 18 first-per-animal-year original source movement
proxies, with identical original GPS/MD5 and fixed 30km stationary-site
center. The earlier 15/18 brackets were obtained by taking the last
source-day fix and the first following-day outside fix. That estimator may
measure an arbitrary day boundary, not the shortest observed GPS crossing.

Before reading source events, compare TWO predeclared estimators:
  1. First within->outside 30km consecutive-fix crossing from start of
     anchor day through the end of the following day (raw geometric bracket).
  2. First such crossing with ≥2 outward fixes and a fix 8–12h after the
     first outside fix, and no recorded returns inside during the first
     12h (sampled sustained-outside evidence; not proof of no return).
Missing followups/left-censoring and GPS sampling gaps are explicit.

This is an exploratory measurement audit after prior vulture weather
results, not a cue-use effect, hour-specific weather test, verified actual
departure, stagewise recourse or evolutionary fitness test.
NO endangered-bird positions, animal IDs, real dates or individual bracket
widths are exported.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import statistics
import tempfile
from collections import Counter,defaultdict
from datetime import datetime, timedelta, time, timezone
from pathlib import Path

from scripts.qc_payoff_b_unopened_gps_source import SOURCES
from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_payoff_b_predecision_candidates import (
    daily_source_positions,haversine,
)
from scripts.qc_payoff_b_new_vulture_departure_brackets import (
    choose_first_per_animal_year,
    EXACT_PRIOR_DEDUP_CANDIDATES,
    EXACT_ANIMAL_YEARS_WITH_CASE,
)
from scripts.qc_payoff_b_stationary_case_controls import brackets

SOURCE=SOURCES["egyptian_vulture"]
DISTANCE_KM=30.0
BRACKET_THRESHOLDS_HOURS=(1.0,3.0,6.0,12.0,24.0)
MAX_BRACKET_HOURS=24.0
SUSTAINED_HOURS=12.0
SUSTAINED_LATE_OBSERVATION_HOURS=(8.0,12.0)
MIN_OUTSIDE_FIXES=2
MAX_PLAUSIBLE_CROSSING_SPEED_KMH=160.0

def normalize_utc(raw):
    stamp=datetime.fromisoformat((raw or "").strip().replace("Z","+00:00"))
    if stamp.tzinfo:
        return stamp.astimezone(timezone.utc).replace(tzinfo=None)
    return stamp

def assessment(fixes,center,anchor_day):
    """Original fixes are (UTC datetime, latitude, longitude), never exported."""
    sorted_fixes=sorted(fixes,key=lambda v:v[0])
    first_allowed=datetime.combine(anchor_day,time.min)
    last_allowed=first_allowed+timedelta(days=2)
    evaluated=[]
    for dt,lat,lon in sorted_fixes:
        if not (first_allowed-timedelta(days=1)<=dt<
                last_allowed+timedelta(days=1)):
            continue
        evaluated.append((dt,haversine(center[0],center[1],lat,lon)))
    raw=[]
    for previous,current in zip(evaluated,evaluated[1:]):
        t0,r0=previous
        t1,r1=current
        if not (first_allowed<=t1<last_allowed):
            continue
        if not (r0<=DISTANCE_KM<r1):
            continue
        width=(t1-t0).total_seconds()/3600
        if width<=0:
            continue
        forward=[p for p in evaluated if t1<=p[0]<=t1+timedelta(hours=SUSTAINED_HOURS)]
        returns=any(r<=DISTANCE_KM for t,r in forward if t>t1)
        outward=sum(r>DISTANCE_KM for t,r in forward)
        late=any(
            (SUSTAINED_LATE_OBSERVATION_HOURS[0] <=
             (t-t1).total_seconds()/3600 <=
             SUSTAINED_LATE_OBSERVATION_HOURS[1])
            and r>DISTANCE_KM for t,r in forward
        )
        sustained=(not returns and outward>=MIN_OUTSIDE_FIXES and late)
        ground_speed=(r1-r0)/width  # radial rate is LOWER bound on ground speed
        raw.append({
            "width_hours":width,
            "outside_time":t1,
            "status":"SAMPLED_12H_OUTSIDE" if sustained else
                     "OBSERVED_RETURN_WITHIN_12H" if returns else
                     "INSUFFICIENT_FOLLOWUP_TO_SHOW_SUSTAINED",
            "early_on_anchor_day":t1.date()==anchor_day,
            "radial_speed_lower_bound_above_160kmh":
                ground_speed>MAX_PLAUSIBLE_CROSSING_SPEED_KMH,
        })
    if not raw:
        return {
            "status":"NO_INSIDE_OUTSIDE_CROSSING_IN_LOCKED_48H_WINDOW",
            "n_original_fixes_in_window":len(evaluated),
            "first_observed_fix_already_outside":bool(evaluated and evaluated[0][1]>DISTANCE_KM),
            "raw":None,"sustained":None,
            "n_raw_crossings":0,
        }
    first=raw[0]
    first_sustained=next((x for x in raw if x["status"]=="SAMPLED_12H_OUTSIDE"),None)
    return {
        "status":"AT_LEAST_ONE_SOURCE_GPS_THRESHOLD_CROSSING",
        "n_original_fixes_in_window":len(evaluated),
        "first_observed_fix_already_outside":bool(evaluated and evaluated[0][1]>DISTANCE_KM),
        "n_raw_crossings":len(raw),
        "raw":first,
        "sustained":first_sustained,
        "n_candidates_with_sampled_return":sum(x["status"]=="OBSERVED_RETURN_WITHIN_12H" for x in raw),
        "n_sustained_evidence_candidates":sum(x["status"]=="SAMPLED_12H_OUTSIDE" for x in raw),
    }

def collect_source_events(path,selected):
    """Stream source once, keep only four source days per selected animal-year."""
    byid=defaultdict(list)
    meta=Counter()
    idyears={(key[1],key[2]):key for key in selected}
    with Path(path).open(encoding="utf-8-sig",errors="replace",newline="") as file:
        reader=csv.DictReader(file)
        fields=reader.fieldnames or []
        needed={"timestamp","individual-local-identifier","location-lat","location-long"}
        if not needed.issubset(fields):
            raise ValueError("Original source position/time/identity fields absent")
        for row in reader:
            ident=(row.get("individual-local-identifier") or "").strip()
            if not ident:
                continue
            try:
                dt=normalize_utc(row.get("timestamp") or "")
                lat=float(row.get("location-lat") or "")
                lon=float(row.get("location-long") or "")
                if not (math.isfinite(lat) and math.isfinite(lon) and
                        -90<=lat<=90 and -180<=lon<=180):
                    raise ValueError("GPS coordinates invalid")
            except (ValueError,OverflowError,TypeError):
                meta["invalid_original_fix"]+=1
                continue
            key=idyears.get((ident,dt.year))
            if key is None:
                continue
            anchor=selected[key][0]
            if anchor-timedelta(days=1)<=dt.date()<=anchor+timedelta(days=2):
                byid[key].append((dt,lat,lon))
                meta["source_fixes_in_declared_evaluation_windows"]+=1
    return byid,meta

def quartiles(values):
    if not values:return None
    arr=sorted(values)
    def interpol(q):
        i=(len(arr)-1)*q
        base=int(i)
        return arr[base]*(1-i+base)+arr[min(base+1,len(arr)-1)]*(i-base)
    return {"min":arr[0],"q25":interpol(.25),
            "median":statistics.median(arr),"q75":interpol(.75),"max":arr[-1]}

def diagnostic(selected,source_fixes,old_brackets):
    allstatus=Counter()
    raw_widths=[]
    sustained_widths=[]
    n_crossings=0
    raw_early=0
    returns=0
    fast_radial=0
    older=Counter()
    lower_old_width=[]
    for key,(day,center,_,_) in sorted(selected.items()):
        result=assessment(source_fixes.get(key,[]),center,day)
        allstatus[result["status"]]+=1
        old=old_brackets[key]
        older[old["status"]]+=1
        if old["status"]=="BRACKET_WITHIN_24H":lower_old_width.append(old["hours"])
        n_crossings+=result["n_raw_crossings"]
        if result["raw"] is not None:
            candidate=result["raw"]
            raw_widths.append(candidate["width_hours"])
            raw_early+=candidate["early_on_anchor_day"]
            fast_radial+=candidate["radial_speed_lower_bound_above_160kmh"]
            returns+=candidate["status"]=="OBSERVED_RETURN_WITHIN_12H"
        if result["sustained"] is not None:
            sustained_widths.append(result["sustained"]["width_hours"])
    return {
      "original_candidate_animal_years":len(selected),
      "all_predeclared_raw_C30_threshold_status_counts":dict(sorted(allstatus.items())),
      "old_UTC_day_boundary_original_source_bracket_status_counts":dict(sorted(older.items())),
      "old_bracket_under24h_width_summary":quartiles(lower_old_width),
      "new_fix_to_fix_first_source_crossing_width_summary":quartiles(raw_widths),
      "first_sustained_12h_sampled_outside_width_summary":quartiles(sustained_widths),
      "raw_first_crossings_on_original_anchor_day":raw_early,
      "all_raw_threshold_crossings_in_windows":n_crossings,
      "first_crossing_has_sampled_return_within12h":returns,
      "first_crossing_radial_speed_lower_bound_over160kmh":fast_radial,
      "original_distinct_animal_years_with_sustained_12h_outside_evidence":len(sustained_widths),
      "new_raw_fix_to_fix_brackets_under_hours":{
          str(int(k)):sum(v<=k for v in raw_widths)
          for k in BRACKET_THRESHOLDS_HOURS
      },
      "new_sustained_outside_brackets_under_hours":{
          str(int(k)):sum(v<=k for v in sustained_widths)
          for k in BRACKET_THRESHOLDS_HOURS
      },
      "GPS_position_crossing_equals_true_behavioral_departure":False,
      "12h_no_observed_return_equals_biological_site_departure_proven":False,
      "cue_reception_and_future_route_info_measured":False,
      "fixed_source_case_gate_modified":False,
      "original_animal_identifiers_event_times_positions_exported":False,
    }

def run():
    with tempfile.TemporaryDirectory() as d:
        file=Path(d)/"public_original_CC0_GPS.csv"
        digest=download_verified(SOURCE,file)
        groups,quality,identity=daily_source_positions(file,SOURCE["taxon"])
        selected,n=choose_first_per_animal_year(groups)
        if n!=EXACT_PRIOR_DEDUP_CANDIDATES or len(selected)!=EXACT_ANIMAL_YEARS_WITH_CASE:
            raise ValueError("Original first-event cohort count not identical")
        old_status,old_widths,old=brackets(file,selected,SOURCE["taxon"],return_internal=True)
        if (old_status.get("BRACKET_WITHIN_24H",0)!=15 or
            old_status.get("LAST_SOURCE_FIX_OUTSIDE",0)!=3):
            raise ValueError("Original 15/18 timing bracket receipt not reproduced")
        fix,errors=collect_source_events(file,selected)
        checked=diagnostic(selected,fix,old)
        return {
            "status":"CONTINUOUS_FIX_LEVEL_SOURCE_RESOLUTION_AUDITED",
            "original_source_doi":SOURCE["doi"],
            "source_taxon":SOURCE["taxon"],
            "original_MD5_and_bytes":digest,
            "source_original_animal_years":len(selected),
            "source_scanned_valid_fixes_in_locked_windows":
                errors["source_fixes_in_declared_evaluation_windows"],
            "source_parse_errors_in_timing_scan":errors["invalid_original_fix"],
            "source_event_sampling_diagnostic":checked,
            "GPS_fix_location_is_exact_behavioral_commitment":False,
            "source_hourly_weather_reanalysis_tested":False,
            "fitness_or_recourse_tested":False,
            "raw_sensitive_tracking_data_exported":False,
        }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,
        default=Path("outputs/payoff_b_vulture_continuous_brackets"))
    a=ap.parse_args()
    out={
      "schema":"payoff_b_new_vulture_fix_level_source_bracket_audit_20261022",
      "method_status":"POST_SOURCE_GEOMETRY_MEASUREMENT_DIAGNOSTIC_NOT_HYPOTHESIS_TEST",
    }
    try:out["result"]=run()
    except (ValueError,OSError,OverflowError,TypeError) as err:
        out["result"]={
            "status":"SOURCE_FIXED_CASE_OR_TIMING_QC_FAILED",
            "error":type(err).__name__+": "+str(err)[:300],
        }
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"egyptian_vulture.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(out,ensure_ascii=False,indent=2))
    if out["result"]["status"]!="CONTINUOUS_FIX_LEVEL_SOURCE_RESOLUTION_AUDITED":
        raise SystemExit("Fix-level source temporal resolution audit failed")

if __name__=="__main__":main()
