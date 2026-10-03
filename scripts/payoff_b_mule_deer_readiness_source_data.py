#!/usr/bin/env python3
"""Post-freeze Ortega mule-deer readiness analysis from verified Source Data.

Frozen contract:
data/payoff_b_mule_deer_readiness_source_data_contract_20261003.json

Question:
Does March nutritional condition (scaled IFBFat), measured before migration in a
strictly temporally safe subset, predict standardized spring-migration start?

This is a post-freeze mechanistic bridge only. It cannot establish a molecular
clock or readiness-gated feedback (H2), and it does not alter frozen GEB V2.
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
from xml.etree import ElementTree as ET

from payoff_b_ortega_source_data_probe import (
    DEFAULT_URL,
    NS,
    cell_value,
    col_index,
    shared_strings,
    workbook_sheet_paths,
)

EXPECTED_SHA256="2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364"
READINESS_SHEET="SFig1"
PHASE_SHEET="Fig1a,b;Fig3;SFig2;STables1,6"


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


def sheet_rows(zf: zipfile.ZipFile,path: str,strings: list[str],max_cols: int=80) -> list[list[str]]:
    root=ET.fromstring(zf.read(path))
    rows=[]
    for row in root.findall("main:sheetData/main:row",NS):
        vals={}
        for cell in row.findall("main:c",NS):
            idx=col_index(cell.attrib.get("r",""))
            if idx>=max_cols:
                continue
            vals[idx]=cell_value(cell,strings)
        if not vals:
            rows.append([])
            continue
        width=min(max(vals)+1,max_cols)
        arr=[""]*width
        for idx,val in vals.items():
            if idx<width:
                arr[idx]=val
        rows.append(arr)
    return rows


def norm(s: str) -> str:
    return str(s).strip()


def parse_float(s: str) -> float | None:
    s=norm(s)
    if s=="" or s.upper() in {"NA","NAN","NULL"}:
        return None
    try:
        x=float(s)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def find_table(rows: list[list[str]], required: set[str]) -> tuple[list[str],list[list[str]]]:
    for i,row in enumerate(rows):
        names=[norm(x) for x in row]
        if required.issubset(set(names)):
            header=names
            data=[]
            for rr in rows[i+1:]:
                if not rr or all(norm(x)=="" for x in rr):
                    if data:
                        break
                    continue
                # stop if a later independent block header begins
                if required.issubset(set(norm(x) for x in rr)):
                    break
                data.append(rr)
            return header,data
    raise ValueError(f"header with required fields not found: {sorted(required)}")


def records(header: list[str],rows: list[list[str]]) -> list[dict[str,str]]:
    out=[]
    for row in rows:
        d={h:(row[i] if i<len(row) else "") for i,h in enumerate(header) if h}
        if any(norm(v) for v in d.values()):
            out.append(d)
    return out


def mean(xs):
    return sum(xs)/len(xs)


def sample_var(xs):
    if len(xs)<2:
        raise ValueError("variance requires n>=2")
    m=mean(xs)
    return sum((x-m)**2 for x in xs)/(len(xs)-1)


def sample_cov(xs,ys):
    if len(xs)!=len(ys) or len(xs)<2:
        raise ValueError("covariance requires equal n>=2")
    mx,my=mean(xs),mean(ys)
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/(len(xs)-1)


def slope(xs,ys):
    return sample_cov(xs,ys)/sample_var(xs)


def pearson(xs,ys):
    return sample_cov(xs,ys)/math.sqrt(sample_var(xs)*sample_var(ys))


def rankdata(xs):
    order=sorted(range(len(xs)),key=lambda i:xs[i])
    ranks=[0.0]*len(xs)
    pos=0
    while pos<len(order):
        end=pos+1
        while end<len(order) and xs[order[end]]==xs[order[pos]]:
            end+=1
        r=(pos+1+end)/2.0
        for j in range(pos,end):
            ranks[order[j]]=r
        pos=end
    return ranks


def spearman(xs,ys):
    return pearson(rankdata(xs),rankdata(ys))


def percentile(xs,p):
    ys=sorted(xs)
    if not ys:
        raise ValueError("empty percentile")
    if len(ys)==1:
        return ys[0]
    q=(len(ys)-1)*p
    lo=int(math.floor(q)); hi=int(math.ceil(q))
    if lo==hi:
        return ys[lo]
    f=q-lo
    return ys[lo]*(1-f)+ys[hi]*f


def ci95(xs):
    return [percentile(xs,0.025),percentile(xs,0.975)]


def is_leap(year: int) -> bool:
    return year%4==0 and (year%100!=0 or year%400==0)


def march31_doy(year: int) -> int:
    return 91 if is_leap(year) else 90


def animal_from_idyr(idyr: str) -> str:
    return idyr.rsplit("_",1)[0]


def residualize_by_year(rows, field):
    by=defaultdict(list)
    for r in rows:
        by[r["year"]].append(r[field])
    means={k:mean(v) for k,v in by.items()}
    return [r[field]-means[r["year"]] for r in rows]


def metrics(rows):
    x=[r["fat"] for r in rows]
    y=[r["std_start"] for r in rows]
    xr=residualize_by_year(rows,"fat")
    yr=residualize_by_year(rows,"std_start")
    return {
        "n":len(rows),
        "animals":len({r["animal"] for r in rows}),
        "years":sorted({r["year"] for r in rows}),
        "fat_min":min(x),
        "fat_max":max(x),
        "start_doy_min":min(r["raw_start"] for r in rows),
        "start_doy_max":max(r["raw_start"] for r in rows),
        "slope_std_start_per_scaledIFBFat":slope(x,y),
        "pearson_r":pearson(x,y),
        "spearman_rho":spearman(x,y),
        "year_fe_slope":slope(xr,yr) if sample_var(xr)>0 else None,
    }


def cluster_bootstrap(rows,reps,seed):
    by=defaultdict(list)
    for r in rows:
        by[r["animal"]].append(r)
    ids=sorted(by)
    rng=random.Random(seed)
    vals=[]
    vals_fe=[]
    vals_rho=[]
    for _ in range(reps):
        sampled=[rng.choice(ids) for _ in ids]
        rr=[]
        for a in sampled:
            rr.extend(by[a])
        try:
            m=metrics(rr)
            vals.append(m["slope_std_start_per_scaledIFBFat"])
            vals_rho.append(m["spearman_rho"])
            if m["year_fe_slope"] is not None:
                vals_fe.append(m["year_fe_slope"])
        except (ValueError,ZeroDivisionError):
            continue
    return {
        "cluster_unit":"animal",
        "unique_animals":len(ids),
        "replicates_requested":reps,
        "replicates_completed":len(vals),
        "slope_ci95":ci95(vals),
        "year_fe_slope_ci95":ci95(vals_fe) if vals_fe else None,
        "spearman_ci95":ci95(vals_rho),
    }


def leave_one_animal_out(rows):
    ids=sorted({r["animal"] for r in rows})
    vals=[]
    for a in ids:
        rr=[r for r in rows if r["animal"]!=a]
        if len(rr)<3:
            continue
        try:
            vals.append(slope([r["fat"] for r in rr],[r["std_start"] for r in rr]))
        except (ValueError,ZeroDivisionError):
            pass
    return {"n_fits":len(vals),"min_slope":min(vals),"max_slope":max(vals)} if vals else None


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--url",default=DEFAULT_URL)
    ap.add_argument("--bootstrap-replicates",type=int,default=10000)
    ap.add_argument("--seed",type=int,default=20261003)
    ap.add_argument("--output",type=Path,default=Path("outputs/payoff_b_mule_deer_readiness_result.json"))
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

    rh,rd=find_table(ready_rows,{"id_yr","standardized_DOY_Start","scaledIFBFat"})
    ph,pd=find_table(phase_rows,{"id_yr","year","DOY_Start"})
    ready=records(rh,rd)
    phase=records(ph,pd)

    phase_map={}
    for row in phase:
        idyr=norm(row.get("id_yr",""))
        yearf=parse_float(row.get("year",""))
        start=parse_float(row.get("DOY_Start",""))
        if idyr and yearf is not None and start is not None:
            phase_map[idyr]={"year":int(round(yearf)),"raw_start":start}

    joined=[]
    for row in ready:
        idyr=norm(row.get("id_yr",""))
        fat=parse_float(row.get("scaledIFBFat",""))
        std=parse_float(row.get("standardized_DOY_Start",""))
        if not idyr or fat is None or std is None or idyr not in phase_map:
            continue
        pr=phase_map[idyr]
        joined.append({
            "id_yr":idyr,
            "animal":animal_from_idyr(idyr),
            "year":pr["year"],
            "raw_start":pr["raw_start"],
            "std_start":std,
            "fat":fat,
            "march31_doy":march31_doy(pr["year"]),
            "temporally_safe":pr["raw_start"]>march31_doy(pr["year"]),
        })

    safe=[r for r in joined if r["temporally_safe"]]
    unsafe=[r for r in joined if not r["temporally_safe"]]

    result={
        "date":"2026-10-03",
        "status":"POSTFREEZE_MULE_DEER_READINESS_SOURCE_DATA_RESULT",
        "frozen_submission_affected":False,
        "source":{
            "article":"Ortega et al. 2023 Nature Communications 14:2008",
            "doi":"10.1038/s41467-023-37750-z",
            "source_data_sha256":sha,
            "readiness_sheet":READINESS_SHEET,
            "phase_sheet":PHASE_SHEET,
        },
        "schema":{
            "readiness_header":rh,
            "phase_header":ph,
            "readiness_rows_with_joinable_fat_and_timing":len(joined),
            "temporally_safe_rows":len(safe),
            "unsafe_or_ambiguous_rows":len(unsafe),
            "unsafe_rows":[
                {k:r[k] for k in ("id_yr","year","raw_start","std_start","fat","march31_doy")}
                for r in unsafe
            ],
        },
        "all_joined_descriptive":metrics(joined) if len(joined)>=3 else None,
        "safe_primary":metrics(safe) if len(safe)>=3 else None,
        "safe_cluster_bootstrap":cluster_bootstrap(
            safe,args.bootstrap_replicates,args.seed
        ) if len(safe)>=3 else None,
        "safe_leave_one_animal_out":leave_one_animal_out(safe) if len(safe)>=3 else None,
        "classification":{
            "minimum_safe_n":20,
            "timer_upgrade_rule":"T3_CANDIDATE only if safe n>=20 and animal-cluster slope CI excludes zero",
            "H1_rule":"H1_CANDIDATE only if timer upgrade passes because D2 signed feedback already exists in this system",
            "H2_rule":"NO; requires separate readiness x signed-phase interaction",
        },
        "boundaries":[
            "scaledIFBFat is nutritional/physiological state, not a molecular clock",
            "safe subset only guarantees March measurement preceded migration start; exact capture day is unknown",
            "association with departure timing does not prove a threshold gate",
            "no H2 readiness-gated feedback inference is licensed",
            "frozen GEB V2 and preregistered outcomes are unchanged",
        ],
    }

    if result["safe_primary"] is not None:
        ci=result["safe_cluster_bootstrap"]["slope_ci95"]
        passes=(
            result["safe_primary"]["n"]>=20
            and (ci[0]>0 or ci[1]<0)
        )
        result["classification"]["timer_upgrade_passes"]=passes
        result["classification"]["licensed_timer_label"]="T3_CANDIDATE" if passes else "T3_UNRESOLVED"
        result["classification"]["licensed_hybrid_label"]="H1_CANDIDATE" if passes else "H0"
    else:
        result["classification"]["timer_upgrade_passes"]=False
        result["classification"]["licensed_timer_label"]="T0"
        result["classification"]["licensed_hybrid_label"]="H0"

    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
