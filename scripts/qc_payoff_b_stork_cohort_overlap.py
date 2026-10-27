#!/usr/bin/env python3
"""Verify published white-stork *cohort* reuse across distinct Movebank studies.

Rotics et al. 2016 juvenile+adult autumn (DOI 10.5441/001/1.hn1bd23k)
versus Rotics et al. 2018 adult longitudinal spring/reproduction
(10.5441/001/1.v8d24552, already opened in PAYOFF-B).

Stage uses original public CC0 source reference CSVs only, checked by exact
publisher file length/MD5. The overlapping individual-ID or ring-ID counts
are published as aggregate *only*, not original identifiers, study-sites
or GPS coordinates. An absence of exact identifiers does not prove
complete biological independence if studies reassign subject identifiers.
"""
from __future__ import annotations
import argparse,csv,json,tempfile
from collections import Counter
from pathlib import Path

from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_public_movebank_stork_breeding_2018 import (
    FILES, download_cc0, DOI as PREVIOUS_STORK_DOI,
)

NEW_DOI="10.5441/001/1.hn1bd23k"
NEW_REF={
    "uuid":"f5bfa548-4c4b-47c2-a842-3a6ae2e70cda",
    "size":43098,
    "md5":"b38407ed744cf2bd4806afce929f604a"
}
KEY_FIELDS=("animal-id","animal-ring-id","deployment-id","tag-id")
MISSING={"","NA","N/A","NULL","NONE","UNKNOWN","NOT AVAILABLE","NO DATA"}
REFERENCE_ROW_COUNTS={"new_autumn":122,"prior_adult":36}


def source_rows(path):
    with Path(path).open(encoding="utf-8-sig",errors="replace",newline="") as f:
        rdr=csv.DictReader(f)
        columns=rdr.fieldnames or []
        if not set(KEY_FIELDS).issubset(set(columns)):
            raise ValueError("Original reference does not have required identity fields")
        rows=list(rdr)
    return rows


def key(s):
    value=str(s or "").strip()
    return "" if value.upper() in MISSING else value


def compare_refs(new,old):
    if not new or not old:
        raise ValueError("No rows in one source reference")
    counts={}
    for field in KEY_FIELDS:
        a={key(r.get(field)) for r in new}-{""}
        b={key(r.get(field)) for r in old}-{""}
        shared=a&b
        counts[field]={
            "new_distinct_nonmissing_values":len(a),
            "previous_distinct_nonmissing_values":len(b),
            "overlapping_identifier_values":len(shared),
            "new_source_reference_rows_with_a_shared_identifier":
                sum(key(r.get(field)) in shared for r in new),
            "previous_source_reference_rows_with_a_shared_identifier":
                sum(key(r.get(field)) in shared for r in old),
        }
    shared_animals=counts["animal-id"]["overlapping_identifier_values"]
    shared_ring=counts["animal-ring-id"]["overlapping_identifier_values"]
    shared_deploy=counts["deployment-id"]["overlapping_identifier_values"]
    shared_tag=counts["tag-id"]["overlapping_identifier_values"]
    direct_reuse=(shared_animals>0 or shared_ring>0 or shared_deploy>0)
    stages={}
    for label,rows in (("new_autumn",new),("prior_adult",old)):
        stages[label]={
            "source_reference_rows":len(rows),
            "life_stage_counts":dict(sorted(Counter(
                key(x.get("animal-life-stage")) or "UNSPECIFIED"
                for x in rows).items())),
            "deployment_end_type_counts":dict(sorted(Counter(
                key(x.get("deployment-end-type")) or "UNSPECIFIED"
                for x in rows).items())),
            "reference_fields_include_death_comments":
                any("death" in k for k in rows[0]),
            "recorded_death_end_type_is_individual_fitness_time_series":False,
        }
    return {
        "original_published_reference_row_counts":stages,
        "original_identifier_overlap_by_field":counts,
        "shared_exact_animal_or_ring_or_deployment_identifier":direct_reuse,
        "shared_tag_ID_indicates_same_animal_not_guaranteed":shared_tag>0,
        "cohort_verdict":
            "DO_NOT_COUNT_AS_INDEPENDENT_PUBLISHED_COHORT_ID_OVERLAP"
            if direct_reuse else
            "NO_EXACT_PUBLISHED_ID_COLLISION_BIOLOGICAL_INDEPENDENCE_UNVERIFIED",
        "published_fitness_endpoint_join_ready":False,
        "cohort_independence_proven":False,
        "sensitive_animal_IDs_ring_IDs_locations_exported":False,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=Path("outputs/payoff_b_stork_overlap"))
    args=p.parse_args()
    record={
        "schema":"payoff_b_stork_2016_2018_public_cohort_overlap_v1",
        "new_source_doi":NEW_DOI,
        "previous_payoff_source_doi":PREVIOUS_STORK_DOI,
        "comparison_before_juvenile_fall_GPS_outcome_opened":True,
    }
    try:
        with tempfile.TemporaryDirectory() as d:
            new=Path(d)/"2016_stork_reference.csv"
            old=Path(d)/"2018_stork_reference.csv"
            snew=download_verified(NEW_REF,new)
            sold=download_cc0("reference",old)
            rowsnew,rowsold=source_rows(new),source_rows(old)
            expected=REFERENCE_ROW_COUNTS
            if len(rowsnew)!=expected["new_autumn"] or len(rowsold)!=expected["prior_adult"]:
                raise ValueError("Original published reference source row counts drift")
            record["source_file_checksum"]=dict(new_autumn=snew,prior_adult=sold)
            record["source_comparison"]=compare_refs(rowsnew,rowsold)
            record["status"]="ORIGINAL_PUBLIC_IDENTITY_RELATION_AUDIT_COMPLETE"
    except (OSError,ValueError,TypeError) as e:
        record["status"]="SOURCE_OR_IDENTITY_GATE_FAILED"
        record["error"]=type(e).__name__+": "+str(e)[:280]
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"stork_2016_versus_2018.json").write_text(
        json.dumps(record,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(record,indent=2,ensure_ascii=False))
    if record["status"]!="ORIGINAL_PUBLIC_IDENTITY_RELATION_AUDIT_COMPLETE":
        raise SystemExit("Original CC0 subject-ID comparison failed")

if __name__=="__main__":main()
