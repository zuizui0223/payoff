#!/usr/bin/env python3
"""Sample full GPS stationary-day risk set, then retrieve *prior* physical weather.

This outcome-stratified source-availability pilot is not a real-world forecast
use, migration hazard or fitness test. Counts only, never ID/day/coordinates.
"""
from __future__ import annotations
import argparse,hashlib,json,random,statistics,tempfile
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path

from scripts.qc_payoff_b_complete_stationary_riskset import collect
from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_predecision_candidates import SYSTEMS,daily_source_positions
from scripts.audit_payoff_b_paired_weather import fetch_weather,source_query
from scripts.run_payoff_b_stork_stage_handoff_pilot import percentile

SALT="PAYOFF-B-FULL-AT-RISK-20261022-v1"
CAPS={"NORTHWARD_CANDIDATE":16,"STAYED_TWO_DAYS":32}
MINIMUM={"NORTHWARD_CANDIDATE":12,"STAYED_TWO_DAYS":20}
EXPECTED={"stork":(1633,156,941,352,184),
          "white_fronted_goose":(2008,111,1456,285,156),
          "curlew":(1868,66,1632,90,80)}


def sample_riskdays(private,caps=CAPS):
    grouped=defaultdict(list)
    for key,day,site,label in private:
        if label not in caps:continue
        tax,ident,year=key
        h=hashlib.sha256(
            (SALT+"|"+tax+"|"+ident+"|"+str(year)+"|"+day.isoformat()).encode()
        ).hexdigest()
        grouped[(label,day.month)].append((h,key,day,site,label))
    for b in grouped.values():b.sort(key=lambda x:x[0])
    out=[]
    for label,cap in caps.items():
        seen=set()
        pool={m:list(grouped.get((label,m),[])) for m in range(2,6)}
        while len([x for x in out if x[4]==label])<cap and any(pool.values()):
            hit=False
            for month in range(2,6):
                rows=pool[month]
                while rows and rows[0][1] in seen:rows.pop(0)
                if rows and sum(x[4]==label for x in out)<cap:
                    item=rows.pop(0)
                    out.append(item)
                    seen.add(item[1])
                    hit=True
            if not hit:break
    return out


def sample_info(rows):
    c=Counter(row[4] for row in rows)
    months=defaultdict(Counter)
    seen=defaultdict(set)
    for digest,key,day,site,label in rows:
        if key in seen[label]:raise ValueError("Repeated identity/year within status")
        seen[label].add(key)
        months[label][str(day.month)]+=1
    return {
        "selected_riskday_outcomes":dict(sorted(c.items())),
        "selected_month_distribution":{
            k:dict(sorted(v.items())) for k,v in sorted(months.items())
        },
        "at_most_one_sample_day_per_animal_year_and_status":True,
        "selection_uses_weather":False,
        "sample_is_outcome_stratified":True,
        "sampled_case_fraction_is_population_probability":False,
    }


def quantiles(values):
    if not values:return None
    rng=random.Random(20261022+len(values))
    means=[statistics.mean(rng.choices(values,k=len(values))) for _ in range(1500)]
    return [percentile(means,.025),percentile(means,.975)]


def summarize(rows,mapped):
    complete=defaultdict(list)
    errors=Counter()
    for digest,key,day,site,label in rows:
        url,*_=source_query(site,day)
        r=mapped.get(url)
        if r is None or "error" in r:
            errors[r.get("error","MISSING") if r is not None else "NO_DATA"]+=1
            continue
        complete[label].append({
            "month":day.month,
            "temperature_anomaly_c":r["T2M"]["predecision_anomaly"],
            "wind_speed_anomaly_m_s":r["WS10M"]["predecision_anomaly"],
            "temperature_prior_day_c":r["T2M"]["last_predecision_day"],
            "wind_speed_prior_day_m_s":r["WS10M"]["last_predecision_day"],
        })
    descriptions={}
    for label,items in complete.items():
        row={"n_valid_riskdays":len(items)}
        for variable in ("temperature_anomaly_c","wind_speed_anomaly_m_s",
                         "temperature_prior_day_c","wind_speed_prior_day_m_s"):
            v=[z[variable] for z in items]
            row[variable]={
                "mean":statistics.mean(v),"median":statistics.median(v),
                "bootstrap_95pct_descriptive":quantiles(v),
            }
        descriptions[label]=row
    monthly=[]
    for month in range(2,6):
        case=[a for a in complete.get("NORTHWARD_CANDIDATE",[])
              if a["month"]==month]
        stay=[a for a in complete.get("STAYED_TWO_DAYS",[])
              if a["month"]==month]
        if min(len(case),len(stay))<2:continue
        monthly.append({
            "month":month,"case_days":len(case),"stay_days":len(stay),
            "case_minus_stay_temperature_anomaly_c":
                statistics.mean(v["temperature_anomaly_c"] for v in case)-
                statistics.mean(v["temperature_anomaly_c"] for v in stay),
            "case_minus_stay_wind_speed_anomaly_m_s":
                statistics.mean(v["wind_speed_anomaly_m_s"] for v in case)-
                statistics.mean(v["wind_speed_anomaly_m_s"] for v in stay),
        })
    return {
        "complete_weather_by_outcome":descriptions,
        "weather_missing_reasons":dict(sorted(errors.items())),
        "descriptive_month_moderated_contrasts":monthly,
        "modelled_true_migration_hazard":False,
        "observational_causal_weather_use":False,
        "weather_reanalysis_is_observed_forecast":False,
        "sources_not_independent_per_bird_day":True,
        "individual_gps_date_or_weather_exported":False,
    }


