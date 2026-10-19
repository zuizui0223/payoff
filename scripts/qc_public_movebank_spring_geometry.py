#!/usr/bin/env python3
"""Outcome-blind normalized northward movement coverage for distinct bird taxa.

Only GPS/Argos source-location geometry is examined, not movement/cue/fitness
effect fits. No individual IDs, raw observations or exact locations exported.
The rule and all source MD5 values were committed before this script ran.
"""
from __future__ import annotations
import argparse,csv,json,math,statistics,tempfile
from collections import Counter,defaultdict
from datetime import datetime
from pathlib import Path

from scripts.qc_public_movebank_crossguild import (
    SOURCES,download_verified,
)
from scripts.qc_public_movebank_crossguild_v2 import SOURCE as V2

SYSTEMS={"curlew":"curlew","woodcock_argos":"woodcock_argos",
         "dabbling_ducks":"dabbling_ducks","stork":"stork"}
MONTHS={2,3,4,5}
MIN_UNIQUE_SPRING_DAYS=12
MIN_LAT_RANGE=10.0
MIN_EARLY_LATE_NORTHING=7.0
CROSSING_FRACTIONS=(0.2,0.8)


def quantile(values,p):
    v=sorted(values)
    if not v:raise ValueError("empty quantile")
    k=(len(v)-1)*p
    i=int(k)
    return v[i]*(1-(k-i))+v[min(i+1,len(v)-1)]*(k-i)


def analyze_one(daily):
    """daily: sequence of (date, mean latitude) ordered within Feb-May."""
    s=sorted(daily)
    if len(s)<MIN_UNIQUE_SPRING_DAYS:
        return {"status":"NOT_ENOUGH_SPRING_DATES"}
    lo=quantile([lat for _,lat in s],0.1)
    hi=quantile([lat for _,lat in s],0.9)
    span=hi-lo
    if span<MIN_LAT_RANGE:
        return {"status":"LATITUDINAL_RANGE_UNRESOLVED"}
    begin=statistics.median(lat for _,lat in s[:5])
    end=statistics.median(lat for _,lat in s[-5:])
    if end-begin<MIN_EARLY_LATE_NORTHING:
        return {"status":"NET_NORTHWARD_CHANGE_UNRESOLVED"}
    thresh_low=lo+CROSSING_FRACTIONS[0]*span
    thresh_high=lo+CROSSING_FRACTIONS[1]*span
    if s[0][1]>=thresh_low:
        return {"status":"LEFT_CENSORED_AT_FIRST_SPRING_OBSERVATION"}
    t20=next((d for d,lat in s if lat>=thresh_low),None)
    t80=next((d for d,lat in s if lat>=thresh_high),None)
    if t20 is None or t80 is None or t80<=t20:
        return {"status":"BOTH_CHECKPOINTS_NOT_OBSERVABLE"}
    return {
        "status":"TWO_NORTHWARD_CHECKPOINTS",
        "first20_doy":t20.timetuple().tm_yday,
        "first80_doy":t80.timetuple().tm_yday,
        "interval_days":(t80-t20).days,
        "net_northing_deg":end-begin,
        "latitudinal_observed_span_deg":span,
    }


def origin_source(system,tmpfile):
    if system=="stork":
        from scripts.qc_public_movebank_stork_gps_join_2018 import download_gps
        from scripts.qc_public_movebank_stork_breeding_2018 import DOI
        data=download_gps(tmpfile)
        return DOI,"Ciconia ciconia","GPS",data
    record=(SOURCES[system] if system in SOURCES else V2[system])
    return (record["doi"],record["taxon"],
            record.get("original_sensor","GPS"),download_verified(record,tmpfile))


