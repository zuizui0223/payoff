#!/usr/bin/env python3
"""Figshare original red-knot 6/12/24 h feeding experiment source-only audit.

Provider REST API and small public original files only. Emit file identity,
SHA256, original non-sensitive variable *names*, row counts and categorical
cardinalities — never bird identity, aviary identifiers, telemetry or rows.
No original biological coefficient or inferred treatment effect is fitted.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import urlparse
import requests

BASE="https://api.figshare.com/v2"
ARTICLE=28660718
MAX_FILE=8*1024*1024
MAX_EXTRACT=8*1024*1024
MAX_JSON=2*1024*1024
MAX_FILES=15
TIMEOUT=(12,45)
TABULAR=(".csv",".tsv",".txt",".json")
SMALL_SCRIPT=(".r",".rmd")
EXCLUDED=(".pdf",".doc",".docx",".jpg",".jpeg",".png",".tif",".tiff")

CANDIDATE={
  "individual":re.compile(r"(?i)(?:bird|individual|animal|ring|band|^id$|^tag.?id$)"),
  "aviary":re.compile(r"(?i)(?:aviary|cage|enclosure|pen|housing|group)"),
  "treatment":re.compile(r"(?i)(?:food|feed|treat|access|regime|hours)"),
  "year":re.compile(r"(?i)(?:year|season|cohort)"),
  "departure":re.compile(r"(?i)(?:depart|migrat|takeoff|release|censor|surviv|detect)"),
  "physiology":re.compile(r"(?i)(?:mass|weight|plumage|moult|molt|tarsus|gain|slope|rate)"),
}

class Hold(RuntimeError):pass


def fetch_small(session,url,limit=MAX_JSON):
    r=session.get(url,timeout=TIMEOUT,stream=True)
    try:
        if r.status_code!=200:
            raise Hold(f"OFFICIAL_PROVIDER_HTTP_{r.status_code}")
        if int(r.headers.get("Content-Length","0") or 0)>limit:
            raise Hold("PROVIDER_DECLARED_RESPONSE_TOO_LARGE")
        data=bytearray()
        for chunk in r.iter_content(65536):
            data.extend(chunk)
            if len(data)>limit:
                raise Hold("PROVIDER_STREAM_EXCEEDS_BYTE_CAP")
        return bytes(data)
    finally:r.close()


def official_provider(url,fileid):
    p=urlparse(str(url))
    return (p.scheme=="https" and p.hostname in {
        "figshare.com","ndownloader.figshare.com"
    } and (p.path.endswith(f"/files/{fileid}")
      or p.path.endswith(f"/files/{fileid}/")))


def original_file_metadata(obj):
    if not isinstance(obj,dict):
        raise ValueError("Unexpected original Figshare article object")
    files=obj.get("files")
    if not isinstance(files,list):
        raise ValueError("Original Figshare paper has no file listing")
    out=[]
    seen=set()
    for f in files:
        fileid=f.get("id")
        name=f.get("name")
        size=f.get("size")
        if not isinstance(fileid,int) or not isinstance(name,str) or not isinstance(size,int):
            raise ValueError("Original Figshare filename/id/size missing")
        if fileid in seen:
            raise ValueError("Duplicate Figshare file identifier")
        seen.add(fileid)
        out.append({
            "provider_file_id":fileid,
            "original_name":name,
            "source_size_bytes":size,
            "source_MD5_reported_not_SHA256":f.get("supplied_md5") or f.get("computed_md5"),
            "original_official_download_url":f.get("download_url"),
        })
    return out


def schema(raw,name):
    lower=name.lower()
    try:text=raw.decode("utf-8-sig")
    except UnicodeDecodeError:text=raw.decode("cp1252")
    if lower.endswith(".json"):
        obj=json.loads(text)
        if not isinstance(obj,list) or not obj or not isinstance(obj[0],dict):
            raise ValueError("No flat JSON table")
        columns=list(obj[0])
        records=obj
    else:
        h=text[:14000]
        delimiter="\t" if lower.endswith(".tsv") else ","
        if lower.endswith(".txt") or (lower.endswith(".csv") and ";" in h.splitlines()[0] and "," not in h.splitlines()[0]):
            try:delimiter=csv.Sniffer().sniff(h,delimiters=",;\t").delimiter
            except csv.Error:raise ValueError("No source tabular delimiter")
        table=csv.DictReader(io.StringIO(text),delimiter=delimiter)
        columns=table.fieldnames
        if not columns or len(columns)>250 or len(columns)<2:
            raise ValueError("Source table lacks structured columns")
        records=list(table)
    if len(records)>100000 or not records:
        raise ValueError("No records or source row count exceeds bound")
    candidates={key:[c for c in columns if matcher.search(c)] for key,matcher in CANDIDATE.items()}
    # Cardinalities, never categorical raw values or original identifiers.
    grouped={}
    for key,fields in candidates.items():
        grouped[key]={}
        for c in fields[:8]:
            values=[str(r.get(c,"")) for r in records]
            present=[v for v in values if v.strip() not in ("","NA","NaN","nan","null")]
            grouped[key][c]={
                "n_nonmissing":len(present),
                "n_unique_nonmissing":len(set(present)),
                "original_values_exported":False,
            }
    return {
        "original_tabular_file":Path(name).name,
        "n_original_rows":len(records),
        "n_original_columns":len(columns),
        "original_column_names":columns,
        "field_roles_by_name_only":candidates,
        "candidate_field_aggregate_cardinality":grouped,
        "individual_aviary_year_treatment_join_proven":False,
        "post_release_departure_outcome_real_not_censored_proven":False,
    }


def inspect_zip(raw,filename):
    out={"archive_source_filename":filename,"members":[],"source_table_schemas":[]}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if len(z.infolist())>100:
            raise Hold("ORIGINAL_ARCHIVE_HAS_OVER_100_MEMBERS")
        for info in z.infolist():
            ext=Path(info.filename).suffix.lower()
            out["members"].append({
                "original_member_name":info.filename,
                "source_uncompressed_size":info.file_size,
                "extension":ext,
                "original_record_bytes_emitted":False,
            })
            if info.is_dir() or info.file_size>MAX_EXTRACT or ext not in TABULAR:
                continue
            with z.open(info) as f:
                body=f.read(MAX_EXTRACT+1)
            if len(body)>MAX_EXTRACT:
                continue
            try:
                out["source_table_schemas"].append(schema(body,info.filename))
            except (ValueError,UnicodeError,json.JSONDecodeError,csv.Error):
                continue
    return out


def audit(session)->dict:
    result={
        "as_of":"2026-11-20",
        "source":"Lameris et al 2025 Functional Ecology DOI 10.1111/1365-2435.70183",
        "original_dataset_DOI":"10.6084/m9.figshare.28660718",
        "source_original_Figshare_article_id":ARTICLE,
        "original_published_result_prior_art":"Randomized food access 6,12,24 h affected mass deposition and tracked migration departure",
        "treatment_unit_is_original_aviary_not_each_measurement":True,
        "source_data_access_status":"NOT_RUN",
        "original_source_metadata":{},
        "original_file_audits":[],
        "raw_bird_aviary_IDs_or_coordinate_values_exported":False,
        "new_biological_effect_fitted":False,
        "original_bird_cue_reliability_q_measured":False,
        "information_deadline_or_interactor_payoff_identified":False,
        "source_individual_aviary_year_departure_join_confirmed":False
    }
    try:
        obj=json.loads(fetch_small(session,f"{BASE}/articles/{ARTICLE}"))
        files=original_file_metadata(obj)
        result["original_source_metadata"]={
            "article_title":obj.get("title"),
            "provider_DOI":obj.get("doi"),
            "published_date":obj.get("published_date"),
            "version":obj.get("version"),
            "license":obj.get("license"),
            "n_original_filenames":len(files),
        }
        accepted=0
        for f in files:
            row={k:v for k,v in f.items() if k!="original_official_download_url"}
            suffix=Path(f["original_name"]).suffix.lower()
            if (accepted>=MAX_FILES or f["source_size_bytes"]<=0
                    or f["source_size_bytes"]>MAX_FILE
                    or suffix in EXCLUDED or suffix not in TABULAR+SMALL_SCRIPT+(".zip",)):
                row["source_status"]="SKIPPED_FORMAT_SIZE_OR_COUNT"
                result["original_file_audits"].append(row)
                continue
            if not official_provider(f["original_official_download_url"],f["provider_file_id"]):
                row["source_status"]="SOURCE_OFFICIAL_URL_UNVERIFIED"
                result["original_file_audits"].append(row)
                continue
            accepted+=1
            try:
                raw=fetch_small(session,f["original_official_download_url"],MAX_FILE)
                row["source_status"]="ORIGINAL_PUBLIC_BYTES_ACQUIRED"
                row["actual_original_bytes_sha256"]=hashlib.sha256(raw).hexdigest()
                row["n_downloaded_bytes"]=len(raw)
                m=f["source_MD5_reported_not_SHA256"]
                if m and len(m)==32:
                    if hashlib.md5(raw).hexdigest().lower()!=m.lower():
                        raise ValueError("Original Figshare MD5 mismatch")
                    row["provider_MD5_verified"]=True
                else:row["provider_MD5_verified"]=False
                if suffix==".zip":
                    row["zip_member_audit"]=inspect_zip(raw,f["original_name"])
                elif suffix in TABULAR:
                    try:row["source_table_schema"]=schema(raw,f["original_name"])
                    except (ValueError,UnicodeError,csv.Error,json.JSONDecodeError):
                        row["source_status"]="PUBLIC_FILE_READ_NO_FLAT_SOURCE_SCHEMA"
                else:
                    # Source script existence not repeated in response; no R code reproduced.
                    row["source_script_metadata_only"]={"size_bytes":len(raw),"original_lines":len(raw.splitlines())}
            except (Hold,requests.RequestException,ValueError,zipfile.BadZipFile) as error:
                row["source_status"]="ORIGINAL_PUBLIC_BYTES_OR_SCHEMA_HOLD"
                row["source_hold_type"]=type(error).__name__
                row["source_hold_reason"]=str(error)[:160]
            result["original_file_audits"].append(row)
        flat=sum("source_table_schema" in r for r in result["original_file_audits"])
        zipped=sum(len(r.get("zip_member_audit",{}).get("source_table_schemas",[]))
                   for r in result["original_file_audits"])
        result["n_original_plain_or_archived_tabular_schemas"]=flat+zipped
        result["source_data_access_status"]=(
            "ORIGINAL_TABULAR_SCHEMA_FOUND_TREATMENT_AVIARY_OUTCOME_JOIN_NOT_VERIFIED"
            if flat+zipped else "PUBLISHED_FILES_AUDITED_NO_ADMITTED_SOURCE_TABLE"
        )
    except (Hold,requests.RequestException,json.JSONDecodeError,ValueError) as error:
        result["source_data_access_status"]="ORIGINAL_FIGSHARE_METADATA_ACCESS_HOLD"
        result["source_hold_reason"]=str(error)[:200]
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    result=audit(requests.Session())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
      "source_status":result["source_data_access_status"],
      "n_source_files":result["original_source_metadata"].get("n_original_filenames"),
      "n_source_table_schemas":result.get("n_original_plain_or_archived_tabular_schemas"),
      "files":[{"name":f["original_name"],"bytes":f["source_size_bytes"],
                "status":f["source_status"],
                "tabular_rows":f.get("source_table_schema",{}).get("n_original_rows"),
                "zip_members":[x["original_member_name"]
                               for x in f.get("zip_member_audit",{}).get("members",[])]
                } for f in result["original_file_audits"]],
      "no_new_biological_fit":True,
    },ensure_ascii=False))


if __name__=="__main__":
    main()