def run_source(system,weather_fetch=fetch_weather):
    with tempfile.TemporaryDirectory() as td:
        original=Path(td)/"public.csv"
        doi,taxon,sensor,integrity=origin_source(system,original)
        tracks,source_counts,ident=daily_source_positions(original,taxon)
        risk,c,_,_=collect(tracks)
        keys=("all_at_risk_stationary_days","NORTHWARD_CANDIDATE",
              "STAYED_TWO_DAYS","OTHER_MOVEMENT","CENSORED")
        if tuple(c[k] for k in keys)!=EXPECTED[system]:
            raise ValueError("Source risk-set admission counts changed")
        selected=sample_riskdays(risk)
        selection=sample_info(selected)
        counts=selection["selected_riskday_outcomes"]
        if any(counts.get(k,0)<MINIMUM[k] for k in CAPS):
            return {"status":"NOT_ESTIMABLE_SAMPLE_SIZE",
                    "source_doi":doi,"sample":selection}
        jobs={}
        for digest,key,day,site,label in selected:
            url,*_=source_query(site,day)
            jobs[url]=(site,day)
        values={}
        with ThreadPoolExecutor(max_workers=4) as pool:
            pending={pool.submit(weather_fetch,site,day):url
                     for url,(site,day) in jobs.items()}
            for fut in as_completed(pending):
                url=pending[fut]
                try:values[url]=fut.result()
                except Exception as e:values[url]={"error":type(e).__name__}
        summary=summarize(selected,values)
        admitted=summary["complete_weather_by_outcome"]
        good=all(admitted.get(k,{}).get("n_valid_riskdays",0)>=MINIMUM[k]
                 for k in CAPS)
        return {
            "status":"WEATHER_DESCRIPTIVE_SOURCE_COMPLETE"
                     if good else "NOT_ESTIMABLE_WEATHER_COMPLETENESS",
            "source_doi":doi,"source_taxon":taxon,
            "original_pinned_source":integrity,
            "source_counts":dict(sorted(c.items())),
            "selection":selection,
            "unique_public_weather_queries":len(jobs),
            "aggregate_weather":summary,
            "meteorology_is_retrospective_not_perceived_by_bird":True,
            "no_record_level_outputs":True,
        }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--system",choices=SYSTEMS,required=True)
    ap.add_argument("--out",type=Path,default=Path("outputs/payoff_b_riskday_weather"))
    a=ap.parse_args()
    record={
        "schema":"payoff_b_riskday_weather_source_pilot_20261022",
        "system":a.system,
        "analysis":"SAMPLED_RISKSET_DESCRIPTIVE_NOT_CAUSAL",
        "physical_input_timing":"UTC reference day minus one, vs 7 prior days",
        "selection_limit":"16 cases/32 stays per source, independent month-round-robin hash",
    }
    try:record["result"]=run_source(a.system)
    except Exception as e:
        record["result"]={"status":"SOURCE_OR_METEOROLOGY_FAILURE",
                          "error":type(e).__name__+": "+str(e)[:240]}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/(a.system+".json")).write_text(
        json.dumps(record,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(record,indent=2,ensure_ascii=False))
    if record["result"]["status"]!="WEATHER_DESCRIPTIVE_SOURCE_COMPLETE":
        raise SystemExit("Riskday meteorology source admission failed")


if __name__=="__main__":main()
