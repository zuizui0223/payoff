#!/usr/bin/env python3
"""Bounded source-only inspection of published amphibian and herbivore datasets."""
import csv,hashlib,io,json,math,re,sys,zipfile
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse
import requests,openpyxl
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold
SOURCES={3984482:"MurilloRincon2017_priority",4239314:"MurilloRincon2017_immune",27679935:"Weir2024_hosts"}
CAP=6_000_000
def schema(b,name):
    if name.lower().endswith(".xlsx"):
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            if sum(x.file_size for x in z.infolist())>30_000_000:raise Hold("EXPANSION")
        w=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
        out=[]
        try:
            for s in w.worksheets:
                rows=list(s.iter_rows(values_only=True))
                h=next((r for r in rows[:15] if sum(isinstance(v,str) and bool(v.strip()) for v in r)>=2),())
                ix=rows.index(h) if h else -1
                design={}
                for j,v in enumerate(h):
                    if not isinstance(v,str) or not re.search(r"(^id$|group|treat|phenol|delay|food|prior|tank|aquari|block|container|family|population|host|plant|replic|surviv|year|clutch|species)",v,re.I):continue
                    if re.search(r"mass|weight|duration|rate|time|date|length|day|count|number|size|surviv|grow",v,re.I) and not re.search(r"^surviv(?:al|ed)?$",v,re.I):continue
                    values=Counter(str(r[j])[:70] for r in rows[ix+1:] if j<len(r) and r[j] is not None)
                    if len(values)<=20:design[v]={"levels":dict(values)}
                    else:design[v]={"distinct":len(values),"nonmissing":sum(values.values())}
                out.append({"sheet":s.title,"rows":len(rows),"columns":s.max_column,"header_row_index_1based":ix+1,"headers":[str(v)[:100] if v is not None else None for v in h],"design_levels_or_counts":design})
        finally:w.close()
        return {"sheets":out}
    if name.lower().endswith(".csv"):
        t=b.decode("utf-8-sig")
        d=csv.Sniffer().sniff(t[:4096],delimiters=",;\t")
        r=csv.DictReader(io.StringIO(t),dialect=d);rows=list(r)
        return {"headers":r.fieldnames,"rows":len(rows)}
    return {"status":"UNINSPECTED_FORMAT"}
def run():
    out={"status":"SOURCE_SCHEMA_ONLY_NO_NEW_EFFECT","sources":{}}
    with requests.Session() as s:
        for aid,study in SOURCES.items():
            a=out["sources"][study]={"article_id":aid,"files":[],"status":"HOLD"}
            try:
                m=json.loads(fetch(s,f"https://api.figshare.com/v2/articles/{aid}",cap=800000))
                if m.get("id")!=aid:raise Hold("ARTICLE_ID_MISMATCH")
                a.update(title=m.get("title"),doi=m.get("doi"),license=m.get("license"),version=m.get("version"))
                if m.get("is_public") is False:raise Hold("NOT_PUBLIC")
                for f in m.get("files",[]):
                    name=f.get("name","");size=f.get("size");md5=f.get("computed_md5") or f.get("supplied_md5");fid=f.get("id")
                    z={"name":name,"bytes":size,"provider_md5":md5,"id":fid,"status":"METADATA_ONLY"};a["files"].append(z)
                    if not name.lower().endswith((".xlsx",".csv")):continue
                    if not isinstance(size,int) or not 0<size<=CAP or not md5 or not isinstance(fid,int):z["status"]="HOLD_UNVERIFIABLE";continue
                    try:
                        b=fetch(s,f"https://api.figshare.com/v2/file/download/{fid}",cap=CAP)
                        if len(b)!=size or hashlib.md5(b).hexdigest()!=md5:raise Hold("SOURCE_BYTES_MISMATCH")
                        z.update(status="PROVIDER_MD5_VERIFIED",sha256=hashlib.sha256(b).hexdigest(),schema=schema(b,name))
                    except (Hold,ValueError,requests.RequestException,zipfile.BadZipFile,csv.Error) as e:z.update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
                a["status"]="SOURCE_METADATA_RETRIEVED"
            except (Hold,ValueError,requests.RequestException,KeyError) as e:a.update(error=str(e) if isinstance(e,Hold) else type(e).__name__)
    return out
if __name__=="__main__":
    d=run();p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+"\n")
    print(json.dumps(d,ensure_ascii=True,separators=(",",":")),flush=True)
