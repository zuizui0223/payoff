#!/usr/bin/env python3
"""Bounded CC0 GPS ZIP transport probe, NOT tracking-data or metadata extraction.

Only HEAD and a single 4KiB HTTP Range request for the smallest original
GPS ZIP in each pinned Bontekoe 2023 cohort. Does not decompress ZIP bytes,
return source filenames, coordinates, GPS events or fish hidden endpoints.
"""
from __future__ import annotations
import argparse,hashlib,json,re,sys
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.parse import urlparse
from urllib.request import Request,build_opener,HTTPRedirectHandler

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))
from payoff_b_stork_dspace_file_metadata_20261124 import (
  get_metadata,bundle_entries,bitstream_entries,ROOT,UUID_RE
)

CONTRACT=HERE.parent/"data/payoff_b_stork_gps_zip_range_contract_20261124.json"

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,request,fp,code,msg,headers,newurl):
        return None

def select_gps_zip(entries,expected):
    chosen=[x for x in entries
            if str(x.get("name","")).lower().endswith(".zip")
            and re.search(r"gps|location",str(x.get("name") or ""),re.I)]
    if not chosen:
        raise ValueError("No GPS ZIP in original source bundle")
    selected=min(chosen,key=lambda x:int(x.get("sizeBytes") or 0))
    uuid=str(selected.get("uuid") or selected.get("id") or "")
    if not UUID_RE.fullmatch(uuid):
        raise ValueError("GPS ZIP ID missing")
    size=selected.get("sizeBytes")
    if not isinstance(size,int) or size!=expected:
        raise ValueError("Original pre-registered source file size changed")
    check=selected.get("checkSum") or {}
    if str(check.get("checkSumAlgorithm","")).upper()!="MD5":
        raise ValueError("Source ZIP metadata checksum missing")
    content=ROOT+f"/server/api/core/bitstreams/{uuid}/content"
    if (selected.get("_links",{}).get("content",{}) or {}).get("href")!=content:
        raise ValueError("Original DSpace content URL not pinned")
    return {"url":content,"size_bytes":size,"public_md5_present":True}


def request_head(url,opener):
    req=Request(url,method="HEAD",headers={"User-Agent":"PAYOFF-B-CC0-GPS-range-metadata/1.0"})
    try:
        with opener.open(req,timeout=25) as resp:
            return {"http_status":int(resp.status),
                    "accept_ranges":str(resp.headers.get("Accept-Ranges","")).lower()=="bytes",
                    "declared_content_length":_int_or_none(resp.headers.get("Content-Length"))}
    except HTTPError as e:
        e.close()
        return {"http_status":int(e.code),"accept_ranges":False,"declared_content_length":None}
    except (URLError,OSError,TimeoutError) as e:
        return {"http_status":None,"accept_ranges":False,"declared_content_length":None,
                "error_class":type(e).__name__}

def _int_or_none(s):
    try:return int(s)
    except (ValueError,TypeError):return None

def request_tiny_range(url,expected,limit,opener):
    if limit!=4096:
        raise ValueError("ZIP transport probe fixed at exactly 4KiB")
    req=Request(url,headers={"Range":"bytes=0-4095",
                             "Accept":"application/zip,application/octet-stream,*/*",
                             "User-Agent":"PAYOFF-B-CC0-GPS-4KiB-header-only/1.0"})
    try:
        with opener.open(req,timeout=25) as resp:
            status=int(resp.status)
            # Do not read a single archive byte if the server ignores Range.
            if status!=206:
                return {"status":"RANGE_NOT_HONORED","http_status":status,
                        "bytes_read":0,"zip_header_verified":False}
            location=urlparse(resp.geturl())
            if location.hostname!="datarepository.movebank.org" or location.path!=urlparse(url).path:
                raise ValueError("Unexpected archive content redirect")
            spec=str(resp.headers.get("Content-Range",""))
            if spec!=f"bytes 0-4095/{expected}":
                return {"status":"RANGE_RESPONSE_BOUNDS_MISMATCH","http_status":206,
                        "bytes_read":0,"zip_header_verified":False}
            chunk=resp.read(limit+1)
            if len(chunk)!=limit or chunk[:4]!=b"PK\x03\x04":
                return {"status":"ZIP_HEADER_NOT_VERIFIED","http_status":206,
                        "bytes_read":len(chunk),"zip_header_verified":False}
            return {"status":"ORIGINAL_ZIP_4K_RANGE_VERIFIED","http_status":206,
                    "bytes_read":len(chunk),"zip_header_verified":True,
                    "chunk_sha256":hashlib.sha256(chunk).hexdigest(),
                    "original_full_zip_checksum_verified":False}
    except HTTPError as exc:
        status=exc.code
        exc.close()
        return {"status":"RANGE_HTTP_FAILURE","http_status":int(status),
                "bytes_read":0,"zip_header_verified":False}
    except (URLError,OSError,ValueError,TimeoutError) as exc:
        return {"status":"RANGE_TRANSPORT_NOT_VERIFIED",
                "error_class":type(exc).__name__,
                "bytes_read":0,"zip_header_verified":False}

