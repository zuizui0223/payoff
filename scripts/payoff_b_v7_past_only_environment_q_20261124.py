#!/usr/bin/env python3
"""V7 source-only historical information q: prior-years-only original phenology.

This independent supplementary availability gate does not change the frozen
2026-10-05 V7 primary contract. It calculates environmental predictability
ONLY when a separately authenticated original Kölzsch 2015 source-onset table
is provided. It never reads goose timing, individual GPS, social observation
or a model of fitness. A missing source returns NOT_ESTIMABLE, not fake data.
"""
from __future__ import annotations

import argparse,csv,json,math
from collections import defaultdict
from pathlib import Path
from statistics import mean
from hashlib import sha256

SCHEMA_DOY=("flyway","transition","year","source_spring_onset_doy","target_spring_onset_doy")
SCHEMA_ANOMALY=("flyway","transition","year","source_onset_anomaly_days","target_onset_anomaly_days")
SCHEMA=SCHEMA_DOY
CONTRACT=Path(__file__).resolve().parents[1]/"data/payoff_b_v7_predecision_historical_q_support_contract_20261124.json"

def _onset_num(x,representation):
    try:v=float(x)
    except (TypeError,ValueError):return None
    if not math.isfinite(v):return None
    # Original supporting Tables S2–S7 report onset *anomalies*. A constant
    # full-series mean subtraction is harmless to past-only correlation and
    # forecast-minus-observed differences, but NOT a source DOY.
    if representation=="anomaly":
        return v if -100<=v<=100 else None
    return v if 1<=v<=366 else None

def parse_env_rows(csv_text,representation="doy"):
    if representation not in ("doy","anomaly"):
        raise ValueError("Unregistered original spring-source representation")
    fields=SCHEMA_DOY if representation=="doy" else SCHEMA_ANOMALY
    lines=csv.DictReader(csv_text.splitlines())
    if tuple(lines.fieldnames or ())!=fields:
        raise ValueError("Only exact historical environment-only five-field source allowed")
    rows=[]
    observed=set()
    for item in lines:
        group=str(item["flyway"] or "").strip().lower()
        transition=str(item["transition"] or "").strip()
        year=int(item["year"])
        if not group or not transition or year<1982 or year>2011:
            raise ValueError("Unexpected historical climate cohort/time field")
        key=(group,transition,year)
        if key in observed:
            raise ValueError("Duplicate original transition-year phenology source")
        observed.add(key)
        rows.append({"flyway":group,"transition":transition,"year":year,
                     "source":_onset_num(item[fields[3]],representation),
                     "target":_onset_num(item[fields[4]],representation)})
    return rows

def historical_forecast(rows,focal_year,min_prior=20):
    if not 2006<=focal_year<=2011:
        raise ValueError("Out of registered original migration years")
    if any(r["year"]>=focal_year for r in rows):
        raise ValueError("Future or focal environmental target leaked into training")
    prior=[r for r in rows if r["source"] is not None and r["target"] is not None]
    if len(prior)<min_prior:
        return {"status":"INSUFFICIENT_PAST_ENVIRONMENT_YEARS","n_prior_pairs":len(prior)}
    xs=[r["source"] for r in prior]
    ys=[r["target"] for r in prior]
    avgx=mean(xs);avgy=mean(ys)
    sx=sum((x-avgx)**2 for x in xs)
    sy=sum((y-avgy)**2 for y in ys)
    if sx<=0 or sy<=0:
        return {"status":"ZERO_VARIANCE_HISTORICAL_Q_NOT_ESTIMABLE","n_prior_pairs":len(prior)}
    cov=sum((x-avgx)*(y-avgy) for x,y in zip(xs,ys))
    r=cov/math.sqrt(sx*sy)
    slope=cov/sx
    return {"status":"PAST_ONLY_ENVIRONMENT_PREDICTIVE_MODEL_ESTIMABLE",
            "n_prior_pairs":len(prior),
            "latest_training_year":max(x["year"] for x in prior),
            "signed_historical_source_target_r":r,
            "past_source_mean":avgx,
            "past_destination_mean":avgy,
            "historical_slope":slope}

