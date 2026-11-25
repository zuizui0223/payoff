#!/usr/bin/env python3
"""Frozen oak paired-stage contrast. Original source data are never exported."""
import csv, hashlib, io, json, sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlparse
import numpy as np
import requests
from payoff_b_buffering_oak_zenodo_source_gate_20261125 import OAK_URL,OAK_MD5,OAK_DOI,V_DOI
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch, Hold, BASE, walk, provider_id
SHA="3075bfa3f41a0f702d23bab9ce444318160ce37fea91cf7eea602dc098e5bd21"
HEADER=["TreeID","year","Treatment","Tag","flowers","acorns_june","acorns_final"]
ARM0={"control","natural","open pollination","open pollinated"}
ARM1={"pollen","pollen addition","pollen supplemented","pollen supplementation","hand pollinated","hand pollination","supplemented","supplementation","pollen added","pollen supplement","pollinated"}
MISSING={"","na","nan","null"}
def norm(s):return " ".join(s.lower().replace("_"," ").replace("-"," ").strip().split())
def arm(x):
    k=norm(x)
    if k in ARM0:return 0
    if k in ARM1:return 1
    raise Hold("TREATMENT_LABEL_NOT_AUTHENTICATED")
def integer(s):
    x=float(s.strip().replace(",","."))
    if not np.isfinite(x) or x<0 or x!=int(x):raise Hold("INVALID_OBSERVED_COUNT")
    return int(x)
def aggregate(rows):
    audit={"n_rows":len(rows),"labels":sorted({r["Treatment"] for r in rows}),
           "years":sorted({r["year"] for r in rows}),"exclusions_by_arm":{}}
    print("SOURCE_DESIGN",json.dumps(audit),flush=True)
    if set(audit["years"])!={"2018","2019"}:raise Hold("SOURCE_YEARS_UNRESOLVED")
    if {arm(k) for k in audit["labels"]}!={0,1}:raise Hold("MISSING_ARM")
    sums=defaultdict(lambda:np.zeros(3,dtype=int)); keys=set(); ex=defaultdict(Counter)
    reverse=0
    for r in rows:
        b=arm(r["Treatment"]);ex[b]["rows"]+=1
        if any((r[k] or "").strip().lower() in MISSING for k in ("TreeID","year","Tag","flowers","acorns_june","acorns_final")):
            ex[b]["incomplete"]+=1;continue
        key=(r["TreeID"].strip(),r["year"],b,r["Tag"].strip())
        if key in keys:raise Hold("DUPLICATE_COMPLETE_SHOOT_KEY")
        keys.add(key)
        n,j,f=(integer(r[k]) for k in HEADER[-3:])
        if j>n or f>n:raise Hold("ACORNS_EXCEED_FLOWERS")
        if n==0:ex[b]["zero_flowers"]+=1;continue
        reverse+=f>j
        sums[key[:3]]+=np.array([n,j,f],int)
        ex[b]["complete_positive_flower_shoots"]+=1
    d=defaultdict(dict)
    for (tree,y,b),val in sums.items():d[(tree,y)][b]=val
    records=[]
    for (tree,y),v in sorted(d.items()):
        if set(v)!={0,1}:continue
        records.append((tree,y,v[0][1:]/v[0][0],v[1][1:]/v[1][0]))
    audit.update(exclusions_by_arm={str(k):dict(v) for k,v in ex.items()},
        observed_tree_years=len(d),paired_tree_years=len(records),
        paired_trees=len({r[0] for r in records}),
        paired_year_counts=dict(Counter(r[1] for r in records)),
        complete_shoots_final_gt_june=int(reverse))
    print("PREFIT_SUPPORT",json.dumps(audit),flush=True)
    return records,audit
def estimates(rates):
    # [control June, control final, supplement June, supplement final]
    z=np.mean(rates,axis=0)
    rd=(z[2:]-z[:2])*100
    out=np.array([*z,*rd,rd[1]-rd[0],np.nan,np.nan,np.nan])
    if np.all(z>0):
        lr=np.log(z[2:]/z[:2])
        out[-3:]=[*lr,lr[1]-lr[0]]
    return out
NAMES=["control_june","control_final","supplement_june","supplement_final",
       "rd_june_pp","rd_final_pp","rd_final_minus_june_pp","logrr_june","logrr_final","logrr_final_minus_june"]
