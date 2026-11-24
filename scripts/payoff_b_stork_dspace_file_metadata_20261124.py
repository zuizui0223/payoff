#!/usr/bin/env python3
"""Original CC0 white-stork DSpace item/bundle/bitstream METADATA gate.

No bitstream '/content' endpoint is ever called. Exact item UUIDs were
recovered from public DSpace title search and pinned in source contract.
File names/IDs of source rows are not published; only extension, size and
coarse content-type indicators from public metadata. It is NOT GPS analysis.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse
from hashlib import sha256

ROOT="https://datarepository.movebank.org"
CONTRACT=Path(__file__).resolve().parents[1]/"data/payoff_b_stork_social_opportunity_access_contract_20261124.json"
UUID_RE=re.compile(r"^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$")
MAX_BYTES=262144


def get_metadata(path,known_items,known_bundles):
    # Do not allow any URL discovered in JSON to be followed blindly.
    if path.endswith("/content") or "/bitstreams/" in path and "/content" in path:
        raise ValueError("Bitstream-content download forbidden")
    m=re.fullmatch(r"/server/api/core/items/([0-9a-f-]+)(/bundles)?",path)
    n=re.fullmatch(r"/server/api/core/bundles/([0-9a-f-]+)/bitstreams",path)
    if m:
        if m.group(1) not in known_items or not UUID_RE.fullmatch(m.group(1)):
            raise ValueError("Item is not one of the three SHA-pinned public source records")
    elif n:
        if n.group(1) not in known_bundles or not UUID_RE.fullmatch(n.group(1)):
            raise ValueError("Bundle UUID not recovered from verified item")
    else:
        raise ValueError("Unknown/unlicensed API method path")
    req=urllib.request.Request(ROOT+path,headers={
        "Accept":"application/hal+json,application/json",
        "User-Agent":"PAYOFF-B-bonafide-public-metadata-gate/1.0"
    })
    try:
        with urllib.request.urlopen(req,timeout=24) as resp:
            u=urlparse(resp.geturl())
            if u.hostname!="datarepository.movebank.org" or not u.path.startswith("/server/api/core/"):
                raise ValueError("Unauthorized external API redirect")
            if "json" not in str(resp.headers.get("Content-Type","")).lower():
                raise ValueError("Expected public JSON metadata, not binary data")
            raw=resp.read(MAX_BYTES+1)
            if len(raw)>MAX_BYTES:
                raise ValueError("Oversize API JSON, refusing")
        return {"status":"PUBLIC_METADATA_OK","data":json.loads(raw)}
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,OSError,ValueError,json.JSONDecodeError) as e:
        return {"status":"PUBLIC_METADATA_FAILED","error_class":type(e).__name__,
                "http_status":int(e.code) if isinstance(e,urllib.error.HTTPError) else None,
                "data":None}


def bundle_entries(data):
    embedded=data.get("_embedded") or {}
    entries=embedded.get("bundles") or []
    if not isinstance(entries,list):
        return []
    return [e for e in entries if isinstance(e,dict)]


def bitstream_entries(data):
    embedded=data.get("_embedded") or {}
    entries=embedded.get("bitstreams") or []
    if not isinstance(entries,list):
        return []
    return [e for e in entries if isinstance(e,dict)]


def safe_file_type(name):
    ext=Path(str(name or "")).suffix.lower()
    return ext[:12] if ext else "NO_SUFFIX"


def public_file_entry(e):
    name=str(e.get("name",""))
    checksum=e.get("checkSum") or {}
    if not isinstance(checksum,dict): checksum={}
    sz=e.get("sizeBytes")
    return {
       "extension":safe_file_type(name),
       "size_bytes":int(sz) if isinstance(sz,(int,float)) and sz>=0 else None,
       "name_has_GPS":bool(re.search(r"gps|location",name,re.IGNORECASE)),
       "name_has_ACC":bool(re.search(r"acc|accelerat",name,re.IGNORECASE)),
       "name_has_README":bool(re.search(r"readme|manifest|description",name,re.IGNORECASE)),
       "has_MD5_checksum":str(checksum.get("checkSumAlgorithm","")).upper()=="MD5",
       "bitstream_content_requested":False,
       "raw_file_or_identifier_returned":False,
    }


def audit(contract):
    sites=contract["verified_public_item_ids"]
    items={v["uuid"] for v in sites.values()}
    result={
      "date":contract["date"],
      "status":"METADATA_BUNDLE_INVENTORY_COMPLETED",
      "original_stork_archives":[],
      "n_items_expected":3,
      "original_GPS_event_rows_downloaded":False,
      "bitstream_content_requested":False,
      "user_credentials_sent":False,
      "terms_autoaccepted":False,
      "social_predictive_accuracy_or_Bayesian_payoff_estimated":False,
      "no_ebird":True,
    }
    for cohort,v in sites.items():
        uuid=v["uuid"]
        item=get_metadata(f"/server/api/core/items/{uuid}",items,set())
        if item["status"]!="PUBLIC_METADATA_OK":
            result["original_stork_archives"].append({
               "cohort":cohort,"status":"ITEM_METADATA_UNAVAILABLE",
               "error_class":item.get("error_class"),
               "http_status":item.get("http_status"),
            })
            continue
        raw=item["data"] or {}
        if str(raw.get("handle",""))!=v["handle"] or str(raw.get("uuid") or raw.get("id",""))!=uuid:
            result["original_stork_archives"].append({
               "cohort":cohort,"status":"ITEM_IDENTITY_MISMATCH"})
            continue
        bundle_result=get_metadata(f"/server/api/core/items/{uuid}/bundles",items,set())
        if bundle_result["status"]!="PUBLIC_METADATA_OK":
            result["original_stork_archives"].append({
               "cohort":cohort,"status":"BUNDLE_METADATA_UNAVAILABLE",
               "error_class":bundle_result.get("error_class"),
               "http_status":bundle_result.get("http_status")})
            continue
        bundles=bundle_entries(bundle_result["data"] or {})
        counted=[]
        for b in bundles[:8]:
            buuid=str(b.get("uuid") or b.get("id") or "")
            if not UUID_RE.fullmatch(buuid):
                continue
            listing=get_metadata(f"/server/api/core/bundles/{buuid}/bitstreams",items,{buuid})
            if listing["status"]=="PUBLIC_METADATA_OK":
                entries=bitstream_entries(listing["data"] or {})
                counted.append({
                   "bundle_type":str(b.get("name") or "UNNAMED")[:40],
                   "status":"BITSTREAM_METADATA_OK",
                   "n_public_metadata_files":len(entries),
                   "files":[public_file_entry(x) for x in entries[:50]],
                   "possible_more_than_first_page":bool((listing["data"] or {}).get("_links",{}).get("next"))
                })
            else:
                counted.append({
                   "bundle_type":str(b.get("name") or "UNNAMED")[:40],
                   "status":"BITSTREAM_METADATA_UNAVAILABLE",
                   "http_status":listing.get("http_status"),
                   "error_class":listing.get("error_class")})
        result["original_stork_archives"].append({
           "cohort":cohort,"status":"ITEM_HANDLE_VERIFIED",
           "n_published_bundles_metadata":len(bundles),
           "n_bundles_inspected":len(counted),
           "bundles":counted,
           "bitstream_bytes_read":False,
        })
    result["n_verified_item_handles"]=sum(
       x["status"]=="ITEM_HANDLE_VERIFIED" for x in result["original_stork_archives"]
    )
    result["conclusion"]="This documents public file METADATA only, not file download accessibility, code-ready variable schema, valid cross-study identity joins, predecision social information, q or fitness."
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--contract",type=Path,default=CONTRACT)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    c=json.loads(args.contract.read_text())
    z=audit(c)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(z,indent=2,ensure_ascii=False)+"\n")
    print("PAYOFF_STORK_BITSTREAM_METADATA="+json.dumps(z,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
