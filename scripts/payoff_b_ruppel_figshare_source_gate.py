#!/usr/bin/env python3
"""Original 2023 Figshare three-decision source *admission*, not an effect fit.

Read published public Figshare collection 6403996 and linked article metadata.
Only bounded, public, provider-named small tabular/ZIP files are inspected.
Only schema names, summary counts, SHA256 and source access statuses emitted.
Never export original animal IDs, GPS, response values or individual tracks.
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

BASE = "https://api.figshare.com/v2"
COLLECTION_ID = 6403996
PUBLISHED_PAPER = "10.1098/rsos.221420"
PUBLISHED_COLLECTION = "10.6084/m9.figshare.c.6403996"
MAX_PUBLIC_BYTES = 8_000_000
MAX_META_BYTES = 2_000_000
MAX_FILES = 12
TIMEOUT = (12, 35)
ACCEPTED_EXT = (".csv", ".tsv", ".txt", ".json", ".zip")
ID_PATTERN = re.compile(r"(?:^id$|bird.?id|individual|tag.?id|deploy.?id|^id_|^bird$)",re.I)
TIME_PATTERN = re.compile(r"date|time|timestamp|sunset|hour|^doy$|day",re.I)
DECISION_PATTERN = re.compile(r"depart|route|landing|land|flight|stopover|takeoff|offshore|onshore",re.I)
WEATHER_PATTERN = re.compile(r"weather|wind|temp|press|cloud|precip|rain|humidity|fog",re.I)


class SourceHold(RuntimeError):
    pass


def _small_json(client:requests.Session,url:str):
    r=client.get(url,timeout=TIMEOUT,stream=True)
    try:
        if r.status_code!=200:
            raise SourceHold(f"ORIGINAL_FIGSHARE_API_HTTP_{r.status_code}")
        size=int(r.headers.get("Content-Length","0") or 0)
        if size>MAX_META_BYTES:
            raise SourceHold("PUBLIC_METADATA_EXCEEDS_SIZE_GUARD")
        data=bytearray()
        for block in r.iter_content(16384):
            data.extend(block)
            if len(data)>MAX_META_BYTES:
                raise SourceHold("PUBLIC_METADATA_BODY_EXCEEDS_SIZE_GUARD")
        return json.loads(data)
    finally:
        r.close()


def _provider_download_url(url:str)->bool:
    try:
        p=urlparse(url)
    except (TypeError,ValueError):
        return False
    return (
        p.scheme=="https"
        and p.hostname in {"figshare.com","ndownloader.figshare.com"}
        and re.search(r"/(?:ndownloader/)?files/\d+(?:/|$)",p.path) is not None
    )


def _small_provider_bytes(client:requests.Session,url:str,declared_size:int)->bytes:
    if not _provider_download_url(url):
        raise SourceHold("FILE_DOWNLOAD_NOT_OFFICIAL_FIGSHARE_URL")
    if not 0 < declared_size <= MAX_PUBLIC_BYTES:
        raise SourceHold("FILE_EXCEEDS_8MB_ADMISSION_BOUND")
    r=client.get(url,timeout=TIMEOUT,stream=True)
    try:
        if r.status_code!=200:
            raise SourceHold(f"FIGSHARE_ORIGINAL_FILE_HTTP_{r.status_code}")
        if int(r.headers.get("Content-Length","0") or 0)>MAX_PUBLIC_BYTES:
            raise SourceHold("FILE_CONTENT_LENGTH_EXCEEDS_BOUND")
        out=bytearray()
        for part in r.iter_content(65536):
            out.extend(part)
            if len(out)>MAX_PUBLIC_BYTES:
                raise SourceHold("FILE_STREAM_EXCEEDS_BOUND")
        return bytes(out)
    finally:
        r.close()


def _delimited_schema(raw:bytes,name:str)->dict:
    if b"\0" in raw[:30000] or len(raw)>MAX_PUBLIC_BYTES:
        raise ValueError("Not a bounded text data file")
    try:
        text=raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text=raw.decode("cp1252")
    if name.lower().endswith(".json"):
        obj=json.loads(text)
        if isinstance(obj,list) and obj and isinstance(obj[0],dict):
            columns=list(obj[0].keys())
            data=obj
        else:
            raise ValueError("JSON file not a flat original source table")
        n=len(data)
        values=lambda col: [row.get(col) for row in data]
    else:
        head=text[:12000]
        delim = "\t" if name.lower().endswith(".tsv") else ","
        if not name.lower().endswith((".csv",".tsv")):
            try:
                delim=csv.Sniffer().sniff(head,delimiters=",;\t").delimiter
            except csv.Error:
                raise ValueError("TXT source has no obvious tabular delimiter")
        elif name.lower().endswith(".csv") and ";" in head.splitlines()[0] and "," not in head.splitlines()[0]:
            delim=";"
        reader=csv.DictReader(io.StringIO(text),delimiter=delim)
        columns=reader.fieldnames
        if columns is None or len(columns)<2 or len(columns)>350:
            raise ValueError("Missing original source field header")
        data=list(reader)
        n=len(data)
        values=lambda col:[row.get(col) for row in data]
    if n==0:
        raise ValueError("Tabular source has no rows")
    if len(columns)>350 or n>250000:
        raise ValueError("Source table exceeds bounded row or column count")
    ids=[c for c in columns if ID_PATTERN.search(c)]
    times=[c for c in columns if TIME_PATTERN.search(c)]
    decisions=[c for c in columns if DECISION_PATTERN.search(c)]
    weather=[c for c in columns if WEATHER_PATTERN.search(c)]
    counts={}
    for col in ids[:5]:
        vals=[str(v) for v in values(col) if v not in ("",None)]
        counts[col]={"n_original_rows_nonblank":len(vals),"n_unique":len(set(vals))}
    return {
        "filename":name.split("/")[-1],
        "n_original_rows":n,
        "columns":columns,
        "candidate_id_columns":ids,
        "candidate_time_columns":times,
        "candidate_decision_columns":decisions,
        "candidate_weather_columns":weather,
        "aggregate_candidate_id_counts":counts,
        "original_same_bird_all_three_decisions_certified":False,
        "individual_time_order_certified":False,
    }


def _tabular_candidates(raw:bytes,name:str)->list[dict]:
    if name.lower().endswith(".zip"):
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                out=[]
                for info in z.infolist():
                    suffix=info.filename.lower()
                    if info.is_dir() or not suffix.endswith((".csv",".tsv",".txt",".json")):
                        continue
                    if info.file_size>MAX_PUBLIC_BYTES or len(out)>=8:
                        continue
                    with z.open(info) as reader:
                        val=reader.read(MAX_PUBLIC_BYTES+1)
                    if len(val)>MAX_PUBLIC_BYTES:
                        continue
                    try:
                        out.append(_delimited_schema(val,info.filename))
                    except (ValueError,UnicodeError,csv.Error,json.JSONDecodeError):
                        pass
                return out
        except (zipfile.BadZipFile,ValueError):
            return []
    try:
        return [_delimited_schema(raw,name)]
    except (ValueError,UnicodeError,csv.Error,json.JSONDecodeError):
        return []


def inspect_public_source(client:requests.Session)->dict:
    receipt={
        "as_of":"2026-11-19",
        "original_article_DOI":PUBLISHED_PAPER,
        "original_figshare_collection_DOI":PUBLISHED_COLLECTION,
        "original_figshare_collection_id":COLLECTION_ID,
        "source_claim_already_published":"Weather effects on coastal stopover departure, routing and landing in 2023",
        "new_biological_response_fitted":False,
        "original_bird_identifiers_exported":False,
        "original_full_animal_tracks_exported":False,
        "raw_eBird_records_used":False,
        "natural_q_wait_D_eff_and_r_t_identified":False,
        "figshare_public_collection_api_admitted":False,
        "source_status":"NOT_RUN",
        "source_assessment":{
            "matching_individual_ids_across_all_three_decisions":False,
            "independent_precue_weather_timestamps_verified":False,
            "minimum_30_original_birds_linked":False,
            "minimum_10_landing_individuals_verified":False
        },
    }
    try:
        collection=_small_json(client,f"{BASE}/collections/{COLLECTION_ID}/articles")
        if not isinstance(collection,list):
            raise SourceHold("FIGSHARE_COLLECTION_ARTICLE_LIST_UNEXPECTED_FORMAT")
        ids=[int(v["id"]) for v in collection if isinstance(v,dict)
             and str(v.get("id","")).isdigit()]
        if not ids or len(ids)>30:
            raise SourceHold("FIGSHARE_COLLECTION_ORIGINAL_ARTICLES_NOT_RESOLVED")
        receipt["figshare_public_collection_api_admitted"]=True
        receipt["n_original_linked_article_records"]=len(ids)
        receipt["article_metadata"]=[]
        receipt["aggregate_tabular_source_schemas"]=[]
        candidate_count=0
        for article_id in ids:
            meta=_small_json(client,f"{BASE}/articles/{article_id}")
            files=meta.get("files",[])
            if not isinstance(files,list):
                raise SourceHold("FIGSHARE_ORIGINAL_ARTICLE_FILES_INVALID")
            entry={
                "provider_article_id":article_id,
                "provider_article_DOI":meta.get("doi"),
                "published_date":meta.get("published_date"),
                "title":meta.get("title"),
                "license":meta.get("license"),
                "source_original_files":[]
            }
            for file in files:
                size=file.get("size")
                if not isinstance(size,int) or size<0:
                    size=None
                name=str(file.get("name",""))
                provider_md5=file.get("supplied_md5") or file.get("computed_md5")
                row={
                    "provider_file_id":file.get("id"),
                    "provider_name":name,
                    "provider_reported_bytes":size,
                    "provider_md5_reported_not_SHA256":provider_md5,
                    "source_download_status":"NOT_REQUESTED",
                }
                entry["source_original_files"].append(row)
                if (size is None or size>MAX_PUBLIC_BYTES
                    or not name.lower().endswith(ACCEPTED_EXT)
                    or candidate_count>=MAX_FILES):
                    row["source_download_status"]="SKIP_FORMAT_OR_SIZE_OR_FILE_LIMIT"
                    continue
                candidate_count+=1
                try:
                    content=_small_provider_bytes(client,str(file.get("download_url","")),size)
                    row["downloaded_original_bytes_sha256"]=hashlib.sha256(content).hexdigest()
                    row["downloaded_original_bytes_size"]=len(content)
                    row["source_download_status"]="PUBLIC_ORIGINAL_BYTES_READ"
                    parsed=_tabular_candidates(content,name)
                    for item in parsed:
                        item["source_original_article_id"]=article_id
                        item["parent_provider_file_id"]=file.get("id")
                        receipt["aggregate_tabular_source_schemas"].append(item)
                    row["n_bounded_tabular_tables"]=len(parsed)
                except (SourceHold, requests.RequestException, TimeoutError) as error:
                    row["source_download_status"]="ORIGINAL_SOURCE_ACCESS_HOLD"
                    row["source_hold_reason"]=str(error)[:180]
            receipt["article_metadata"].append(entry)
        receipt["n_original_tabular_tables"]=len(receipt["aggregate_tabular_source_schemas"])
        if receipt["n_original_tabular_tables"] == 0:
            receipt["source_status"]="PUBLISHED_SUPPLEMENT_WITHOUT_ORIGINAL_TABULAR_EVENTS"
        else:
            receipt["source_status"]="ORIGINAL_TABULAR_SCHEMA_FOUND_ID_JOIN_UNVERIFIED"
    except (SourceHold,requests.RequestException,ValueError,KeyError,
            json.JSONDecodeError,TimeoutError) as error:
        receipt["source_status"]="SOURCE_METADATA_ACCESS_BLOCKED"
        receipt["source_hold_reason"]=str(error)[:260]
    return receipt


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True,type=Path)
    opts=parser.parse_args()
    result=inspect_public_source(requests.Session())
    opts.output.parent.mkdir(parents=True,exist_ok=True)
    opts.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "source_status":result["source_status"],
        "n_original_linked_article_records":result.get("n_original_linked_article_records"),
        "n_original_tabular_tables":result.get("n_original_tabular_tables"),
        "n_original_files_listed":sum(len(k["source_original_files"]) for k in result.get("article_metadata",[])),
        "source_hold_reason":result.get("source_hold_reason"),
        "individual_three_decision_link_certified":False,
        "new_ecological_effect_fitted":False
    },ensure_ascii=False))


if __name__=="__main__":
    main()