def analyze(records,audit):
    if audit["paired_trees"]<30 or any(audit["paired_year_counts"].get(y,0)<15 for y in ("2018","2019")):
        raise Hold("INSUFFICIENT_PAIRED_TREE_SUPPORT")
    arr=np.array([np.r_[r[2],r[3]] for r in records])
    clusters=defaultdict(list)
    for i,r in enumerate(records):clusters[r[0]].append(i)
    groups=list(clusters.values());rng=np.random.default_rng(20261125)
    boot=np.empty((10000,len(NAMES)))
    for i in range(len(boot)):
        ix=np.concatenate([groups[k] for k in rng.integers(0,len(groups),len(groups))])
        boot[i]=estimates(arr[ix])
    point=estimates(arr)
    def pack(p,b):
        o={}
        for i,n in enumerate(NAMES):
            o[n]={"estimate":float(p[i]) if np.isfinite(p[i]) else None,
                  "interval_95":np.quantile(b[:,i],[.025,.975]).tolist() if np.all(np.isfinite(b[:,i])) else None}
        return o
    by_year={}
    for y in ("2018","2019"):
        z=estimates(arr[np.array([r[1]==y for r in records])])
        by_year[y]={k:float(v) if np.isfinite(v) else None for k,v in zip(NAMES,z)}
    return {"status":"EXPLORATORY_SECONDARY_STAGE_CONTRAST_COMPLETE","estimates":pack(point,boot),
        "year_strata":by_year,"bootstrap_draws":10000,"bootstrap_unit":"whole_tree",
        "primary_theta_eligible":False,"causal_mismatch_claim":False}

def paginated_vazquez_metadata(s):
    u=BASE+"/versions/420579/files";seen=set();files={}
    while u:
        if u in seen or len(seen)>=20:raise Hold("PAGINATION_LIMIT")
        p=urlparse(u)
        if (p.scheme,p.netloc)!=("https","datadryad.org") or not p.path.startswith("/api/v2/versions/420579/files"):
            raise Hold("UNEXPECTED_PAGINATION_URL")
        seen.add(u);obj=json.loads(fetch(s,u))
        for x in walk(obj):
            raw=x.get("path") or x.get("filename") or x.get("name")
            fid=provider_id(x,"files")
            if raw and fid is not None:
                n=str(raw).split("/")[-1]
                rec={"file_id":fid,"size":x.get("size") or x.get("sizeBytes"),"digest":x.get("digest"),"digest_type":x.get("digestType")}
                if n in files and files[n]!=rec:raise Hold("CONFLICTING_FILE_METADATA")
                files[n]=rec
        nxt=obj.get("_links",{}).get("next",{}).get("href")
        u=urljoin(u,nxt) if nxt else None
    expected={"plants.csv","trampas.csv","emerg.csv","polen_megach_2006.csv","polen_megach_2007.csv","polen_megach_2008.csv"}
    return {"status":"METADATA_ONLY_NO_RAW_DOWNLOAD","pages":len(seen),"files":files,"required_complete":expected.issubset(files),"missing":sorted(expected-set(files))}

def self_test():
    # Within-tree-year equal weighting and paired effect signs, not actual data.
    p=estimates(np.array([[.2,.1,.4,.2],[.4,.2,.6,.3]]))
    assert np.allclose(p[4:7],[20,10,-10])
    assert np.isclose(p[-1],0)
    assert arm("Control")==0 and arm("Pollen addition")==1
    try:arm("opaque")
    except Hold:pass
    else:raise AssertionError("opaque treatment accepted")
    print("SYNTHETIC_CHECKS_PASS",flush=True)
def run():
    self_test(); out={"status":"NO_PRIMARY_THETA","oak":{"doi":OAK_DOI},"vazquez":{"doi":V_DOI}}
    with requests.Session() as s:
        try:
            b=fetch(s,OAK_URL,cap=100000)
            if hashlib.md5(b).hexdigest()!=OAK_MD5 or hashlib.sha256(b).hexdigest()!=SHA:
                raise Hold("SOURCE_HASH_MISMATCH")
            reader=csv.DictReader(io.StringIO(b.decode("utf-8-sig")),delimiter=";")
            if reader.fieldnames!=HEADER:raise Hold("SOURCE_SCHEMA_MISMATCH")
            rows=list(reader)
            if len(rows)!=960:raise Hold("SOURCE_N_MISMATCH")
            records,audit=aggregate(rows);out["oak"]["audit"]=audit
            out["oak"].update(analyze(records,audit))
        except (Hold,ValueError,requests.RequestException,KeyError) as e:
            out["oak"].update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
        try:out["vazquez"].update(paginated_vazquez_metadata(s))
        except (Hold,ValueError,requests.RequestException,KeyError) as e:
            out["vazquez"].update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
    print(json.dumps(out,indent=2,ensure_ascii=False),flush=True);return out
if __name__=="__main__":
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(run(),indent=2,ensure_ascii=False)+"\n")
