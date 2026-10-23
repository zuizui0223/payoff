#!/usr/bin/env python3
"""Full stationary GPS risk-day weather joining with NASA daily batch queries.

Original public CC0 sources, MD5 verified; 0.5-degree calendar-month batches.
An event's weather predictor is ONLY day-1 vs days-8..-2, even though the
batch response may contain later calendar dates. All 5,509 source riskdays
are retained; right-censored/other movements never become nondepartures.

No animal IDs, GPS, days, or cell identifiers are exported. Case/stay
weather contrasts are descriptive, not evidence of biological forecast
use, migration hazard, decision compensation or reproductive fitness.
"""
from __future__ import annotations
import argparse,json,math,statistics,tempfile,time,urllib.parse,urllib.request
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import date,datetime,timedelta
from pathlib import Path

from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_predecision_candidates import SYSTEMS,daily_source_positions
from scripts.qc_payoff_b_complete_stationary_riskset import collect
from scripts.plan_payoff_b_batch_weather_requests import (
    plan_batch_queries,month_end,MAX_MONTH_GRID_REQUESTS_WITHOUT_MANUAL_REVIEW,
)

VARS=("T2M","WS10M","V10M","ALLSKY_SFC_SW_DWN")
API="https://power.larc.nasa.gov/api/temporal/daily/point"
THROTTLE_SECONDS=0.1
WORKERS=3
EXPECTED={
    "stork":(1633,156,941,352,184,343),
    "white_fronted_goose":(2008,111,1456,285,156,334),
    "curlew":(1868,66,1632,90,80,132),
}
MIN_CLASS_COMPLETENESS=.90
MIN_OVERLAP_CASES=25
MIN_OVERLAP_STRATA=10


def grid_cell(site):
    return round(site[0]*2)/2,round(site[1]*2)/2


def batch_key(day,site):
    return day.year,day.month,grid_cell(site)


def batch_range(key):
    year,month,cell=key
    return date(year,month,1)-timedelta(days=8),month_end(year,month)


def api_url(key):
    year,month,(lat,lon)=key
    first,last=batch_range(key)
    query=urllib.parse.urlencode({
        "parameters":",".join(VARS),"community":"SB",
        "latitude":f"{lat:.1f}","longitude":f"{lon:.1f}",
        "start":first.strftime("%Y%m%d"),
        "end":last.strftime("%Y%m%d"),"format":"JSON",
        "time-standard":"UTC",
    })
    return API+"?"+query


def load_daily_payload(payload,key):
    if not isinstance(payload,dict):
        raise ValueError("NASA POWER daily payload not an object")
    vals=(payload.get("properties") or {}).get("parameter") or {}
    hdr=payload.get("header") or {}
    ts=str(hdr.get("time_standard") or "").upper()
    if ts and ts not in ("UTC","UNIVERSAL TIME COORDINATED"):
        raise ValueError("NASA POWER daily response not in UTC")
    if not isinstance(vals,dict):
        raise ValueError("Daily meteorological properties missing")
    first,last=batch_range(key)
    extracted={}
    for var in VARS:
        series=vals.get(var)
        if not isinstance(series,dict):
            raise ValueError("NASA source lacks requested daily "+var)
        out={}
        for stamp,value in series.items():
            s=str(stamp)
            if len(s)!=8 or not s.isdigit():
                raise ValueError("Invalid daily meteorology date key")
            day=datetime.strptime(s,"%Y%m%d").date()
            if not first<=day<=last:
                raise ValueError("NASA daily series returned outside batch month/context")
            try:v=float(value)
            except (ValueError,TypeError):continue
            if not math.isfinite(v) or v==-999.:continue
            if var in ("WS10M","ALLSKY_SFC_SW_DWN") and v<0:continue
            out[day]=v
        extracted[var]=out
    return extracted


