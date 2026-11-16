"""Original Zenodo 17521558 Little Owl actual provisioning source-admission.

Not a new ecological effect: published Sailas et al. (2026) already modeled
habitat and weather effects. Only record official data schemas, checksum and
source identifiers. No synthetic effects, no inferred prey or fitness.
"""
import argparse
import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path
from collections import Counter
from openpyxl import load_workbook

from scripts.payoff_b_scotland_resource_source_probe import open_url

RECORD_ID=17521558
API=f"https://zenodo.org/api/records/{RECORD_ID}"
MAX_FILE_BYTES=38_000_000
MAX_TOTAL_BYTES=55_000_000
MAX_MEMBER_BYTES=30_000_000
MAX_MEMBERS=100
MAX_ROWS=180_000
SOURCE_EXT=(".csv",".tsv",".xlsx",".zip",".txt",".md",".r",".rds")

def verify(raw, expected):
    if not expected or ":" not in expected:
        return {"verified":False,"failure":"NO_OFFICIAL_CHECKSUM"}
    alg,hexval=expected.split(":",1)
    if alg not in ("md5","sha256"):
        return {"verified":False,"failure":"UNKNOWN_OFFICIAL_CHECKSUM"}
    got=hashlib.new(alg,raw).hexdigest()
    return {"verified":got.lower()==hexval.lower(),"algorithm":alg,
            "original":hexval.lower(),"calculated":got}

def summarise_csv(raw, name):
    # UTF-8 followed by CP1252 for plain source tables; never OCR.
    try:
        txt=raw.decode("utf-8-sig")
        encoding="utf-8-sig"
    except UnicodeDecodeError:
        txt=raw.decode("cp1252")
        encoding="cp1252"
    first=txt[:500].splitlines()[0] if txt else ""
    delim="\t" if name.lower().endswith(".tsv") or first.count("\t")>first.count(",") else ","
    rdr=csv.DictReader(io.StringIO(txt,newline=""),delimiter=delim)
    heads=rdr.fieldnames or []
    preview=[]
    nn=0
    cols=Counter()
    for row in rdr:
        nn+=1
        if nn<=3:
            preview.append({h:(row.get(h) or "")[:90] for h in heads[:32]})
        if nn>=MAX_ROWS:
            break
    return {"format":"table","encoding":encoding,"n_rows_scanned":nn,
            "row_limit":MAX_ROWS,"n_columns":len(heads),"columns":heads,
            "preview":preview,"delimiter":delim}

def summarise_xlsx(raw):
    wb=load_workbook(io.BytesIO(raw),read_only=True,data_only=True)
    tabs=[]
    for ws in wb.worksheets:
        first=[]
        for row in ws.iter_rows(min_row=1,max_row=4,values_only=True):
            first.append([str(v)[:70] if v is not None else ""
                        for v in row[:55]])
        tabs.append({"sheet":ws.title,"max_row":ws.max_row,
                     "max_column":ws.max_column,"preview":first})
    wb.close()
    return {"format":"xlsx","sheets":tabs}

def inspect(raw,name):
    name=name.lower()
    if name.endswith((".csv",".tsv")):
        return summarise_csv(raw,name)
    if name.endswith(".xlsx"):
        return summarise_xlsx(raw)
    if name.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            members=[]
            info=archive.infolist()
            if len(info)>MAX_MEMBERS:
                return {"format":"zip","status":"EXCESSIVE_MEMBERS_STOP",
                        "n_members":len(info)}
            for x in info:
                item={"name":x.filename,"bytes":x.file_size}
                if x.file_size>MAX_MEMBER_BYTES:
                    item["status"]="SKIP_MEMBER_TOO_LARGE"
                elif x.filename.lower().endswith((".csv",".tsv",".xlsx")):
                    raw_member=archive.read(x)
                    item["content_sha256"]=hashlib.sha256(raw_member).hexdigest()
                    item["schema"]=inspect(raw_member,x.filename)
                members.append(item)
        return {"format":"zip","n_members":len(members),"members":members}
    if name.endswith((".md",".txt",".r")):
        return {"format":"text","first_3000_chars":raw.decode(
            "utf-8",errors="replace")[:3000]}
    return {"format":"not_inspected"}

def audit():
    response=open_url(API,max_read=2_000_000,timeout=50)
    body=response.get("body")
    out={"status":"PAYOFF_B_LITTLE_OWL_ZENODO_SOURCE_SCHEMA_GATE",
         "doi_expected":"10.5281/zenodo.17521558",
         "official_api":API,
         "no_novel_ecological_effect_fitted":True,
         "record_http_status":response.get("http_status"),
         "downloaded_original_bytes":0}
    if response.get("http_status")!=200 or not body:
        out["gate"]="NO_GO_ZENODO_API"
        return out
    out["metadata_sha256"]=hashlib.sha256(body).hexdigest()
    meta=json.loads(body)
    out["record_title"]=meta.get("metadata",{}).get("title")
    out["record_doi"]=meta.get("doi")
    out["record_date"]=meta.get("metadata",{}).get("publication_date")
    out["record_license"]=meta.get("metadata",{}).get("license")
    out["files"]=[]
    budget=MAX_TOTAL_BYTES
    for f in meta.get("files",[]):
        key=f.get("key") or ""
        size=f.get("size")
        url=f.get("links",{}).get("self")
        item={"key":key,"size":size,"source_checksum":f.get("checksum"),
              "source_file_url":url}
        if not url or not isinstance(size,int) or size<=0 or size>MAX_FILE_BYTES or size>budget or not key.lower().endswith(SOURCE_EXT):
            item["status"]="METADATA_ONLY_SIZE_OR_FORMAT_OR_LINK"
            out["files"].append(item)
            continue
        r=open_url(url,max_read=size,timeout=90)
        raw=r.get("body")
        item["http_status"]=r.get("http_status")
        if not raw or r.get("http_status")!=200:
            item["status"]="SOURCE_UNAVAILABLE"
        elif len(raw)!=size:
            item["status"]="SIZE_MISMATCH"
        else:
            check=verify(raw,f.get("checksum"))
            item["original_sha256"]=hashlib.sha256(raw).hexdigest()
            item["checksum_verification"]=check
            if not check["verified"]:
                item["status"]="CHECKSUM_FAILURE_STOP"
            else:
                item["status"]="SOURCE_VERIFIED"
                item["source_schema"]=inspect(raw,key)
                budget-=len(raw)
                out["downloaded_original_bytes"]+=len(raw)
        out["files"].append(item)
    out["gate"]="SOURCE_ORIGINAL_SCHEMA_ADMITTED" if any(
        f["status"]=="SOURCE_VERIFIED" and f.get("source_schema",{}).get("format") in ("table","xlsx","zip")
        for f in out["files"]) else "HOLD_NO_VERIFIED_PROVISIONING_TABLE"
    out["prey_to_fitness_join_made"]=False
    out["prey_delivered_is_not_source_population_prey_stock"]=True
    out["not_independent_of_sailas_2026"]=True
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    o=audit()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(o,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(o,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
