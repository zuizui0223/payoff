#!/usr/bin/env python3
"""Predecision northward wind and shortwave irradiance source-only contrast.

V10M = MERRA-2/NASA POWER northward wind at 10m (positive northward).
ALLSKY_SFC_SW_DWN = downwelling solar irradiance (W m^-2).
Same fixed 16 moving/32 nonmoving selected riskdays per bird taxon as
temperature/wind speed pilot, with no post-source sign-based exclusions.

A northward surface wind is not proof of favorable true flight-altitude
wind or intended flight route; sunlight is not a measured thermal updraft.
"""
from __future__ import annotations
import argparse,json,math,statistics,tempfile,time,urllib.parse,urllib.request
from pathlib import Path
from collections import Counter,defaultdict
from datetime import timedelta,datetime
from concurrent.futures import ThreadPoolExecutor,as_completed

from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_predecision_candidates import SYSTEMS,daily_source_positions
from scripts.qc_payoff_b_complete_stationary_riskset import collect
from scripts.audit_payoff_b_riskday_weather import (
    sample_riskdays,sample_info,EXPECTED,MINIMUM
)
from scripts.audit_payoff_b_paired_weather import source_query
from scripts.run_payoff_b_stork_stage_handoff_pilot import percentile

SOURCE_VARS=("V10M","ALLSKY_SFC_SW_DWN")
HOURS_MIN=18
PRE_BASELINE_DAYS=7
SAMPLED_CASES=16
SAMPLED_STAYS=32


def request_query(site,day):
    base,start,reference=source_query(site,day)
    parts=urllib.parse.urlsplit(base)
    query=urllib.parse.parse_qs(parts.query)
    query["parameters"]=[",".join(SOURCE_VARS)]
    url=urllib.parse.urlunsplit((parts.scheme,parts.netloc,parts.path,
                                urllib.parse.urlencode(query,doseq=True),""))
    return url,start,reference


def parse_weather(payload,start,end):
    props=(payload.get("properties") or {}).get("parameter") or {}
    if not isinstance(props,dict):
        raise ValueError("Missing NASA POWER meteorology")
    hdr=payload.get("header") or {}
    ts=str(hdr.get("time_standard") or "").upper()
    if ts and ts not in ("UTC","UNIVERSAL TIME COORDINATED"):
        raise ValueError("NASA weather not UTC")
    result={}
    for var in SOURCE_VARS:
        table=props.get(var)
        if not isinstance(table,dict):
            raise ValueError("Missing directional weather field "+var)
        days=defaultdict(list)
        for key,val in table.items():
            stamp=str(key)
            if len(stamp)!=10 or not stamp.isdigit():
                raise ValueError("Invalid hourly key")
            dt=datetime.strptime(stamp,"%Y%m%d%H")
            if not start<=dt.date()<=end:
                raise ValueError("Weather after predecision or before baseline")
            f=float(val)
            if not math.isfinite(f) or f==-999.0:continue
            if var=="ALLSKY_SFC_SW_DWN" and f<0:continue
            days[dt.date()].append(f)
        dmeans=[]
        for n in range(PRE_BASELINE_DAYS+1):
            d=start+timedelta(days=n)
            a=days.get(d,[])
            if len(a)<HOURS_MIN:
                raise ValueError("Incomplete eight-day weather record")
            dmeans.append(statistics.mean(a))
        result[var]={
            "prior_decision_day_mean":dmeans[-1],
            "previous_seven_day_mean":statistics.mean(dmeans[:-1]),
            "change_vs_previous_seven_days":
                dmeans[-1]-statistics.mean(dmeans[:-1])
        }
    return result


def read_weather(site,day):
    url,start,end=request_query(site,day)
    last=None
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={
                "Accept":"application/json",
                "User-Agent":"PAYOFF-B-Predecision-Directional-Weather-20261022"
            })
            with urllib.request.urlopen(req,timeout=85) as f:
                dest=urllib.parse.urlsplit(f.geturl())
                if dest.scheme!="https" or dest.hostname!="power.larc.nasa.gov":
                    raise ValueError("Unexpected weather source")
                payload=json.load(f)
            return parse_weather(payload,start,end)
        except (OSError,ValueError,TypeError,TimeoutError) as e:
            last=e
            if attempt<2:time.sleep(attempt+1)
    raise RuntimeError(type(last).__name__+": "+str(last)[:120])


