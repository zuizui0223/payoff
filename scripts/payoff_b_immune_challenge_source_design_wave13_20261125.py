#!/usr/bin/env python3
"""Original immune workbook design audit: no biological effect estimates."""
import hashlib,io,json,math,sys
from collections import Counter,defaultdict
from pathlib import Path
import openpyxl,requests
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold

SHA="e7d47607bc2501d73ca94d430104bec6adde1eeb89feb8c1344f0de211938488"
MD5="bbf6ad22d4ca9add79723a7a85f8bb3c"
HEAD=["Larvae","Family","Male","Female","Phenology","PhenN","Immunity","ImmN","ImmResp","RespPerc","Mass","LarvalPeriod"]
MISSING={"","na","n/a","nan","null","none","dead","-"}

def missing(x):
    return x is None or str(x).strip().lower() in MISSING
def numeric(x):
    if missing(x):return "missing"
    try:v=float(x)
    except (ValueError,TypeError):return "other_token"
    if not math.isfinite(v):return "nonfinite"
    return "nonpositive" if v<=0 else "positive"

def audit(b):
    if len(b)!=48122 or hashlib.md5(b).hexdigest()!=MD5 or hashlib.sha256(b).hexdigest()!=SHA:
        raise Hold("SOURCE_INTEGRITY")
    w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
    try:
        info=[[str(x) for x in r if x is not None] for r in w["Info"].iter_rows(values_only=True) if any(x is not None for x in r)]
        defs={str(r[0]).strip():" ".join(str(x) for x in r[1:] if x is not None) for r in w["Variables"].iter_rows(values_only=True) if r and r[0] is not None}
        it=w["Data"].iter_rows(values_only=True)
        if list(next(it))!=HEAD:raise Hold("HEADER")
        rows=[dict(zip(HEAD,r)) for r in it if any(x is not None for x in r)]
    finally:w.close()
    if len(rows)!=426:raise Hold("ROWS")
    groups=defaultdict(list);codes=defaultdict(Counter)
    for r in rows:
        if any(missing(r[k]) for k in ("Larvae","Family","Male","Female")):
            raise Hold("ID_MISSING")
        groups[str(r["Family"])].append(r)
        for k,n in (("Phenology","PhenN"),("Immunity","ImmN")):codes[k][(str(r[k]),str(r[n]))]+=1
    if len(groups)!=21:raise Hold("FAMILIES")
    graph={f:set() for f in groups}; parents={k:defaultdict(set) for k in ("Male","Female")}
    pair_counts=Counter();cells=defaultdict(Counter);per_fam={};parent_conflicts=0
    for f,rs in groups.items():
        if any(len({str(r[k]) for r in rs})!=1 for k in ("Male","Female")):
            parent_conflicts+=1
        for k in parents:
            for r in rs:parents[k][str(r[k])].add(f)
        pair_counts.update({(str(rs[0]["Male"]),str(rs[0]["Female"])):1})
        ff=defaultdict(Counter)
        for r in rs:
            key=str(r["Phenology"])+"|"+str(r["Immunity"])
            for x in (cells[key],ff[key]):
                x["rows"]+=1
                for k in ("LarvalPeriod","Mass","ImmResp","RespPerc"):
                    x[k+"_"+numeric(r[k])]+=1
                if numeric(r["LarvalPeriod"])==numeric(r["Mass"])=="positive":x["complete_duration_mass"]+=1
        per_fam[f]={k:dict(v) for k,v in ff.items()}
    for p in parents.values():
        for fs in p.values():
            for f in fs:graph[f].update(fs-{f})
    todo=set(graph);components=[]
    while todo:
        stack=[min(todo)];comp=set()
        while stack:
            f=stack.pop()
            if f in comp:continue
            comp.add(f);todo.discard(f);stack.extend(sorted(graph[f]-comp))
        components.append(comp)
    keys=sorted(cells)
    all6=sum(set(v)==set(keys) for v in per_fam.values()) if len(keys)==6 else 0
    complete6=sum(set(v)==set(keys) and all(x.get("complete_duration_mass",0)>0 for x in v.values()) for v in per_fam.values()) if len(keys)==6 else 0
    return {"status":"IMMUNE_SOURCE_DESIGN_ONLY","source_sha256":SHA,"source_rows":len(rows),"info":info,
       "dictionary":{k:defs.get(k) for k in HEAD},"families":len(groups),
       "unique_larvae_global":len({str(r["Larvae"]) for r in rows}),"unique_larvae_within_family":len({(str(r["Family"]),str(r["Larvae"])) for r in rows}),
       "families_with_parent_conflict":parent_conflicts,"distinct_parent_pairs_using_first_family_row":len(pair_counts),
       "parent_counts":{k:len(v) for k,v in parents.items()},
       "reused_same_sex_parent_counts":{k:sum(len(fs)>1 for fs in v.values()) for k,v in parents.items()},
       "parent_connected_family_component_sizes":sorted(map(len,components),reverse=True),
       "phenotype_and_immune_code_checks":{k:[{"label":a,"code":b,"n":v} for (a,b),v in sorted(c.items())] for k,c in codes.items()},
       "cells":{k:dict(v) for k,v in sorted(cells.items())},"families_all_6_cells":all6,"families_all_6_complete_duration_mass":complete6,
       "per_cell_family_support":{k:sum(k in v and v[k].get("complete_duration_mass",0)>0 for v in per_fam.values()) for k in keys},
       "primary_theta_added":0,"note":"No biological outcome values or models exported; signed immune responses not treated as invalid merely for nonpositive values; parent grouping is diagnostic, not proof of independence."}
if __name__=="__main__":
    try:
        with requests.Session() as s:b=fetch(s,"https://api.figshare.com/v2/file/download/6912350",cap=100000)
        d=audit(b)
    except (Hold,ValueError,KeyError,requests.RequestException) as e:d={"status":"HOLD","error":str(e) if isinstance(e,Hold) else type(e).__name__}
    print(json.dumps(d,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+"\n")
