"""Bounded official Dryad Seress 2020 original supplementary study preflight.

No biological effect fitted; metadata/file checks only. Use official public
Dryad API (GET only), with no credentials or license bypass. Published
dataset DOI 10.5061/dryad.qbzkh18dj.
"""
import argparse
import hashlib
import io
import json
import re
import urllib.parse
from pathlib import Path
import openpyxl

from scripts.payoff_b_scotland_resource_source_probe import open_url

DOI="10.5061/dryad.qbzkh18dj"
DOI_ARG=urllib.parse.quote("doi:"+DOI,safe="")
ROOT=f"https://datadryad.org/api/v2/datasets/{DOI_ARG}"
MAX_META_BYTES=1_500_000
MAX_FILE_BYTES=7_000_000
MAX_TOTAL_BYTES=16_000_000


def json_source(url):
    out=open_url(url,max_read=MAX_META_BYTES,timeout=45)
    raw=out.get("body")
    if out.get("http_status")!=200 or not raw:
        return None,{"status":"SOURCE_UNAVAILABLE",**{k:v for k,v in out.items() if k!="body"}}
    try:
        obj=json.loads(raw)
    except json.JSONDecodeError:
        return None,{"status":"NON_JSON_RESPONSE","url":url}
    return obj,{"status":"JSON_READ","url":url,
                "sha256":hashlib.sha256(raw).hexdigest(),
                "byte_length":len(raw)}


def embedded_nodes(obj,name):
    """Return list nodes from a Dryad HAL collection, never guess records."""
    if not isinstance(obj,dict):
        return []
    embedded=obj.get("_embedded",{})
    if not isinstance(embedded,dict):
        return []
    items=embedded.get(name)
    if isinstance(items,list):
        return [r for r in items if isinstance(r,dict)]
    for k,v in embedded.items():
        if (k.split(":")[-1] == name.split(":")[-1]
            and isinstance(v,list)):
            return [r for r in v if isinstance(r,dict)]
    return []


def version_ids_from_listing(payload):
    """Only structured version IDs, not unrelated numeric strings."""
    vals=[]
    if isinstance(payload,list):
        options=payload
    elif isinstance(payload,dict):
        options=embedded_nodes(payload,"stash:versions")
        # Dryad may return a single version object rather than a HAL page.
        if not options and payload.get("versionNumber") is not None and payload.get("id") is not None:
            options=[payload]
        if not options and isinstance(payload.get("versions"),list):
            options=payload["versions"]
    else:
        options=[]
    for obj in options:
        value=obj.get("id")
        # Dryad published HAL version objects expose IDs in canonical self href,
        # not as an id property. Only match the exact documented API path.
        if value is None:
            href=obj.get("_links",{}).get("self",{}).get("href","")
            found=re.fullmatch(r"(?:https://datadryad.org)?/api/v2/versions/(\\d+)",href)
            if found:
                value=int(found.group(1))
        if isinstance(value,int):
            vals.append((value,obj.get("versionNumber"),obj))
        elif isinstance(value,str) and value.isdigit():
            vals.append((int(value),obj.get("versionNumber"),obj))
    return sorted(vals,key=lambda z:z[0])


def file_rows_from_listing(payload):
    if not isinstance(payload,dict):
        return []
    items=embedded_nodes(payload,"stash:files")
    return [{
        "id":f.get("id") if f.get("id") is not None else (
             int(re.fullmatch(r"(?:https://datadryad.org)?/api/v2/files/(\\d+)",
               f.get("_links",{}).get("self",{}).get("href","")).group(1))
             if re.fullmatch(r"(?:https://datadryad.org)?/api/v2/files/(\\d+)",
               f.get("_links",{}).get("self",{}).get("href","")) else None),
        "path":f.get("path") or f.get("fileName") or f.get("filename"),
        "size":f.get("size"),
        "digest":f.get("digest"),
        "digestType":f.get("digestType"),
        "mimeType":f.get("mimeType"),
        "description":f.get("description")
    } for f in items]


def validate_manifest_digest(raw,record):
    name=(record.get("digestType") or "").lower().replace("-","")
    dig=record.get("digest")
    if not dig or name not in ("md5","sha256"):
        return {"verified":False,"reason":"SOURCE_DIGEST_NOT_AVAILABLE_OR_UNKNOWN",
                "digestType":record.get("digestType")}
    got=hashlib.new(name,raw).hexdigest()
    return {"verified":got.lower()==str(dig).lower(),
            "algorithm":name,"expected":str(dig).lower(),"observed":got}


def workbook_schema(raw):
    wb=openpyxl.load_workbook(io.BytesIO(raw),read_only=True,data_only=True)
    sheets=[]
    for ws in wb.worksheets:
        preview=[]
        for row in ws.iter_rows(min_row=1,max_row=5,values_only=True):
            preview.append([str(x)[:150] if x is not None else ""
                            for x in row[:70]])
        sheets.append({
            "sheet":ws.title,
            "max_row":ws.max_row,
            "max_column":ws.max_column,
            "first_five_rows":preview,
        })
    wb.close()
    return sheets