def summarize_source(selection,mapped):
    rows=defaultdict(list)
    errors=Counter()
    by_month=defaultdict(lambda:defaultdict(list))
    for digest,key,day,site,label in selection:
        url,*_=request_query(site,day)
        item=mapped.get(url)
        if not item or "error" in item:
            errors[item.get("error","UNKNOWN") if item else "MISSING"]+=1
            continue
        v={
          "northwind_prior_day":item["V10M"]["prior_decision_day_mean"],
          "northwind_anomaly":item["V10M"]["change_vs_previous_seven_days"],
          "shortwave_prior_day":item["ALLSKY_SFC_SW_DWN"]["prior_decision_day_mean"],
          "shortwave_anomaly":item["ALLSKY_SFC_SW_DWN"]["change_vs_previous_seven_days"],
        }
        rows[label].append(v)
        by_month[day.month][label].append(v)
    stats={}
    keys=("northwind_prior_day","northwind_anomaly",
          "shortwave_prior_day","shortwave_anomaly")
    for label,observations in rows.items():
        stats[label]={"n_weather_complete_days":len(observations)}
        for k in keys:
            a=[x[k] for x in observations]
            stats[label][k]={"mean":statistics.mean(a),
                             "median":statistics.median(a)}
    diff={}
    a=rows.get("NORTHWARD_CANDIDATE",[])
    b=rows.get("STAYED_TWO_DAYS",[])
    if a and b:
        diff={
            k:statistics.mean(x[k] for x in a)-
              statistics.mean(x[k] for x in b) for k in keys
        }
    monthly=[]
    for month in range(2,6):
        a=by_month[month].get("NORTHWARD_CANDIDATE",[])
        b=by_month[month].get("STAYED_TWO_DAYS",[])
        if min(len(a),len(b))<2:continue
        monthly.append({
            "month":month,"cases":len(a),"stays":len(b),
            **{k+"_case_minus_stay":statistics.mean(x[k] for x in a)-
                statistics.mean(x[k] for x in b) for k in keys}
        })
    return {
        "group_means":stats,
        "case_minus_stay_group_mean_differences":diff,
        "within_month_descriptive_differences":monthly,
        "weather_missing":dict(sorted(errors.items())),
        "northward_wind_10m_is_route_specific_tailwind":False,
        "solar_radiation_is_observed_updraft":False,
        "actual_animal_environmental_forecast_measured":False,
        "individual_observations_exported":False,
    }


def run_source(system,fetch=read_weather):
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"source.csv"
        doi,taxon,sensor,checksum=origin_source(system,path)
        g,c,idcol=daily_source_positions(path,taxon)
        risk,counts,_,_=collect(g)
        names=("all_at_risk_stationary_days","NORTHWARD_CANDIDATE",
               "STAYED_TWO_DAYS","OTHER_MOVEMENT","CENSORED")
        if tuple(counts[k] for k in names)!=EXPECTED[system]:
            raise ValueError("Original at-risk source cohort changed")
        selected=sample_riskdays(risk)
        info=sample_info(selected)
        if info["selected_riskday_outcomes"]!={"NORTHWARD_CANDIDATE":16,
                                               "STAYED_TWO_DAYS":32}:
            raise ValueError("Selected sample size deviated")
        unique={}
        for digest,key,day,site,label in selected:
            url,*_=request_query(site,day)
            unique[url]=(site,day)
        responses={}
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures={pool.submit(fetch,site,day):url
                     for url,(site,day) in unique.items()}
            for fut in as_completed(futures):
                url=futures[fut]
                try:responses[url]=fut.result()
                except Exception as e:responses[url]={"error":type(e).__name__}
        summary=summarize_source(selected,responses)
        passing=all(
            summary["group_means"].get(k,{}).get("n_weather_complete_days",0)
            >=MINIMUM[k] for k in MINIMUM)
        return {
            "status":"SOURCE_NORTHWIND_SOLAR_DESCRIPTIVE_COMPLETE"
                     if passing else "NOT_ESTIMABLE_INCOMPLETE_WEATHER",
            "source_doi":doi,"taxon":taxon,"sensor":sensor,
            "original_checksum":checksum,
            "sample":info,"unique_weather_queries":len(unique),
            "summary":summary,
            "true_direction_of_intended_route_not_observed":True,
            "physiological_fitness_effect_not_tested":True,
        }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--system",choices=SYSTEMS,required=True)
    parser.add_argument("--out",type=Path,
        default=Path("outputs/payoff_b_directional_weather"))
    a=parser.parse_args()
    receipt={
      "schema":"payoff_b_riskset_northwind_solar_source_v1",
      "source":a.system,
      "interpretation":"POST_TEMPERATURE_EXPLORATORY_PHYSICAL_CUE_PROXIES_ONLY",
      "meteorological_predictors":list(SOURCE_VARS),
      "weather_time":"UTC day before source anchor, previous 7-day baseline",
    }
    try:receipt["result"]=run_source(a.system)
    except Exception as e:
        receipt["result"]={"status":"FAILED_SOURCE_OR_WEATHER_GATE",
                           "error":type(e).__name__+": "+str(e)[:250]}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/(a.system+".json")).write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(receipt,indent=2,ensure_ascii=False))
    if receipt["result"]["status"]!="SOURCE_NORTHWIND_SOLAR_DESCRIPTIVE_COMPLETE":
        raise SystemExit("Northward wind/solar source gate failed")


if __name__=="__main__":main()
