#!/usr/bin/env python3
"""Hash-pinned GloPL variance fingerprints; no correction or new pooled fit."""
import csv,hashlib,io,json,math,re,sys,zipfile
from collections import Counter,defaultdict
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
import requests
from bs4 import BeautifulSoup
import payoff_b_glopl_seasonal_contrast_20261125 as c
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold

ARMS=("Natural","Sup","Bagout"); EPS=(.00005,.0002,.0005)
def label(x,p,n,t):
    sd=math.sqrt(p*(1-p));se=sd/math.sqrt(n)
    hits=[k for k,v in (("SD",sd),("SE",se)) if abs(x-v)<=t and abs(x/v-1)<=.02]
    return hits[0] if len(hits)==1 else "ambiguous" if hits else "neither"
def key(r):return r["unique_study_number"]
def source(b):
    c.verify_git_blob(b)
    if hashlib.sha256(b).hexdigest()!=c.SHA:raise Hold("SHA256")
    r=list(csv.DictReader(io.StringIO(b.decode("latin-1"))))
    if len(r)!=2969 or len({x["unique_number"] for x in r})!=2969:raise Hold("SOURCE_IDS")
    return r
def audit(rows,inventory):
    seasonal={str(x[k]) for x in inventory["exact_label_pair_screen"]["pairs"] for k in ("early_row","late_row")}
    result={}
    for e in ("FS","SO"):
        arms={a:Counter() for a in ARMS}; levels=defaultdict(Counter); studies=defaultdict(Counter); pubs=defaultdict(Counter)
        sub=Counter();matches=[]; tolerances={str(t):Counter() for t in EPS}; target=Counter()
        for r in rows:
            for a in ARMS:
                p,n,sd=(c.number(r.get(f"{a}_{x}_{e}")) for x in ("X","N","SD"))
                pub=c.doi(r["DOI"])
                if pub in c.MISSING:pub=r["Author"]+"|"+r["Year"]
                if p is None or n is None or sd is None:reason="missing_or_nonnumeric"
                elif not 0<p<1:reason="boundary_or_out_of_range_mean"
                elif n<2 or not n.is_integer():reason="invalid_n"
                elif sd<=0:reason="nonpositive_reported_sd"
                else:
                    reason=label(sd,p,n,.0002)
                    for t in EPS:tolerances[str(t)][label(sd,p,n,t)]+=1
                    if reason=="SE":
                        matches.append({"row":r["unique_number"],"study":key(r),"doi":pub,"arm":a,"level":r["Level_of_Supplementation"],"author":r["Author"],"year":r["Year"]})
                    studies[key(r)][reason]+=1;pubs[pub][reason]+=1;levels[r["Level_of_Supplementation"]][reason]+=1
                arms[a][reason]+=1
                if r["unique_number"] in seasonal:sub[reason]+=1
                if key(r)=="287":target[reason]+=1
        def groups(d):
            q={k:dict(v) for k,v in d.items() if v["SE"]>0}
            return {"tested_groups":len(d),"SE_fingerprint_groups":len(q),
                "all_tested_cells_SE":sum(x["SE"]==sum(x.values()) for x in q.values()),
                "mixed_groups":sum(x["SE"]!=sum(x.values()) for x in q.values())}
        totals=sum(arms.values(),Counter())
        result[e]={"all_cells":len(rows)*3,"eligible_numeric_cells":sum(totals[k] for k in ("SD","SE","neither","ambiguous")),
            "counts":dict(totals),"arms":{k:dict(v) for k,v in arms.items()},"tolerance_sensitivity":{k:dict(v) for k,v in tolerances.items()},
            "study_groups":groups(studies),"publication_groups":groups(pubs),"seasonal_pair_cells":dict(sub),"collinsia_control":dict(target),
            "by_supplementation_level":{k:dict(v) for k,v in levels.items()},"flagged_cells":matches,
            "flagged_publication_summary":[{"doi":k,"counts":dict(v)} for k,v in sorted(pubs.items(),key=lambda kv:(-kv[1]["SE"],kv[0])) if v["SE"]>0]}
    return result
def trifolium(rows):
    by={r["unique_number"]:r for r in rows};out={}
    for sp,ids in (("Trifolium_dasyphyllum",("2192","2193")),("Trifolium_parryi",("2194","2195"))):
        z={"status":"HOLD","row_ids":list(ids)};out[sp]=z
        arms=[]
        for rid,phase,ns in zip(ids,("Early_season","Late_season"),((15,12),(5,4))):
            r=by[rid]
            if (c.doi(r["DOI"]),r["unique_study_number"],r["Species_Author"],r["population"],r["year_of_study"],r[c.NOTE],r["Level_of_Supplementation"],r["Emasculated_treatment"])!=("10.1890/11-1271.1","1139",sp,"1","2007",phase,"inflorescense","no"):
                z["error"]="PINNED_CONTEXT_MISMATCH";break
            a=c.endpoint(r,"SPFL")
            actual=[a[x]["n"] for x in ("Natural","Sup")]
            z.setdefault("n_check",[]).append({"phase":phase,"expected_plant_n":list(ns),"compiled_n":actual})
            if actual!=list(ns):
                z["error"]="SOURCE_PLANT_N_MISMATCH";break
            if not all(c.good_mean(x["mean"]) for x in a.values()):
                z["error"]="NONPOSITIVE_MEANS";break
            arms.append(a)
        if len(arms)==2:
            e,l=arms;le=math.log(e["Sup"]["mean"]/e["Natural"]["mean"]);ll=math.log(l["Sup"]["mean"]/l["Natural"]["mean"])
            z.update(status="SECONDARY_COMPILED_POINT_ONLY",early=e,late=l,early_lnRR=le,late_lnRR=ll,late_minus_early_lnRR=ll-le,
                variance="HOLD_SD_SEMANTICS_AND_DEPENDENCE",claim="Conditional on GloPL mapping Sup to source hand-pollinated arm; natural timing cohorts; caging protocol not fully verified.")
    return out
