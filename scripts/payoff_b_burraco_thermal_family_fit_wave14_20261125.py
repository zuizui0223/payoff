#!/usr/bin/env python3
"""Pinned Burraco 2021 family-level secondary contrasts, conditional on two rooms."""
import hashlib,io,json,math,sys,itertools
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import openpyxl,requests
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold
SHA="10d4be0c29be5b767ceddd44c014ed1f704f95c3a1b87eddfae1d96dd091de53"
MD5="d492e35ec5d8ebb038449cbd83efe595"
HEAD=["Vial","Family","FamN","Phenology","PCode","PhenN","Temp","TCode","TempN","Food","FCode","FoodN","LarvaeN","Survival","Days","Mass","Growth rate"]
PH={"Normal":0,"Delayed 6 days":6,"Delayed 12 days":12}
ROOM={"Warm 19 C":"warm","Cold 15 C":"cold","Cold15 C":"cold"}
FOOD={"Ad Libitum":"full","Restricted":"limited"}
CELLS=list(itertools.product((0,6,12),("warm","cold"),("full","limited")))
IDX={k:i for i,k in enumerate(CELLS)}
MISSING={"","na","n/a","nan","null","none","-"}
def missing(x):return x is None or str(x).strip().lower() in MISSING
def finite_pos(x):
    if missing(x):return None
    try:v=float(x)
    except (TypeError,ValueError):raise Hold("NONNUMERIC_ENDPOINT")
    if not math.isfinite(v) or v<=0:raise Hold("INVALID_ENDPOINT")
    return v
def slot(v):
    if missing(v):raise Hold("MISSING_SLOT")
    x=float(v)
    if not x.is_integer() or x<1 or x>6:raise Hold("INVALID_SLOT")
    return int(x)
def read(b):
    if len(b)!=87598 or hashlib.md5(b).hexdigest()!=MD5 or hashlib.sha256(b).hexdigest()!=SHA:raise Hold("SOURCE_HASH")
    w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
    try:
        s=w["Sheet1"]
        r=[list(x) for x in s.iter_rows(values_only=True) if any(v is not None for v in x)]
        if r[2][:len(HEAD)]!=HEAD or any(v is not None for v in r[2][len(HEAD):]):raise Hold("HEADER")
        marks=[a[17] if len(a)>17 else None for a in r[3:]]
        if sum(v=="*" for v in marks)!=4 or any(v not in (None,"*") for v in marks) or any(any(v is not None for v in a[18:]) for a in r[3:]):
            raise Hold("AUXILIARY_MARKER_STRUCTURE_CHANGED")
        rows=[dict(zip(HEAD,a[:17]),_source_marker=m) for a,m in zip(r[3:],marks)]
    finally:w.close()
    if len(rows)!=787:raise Hold("SOURCE_ROW_COUNT")
    mappings=defaultdict(lambda:defaultdict(set))
    keys=Counter();vials=defaultdict(list);families=set();rows2=[];marked=set();zero_duration=0
    for r in rows:
        if any(missing(r[k]) for k in HEAD[:14]):raise Hold("MISSING_DESIGN_OR_SURVIVAL")
        try:f=str(r["Family"]);d=PH[r["Phenology"]];t=ROOM[r["Temp"]];q=FOOD[r["Food"]]
        except KeyError:raise Hold("SOURCE_LABEL")
        k=(f,d,t,q,slot(r["LarvaeN"]))
        for col,sem in (("FamN",f),("PCode",d),("PhenN",d),("TCode",t),("TempN",t),("FCode",q),("FoodN",q)):
            mappings[col][str(r[col])].add(str(sem))
        if r["_source_marker"]=="*":marked.add(k)
        keys[k]+=1;families.add(f)
        vials[str(r["Vial"])].append(k)
        sflag=float(r["Survival"])
        if sflag not in (0,1):raise Hold("SURVIVAL_CODE")
        if r["Days"] in (0,"0"):
            if str(r["Vial"])!="6-E-L-A-1" or k!=("6",12,"cold","full",1) or sflag!=1:
                raise Hold("UNEXPECTED_ZERO_DURATION")
            zero_duration+=1;days=None
        else:days=finite_pos(r["Days"])
        mass=finite_pos(r["Mass"])
        if sflag==0 and (days is not None or mass is not None):raise Hold("DEAD_WITH_METAMORPHOSIS_ENDPOINT")
        rows2.append((str(r["Vial"]),k,int(sflag),days,mass))
    if len(families)!=11:raise Hold("FAMILY_COUNT")
    for col,m in mappings.items():
        if any(len(v)!=1 for v in m.values()) or len(set(next(iter(v)) for v in m.values()))!=len(m):raise Hold("NONBIJECTIVE_CODE_"+col)
    planned=set((f,*c,i) for f in families for c in CELLS for i in range(1,7))
    duplicate_keys=[{"family":k[0],"delay":k[1],"room":k[2],"food":k[3],"slot":k[4],"n":n} for k,n in keys.items() if n>1]
    duplicates={k:[list(x) for x in v] for k,v in vials.items() if len(v)>1}
    absent=planned-set(keys)
    design={"source_rows":len(rows),"families":len(families),"unique_vials":len(vials),
            "unique_planned_keys":len(keys),"planned_slots":len(planned),"absent_slots":len(absent),
            "absent_by_cell":{"|".join(map(str,k)):n for k,n in sorted(Counter(k[1:4] for k in absent).items())},
            "duplicate_planned_keys":duplicate_keys,"duplicate_vial_design_keys":duplicates,
            "code_maps":{col:{k:sorted(v) for k,v in m.items()} for col,m in mappings.items()},
            "unlabelled_marker_count":len(marked),"marker_keys_overlap_duplicate_vial_rows":sum(k in marked for vv in duplicates.values() for k in map(tuple,vv)),
            "survival_counts":dict(Counter(a[2] for a in rows2)),
            "zero_duration_excluded_from_paired_endpoints":zero_duration,
            "nonmissing_duration":sum(a[3] is not None for a in rows2),"nonmissing_mass":sum(a[4] is not None for a in rows2)}
    print("DESIGN "+json.dumps(design,ensure_ascii=True),flush=True)
    if duplicate_keys or set(keys)-planned or len(absent)!=5 or len(duplicates)!=1 or any(len(v)!=2 or len({tuple(x) for x in v})!=2 for v in duplicates.values()):
        return None,design
    if design["survival_counts"]!={1:697,0:90} or zero_duration!=1 or design["nonmissing_duration"]!=696 or design["nonmissing_mass"]!=694:
        raise Hold("SOURCE_SUPPORT_CHANGED")
    return (rows2,families,set(duplicates),marked),design

