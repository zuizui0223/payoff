#!/usr/bin/env python3
"""Source-only matched stay/departure opportunities in published CC0 GPS.

This retrospective screen does not estimate cue use, active correction,
fitness, or a causal effect. No animal identity, date or location is exported.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,statistics,tempfile
from collections import Counter,defaultdict
from datetime import datetime,timedelta,timezone
from pathlib import Path
from scripts.qc_public_movebank_spring_geometry import origin_source
from scripts.qc_payoff_b_predecision_candidates import (
    SYSTEMS,daily_source_positions,detect_transfer_candidates,
    STATIONARY_RADIUS_KM,haversine,vector_mean_lon)

EXPECTED={"stork":145,"white_fronted_goose":106,"curlew":59}
CONTROL_DAYS=(5,21)
RADIUS_KM=30.0
BRACKET_MAX_HOURS=24
SALT="PAYOFF-B-PREWEATHER-MATCH-V1-20261019"

def site(rows):
    anchor=rows[:3]
    return (statistics.median(x[1] for x in anchor),
        vector_mean_lon(sum(math.cos(math.radians(x[2])) for x in anchor),
                        sum(math.sin(math.radians(x[2])) for x in anchor)))

def opportunities(daily):
    p=sorted(daily)
    cases=set(detect_transfer_candidates(p)[1])
    controls=[]
    for i in range(2,len(p)-2):
        a=p[i-2:i+3]
        if any((a[j+1][0]-a[j][0]).days!=1 for j in range(4)):
            continue
        center=site(a)
        if any(haversine(*center,x[1],x[2])>RADIUS_KM for x in a[:3]):
            continue
        if all(haversine(*center,x[1],x[2])<=RADIUS_KM for x in a[3:]):
            controls.append((a[2][0],center))
    return cases,controls

def match_opportunities(groups):
    totals=Counter();selected={}
    for k,daily in sorted(groups.items()):
        cases,controls=opportunities(daily)
        totals["original_case_candidates"]+=len(cases)
        totals["all_prior_stationary_control_opportunities"]+=len(controls)
        if cases:totals["identity_years_with_cases"]+=1
        bydate={x[0]:x for x in daily}
        pairs=[]
        for day in sorted(cases):
            center=site([bydate[day-timedelta(days=j)] for j in (2,1,0)])
            eligible=[r for r in controls if CONTROL_DAYS[0]<=(day-r[0]).days<=CONTROL_DAYS[1]
                      and haversine(*center,*r[1])<=RADIUS_KM]
            if not eligible:
                totals["cases_without_matched_prior_control"]+=1
                continue
            totals["cases_with_matched_prior_control"]+=1
            control=max(eligible,key=lambda r:r[0])
            digest=hashlib.sha256((SALT+"|"+str(k)+"|"+day.isoformat()).encode()).hexdigest()
            pairs.append((digest,day,center,control))
        if pairs:
            _,day,center,control=min(pairs,key=lambda v:v[0])
            selected[k]=(day,center,control[0],control[1])
    totals["distinct_matched_identity_years"]=len(selected)
    return selected,totals

def utc(t):
    dt=datetime.fromisoformat(t.replace("Z","+00:00"))
    return dt.astimezone(timezone.utc).replace(tzinfo=None) if dt.tzinfo else dt

def brackets(gps,selected,source_taxon,return_internal=False):
    """Bracket by last day-3 fix inside 30 km and first day-4 fix outside."""
    indexed={}
    for k,(day,center,control_day,control_site) in selected.items():
        indexed[(k[1],k[2])]=(k,day,center)
    events=defaultdict(lambda:[[],[]])
    with Path(gps).open(encoding="utf-8-sig",newline="",errors="replace") as f:
        rd=csv.DictReader(f)
        names=rd.fieldnames or []
        identcol=next((c for c in ("individual-local-identifier",
                       "deployment-id","tag-local-identifier") if c in names),None)
        if identcol is None:raise ValueError("No event identity")
        for row in rd:
            ident=(row.get(identcol) or "").strip()
            if not ident:continue
            try:
                dt=utc((row.get("timestamp") or "").strip())
                lat=float(row.get("location-lat") or "")
                lon=float(row.get("location-long") or "")
                if not(math.isfinite(lat) and math.isfinite(lon) and
                       -90<=lat<=90 and -180<=lon<=180):continue
            except (ValueError,TypeError,OverflowError):continue
            current=indexed.get((ident,dt.year))
            if current is None:continue
            key,day,center=current
            tax=(row.get("individual-taxon-canonical-name") or "").strip() or source_taxon
            if tax!=key[0]:continue
            if dt.date()==day:events[key][0].append((dt,lat,lon))
            if dt.date()==day+timedelta(days=1):events[key][1].append((dt,lat,lon))
    statuses=Counter();widths=[];internal={}
    for key,(day,center,_,_) in selected.items():
        first,second=events[key]
        if not first or not second:
            statuses["SOURCE_OR_NEXT_FIX_MISSING"]+=1
            internal[key]={"status":"SOURCE_OR_NEXT_FIX_MISSING"}
            continue
        last=max(first)
        if haversine(*center,last[1],last[2])>RADIUS_KM:
            statuses["LAST_SOURCE_FIX_OUTSIDE"]+=1
            internal[key]={"status":"LAST_SOURCE_FIX_OUTSIDE"}
            continue
        out=min((p for p in second if haversine(*center,p[1],p[2])>=RADIUS_KM),
                default=None)
        if out is None:
            statuses["NO_OUTBOUND_NEXT_DAY_FIX"]+=1
            internal[key]={"status":"NO_OUTBOUND_NEXT_DAY_FIX"}
            continue
        hours=(out[0]-last[0]).total_seconds()/3600
        if hours<=0:
            statuses["INVALID_TIME_ORDER"]+=1
            internal[key]={"status":"INVALID_TIME_ORDER"}
        elif hours>BRACKET_MAX_HOURS:
            statuses["BRACKET_OVER_24H"]+=1
            internal[key]={"status":"BRACKET_OVER_24H"}
        else:
            statuses["BRACKET_WITHIN_24H"]+=1
            widths.append(hours)
            internal[key]={"status":"BRACKET_WITHIN_24H","hours":hours}
    return (statuses,widths,internal) if return_internal else (statuses,widths)

def percentile(a,q):
    if not a:return None
    s=sorted(a);v=(len(s)-1)*q;j=int(v)
    return s[j]*(1-v+j)+s[min(j+1,len(s)-1)]*(v-j)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--system",choices=SYSTEMS,required=True)
    p.add_argument("--out",type=Path,default=Path("outputs/payoff_b_stationary_control"))
    a=p.parse_args()
    receipt=dict(source_system=a.system,status="NOT_RUN",source_only=True)
    try:
        with tempfile.TemporaryDirectory() as d:
            gps=Path(d)/"original.csv"
            doi,taxon,sensor,checksum=origin_source(a.system,gps)
            groups,counters,idcol=daily_source_positions(gps,taxon)
            selected,counts=match_opportunities(groups)
            if counts["original_case_candidates"]!=EXPECTED[a.system]:
                raise ValueError("Original frozen case count changed")
            status,width=brackets(gps,selected,taxon)
            receipt.update(
                source_doi=doi,source_checksum=checksum,
                source_counts=dict(sorted(counts.items())),
                bracket_status_counts=dict(sorted(status.items())),
                bracket_hours={"median":percentile(width,.5),
                               "q25":percentile(width,.25),
                               "q75":percentile(width,.75)},
                bracket_6h=sum(w<=6 for w in width),
                bracket_12h=sum(w<=12 for w in width),
                bracket_24h=len(width),
                predecision_weather_control_values="NOT_QUERIED",
                cue_uptake_or_fitness="NOT_TESTED",
                exact_departure_instant_known=False,
                identity_and_location_exported=False,
                status="MATCHED_SOURCE_QC_COMPLETE")
    except (OSError,ValueError,TypeError) as e:
        receipt.update(status="SOURCE_QC_FAILED",
                       error=type(e).__name__+": "+str(e)[:280])
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/(a.system+".json")).write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))
    if receipt["status"]!="MATCHED_SOURCE_QC_COMPLETE":
        raise SystemExit("source-control matching audit failed")

if __name__=="__main__":main()
