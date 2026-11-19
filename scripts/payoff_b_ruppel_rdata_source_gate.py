#!/usr/bin/env python3
"""Original SHA256-pinned 2023 Figshare RData bird-weather source audit.

No new biological effect fit. No individual bird IDs, GPS, event rows,
weather values or original RMarkdown code are exported. Only source schema,
field type, table sizes, missing counts and potential ID cardinalities.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
import zipfile
from pathlib import Path

import pandas as pd
import pyreadr

ZIP_NAME="rsos221420_si_002.zip"
ZIP_SIZE=100303
ZIP_SHA256="0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6"
ZIP_PUBLISHED_FILE_ID=38968813
ORIGINAL_DOI="10.6084/m9.figshare.c.6403996"
MEMBERS=("data.Event.RData","flights.RData")
SOURCE_CODE_MEMBER="Rcode.Rmd"

ID_NAMES=re.compile(r"(?:^id$|bird|tag|ring|individual|animal|^name$)",re.I)
TIME_NAMES=re.compile(r"(?:date|time|hour|day|doy|sunset|takeoff|departure|start|end)",re.I)
DECISION_NAMES=re.compile(r"(?:departure|depart|flight|route|offshore|onshore|land|stopover|outcome|success)",re.I)
ENV_NAMES=re.compile(r"(?:wind|temp|press|cloud|rain|precip|humidity|weather|u10|v10)",re.I)


def file_sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def validate_zip(path:Path,source_size:int=ZIP_SIZE,
                 source_hash:str=ZIP_SHA256)->zipfile.ZipFile:
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.name!=ZIP_NAME:
        raise ValueError("Original provider ZIP filename changed")
    if path.stat().st_size!=source_size:
        raise ValueError("Original 2023 Figshare ZIP length changed")
    if file_sha256(path)!=source_hash:
        raise ValueError("Original 2023 Figshare ZIP SHA256 changed")
    z=zipfile.ZipFile(path)
    found={n for n in z.namelist()}
    if not set(MEMBERS+(SOURCE_CODE_MEMBER,)).issubset(found):
        z.close()
        raise ValueError("Original 2023 Figshare ZIP source members changed")
    if len(found)>30 or any(x.file_size>1_000_000 for x in z.infolist()):
        z.close()
        raise ValueError("Unexpected source ZIP member count or expanded size")
    return z


def dataframe_schema(df:pd.DataFrame,source_member:str,
                     r_object_name:str)->dict:
    if len(df)>500000 or len(df.columns)>180:
        raise ValueError("Original RData dataframe too wide or large")
    cols=[str(c) for c in df.columns]
    if any(len(c)>180 for c in cols):
        raise ValueError("Original source field name exceeds safe reporting limit")
    ids=[c for c in cols if ID_NAMES.search(c)]
    time=[c for c in cols if TIME_NAMES.search(c)]
    decisions=[c for c in cols if DECISION_NAMES.search(c)]
    env=[c for c in cols if ENV_NAMES.search(c)]
    unique_id_counts={}
    for c in ids[:10]:
        v=df[c].dropna().astype(str)
        unique_id_counts[c]={
            "n_rows_present":int(len(v)),
            "n_distinct_values":int(v.nunique()),
            "n_repeated_records":int(len(v)-v.nunique()),
            "raw_original_ID_values_emitted":False,
        }
    return {
        "source_RData_member":source_member,
        "source_R_object":r_object_name,
        "original_rows":int(df.shape[0]),
        "n_original_columns":int(df.shape[1]),
        "original_column_names":cols,
        "column_dtypes":{str(c):str(df[c].dtype) for c in df.columns},
        "candidate_individual_id_columns":ids,
        "candidate_time_columns":time,
        "candidate_decision_columns":decisions,
        "candidate_weather_columns":env,
        "aggregate_candidate_id_cardinality":unique_id_counts,
        "unresolved_same_individual_weather_decision_join":True,
        "no_model_fit_performed":True,
    }


def inspect_rdata_zip(path:Path)->dict:
    meta={
        "as_of":"2026-11-19",
        "source":"Rüppel et al. 2023 Royal Society Open Science 10:221420",
        "source_original_DOI":ORIGINAL_DOI,
        "provider_file_id":ZIP_PUBLISHED_FILE_ID,
        "original_provider_filename":ZIP_NAME,
        "validated_original_ZIP_SHA256":ZIP_SHA256,
        "original_file_bytes_verified":False,
        "original_RData_parser_supported":False,
        "original_RData_objects":[],
        "no_new_biological_effect":True,
        "no_original_bird_ID_row_export":True,
        "actual_individual_cue_beliefs_measured":False,
        "direct_theoretical_information_deadline":"NOT_IDENTIFIED",
        "source_same_bird_three_decision_fit_admitted":False,
        "source_status":"NOT_RUN",
    }
    with validate_zip(path) as archive:
        meta["original_file_bytes_verified"]=True
        meta["original_zip_member_metadata"]=[
            {"name":x.filename,"bytes_uncompressed":x.file_size,
             "compression":x.compress_type}
            for x in archive.infolist()
        ]
        rawcode=archive.read(SOURCE_CODE_MEMBER).decode("utf-8",errors="replace")
        meta["original_RMarkdown_audit"]={
            "n_lines":len(rawcode.splitlines()),
            "references_data_Event":bool(re.search(r"data\.Event",rawcode,re.I)),
            "references_flights":bool(re.search(r"\bflights\b",rawcode,re.I)),
            "n_merge_join_keywords":len(re.findall(
                r"\b(?:merge|left_join|inner_join|right_join|full_join|join)\s*\(",
                rawcode,flags=re.I
            )),
            "n_read_input_operations":len(re.findall(
                r"\b(?:readRDS|load|read\.csv|read_csv|read\.table)\s*\(",
                rawcode,flags=re.I
            )),
            "no_original_source_lines_exported":True,
        }
        with tempfile.TemporaryDirectory(prefix="payoff_b_figshare_RData_") as root:
            for member in MEMBERS:
                filepath=Path(root)/member
                filepath.write_bytes(archive.read(member))
                try:
                    objects=pyreadr.read_r(str(filepath))
                except Exception as error:
                    meta["source_status"]="ORIGINAL_RDATA_PARSER_UNSUPPORTED"
                    meta["parser_failed_original_member"]=member
                    meta["parser_error_type"]=type(error).__name__
                    return meta
                for objname,frame in objects.items():
                    if isinstance(frame,pd.DataFrame):
                        meta["original_RData_objects"].append(
                            dataframe_schema(frame,member,str(objname))
                        )
                    else:
                        meta["original_RData_objects"].append({
                            "source_RData_member":member,
                            "source_R_object":str(objname),
                            "python_type":type(frame).__name__,
                            "source_table_schema_unverified":True
                        })
    meta["original_RData_parser_supported"]=True
    if not meta["original_RData_objects"]:
        meta["source_status"]="ORIGINAL_RDATA_NO_SUPPORTED_FRAMES"
    else:
        meta["source_status"]="ORIGINAL_RDATA_TABLE_SCHEMAS_READ_JOIN_UNVERIFIED"
    return meta


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--original-zip",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    result=inspect_rdata_zip(a.original_zip)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "source_status":result["source_status"],
        "source_sha256_verified":result["original_file_bytes_verified"],
        "original_RData_names":[v["source_R_object"] for v in result["original_RData_objects"]],
        "n_original_RData_frames":len(result["original_RData_objects"]),
        "three_decision_join_authenticated":False,
        "new_biological_effect_fitted":False,
    },ensure_ascii=False))


if __name__=="__main__":
    main()
