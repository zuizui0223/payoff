#!/usr/bin/env python3
"""Wave 12, fixed secondary container-level compensation comparison."""
import hashlib,io,json,math,sys
from pathlib import Path
from collections import Counter,defaultdict
import numpy as np
import requests,openpyxl
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold
MD5="dafa108fd1189267ef9fcda5e3353f5f"
SHA="19535539c5585ecd2ed2de6131058267920007b52625468081c8f1a267c5c08a"
HEAD=["Container","ContainerID","Block","LarvaeN","Mix","Food","FoodN","Phenology","PhenN","LarvalPeriod","Mass","Growth"]
PH={"Normal":"N","Delayed (6days)":"D","Extra delayed (12 days)":"E"}
GROUPS={"N":Counter(N=12),"D":Counter(D=12),"E":Counter(E=12),"ND":Counter(N=6,D=6),"NE":Counter(N=6,E=6)}
FOODS=("High","Low")
MISSING={"","na","n/a","nan","null","none","dead","-"}
def val(x):
    if x is None or str(x).strip().lower() in MISSING:return None
    try:v=float(x)
    except (ValueError,TypeError):raise Hold("UNRECOGNIZED_ENDPOINT_TOKEN")
    if not math.isfinite(v) or v<=0:raise Hold("NONPOSITIVE_OR_NONFINITE_ENDPOINT")
    return v
def read(b):
    if len(b)!=81042 or hashlib.md5(b).hexdigest()!=MD5 or hashlib.sha256(b).hexdigest()!=SHA:raise Hold("SOURCE_INTEGRITY")
    w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
    try:
        defs={str(r[0]).strip():" ".join(str(x) for x in r[1:] if x is not None) for r in w["Variables"].iter_rows(values_only=True) if r and r[0] is not None}
        print("DICTIONARY "+json.dumps({k:defs.get(k) for k in HEAD},ensure_ascii=True),flush=True)
        if any(not defs.get(k) for k in ("Container","Mix","Food","Phenology","LarvalPeriod","Mass")):raise Hold("DICTIONARY_INCOMPLETE")
        if "day" not in defs["LarvalPeriod"].lower() or not ("metamorph" in defs["Mass"].lower()):raise Hold("ENDPOINT_SEMANTICS_NOT_CONFIRMED")
        it=w["Data"].iter_rows(values_only=True)
        if list(next(it))!=HEAD:raise Hold("HEADER")
        rr=[dict(zip(HEAD,r)) for r in it if any(v is not None for v in r)]
    finally:w.close()
    if len(rr)!=828:raise Hold("ROWS")
    tanks=defaultdict(list)
    for r in rr:
        if r["ContainerID"] is None:raise Hold("MISSING_TANK_ID")
        tanks[r["ContainerID"]].append(r)
    if len(tanks)!=69 or any(len(r)!=12 for r in tanks.values()):raise Hold("TANK_GRAIN")
    if len({r[0]["Container"] for r in tanks.values()})!=69:raise Hold("TANK_LABEL_NOT_UNIQUE")
    counts=Counter(); mix=defaultdict(set); out=defaultdict(list); block_support=Counter()
    for rs in tanks.values():
        for k in ("Container","ContainerID","Block","Food","Mix","FoodN"):
            if len({r[k] for r in rs})!=1 or rs[0][k] is None:raise Hold("INCONSISTENT_TANK_ASSIGNMENT")
        if len({r["LarvaeN"] for r in rs})!=12:raise Hold("INDIVIDUAL_SLOT_GRAIN")
        f,block=rs[0]["Food"],str(rs[0]["Block"])
        if f not in FOODS:raise Hold("FOOD_LABEL")
        p=Counter(PH.get(r["Phenology"],"?") for r in rs)
        if p["?"]:
            if any(r["Phenology"] not in PH and r["Phenology"] is not None and str(r["Phenology"]).strip().lower() not in MISSING for r in rs):raise Hold("UNKNOWN_PHENOLOGY_LABEL")
            counts["missing_phenology_rows"]+=p["?"];counts["tanks_excluded_unknown_phenology"]+=1;continue
        g=next((k for k,v in GROUPS.items() if p==v),None)
        if g is None:raise Hold("UNEXPECTED_TANK_COMPOSITION")
        mix[str(rs[0]["Mix"])].add("mixed" if len(g)>1 else "single")
        block_support[(f,g,block)]+=1
        values=defaultdict(list)
        for r in rs:
            a,b=val(r["LarvalPeriod"]),val(r["Mass"])
            if a is None:counts["missing_duration"]+=1
            if b is None:counts["missing_mass"]+=1
            if a is not None and b is not None:values[PH[r["Phenology"]]].append([a,b]);counts["complete_individuals"]+=1
        if set(values)!=set(g):counts["tanks_excluded_empty_cohort"]+=1;continue
        z={k:np.mean(v,axis=0) for k,v in values.items()}
        out[(f,g)].append((block,z))
    if len(mix)!=2 or set.union(*mix.values())!={"mixed","single"} or any(len(v)!=1 for v in mix.values()):raise Hold("MIX_LABEL_MISMATCH")
    if any(len(out[(f,g)])<4 for f in FOODS for g in GROUPS):raise Hold("INSUFFICIENT_TANKS")
    return out,{"source_rows":828,"source_tanks":69,"missing_and_attrition":dict(counts),"mix_mapping":{k:sorted(v) for k,v in mix.items()},"block_support_pre_endpoint":{"|".join(k):v for k,v in sorted(block_support.items())},"usable_tanks":{"|".join(k):len(v) for k,v in out.items()},"duration_definition":defs["LarvalPeriod"],"mass_definition":defs["Mass"]}
