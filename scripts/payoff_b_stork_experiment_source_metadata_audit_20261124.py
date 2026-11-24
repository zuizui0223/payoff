#!/usr/bin/env python3
"""Read ONLY original public DOI metadata for Bontekoe 2023 white-stork experiment.

DO NOT access or download original tracking data, events, animals, coordinates,
Movebank terms, or Zenodo file bytes. This is a license-preserving source gate
for a potentially new question, not a behavioral or survival reanalysis.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import urllib.error
import urllib.request

ZENODO="https://zenodo.org/api/records/8108611"
DATACITE="https://api.datacite.org/dois/"
STORK_ARCHIVES=[
    "10.5441/001/1.271",
    "10.5441/001/1.276",
    "10.5441/001/1.277",
]
BYTE_CAP=1_000_000

def fetch_json(url,timeout=18):
    allowed=(
        url==ZENODO or
        (url.startswith(DATACITE) and
         url[len(DATACITE):] in STORK_ARCHIVES)
    )
    if not allowed:
        raise ValueError("External metadata endpoint not allowlisted")
    request=urllib.request.Request(
        url,headers={"Accept":"application/json",
        "User-Agent":"PAYOFF-B academic public metadata source-audit/1.0"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as reply:
        if reply.status!=200:
            raise RuntimeError("Unexpected status code")
        data=reply.read(BYTE_CAP+1)
    if len(data)>BYTE_CAP:
        raise ValueError("Metadata exceeds one-MB audit cap")
    return json.loads(data.decode("utf-8"))


def safe_string(value,max_len=280):
    return str(value or "").replace("\n"," ").replace("\r"," ")[:max_len]


def read_zenodo(z):
    if not str(z.get("id",""))=="8108611":
        raise ValueError("Zenodo record ID mismatched")
    metadata=z.get("metadata") or {}
    files=z.get("files") or []
    # Metadata-only file index. Download links are not fetched.
    return {
        "record_id":int(z["id"]),
        "doi":safe_string(metadata.get("doi") or z.get("doi"),150),
        "title":safe_string(metadata.get("title"),400),
        "created":safe_string(z.get("created"),50),
        "license_id":safe_string((metadata.get("license") or {}).get("id") if isinstance(metadata.get("license"),dict) else metadata.get("license"),80),
        "file_count":len(files),
        "files":[
            {"name":safe_string(f.get("key"),240),
             "size_bytes":f.get("size"),
             "checksum":safe_string(f.get("checksum"),120)}
            for f in files[:100]
        ],
        "metadata_only":True,
        "source_archive_files_downloaded":False,
    }


def read_datacite(z,expected_doi):
    attrs=z.get("data",{}).get("attributes") or {}
    reported=str(attrs.get("doi") or "").lower()
    if reported != expected_doi.lower():
        raise ValueError("DataCite DOI did not match requested original archive")
    title_items=attrs.get("titles") or []
    rights_list=attrs.get("rightsList") or []
    related=attrs.get("relatedIdentifiers") or []
    return {
        "doi":reported,
        "title":safe_string(title_items[0].get("title") if title_items else "",350),
        "publication_year":attrs.get("publicationYear"),
        "publisher":safe_string(attrs.get("publisher"),120),
        "rights":[safe_string(r.get("rights") or r.get("rightsUri"),130) for r in rights_list[:4]],
        "resource_type":safe_string((attrs.get("types") or {}).get("resourceTypeGeneral"),100),
        "landing_page":safe_string(attrs.get("url"),250),
        "related_doi":[safe_string(x.get("relatedIdentifier"),150) for x in related
                       if str(x.get("relatedIdentifierType","")).lower()=="doi"][:5],
        "doi_metadata_only":True,
        "tracking_event_rows_requested":False,
    }


def audit():
    ret={
      "date":"2026-11-24",
      "status":"SOURCE_METADATA_NOT_YET_CLASSIFIED",
      "original_paper":"10.1098/rspb.2023.1268",
      "metadata_source":"Zenodo public record 8108611 and DataCite public DOI records",
      "original_tracking_or_code_files_downloaded":False,
      "movebank_events_requested":False,
      "license_terms_accepted":False,
      "ebird_used":False,
      "new_ecological_effect_fitted":False,
      "original_published_results_reestimated":False,
      "zenodo_code":None,
      "movebank_archives":[],
    }
    try:
        ret["zenodo_code"]={"status":"VERIFIED","metadata":read_zenodo(fetch_json(ZENODO))}
    except Exception as e:
        ret["zenodo_code"]={"status":"NOT_VERIFIED","error":type(e).__name__,
                            "summary":safe_string(e,180)}
    for doi in STORK_ARCHIVES:
        try:
            # slashes are valid in path and exactly pinned by the allowlist.
            data=read_datacite(fetch_json(DATACITE+doi),doi)
            ret["movebank_archives"].append({"status":"VERIFIED","doi":doi,"metadata":data})
        except Exception as e:
            ret["movebank_archives"].append({"status":"NOT_VERIFIED","doi":doi,
               "error":type(e).__name__,"summary":safe_string(e,180)})
    valid_archive=sum(item["status"]=="VERIFIED" for item in ret["movebank_archives"])
    zenodo_verified=ret["zenodo_code"]["status"]=="VERIFIED"
    ret["status"]="METADATA_SOURCE_GATE_PASS" if valid_archive==3 and zenodo_verified else "METADATA_SOURCE_GATE_INCOMPLETE"
    ret["verified_doi_archives"]=valid_archive
    ret["possible_future_work"]="Check permitted original tracking data fields separately; code/archive metadata alone cannot establish actual cue measurement, biological novelty, nor event-download permission."
    return ret


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=pathlib.Path,required=True)
    args=ap.parse_args()
    result=audit()
    args.output.parent.mkdir(exist_ok=True,parents=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("PAYOFF_B_STORK_SOURCE_AUDIT="+json.dumps(result,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
