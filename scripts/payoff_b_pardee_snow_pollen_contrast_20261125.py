#!/usr/bin/env python3
"""Frozen secondary snowmelt-by-supplied-pollen contrast; no raw rows exported."""
import csv, hashlib, io, json, sys, re
from collections import defaultdict, Counter
from pathlib import Path
import numpy as np
import openpyxl, requests
from payoff_b_pardee_snowmelt_source_gate_20261125 import source, FILES
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import Hold

HASH={
"Claytonia_SeedSet.csv":"99c16b2acb7c05f137bee78817341db152ef7ce9a8919d0657eeec5dcb84b0a4",
"Delphinium_SeedSet.csv":"d83f0dbd18f5fc3319d3a9683e8907ef5541976adc284fa2d26683cc9947431e",
"Potentilla_SeedSet.csv":"c8abb56006db201527ceac347dced3a238f835c6c92e98a811607d40417c957a",
"MetaData.xlsx":"24c7da09bf04487cbc1ef8487cd2a4b58c3818c85c833ef997cbb413f894e03a"}
N={"Claytonia":231,"Delphinium":229,"Potentilla":260}
MISSING={"","na","nan","null"}
STRATA=[(0,0),(0,1),(1,0),(1,1)]
def verified(s,name):
    b=source(s,name)
    if hashlib.sha256(b).hexdigest()!=HASH[name]:raise Hold("SOURCE_SHA256_MISMATCH")
    return b
def dictionary(b):
    w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
    relevant=[]
    try:
        for sh in w.worksheets:
            for row in sh.iter_rows(values_only=True):
                v=" | ".join(str(x) for x in row if x is not None)
                if re.search(r"\bpollen\b|pollen_supplemented|\bAP\b|\bNP\b|total_seeds",v,re.I):
                    relevant.append({"sheet":sh.title,"text":v[:800]})
    finally:w.close()
    # Explicit provenance mapping, never infer from outcome signs.
    print("SOURCE_DICTIONARY",json.dumps(relevant[:80],ensure_ascii=False),flush=True)
    joint=" ".join(x["text"] for x in relevant)
    ap=bool(re.search(r"\bAP\b.{0,60}(?:add(?:ed|ition)?|supplement(?:ed|al|ation)?).{0,30}pollen|(?:add(?:ed|ition)?|supplement(?:ed|al|ation)?).{0,30}pollen.{0,40}\bAP\b|\bAP\b.{0,50}pollen.{0,30}(?:add|supplement)",joint,re.I))
    np_=bool(re.search(r"\bNP\b.{0,60}(?:natural|no|not|non).{0,30}pollen|(?:natural|no|not|non).{0,30}pollen.{0,40}\bNP\b|\bNP\b.{0,50}pollen.{0,30}(?:natural|not|no)",joint,re.I))
    return {"confirmed_by_dictionary_pattern":ap and np_,"ap":ap,"np":np_,"relevant_rows":relevant[:80]}
def parse(b,species):
    r=csv.DictReader(io.StringIO(b.decode("utf-8-sig")))
    req={"Plot","SnowTreat","FrostTreat","Plant_num","Pollen_supplemented","Total_seeds"}
    if not req.issubset(r.fieldnames or []):raise Hold("REQUIRED_HEADER_MISSING")
    rows=list(r)
    if len(rows)!=N[species]:raise Hold("SOURCE_ROW_COUNT_MISMATCH")
    alloc={};seen=set();counts=Counter();plots=defaultdict(lambda:defaultdict(list))
    for row in rows:
        plot=row["Plot"].strip();plant=row["Plant_num"].strip()
        if plot.lower() in MISSING or plant.lower() in MISSING:raise Hold("MISSING_PLOT_PLANT_ID")
        k=(plot,plant)
        if k in seen:raise Hold("DUPLICATE_PLOT_PLANT")
        seen.add(k)
        try:a=({"Natural":0,"Removal":1}[row["SnowTreat"]],{"NoFrost":0,"Frost":1}[row["FrostTreat"]])
        except KeyError:raise Hold("UNEXPECTED_TREATMENT")
        if plot in alloc and alloc[plot]!=a:raise Hold("PLOT_ALLOCATION_CONFLICT")
        alloc[plot]=a
        p=row["Pollen_supplemented"].strip();y=row["Total_seeds"].strip()
        if p.lower() in MISSING:counts["missing_pollen"]+=1;continue
        if p not in ("AP","NP"):raise Hold("UNEXPECTED_POLLEN_CODE")
        if y.lower() in MISSING:counts["missing_seeds"]+=1;continue
        y=float(y)
        if not np.isfinite(y) or y<0 or y!=int(y):raise Hold("INVALID_SEED_COUNT")
        counts["complete_plant_rows"]+=1
        if y==0:counts["zero_seeds"]+=1
        plots[plot][p].append(y)
    groups={k:[] for k in STRATA};allplots=Counter(alloc.values())
    for p,arms in plots.items():
        if set(arms)!={"AP","NP"}:
            counts["unpaired_observed_plots"]+=1;continue
        groups[alloc[p]].append([np.mean(arms["NP"]),np.mean(arms["AP"])])
    audit={"rows":len(rows),"exclusions":dict(counts),"source_plots_by_snow_frost":{str(k):allplots[k] for k in STRATA},"paired_plots_by_snow_frost":{str(k):len(groups[k]) for k in STRATA}}
    return groups,audit
