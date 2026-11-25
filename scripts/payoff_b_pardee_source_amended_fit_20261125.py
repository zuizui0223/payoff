#!/usr/bin/env python3
"""Explicit post-diagnostic source amendment; no primary theta or raw rows."""
import csv, io, json, sys
from collections import defaultdict
from pathlib import Path
from unittest.mock import patch
import numpy as np
import requests
import payoff_b_pardee_snow_pollen_contrast_20261125 as core
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import Hold

PLAN={"Claytonia":["unchanged","canonical_only"],"Delphinium":["literal_NA"],"Potentilla":["drop_conflict","retain_first","retain_last"]}
CANONICAL={str(i) for i in range(1,9)}
DESIGN=("Plot","Plant_num","SnowTreat","FrostTreat","Pollen_supplemented")

def normalize(b,sp,mode):
    reader=csv.DictReader(io.StringIO(b.decode("utf-8-sig")))
    h=reader.fieldnames
    if not h or len(set(h))!=len(h) or not set((*DESIGN,"Total_seeds")).issubset(h):raise Hold("SCHEMA")
    rows=list(reader)
    if len(rows)!=core.N[sp] or any(None in r or any(v is None for v in r.values()) for r in rows):
        raise Hold("SOURCE_ROWS")
    keys=defaultdict(list)
    for i,r in enumerate(rows):
        keys[(r["Plot"].strip(),r["Plant_num"].strip())].append(i)
    duplicate=[ix for ix in keys.values() if len(ix)>1]
    nas=[i for i,r in enumerate(rows) if r["Total_seeds"].strip()=="N/A"]
    noncanonical=[i for i,r in enumerate(rows) if r["Plant_num"].strip() not in CANONICAL]
    if (len(duplicate),len(nas),len(noncanonical))!={"Claytonia":(0,0,9),"Delphinium":(0,1,0),"Potentilla":(1,0,0)}[sp]:
        raise Hold("DIAGNOSTIC_NO_LONGER_MATCHES")
    for r in rows:
        p=r["Plant_num"].strip(); c=r["Pollen_supplemented"].strip()
        if p in CANONICAL and c in ("NP","AP") and c!=("NP" if int(p)<=4 else "AP"):
            raise Hold("CANONICAL_ASSIGNMENT_MISMATCH")
    drop=set();normalized=0
    if sp=="Delphinium" and mode=="literal_NA":
        rows[nas[0]]["Total_seeds"]="";normalized=1
    elif sp=="Potentilla":
        ix=duplicate[0]
        if len(ix)!=2:raise Hold("EXPECTED_DUPLICATE_PAIR")
        a,z=(rows[k] for k in ix)
        if any(a[c].strip()!=z[c].strip() for c in DESIGN) or a==z or a["Total_seeds"]==z["Total_seeds"]:
            raise Hold("DUPLICATE_SEMANTICS_CHANGED")
        if mode=="drop_conflict":drop.update(ix)
        elif mode=="retain_first":drop.add(ix[1])
        elif mode=="retain_last":drop.add(ix[0])
        else:raise Hold("UNKNOWN_MODE")
    elif sp=="Claytonia":
        if mode=="canonical_only":drop.update(noncanonical)
        elif mode!="unchanged":raise Hold("UNKNOWN_MODE")
    else:raise Hold("UNKNOWN_MODE")
    out=io.StringIO(newline="")
    w=csv.DictWriter(out,fieldnames=h);w.writeheader();w.writerows(r for i,r in enumerate(rows) if i not in drop)
    audit={"original_rows":len(rows),"cleaned_rows":len(rows)-len(drop),
           "excluded_source_rows":len(drop),"literal_NA_normalized_to_missing":normalized,
           "duplicate_key_groups":len(duplicate),"noncanonical_plant_rows":len(noncanonical)}
    return out.getvalue().encode("utf-8"),audit

def analyze(b,sp,mode):
    cleaned,audit=normalize(b,sp,mode)
    # Core checks the supplied CSV length against N. Verify raw N above;
    # temporarily supply explicit cleaned length only. No change to core fit.
    with patch.dict(core.N,{sp:audit["cleaned_rows"]}):
        g,a=core.parse(cleaned,sp)
    result=core.fit(g,a)
    return {"normalization":audit,"audit":a,**result}

def self_test():
    # Tiny synthetic files; test normalization only, no biology.
    h=["Plot","SnowTreat","FrostTreat","Plant_num","Pollen_supplemented","Total_seeds"]
    def data(rows):
        o=io.StringIO();w=csv.writer(o);w.writerow(h);w.writerows(rows);return o.getvalue().encode()
    def r(plot,p,seed,code=None):
        return [plot,"Natural","Frost",p,code or ("NP" if int(p)<=4 else "AP"),seed]
    with patch.dict(core.N,{"Delphinium":2,"Potentilla":3}):
        b=data([r("a","1","N/A"),r("a","5",0)])
        v,a=normalize(b,"Delphinium","literal_NA")
        assert a["literal_NA_normalized_to_missing"]==1 and a["cleaned_rows"]==2
        rec=list(csv.DictReader(io.StringIO(v.decode())))
        assert rec[0]["Total_seeds"]=="" and rec[1]["Total_seeds"]=="0"
        b=data([r("a","1",1),r("a","1",2),r("a","5",0)])
        for mode,n,expected in [("drop_conflict",1,["0"]),("retain_first",2,["1","0"]),("retain_last",2,["2","0"])]:
            v,a=normalize(b,"Potentilla",mode)
            assert a["cleaned_rows"]==n
            assert [x["Total_seeds"] for x in csv.DictReader(io.StringIO(v.decode()))]==expected
        try:normalize(data([r("a","1",1),r("a","1",1),r("a","5",0)]),"Potentilla","drop_conflict")
        except Hold:pass
        else:raise AssertionError("identical duplicate unexpectedly accepted")
    print("NORMALIZATION_SYNTHETIC_CHECKS_PASS",flush=True)

def run():
    self_test()
    out={"status":"EXPLORATORY_SECONDARY_AMENDMENT","source_doi":"10.5061/dryad.kd1r166","primary_theta_eligible":False,"species":{}}
    with requests.Session() as s:
        d=core.dictionary(core.verified(s,"MetaData.xlsx"))
        if not d["confirmed_by_dictionary_pattern"]:raise Hold("DICTIONARY_NOT_CONFIRMED")
        out["dictionary_confirmed"]=True
        for sp,modes in PLAN.items():
            b=core.verified(s,sp+"_SeedSet.csv")
            out["species"][sp]={}
            for mode in modes:
                try:out["species"][sp][mode]=analyze(b,sp,mode)
                except (Hold,ValueError,KeyError) as e:out["species"][sp][mode]={"status":"HOLD","error":str(e) if isinstance(e,Hold) else type(e).__name__}
    print(json.dumps(out,indent=2),flush=True)
    return out
if __name__=="__main__":
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(run(),indent=2)+"\n")