def appendix(s):
    out={}
    for aid in (3553698,3553701,3553704):
        d=out[str(aid)]={}
        try:
            meta=json.loads(fetch(s,f"https://api.figshare.com/v2/articles/{aid}",cap=800000))
            if meta.get("id")!=aid:raise Hold("FIGSHARE_ID")
            d.update(status="METADATA_ONLY",doi=meta.get("doi"),license=meta.get("license"),files=[{k:f.get(k) for k in ("id","name","size","computed_md5","supplied_md5","downloadUrl")} for f in meta.get("files",[])])
            if aid!=3553698:continue
            d["file_checks"]=[]
            for f in meta.get("files",[]):
                item={"name":f.get("name")};d["file_checks"].append(item)
                u=f.get("downloadUrl","");p=urlparse(u)
                if p.scheme!="https" or not (p.hostname=="figshare.com" or (p.hostname or "").endswith(".figshare.com")):raise Hold("UNEXPECTED_SOURCE_HOST")
                size=f.get("size");md5=f.get("computed_md5") or f.get("supplied_md5")
                if not isinstance(size,int) or not md5 or size>2_000_000:raise Hold("NO_BOUNDED_CHECKSUM")
                b=fetch(s,u,cap=2_000_000)
                if len(b)!=size or hashlib.md5(b).hexdigest()!=md5:raise Hold("FILE_INTEGRITY")
                item.update(status="ORIGINAL_BYTES_VERIFIED",bytes=size,sha256=hashlib.sha256(b).hexdigest())
                name=f["name"].lower();tables=[]
                if name.endswith((".html",".htm")):
                    soup=BeautifulSoup(b,"html.parser")
                    tables=[[[cell.get_text(" ",strip=True) for cell in tr.find_all(["th","td"],recursive=False)] for tr in t.find_all("tr")] for t in soup.find_all("table")]
                elif name.endswith(".docx"):
                    with zipfile.ZipFile(io.BytesIO(b)) as z:
                        if sum(x.file_size for x in z.infolist())>8_000_000:raise Hold("DOCX_EXPANSION")
                        root=ET.fromstring(z.read("word/document.xml"))
                    ns={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
                    tables=[[[" ".join(x.text or "" for x in cell.findall(".//w:t",ns)) for cell in tr.findall("w:tc",ns)] for tr in t.findall("w:tr",ns)] for t in root.findall(".//w:tbl",ns)]
                else:
                    item["parse_status"]="FORMAT_HOLD";continue
                # Report table shape and short numeric/statistical labels only;
                # do not redistribute appendix text.
                item["table_shapes"]=[{"rows":len(t),"widths":dict(Counter(len(r) for r in t))} for t in tables]
                item["numeric_rows"]=[{"table":i+1,"row":j+1,"term":re.sub(r"\s+"," ",r[0])[:65],"cells":[v for v in r[1:] if re.fullmatch(r"[<>=]?\s*[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?(?:\s*,\s*\d+)?",v.strip())]} for i,t in enumerate(tables) for j,r in enumerate(t) if r and len(r)>1 and re.search(r"pollin|flower|species|treatment|time|error|density|seed|block",r[0],re.I) and any(re.search(r"\d",v) for v in r[1:])]
                item["parse_status"]="STRUCTURE_AND_SELECTED_STATISTICS_ONLY"
        except (Hold,ValueError,requests.RequestException,KeyError,zipfile.BadZipFile,ET.ParseError) as e:d.update(error=str(e) if isinstance(e,Hold) else type(e).__name__)
    return out
def self_test():
    assert label(.05,.5,100,.0002)=="SE"
    assert label(.5,.5,100,.0002)=="SD"
    assert label(.1,.5,100,.0002)=="neither"
    print("SYNTHETIC_FINGERPRINT_CHECKS_PASS",flush=True)
if __name__=="__main__":
    self_test()
    inv=json.loads(Path("data/payoff_b_glopl_seasonal_inventory_initial_20261125.json").read_text())
    with requests.Session() as s:
        rr=source(fetch(s,c.GLOPL_URL,cap=6_000_000))
        d={"status":"SOURCE_UNCERTAINTY_AUDIT_AND_SECONDARY_TRIFOLIUM_GATE","source_sha256":c.SHA,"source_rows":len(rr),
           "fingerprint":audit(rr,inv),"trifolium":trifolium(rr),"figshare":appendix(s),"primary_theta_added":0}
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=True)+"\n")
    # omit per-cell flags in logs, retain exact IDs in aggregate receipt
    compact={**d,"fingerprint":{e:{k:v for k,v in x.items() if k!="flagged_cells"} for e,x in d["fingerprint"].items()}}
    print(json.dumps(compact,ensure_ascii=True,separators=(",",":")),flush=True)
