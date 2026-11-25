#!/usr/bin/env python3
"""Read-only small public Dryad source gate for interaction-buffering candidates.

No outcome fitting. Never bypass an authorization failure or publish raw files.
Official provider file IDs/digests and exact filenames are required. The
workflow exports aggregate provenance and XLSX sheet/header structure only.
"""
from __future__ import annotations
import argparse, hashlib, io, json, re, zipfile
from pathlib import Path
from urllib.parse import quote
import requests
import openpyxl

BASE="https://datadryad.org/api/v2"
CAP=6_000_000
SOURCES={
 "Schenk2018":("10.5061/dryad.rm317",{
  "Activity Index (early vs. late activity).xlsx",
  "Survival rate, Activity Index, brood cells, nests, female offspring, Temp.xlsx"}),
 "Nanke2026":("10.5061/dryad.wm37pvn3g",{"Data_Corydalis.xlsx"}),
 "KudoCooper2019":("10.5061/dryad.q4fm37m",{"Kudo&Cooper_SourceData.xlsx"}),
 "Vazquez2023":("10.5061/dryad.37pvmcvmp",{
  "plants.csv","trampas.csv","emerg.csv","polen_megach_2006.csv",
  "polen_megach_2007.csv","polen_megach_2008.csv"})
}

class Hold(RuntimeError): pass

def fetch(session,url,cap=CAP):
    with session.get(url,stream=True,timeout=(8,18),allow_redirects=True) as r:
        if r.status_code!=200: raise Hold(f"HTTP_{r.status_code}")
        size=r.headers.get("Content-Length")
        if size and int(size)>cap: raise Hold("BODY_LIMIT")
        out=bytearray()
        for b in r.iter_content(65536):
            out.extend(b)
            if len(out)>cap: raise Hold("BODY_LIMIT")
        return bytes(out)

def walk(x):
    if isinstance(x,dict):
        yield x
        for v in x.values(): yield from walk(v)
    elif isinstance(x,list):
        for v in x: yield from walk(v)

def provider_id(x,kind):
    val=x.get("id") or (x.get("versionId") if kind=="versions" else None)
    href=x.get("_links",{}).get("self",{}).get("href","")
    m=re.search(r"/"+kind+r"/(\d+)(?:[/?#]|$)",str(href))
    if m: return int(m.group(1))
    if str(val).isdigit(): return int(val)
    return None

def manifest(session,doi):
    u=BASE+"/datasets/"+quote("doi:"+doi,safe="")
    dataset=json.loads(fetch(session,u))
    ident=str(dataset.get("identifier",""))
    if doi.lower() not in ident.lower(): raise Hold("DOI_MISMATCH")
    vv=json.loads(fetch(session,u+"/versions"))
    candidates={}
    for x in walk(vv):
        if not any(k in x for k in ("versionNumber","versionStatus","versionId")): continue
        vid=provider_id(x,"versions")
        if vid is not None: candidates[vid]=x
    if not candidates: raise Hold("VERSION_ID_UNRESOLVED")
    def rank(k):
        v=candidates[k].get("versionNumber",0)
        return (int(v) if str(v).isdigit() else 0,k)
    vid=max(candidates,key=rank)
    fs=json.loads(fetch(session,f"{BASE}/versions/{vid}/files"))
    records={}
    for x in walk(fs):
        raw=x.get("path") or x.get("filename") or x.get("name")
        fid=provider_id(x,"files")
        if not raw or fid is None: continue
        name=str(raw).split("/")[-1]
        records[name]={
            "file_id":fid,"name":name,"bytes":x.get("size") or x.get("sizeBytes"),
            "digest":x.get("digest") or x.get("md5"),
            "digest_type":x.get("digestType") or ("MD5" if x.get("md5") else None)
        }
    if not records: raise Hold("FILE_LIST_UNRESOLVED")
    return {"doi":doi,"title":dataset.get("title"),"version":vid,
            "license":dataset.get("license"),"files":records}

