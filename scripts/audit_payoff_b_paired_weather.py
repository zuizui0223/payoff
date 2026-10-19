#!/usr/bin/env python3
"""Exploratory matched pre-departure weather anomalies versus staying put.

One individual-year pair per source, one case and one prior stationary control.
Source matching and time bracketing are frozen BEFORE fetching these
meteorological values. Actual bird cue use and fitness are NOT measured.
Historical NASA POWER is reconstructed physical weather, not a forecast.
Never export event dates, individuals, raw sites or single-pair weather.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import tempfile
import time
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import timedelta,datetime
from pathlib import Path

from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_predecision_candidates import (
    SYSTEMS,daily_source_positions,
)
from scripts.qc_payoff_b_stationary_case_controls import (
    matched_source_pairs,brackets,EXPECTED,
)
from scripts.run_payoff_b_stork_stage_handoff_pilot import percentile

NASA_API="https://power.larc.nasa.gov/api/temporal/hourly/point"
EXPECTED_BRACKET24={"stork":32,"white_fronted_goose":32,"curlew":25}
HASH="PAYOFF-B-MATCHED-PREDECISION-WEATHER-20261019-v1"
MAX_PAIRS_PER_SYSTEM=12
MIN_COMPLETE_PAIRS=10
OBSERVATION_DAY_OFFSET=-1
WEATHER_CONTEXT_DAYS=7
MIN_HOURS_PER_DAY=18
THREADS=4
BOOT_DRAWS=3000
SEED=20261019


def source_sample(selected,internal,system):
    valid=[]
    for key,record in selected.items():
        if internal[key]["status"]!="BRACKET_WITHIN_24H":
            continue
        case_day,site,control_day,control_site=record
        digest=hashlib.sha256((
            HASH+"|"+str(key)+"|"+case_day.isoformat()
        ).encode("utf-8")).hexdigest()
        valid.append((digest,key,record))
    if len(valid)!=EXPECTED_BRACKET24[system]:
        raise ValueError("Original pre-weather bracket admission count changed")
    valid.sort(key=lambda t:t[0])
    return [r for _,_,r in valid[:MAX_PAIRS_PER_SYSTEM]],len(valid)


def source_query(site,stage_day):
    lat,lon=site
    lat=round(lat*2)/2
    lon=round(lon*2)/2
    reference=stage_day+timedelta(days=OBSERVATION_DAY_OFFSET)
    start=reference-timedelta(days=WEATHER_CONTEXT_DAYS)
    args={
        "parameters":"T2M,WS10M","community":"SB",
        "latitude":f"{lat:.1f}","longitude":f"{lon:.1f}",
        "start":start.strftime("%Y%m%d"),
        "end":reference.strftime("%Y%m%d"),
        "format":"JSON","time-standard":"UTC",
    }
    return NASA_API+"?"+urllib.parse.urlencode(args),start,reference


def parse_nasa_span(payload,start,reference):
    if not isinstance(payload,dict):
        raise ValueError("NASA response not JSON object")
    props=(payload.get("properties") or {}).get("parameter") or {}
    if not isinstance(props,dict):
        raise ValueError("NASA hourly parameters missing")
    hdr=payload.get("header") or {}
    ts=str(hdr.get("time_standard") or "").upper()
    if ts and ts not in ("UTC","UNIVERSAL TIME COORDINATED"):
        raise ValueError("Unexpected non-UTC reanalysis")
    output={}
    for key in ("T2M","WS10M"):
        values=props.get(key)
        if not isinstance(values,dict):
            raise ValueError("Missing NASA weather variable")
        days={}
        for stamp,value in values.items():
            if len(str(stamp))!=10 or not str(stamp).isdigit():
                raise ValueError("Unexpected NASA time code")
            dt=datetime.strptime(str(stamp),"%Y%m%d%H")
            if not start<=dt.date()<=reference:
                raise ValueError("Weather response includes future or outside reference dates")
            num=float(value)
            if not math.isfinite(num) or num==-999.0:
                continue
            if key=="WS10M" and num<0:
                continue
            days.setdefault(dt.date(),[]).append(num)
        daily=[]
        for i in range(WEATHER_CONTEXT_DAYS+1):
            day=start+timedelta(days=i)
            obs=days.get(day,[])
            if len(obs)<MIN_HOURS_PER_DAY:
                raise ValueError("Incomplete predecision weather context")
            daily.append(statistics.mean(obs))
        output[key]={
            "last_predecision_day":daily[-1],
            "prior_week_mean":statistics.mean(daily[:-1]),
            "predecision_anomaly":daily[-1]-statistics.mean(daily[:-1])
        }
    return output


def fetch_weather(site,day):
    url,start,reference=source_query(site,day)
    err=None
    for i in range(3):
        try:
            req=urllib.request.Request(url,headers={
                "Accept":"application/json",
                "User-Agent":"PAYOFF-B-Paired-Weather-Exploratory/0.1",
            })
            with urllib.request.urlopen(req,timeout=80) as response:
                host=urllib.parse.urlparse(response.geturl())
                if host.scheme!="https" or host.hostname!="power.larc.nasa.gov":
                    raise ValueError("Unexpected meteorology domain")
                payload=json.load(response)
            return parse_nasa_span(payload,start,reference)
        except (OSError,ValueError,TimeoutError,TypeError) as exc:
            err=exc
            if i<2:time.sleep(1+i)
    raise RuntimeError(type(err).__name__+": "+str(err)[:100])


def bootstrap_mean(values,draws=BOOT_DRAWS,seed=SEED):
    if not values:
        return None
    rng=random.Random(seed)
    res=[
        statistics.mean(rng.choices(values,k=len(values)))
        for _ in range(draws)
    ]
    return [percentile(res,.025),percentile(res,.975)]


def summarize_paired(rows,system):
    def stats(key):
        a=[row[key] for row in rows]
        return {
            "n_pairs":len(a),
            "mean":statistics.mean(a) if a else None,
            "median":statistics.median(a) if a else None,
            "bootstrap_mean_95pct_CI_descriptive":
                bootstrap_mean(a,seed=SEED+sum(ord(c) for c in key))
                if a else None,
            "n_positive_differences":sum(x>0 for x in a),
            "n_negative_differences":sum(x<0 for x in a),
        }
    return {
        "source":system,
        "complete_matched_pairs":len(rows),
        "difference_case_minus_stay_temperature_c":
            stats("temp_raw_difference"),
        "difference_case_minus_stay_wind10m_m_s":
            stats("wind_raw_difference"),
        "paired_seven_day_anomaly_difference_temp_c":
            stats("temp_anomaly_difference"),
        "paired_seven_day_anomaly_difference_wind_m_s":
            stats("wind_anomaly_difference"),
        "case_minus_prior_control_days":
            stats("calendar_gap_days"),
        "source_effect_classification":
            "DESCRIPTIVE_POSTOUTCOME_EXPLORATORY_NOT_CAUSAL",
        "source_pairs_are_not_randomized":True,
        "weather_predictive_accuracy_unmeasured":True,
        "actual_bird_cue_use_unmeasured":True,
        "species_crosspooling_prohibited":True,
        "reanalysis_weather_is_not_historical_forecast":True,
        "animal_IDs_date_or_positions_exported":False,
    }


def run_system(system,fetch=fetch_weather):
    with tempfile.TemporaryDirectory() as d:
        gps=Path(d)/"source.csv"
        doi,taxon,sensor,original=origin_source(system,gps)
        groups,counters,idcol=daily_source_positions(gps,taxon)
        selected,gates=matched_source_pairs(groups)
        if gates["original_case_candidates"]!=EXPECTED[system]:
            raise ValueError("Frozen original case count changed")
        stats,widths,internal=brackets(gps,selected,taxon,return_internal=True)
        sample,bracket_n=source_sample(selected,internal,system)
        if len(sample)<MIN_COMPLETE_PAIRS:
            return {"status":"NOT_ESTIMABLE_PREWEATHER_ADMISSION",
                    "matched_24h_cases":bracket_n,"source_doi":doi}
        reqs=[]
        for case_day,site,control_day,control_site in sample:
            reqs.append((site,case_day))
            reqs.append((control_site,control_day))
        # Dedupe coarsened space/time without writing source coordinates.
        query_keys={}
        for loc,day in reqs:
            url,*_=source_query(loc,day)
            query_keys[url]=(loc,day)
        results={}
        with ThreadPoolExecutor(max_workers=THREADS) as pool:
            pending={pool.submit(fetch,loc,day):url
                     for url,(loc,day) in query_keys.items()}
            for future in as_completed(pending):
                url=pending[future]
                try:
                    results[url]=future.result()
                except Exception as e:
                    results[url]={"error":type(e).__name__}
        paired=[]
        misses=Counter()
        for case_day,site,control_day,control_site in sample:
            a_url,*_=source_query(site,case_day)
            b_url,*_=source_query(control_site,control_day)
            a,b=results[a_url],results[b_url]
            if "error" in a or "error" in b:
                misses[a.get("error") or b.get("error") or "UNKNOWN"]+=1
                continue
            paired.append({
                "calendar_gap_days":float((case_day-control_day).days),
                "temp_raw_difference":a["T2M"]["last_predecision_day"]-b["T2M"]["last_predecision_day"],
                "wind_raw_difference":a["WS10M"]["last_predecision_day"]-b["WS10M"]["last_predecision_day"],
                "temp_anomaly_difference":a["T2M"]["predecision_anomaly"]-b["T2M"]["predecision_anomaly"],
                "wind_anomaly_difference":a["WS10M"]["predecision_anomaly"]-b["WS10M"]["predecision_anomaly"],
            })
        valid=len(paired)
        return {
            "source_doi":doi,
            "source_name":taxon,
            "sensor":sensor,
            "original_source_checksum":original,
            "matched_source_candidate_count":gates["distinct_matched_identity_years"],
            "matched_brackets_24h":bracket_n,
            "selected_one_per_identity_year":len(sample),
            "unique_weather_spans":len(query_keys),
            "pair_weather_failures":len(sample)-valid,
            "failure_types":dict(sorted(misses.items())),
            "status":"MATCHED_WEATHER_EXPLORATORY_DESCRIPTIVES"
                    if valid>=MIN_COMPLETE_PAIRS else
                    "NOT_ESTIMABLE_WEATHER_COMPLETENESS",
            "summary":summarize_paired(paired,system)
                    if valid>=MIN_COMPLETE_PAIRS else None,
            "no_raw_event_or_site_export":True,
        }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--system",choices=SYSTEMS,required=True)
    p.add_argument("--out",type=Path,
        default=Path("outputs/payoff_b_matched_weather"))
    q=p.parse_args()
    receipt={
        "schema":"payoff_b_exploratory_matched_predeparture_weather_20261019",
        "source_system":q.system,
        "analysis_scope":"PRIOR_DAY_MINUS_PREVIOUS_7_DAYS_MATCHED_CASE_STAY",
        "predecision_weather_reference_offset_days":OBSERVATION_DAY_OFFSET,
        "previous_weather_baseline_days":WEATHER_CONTEXT_DAYS,
        "at_least_hourly_values_per_day":MIN_HOURS_PER_DAY,
        "pairs_sampled_by_source_only_hash":MAX_PAIRS_PER_SYSTEM,
        "min_complete_pairs_for_descriptive_result":MIN_COMPLETE_PAIRS,
        "source_only_not_causal":True,
    }
    try:
        receipt["result"]=run_system(q.system)
    except Exception as e:
        receipt["result"]={"status":"SOURCE_OR_WEATHER_GATE_FAILURE",
                           "error":type(e).__name__+": "+str(e)[:180]}
    q.out.mkdir(parents=True,exist_ok=True)
    (q.out/(q.system+".json")).write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2,ensure_ascii=False))
    if receipt["result"]["status"]!="MATCHED_WEATHER_EXPLORATORY_DESCRIPTIVES":
        raise SystemExit("Pair-weather source gate failed; no effect was promoted")


if __name__=="__main__":
    main()
