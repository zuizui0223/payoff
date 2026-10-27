#!/usr/bin/env python3
"""Source-only spring northward-progression coverage in stork GPS tracks.

No reproductive effect is calculated. Relative latitude progress is NOT
arrival at breeding grounds, stopover detection or a cue-actionability measure.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import statistics
import tempfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from scripts.qc_public_movebank_stork_gps_join_2018 import (
    download_gps, identifier_mappings, choose_gps_identifier, parse_time,
    load_reference_and_breeding,
)
from scripts.qc_public_movebank_stork_breeding_2018 import FILES, download_cc0, DOI

WINTER_MIN_UNIQUE_DAYS = 5
SPRING_MIN_UNIQUE_DAYS = 10
MIN_NORTHWARD_SPAN_DEG = 10.0
LOW_FRACTION = 0.2
HIGH_FRACTION = 0.8


def quantile(values, fraction):
    ordered = sorted(values)
    if not ordered:
        raise ValueError("empty quantile input")
    x = (len(ordered) - 1) * fraction
    i = int(x)
    f = x - i
    return ordered[i] * (1.0 - f) + ordered[min(i + 1, len(ordered)-1)] * f


def first_crossing(spring, boundary):
    for day, value in spring:
        if value >= boundary:
            return day
    return None


def classify_progression(days):
    """Daily position sequences are preaggregated; no individual identifiers."""
    winter = [
        value for day, value in days
        if day.month in (1,2)
    ]
    spring = sorted([
        (day, value) for day, value in days
        if day.month in (3,4)
    ])
    if len(winter) < WINTER_MIN_UNIQUE_DAYS:
        return {"status": "WINTER_DAYS_INSUFFICIENT"}
    if len(spring) < SPRING_MIN_UNIQUE_DAYS:
        return {"status": "SPRING_DAYS_INSUFFICIENT"}
    baseline = statistics.median(winter)
    late_northern_lat = quantile([value for _,value in spring], 0.9)
    northing = late_northern_lat - baseline
    if northing < MIN_NORTHWARD_SPAN_DEG:
        return {"status": "NORTHWARD_LATITUDE_RANGE_INSUFFICIENT", "northing_deg": northing}
    low, high = (
        baseline + fraction * northing
        for fraction in (LOW_FRACTION,HIGH_FRACTION)
    )
    if spring[0][1] >= low:
        return {"status": "SPRING_LEFT_CENSORED", "northing_deg": northing}
    begin = first_crossing(spring,low)
    end = first_crossing(spring,high)
    if not begin or not end or not begin < end:
        return {"status": "CROSSING_NOT_IDENTIFIABLE", "northing_deg": northing}
    return {
        "status": "NORTHWARD_PROGRESS_OBSERVED",
        "northing_deg": northing,
        "first_20_percent_doy": begin.timetuple().tm_yday,
        "first_80_percent_doy": end.timetuple().tm_yday,
        "twenty_to_eighty_day_span": (end - begin).days,
        "start_month": begin.month, "end_month": end.month,
        "has_breeding_arrival_proof": False,
    }


def extract_track_progress(gpspath, refs, pairs):
    maps, _ = identifier_mappings(refs)
    chosen = choose_gps_identifier(gpspath,maps)
    method = chosen["identity_method"]
    assoc = maps[method]
    day_sum = defaultdict(float)
    day_n = Counter()
    counter = Counter()
    with Path(gpspath).open(encoding="utf-8-sig",errors="replace",newline="") as f:
        reader=csv.DictReader(f)
        for row in reader:
            dep=assoc.get((row.get(method) or "").strip())
            if dep is None:
                counter["identity_not_joined"]+=1
                continue
            try:
                dt=parse_time(row.get("timestamp"))
                lat=float(row.get("location-lat") or "")
                lon=float(row.get("location-long") or "")
                if not math.isfinite(lat) or not math.isfinite(lon):
                    raise ValueError("nonfinite")
                if not -90<=lat<=90 or not -180<=lon<=180:
                    raise ValueError("out of bounds")
            except (ValueError,TypeError):
                counter["bad_time_or_coordinates"]+=1
                continue
            pair=(dep,dt.year)
            if pair not in pairs or dt.month not in (1,2,3,4):
                continue
            key=(pair,dt.date())
            day_sum[key]+=lat
            day_n[key]+=1
            counter["matched_gps_events_JanApr"]+=1
    grouped=defaultdict(list)
    for key,total in day_sum.items():
        pair,day=key
        grouped[pair].append((day,total/day_n[key]))
    all_results={}
    for pair in sorted(pairs):
        status=classify_progression(grouped.get(pair,[]))
        all_results[pair]=status
    return all_results,counter,chosen


def _percentiles(values):
    if not values:
        return None
    return {str(int(p*100)):quantile(values,p) for p in (0,0.25,0.5,0.75,1)}


def summarise_progress(classified,counters,choice,numeric_pairs):
    statuses=Counter(r["status"] for r in classified.values())
    success={
        k:v for k,v in classified.items()
        if v["status"]=="NORTHWARD_PROGRESS_OBSERVED"
    }
    winter_limited={
        k for k,v in classified.items() if v["status"]=="WINTER_DAYS_INSUFFICIENT"
    }
    results={
        "source_doi":DOI,
        "classification":"GPS_DERIVED_NORTHWARD_PROGRESS_ONLY",
        "breeding_animal_years_checked":len(classified),
        "status_counts":dict(sorted(statuses.items())),
        "success_unique_animal_years":len(success),
        "success_with_numeric_fledgling_outcome_available":len(set(success)&numeric_pairs),
        "winter_coverage_exclusion_count":len(winter_limited),
        "success_animal_identifiers_distinct":len({a for a,y in success}),
        "success_animals_with_more_than_one_year":sum(
            c>=2 for c in Counter(a for a,y in success).values()
        ),
        "first_20_percent_doy_quantiles":_percentiles([
            x["first_20_percent_doy"] for x in success.values()
        ]),
        "first_80_percent_doy_quantiles":_percentiles([
            x["first_80_percent_doy"] for x in success.values()
        ]),
        "twenty_to_eighty_span_days_quantiles":_percentiles([
            x["twenty_to_eighty_day_span"] for x in success.values()
        ]),
        "northward_span_degrees_quantiles":_percentiles([
            x["northing_deg"] for x in success.values()
        ]),
        "gps_identity_join_method":choice["identity_method"],
        "raw_events_JanApr":counters.get("matched_gps_events_JanApr",0),
        "source_bad_datetime_or_geo":counters.get("bad_time_or_coordinates",0),
        "source_unjoined_identity":counters.get("identity_not_joined",0),
        "parameter_lock":{
            "winter_months":"January-February",
            "spring_months":"March-April",
            "winter_min_unique_dates":WINTER_MIN_UNIQUE_DAYS,
            "spring_min_unique_dates":SPRING_MIN_UNIQUE_DAYS,
            "minimum_northward_latitude_span_degrees":MIN_NORTHWARD_SPAN_DEG,
            "relative_progress_thresholds":[LOW_FRACTION,HIGH_FRACTION],
            "daily_statistic":"unweighted mean of valid GPS latitude fixes",
            "northern_latitude_target":"90th percentile of spring daily mean latitude",
            "first_spring_day_past_20pct":"exclude as left-censored",
        },
        "study_breeding_destination_verified":False,
        "actual_departure_and_arrival_verified":False,
        "environmental_forecast_input_measured":False,
        "reproductive_regression_fitted":False,
        "individual_ids_or_daily_locations_exported":False,
    }
    return results


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",type=Path,
                    default=Path("outputs/payoff_b_stork_northward_progress_qc.json"))
    args=ap.parse_args()
    out={"status":"NOT_STARTED","source_doi":DOI}
    try:
        with tempfile.TemporaryDirectory() as working:
            root=Path(working)
            files={k:root/(k+(".txt" if k=="readme" else ".csv")) for k in FILES}
            for name,path in files.items():
                download_cc0(name,path)
            refs,pairs,numeric=load_reference_and_breeding(files["reference"],files["breeding"])
            gps=root/"gps.csv"
            out["gps_integrity"]=download_gps(gps)
            classified,counter,method=extract_track_progress(gps,refs,pairs)
            out["result"]=summarise_progress(classified,counter,method,numeric)
            out["status"]="SOURCE_ONLY_NORTHWARD_PROGRESS_QC_COMPLETE"
    except (OSError,ValueError,TypeError) as exc:
        out["status"]="SOURCE_OR_COVERAGE_PROCESS_FAILED"
        out["error"]=type(exc).__name__+": "+str(exc)[:400]
    out["raw_animal_data_stored_in_artifact"]=False
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False,indent=2))
    if out["status"]!="SOURCE_ONLY_NORTHWARD_PROGRESS_QC_COMPLETE":
        raise SystemExit("Source-only northward progression QC failed")

if __name__=="__main__":
    main()
