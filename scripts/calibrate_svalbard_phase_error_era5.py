#!/usr/bin/env python3
"""Replicate the frozen Svalbard barnacle-goose R2->R4 controller with ERA5.

The fixed-transition lambda and stopover slopes are invariant to adding a
constant phenology anchor within each region. Therefore this reliability lane
uses source-specific annual onset anomalies only and does not depend on the
published/figure-derived absolute anchor values used elsewhere in the Svalbard
analysis.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import asdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

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


def request_era5_daily(session,endpoint,lat,lon,start_year,end_year):
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
                    value=float(temp)
                    if not math.isfinite(value):
                        continue
                    by_day.setdefault(str(ts)[:10],[]).append(value)
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


def build_transition_table(stopovers,eligible,anomalies):
    import numpy as np
    import pandas as pd

    stops=stopovers[stopovers["region_id"].astype(str).isin(eligible)].copy()
    stops["region_id"]=stops["region_id"].astype(str)
    stops=stops.sort_values(["individual_id","year","start"])
    visits=[]
    for (ind,year),d in stops.groupby(["individual_id","year"]):
        d=d[d["region_id"].notna()].copy()
        current=None
        for _,row in d.iterrows():
            rid=str(row["region_id"])
            if current is None or rid!=current["region_id"]:
                if current is not None:
                    visits.append(current)
                current={
                    "individual_id":str(ind),
                    "year":int(year),
                    "region_id":rid,
                    "arrival":row["start"],
                    "departure":row["end"],
                }
            else:
                current["departure"]=max(current["departure"],row["end"])
        if current is not None:
            visits.append(current)

    frame=pd.DataFrame(visits)
    frame["arrival"]=pd.to_datetime(frame["arrival"],utc=True)
    frame["departure"]=pd.to_datetime(frame["departure"],utc=True)
    frame["arrival_doy"]=frame["arrival"].map(doy_fraction)
    frame["stopover_days"]=(frame["departure"]-frame["arrival"]).dt.total_seconds()/86400.0

    env=anomalies[anomalies["fit_status"]=="PASS"][
        ["region_id","year","onset_anomaly_days"]
    ].copy()
    env["region_id"]=env["region_id"].astype(str)
    frame=frame.merge(env,on=["region_id","year"],how="left")
    frame["arrival_phase"]=frame["arrival_doy"]-frame["onset_anomaly_days"]

    out=[]
    for (ind,year),d in frame.groupby(["individual_id","year"]):
        d=d.sort_values("arrival").reset_index(drop=True)
        for i in range(len(d)-1):
            a,b=d.iloc[i],d.iloc[i+1]
            if a["region_id"]==b["region_id"]:
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
    return pd.DataFrame(out)


def main():
    args=parse_args()
    try:
        import pandas as pd
        import requests
    except ImportError as exc:
        raise RuntimeError("Svalbard ERA5 calibration requires pandas and requests") from exc

    reg=json.loads(args.registration_json.read_text(encoding="utf-8"))
    src=reg["source_artifact"]["required_files"]
    regions=pd.read_csv(args.source_dir/src["regions"])
    stops=pd.read_csv(args.source_dir/src["stopovers"],parse_dates=["start","end"])
    power=pd.read_csv(args.source_dir/src["power_onsets"])

    eligible_regions=regions[regions["published_region_eligible"]==True].copy()
    eligible=set(eligible_regions["region_id"].astype(str))
    if eligible!={"R1","R2","R3","R4"}:
        raise SystemExit(f"unexpected eligible Svalbard regions: {sorted(eligible)}")

    start_year=int(reg["phenology_contract"]["baseline_start_year"])
    end_year=int(reg["phenology_contract"]["baseline_end_year"])
    expected_years=int(reg["phenology_contract"]["expected_years_per_region"])
    endpoint=reg["replicate_environment_source"]["api_endpoint"]
    session=requests.Session()
    session.headers.update({"User-Agent":"PAYOFF-B-Svalbard-ERA5-reliability/1.0"})

    rows=[]
    for region in eligible_regions.itertuples(index=False):
        rid=str(region.region_id); lat=float(region.lat); lon=float(region.lon)
        daily=request_era5_daily(session,endpoint,lat,lon,start_year,end_year)
        dframe=pd.DataFrame(daily,columns=["date","t2m_c"])
        dframe["date"]=pd.to_datetime(dframe["date"])
        dframe["year"]=dframe["date"].dt.year
        for year in range(start_year,end_year+1):
            d=dframe[dframe["year"]==year].sort_values("date")
            status="PASS"; onset=None; r2=None
            try:
                if len(d)<360:
                    raise ValueError(f"daily_coverage={len(d)}")
                fit=fit_gdd_jerk(d["t2m_c"].to_numpy(),lat,min_r_squared=0.95)
                onset=float(fit.onset_day); r2=float(fit.r_squared)
            except Exception as exc:
                status=f"FAIL:{type(exc).__name__}:{exc}"
            rows.append({
                "region_id":rid,"year":year,"onset_doy":onset,
                "gdd_fit_r2":r2,"fit_status":status
            })

    era=pd.DataFrame(rows)
    passed=era["fit_status"]=="PASS"
    means=era.loc[passed].groupby("region_id")["onset_doy"].mean().to_dict()
    era["region_mean_doy"]=era["region_id"].map(means)
    era["onset_anomaly_days"]=era["onset_doy"]-era["region_mean_doy"]

    args.output_dir.mkdir(parents=True,exist_ok=True)
    era_path=args.output_dir/"svalbard_era5_gdd_anomalies.csv"
    era.to_csv(era_path,index=False)

    power_anom=power.copy()
    if "onset_anomaly_days" not in power_anom.columns:
        raise SystemExit("POWER onset source lacks onset_anomaly_days")

    power_trans=build_transition_table(stops,eligible,power_anom)
    era_trans=build_transition_table(stops,eligible,era)
    primary=reg["primary_transition"]
    o=primary["origin_region"]; d=primary["destination_region"]
    psub=power_trans[(power_trans.origin_region==o)&(power_trans.destination_region==d)].copy()
    esub=era_trans[(era_trans.origin_region==o)&(era_trans.destination_region==d)].copy()
    pfit=fit_fixed_transition_controller(psub,origin_phase_column="origin_phase",destination_phase_column="destination_phase")
    efit=fit_fixed_transition_controller(esub,origin_phase_column="origin_phase",destination_phase_column="destination_phase")

    power_identity=abs(pfit.lambda_hat-float(primary["expected_POWER_lambda"])) <= float(reg["gates"]["power_refit_max_abs_lambda_error"])
    sample_identity=(
        pfit.n==int(primary["expected_n"])
        and pfit.n_individuals==int(primary["expected_individuals"])
        and efit.n==pfit.n
        and efit.n_individuals==pfit.n_individuals
    )
    coverage_by_region={
        str(rid):int(
            era.loc[
                (era["region_id"].astype(str)==str(rid)) & passed,
                "year",
            ].nunique()
        )
        for rid in sorted(eligible)
    }
    coverage_gate=all(v==expected_years for v in coverage_by_region.values())

    paired=power_anom[power_anom["fit_status"]=="PASS"][
        ["region_id","year","onset_anomaly_days"]
    ].merge(
        era[era["fit_status"]=="PASS"][
            ["region_id","year","onset_anomaly_days"]
        ],
        on=["region_id","year"],suffixes=("_power","_era5"),how="inner"
    )
    paired["difference"]=paired["onset_anomaly_days_era5"]-paired["onset_anomaly_days_power"]
    disagreement=summarize_replicate_differences(paired["difference"])

    gate=bool(power_identity and sample_identity and coverage_gate)
    receipt={
        "status":"svalbard_era5_reliability_complete" if gate else "svalbard_era5_reliability_gate_fail",
        "registration_source":str(args.registration_json),
        "coverage_by_region":coverage_by_region,
        "coverage_gate":coverage_gate,
        "power_identity_gate":power_identity,
        "sample_identity_gate":sample_identity,
        "power_controller":asdict(pfit),
        "era5_controller":asdict(efit),
        "era5_minus_power_lambda_hat":efit.lambda_hat-pfit.lambda_hat,
        "region_year_replicate_disagreement":asdict(disagreement),
        "Aikens_lambda_outcome_opened":False,
        "claim_boundary":reg["claim_boundary"]
    }
    args.receipt_output.parent.mkdir(parents=True,exist_ok=True)
    args.receipt_output.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(args.receipt_output)
    print(json.dumps(receipt,indent=2))
    if args.fail_on_gate_failure and not gate:
        raise SystemExit("Svalbard ERA5 reliability gate failed")


if __name__=="__main__":
    main()