def label(c):return "|".join(map(str,c))
def prepare(source,mode):
    rr,fs,dup,marked=source;groups=defaultdict(list)
    for vial,key,s,day,mass in rr:
        if mode in ("strict","strict_unmarked") and vial in dup:continue
        if mode=="strict_unmarked" and key in marked:continue
        groups[(key[0],key[1:4])].append((s,day,mass))
    dm={};sv={};bounds={};n_dm=0
    support={label(c):Counter() for c in CELLS}
    for f in sorted(fs):
        a=[];b=[];lo=[];hi=[];all_dm=True;all_sv=True
        for c in CELLS:
            x=groups[(f,c)]
            if len(x)>6:raise Hold("CELL_SLOT_OVERFLOW")
            valid=[r for r in x if r[0]==1 and r[1] is not None and r[2] is not None]
            z=support[label(c)];z["observed_rows"]+=len(x);z["survived"]+=sum(r[0] for r in x);z["complete_survivor_endpoints"]+=len(valid)
            z["families_observed"]+=bool(x);z["families_complete_endpoints"]+=bool(valid)
            if x:b.append(sum(r[0] for r in x)/len(x))
            else:all_sv=False;b.append(np.nan)
            lo.append(sum(r[0] for r in x)/6);hi.append((sum(r[0] for r in x)+6-len(x))/6)
            if valid:a.append(np.mean([[r[1],r[2]] for r in valid],axis=0))
            else:all_dm=False;a.append([np.nan,np.nan])
        if all_dm:
            dm[f]=a;n_dm+=sum(len([r for r in groups[(f,c)] if r[0]==1 and r[1] is not None and r[2] is not None]) for c in CELLS)
        if all_sv:sv[f]=b
        bounds[f]=[lo,hi]
    aud={"mode":mode,"observed_rows":sum(len(v) for v in groups.values()),"family_count_duration_mass":len(dm),"family_count_survival":len(sv),
         "duration_mass_complete_rows_in_included_families":n_dm,"per_cell_support":{k:dict(v) for k,v in support.items()},
         "missing_planned_slots_by_mode":792-sum(len(v) for v in groups.values()),
         "family_ids_overlap":len(set(dm)&set(sv))}
    if len(dm)<8 or len(sv)<8:return None,aud
    b=np.array(list(bounds.values())).mean(axis=0)
    aud["survival_intended_slot_bounds"]={label(c):[float(b[0,i]),float(b[1,i])] for i,c in enumerate(CELLS)}
    return (np.array(list(dm.values()),float),np.array(list(sv.values()),float)),aud

