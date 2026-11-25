#!/usr/bin/env python3
"""Observed host assay and hypothetical alternative-host selection across held-out populations.
No actual mismatch or behavior, no primary theta.
"""
import hashlib,io,json,itertools,sys,math
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import openpyxl,requests
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold

SHA="76992552871f727ccbe0d5718c1bc1a7a93aaddd57cb0a8f2cef669e74ee6598"
MD5="cc97938880788705d34d69baf351954b"
HOSTS=sorted(["Acer","Alnus","Betula","Crataegus","Malus","Prunus","Quercus","Salba","Scapraea"])
OAK=HOSTS.index("Quercus")
ALT=[i for i in range(len(HOSTS)) if i!=OAK]
KS=(1,2,4,8)
SUB={k:np.asarray(list(itertools.combinations(range(8),k)),int) for k in KS}
HEADS={"pupal_mass":["ind","pop","host","culu","survp","masspg","masspm","sex"],
       "development_time":["ind","host","pop","julian","survp","culu","pup","duration"]}

def read(b):
    if len(b)!=282857 or hashlib.md5(b).hexdigest()!=MD5 or hashlib.sha256(b).hexdigest()!=SHA:raise Hold("SOURCE_INTEGRITY")
    w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
    out={}
    try:
        dic=[list(r) for r in w["key"].iter_rows(values_only=True) if any(x is not None for x in r)]
        print("DICTIONARY "+json.dumps(dic,ensure_ascii=True,default=str),flush=True)
        key={str(r[0]).strip().lower():str(r[1]) for r in dic if len(r)>=2 and r[0] is not None}
        if not all(k in key for k in ("ind","pop","host","culu","survp")):raise Hold("SOURCE_DICTIONARY")
        for name,h in HEADS.items():
            it=w[name].iter_rows(values_only=True)
            if list(next(it))!=h:raise Hold("HEADER")
            r=[dict(zip(h,x)) for x in it if any(v is not None for v in x)]
            if len(r)!=3600:raise Hold("ROW_COUNT")
            if any(x[k] is None for x in r for k in ("ind","pop","host","culu","survp")):raise Hold("MISSING_DESIGN")
            if len({str(x["ind"]) for x in r})!=3600:raise Hold("NONUNIQUE_INDIVIDUAL_LABEL")
            g=defaultdict(list)
            for x in r:
                if x["host"] not in HOSTS:raise Hold("HOST_CODE")
                z=float(x["survp"])
                if z not in (0,1):raise Hold("SURVIVAL_CODE")
                g[(str(x["pop"]),x["host"],str(x["culu"]))].append(int(z))
            pops=sorted({k[0] for k in g})
            if len(pops)!=4 or len(g)!=180 or any(len(v)!=20 for v in g.values()):raise Hold("CULTURE_GRAIN")
            if any(sum(k[:2]==(p,h) for k in g)!=5 for p in pops for h in HOSTS):raise Hold("POP_HOST_SUPPORT")
            out[name]=g
    finally:w.close()
    if set(out["pupal_mass"])!=set(out["development_time"]):raise Hold("CROSS_SHEET_CULTURE_KEYS")
    # Do not join by nominal individual labels: source explicitly says endpoint
    # correspondence at individual level was not possible.
    g=out["pupal_mass"]
    if any(sum(v)!=sum(out["development_time"][k]) for k,v in g.items()):raise Hold("CROSS_SHEET_SURVIVAL_TOTAL")
    pops=sorted({k[0] for k in g})
    a=np.array([[sorted([(k[2],sum(v)/20) for k,v in g.items() if k[:2]==(p,h)]) for h in HOSTS] for p in pops],object)
    # array dimensions populations x host x culture x (label, proportion)
    arr=np.asarray(a[:,:,:,1],float)
    return pops,arr,{"n_source_rows_per_sheet":3600,"culture_count":180,"cultures_per_pop_host":5,
        "larvae_per_culture":20,"same_culture_survival_totals":True,"source_dictionary":key,
        "no_individual_cross_sheet_join":True,"original_survival_total":sum(map(sum,g.values()))}

def policies(m):
    # m: draws x population x host. Ranking learned exclusively from other
    # populations in every draw; ties resolved by alphabetical host order.
    a=m[:,:,ALT];oak=m[:,:,OAK];n=len(m)
    out={}
    for p in range(4):
        tr=a[:,[i for i in range(4) if i!=p],:].mean(axis=1)
        te=a[:,p,:]
        for k in KS:
            combos=SUB[k]
            scores=tr[:,combos] # draws, subsets, options
            select=np.argmax(scores,axis=2)
            option=np.take_along_axis(np.broadcast_to(combos,(n,*combos.shape)),select[:,:,None],axis=2)[:,:,0]
            val=np.take_along_axis(te,option,axis=1)
            alternatives=te[:,combos]
            blind=alternatives.mean(axis=2)
            oracle=alternatives.max(axis=2)
            d=out.setdefault(k,{"blind":[],"train_ranked":[],"oracle":[],"fraction_train_ranked_gt_oak":[]})
            d["blind"].append(blind.mean(axis=1))
            d["train_ranked"].append(val.mean(axis=1))
            d["oracle"].append(oracle.mean(axis=1))
            d["fraction_train_ranked_gt_oak"].append((val>oak[:,p,None]+1e-12).mean(axis=1))
    for k,v in out.items():
        out[k]={name:np.stack(x,axis=1) for name,x in v.items()}
    return out