def download_batch(key):
    url=api_url(key)
    last=None
    for attempt in range(3):
        try:
            time.sleep(THROTTLE_SECONDS)
            req=urllib.request.Request(url,headers={
                "Accept":"application/json",
                "User-Agent":"PAYOFF-B-complete-public-riskset-weather-20261022/1.0"
            })
            with urllib.request.urlopen(req,timeout=80) as response:
                final=urllib.parse.urlsplit(response.geturl())
                if final.scheme!="https" or final.hostname!="power.larc.nasa.gov":
                    raise ValueError("Unexpected daily weather source")
                source=json.load(response)
            return load_daily_payload(source,key)
        except (OSError,ValueError,TypeError,TimeoutError) as e:
            last=e
            if attempt<2:time.sleep(attempt+1)
    raise RuntimeError(type(last).__name__+": "+str(last)[:130])


def event_prior_weather(source,ref_day):
    """Only day-1 through day-8 are allowed as predictors."""
    prior=ref_day-timedelta(days=1)
    base=[prior-timedelta(days=k) for k in range(1,8)]
    result={}
    for var in VARS:
        values=source[var]
        if prior not in values or any(day not in values for day in base):
            return None
        recent=values[prior]
        avg=statistics.mean(values[day] for day in base)
        result[var+"_last"]=recent
        result[var+"_anomaly"]=recent-avg
    return result


def _mean(values):
    return statistics.mean(values) if values else None


def calculate_contrast(labelled):
    """labelled contains only sampled internal source identity and grid."""
    case="NORTHWARD_CANDIDATE"
    stay="STAYED_TWO_DAYS"
    variables=[x+"_anomaly" for x in VARS]
    variables+=[x+"_last" for x in VARS]
    by_label=defaultdict(list)
    by_gridmonth=defaultdict(lambda:defaultdict(list))
    for key,day,cell,label,met in labelled:
        if label not in (case,stay):
            continue
        by_label[label].append(met)
        by_gridmonth[(day.year,day.month,cell)][label].append(met)
    raw={}
    for var in variables:
        a=[r[var] for r in by_label[case]]
        b=[r[var] for r in by_label[stay]]
        raw[var]=_mean(a)-_mean(b) if a and b else None
    overlap=[v for v in by_gridmonth.values() if v[case] and v[stay]]
    n_overlap_cases=sum(len(v[case]) for v in overlap)
    within={}
    for var in variables:
        pairs=[(len(v[case]),statistics.mean(x[var] for x in v[case])-
                statistics.mean(x[var] for x in v[stay]))
               for v in overlap]
        within[var]=(
            sum(weight*effect for weight,effect in pairs)/sum(w for w,e in pairs)
            if pairs else None
        )
    return {
        "complete_case_source_days":len(by_label[case]),
        "complete_stay_source_days":len(by_label[stay]),
        "source_group_mean_case_minus_stay":raw,
        "grid_year_month_adjusted_case_weighted_descriptive_difference":within,
        "overlap_strata_grid_year_month":len(overlap),
        "case_days_inside_strata_with_both_labels":n_overlap_cases,
        "grid_year_month_clusters_are_statistically_independent":False,
        "site_year_month_adjusted_difference_is_causal":False,
    }


