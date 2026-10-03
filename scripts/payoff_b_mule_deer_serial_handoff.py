#!/usr/bin/env python3
"""Post-freeze mule-deer serial handoff audit.

Frozen contract:
data/payoff_b_mule_deer_serial_handoff_contract_20261003.json

Tests an observational Markov-style handoff:
predeparture physiological condition -> entry phase -> downstream phase.

This is not a causal mediation analysis and does not identify the primitive
clock parameters.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import urllib.request
import zipfile
from collections import defaultdict
from io import BytesIO
from pathlib import Path

from payoff_b_ortega_source_data_probe import DEFAULT_URL, shared_strings, workbook_sheet_paths
from payoff_b_mule_deer_readiness_source_data import (
    EXPECTED_SHA256,
    READINESS_SHEET,
    PHASE_SHEET,
    sheet_rows,
    find_table,
    records,
    norm,
    parse_float,
    march31_doy,
    animal_from_idyr,
    mean,
    sample_var,
    slope,
    percentile,
)


def download(url: str) -> bytes:
    req=urllib.request.Request(
        url,
        headers={
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130 Safari/537.36",
            "Accept":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream,*/*",
        },
    )
    with urllib.request.urlopen(req,timeout=60) as res:
        return res.read()


def ci95(xs):
    return [percentile(xs,0.025),percentile(xs,0.975)]


def multiple_ols(x1,x2,y):
    if not (len(x1)==len(x2)==len(y)) or len(y)<4:
        raise ValueError("multiple OLS needs equal n>=4")
    mx1,mx2,my=mean(x1),mean(x2),mean(y)
    a=[x-mx1 for x in x1]
    b=[x-mx2 for x in x2]
    c=[x-my for x in y]
    s11=sum(v*v for v in a)
    s22=sum(v*v for v in b)
    s12=sum(u*v for u,v in zip(a,b))
    sy1=sum(u*v for u,v in zip(a,c))
    sy2=sum(u*v for u,v in zip(b,c))
    det=s11*s22-s12*s12
    if abs(det)<1e-12:
        raise ValueError("singular predictors")
    beta1=(sy1*s22-sy2*s12)/det
    beta2=(sy2*s11-sy1*s12)/det
    intercept=my-beta1*mx1-beta2*mx2
    return {
        "intercept":intercept,
        "beta_DFP_Start":beta1,
        "beta_scaledIFBFat":beta2,
    }


def residualize_by_year(rows,field):
    by=defaultdict(list)
    for r in rows:
        by[r["year"]].append(r[field])
    ym={y:mean(v) for y,v in by.items()}
    return [r[field]-ym[r["year"]] for r in rows]


def fit(rows):
    x=[r["dfp_start"] for r in rows]
    f=[r["fat"] for r in rows]
    y=[r["dfp_end"] for r in rows]
    raw=multiple_ols(x,f,y)

    xr=residualize_by_year(rows,"dfp_start")
    fr=residualize_by_year(rows,"fat")
    yr=residualize_by_year(rows,"dfp_end")
    year_fe=multiple_ols(xr,fr,yr)

    total=slope(f,y)
    total_start=slope(x,y)
    return {
        "n":len(rows),
        "animals":len({r["animal"] for r in rows}),
        "raw":raw,
        "year_fe":year_fe,
        "total_IFBFat_to_DFP_End":total,
        "total_DFP_Start_to_DFP_End":total_start,
    }


def bootstrap(rows,reps,seed):
    by=defaultdict(list)
    for r in rows:
        by[r["animal"]].append(r)
    ids=sorted(by)
    rng=random.Random(seed)
    bx=[]; bf=[]; yx=[]; yf=[]; totalf=[]
    completed=0
    for _ in range(reps):
        sampled=[rng.choice(ids) for _ in ids]
        rr=[]
        for a in sampled:
            rr.extend(by[a])
        try:
            m=fit(rr)
        except (ValueError,ZeroDivisionError):
            continue
        bx.append(m["raw"]["beta_DFP_Start"])
        bf.append(m["raw"]["beta_scaledIFBFat"])
        yx.append(m["year_fe"]["beta_DFP_Start"])
        yf.append(m["year_fe"]["beta_scaledIFBFat"])
        totalf.append(m["total_IFBFat_to_DFP_End"])
        completed+=1
    return {
        "cluster_unit":"animal",
        "unique_animals":len(ids),
        "replicates_requested":reps,
        "replicates_completed":completed,
        "raw_DFP_Start_ci95":ci95(bx),
        "raw_scaledIFBFat_ci95":ci95(bf),
        "year_fe_DFP_Start_ci95":ci95(yx),
        "year_fe_scaledIFBFat_ci95":ci95(yf),
        "total_IFBFat_to_DFP_End_ci95":ci95(totalf),
    }


def loo(rows):
    ids=sorted({r["animal"] for r in rows})
    bx=[]; bf=[]
    for a in ids:
        rr=[r for r in rows if r["animal"]!=a]
        try:
            m=fit(rr)["raw"]
        except (ValueError,ZeroDivisionError):
            continue
        bx.append(m["beta_DFP_Start"])
        bf.append(m["beta_scaledIFBFat"])
    return {
        "n_fits":len(bx),
        "DFP_Start_range":[min(bx),max(bx)],
        "scaledIFBFat_range":[min(bf),max(bf)],
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--url",default=DEFAULT_URL)
    ap.add_argument("--bootstrap-replicates",type=int,default=10000)
    ap.add_argument("--seed",type=int,default=20261003)
    ap.add_argument("--output",type=Path,default=Path("outputs/payoff_b_mule_deer_serial_handoff_result.json"))
    args=ap.parse_args()

    raw=download(args.url)
    sha=hashlib.sha256(raw).hexdigest()
    if sha!=EXPECTED_SHA256:
        raise SystemExit(f"source SHA mismatch: {sha}")

    with zipfile.ZipFile(BytesIO(raw)) as zf:
        strings=shared_strings(zf)
        paths=dict(workbook_sheet_paths(zf))
        ready_rows=sheet_rows(zf,paths[READINESS_SHEET],strings)
        phase_rows=sheet_rows(zf,paths[PHASE_SHEET],strings)

    rh,rd=find_table(ready_rows,{"id_yr","scaledIFBFat"})
    ph,pd=find_table(phase_rows,{"id_yr","year","DOY_Start","DFP_Start","DFP_End"})
    ready=records(rh,rd)
    phase=records(ph,pd)

    fatmap={}
    for row in ready:
        i=norm(row.get("id_yr",""))
        fat=parse_float(row.get("scaledIFBFat",""))
        if i and fat is not None:
            fatmap[i]=fat

    joined=[]
    for row in phase:
        i=norm(row.get("id_yr",""))
        yf=parse_float(row.get("year",""))
        raw_start=parse_float(row.get("DOY_Start",""))
        start=parse_float(row.get("DFP_Start",""))
        end=parse_float(row.get("DFP_End",""))
        if not i or i not in fatmap or yf is None or raw_start is None or start is None or end is None:
            continue
        year=int(round(yf))
        if raw_start<=march31_doy(year):
            continue
        joined.append({
            "id_yr":i,
            "animal":animal_from_idyr(i),
            "year":year,
            "raw_start":raw_start,
            "dfp_start":start,
            "dfp_end":end,
            "fat":fatmap[i],
        })

    if len(joined)!=62:
        raise SystemExit(f"expected 62 safe rows, got {len(joined)}")

    f=fit(joined)
    bs=bootstrap(joined,args.bootstrap_replicates,args.seed)
    l=loo(joined)

    def crosses_zero(ci):
        return ci[0] < 0 < ci[1]

    handoff=(
        f["raw"]["beta_DFP_Start"]>0
        and bs["raw_DFP_Start_ci95"][0]>0
        and crosses_zero(bs["raw_scaledIFBFat_ci95"])
    )
    phase_pass=f["raw"]["beta_DFP_Start"]>0 and bs["raw_DFP_Start_ci95"][0]>0
    fat_null=crosses_zero(bs["raw_scaledIFBFat_ci95"])
    if handoff:
        label="HANDOFF_COMPATIBLE"
    elif phase_pass or fat_null:
        label="MIXED"
    else:
        label="NOT_COMPATIBLE"

    result={
        "date":"2026-10-03",
        "status":"POSTFREEZE_MULE_DEER_SERIAL_HANDOFF_RESULT",
        "frozen_submission_affected":False,
        "source_sha256":sha,
        "sample":{"n":len(joined),"animals":len({r["animal"] for r in joined})},
        "fit":f,
        "bootstrap":bs,
        "leave_one_animal_out":l,
        "decision_rule":{
            "phase_pass":phase_pass,
            "fat_conditional_null":fat_null,
            "outcome":label,
        },
        "boundaries":[
            "observational Markov-style handoff signature, not causal mediation",
            "IFBFat is a physiological-condition proxy, not direct readiness gate G",
            "conditioning on DFP_Start can induce bias if unmeasured common causes affect start and end phase",
            "serial theorem was formulated after the H2 proxy result and is not prospectively confirmed by this same dataset",
            "frozen GEB V2 unchanged",
        ],
    }

    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