def pack(x):
    a=np.asarray(x,float)
    return {"estimate":float(a[0]),"interval95_conditional_cultures":np.quantile(a[1:],[.025,.975]).tolist()}

def fit(pops,arr):
    rng=np.random.default_rng(20261125)
    idx=rng.integers(0,5,size=(10000,4,9,5))
    b=np.take_along_axis(np.broadcast_to(arr,(10000,*arr.shape)),idx,axis=3).mean(axis=3)
    m=np.concatenate([arr.mean(axis=2)[None,:,:],b],axis=0)
    oak=m[:,:,OAK]
    point=m[0]
    pm={}
    for i,p in enumerate(pops):
        s=point[i]
        tr=point[[j for j in range(4) if j!=i],:][:,ALT].mean(axis=0)
        order=np.argsort(-tr,kind="stable")
        pm[p]={"host_survival":dict(zip(HOSTS,s.tolist())),
               "host_counts_survived":dict(zip(HOSTS,np.rint(s*100).astype(int).tolist())),
               "alternative_gt_oak":int(sum(s[j]>s[OAK]+1e-12 for j in ALT)),
               "alternative_eq_oak":int(sum(abs(s[j]-s[OAK])<=1e-12 for j in ALT)),
               "alternative_lt_oak":int(sum(s[j]<s[OAK]-1e-12 for j in ALT)),
               "training_ranked_alternatives":[HOSTS[ALT[j]] for j in order]}
    op=policies(m);po={}
    for k,v in op.items():
        po[str(k)]={"n_equally_weighted_subsets":len(SUB[k]),"per_population":{},"across_population":{}}
        for name,val in v.items():
            if name.startswith("fraction"):
                po[str(k)]["across_population"][name]=pack(val.mean(axis=1))
                for i,p in enumerate(pops):po[str(k)]["per_population"].setdefault(p,{})[name]=float(val[0,i])
                continue
            dif=val-oak
            po[str(k)]["across_population"][name]={"survival":pack(val.mean(axis=1)),
                "difference_vs_oak":pack(dif.mean(axis=1))}
            for i,p in enumerate(pops):po[str(k)]["per_population"].setdefault(p,{})[name]={
                "survival":float(val[0,i]),"difference_vs_oak":float(dif[0,i])}
        po[str(k)]["across_population"]["ranked_minus_blind"]=pack((v["train_ranked"]-v["blind"]).mean(axis=1))
    fixed={h:{"survival":pack(m[:,:,i].mean(axis=1)),
              "difference_vs_oak":pack((m[:,:,i]-oak).mean(axis=1))} for i,h in enumerate(HOSTS)}
    return {"populations":pm,"equal_population_fixed_host_contrasts":fixed,"option_policy":po,
            "oak_survival":pack(oak.mean(axis=1)),"bootstrap_draws":10000,
            "uncertainty":"Conditional resampling of five observed cultures within each population-host cell. Mixed-brood dependence not identified; four populations fixed. Selection is recomputed in every draw. No prospective/generalizable coverage guarantee."}

def selftest():
    m=np.zeros((1,4,9),float);m[:,:,OAK]=.2
    m[:,:,ALT[0]]=.6;m[:,:,ALT[1]]=.4
    a=policies(m)
    assert np.allclose(a[8]["train_ranked"],.6)
    assert np.allclose(a[1]["blind"],a[8]["blind"])
    assert np.allclose(a[1]["train_ranked"],a[1]["blind"])
    assert np.all(a[8]["oracle"]>=a[8]["train_ranked"])
    # Held-out choice must not exploit the held-out population.
    m[0,0,ALT[0]]=0;m[0,0,ALT[1]]=1
    a=policies(m)
    assert a[8]["train_ranked"][0,0]==0 and a[8]["oracle"][0,0]==1
    print("SYNTHETIC_POLICY_CHECKS_PASS",flush=True)
if __name__=="__main__":
    selftest()
    out={"status":"HOLD","source_sha256":SHA,"primary_theta_added":0,"meta_pooled":False}
    try:
        with requests.Session() as s:b=fetch(s,"https://api.figshare.com/v2/file/download/50395776",cap=400000)
        pops,a,aud=read(b);out["audit"]=aud
        print("DESIGN "+json.dumps(aud,ensure_ascii=True),flush=True)
        out.update(status="SECONDARY_HOST_OPTION_TRANSFER_COMPLETE",result=fit(pops,a))
    except (Hold,ValueError,KeyError,requests.RequestException) as e:out["error"]=str(e) if isinstance(e,Hold) else type(e).__name__
    print(json.dumps(out,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2,ensure_ascii=True)+"\n")