def run_system(system,fetch=download_batch):
    with tempfile.TemporaryDirectory() as td:
        raw=Path(td)/"original_source.csv"
        doi,taxon,sensor,integrity=origin_source(system,raw)
        groups,quality,idcol=daily_source_positions(raw,taxon)
        risk,counts,_,_=collect(groups)
        plan=plan_batch_queries(risk)
        k=("all_at_risk_stationary_days","NORTHWARD_CANDIDATE",
           "STAYED_TWO_DAYS","OTHER_MOVEMENT","CENSORED")
        n=tuple(counts[t] for t in k)+(plan["unique_grid_calendar_months"],)
        if n!=EXPECTED[system]:
            raise ValueError("Published source/0.5-degree batch registry drift")
        batches={batch_key(day,site) for group,day,site,label in risk}
        if len(batches)>MAX_MONTH_GRID_REQUESTS_WITHOUT_MANUAL_REVIEW:
            return {"status":"NOT_ADMITTED_TOO_MANY_API_BATCH_REQUESTS",
                    "batch_request_count":len(batches)}
        weather={}
        errors=Counter()
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures={pool.submit(fetch,k):k for k in sorted(batches)}
            for fut in as_completed(futures):
                b=futures[fut]
                try:weather[b]=fut.result()
                except Exception as e:errors[type(e).__name__]+=1
        missing=Counter()
        classified=[]
        for key,day,site,label in risk:
            batch=weather.get(batch_key(day,site))
            if batch is None:
                missing[label+"_BATCH_NOT_AVAILABLE"]+=1
                continue
            v=event_prior_weather(batch,day)
            if v is None:
                missing[label+"_WEATHER_CONTEXT_MISSING"]+=1
                continue
            classified.append((key,day,grid_cell(site),label,v))
        complete=Counter(x[3] for x in classified)
        good=all(
            complete[lab]>=counts[lab]*MIN_CLASS_COMPLETENESS
            for lab in ("NORTHWARD_CANDIDATE","STAYED_TWO_DAYS")
        )
        if not good:
            return {"status":"NOT_ESTIMABLE_WEATHER_MISSINGNESS",
                    "source_doi":doi,"source_counts":dict(sorted(counts.items())),
                    "weather_complete_source_counts":dict(sorted(complete.items())),
                    "source_failure_classes":dict(sorted(missing.items())),
                    "API_batches_requested":len(batches),
                    "API_batches_failed":sum(errors.values())}
        contrast=calculate_contrast(classified)
        admitted=(contrast["case_days_inside_strata_with_both_labels"]>=
                  MIN_OVERLAP_CASES and
                  contrast["overlap_strata_grid_year_month"]>=MIN_OVERLAP_STRATA)
        return {
            "status":"ALL_RISKDAY_SOURCE_WEATHER_ASSOCIATION_DESCRIPTIVE_COMPLETE"
                     if admitted else "NOT_ESTIMABLE_GRID_MONTH_OVERLAP",
            "source_doi":doi,"source_taxon":taxon,
            "original_source_checksum":integrity,
            "API_batches_requested":len(batches),
            "API_batches_failed":sum(errors.values()),
            "API_failure_types":dict(sorted(errors.items())),
            "source_total_riskdays":len(risk),
            "weather_complete_source_days":len(classified),
            "weather_complete_source_counts":dict(sorted(complete.items())),
            "weather_missing_by_source_label":dict(sorted(missing.items())),
            "riskset_original_counts":dict(sorted(counts.items())),
            "batch_cost_and_overlap_source_only":plan,
            "descriptive_weather_contrast":contrast,
            "modelled_true_departure_hazard":False,
            "predictor_uses_future_day_location_or_meteorology":False,
            "animal_perceived_cue_or_recourse_measured":False,
            "fitness_effect_tested":False,
            "GPS_coordinates_ID_dates_exported":False,
        }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--system",choices=SYSTEMS,required=True)
    ap.add_argument("--out",type=Path,
        default=Path("outputs/payoff_b_full_riskday_daily_weather"))
    arg=ap.parse_args()
    result={
      "schema":"payoff_b_all_stationary_riskday_daily_weather_v1",
      "system":arg.system,
      "source_class":"POST_V7V8_EXPLORATORY_GRID_MONTH_DESCRIPTIVES_ONLY",
      "NASA_source":"POWER daily UTC T2M,WS10M,V10M,ALLSKY_SFC_SW_DWN",
      "predictor_window":"day-1 minus days-2 to -8",
    }
    try:result["result"]=run_system(arg.system)
    except Exception as e:
        result["result"]={"status":"SOURCE_OR_WEATHER_GATE_FAILED",
                          "error":type(e).__name__+": "+str(e)[:260]}
    arg.out.mkdir(parents=True,exist_ok=True)
    (arg.out/(arg.system+".json")).write_text(
        json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if result["result"]["status"]!="ALL_RISKDAY_SOURCE_WEATHER_ASSOCIATION_DESCRIPTIVE_COMPLETE":
        raise SystemExit("Full risk-day weather source/overlap gate not admitted")


if __name__=="__main__":main()
