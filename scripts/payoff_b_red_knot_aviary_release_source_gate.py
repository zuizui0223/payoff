#!/usr/bin/env python3
"""2025 original red-knot randomized aviary and departure source-grain check.

Exact original SHA256 public Figshare data/code/README, no biological model.
Exports ONLY treatment×year counts, nonmissing outcome cardinalities, and
boolean evidence of aviary-level source definitions. Never original bird IDs,
departure dates, release dates, mass trajectories, locations or source lines.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import re
from collections import defaultdict
from pathlib import Path
import requests

SOURCE_URL="https://doi.org/10.6084/m9.figshare.28660718"
ARTICLE_DOI="10.1111/1365-2435.70183"
FILES={
 "4.combined_data.csv":(
    53244101,24894,"755833eb13e241def834f12ea2c8d775ec643def807b23a4b3695ee7805e834f"),
 "6.statistical_analyses.R":(
    53244107,58726,"07ba64cc5fe97ddb0af13763e6869303b99e67997a035c2f63af5628951d89fd"),
 "README.txt":(
    53244110,4654,"d624be841db09cfb58cbe85fffaa39ae2262cbfbca60e68f196f8aef75155cbc"),
}
REQUEST_CAP=100_000
ALLOWED_YEARS={"2021","2022","2023"}
ALLOWED_HOURS={"6","12","24"}


def fetch_verified(session:requests.Session,filename:str)->bytes:
    file_id,expected_size,digest=FILES[filename]
    url=f"https://figshare.com/ndownloader/files/{file_id}"
    with session.get(url,timeout=(12,40),stream=True) as response:
        if response.status_code!=200:
            raise ValueError(f"Original Figshare {filename} HTTP_{response.status_code}")
        if int(response.headers.get("Content-Length",0) or 0)>REQUEST_CAP:
            raise ValueError("Original Figshare file exceeds bounded source cap")
        raw=bytearray()
        for chunk in response.iter_content(8192):
            raw.extend(chunk)
            if len(raw)>REQUEST_CAP:
                raise ValueError("Original Figshare stream beyond bounded source cap")
    if len(raw)!=expected_size or hashlib.sha256(raw).hexdigest()!=digest:
        raise ValueError("Original Figshare source identity size/SHA256 changed")
    return bytes(raw)


def normalize_hour(value:str)->str | None:
    if value is None:return None
    s=str(value).strip().lower().replace(" ","")
    s=re.sub(r"(?:hours|hour|hrs|hr|h)/?day$","",s)
    s=re.sub(r"(?:hours|hour|hrs|hr|h)$","",s)
    return s if s in ALLOWED_HOURS else None


def analyze_original_table(raw:bytes)->dict:
    try:text=raw.decode("utf-8-sig")
    except UnicodeDecodeError:text=raw.decode("cp1252")
    reader=csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ValueError("Original experimental source lacks header")
    fields=set(reader.fieldnames)
    expected={"BirdID.year","year","treatment","release_date",
              "departed","departure","departure_jul"}
    if not expected.issubset(fields):
        raise ValueError("Original experimental bird-year/source outcome schema drift")
    if any("aviary" in f.lower() or "cage" in f.lower()
           or "enclosure" in f.lower() for f in fields):
        aviary_columns=[f for f in fields if re.search(r"aviary|cage|enclosure",f,re.I)]
    else:aviary_columns=[]
    rows=list(reader)
    if len(rows)!=102:
        raise ValueError("Original combined_data.csv size 102 rows changed")
    b_ids=[r["BirdID.year"] for r in rows]
    if len(set(b_ids))!=102 or not all(b_ids):
        raise ValueError("Original bird-year key missing or duplicated")
    years={str(r["year"]).strip() for r in rows}
    treatments={str(r["treatment"]).strip() for r in rows}
    hour_mappings={t:normalize_hour(t) for t in treatments}
    year_status="SOURCE_2021_2023_LABELS_VERIFIED" if years==ALLOWED_YEARS else "SOURCE_YEAR_ENCODING_NOT_EXACTLY_2021_2023"
    treatment_status="SOURCE_HOURS_6_12_24_VERIFIED" if (
        set(hour_mappings.values())==ALLOWED_HOURS and None not in hour_mappings.values()
    ) else "SOURCE_TREATMENT_CODES_NEED_ORIGINAL_README_MAPPING"
    by_year={}
    for yr in sorted(years):
        subset=[r for r in rows if str(r["year"]).strip()==yr]
        by_year[yr] if False else None
        # Do not output original unknown year codes; only recognized calendar
        # year labels are safe grouped metadata with defensible semantics.
        if year_status!="SOURCE_2021_2023_LABELS_VERIFIED":
            continue
        record={
            "n_original_source_rows":len(subset),
            "source_release_date_present":sum(bool(str(r["release_date"]).strip()) for r in subset),
            "source_departed_indicator_present":sum(bool(str(r["departed"]).strip()) for r in subset),
            "source_departure_date_present":sum(bool(str(r["departure"]).strip()) for r in subset),
            "source_departure_julian_present":sum(bool(str(r["departure_jul"]).strip()) for r in subset),
            "per_treatment":{}
        }
        for tr in sorted(treatments):
            key=hour_mappings.get(tr)
            if key is None or treatment_status!="SOURCE_HOURS_6_12_24_VERIFIED":
                continue
            a=[r for r in subset if str(r["treatment"]).strip()==tr]
            record["per_treatment"][key]={
                "n_original_rows":len(a),
                "release_date_nonmissing":sum(bool(str(r["release_date"]).strip()) for r in a),
                "departed_flag_nonmissing":sum(bool(str(r["departed"]).strip()) for r in a),
                "departure_date_nonmissing":sum(bool(str(r["departure"]).strip()) for r in a),
            }
        by_year[yr]=record
    out={
        "original_source_combined_rows":len(rows),
        "n_source_bird_year_keys":len(set(b_ids)),
        "original_source_variables":list(reader.fieldnames),
        "n_original_year_categories":len(years),
        "year_code_status":year_status,
        "n_original_treatment_categories":len(treatments),
        "treatment_code_status":treatment_status,
        "source_aviary_or_cage_membership_columns":aviary_columns,
        "actual_author_specific_aviary_id_per_individual_verified":False,
        "source_year_treatment_release_and_departure_aggregate":by_year,
        "source_n_original_release_date_nonmissing":sum(bool(str(r["release_date"]).strip()) for r in rows),
        "source_n_original_departed_flag_nonmissing":sum(bool(str(r["departed"]).strip()) for r in rows),
        "source_n_original_departure_date_nonmissing":sum(bool(str(r["departure"]).strip()) for r in rows),
        "source_n_original_departure_julian_nonmissing":sum(bool(str(r["departure_jul"]).strip()) for r in rows),
        "original_bird_identifiers_or_dates_exported":False,
        "missing_departure_assumed_a_nondeparture":False,
    }
    return out


def codebook_aviary_mentions(readme:bytes,code:bytes)->dict:
    def summarize(s):
        source=s.decode("utf-8",errors="replace")
        return {
            "n_original_lines":len(source.splitlines()),
            "n_aviary_mentions":len(re.findall(r"\baviar(?:y|ies)\b",source,re.I)),
            "n_cage_enclosure_mentions":len(re.findall(r"\b(?:cage|enclosure)\b",source,re.I)),
            "n_treatment_mentions":len(re.findall(r"\btreatment\b",source,re.I)),
            "n_explicit_aviary_by_year_model_tokens":len(re.findall(r"\b(?:frailty|cluster)\s*\(|\(\s*1\s*\|\s*(?:aviary|cage)",source,re.I)),
            "source_code_lines_exported":False,
        }
    return {
        "original_readme_summary":summarize(readme),
        "original_analysis_R_summary":summarize(code),
        "aviary_membership_for_each_individual_proven_by_text_search":False,
    }


def audit(session)->dict:
    original={}
    for name in FILES:
        original[name]=fetch_verified(session,name)
    table=analyze_original_table(original["4.combined_data.csv"])
    codebook=codebook_aviary_mentions(original["README.txt"],
                                     original["6.statistical_analyses.R"])
    if table["original_source_combined_rows"]!=102:
        raise ValueError("Original source combined rows invalid")
    pilot=table["source_year_treatment_release_and_departure_aggregate"].get("2021")
    pilot_departs=int(pilot["source_departure_date_present"]) if pilot else None
    aviary_verified=False
    status="AVIARY_LEVEL_TREATMENT_EFFECT_REANALYSIS_NOT_ESTIMABLE"
    # Never derive an aviary ID from BirdID, year, capture site, sex or
    # ambiguous treatment groups; such a mapping requires author codebook.
    return {
        "as_of":"2026-11-20",
        "source_original_paper":ARTICLE_DOI,
        "original_public_Figshare_DOI":"10.6084/m9.figshare.28660718",
        "source_file_sha256_checks_passed":{
            name:{"file_id":fid,"exact_sha256":digest,"file_size_bytes":size}
            for name,(fid,size,digest) in FILES.items()},
        "source_original_table":table,
        "readme_and_original_statistical_codebook_audit":codebook,
        "2021_pilot_tracked_departures_absent_supported_by_table":(
            pilot is not None and pilot_departs==0
        ),
        "aviary_mapping_independently_authenticated":aviary_verified,
        "study_design_gate":status,
        "no_new_treatment_effect_fitted":True,
        "original_published_6_12_24h_food_departure_effect_prior_art":True,
        "subjective_anticipated_environmental_information_measured":False,
        "biological_information_deadline_q_x_actionability_identified":False,
        "no_original_source_animal_data_export":True,
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    result=audit(requests.Session())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    safe=result["source_original_table"]
    print(json.dumps({
        "status":result["study_design_gate"],
        "original_bird_year_rows":safe["original_source_combined_rows"],
        "year_code_status":safe["year_code_status"],
        "treatment_code_status":safe["treatment_code_status"],
        "year_treatment_counts":safe["source_year_treatment_release_and_departure_aggregate"],
        "aviary_fields_present":safe["source_aviary_or_cage_membership_columns"],
        "pilot_no_departure":result["2021_pilot_tracked_departures_absent_supported_by_table"],
        "new_biological_effects":0,
    },ensure_ascii=False))


if __name__=="__main__":
    main()