def read_daily(path,expected_taxon):
    daylat=defaultdict(float)
    dayn=Counter()
    errors=Counter()
    taxa=Counter()
    with Path(path).open(newline="",encoding="utf-8-sig",errors="replace") as f:
        rd=csv.DictReader(f)
        cols=rd.fieldnames or []
        necessary={"timestamp","location-lat","location-long"}
        if not necessary.issubset(cols):
            raise ValueError("source lacks timestamp or WGS84 location")
        identity=next((x for x in ("individual-local-identifier",
                                  "deployment-id","tag-local-identifier")
                       if x in cols),None)
        if identity is None:raise ValueError("no source identity column")
        for row in rd:
            try:
                dt=datetime.fromisoformat((row.get("timestamp") or "").strip().replace("Z","+00:00"))
                lat=float(row.get("location-lat") or "")
                lon=float(row.get("location-long") or "")
                if not(math.isfinite(lat) and math.isfinite(lon) and
                       -90<=lat<=90 and -180<=lon<=180):
                    raise ValueError("invalid coordinates")
            except (TypeError,ValueError):
                errors["invalid_time_or_location"]+=1
                continue
            ident=(row.get(identity) or "").strip()
            if not ident:
                errors["empty_identity"]+=1
                continue
            if dt.month not in MONTHS:
                errors["valid_outside_spring_months"]+=1
                continue
            tax=(row.get("individual-taxon-canonical-name") or "").strip()
            if not tax:tax=expected_taxon
            taxa[tax]+=1
            key=(tax,ident,dt.year,dt.date())
            daylat[key]+=lat
            dayn[key]+=1
            errors["spring_geo_fixes"]+=1
    groups=defaultdict(list)
    for (tax,ident,year,day),lat_total in daylat.items():
        groups[(tax,ident,year)].append((day,lat_total/dayn[(tax,ident,year,day)]))
    return groups,errors,taxa,identity


def _quantiles(values):
    if not values:return None
    return {"min":min(values),"q25":quantile(values,.25),
            "median":statistics.median(values),
            "q75":quantile(values,.75),"max":max(values)}


def summarize(groups,errors,taxa,identity):
    statuses=Counter()
    by_tax=defaultdict(Counter)
    successful=[]
    for (tax,ident,year),rows in groups.items():
        r=analyze_one(rows)
        statuses[r["status"]]+=1
        by_tax[tax][r["status"]]+=1
        if r["status"]=="TWO_NORTHWARD_CHECKPOINTS":
            successful.append(r)
    return {
        "source_identity_field":identity,
        "source_taxon_name_fix_counts":dict(sorted(taxa.items())),
        "total_unique_taxon_identity_calendar_years_with_spring_fixes":len(groups),
        "all_status_counts":dict(sorted(statuses.items())),
        "status_counts_by_publisher_taxon":{
            k:dict(sorted(v.items())) for k,v in sorted(by_tax.items())},
        "complete_two_checkpoint_identity_years":len(successful),
        "first20_doy_quartiles":_quantiles([v["first20_doy"] for v in successful]),
        "first80_doy_quartiles":_quantiles([v["first80_doy"] for v in successful]),
        "interval_20_to_80_days_quartiles":_quantiles([v["interval_days"] for v in successful]),
        "latitudinal_span_degrees_quartiles":_quantiles([v["latitudinal_observed_span_deg"] for v in successful]),
        "source_qc_counts":dict(sorted(errors.items())),
        "fixed_observation_gate":{
            "months":"Feb-May","min_daily_dates":MIN_UNIQUE_SPRING_DAYS,
            "lat_10to90_degree_min":MIN_LAT_RANGE,
            "early5_vs_late5_day_median_lat_increase_min":MIN_EARLY_LATE_NORTHING,
            "relative_latitude_crossings":list(CROSSING_FRACTIONS)},
        "spatial_route_causality_proven":False,
        "true_migration_start_or_breeding_arrival_proven":False,
        "cue_or_actionability_measured":False,
        "fitness_estimated":False,
        "gps_argos_cohort_independence_verified":False,
        "raw_ids_or_locations_exported":False,
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--system",choices=sorted(SYSTEMS),required=True)
    ap.add_argument("--out",type=Path,
                   default=Path("outputs/payoff_b_crossguild_northward"))
    args=ap.parse_args()
    result={"source_system":args.system,"status":"NOT_OPENED",
            "analysis_class":"OUTCOME_BLIND_SOURCE_GEOMETRY",
            "hypothesis_testing":"NOT_RUN"}
    try:
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"original_source.csv"
            doi,taxon,sensor,source=origin_source(args.system,p)
            result.update(source_doi=doi,publisher_taxa=taxon,source_sensor=sensor,
                          source_integrity=source)
            groups,errors,taxa,identity=read_daily(p,taxon)
            result["geometry_admission"]=summarize(groups,errors,taxa,identity)
            result["status"]="SPRING_SOURCE_GEOMETRY_QC_COMPLETE"
    except (OSError,ValueError,TypeError) as e:
        result["status"]="SOURCE_GEOMETRY_GATE_FAILED"
        result["error"]=type(e).__name__+": "+str(e)[:350]
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/(args.system+".json")).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    if result["status"]!="SPRING_SOURCE_GEOMETRY_QC_COMPLETE":
        raise SystemExit("source geometry QC failed")

if __name__=="__main__":main()
