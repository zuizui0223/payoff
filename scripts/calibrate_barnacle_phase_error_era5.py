#!/usr/bin/env python3
"""Replicate two preregistered barnacle-goose lambda estimates with ERA5."""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.barnacle_phase_error_calibration import (
    fit_fixed_transition_controller,
    fit_gdd_jerk,
    summarize_replicate_differences,
)


def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",type=Path,required=True)
    p.add_argument("--registration-json",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    p.add_argument("--receipt-output",type=Path,required=True)
    p.add_argument("--fail-on-gate-failure",action="store_true")
    return p.parse_args()


def request_era5_daily(session, endpoint, lat, lon, start_year, end_year):
    rows=[]
    for y0 in range(start_year,end_year+1,4):
        y1=min(end_year,y0+3)
        params={
            "latitude":f"{lat:.8f}",
            "longitude":f"{lon:.8f}",
            "start_date":f"{y0}-01-01",
            "end_date":f"{y1}-12-31",
            "hourly":"temperature_2m",
            "models":"era5",
            "timezone":"GMT",
            "cell_selection":"nearest",
            "elevation":"nan",
            "temperature_unit":"celsius",
        }
        last=None
        for attempt in range(5):
            try:
                response=session.get(endpoint,params=params,timeout=120)
                response.raise_for_status()
                payload=response.json()
                hourly=payload["hourly"]
                by_day={}
                for ts,temp in zip(hourly["time"],hourly["temperature_2m"]):
                    if temp is None:
                        continue
                    v=float(temp)
                    if not math.isfinite(v):
                        continue
                    by_day.setdefault(str(ts)[:10],[]).append(v)
                for day,values in by_day.items():
                    if len(values)==24:
                        rows.append((day,sum(values)/24.0))
                last=None
                break
            except Exception as exc:
                last=exc
                time.sleep(1.5*(attempt+1))
        if last is not None:
            raise RuntimeError(f"ERA5 request failed for {lat},{lon}: {last}")
        time.sleep(0.15)
    return rows


def doy_fraction(ts):
    import pandas as pd
    ts=pd.Timestamp(ts)
    start=pd.Timestamp(year=ts.year,month=1,day=1,tz=ts.tz)
    return 1.0+(ts-start).total_seconds()/86400.0


def build_transitions(stopovers,eligible,anomalies):
    import numpy as np
    stops=stopovers[stopovers["region_id"].astype(str).isin(eligible)].copy()
    stops["region_id"]=stops["region_id"].astype(str)
    stops["arrival_doy"]=stops["start"].apply(doy_fraction)
    stops["departure_doy"]=stops["end"].apply(doy_fraction)
    stops["stopover_days"]=stops["duration_hours"]/24.0
    env=anomalies[anomalies["fit_status"]=="PASS"][
        ["region_id","year","onset_anomaly_days"]
    ].copy()
    env["region_id"]=env["region_id"].astype(str)
    visits=stops.merge(env,on=["region_id","year"],how="left")
    visits["arrival_phase"]=visits["arrival_doy"]-visits["onset_anomaly_days"]
    visits["departure_phase"]=visits["departure_doy"]-visits["onset_anomaly_days"]
    out=[]
    for (ind,year),d in visits.groupby(["individual_id","year"]):
        d=d.sort_values("start").reset_index(drop=True)
        for i in range(len(d)-1):
            a,b=d.iloc[i],d.iloc[i+1]
            if str(a["region_id"])==str(b["region_id"]):
                continue
            if not np.isfinite(a["arrival_phase"]) or not np.isfinite(b["arrival_phase"]):
                continue
            out.append({
                "individual_id":str(ind),
                "year":int(year),
                "origin_region":str(a["region_id"]),
                "destination_region":str(b["region_id"]),
                "origin_phase":float(a["arrival_phase"]),
                "destination_phase":float(b["arrival_phase"]),
                "origin_stopover_days":float(a["stopover_days"]),
            })
    import pandas as pd
    return pd.DataFrame(out)


def main():
    args=parse_args()
    try:
        import pandas as pd
        import requests
    except ImportError as exc:
        raise RuntimeError("barnacle ERA5 calibration requires pandas and requests") from exc

    reg=json.loads(args.registration_json.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    endpoint=reg["replicate_environment_source"]["api_endpoint"]
    start_year=int(reg["phenology_contract"]["baseline_start_year"])
    end_year=int(reg["phenology_contract"]["baseline_end_year"])
    expected_years=end_year-start_year+1
    session=requests.Session()
    session.headers.update({"User-Agent":"PAYOFF-B-barnacle-ERA5-reliability/1.0"})

    flyway_results=[]
    all_gate=True
    for spec in reg["flyways"]:
        fly=spec["flyway"]
        files=spec["required_files"]
        regions=pd.read_csv(args.source_dir/files["regions"])
        stopovers=pd.read_csv(args.source_dir/files["stopovers"],parse_dates=["start","end"])
        power=pd.read_csv(args.source_dir/files["power_anomalies"])
        eligible_regions=regions
        if "published_region_eligible" in regions.columns:
            eligible_regions=regions[regions["published_region_eligible"]==True].copy()
        eligible=set(eligible_regions["region_id"].astype(str))

        era_rows=[]
        for row in eligible_regions.itertuples(index=False):
            rid=str(row.region_id); lat=float(row.lat); lon=float(row.lon)
            daily=request_era5_daily(session,endpoint,lat,lon,start_year,end_year)
            frame=pd.DataFrame(daily,columns=["date","t2m_c"])
            frame["date"]=pd.to_datetime(frame["date"])
            frame["year"]=frame["date"].dt.year
            for year in range(start_year,end_year+1):
                d=frame[frame["year"]==year].sort_values("date")
                status="PASS"; onset=None; r2=None
                try:
                    if len(d)<360:
                        raise ValueError(f"daily_coverage={len(d)}")
                    fit=fit_gdd_jerk(d["t2m_c"].to_numpy(),lat,min_r_squared=0.95)
                    onset=float(fit.onset_day); r2=float(fit.r_squared)
                except Exception as exc:
                    status=f"FAIL:{type(exc).__name__}:{exc}"
                era_rows.append({
                    "region_id":rid,"year":year,"onset_doy_raw":onset,
                    "gdd_fit_r2":r2,"fit_status":status
                })

        era=pd.DataFrame(era_rows)
        passed=era["fit_status"]=="PASS"
        means=era.loc[passed].groupby("region_id")["onset_doy_raw"].mean().to_dict()
        era["region_mean_raw_doy"]=era["region_id"].map(means)
        era["onset_anomaly_days"]=era["onset_doy_raw"]-era["region_mean_raw_doy"]
        era_path=args.output_dir/f"{fly}_era5_gdd_anomalies.csv"
        era.to_csv(era_path,index=False)

        power_trans=build_transitions(stopovers,eligible,power)
        era_trans=build_transitions(stopovers,eligible,era)
        primary=spec["primary_transition"]
        o=primary["origin_region"]; d=primary["destination_region"]
        psub=power_trans[(power_trans.origin_region==o)&(power_trans.destination_region==d)].copy()
        esub=era_trans[(era_trans.origin_region==o)&(era_trans.destination_region==d)].copy()
        pfit=fit_fixed_transition_controller(psub,origin_phase_column="origin_phase",destination_phase_column="destination_phase")
        efit=fit_fixed_transition_controller(esub,origin_phase_column="origin_phase",destination_phase_column="destination_phase")

        power_identity=abs(pfit.lambda_hat-float(primary["expected_POWER_lambda"])) <= float(reg["gates"]["power_refit_max_abs_lambda_error"])
        n_identity=(pfit.n==int(primary["expected_n"]) and pfit.n_individuals==int(primary["expected_individuals"]) and efit.n==pfit.n and efit.n_individuals==pfit.n_individuals)
        coverage_by_region={
            str(rid):int((era[(era.region_id.astype(str)==str(rid))]&passed)["year"].nunique())
            for rid in sorted(eligible)
        }
        coverage_gate=all(v==expected_years for v in coverage_by_region.values())

        paired=power[power["fit_status"]=="PASS"][["region_id","year","onset_anomaly_days"]].merge(
            era[era["fit_status"]=="PASS"][["region_id","year","onset_anomaly_days"]],
            on=["region_id","year"],suffixes=("_power","_era5"),how="inner"
        )
        paired["difference"]=paired["onset_anomaly_days_era5"]-paired["onset_anomaly_days_power"]
        disagreement=summarize_replicate_differences(paired["difference"])
        fly_gate=bool(power_identity and n_identity and coverage_gate)
        all_gate=all_gate and fly_gate
        flyway_results.append({
            "flyway":fly,
            "primary_transition":primary,
            "coverage_by_region":coverage_by_region,
            "coverage_gate":coverage_gate,
            "power_identity_gate":power_identity,
            "sample_identity_gate":n_identity,
            "power_controller":asdict(pfit),
            "era5_controller":asdict(efit),
            "era5_minus_power_lambda_hat":efit.lambda_hat-pfit.lambda_hat,
            "region_year_replicate_disagreement":asdict(disagreement),
            "gate_passed":fly_gate
        })

    receipt={
        "status":"barnacle_era5_reliability_complete" if all_gate else "barnacle_era5_reliability_gate_fail",
        "registration_source":str(args.registration_json),
        "source_artifact":reg["source_artifact"],
        "flyways":flyway_results,
        "Aikens_lambda_outcome_opened":False,
        "claim_boundary":reg["claim_boundary"]
    }
    args.receipt_output.parent.mkdir(parents=True,exist_ok=True)
    args.receipt_output.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(args.receipt_output)
    print(json.dumps(receipt,indent=2))
    if args.fail_on_gate_failure and not all_gate:
        raise SystemExit("barnacle ERA5 reliability gate failed")


if __name__=="__main__":
    main()
