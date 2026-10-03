#!/usr/bin/env python3
"""Post-freeze mule-deer two-clock channel dissociation audit.

Frozen contract:
data/payoff_b_mule_deer_two_clock_channel_contract_20261003.json

Question:
Within the temporally safe March-IFBFat subset, does signed ecological phase
(DFP_Start) predict post-departure speed/stopover after accounting for IFBFat,
while IFBFat itself contributes little to those downstream actuators?

This is a source-data reproduction / mechanism-separation audit, not H2.
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
            if i<width:
                arr[i]=v
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
    raise ValueError(f"required header not found: {required}")


def records(header,rows):
    out=[]
    for row in rows:
        d={h:(row[i] if i<len(row) else "") for i,h in enumerate(header) if h}
        if any(norm(v) for v in d.values()):
            out.append(d)
    return out


def is_leap(y):
    return y%4==0 and (y%100!=0 or y%400==0)


def march31_doy(y):
    return 91 if is_leap(y) else 90


def animal(idyr):
    return idyr.rsplit("_",1)[0]


def mean(xs):
    return sum(xs)/len(xs)


def centered(xs):
    m=mean(xs)
    return [x-m for x in xs]


def multiple_ols(x1,x2,y):
    if not (len(x1)==len(x2)==len(y)) or len(y)<4:
        raise ValueError("multiple OLS needs equal n>=4")
    a=centered(x1); b=centered(x2); c=centered(y)
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
    intercept=mean(y)-beta1*mean(x1)-beta2*mean(x2)
    return {"intercept":intercept,"beta_DFP_Start":beta1,"beta_scaledIFBFat":beta2}


def residualize_year(rows,field):
    by=defaultdict(list)
    for r in rows: by[r["year"]].append(r[field])
    ym={y:mean(v) for y,v in by.items()}
    return [r[field]-ym[r["year"]] for r in rows]


def fit(rows,response):
    rr=[r for r in rows if r.get(response) is not None]
    x1=[r["dfp"] for r in rr]
    x2=[r["fat"] for r in rr]
    y=[r[response] for r in rr]
    raw=multiple_ols(x1,x2,y)
    yr=multiple_ols(
        residualize_year(rr,"dfp"),
        residualize_year(rr,"fat"),
        residualize_year(rr,response),
    )
    return {"n":len(rr),"raw":raw,"year_fe":yr}


def percentile(xs,p):
    s=sorted(xs)
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
    bphase=[]; bfat=[]; yphase=[]; yfat=[]
    completed=0
    for _ in range(reps):
        sampled=[rng.choice(ids) for _ in ids]
        rr=[]
        for a in sampled: rr.extend(by[a])
        try:
            m=fit(rr,response)
        except (ValueError,ZeroDivisionError):
            continue
        bphase.append(m["raw"]["beta_DFP_Start"])
        bfat.append(m["raw"]["beta_scaledIFBFat"])
        yphase.append(m["year_fe"]["beta_DFP_Start"])
        yfat.append(m["year_fe"]["beta_scaledIFBFat"])
        completed+=1
    return {
        "cluster_unit":"animal",
        "unique_animals":len(ids),
        "replicates_requested":reps,
        "replicates_completed":completed,
        "raw_DFP_Start_ci95":ci95(bphase),
        "raw_scaledIFBFat_ci95":ci95(bfat),
        "year_fe_DFP_Start_ci95":ci95(yphase),
        "year_fe_scaledIFBFat_ci95":ci95(yfat),
    }


def loo(rows,response):
    ids=sorted({r["animal"] for r in rows if r.get(response) is not None})
    p=[]; f=[]
    for a in ids:
        rr=[r for r in rows if r["animal"]!=a and r.get(response) is not None]
        try: m=fit(rr,response)["raw"]
        except (ValueError,ZeroDivisionError): continue
        p.append(m["beta_DFP_Start"]); f.append(m["beta_scaledIFBFat"])
    return {
        "n_fits":len(p),
        "DFP_Start_range":[min(p),max(p)],
        "scaledIFBFat_range":[min(f),max(f)],
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--url",default=DEFAULT_URL)
    ap.add_argument("--bootstrap-replicates",type=int,default=10000)
    ap.add_argument("--seed",type=int,default=20261003)
    ap.add_argument("--output",type=Path,default=Path("outputs/payoff_b_mule_deer_two_clock_channel_result.json"))
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

    # Match the already validated Ortega variance-funnel parser: the first
    # actuator block occupies A:G, with row 1 as a group title and row 2 as
    # the actual header. Do not stop at internal blank rows.
    actuator_header=[norm(x) for x in actuator_matrix[1][:7]]
    actuator_idx={name:i for i,name in enumerate(actuator_header)}
    act=[]
    for row in actuator_matrix[2:]:
        if not row:
            continue
        def get_a(name):
            i=actuator_idx[name]
            return row[i] if i<len(row) else ""
        idyr=norm(get_a("id_yr"))
        if not idyr:
            continue
        act.append({
            "id_yr":idyr,
            "rate.km.day":get_a("rate.km.day"),
            "stopover.day":get_a("stopover.day"),
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
    amap={}
    for row in act:
        i=norm(row.get("id_yr",""))
        if not i: continue
        amap[i]={
            "rate":parse_float(row.get("rate.km.day","")),
            "stopover":parse_float(row.get("stopover.day","")),
        }

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

    result={
        "date":"2026-10-03",
        "status":"POSTFREEZE_MULE_DEER_TWO_CLOCK_CHANNEL_DISSOCIATION_RESULT",
        "frozen_submission_affected":False,
        "source_sha256":sha,
        "safe_joined_rows":len(joined),
        "safe_animals":len({r["animal"] for r in joined}),
        "parser_guard":{
            "actuator_rows_parsed":len(act),
            "expected_movement_rate_rows":152,
            "parser_matches_validated_variance_funnel_layout":True
        },
        "movement_rate":{
            "fit":fit(joined,"rate"),
            "bootstrap":bootstrap(joined,"rate",args.bootstrap_replicates,args.seed),
            "leave_one_animal_out":loo(joined,"rate"),
        },
        "stopover":{
            "fit":fit(joined,"stopover"),
            "bootstrap":bootstrap(joined,"stopover",args.bootstrap_replicates,args.seed+1),
            "leave_one_animal_out":loo(joined,"stopover"),
        },
        "interpretation_rule":{
            "dissociation_supported":"DFP_Start coefficient has expected sign and bootstrap CI excludes zero while scaledIFBFat bootstrap CI includes zero for both actuators",
            "H2":"never licensed by this audit",
        },
        "boundaries":[
            "source paper already reports nutritional condition did not influence migration speed/stopover; this is a continuous source-data reproduction",
            "observational coefficient dissociation is not causal independence",
            "all rows are post-readiness for the focal downstream actuators, so a null IFBFat interaction cannot test H2 gating",
            "frozen GEB V2 unchanged",
        ],
    }

    def ex0(ci): return ci[0]<0<ci[1]
    rate=result["movement_rate"]["bootstrap"]
    stop=result["stopover"]["bootstrap"]
    supported=(
        rate["raw_DFP_Start_ci95"][0]>0
        and stop["raw_DFP_Start_ci95"][1]<0
        and ex0(rate["raw_scaledIFBFat_ci95"])
        and ex0(stop["raw_scaledIFBFat_ci95"])
    )
    result["interpretation_rule"]["dissociation_supported_boolean"]=supported

    if len(act) != 152:
        raise SystemExit(f"expected 152 actuator rows from validated first block, got {len(act)}")
    if len(joined) < 20:
        raise SystemExit(f"safe joined sample unexpectedly small: {len(joined)}")

    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
