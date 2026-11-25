#!/usr/bin/env python3
"""Wave 8: repeated-unit-aware descriptive Collinsia source extraction; no primary theta."""
import csv,hashlib,io,json,math,sys
from pathlib import Path
import requests
import payoff_b_glopl_seasonal_contrast_20261125 as c
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold

# Table 2, Kalisz & Vogler 2003, published success/failure counts and rounded
# percentage for O1 (supplemented intact), O2 (emasculated), O3 (intact).
# The searchable rendering for TMC 2000 early O3 is inconsistent; flag it.
# Only early/late rows used; no claim of access to individual plant records.
TABLE=[
("BT",1999,"early",[(118,39,75),(117,39,75),(129,39,77)]),
("BT",1999,"late",[(8,151,5),(4,143,3),(13,156,8)]),
("BT",2000,"early",[(154,28,85),(120,45,72),(158,35,82)]),
("BT",2000,"late",[(132,43,75),(106,52,67),(122,65,65)]),
("EF",1999,"early",[(107,46,70),(104,33,76),(108,51,68)]),
("EF",1999,"late",[(10,143,6),(10,137,7),(12,180,6)]),
("EF",2000,"early",[(149,9,94),(144,28,84),(172,15,92)]),
("EF",2000,"late",[(75,80,48),(49,55,47),(81,81,50)]),
("TMC",1999,"early",[(43,122,26),(44,122,26),(55,105,34)]),
("TMC",1999,"late",[(3,138,2),(0,159,0),(4,140,3)]),
("TMC",2000,"early",[(113,15,88),(161,16,91),(170,170,92)]),
("TMC",2000,"late",[(13,129,9),(21,143,13),(29,157,16)])]
def table_rate(v):
    a,b,pct=v
    if min(a,b)<0 or a+b<=0:raise Hold("TABLE_COUNT_INVALID")
    p=a/(a+b)
    return p if abs(100*p-pct)<=1 else None
def decompose():
    rows={}
    for site,y,t,a in TABLE:
        p1,p2,p3=(table_rate(x) for x in a)
        key=f"{site}-{y}"
        z={"p1":p1,"p2":p2,"p3":p3,"source_count_percent_conflict":[k for k,p in zip(("O1","O2","O3"),(p1,p2,p3)) if p is None]}
        if p1 is not None:z["remaining_failure_after_supplement"]=1-p1
        if all(x is not None for x in (p1,p2,p3)):
            z.update(residual_supplement_difference=p1-p3,intact_minus_emasculated=p3-p2,
                     total_failure_emasculated=1-p2)
            assert math.isclose((1-p1)+(p1-p3)+(p3-p2),1-p2)
        rows.setdefault(key,{})[t]=z
    for z in rows.values():
        e,l=z["early"],z["late"]
        for k in ("p1","remaining_failure_after_supplement","residual_supplement_difference","intact_minus_emasculated"):
            z["late_minus_early_"+k]=l[k]-e[k] if e.get(k) is not None and l.get(k) is not None else None
    return rows

def source_rows(b):
    c.verify_git_blob(b)
    if hashlib.sha256(b).hexdigest()!=c.SHA:raise Hold("SOURCE_SHA")
    rows=list(csv.DictReader(io.StringIO(b.decode("latin-1"))))
    byid={r["unique_number"]:r for r in rows}
    if len(rows)!=2969 or len(byid)!=2969:raise Hold("SOURCE_IDS")
    return byid
def collinsia(b):
    byid=source_rows(b)
    result={}
    for i,(site,pop) in enumerate([("BT","1"),("EF","2"),("TMC","3")]):
        for j,year in enumerate(["1999","2000"]):
            ids=[str(988+i*6+j*3+k) for k in range(3)]
            periods={}
            for id,phase in zip(ids,["early","mid","late"]):
                r=byid[id]
                if (c.doi(r["DOI"]),r["unique_study_number"],r["Species_Author"],r["population"],r["year_of_study"],r[c.NOTE],r["Level_of_Supplementation"],r["Emasculated_treatment"])!=("10.1890/02-0519","287","Collinsia_verna",pop,year,f"{site}-{year}-{phase}","flower","no"):
                    raise Hold("PINNED_SOURCE_CONTEXT")
                a=c.endpoint(r,"FS")
                if not all(z["mean"] is not None and 0<z["mean"]<=1 for z in a.values()):raise Hold("INVALID_FS_MEAN")
                periods[phase]={"id":id,"arms":a,"lnRR":math.log(a["Sup"]["mean"]/a["Natural"]["mean"]),
                                "risk_difference":a["Sup"]["mean"]-a["Natural"]["mean"]}
            e,l=periods["early"],periods["late"]
            result[f"{site}-{year}"]={"periods":periods,
               "delta_late_minus_early_lnRR":l["lnRR"]-e["lnRR"],
               "late_minus_early_supplemented_fruit_set":l["arms"]["Sup"]["mean"]-e["arms"]["Sup"]["mean"],
               "late_minus_early_natural_fruit_set":l["arms"]["Natural"]["mean"]-e["arms"]["Natural"]["mean"],
               "delta_supplement_risk_difference":l["risk_difference"]-e["risk_difference"],
               "variance_status":"HOLD_REPEATED_PLANT_AND_SD_N_GRAIN",
               "admitted_primary":False}
    return result
def metadata(s):
    out={}
    for k in (3297944,3304797):
        try:
            u=f"https://api.figshare.com/v2/collections/{k}/articles?page_size=100"
            v=json.loads(fetch(s,u,cap=800000))
            if not isinstance(v,list):raise Hold("COLLECTION_SHAPE")
            # Metadata only; no data files opened.
            out[str(k)]={"status":"PUBLIC_COLLECTION_METADATA_ONLY","items":[{f:a.get(f) for f in ("id","title","doi","url_public_html","published_date")} for a in v]}
        except (Hold,ValueError,requests.RequestException) as e:
            out[str(k)]={"status":"HOLD","error":str(e) if isinstance(e,Hold) else type(e).__name__}
    return out
def self_test():
    assert table_rate((170,170,92)) is None
    assert table_rate((0,159,0))==0
    assert table_rate((120,45,72)) is not None
    d=decompose()
    assert len(d)==6 and sum(z["late_minus_early_intact_minus_emasculated"] is not None for z in d.values())==5
    print("SYNTHETIC_AND_TABLE_ARITHMETIC_CHECKS_PASS",flush=True)
if __name__=="__main__":
    self_test()
    with requests.Session() as s:
        d={"status":"COLLINSIA_SECONDARY_POINT_ESTIMATES_ONLY","source_sha256":c.SHA,
           "collinsia_glopl":collinsia(fetch(s,c.GLOPL_URL,cap=6000000)),
           "collinsia_table2_decomposition":decompose(),"figshare":metadata(s),
           "trifolium":{"status":"HOLD_EXACT_SOURCE_UNIT_AND_ARM_MAPPING","source_ids":["2192","2193","2194","2195"]},
           "primary_theta_added":0}
    print(json.dumps(d,indent=2,ensure_ascii=True),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+"\n")