def groupmeans(group):
    return {k:np.mean([z[k] for _,z in group],axis=0) for k in group[0][1]}
def contrasts(gs,f,d):
    n=groupmeans(gs[(f,"N")])["N"]
    h=groupmeans(gs[(f,d)])[d]
    m=groupmeans(gs[(f,"N"+d)])
    a,b=m["N"],m[d]
    ds=h[0]-n[0];dm=b[0]-a[0]
    ms=math.log(h[1]/n[1]);mm=math.log(b[1]/a[1])
    return {"single_duration_difference":float(ds),"mixed_duration_difference":float(dm),"duration_interaction_days":float(dm-ds),
        "single_mass_lnRR":ms,"mixed_mass_lnRR":mm,"mass_log_interaction":mm-ms,
        "means":{"single_N":n.tolist(),"single_delayed":h.tolist(),"mixed_N":a.tolist(),"mixed_delayed":b.tolist()}}
KEYS=[(f,d) for f in FOODS for d in ("D","E")]
def compute(gs):
    return [contrasts(gs,f,d) for f,d in KEYS]
def run_fit(gs):
    main=compute(gs)
    rng=np.random.default_rng(20261125)
    boot=np.empty((10000,8))
    # Vectorized within-food/composition resampling of complete containers.
    # Shared N and within-tank cohort vectors are retained in every draw.
    means={}
    for k,g in gs.items():
        idx=rng.integers(0,len(g),size=(10000,len(g)))
        means[k]={p:np.asarray([v[p] for _,v in g])[idx].mean(axis=1) for p in g[0][1]}
    for i,(f,d) in enumerate(KEYS):
        n=means[(f,"N")]["N"];h=means[(f,d)][d];a=means[(f,"N"+d)]["N"];b=means[(f,"N"+d)][d]
        boot[:,i]=(b[:,0]-a[:,0])-(h[:,0]-n[:,0])
        boot[:,i+4]=np.log(b[:,1]/a[:,1])-np.log(h[:,1]/n[:,1])
    result={}
    for i,(f,d) in enumerate(KEYS):
        z=main[i];rel=[(f,"N"),(f,d),(f,"N"+d)]
        bs=sorted(set.intersection(*[{b for b,_ in gs[k]} for k in rel]))
        z.update(nominal_cold_delay_days={"D":6,"E":12}[d],
                 usable_tanks={k[1]:len(gs[k]) for k in rel},
                 duration_interval95=np.quantile(boot[:,i],[.025,.975]).tolist(),
                 mass_log_interval95=np.quantile(boot[:,i+4],[.025,.975]).tolist(),
                 block_common_support=bs)
        if len(bs)>=2:
            each=[contrasts({k:[v for v in gs[k] if v[0]==b] for k in rel},f,d) for b in bs]
            z["equal_block_duration_interaction"]=float(np.mean([v["duration_interaction_days"] for v in each]))
            z["equal_block_mass_interaction"]=float(np.mean([v["mass_log_interaction"] for v in each]))
            z["leave_one_common_block_out_duration"]={b:float(np.mean([v["duration_interaction_days"] for j,v in zip(bs,each) if j!=b])) for b in bs}
        else:z["block_sensitivity_status"]="HOLD_INSUFFICIENT_COMMON_BLOCKS"
        result[f+"_"+d]=z
    return result,{"labels":[f+"_"+d+"_duration" for f,d in KEYS]+[f+"_"+d+"_mass" for f,d in KEYS],"covariance":np.cov(boot,rowvar=False).tolist(),"draws":10000,"scope":"Conditional on observed tanks, food/composition stratified bootstrap; blocks not independently resampled."}
def self_test():
    def a(block,**p):return (block,{k:np.array(v,dtype=float) for k,v in p.items()})
    g={("High","N"):[a("1",N=[40,1])],("High","D"):[a("1",D=[36,1])],("High","ND"):[a("1",N=[38,1],D=[44,.8])]}
    v=contrasts(g,"High","D")
    assert v["duration_interaction_days"]==10 and abs(v["mass_log_interaction"]-math.log(.8))<1e-12
    print("SYNTHETIC_CONTRAST_CHECKS_PASS",flush=True)
if __name__=="__main__":
    self_test()
    out={"status":"HOLD","source_sha256":SHA,"primary_theta_added":0}
    try:
        with requests.Session() as s:b=fetch(s,"https://api.figshare.com/v2/file/download/6328354",cap=100000)
        g,a=read(b);out["audit"]=a
        print("DESIGN "+json.dumps(a,ensure_ascii=True),flush=True)
        z,cov=run_fit(g)
        out.update(status="SECONDARY_CONTAINER_CONTRASTS_COMPLETE",contrasts=z,bootstrap=cov)
    except (Hold,ValueError,KeyError,requests.RequestException) as ex:
        out["error"]=str(ex) if isinstance(ex,Hold) else type(ex).__name__
    print(json.dumps(out,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+"\n")