def one_focal_year(training,focal):
    h=historical_forecast(training,focal["year"])
    if h["status"]!="PAST_ONLY_ENVIRONMENT_PREDICTIVE_MODEL_ESTIMABLE":
        return h
    if focal["source"] is None or focal["target"] is None:
        return {"status":"CURRENT_YEAR_ENVIRONMENT_OBSERVATION_MISSING"}
    forecast=h["past_destination_mean"]+h["historical_slope"]*(focal["source"]-h["past_source_mean"])
    return {
       "status":"FORWARD_ENVIRONMENT_SPRING_FORECAST_SCORED_NOT_BIRD_DECISION",
       "year":focal["year"],
       "n_prior_pairs":h["n_prior_pairs"],
       "latest_training_year":h["latest_training_year"],
       "signed_historical_source_target_r":h["signed_historical_source_target_r"],
       "source_to_target_forecast_squared_error_days2":(forecast-focal["target"])**2,
       "past_destination_climatology_squared_error_days2":(h["past_destination_mean"]-focal["target"])**2,
       "current_year_target_used_in_training":False,
       "future_environment_years_used_in_training":False,
       "actual_bird_had_source_onset_before_departure_verified":False,
    }

def evaluate(data,contract):
    original_years=contract["time_rule"]["focal_migration_years"]
    groups=defaultdict(list)
    for row in data:
        groups[(row["flyway"],row["transition"])].append(row)
    out=[]
    for group,items in sorted(groups.items()):
        byyear={r["year"]:r for r in items}
        for year in original_years:
            if year not in byyear:
                continue
            past=[r for r in items if r["year"]<year]
            result=one_focal_year(past,byyear[year])
            if result["status"]=="FORWARD_ENVIRONMENT_SPRING_FORECAST_SCORED_NOT_BIRD_DECISION":
                result["flyway"],result["transition"]=group
                out.append(result)
    flyways={r["flyway"] for r in out}
    transitions={(r["flyway"],r["transition"]) for r in out}
    scored_years={r["year"] for r in out}
    admissible=(
      len(transitions)>=contract["threshold_gate"]["independent_historical_transitions_min"]
      and len(flyways)>=contract["threshold_gate"]["independent_flyways_min"]
      and len(scored_years)>=contract["threshold_gate"]["distinct_focal_years_min"]
    )
    n=len(out)
    return {
      "status":"HISTORICAL_ENVIRONMENT_Q_SUPPORT_ESTIMABLE_ONLY" if admissible else
               "V7_HISTORICAL_Q_SOURCE_SUPPORT_GATE_NOT_MET",
      "n_environment_only_forward_year_scores":n,
      "n_flyways_with_forward_year_scores":len(flyways),
      "n_frozen_transitions_with_forward_year_scores":len(transitions),
      "n_distinct_focal_years_with_scores":len(scored_years),
      "environmental_forecast_scores_only":out,
      "actual_predeparture_source_onset_exposure_verified":False,
      "bird_focal_migration_timing_accessed":False,
      "information_reliability_q_as_bird_cognition_estimated":False,
      "ecological_recourse_r_or_q_times_r_fitted":False,
      "no_ebird":True,
      "claim_limit":"Past-only environmental forecast association, not evidence birds had or used this information before departure; V7 original q definition is unchanged."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-csv",type=Path)
    p.add_argument("--source-format",choices=["doy","anomaly"])
    p.add_argument("--contract",type=Path,default=CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    contract_bytes=args.contract.read_bytes()
    c=json.loads(contract_bytes)
    if args.source_csv is None:
        result={
          "status":"V7_HISTORICAL_Q_SOURCE_NOT_MATERIALIZED",
          "original_historical_source":"Kölzsch 2015 original 1982–2011 stopover region spring onset series",
          "reason":"No authenticated region-transition/year environmental source table was supplied. No q value or new biology is invented.",
          "no_bird_GPS_or_migration_outcome_opened":True,
          "no_original_V7_contract_changed":True,
          "no_ebird":True
        }
    else:
        if args.source_format is None:
            raise ValueError("Explicit original environment representation required (doy or anomaly)")
        parsed=parse_env_rows(args.source_csv.read_text(),representation=args.source_format)
        result=evaluate(parsed,c)
        result["source_representation"]=args.source_format
        result["source_file_sha256"]=sha256(args.source_csv.read_bytes()).hexdigest()
        result["historical_environment_source_authentication"] = "EXTERNAL_SOURCE_PROVENANCE_MUST_BE_VERIFIED_SEPARATELY"
    result["date"]=c["date"]
    result["source_gate_contract_sha256"]=sha256(contract_bytes).hexdigest()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print("V7_PAST_ONLY_Q_SOURCE_DIAG="+json.dumps(result,separators=(",",":")))

if __name__=="__main__":
    main()
