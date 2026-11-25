#!/usr/bin/env python3
"""Source-diagnostic amendment: strict 64 tanks and two fixed sensitivities.
Reuses the frozen endpoint and whole-container bootstrap without altering raw data.
"""
import hashlib,io,json,re,sys
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import openpyxl,requests
import payoff_b_priority_compensation_tank_fit_20261125 as core
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold

MODES=("strict64","numeric65","observed69")
MISSING_TEXT="ND-H-1"
UNBALANCED={"ND-H-5","ND-L-3","NE-L-6","NE-L-7"}
NUM={"1":"N","2":"D","3":"E"}
EXPECTED_COUNTS={"strict64":64,"numeric65":65,"observed69":69}

def source(b):
    if len(b)!=81042 or hashlib.md5(b).hexdigest()!=core.MD5 or hashlib.sha256(b).hexdigest()!=core.SHA:
        raise Hold("SOURCE_INTEGRITY")
    w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
    try:
        defs={str(r[0]).strip():" ".join(str(x) for x in r[1:] if x is not None)
              for r in w["Variables"].iter_rows(values_only=True) if r and r[0] is not None}
        if not all(defs.get(k) for k in ("Container","Mix","Food","Phenology","PhenN","LarvalPeriod","Mass")):
            raise Hold("DICTIONARY_INCOMPLETE")
        if "1:N" not in defs["PhenN"] or "2:D" not in defs["PhenN"] or "3:E" not in defs["PhenN"]:
            raise Hold("PHENOTYPE_CODE_DICTIONARY")
        if "day" not in defs["LarvalPeriod"].lower() or "metamorph" not in defs["Mass"].lower() or "gram" not in defs["Mass"].lower():
            raise Hold("ENDPOINT_DICTIONARY")
        it=w["Data"].iter_rows(values_only=True)
        if list(next(it))!=core.HEAD:raise Hold("SOURCE_HEADER")
        rows=[dict(zip(core.HEAD,r)) for r in it if any(v is not None for v in r)]
    finally:w.close()
    tanks=defaultdict(list)
    for r in rows:
        if r["ContainerID"] is None:raise Hold("MISSING_TANK_ID")
        tanks[r["ContainerID"]].append(r)
    if len(rows)!=828 or len(tanks)!=69 or any(len(v)!=12 for v in tanks.values()):
        raise Hold("SOURCE_GRAIN")
    if len({v[0]["Container"] for v in tanks.values()})!=69:
        raise Hold("SOURCE_TANK_LABELS")
    return tanks,defs

def classify(rs):
    x=rs[0]
    for k in ("Container","ContainerID","Block","Food","Mix","FoodN"):
        if x[k] is None or len({r[k] for r in rs})!=1:raise Hold("INCONSISTENT_TANK_ASSIGNMENT")
    if {str(r["LarvaeN"]) for r in rs}!={str(i) for i in range(1,13)}:
        raise Hold("SLOT_GRAIN")
    code=str(x["Container"])
    m=re.fullmatch(r"(NN|DD|EE|ND|NE)-(H|L)-(\d+)",code)
    if not m:raise Hold("UNRESOLVED_CODE")
    raw,f,_=m.groups()
    g=raw[0] if raw[0]==raw[1] else raw
    food={"H":"High","L":"Low"}[f]
    if x["Food"]!=food or str(x["FoodN"])!=("1" if f=="H" else "2") or str(x["Mix"])!=("1" if len(g)==1 else "2"):
        raise Hold("ASSIGNMENT_CONFLICT")
    if str(x["Block"]) not in {"1","2","3","4"}:raise Hold("BLOCK")
    text=[core.PH.get(r["Phenology"]) for r in rs]
    num=[NUM.get(str(r["PhenN"])) for r in rs]
    if None in num:raise Hold("UNKNOWN_NUMERIC_PHENOTYPE")
    for t,n,r in zip(text,num,rs):
        if t is None:
            if code!=MISSING_TEXT or r["Phenology"] is not None or n!="N":
                raise Hold("UNEXPECTED_MISSING_LABEL")
        elif t!=n:raise Hold("PHENOTYPE_FIELDS_CONFLICT")
    exp=core.GROUPS[g]
    if code==MISSING_TEXT:
        if text.count(None)!=1 or Counter(num)!=exp or g!="ND" or f!="H":
            raise Hold("MISSING_LABEL_DIAGNOSTIC_CHANGED")
        kind="numeric_text_missing"
    elif code in UNBALANCED:
        if None in text or len(g)!=2 or Counter(text)!=Counter({"N":5,g[1]:7}):
            raise Hold("UNBALANCED_DIAGNOSTIC_CHANGED")
        kind="observed_5_7"
    else:
        if None in text or Counter(text)!=exp:raise Hold("UNEXPECTED_COMPOSITION")
        kind="strict"
    return code,food,g,str(x["Block"]),kind,num

