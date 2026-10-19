#!/usr/bin/env python3
"""Read-only independent meteorological pre-movement *availability* screen.

Uses original public CC0 GPS files; source stationary-to-northward candidate
counts are checked against the already opened published original QC.
A fixed outcome-blind hash selects 12 distinct animal-years per system.
Only original UTC-day T-1 retrospective NASA POWER hourly data are retrieved.

Meteorological conditions predate *observed movement* but are NOT proof
of actual bird perception, prediction, intentional cue use or fitness.
No raw tracks, weather-event combinations, times or source coordinates
are uploaded; original coordinates are coarse-gridded BEFORE NASA requests.
"""
from __future__ import annotations
import argparse,hashlib,json,math,statistics,tempfile,time
import urllib.parse,urllib.request,urllib.error
from collections import Counter,defaultdict
from datetime import timedelta
from pathlib import Path

from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_predecision_candidates import (
    SYSTEMS,daily_source_positions,detect_transfer_candidates,
    vector_mean_lon,
)

MAX_EVENTS=12
MIN_VALID_HOURLY_TEMPS=18
MIN_VALID_HOURLY_WINDS=18
HASH_VERSION="PAYOFF-B-PREDECISION-METADATA-20261019-v1"
EXPECTED_CANDIDATES={"stork":145,"white_fronted_goose":106,"curlew":59}
API="https://power.larc.nasa.gov/api/temporal/hourly/point"
RETRIES=2


def stage_site(daily,day):
    index={row[0]:row for row in daily}
    pos=[index.get(day-timedelta(days=k)) for k in (2,1,0)]
    if any(v is None for v in pos):
        raise ValueError("Original stationary days missing")
    lat=statistics.median(v[1] for v in pos)
    lon=vector_mean_lon(
        sum(math.cos(math.radians(v[2])) for v in pos),
        sum(math.sin(math.radians(v[2])) for v in pos)
    )
    return lat,lon,day-timedelta(days=1)


def collect_events(groups):
    selected_one_per_individual_year=[]
    all_candidates=0
    for (tax,ident,year),daily in groups.items():
        _,dates=detect_transfer_candidates(daily)
        all_candidates+=len(dates)
        if not dates:continue
        source=[]
        for day in dates:
            lat,lon,preceding=stage_site(daily,day)
            key=f"{HASH_VERSION}|{tax}|{ident}|{year}|{day.isoformat()}"
            digest=hashlib.sha256(key.encode()).hexdigest()
            source.append((digest,lat,lon,preceding))
        selected_one_per_individual_year.append(min(source,key=lambda p:p[0]))
    chosen=sorted(selected_one_per_individual_year,key=lambda p:p[0])[:MAX_EVENTS]
    return all_candidates,chosen,len(selected_one_per_individual_year)


def nasa_power_request(lat,lon,day):
    # Coarsen raw site coordinate to 0.5-degree grid before any external API
    # request. Neither raw nor coarsened positions appear in the artifact.
    qlat=round(lat*2)/2
    qlon=round(lon*2)/2
    dt=day.strftime("%Y%m%d")
    query=urllib.parse.urlencode({
        "parameters":"T2M,WS10M",
        "community":"SB",
        "latitude":f"{qlat:.1f}",
        "longitude":f"{qlon:.1f}",
        "start":dt,"end":dt,
        "format":"JSON","time-standard":"UTC",
    })
    return API+"?"+query


def parse_power_day(obj,day):
    if not isinstance(obj,dict):
        raise ValueError("NASA POWER response is not an object")
    params=(obj.get("properties") or {}).get("parameter") or {}
    if not isinstance(params,dict):
        raise ValueError("No NASA hourly parameters")
    header=obj.get("header") or {}
    if isinstance(header,dict):
        standard=str(header.get("time_standard") or "").upper()
        if standard and standard not in ("UTC","UNIVERSAL TIME COORDINATED"):
            raise ValueError("NASA response was not in requested UTC")
    expected=day.strftime("%Y%m%d")
    records={}
    for var in ("T2M","WS10M"):
        table=params.get(var)
        if not isinstance(table,dict):
            raise ValueError("Missing NASA source parameter "+var)
        arr=[]
        for key,val in table.items():
            if not str(key).startswith(expected):
                raise ValueError("NASA source returned a later or earlier calendar day")
            try:
                hour=int(str(key)[8:10])
                v=float(val)
            except (TypeError,ValueError):
                raise ValueError("Invalid NASA hourly value/time")
            if not (0<=hour<=23):
                raise ValueError("hour outside UTC day")
            if math.isfinite(v) and v!=-999.0:
                if var=="WS10M" and v<0:continue
                arr.append(v)
        records[var]=arr
    counts={key:len(a) for key,a in records.items()}
    valid=(counts["T2M"]>=MIN_VALID_HOURLY_TEMPS and
           counts["WS10M"]>=MIN_VALID_HOURLY_WINDS)
    return {
        "source_valid":valid,
        "valid_temperature_hours":counts["T2M"],
        "valid_wind_hours":counts["WS10M"],
        "temperature_mean_celsius":
            statistics.mean(records["T2M"]) if valid else None,
        "wind_speed_10m_mean_m_s":
            statistics.mean(records["WS10M"]) if valid else None,
    }


