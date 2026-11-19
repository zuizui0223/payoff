#!/usr/bin/env python3
"""Offline original Curlew source admission after Dryad file API HTTP 401.

Accept only (1) the full SHA-256-verified original 2026 Dryad ZIP, or
(2) the small user-supplied extracted dt_hab_Curlew.csv, with identity
explicitly UNKNOWN without the original ZIP digest. Export aggregates only.
Never output bird/season IDs, GPS coordinates or nest locations.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from scripts.payoff_b_curlew_dryad_source_gate import (
    MAX_CSV_BYTES,
    TARGET_CSV,
    summarize_original_csv
)

PUBLISHED_ZIP_NAME="Curlew_COE_habitat.zip"
PUBLISHED_ZIP_SIZE=590_985_065
PUBLISHED_ZIP_SHA256="e3556851ef646eabad21dc0d482da58028b0327a8aaf459fdb02c3896bd48372"
PUBLISHED_VERSION_ID=466868
PUBLISHED_PUBLIC_DRYAD_FILE_ID=4989265

def digest_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda:handle.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def offline_original_source(file_path:Path,
                            expected_zip_size:int=PUBLISHED_ZIP_SIZE,
                            expected_zip_sha256:str=PUBLISHED_ZIP_SHA256)->dict:
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    record={
        "source":"Dryad 10.5061/dryad.31zcrjf22, publication 2026-10-01",
        "source_version_id":PUBLISHED_VERSION_ID,
        "original_zip_file_id":PUBLISHED_PUBLIC_DRYAD_FILE_ID,
        "no_individual_ID_or_sensitive_coordinate_export":True,
        "source_bird_and_nesting_fit_unopened":True,
        "information_deadline_mechanism":"NOT_ESTIMABLE",
        "source_original_API_anonymous_download":"HTTP_401",
    }
    if file_path.name==PUBLISHED_ZIP_NAME:
        if file_path.stat().st_size!=expected_zip_size:
            raise ValueError("Original author Dryad ZIP source size mismatched")
        if digest_file(file_path)!=expected_zip_sha256:
            raise ValueError("Original author Dryad ZIP source SHA256 mismatched")
        with zipfile.ZipFile(file_path) as archive:
            members=[
                z for z in archive.infolist()
                if z.filename.replace("\\","/").split("/")[-1]==TARGET_CSV
            ]
            if len(members)!=1:
                raise ValueError("Original ZIP has no unique dt_hab_Curlew.csv")
            member=members[0]
            if member.file_size>MAX_CSV_BYTES:
                raise ValueError("Source original CSV exceeds reader size guard")
            with archive.open(member) as f:
                raw=f.read(MAX_CSV_BYTES+1)
            if len(raw)>MAX_CSV_BYTES:
                raise ValueError("Original CSV decompression size exceeded")
        record["source_original_zip_sha256_verified"]=True
        record["source_original_zip_sha256"]=expected_zip_sha256
        record["source_provenance_status"]="PROVIDER_SHA256_AND_SIZE_MATCHED"
    elif file_path.name==TARGET_CSV:
        if file_path.stat().st_size>MAX_CSV_BYTES:
            raise ValueError("Extracted source CSV exceeds size guard")
        raw=file_path.read_bytes()
        record["source_original_zip_sha256_verified"]=False
        record["source_provenance_status"]="USER_SUPPLIED_EXTRACTED_CSV_ORIGIN_NOT_INDEPENDENTLY_HASH_VERIFIED"
    else:
        raise ValueError("Only exact published ZIP or dt_hab_Curlew.csv supported")
    record["verified_source_semantics"]=summarize_original_csv(raw)
    record["actual_original_bird_season_grain_read"]=True
    record["source_csv_sha256"]=hashlib.sha256(raw).hexdigest()
    record["actual_original_cue_and_observability_available"]=False
    record["new_biological_fit_performed"]=False
    return record

def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--local-original-zip",type=Path)
    group.add_argument("--local-derived-csv",type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    out=offline_original_source(args.local_original_zip or args.local_derived_csv)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":out["source_provenance_status"],
        "grain":out["verified_source_semantics"],
        "new_biological_fit":False,
        "direct_information_deadline":"NOT_ESTIMABLE"
    },ensure_ascii=False))

if __name__=="__main__":
    main()
