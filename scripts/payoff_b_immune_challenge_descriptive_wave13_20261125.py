#!/usr/bin/env python3
"""Descriptive, equal-family-weight immune challenge contrasts; no CI."""
import hashlib,io,json,math,sys
from collections import defaultdict,Counter
from pathlib import Path
import openpyxl,requests
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold
from payoff_b_immune_challenge_source_design_wave13_20261125 import SHA,MD5,HEAD,missing,numeric,audit

PH={"Normal":("N","1"),"12-day delayed":("D","2")}
IMM={"PHA-injected":("PHA","1"),"APBS-injected":("APBS","2"),"Control (not-injected)":("Control","3")}
CELLS=[(p,t) for p in ("N","D") for t in ("PHA","APBS","Control")]
INJECTED=[(p,t) for p,t in CELLS if t!="Control"]
def mean(x):
    if not x:raise Hold("EMPTY_CELL")
    return math.fsum(x)/len(x)
def read(b):
    a=audit(b)
    if a["source_rows"]!=426 or a["families"]!=21 or a["unique_larvae_global"]!=426 or a["families_with_parent_conflict"]!=0 or a["parent_connected_family_component_sizes"]!=[9,9,3] or a["families_all_6_complete_duration_mass"]!=17:
        raise Hold("PINNED_DESIGN_CHANGED")
    if not all(x in a["dictionary"]["RespPerc"] for x in ("Percentage","PHA","APBS")) or "grams" not in a["dictionary"]["Mass"] or "days" not in a["dictionary"]["LarvalPeriod"]:
        raise Hold("DICTIONARY")
    w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
    try:
        it=w["Data"].iter_rows(values_only=True)
        if list(next(it))!=HEAD:raise Hold("HEADER")
        rows=[dict(zip(HEAD,r)) for r in it if any(x is not None for x in r)]
    finally:w.close()
    fam=defaultdict(lambda:defaultdict(list));parent={}
    for r in rows:
        p,pn=PH[r["Phenology"]];t,tn=IMM[r["Immunity"]]
        if str(r["PhenN"])!=pn or str(r["ImmN"])!=tn:raise Hold("TREATMENT_CODE_CONFLICT")
        f=str(r["Family"]);pair=(str(r["Male"]),str(r["Female"]))
        if f in parent and parent[f]!=pair:raise Hold("PARENT_CONFLICT")
        parent[f]=pair;fam[f][(p,t)].append(r)
    graph={f:{g for g in parent if f!=g and any(a==b for a,b in zip(parent[f],parent[g]))} for f in parent}
    todo=set(graph);comps=[]
    while todo:
        q=[min(todo)];seen=set()
        while q:
            f=q.pop()
            if f in seen:continue
            seen.add(f);todo.discard(f);q.extend(sorted(graph[f]-seen))
        comps.append(seen)
    comps.sort(key=lambda z:(-len(z),min(z)))
    if sorted(map(len,comps),reverse=True)!=[9,9,3]:raise Hold("PARENT_COMPONENTS")
    result={};support=defaultdict(Counter)
    for f,groups in fam.items():
        z={}
        for k,rs in groups.items():
            both=[r for r in rs if numeric(r["LarvalPeriod"])==numeric(r["Mass"])=="positive"]
            if not both:continue
            v={"duration":mean([float(r["LarvalPeriod"]) for r in both]),"mass":mean([float(r["Mass"]) for r in both]),"n_complete":len(both)}
            if k in INJECTED:
                resp=[]
                for r in rs:
                    if missing(r["RespPerc"]):continue
                    x=float(r["RespPerc"])
                    if not math.isfinite(x):raise Hold("NONFINITE_IMMUNE_RESPONSE")
                    resp.append(x)
                v.update(response=mean(resp),n_response=len(resp))
            z[k]=v
        if set(z)!=set(CELLS):continue
        result[f]=z
        for k,v in z.items():
            support["|".join(k)]["complete_duration_mass_rows"]+=v["n_complete"]
            support["|".join(k)]["immune_response_rows"]+=v.get("n_response",0)
    if len(result)!=17:raise Hold("COMPLETE_FAMILY_COUNT")
    return result,comps,dict(support)

def calc(fam,fs):
    vals={k:{x:mean([fam[f][k][x] for f in fs]) for x in ("duration","mass")} for k in CELLS}
    resp={k:mean([fam[f][k]["response"] for f in fs]) for k in INJECTED}
    dur={t:vals[("D",t)]["duration"]-vals[("N",t)]["duration"] for t in ("PHA","APBS","Control")}
    mass={t:math.log(vals[("D",t)]["mass"]/vals[("N",t)]["mass"]) for t in ("PHA","APBS","Control")}
    im={t:resp[("D",t)]-resp[("N",t)] for t in ("PHA","APBS")}
    def interactions(x):
        return {"PHA_minus_APBS":x["PHA"]-x["APBS"],"APBS_minus_Control":x["APBS"]-x["Control"],"PHA_minus_Control":x["PHA"]-x["Control"]}
    return {"n_families":len(fs),"cell_means":{"|".join(k):v for k,v in vals.items()},
       "duration_delayed_minus_normal_days":dur,"duration_interaction_days":interactions(dur),
       "mass_delayed_vs_normal_lnRR":mass,"mass_log_interaction":interactions(mass),
       "immune_response_cell_means_percent":{"|".join(k):v for k,v in resp.items()},
       "immune_response_delayed_minus_normal_pp":im,"immune_response_interaction_pp":im["PHA"]-im["APBS"]}
def main():
    out={"status":"HOLD","source_sha256":SHA,"primary_theta_added":0}
    try:
        with requests.Session() as s:b=fetch(s,"https://api.figshare.com/v2/file/download/6912350",cap=100000)
        fam,comps,support=read(b);fs=sorted(fam)
        out.update(status="SECONDARY_DESCRIPTIVE_FAMILY_CONTRASTS_COMPLETE",support=support,
            result=calc(fam,fs),components=[{"component":i+1,"all_source_families":len(c),"complete_families":len(c&set(fs))} for i,c in enumerate(comps)],
            leave_one_parent_component_out={str(i+1):calc(fam,[f for f in fs if f not in c]) for i,c in enumerate(comps)},
            uncertainty_status="HOLD_INFERENTIAL_VARIANCE_THREE_PARENT_COMPONENTS_AND_UNVERIFIED_ASSIGNMENT",
            endpoint_note="Immune response uses all observed injected responses within same complete families, not same individual endpoint-complete subset. No causal mediation.")
    except (Hold,ValueError,KeyError,requests.RequestException) as e:out["error"]=str(e) if isinstance(e,Hold) else type(e).__name__
    print(json.dumps(out,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+"\n")
if __name__=="__main__":main()