def audit(contract):
    ids={k:v["id"] for k,v in contract["original_dspace_items"].items()}
    allowed=set(ids.values())
    results=[]
    for cohort,info in contract["original_dspace_items"].items():
        uid=info["id"]
        item=get_metadata(f"/server/api/core/items/{uid}",allowed,set())
        if item["status"]!="PUBLIC_METADATA_OK" or (item["data"] or {}).get("handle")!=info["handle"]:
            results.append({"cohort":cohort,"status":"ORIGINAL_ITEM_NOT_VERIFIED"})
            continue
        bundles=get_metadata(f"/server/api/core/items/{uid}/bundles",allowed,set())
        if bundles["status"]!="PUBLIC_METADATA_OK":
            results.append({"cohort":cohort,"status":"ORIGINAL_BUNDLE_NOT_VERIFIED"})
            continue
        b=[b for b in bundle_entries(bundles["data"] or {})
           if str(b.get("name") or "")=="ORIGINAL" and UUID_RE.fullmatch(str(b.get("uuid") or ""))]
        if len(b)!=1:
            results.append({"cohort":cohort,"status":"ORIGINAL_BUNDLE_NOT_UNIQUE"})
            continue
        bid=b[0]["uuid"]
        files=get_metadata(f"/server/api/core/bundles/{bid}/bitstreams",allowed,{bid})
        if files["status"]!="PUBLIC_METADATA_OK":
            results.append({"cohort":cohort,"status":"ORIGINAL_FILE_METADATA_NOT_VERIFIED"})
            continue
        selection=select_gps_zip(bitstream_entries(files["data"] or {}),
                                 info["expected_smallest_gps_zip_bytes"])
        opener=build_opener(NoRedirect())
        head=request_head(selection["url"],opener)
        tiny=request_tiny_range(selection["url"],selection["size_bytes"],
                                contract["http_probe"]["max_body_bytes_per_file"],opener)
        results.append({
           "cohort":cohort,"status":"GPS_ZIP_PUBLIC_METADATA_VERIFIED",
           "original_zip_size_bytes":selection["size_bytes"],
           "public_original_full_zip_md5_available":selection["public_md5_present"],
           "head":head,"range_first4KiB":tiny,
           "full_ZIP_data_downloaded":False,
           "GPS_event_rows_opened":False,
           "original_ZIP_filename_or_animal_ids_exported":False
        })
    return {
       "date":contract["date"],
       "status":"SMALL_RANGE_PROBE_COMPLETED",
       "n_source_studies":len(results),
       "cohort_receipts":results,
       "n_verified_4KiB_ZIP_headers":sum(
           r.get("range_first4KiB",{}).get("zip_header_verified") is True for r in results),
       "full_GPS_or_ACC_ZIPs_downloaded":False,
       "original_GPS_locations_or_event_rows_parsed":False,
       "zip_members_extracted":False,
       "original_bird_ids_or_coordinates_exported":False,
       "environmental_cue_q_or_recourse_r_estimated":False,
       "no_ebird":True,
       "claim_limit":"Range-support and ZIP magic only. Neither an event-time schema nor the source's full ZIP SHA/MD5 has been validated."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contract",type=Path,default=CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    raw=a.contract.read_bytes();c=json.loads(raw)
    z=audit(c)
    z["contract_sha256"]=hashlib.sha256(raw).hexdigest()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(z,indent=2)+"\n")
    print("STORK_GPS_RANGE_SOURCE_ONLY="+json.dumps(z,separators=(",",":")))

if __name__=="__main__":
    main()
