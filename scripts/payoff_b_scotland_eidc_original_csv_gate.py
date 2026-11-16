"""UKCEH/EIDC same-original-file provenance and row-level source admission.

Anonymous access only. Use official RO-Crate paths from the public support
archive, not guessed unrestricted third-party mirrors. A successful HTML HEAD
or redirect to login is NOT evidence the CSV is available. Never bypass
licence acceptance or authentication.
"""
import argparse
import csv
import hashlib
import io
import json
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

from scripts.payoff_b_scotland_resource_source_probe import EIDC_ID, open_url

BASE=f"https://catalogue.ceh.ac.uk/datastore/eidchub/{EIDC_ID}/"
SUPPORT=f"https://data-package.ceh.ac.uk/sd/{EIDC_ID}.zip"
MAX_DATA_BYTES=12_000_000


def get_support():
    result=open_url(SUPPORT,max_read=3_000_000)
    raw=result.get("body")
    if not raw or result.get("http_status")!=200:
        raise ValueError("Public EIDC support docs unavailable")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        crate=json.loads(z.read("ro-crate-metadata.json"))
        doc=z.read("supporting-documents/datadescription.docx")
    entries=[]
    for x in crate.get("@graph",[]):
        if "File" in str(x.get("@type","")) and str(x.get("@id","")).startswith("data/"):
            entries.append({"path":x["@id"],"bytes":x.get("bytes"),"format":x.get("encodingFormat")})
    # DOCX read only: original textual field definitions, no layout modification
    with zipfile.ZipFile(io.BytesIO(doc)) as z:
        xml=z.read("word/document.xml")
    root=ET.fromstring(xml)
    namespace={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs=[]
    for p in root.findall(".//w:p",namespace):
        txt="".join(t.text or "" for t in p.findall(".//w:t",namespace)).strip()
        if txt:
            paragraphs.append(txt)
    return entries,{"sha256":hashlib.sha256(doc).hexdigest(),
                    "paragraphs":paragraphs[:170],
                    "text_length":sum(len(p) for p in paragraphs)}


def original_csv(path,expected_bytes):
    url=BASE+path
    head=open_url(url,method="HEAD",timeout=25)
    out={"path":path,"url":url,"expected_bytes":expected_bytes,"head":head}
    if head.get("http_status")!=200:
        out["admission"]="NOT_PUBLICLY_ACCESSIBLE_OR_HEAD_BLOCKED"
        return out
    ctype=(head.get("content_type") or "").lower()
    if "html" in ctype:
        out["admission"]="HTML_NOT_SOURCE_DATA"
        return out
    if expected_bytes is None or not isinstance(expected_bytes,int) or expected_bytes>MAX_DATA_BYTES:
        out["admission"]="NO_EXACT_ROCRATE_SIZE_OR_TOO_LARGE"
        return out
    received=open_url(url,max_read=MAX_DATA_BYTES,timeout=70)
    raw=received.get("body")
    if not raw or received.get("http_status")!=200:
        out["admission"]="DOWNLOAD_NOT_AUTHORIZED_OR_UNAVAILABLE"
        out["get_status"]=received.get("http_status")
        return out
    if len(raw)!=expected_bytes:
        out["admission"]="BYTE_MISMATCH_FAIL_CLOSED"
        out["bytes_received"]=len(raw)
        return out
    if raw[:50].lstrip().lower().startswith((b"<html",b"<!doctype")):
        out["admission"]="HTML_NOT_SOURCE_DATA"
        return out
    h=hashlib.sha256(raw).hexdigest()
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig",errors="replace"),newline=""))
    columns=reader.fieldnames or []
    counts=Counter()
    n=0
    for row in reader:
        n+=1
        for key in ("site","Site","year","Year"):
            if key in columns:
                counts[(key,str(row.get(key)))] += 1
    out.update({"admission":"ORIGINAL_BYTE_SIZE_AND_CSV_SCHEMA_PASSED",
                "sha256":h,"original_bytes":len(raw),
                "n_rows":n,"columns":columns,
                "possible_sites":[k[1] for k in counts if k[0].lower()=="site"][:60],
                "possible_years":sorted({k[1] for k in counts if k[0].lower()=="year"})[:60],
                "bird_or_prey_outcome_effect_fitted":False})
    return out


def audit():
    entries,documentation=get_support()
    parsed={x["path"]:original_csv(x["path"],x["bytes"])
            for x in entries}
    all_readable=all(x["admission"]=="ORIGINAL_BYTE_SIZE_AND_CSV_SCHEMA_PASSED"
                     for name,x in parsed.items()
                     if name in ("data/bird_phenology.csv","data/nestlings.csv","data/branch_beating.csv"))
    return {
        "status":"PAYOFF_B_SCOTLAND_EIDC_ORIGINAL_CSV_ADMISSION",
        "source_doi":"10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3",
        "official_rocrate_paths":entries,
        "documentation":documentation,
        "files":parsed,
        "core_triplet_original_csv_admitted":all_readable,
        "joint_site_year_nest_id_verified":False,
        "source_permissions_bypassed":False,
        "fitness_effect_fitted":False,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    x=audit()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(x,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