def fetch_power_day(lat,lon,day):
    url=nasa_power_request(lat,lon,day)
    last=None
    for attempt in range(RETRIES):
        try:
            req=urllib.request.Request(url,headers={
                "Accept":"application/json",
                "User-Agent":"PAYOFF-B-source-only-meteorological-availability/0.1",
            })
            with urllib.request.urlopen(req,timeout=65) as response:
                urlparts=urllib.parse.urlsplit(response.geturl())
                if urlparts.scheme!="https" or urlparts.hostname!="power.larc.nasa.gov":
                    raise ValueError("NASA source redirect unapproved")
                obj=json.load(response)
            return parse_power_day(obj,day)
        except (OSError,TimeoutError,ValueError,json.JSONDecodeError) as e:
            last=e
            if attempt+1<RETRIES:time.sleep(attempt+1)
    raise RuntimeError(type(last).__name__+": "+str(last)[:150])


def source_meteorology_availability(events,fetch=fetch_power_day):
    attempts=len(events)
    failures=Counter()
    temp=[]
    wind=[]
    hourly_temp=[]
    hourly_wind=[]
    # In-run dedupe by rounded public grid cell + date, never stored.
    cache={}
    for digest,lat,lon,day in events:
        key=(round(lat*2)/2,round(lon*2)/2,day)
        if key not in cache:
            try:cache[key]=fetch(lat,lon,day)
            except Exception as e:
                cache[key]={"source_valid":False,
                            "error_type":type(e).__name__}
            # Avoid unnecessary rapid repeated public API calls.
            time.sleep(0.2)
        r=cache[key]
        if not r.get("source_valid",False):
            failures[r.get("error_type","MISSING_HOURLY_DATA")]+=1
            continue
        temp.append(float(r["temperature_mean_celsius"]))
        wind.append(float(r["wind_speed_10m_mean_m_s"]))
        hourly_temp.append(r["valid_temperature_hours"])
        hourly_wind.append(r["valid_wind_hours"])
    return {
        "selected_distinct_identity_years":attempts,
        "source_valid_pre_move_weather_days":len(temp),
        "source_missing_or_invalid_weather_days":attempts-len(temp),
        "source_failures_by_type":dict(sorted(failures.items())),
        "valid_temperature_hours_min":min(hourly_temp) if hourly_temp else None,
        "valid_wind_hours_min":min(hourly_wind) if hourly_wind else None,
        "mean_temperature_across_valid_pilot_events_celsius":
            statistics.mean(temp) if temp else None,
        "mean_wind_speed_across_valid_pilot_events_m_s":
            statistics.mean(wind) if wind else None,
        "api_source":"NASA POWER hourly point original retrospective meteorology, UTC",
        "pre_move_weather_day":"last_stationary_candidate_day_minus_1",
        "original_location_coarsened_before_external_request_deg":0.5,
        "weather_times_stored_in_artifact":False,
        "individual_locations_uploaded_or_published":False,
        "cue_was_actually_perceived_by_bird":False,
        "causal_behavior_or_fitness_effect_tested":False,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--system",choices=SYSTEMS,required=True)
    ap.add_argument("--out",type=Path,
                    default=Path("outputs/payoff_b_predecision_weather_source"))
    args=ap.parse_args()
    receipt={"system":args.system,"status":"NOT_STARTED",
             "analysis":"RETROSPECTIVE_WEATHER_SOURCE_COVERAGE_NOT_INDIVIDUAL_CUE_USE"}
    try:
        with tempfile.TemporaryDirectory() as td:
            gps=Path(td)/"original.csv"
            doi,taxon,sensor,original=origin_source(args.system,gps)
            groups,counters,ident=daily_source_positions(gps,taxon)
            candidates,selected,eligible=collect_events(groups)
            if candidates!=EXPECTED_CANDIDATES[args.system]:
                raise ValueError("Candidate source coverage changed after prior result")
            stats=source_meteorology_availability(selected)
            receipt.update(source_doi=doi,source_taxon=taxon,sensor=sensor,
                           source_integrity=original,
                           fixed_candidate_count=candidates,
                           eligible_distinct_identity_years=eligible,
                           source_meteorology=stats,
                           status="WEATHER_SOURCE_AVAILABILITY_AUDITED")
    except (OSError,ValueError,TypeError) as e:
        receipt["status"]="WEATHER_SOURCE_AUDIT_FAILED"
        receipt["error"]=type(e).__name__+": "+str(e)[:350]
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/(args.system+".json")).write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))
    if receipt["status"]!="WEATHER_SOURCE_AVAILABILITY_AUDITED":
        raise SystemExit("source chronology or original track gate failed")

if __name__=="__main__":main()