def prepare(tanks,defs,mode):
    if mode not in MODES:raise Hold("MODE")
    out=defaultdict(list)
    excluded=Counter();quality=Counter();support=Counter();endpoint=Counter();cohort_support=defaultdict(Counter)
    for rs in tanks.values():
        code,f,g,block,kind,p=classify(rs)
        quality[kind]+=1
        if (kind=="numeric_text_missing" and mode=="strict64") or (kind=="observed_5_7" and mode!="observed69"):
            excluded[kind]+=1;continue
        support[(f,g)]+=1
        vals=defaultdict(list)
        for r,ph in zip(rs,p):
            a=core.val(r["LarvalPeriod"]);m=core.val(r["Mass"])
            if a is None:endpoint["missing_duration"]+=1
            if m is None:endpoint["missing_mass"]+=1
            if a is None or m is None:
                endpoint["incomplete_either"]+=1;continue
            vals[ph].append([a,m])
        if set(vals)!=set(g):
            excluded["empty_endpoint_cohort"]+=1;continue
        z={k:np.mean(v,axis=0) for k,v in vals.items()}
        out[(f,g)].append((block,z))
        for k,v in vals.items():
            cohort_support[f+"|"+g][k]+=len(v)
            endpoint["complete_rows_in_usable_tanks"]+=len(v)
    if dict(quality)!={"strict":64,"numeric_text_missing":1,"observed_5_7":4}:raise Hold("DIAGNOSTIC_COUNTS_CHANGED")
    if sum(support.values())!=EXPECTED_COUNTS[mode]:raise Hold("MODE_DESIGN_COUNT")
    audit={"source_rows":828,"source_tanks":69,"mode":mode,"design_classes":dict(quality),
           "design_admitted_tanks":sum(support.values()),"usable_tanks_total":sum(map(len,out.values())),
           "design_tanks_per_cell":{"|".join(k):v for k,v in sorted(support.items())},
           "usable_tanks_per_cell":{"|".join(k):len(v) for k,v in sorted(out.items())},
           "excluded_tanks":dict(excluded),"endpoint_completeness":dict(endpoint),
           "complete_rows_by_cell_and_cohort":{k:dict(v) for k,v in sorted(cohort_support.items())},
           "duration_definition":defs["LarvalPeriod"],"mass_definition":defs["Mass"]}
    if any(len(out[(f,g)])<4 for f in core.FOODS for g in core.GROUPS):
        return None,{**audit,"hold":"INSUFFICIENT_TANKS_AFTER_ENDPOINT_CHECK"}
    return out,audit

def test_design():
    rs=[]
    for i,p in enumerate(["N"]*5+["D"]*7,1):
        rs.append({"Container":"ND-H-5","ContainerID":1,"Block":2,"Food":"High","FoodN":1,
                   "Mix":2,"LarvaeN":i,"Phenology":"Normal" if p=="N" else "Delayed (6days)",
                   "PhenN":1 if p=="N" else 2})
    assert classify(rs)[4]=="observed_5_7"
    rs[0]["PhenN"]=2
    try:classify(rs)
    except Hold:pass
    else:raise AssertionError("mismatch accepted")
    core.self_test()
    print("AMENDED_DESIGN_SYNTHETIC_CHECKS_PASS",flush=True)

def main():
    test_design()
    out={"status":"HOLD","source_sha256":core.SHA,"primary_theta_added":0,"modes":{}}
    try:
        with requests.Session() as s:b=fetch(s,"https://api.figshare.com/v2/file/download/6328354",cap=100000)
        tanks,defs=source(b)
        for mode in MODES:
            z=out["modes"][mode]={"status":"HOLD"}
            try:
                g,a=prepare(tanks,defs,mode)
                z["audit"]=a
                if g is None:continue
                effects,cov=core.run_fit(g)
                z.update(status="SECONDARY_CONTAINER_CONTRASTS_COMPLETE",contrasts=effects,bootstrap=cov)
            except (Hold,ValueError,KeyError) as e:z["error"]=str(e) if isinstance(e,Hold) else type(e).__name__
        out["status"]="SECONDARY_AMENDMENT_COMPLETE" if all(x["status"]=="SECONDARY_CONTAINER_CONTRASTS_COMPLETE" for x in out["modes"].values()) else "PARTIAL_OR_HOLD"
    except (Hold,ValueError,KeyError,requests.RequestException) as e:out["error"]=str(e) if isinstance(e,Hold) else type(e).__name__
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,ensure_ascii=True,separators=(",",":")),flush=True)
if __name__=="__main__":main()
