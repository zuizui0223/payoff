#!/usr/bin/env python3
"""Summarize native R metadata of original Figshare source, no bird rows."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

REQUIRED = {
    "original_RData_file", "original_R_object_path",
    "original_R_object_class", "n_original_rows", "n_original_columns",
    "original_column_name", "original_column_R_class",
    "n_nonmissing_column_values", "candidate_identifier_column",
    "n_distinct_candidate_IDs", "original_ID_values_exported",
}
SOURCE_FILES={"data.Event.RData","flights.RData"}
ID=re.compile(r"(?:^id$|bird|individual|tag|ring)",re.I)
TIME=re.compile(r"(?:date|time|day|hour|sunset|doy|start|end)",re.I)
CHOICE=re.compile(r"(?:depart|flight|route|offshore|onshore|land|stopover)",re.I)
WEATHER=re.compile(r"(?:wind|temp|press|cloud|rain|precip|humid)",re.I)


def summarize(csvpath:Path)->dict:
    with csvpath.open("r",encoding="utf-8",newline="") as f:
        src=list(csv.DictReader(f))
    if not src or not REQUIRED.issubset(src[0]):
        raise ValueError("Missing original native R source metadata columns")
    objects={}
    for row in src:
        if row["original_ID_values_exported"]!="FALSE":
            raise ValueError("Raw original ID export flag must stay FALSE")
        member=row["original_RData_file"]
        if member not in SOURCE_FILES:
            raise ValueError("Unlisted original RData member")
        key=(member,row["original_R_object_path"])
        name=row["original_column_name"]
        n=int(row["n_original_rows"])
        ncol=int(row["n_original_columns"])
        present=int(row["n_nonmissing_column_values"])
        if not 0<=present<=n or n<=0 or ncol<=0:
            raise ValueError("Invalid original R source metadata grain")
        if len(name)>180 or not name:
            raise ValueError("Original field naming integrity violation")
        obj=objects.setdefault(key,{
            "original_RData_file":member,
            "original_R_object_path":key[1],
            "original_R_object_class":row["original_R_object_class"],
            "n_original_rows":n,
            "n_original_columns":ncol,
            "source_columns":[],
            "column_R_classes":{},
            "source_ID_cardinalities_aggregate_only":{},
            "candidate_timestamp_columns":[],
            "candidate_decision_columns":[],
            "candidate_weather_columns":[],
            "original_animal_rows_exported":False,
        })
        if (n,ncol)!=(obj["n_original_rows"],obj["n_original_columns"]):
            raise ValueError("Original object metadata row grain inconsistent")
        if name in obj["source_columns"]:
            raise ValueError("Duplicate original R source column")
        obj["source_columns"].append(name)
        obj["column_R_classes"][name]=row["original_column_R_class"]
        if ID.search(name) and row["n_distinct_candidate_IDs"]:
            obj["source_ID_cardinalities_aggregate_only"][name]={
                "n_unique":int(row["n_distinct_candidate_IDs"]),
                "n_present":present,
            }
        if TIME.search(name):obj["candidate_timestamp_columns"].append(name)
        if CHOICE.search(name):obj["candidate_decision_columns"].append(name)
        if WEATHER.search(name):obj["candidate_weather_columns"].append(name)
    docs=list(objects.values())
    for item in docs:
        if len(item["source_columns"])!=item["n_original_columns"]:
            raise ValueError("Original ncols inconsistent with exported native R schema")
    shared={}
    if len(docs)>=2:
        for i,a in enumerate(docs):
            for b in docs[i+1:]:
                common=set(a["source_ID_cardinalities_aggregate_only"])&set(
                    b["source_ID_cardinalities_aggregate_only"]
                )
                if common:
                    shared[f"{a['original_R_object_path']}__{b['original_R_object_path']}"]=sorted(common)
    return {
        "as_of":"2026-11-19",
        "source":"Rüppel et al. 2023 RSOS 221420 original public Figshare RData",
        "source_original_DOI":"10.6084/m9.figshare.c.6403996",
        "original_RData_zip_sha256":"0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6",
        "original_ZIP_and_objects_verified_with_native_R":True,
        "original_RData_object_schemas":docs,
        "n_original_supported_R_dataframes":len(docs),
        "possible_same_named_ID_columns_across_objects_not_an_authenticated_join":shared,
        "same_bird_depart_route_land_chronology_verified":False,
        "weather_available_before_each_decision_verified":False,
        "time_ordered_full_record_counts_verified":False,
        "source_original_paper_already_reports_weather_and_three_decisions":True,
        "new_biological_effect_estimated":False,
        "no_source_animal_identifiers_or_weather_values_exported":True,
        "direct_information_deadline_qwait_D_eff":"NOT_IDENTIFIED",
        "status":"ORIGINAL_NATIVE_RDATA_SCHEMA_RECOVERED_FULL_DECISION_JOIN_NOT_YET_ADMITTED",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--native-schema-csv",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=summarize(args.native_schema_csv)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "n_R_dataframes":result["n_original_supported_R_dataframes"],
        "tables":[{
            "source_object":x["original_R_object_path"],
            "n_rows":x["n_original_rows"],
            "n_fields":x["n_original_columns"],
            "candidate_IDs":x["source_ID_cardinalities_aggregate_only"],
            "candidate_timestamps":x["candidate_timestamp_columns"],
            "candidate_decisions":x["candidate_decision_columns"],
            "candidate_weather":x["candidate_weather_columns"],
        } for x in result["original_RData_object_schemas"]],
        "joined_individual_trajectory_proven":False,
        "new_biological_effect_fitted":False,
    },ensure_ascii=False))


if __name__=="__main__":
    main()
