#!/usr/bin/env python3
"""Post-freeze mule-deer H2 proxy-moderation audit.

Frozen contract:
data/payoff_b_mule_deer_h2_proxy_contract_20261003.json

This asks whether a predeparture physiological-condition proxy (March scaled
IFBFat) moderates the signed phase-to-actuator association. It is explicitly a
proxy moderation test, not direct identification of the readiness gate G and
not an H2 confirmation by itself.
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
    DEFAULT_URL, NS, cell_value, col_index, shared_strings, workbook_sheet_paths
)

EXPECTED_SHA256="2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364"
READINESS_SHEET="SFig1"
PHASE_SHEET="Fig1a,b;Fig3;SFig2;STables1,6"
ACTUATOR_SHEET="Fig4d,4e;SFig4"


def download(url):
    req=urllib.request.Request(url,headers={
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130 Safari/537.36",
        "Accept":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream,*/*",
    })
    with urllib.request.urlopen(req,timeout=60) as res:
        return res.read()


def sheet_rows(zf,path,strings,max_cols=100):
    root=ET.fromstring(zf.read(path))
    out=[]
    for row in root.findall("main:sheetData/main:row",NS):
        vals={}
        for cell in row.findall("main:c",NS):
            idx=col_index(cell.attrib.get("r",""))
            if idx>=max_cols:
                continue
            vals[idx]=cell_value(cell,strings)
        if not vals:
            out.append([])
            continue
        width=min(max(vals)+1,max_cols)
        arr=[""]*width
        for i,v in vals.items():
            if i<width: arr[i]=v
        out.append(arr)
    return out


def norm(x): return str(x).strip()


def parse_float(x):
    s=norm(x)
    if s=="" or s.upper() in {"NA","NAN","NULL"}:
        return None
    try: v=float(s)
    except ValueError: return None
    return v if math.isfinite(v) else None


def find_table(rows,required):
    for i,row in enumerate(rows):
        h=[norm(x) for x in row]
        if required.issubset(set(h)):
            data=[]
            for rr in rows[i+1:]:
                if not rr or all(norm(x)=="" for x in rr):
                    if data: break
                    continue
                if required.issubset(set(norm(x) for x in rr)):
                    break
                data.append(rr)
            return h,data
    raise ValueError(f"required header not found: {sorted(required)}")


def records(header,rows):
    out=[]
    for row in rows:
        d={h:(row[i] if i<len(row) else "") for i,h in enumerate(header) if h}
        if any(norm(v) for v in d.values()): out.append(d)
    return out


def is_leap(y):
    return y%4==0 and (y%100!=0 or y%400==0)


def march31_doy(y):
    return 91 if is_leap(y) else 90


def animal(idyr):
    return idyr.rsplit("_",1)[0]


def mean(xs):
    return sum(xs)/len(xs)


def solve_linear(a,b):
    n=len(b)
    m=[list(map(float,a[i]))+[float(b[i])] for i in range(n)]
    for col in range(n):
        pivot=max(range(col,n),key=lambda r:abs(m[r][col]))
        if abs(m[pivot][col])<1e-12:
            raise ValueError("singular design")
        m[col],m[pivot]=m[pivot],m[col]
        pv=m[col][col]
        m[col]=[x/pv for x in m[col]]
        for r in range(n):
            if r==col: continue
            f=m[r][col]
            if f==0: continue
            m[r]=[x-f*y for x,y in zip(m[r],m[col])]
    return [m[i][-1] for i in range(n)]


def ols_design(rows,response,within_year=False):
    rr=[r for r in rows if r.get(response) is not None]
    if len(rr)<6:
        raise ValueError("interaction OLS requires n>=6")

    if within_year:
        by=defaultdict(list)
        for i,r in enumerate(rr):
            by[r["year"]].append(i)
        phase=[0.0]*len(rr); fat=[0.0]*len(rr); y=[0.0]*len(rr)
        for indices in by.values():
            mp=mean([rr[i]["dfp"] for i in indices])
            mf=mean([rr[i]["fat"] for i in indices])
            my=mean([rr[i][response] for i in indices])
            for i in indices:
                phase[i]=rr[i]["dfp"]-mp
                fat[i]=rr[i]["fat"]-mf
                y[i]=rr[i][response]-my
    else:
        mp=mean([r["dfp"] for r in rr])
        mf=mean([r["fat"] for r in rr])
        phase=[r["dfp"]-mp for r in rr]
        fat=[r["fat"]-mf for r in rr]
        y=[r[response] for r in rr]

    inter=[p*f for p,f in zip(phase,fat)]
    X=[[1.0,p,f,z] for p,f,z in zip(phase,fat,inter)]
    pcols=4
    xtx=[[sum(row[i]*row[j] for row in X) for j in range(pcols)] for i in range(pcols)]
    xty=[sum(row[i]*yy for row,yy in zip(X,y)) for i in range(pcols)]
    beta=solve_linear(xtx,xty)
    return {
        "n":len(rr),
        "intercept":beta[0],
        "beta_DFP_Start":beta[1],
        "beta_scaledIFBFat":beta[2],
        "beta_DFP_x_IFBFat":beta[3],
    }


def percentile(xs,p):
    s=sorted(xs)
    if not s: raise ValueError("empty percentile")
    q=(len(s)-1)*p
    lo=int(math.floor(q)); hi=int(math.ceil(q))
    if lo==hi: return s[lo]
    f=q-lo
    return s[lo]*(1-f)+s[hi]*f


def ci95(xs):
    return [percentile(xs,0.025),percentile(xs,0.975)]


def bootstrap(rows,response,reps,seed):
    usable=[r for r in rows if r.get(response) is not None]
    by=defaultdict(list)
    for r in usable: by[r["animal"]].append(r)
    ids=sorted(by)
    rng=random.Random(seed)
    raw=[]; yfe=[]
    for _ in range(reps):
        sampled=[rng.choice(ids) for _ in ids]
        rr=[]
        for a in sampled: rr.extend(by[a])
        try:
            raw.append(ols_design(rr,response,False)["beta_DFP_x_IFBFat"])
            yfe.append(ols_design(rr,response,True)["beta_DFP_x_IFBFat"])
        except (ValueError,ZeroDivisionError):
            continue
    return {
        "cluster_unit":"animal",
        "unique_animals":len(ids),
        "replicates_requested":reps,
        "replicates_completed":len(raw),
        "raw_interaction_ci95":ci95(raw),
        "year_centered_interaction_ci95":ci95(yfe),
    }


def loo(rows,response):
    ids=sorted({r["animal"] for r in rows if r.get(response) is not None})
    vals=[]
    for a in ids:
        rr=[r for r in rows if r["animal"]!=a and r.get(response) is not None]
        try: vals.append(ols_design(rr,response,False)["beta_DFP_x_IFBFat"])
        except (ValueError,ZeroDivisionError): pass
    return {"n_fits":len(vals),"interaction_range":[min(vals),max(vals)]}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--url",default=DEFAULT_URL)
    ap.add_argument("--bootstrap-replicates",type=int,default=10000)
    ap.add_argument("--seed",type=int,default=20261003)
    ap.add_argument("--output",type=Path,default=Path("outputs/payoff_b_mule_deer_h2_proxy_result.json"))
    args=ap.parse_args()

    raw=download(args.url)
    sha=hashlib.sha256(raw).hexdigest()
    if sha!=EXPECTED_SHA256:
        raise SystemExit(f"source SHA mismatch: {sha}")

    with zipfile.ZipFile(BytesIO(raw)) as zf:
        strings=shared_strings(zf)
        paths=dict(workbook_sheet_paths(zf))
        rh,rd=find_table(sheet_rows(zf,paths[READINESS_SHEET],strings),{"id_yr","scaledIFBFat"})
        ph,pd=find_table(sheet_rows(zf,paths[PHASE_SHEET],strings),{"id_yr","year","DOY_Start","DFP_Start"})
        actuator_matrix=sheet_rows(zf,paths[ACTUATOR_SHEET],strings)

    ready=records(rh,rd); phase=records(ph,pd)

    actuator_header=[norm(x) for x in actuator_matrix[1][:7]]
    actuator_idx={name:i for i,name in enumerate(actuator_header)}
    act=[]
    for row in actuator_matrix[2:]:
        if not row: continue
        def get_a(name):
            i=actuator_idx[name]
            return row[i] if i<len(row) else ""
        idyr=norm(get_a("id_yr"))
        if not idyr: continue
        act.append({
            "id_yr":idyr,
            "rate":parse_float(get_a("rate.km.day")),
            "stopover":parse_float(get_a("stopover.day")),
        })

    fatmap={}
    for row in ready:
        i=norm(row.get("id_yr","")); fat=parse_float(row.get("scaledIFBFat",""))
        if i and fat is not None: fatmap[i]=fat

    phmap={}
    for row in phase:
        i=norm(row.get("id_yr","")); yf=parse_float(row.get("year",""))
        start=parse_float(row.get("DOY_Start","")); dfp=parse_float(row.get("DFP_Start",""))
        if i and yf is not None and start is not None and dfp is not None:
            phmap[i]={"year":int(round(yf)),"start":start,"dfp":dfp}

    amap={r["id_yr"]:{"rate":r["rate"],"stopover":r["stopover"]} for r in act}

    joined=[]
    for i,fat in fatmap.items():
        if i not in phmap or i not in amap: continue
        p=phmap[i]
        if p["start"]<=march31_doy(p["year"]): continue
        joined.append({
            "id_yr":i,"animal":animal(i),"year":p["year"],
            "raw_start":p["start"],"dfp":p["dfp"],"fat":fat,
            **amap[i],
        })

    if len(act)!=152:
        raise SystemExit(f"expected 152 actuator rows, got {len(act)}")
    if len(joined)!=62:
        raise SystemExit(f"expected 62 safe joined rows, got {len(joined)}")

    result={
        "date":"2026-10-03",
        "status":"POSTFREEZE_MULE_DEER_H2_PROXY_MODERATION_RESULT",
        "frozen_submission_affected":False,
        "source_sha256":sha,
        "safe_joined_rows":len(joined),
        "safe_animals":len({r["animal"] for r in joined}),
        "movement_rate":{
            "raw":ols_design(joined,"rate",False),
            "year_centered":ols_design(joined,"rate",True),
            "bootstrap":bootstrap(joined,"rate",args.bootstrap_replicates,args.seed),
            "leave_one_animal_out":loo(joined,"rate"),
        },
        "stopover":{
            "raw":ols_design(joined,"stopover",False),
            "year_centered":ols_design(joined,"stopover",True),
            "bootstrap":bootstrap(joined,"stopover",args.bootstrap_replicates,args.seed+1),
            "leave_one_animal_out":loo(joined,"stopover"),
        },
        "decision_rule":{
            "strong_proxy_support":"both interactions have predicted sign and 95% cluster intervals exclude zero",
            "mixed_proxy_support":"exactly one passes",
            "no_proxy_support":"neither passes",
            "H2_status":"not promoted to established H2 from observational proxy moderation alone",
        },
        "boundaries":[
            "IFBFat is a readiness proxy, not direct G",
            "moderation can reflect energetic capacity or other state dependence",
            "all downstream actuator observations occur after migration onset",
            "frozen GEB V2 unchanged",
        ],
    }

    ri=result["movement_rate"]["bootstrap"]["raw_interaction_ci95"]
    si=result["stopover"]["bootstrap"]["raw_interaction_ci95"]
    rate_pass=(result["movement_rate"]["raw"]["beta_DFP_x_IFBFat"]>0 and ri[0]>0)
    stop_pass=(result["stopover"]["raw"]["beta_DFP_x_IFBFat"]<0 and si[1]<0)
    n_pass=int(rate_pass)+int(stop_pass)
    if n_pass==2: label="STRONG_PROXY_SUPPORT"
    elif n_pass==1: label="MIXED_PROXY_SUPPORT"
    else: label="NO_PROXY_SUPPORT"
    result["decision_rule"]["rate_pass"]=rate_pass
    result["decision_rule"]["stopover_pass"]=stop_pass
    result["decision_rule"]["outcome"]=label

    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