def verified_bytes(session,record):
    size=record["bytes"]; digest=record["digest"]; algo=record["digest_type"]
    if not isinstance(size,int) or not 0<size<=CAP: raise Hold("SIZE_MISSING_OR_LIMIT")
    if not isinstance(digest,str) or not algo: raise Hold("PROVIDER_DIGEST_MISSING")
    a=str(algo).lower().replace("-","")
    if a not in {"md5","sha1","sha256","sha512"}: raise Hold("DIGEST_ALGORITHM_UNSUPPORTED")
    b=fetch(session,f'{BASE}/files/{record["file_id"]}/download',min(CAP,size+1))
    if len(b)!=size or hashlib.new(a,b).hexdigest().lower()!=digest.lower():
        raise Hold("SIZE_OR_PROVIDER_DIGEST_MISMATCH")
    return b

def inspect_schema(b,name):
    if name.endswith(".xlsx"):
        if not zipfile.is_zipfile(io.BytesIO(b)): raise Hold("NOT_XLSX")
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            if sum(x.file_size for x in z.infolist())>30_000_000:
                raise Hold("XLSX_EXPANSION_LIMIT")
        wb=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)
        try:
            return {"sheets":[{"sheet":s.title,"reported_rows":s.max_row,
               "reported_columns":s.max_column,
               "first_row_text_headers":[str(v)[:120] if isinstance(v,str) else None
                    for v in next(s.iter_rows(min_row=1,max_row=1,values_only=True),())[:100]]}
                  for s in wb.worksheets]}
        finally: wb.close()
    if name.endswith(".csv"):
        import csv
        f=io.StringIO(b.decode("utf-8-sig"))
        r=csv.reader(f)
        header=next(r,[])
        if not header: raise Hold("NO_CSV_HEADER")
        n=sum(1 for row in r if any(v.strip() for v in row))
        return {"header":header[:100],"nonempty_data_rows":n}
    raise Hold("UNSUPPORTED_FILE_TYPE")

def run():
    result={"status":"SOURCE_GATE_ONLY_NO_BIOLOGICAL_FIT","sources":{}}
    with requests.Session() as session:
        session.headers["User-Agent"]="PAYOFF-B academic public-data provenance check"
        for key,(doi,names) in SOURCES.items():
            row={"doi":doi,"status":"HOLD","required_names":sorted(names)}
            result["sources"][key]=row
            try:
                m=manifest(session,doi)
                row["manifest"]=m
                row["files"]={}
                if not names.issubset(m["files"]):
                    row["missing_expected_names"]=sorted(names-set(m["files"]))
                    raise Hold("EXACT_SOURCE_FILENAMES_NOT_ALL_PRESENT")
                for name in sorted(names):
                    rec=m["files"][name]
                    status={"status":"HOLD"}
                    row["files"][name]=status
                    try:
                        b=verified_bytes(session,rec)
                        status.update({"status":"PROVIDER_DIGEST_VERIFIED",
                                       "bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),
                                       "schema":inspect_schema(b,name)})
                    except (Hold,requests.RequestException,ValueError,UnicodeError,zipfile.BadZipFile) as e:
                        status["status"]="HOLD"
                        status["error"]=str(e)[:180] if isinstance(e,Hold) else type(e).__name__
                if all(v["status"]=="PROVIDER_DIGEST_VERIFIED" for v in row["files"].values()):
                    row["status"]="SOURCE_SCHEMA_READY_NOT_OUTCOME_ADMITTED"
            except (Hold,requests.RequestException,ValueError,KeyError) as e:
                row["error"]=str(e)[:180] if isinstance(e,Hold) else type(e).__name__
            print(key,row["status"],row.get("error",""),flush=True)
            for name,status in row.get("files",{}).items():
                print(" ",name,status["status"],status.get("error",""),flush=True)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--output",required=True)
    args=p.parse_args()
    result=run()
    path=Path(args.output); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
