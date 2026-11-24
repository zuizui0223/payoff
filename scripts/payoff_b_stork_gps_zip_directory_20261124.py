#!/usr/bin/env python3
"""Inspect ONLY the tail ZIP central directory of three original CC0 GPS ZIPs.

Never follow redirects, download a whole GPS ZIP, decompress member content,
publish member filenames or inspect individual GPS/time/location records.
This diagnostic is file *structure* and no Bayesian q / recourse model.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path,PurePosixPath
import struct
import sys
from urllib.error import HTTPError,URLError
from urllib.parse import urlparse
from urllib.request import Request,build_opener

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))
from payoff_b_stork_dspace_file_metadata_20261124 import (
    get_metadata,bundle_entries,bitstream_entries,UUID_RE
)
from payoff_b_stork_gps_zip_range_gate_20261124 import select_gps_zip,NoRedirect

CONTRACT=HERE.parent/"data/payoff_b_stork_gps_zip_directory_contract_20261124.json"
TAIL_N=65557
EOCD=b"PK\x05\x06"
CD_ENTRY=b"PK\x01\x02"

def validate_zip_tail(buf,zip_size,max_members=10000):
    """Output only counts and format; filename bytes are not returned."""
    if len(buf)>TAIL_N or len(buf)<22:
        return {"status":"TAIL_SIZE_UNSUPPORTED"}
    p=buf.rfind(EOCD)
    if p<0 or p+22>len(buf):
        return {"status":"END_OF_CENTRAL_DIRECTORY_NOT_VERIFIED"}
    try:
        (sig,disk,startdisk,countdisk,n,totalbytes,offset,commentlen)=struct.unpack_from(
            "<4s4H2IH",buf,p)
    except struct.error:
        return {"status":"END_OF_CENTRAL_DIRECTORY_MALFORMED"}
    if sig!=EOCD or p+22+commentlen!=len(buf):
        return {"status":"UNEXPECTED_TRAILING_BYTES_OR_COMMENT"}
    if any((disk,startdisk)) or countdisk!=n:
        return {"status":"MULTIDISK_ZIP_UNSUPPORTED"}
    if n in (0,0xFFFF) or totalbytes==0xFFFFFFFF or offset==0xFFFFFFFF:
        return {"status":"ZIP64_OR_EMPTY_CENTRAL_DIRECTORY_UNSUPPORTED"}
    if n>max_members:
        return {"status":"TOO_MANY_SOURCE_MEMBERS"}
    firstpos=zip_size-len(buf)
    begin=offset-firstpos
    end=begin+totalbytes
    if begin<0 or end>p or end<begin:
        return {"status":"CENTRAL_DIRECTORY_OUTSIDE_FIXED_TAIL"}
    pos=begin
    ext_counts=Counter()
    method_counts=Counter()
    compressed_total=0
    uncompressed_total=0
    for _ in range(n):
        if pos+46>end or buf[pos:pos+4]!=CD_ENTRY:
            return {"status":"CENTRAL_DIRECTORY_MEMBER_MALFORMED"}
        try:
            parts=struct.unpack_from("<4s6H3I5H2I",buf,pos)
        except struct.error:
            return {"status":"CENTRAL_DIRECTORY_MEMBER_MALFORMED"}
        method=parts[4]
        compressed=parts[8]
        uncompressed=parts[9]
        name_len,extra_len,comm_len=parts[10:13]
        if compressed==0xFFFFFFFF or uncompressed==0xFFFFFFFF:
            return {"status":"ZIP64_MEMBER_UNSUPPORTED"}
        nxt=pos+46+name_len+extra_len+comm_len
        if nxt>end:
            return {"status":"CENTRAL_DIRECTORY_MEMBER_OUT_OF_BOUNDS"}
        raw_name=buf[pos+46:pos+46+name_len]
        name=raw_name.decode("utf-8","replace")
        suffix=PurePosixPath(name).suffix.lower()[:12] if name else ""
        ext_counts[suffix or "NO_SUFFIX"]+=1
        method_counts[str(method)]+=1
        compressed_total+=compressed
        uncompressed_total+=uncompressed
        pos=nxt
    if pos!=end:
        return {"status":"CENTRAL_DIRECTORY_SIZE_MISMATCH"}
    return {
      "status":"CENTRAL_DIRECTORY_METADATA_VERIFIED",
      "n_original_archive_members":n,
      "extension_counts":dict(ext_counts),
      "compression_method_counts":dict(method_counts),
      "total_member_compressed_size_bytes":compressed_total,
      "total_member_uncompressed_size_bytes":uncompressed_total,
      "raw_member_names_exported":False,
      "member_payloads_decompressed":False,
      "archive_full_checksum_verified":False,
    }

def read_last_bytes(url,source_size,limit=TAIL_N,opener=None):
    if limit!=TAIL_N or source_size<=limit:
        raise ValueError("Only exact 65557-tail Range allowed")
    expected_start=source_size-limit
    req=Request(url,headers={
        "Range":f"bytes={expected_start}-{source_size-1}",
        "Accept":"application/zip,application/octet-stream,*/*",
        "User-Agent":"PAYOFF-B-public-ZIP-CD-metadata-only/1.0"
    })
    opener=opener or build_opener(NoRedirect())
    try:
        with opener.open(req,timeout=30) as resp:
            if int(resp.status)!=206:
                return {"status":"TAIL_RANGE_NOT_HONORED","http_status":int(resp.status),
                        "bytes_read":0}
            u=urlparse(resp.geturl())
            if u.hostname!="datarepository.movebank.org" or u.path!=urlparse(url).path:
                raise ValueError("Unexpected ZIP tail data redirect")
            spec=f"bytes {expected_start}-{source_size-1}/{source_size}"
            if str(resp.headers.get("Content-Range",""))!=spec:
                return {"status":"TAIL_RANGE_BOUNDS_MISMATCH","http_status":206,"bytes_read":0}
            data=resp.read(limit+1)
            if len(data)!=limit:
                return {"status":"ZIP_TAIL_BYTES_UNEXPECTED","http_status":206,
                        "bytes_read":len(data)}
        result=validate_zip_tail(data,source_size)
        result.update({"http_status":206,"bytes_read":len(data),
                       "source_member_payload_accessed":False})
        return result
    except HTTPError as e:
        code=e.code;e.close()
        return {"status":"ZIP_TAIL_HTTP_FAILURE","http_status":int(code),"bytes_read":0}
    except (URLError,TimeoutError,OSError,ValueError) as e:
        return {"status":"ZIP_TAIL_TRANSPORT_FAILED","error_class":type(e).__name__,
                "bytes_read":0}

def audit(contract):
    items=contract["source_items"]
    allowed={x["id"] for x in items.values()}
    result=[]
    for cohort,info in items.items():
        uid=info["id"]
        entry=get_metadata(f"/server/api/core/items/{uid}",allowed,set())
        if entry["status"]!="PUBLIC_METADATA_OK" or (entry["data"] or {}).get("handle")!=info["handle"]:
            result.append({"cohort":cohort,"status":"ORIGINAL_ITEM_NOT_VERIFIED"})
            continue
        bundles=get_metadata(f"/server/api/core/items/{uid}/bundles",allowed,set())
        if bundles["status"]!="PUBLIC_METADATA_OK":
            result.append({"cohort":cohort,"status":"ORIGINAL_BUNDLE_NOT_VERIFIED"})
            continue
        good=[b for b in bundle_entries(bundles["data"] or {})
              if str(b.get("name") or "")=="ORIGINAL" and UUID_RE.fullmatch(str(b.get("uuid") or ""))]
        if len(good)!=1:
            result.append({"cohort":cohort,"status":"ORIGINAL_BUNDLE_NOT_UNIQUE"})
            continue
        bid=good[0]["uuid"]
        files=get_metadata(f"/server/api/core/bundles/{bid}/bitstreams",allowed,{bid})
        if files["status"]!="PUBLIC_METADATA_OK":
            result.append({"cohort":cohort,"status":"ORIGINAL_FILES_NOT_VERIFIED"})
            continue
        selected=select_gps_zip(bitstream_entries(files["data"] or {}),info["zip_size"])
        tail=read_last_bytes(selected["url"],selected["size_bytes"])
        result.append({
          "cohort":cohort,
          "source_zip_size":selected["size_bytes"],
          "public_original_source_md5_metadata_present":selected["public_md5_present"],
          "tail":tail,
          "whole_GPS_archive_downloaded":False,
          "original_member_names_or_GPS_rows_exported":False,
        })
    return {
      "date":contract["date"],
      "status":"ZIP_CENTRAL_DIRECTORY_SOURCE_GATE_COMPLETED",
      "source_archives":result,
      "n_original_archives":len(result),
      "n_verified_central_directories":sum(
          x.get("tail",{}).get("status")=="CENTRAL_DIRECTORY_METADATA_VERIFIED"
          for x in result),
      "n_zip_tail_range_calls_max":len(result),
      "original_GPS_or_ACC_ZIP_payload_downloaded":False,
      "original_GPS_rows_or_coordinates_read":False,
      "ZIP_member_data_decompressed":False,
      "individual_identifiers_exported":False,
      "social_information_q_or_actionability_r_estimated":False,
      "no_ebird":True,
      "claim_boundary":"Original archive directory structure only. No GPS schema, timestamp coverage, animal behavior, social cue, Bayesian q or fitness inferred."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contract",type=Path,default=CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    c=json.loads(args.contract.read_text())
    result=audit(c)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print("STORK_ORIGINAL_ZIP_DIRECTORY="+json.dumps(result,separators=(",",":")))

if __name__=="__main__":
    main()