def probe():
    dataset,dreceipt=json_source(ROOT)
    result={
        "status":"PAYOFF_B_FOOD_SUPPLEMENT_ORIGINAL_DRYAD_ACCESS",
        "doi":DOI,
        "dataset_metadata":dreceipt,
        "source_is_external_experiment_not_scotland_replication":True,
        "published_treatment_effect_is_prior_art":True,
        "feeding_or_fitness_coefficient_fitted":False,
    }
    if dataset is None:
        result["gate"]="NO_GO_DATASET_METADATA"
        return result
    result["source_title"]=dataset.get("title")
    result["license"]=dataset.get("license")
    result["dataset_metadata_keys"]=sorted(dataset)
    listing,lrec=json_source(ROOT+"/versions")
    result["version_list_status"]=lrec
    if isinstance(listing,dict):
        result["version_response_shape"]={
            "top_level_keys":sorted(listing),
            "embedded_keys":sorted(listing.get("_embedded",{})) if isinstance(listing.get("_embedded"),dict) else [],
            "link_keys":sorted(listing.get("_links",{})) if isinstance(listing.get("_links"),dict) else [],
            "has_direct_id":listing.get("id") is not None,
            "has_version_number":listing.get("versionNumber") is not None,
        }
    elif isinstance(listing,list):
        result["version_response_shape"]={"array_length":len(listing)}
    candidates=embedded_nodes(listing,"stash:versions") if isinstance(listing,dict) else []
    result["version_node_evidence"]=[{
        "keys":sorted(node),
        "id":node.get("id"),
        "versionNumber":node.get("versionNumber"),
        "link_self":node.get("_links",{}).get("self"),
        "link_files":node.get("_links",{}).get("stash:files")
    } for node in candidates[:3]]
    ids=version_ids_from_listing(listing)
    result["published_version_ids"]=[{"id":i,"number":n} for i,n,o in ids]
    if not ids:
        result["gate"]="NO_GO_VERSION_ID_UNVERIFIED"
        return result
    version_id=ids[-1][0]
    fobj,frec=json_source(f"https://datadryad.org/api/v2/versions/{version_id}/files")
    result["file_list_status"]=frec
    if fobj is None:
        result["gate"]="NO_GO_FILE_MANIFEST"
        return result
    files=file_rows_from_listing(fobj)
    result["file_manifest"]=files
    bytes_total=0
    checked=[]
    for f in files:
        size=f.get("size")
        file_id=f.get("id")
        name=str(f.get("path") or "")
        if not isinstance(file_id,int):
            if isinstance(file_id,str) and file_id.isdigit():
                file_id=int(file_id)
            else:
                continue
        if (not isinstance(size,int) or size<0
                or size>MAX_FILE_BYTES or bytes_total+size>MAX_TOTAL_BYTES):
            checked.append({"name":name,"id":file_id,
                            "status":"SIZE_LIMIT_OR_UNVERIFIED"})
            continue
        if not name.lower().endswith((".xlsx",".xls",".csv",".txt",".md")):
            continue
        url=f"https://datadryad.org/api/v2/files/{file_id}/download"
        reply=open_url(url,max_read=MAX_FILE_BYTES,timeout=50)
        raw=reply.get("body")
        item={"name":name,"id":file_id,"official_download":url,
              "status_code":reply.get("http_status")}
        if not raw or reply.get("http_status")!=200:
            item["status"]="SOURCE_FILE_UNAVAILABLE"
            checked.append(item)
            continue
        if len(raw)!=size:
            item["status"]="MANIFEST_SIZE_MISMATCH"
            item["got_bytes"]=len(raw)
            checked.append(item)
            continue
        item["download_sha256"]=hashlib.sha256(raw).hexdigest()
        item["digest_verification"]=validate_manifest_digest(raw,f)
        if not item["digest_verification"]["verified"]:
            item["status"]="NO_GO_FILE_DIGEST_MISMATCH_OR_ABSENT"
        elif name.lower().endswith(".xlsx"):
            item["status"]="SOURCE_XLSX_VERIFIED_AND_SCHEMA_OPENED"
            item["sheets"]=workbook_schema(raw)
        else:
            item["status"]="SOURCE_FILE_VERIFIED_NO_XLSX_SCHEMA"
            item["text_first_line"]=raw.decode("utf-8-sig",errors="replace").splitlines()[:2]
        bytes_total+=len(raw)
        checked.append(item)
    result["fetched_files"]=checked
    result["bytes_fetched"]=bytes_total
    result["gate"]="SOURCE_SCHEMA_PARTIALLY_ADMITTED" if any(
        x["status"]=="SOURCE_XLSX_VERIFIED_AND_SCHEMA_OPENED" for x in checked
    ) else "HOLD_NO_CERTIFIED_TABULAR_SOURCE"
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    result=probe()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(result,ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