def summaries(x,endpoint):
    # accepts array ending in 12 cells; vectorized over leading bootstrap dimension.
    out={}
    delays={}
    for d in (6,12):
        for t,q in itertools.product(("warm","cold"),("full","limited")):
            a=x[...,IDX[(d,t,q)]];b=x[...,IDX[(0,t,q)]]
            v=np.log(a/b) if endpoint=="mass" else a-b
            delays[(d,t,q)]=v;out[f"delay|{d}|{t}|{q}"]=v
            if endpoint=="duration":out[f"nominal_recovery|{d}|{t}|{q}"]=-v/d
        for t in ("warm","cold"):out[f"food_interaction|{d}|{t}"]=delays[(d,t,"limited")]-delays[(d,t,"full")]
        for q in ("full","limited"):out[f"room_interaction|{d}|{q}"]=delays[(d,"cold",q)]-delays[(d,"warm",q)]
        out[f"three_way|{d}"]=out[f"food_interaction|{d}|cold"]-out[f"food_interaction|{d}|warm"]
    return out
def pack(a,endpoint):
    if np.any(~np.isfinite(a)):raise Hold("NONFINITE_CELL_MEANS")
    if endpoint=="mass" and np.any(a<=0):raise Hold("ZERO_MASS_MEAN")
    if endpoint=="survival" and np.any((a<0)|(a>1)):raise Hold("SURVIVAL_RANGE")
    rng=np.random.default_rng(20261125)
    idx=rng.integers(0,len(a),size=(10000,len(a)))
    point=a.mean(axis=0);b=a[idx].mean(axis=1)
    p=summaries(point,endpoint);z=summaries(b,endpoint)
    out={}
    for k in p:
        v=z[k]
        out[k]={"estimate":float(p[k]),"interval95":np.quantile(v,[.025,.975]).tolist(),
                "variance_conditional":float(np.var(v,ddof=1))}
    for i in range(len(a)):
        loo=summaries(np.delete(a,i,axis=0).mean(axis=0),endpoint)
        for k,v in loo.items():
            if "interaction" in k or k.startswith("three_way|"):
                out[k].setdefault("leave_one_family_out",[]).append(float(v))
    for v in out.values():
        if "leave_one_family_out" in v:
            vals=v.pop("leave_one_family_out");v["leave_one_family_range"]=[min(vals),max(vals)]
    return {"family_n":len(a),"cell_means":{label(c):float(point[i]) for i,c in enumerate(CELLS)},
            "effects":out,"bootstrap_draws":10000,"uncertainty":"whole-family bootstrap, conditional on two observed rooms; not replicated temperature inference"}
def selftest():
    x=np.zeros(12)
    for i,(d,t,q) in enumerate(CELLS):x[i]=50-d+(d if q=="limited" else 0)+(d if t=="cold" and q=="limited" else 0)
    z=summaries(x,"duration")
    assert z["delay|6|warm|full"]==-6
    assert z["three_way|12"]==12
    assert z["nominal_recovery|6|warm|full"]==1
    print("SYNTHETIC_CONTRAST_CHECK_PASS",flush=True)
def main():
    selftest();out={"status":"HOLD","source_sha256":SHA,"primary_theta_added":0,"modes":{}}
    try:
        with requests.Session() as s:b=fetch(s,"https://api.figshare.com/v2/file/download/25051406",cap=100000)
        source,design=read(b);out["design"]=design
        if source is None:raise Hold("COMPOSITE_KEY_AMBIGUITY_OR_PLANNED_SUPPORT")
        for mode in ("strict","observed","strict_unmarked"):
            z=out["modes"][mode]={"status":"HOLD"}
            try:
                arr,aud=prepare(source,mode);z["audit"]=aud
                if arr is None:continue
                dm,sv=arr
                z.update(duration=pack(dm[:,:,0],"duration"),mass=pack(dm[:,:,1],"mass"),survival=pack(sv,"survival"),status="SECONDARY_CONDITIONAL_CONTRASTS_COMPLETE")
            except (Hold,ValueError,KeyError) as e:z["error"]=str(e)
        out["status"]="SECONDARY_THERMAL_ANALYSIS_COMPLETE" if all(v["status"]=="SECONDARY_CONDITIONAL_CONTRASTS_COMPLETE" for v in out["modes"].values()) else "PARTIAL_OR_HOLD"
    except (Hold,ValueError,KeyError,requests.RequestException) as e:out["error"]=str(e) if isinstance(e,Hold) else type(e).__name__
    print(json.dumps(out,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+"\n")
if __name__=="__main__":main()
