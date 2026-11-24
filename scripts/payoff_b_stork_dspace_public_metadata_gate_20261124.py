#!/usr/bin/env python3
"""Metadata-only check of the documented DSpace REST search endpoint.

The source UI uses <ds-app> and static Angular scripts; the standard DSpace
7/8/9 REST search endpoint is /server/api/discover/search/objects.
This check never retrieves item bitstreams, GPS, event tables or datasets.
Results are limited to public metadata/DOIs and HAL item identifiers.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import urllib.parse
import urllib.request
import urllib.error

HOST="datarepository.movebank.org"
ROOT="https://datarepository.movebank.org/server/api"
QUERY="The price of being late"
SEARCH=ROOT+"/discover/search/objects?"+urllib.parse.urlencode(
    {"query":QUERY,"dsoType":"item","size":"20"}
)
ENDPOINTS={ROOT,SEARCH}
CAP_BYTES=262144


def request_public_metadata(url,open_fn=None):
    if url not in ENDPOINTS:
        raise ValueError("Unregistered API metadata-only URL")
    open_fn=open_fn or urllib.request.urlopen
    req=urllib.request.Request(url,headers={
       "Accept":"application/hal+json,application/json",
       "User-Agent":"PAYOFF-B-public-DSpace-metadata-gate/1.0",
    })
    try:
        with open_fn(req,timeout=20) as resp:
            actual=urllib.parse.urlparse(resp.geturl())
            if actual.hostname!=HOST or not actual.path.startswith("/server/api"):
                raise ValueError("Unexpected repository API redirect")
            typ=str(resp.headers.get("Content-Type",""))
            if "json" not in typ.lower():
                raise ValueError("Repository backend did not serve JSON")
            raw=resp.read(CAP_BYTES+1)
            if len(raw)>CAP_BYTES:
                raise ValueError("Too-large metadata JSON; refuse")
            return {"status":"PUBLIC_JSON_RECEIVED","http_status":int(resp.status),
                    "bytes_received":len(raw),"json":json.loads(raw)}
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,OSError,ValueError,json.JSONDecodeError) as exc:
        return {"status":"NO_PUBLIC_DSPACE_JSON_AVAILABLE",
                "error_class":type(exc).__name__,
                "http_status":int(exc.code) if isinstance(exc,urllib.error.HTTPError) else None,
                "bytes_received":0,"json":None}


def only_public_source_summary(obj):
    if not isinstance(obj,dict):
        return []
    # DSpace search HAL serializes a list of searchResult objects with an
    # embedded indexObject, sometimes nested in searchResult._embedded.
    search_result=obj.get("_embedded",{}).get("searchResult",{})
    candidates=search_result.get("_embedded",{}).get("objects",[])
    if not isinstance(candidates,list):
        candidates=[]
    summary=[]
    for r in candidates[:20]:
        if not isinstance(r,dict):
            continue
        item=r.get("_embedded",{}).get("indexableObject",{}) or {}
        if not isinstance(item,dict):
            item={}
        metadata=item.get("metadata",{}) or {}
        title_vals=metadata.get("dc.title",[])
        title=str(title_vals[0].get("value","")) if title_vals and isinstance(title_vals[0],dict) else ""
        if "price of being late" not in title.lower():
            continue
        summary.append({
           "name":str(item.get("name",""))[:220],
           "uuid":str(item.get("uuid") or item.get("id") or "")[:80],
           "handle":str(item.get("handle",""))[:100],
           "title":title[:280],
           "metadata_only":True,
           "bitstreams_requested":False,
        })
    return summary


def audit():
    root=request_public_metadata(ROOT)
    search=request_public_metadata(SEARCH)
    results=only_public_source_summary(search["json"]) if search["json"] is not None else []
    return {
      "date":"2026-11-24",
      "status":"PUBLIC_DSPACE_METADATA_SEARCH_CHECKED",
      "reason":"The Movebank Data Repository landing HTML is a DSpace Angular app shell; the official DSpace public REST search route is being tested, not presumed.",
      "root":{"status":root["status"],"http_status":root["http_status"],"error_class":root.get("error_class"),"bytes_received":root["bytes_received"]},
      "search":{"status":search["status"],"http_status":search["http_status"],"error_class":search.get("error_class"),"bytes_received":search["bytes_received"]},
      "matched_original_public_items":results,
      "n_matching_public_items":len(results),
      "tracking_or_event_files_downloaded":False,
      "original_bitstreams_requested":False,
      "user_credentials_sent":False,
      "license_terms_accepted":False,
      "claim":"Even if public DSpace items are found, metadata search does not establish direct file download, time-aligned GPS coverage, actual conspecific exposure or predictive cue reliability q.",
      "no_ebird":True,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    result=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print("PAYOFF_DSPACE_PUBLIC_META_RESULT="+json.dumps(result,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
