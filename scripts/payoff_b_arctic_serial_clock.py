#!/usr/bin/env python3
"""Cross-taxon Arctic serial-clock audit.

Frozen contract:
data/payoff_b_arctic_serial_clock_contract_20261003.json

The analysis uses Dryad 2.migration_data.csv from:
doi:10.5061/dryad.w0vt4b93d

Primary question:
Within population-year groups, how much individual departure timing difference
is retained by arrival at the Arctic Circle?

This is an independent post-theory natural test of the serial timing-retention
coordinate. It does not identify a physiological readiness clock or primitive
controller parameters.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import random
import urllib.request
from collections import defaultdict
from pathlib import Path


DEFAULT_URL="https://datadryad.org/downloads/file_stream/4015617"

EXPECTED_COLUMNS={
    "species","individual_id","site","year","depart","AC","arrival",
    "nest.initiation","travel_speed","stopovers.f","species_site",
    "species_site_year"
}


def download(url: str) -> bytes:
    req=urllib.request.Request(
        url,
        headers={"User-Agent":"Mozilla/5.0","Accept":"text/csv,text/plain,*/*"},
    )
    with urllib.request.urlopen(req,timeout=60) as res:
        return res.read()


def parse_float(x):
    s=str(x).strip()
    if s=="" or s.upper() in {"NA","NAN","NULL"}:
        return None
    try:
        v=float(s)
    except ValueError:
        return None
    return v if math.isfinite(v) else None


def sample_var(xs):
    if len(xs)<2:
        raise ValueError("variance requires n>=2")
    m=sum(xs)/len(xs)
    return sum((x-m)**2 for x in xs)/(len(xs)-1)


def sample_cov(xs,ys):
    if len(xs)!=len(ys) or len(xs)<2:
        raise ValueError("covariance requires equal n>=2")
    mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/(len(xs)-1)


def slope(xs,ys):
    return sample_cov(xs,ys)/sample_var(xs)


def pearson(xs,ys):
    return sample_cov(xs,ys)/math.sqrt(sample_var(xs)*sample_var(ys))


def percentile(xs,p):
    s=sorted(xs)
    if not s:
        raise ValueError("empty percentile")
    if len(s)==1:
        return s[0]
    q=(len(s)-1)*p
    lo=int(math.floor(q)); hi=int(math.ceil(q))
    if lo==hi:
        return s[lo]
    f=q-lo
    return s[lo]*(1-f)+s[hi]*f


def ci95(xs):
    return [percentile(xs,0.025),percentile(xs,0.975)]


def prepare_rows(raw: bytes):
    text=raw.decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(text))
    header=set(reader.fieldnames or [])
    missing=EXPECTED_COLUMNS-header
    if missing:
        raise SystemExit(f"missing expected columns: {sorted(missing)}")

    rows=[]
    for r in reader:
        year=parse_float(r.get("year"))
        if year is None:
            continue
        species_site=str(r.get("species_site","")).strip()
        species_site_year=str(r.get("species_site_year","")).strip()
        individual=str(r.get("individual_id","")).strip()
        species=str(r.get("species","")).strip()
        if not species_site or not species_site_year or not individual:
            continue
        rows.append({
            "species":species,
            "individual":individual,
            "population":species_site,
            "population_year":species_site_year,
            "year":int(round(year)),
            "depart":parse_float(r.get("depart")),
            "AC":parse_float(r.get("AC")),
            "arrival":parse_float(r.get("arrival")),
            "nest":parse_float(r.get("nest.initiation")),
            "travel_speed":parse_float(r.get("travel_speed")),
            "stopovers_f":parse_float(r.get("stopovers.f")),
        })
    return rows, sorted(header)


def eligible_group_keys(rows,x,y,min_n=3):
    groups=defaultdict(list)
    for r in rows:
        if r[x] is not None and r[y] is not None:
            groups[r["population_year"]].append(r)
    return {
        k for k,v in groups.items()
        if len(v)>=min_n and sample_var([r[x] for r in v])>0
    }


def centered_pairs(rows,x,y,eligible=None):
    groups=defaultdict(list)
    for r in rows:
        if r[x] is None or r[y] is None:
            continue
        key=r["population_year"]
        if eligible is not None and key not in eligible:
            continue
        groups[key].append(r)

    xs=[]; ys=[]; kept=[]
    for key,rr in groups.items():
        if len(rr)<3:
            continue
        xv=[r[x] for r in rr]
        yv=[r[y] for r in rr]
        if sample_var(xv)<=0:
            continue
        mx=sum(xv)/len(xv); my=sum(yv)/len(yv)
        for r in rr:
            xs.append(r[x]-mx)
            ys.append(r[y]-my)
            kept.append(r)
    return xs,ys,kept


def transition_metrics(rows,x,y,eligible=None):
    xs,ys,kept=centered_pairs(rows,x,y,eligible)
    if len(xs)<3 or sample_var(xs)<=0 or sample_var(ys)<=0:
        raise ValueError("insufficient transition variation")
    return {
        "n":len(xs),
        "individuals":len({r["individual"] for r in kept}),
        "populations":len({r["population"] for r in kept}),
        "population_year_groups":len({r["population_year"] for r in kept}),
        "lambda":slope(xs,ys),
        "r":pearson(xs,ys),
        "variance_x":sample_var(xs),
        "variance_y":sample_var(ys),
        "variance_ratio":sample_var(ys)/sample_var(xs),
        "sd_ratio":math.sqrt(sample_var(ys)/sample_var(xs)),
    }


def actuator_metrics(rows,eligible_depart_ac):
    # Use the same primary groups and departure centering.
    groups=defaultdict(list)
    for r in rows:
        if r["population_year"] in eligible_depart_ac and r["depart"] is not None:
            groups[r["population_year"]].append(r)

    dep=[]; speed=[]; stop=[]
    for key,rr in groups.items():
        dv=[r["depart"] for r in rr if r["depart"] is not None]
        if len(dv)<3:
            continue
        md=sum(dv)/len(dv)
        for r in rr:
            if r["depart"] is None:
                continue
            d=r["depart"]-md
            if r["travel_speed"] is not None:
                dep.append(d); speed.append(r["travel_speed"])
            if r["stopovers_f"] is not None:
                stop.append((d,r["stopovers_f"]))

    out={}
    if len(dep)>=3 and sample_var(dep)>0 and sample_var(speed)>0:
        out["travel_speed"]={
            "n":len(dep),
            "slope_per_late_departure_day":slope(dep,speed),
            "r":pearson(dep,speed),
        }
    if len(stop)>=3:
        dx=[x for x,_ in stop]; sy=[y for _,y in stop]
        if sample_var(dx)>0 and sample_var(sy)>0:
            out["stopovers_fraction"]={
                "n":len(stop),
                "slope_per_late_departure_day":slope(dx,sy),
                "r":pearson(dx,sy),
            }
    return out


def population_lambdas(rows,min_n=20,min_years=3):
    by=defaultdict(list)
    for r in rows:
        if r["depart"] is not None and r["AC"] is not None:
            by[r["population"]].append(r)

    out=[]
    for pop,rr in sorted(by.items()):
        years={r["year"] for r in rr}
        if len(rr)<min_n or len(years)<min_years:
            continue
        eligible=eligible_group_keys(rr,"depart","AC",3)
        try:
            m=transition_metrics(rr,"depart","AC",eligible)
        except ValueError:
            continue
        out.append({
            "population":pop,
            "species":rr[0]["species"],
            "years":len(years),
            **m,
        })
    return out


def cluster_bootstrap(rows,reps,seed,eligible_primary):
    by=defaultdict(list)
    for r in rows:
        by[r["individual"]].append(r)
    ids=sorted(by)
    rng=random.Random(seed)
    lam=[]; vr=[]; speed=[]; stop=[]
    completed=0

    for _ in range(reps):
        sampled=[rng.choice(ids) for _ in ids]
        rr=[]
        for draw_i,ind in enumerate(sampled):
            # Duplicate whole histories; synthetic cluster label is irrelevant
            # to point estimands, but preserves all rows from the drawn bird.
            rr.extend(by[ind])
        try:
            m=transition_metrics(rr,"depart","AC",eligible_primary)
        except (ValueError,ZeroDivisionError):
            continue
        lam.append(m["lambda"]); vr.append(m["variance_ratio"])
        am=actuator_metrics(rr,eligible_primary)
        if "travel_speed" in am:
            speed.append(am["travel_speed"]["slope_per_late_departure_day"])
        if "stopovers_fraction" in am:
            stop.append(am["stopovers_fraction"]["slope_per_late_departure_day"])
        completed+=1

    return {
        "cluster_unit":"individual_id",
        "unique_individuals":len(ids),
        "replicates_requested":reps,
        "replicates_completed":completed,
        "lambda_depart_AC_ci95":ci95(lam),
        "variance_ratio_depart_AC_ci95":ci95(vr),
        "travel_speed_slope_ci95":ci95(speed) if speed else None,
        "stopovers_fraction_slope_ci95":ci95(stop) if stop else None,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--url",default=DEFAULT_URL)
    ap.add_argument("--bootstrap-replicates",type=int,default=10000)
    ap.add_argument("--seed",type=int,default=20261003)
    ap.add_argument("--output",type=Path,default=Path("outputs/payoff_b_arctic_serial_clock_result.json"))
    args=ap.parse_args()

    raw=download(args.url)
    sha=hashlib.sha256(raw).hexdigest()
    rows,header=prepare_rows(raw)

    eligible=eligible_group_keys(rows,"depart","AC",3)
    primary=transition_metrics(rows,"depart","AC",eligible)
    variance_pass=primary["variance_ratio"]<1
    bootstrap=cluster_bootstrap(
        rows,args.bootstrap_replicates,args.seed,eligible
    )

    secondary={}
    for name,x,y in [
        ("AC_to_arrival","AC","arrival"),
        ("arrival_to_nest","arrival","nest"),
        ("depart_to_arrival","depart","arrival"),
    ]:
        elig=eligible_group_keys(rows,x,y,3)
        try:
            secondary[name]=transition_metrics(rows,x,y,elig)
        except ValueError:
            secondary[name]={"status":"INSUFFICIENT"}

    actuators=actuator_metrics(rows,eligible)
    populations=population_lambdas(rows)

    ci=bootstrap["lambda_depart_AC_ci95"]
    primary_pass=(ci[0]>-1 and ci[1]<1)

    result={
        "date":"2026-10-03",
        "status":"POSTFREEZE_ARCTIC_SERIAL_CLOCK_CROSS_TAXON_RESULT",
        "frozen_submission_affected":False,
        "source":{
            "dryad_doi":"10.5061/dryad.w0vt4b93d",
            "migration_file":"2.migration_data.csv",
            "download_url":args.url,
            "sha256":sha,
            "rows_parsed":len(rows),
            "columns":header,
        },
        "primary":{
            "transition":"depart_to_AC",
            **primary,
            "frozen_prediction":"abs(lambda)<1",
            "pass":primary_pass,
        },
        "primary_bootstrap":bootstrap,
        "variance_funnel":{
            "ratio":primary["variance_ratio"],
            "pass_point_estimate":variance_pass,
            "ci95":bootstrap["variance_ratio_depart_AC_ci95"],
            "pass_interval":bootstrap["variance_ratio_depart_AC_ci95"][1]<1,
        },
        "secondary":secondary,
        "actuator_diagnostics":actuators,
        "population_specific":populations,
        "boundaries":[
            "departure date is an entry-timing coordinate, not a physiological readiness measure",
            "within-population-year centering removes shared year/population shifts but does not identify the ecological target itself",
            "travel speed is partly mechanically coupled to departure-arrival duration and is supportive rather than independent",
            "population-specific lambda values are descriptive and not ranked as biological correction strength",
            "primitive G/O/K/g/phi are not identified",
            "frozen GEB V2 and earlier preregistered outcomes are unchanged",
        ],
    }

    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