def est(g):
    # [Natural NP, Natural AP, Removal NP, Removal AP]
    a=np.array([np.mean(x,axis=0) for x in g])
    w=np.r_[a[:2].mean(axis=0),a[2:].mean(axis=0)]
    add=(w[3]-w[1])-(w[2]-w[0])
    low=high=theta=np.nan
    if np.all(w>0):
        low=np.log(w[2]/w[0]);high=np.log(w[3]/w[1]);theta=high-low
    return np.r_[w,low,high,theta,add]
NAMES=["natural_NP","natural_AP","removal_NP","removal_AP","logRR_NP","logRR_AP","theta_snow","additive_interaction"]
def fit(groups,audit):
    if any(len(groups[k])<5 for k in STRATA):raise Hold("INSUFFICIENT_PAIRED_PLOTS")
    g=[np.array(groups[k],float) for k in STRATA]
    point=est(g);rng=np.random.default_rng(20261125);bs=np.empty((10000,len(NAMES)))
    for i in range(len(bs)):
        bs[i]=est([a[rng.integers(0,len(a),len(a))] for a in g])
    d={}
    for i,k in enumerate(NAMES):
        valid=np.isfinite(bs[:,i])
        d[k]={"estimate":float(point[i]) if np.isfinite(point[i]) else None,
          "valid_draws":int(valid.sum()),"interval_95":np.quantile(bs[:,i],[.025,.975]).tolist() if valid.all() else None,
          "bootstrap_variance":float(np.var(bs[:,i],ddof=1)) if valid.all() else None}
    return {"status":"SECONDARY_ESTIMATE","effects":d,"admitted_primary":False,
      "low_pollen_snow_detrimental":bool(point[4]<0)}
def self_test():
    a=np.array([[10,10],[10,10]])
    b=np.array([[5,8],[5,8]])
    p=est([a,a,b,b])
    assert np.isclose(p[6],np.log(1.6)) and p[7]==3
    assert np.isnan(est([a,a,np.zeros_like(b),np.zeros_like(b)])[6])
    print("SYNTHETIC_ARITHMETIC_CHECK_PASS",flush=True)
def run():
    self_test()
    out={"status":"SECONDARY_SNOW_X_POLLEN_NOT_PRIMARY","source_doi":"10.5061/dryad.kd1r166","species":{}}
    with requests.Session() as s:
        try:out["dictionary"]=dictionary(verified(s,"MetaData.xlsx"))
        except (Hold,ValueError,requests.RequestException) as e:
            out["dictionary"]={"confirmed_by_dictionary_pattern":False,"error":str(e) if isinstance(e,Hold) else type(e).__name__}
        if not out["dictionary"]["confirmed_by_dictionary_pattern"]:
            out["status"]="HOLD_POLLEN_MAPPING_NOT_CONFIRMED"
        else:
            for sp in N:
                x={};out["species"][sp]=x
                try:
                    g,a=parse(verified(s,sp+"_SeedSet.csv"),sp);x["audit"]=a
                    print("PREFIT",sp,json.dumps(a),flush=True)
                    x.update(fit(g,a))
                except (Hold,ValueError,requests.RequestException,KeyError) as e:
                    x.update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
    print(json.dumps(out,indent=2,ensure_ascii=False),flush=True);return out
if __name__=="__main__":
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(run(),indent=2,ensure_ascii=False)+"\n")
