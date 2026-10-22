#!/usr/bin/env python3
"""Published CC0 reference-only audit of unopened 2021 multi-study goose source.

No GPS, bird identities, coordinates, dates or animal-level data are exported.
A distinct DataCite DOI is not evidence for a distinct biological cohort.
"""
from __future__ import annotations
import argparse,csv,json,re,tempfile
from pathlib import Path
from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_public_movebank_geese_2016 import download_public_bitstream,DOI as PRIOR_DOI

DOI="10.5441/001/1.254rd102"
REFERENCE=dict(uuid="320fd6d1-0dfc-4ddd-ad17-46427a026291",
               size=3369,md5="c69d2d3f7365b6efc2d7335a153dbdf8")
README=dict(uuid="fd5684d9-88c5-4c30-a017-88acdbc1551b",
            size=19282,md5="8edc618cdba5e36611ac5d7fe1691486")
PUBLISHED_STUDIES={"9589196","44083081"}
PUBLISHED_MANIFEST_REFERENCE_FILES=1
EXPECTED_REFERENCE_ROWS=14
FIELDS=("animal-id","animal-ring-id","deployment-id","tag-id","tag-serial-no")
MISSING={"","na","n/a","null","none","unknown","not available","no data","nan"}


def rows(path):
    with Path(path).open(newline="",encoding="utf-8-sig",errors="replace") as h:
        r=csv.DictReader(h)
        if not {"animal-id","tag-id"}.issubset(set(r.fieldnames or [])):
            raise ValueError("Published reference lacks essential ID columns")
        return list(r)


def normal(v):
    s=str(v or "").strip()
    return "" if s.casefold() in MISSING else s


def subject_overlap(new,old):
    result={}
    for field in FIELDS:
        if field not in new[0] or field not in old[0]:
            result[field]={"status":"UNCOMPARABLE_MISSING_PUBLISHER_FIELD"}
            continue
        a={normal(r.get(field)) for r in new}-{""}
        b={normal(r.get(field)) for r in old}-{""}
        intersection=a&b
        result[field]={
            "status":"EXACT_PUBLISHED_ID_COMPARISON",
            "new_distinct_nonblank":len(a),"old_distinct_nonblank":len(b),
            "common_identifier_values":len(intersection),
            "new_rows_with_shared_ID":sum(normal(r.get(field)) in intersection for r in new),
            "old_rows_with_shared_ID":sum(normal(r.get(field)) in intersection for r in old),
        }
    collision=any(result[k].get("common_identifier_values",0)>0
                  for k in ("animal-id","animal-ring-id","deployment-id"))
    return {
        "new_reference_rows":len(new),
        "old_reference_rows":len(old),
        "per_field":result,
        "exact_animal_ring_or_deployment_ID_collision":collision,
        "shared_tag_alone_does_not_identify_same_animal":True,
        "true_biological_independence_established":False,
        "raw_identifiers_exported":False,
    }


def parse_readme(s):
    plain=s.replace("\\_","_")
    studies=set(re.findall(r"(?i)Movebank Study ID\s+(\d+)",plain))
    lines=[x.strip() for x in plain.splitlines()]
    gps={x for x in lines if x.endswith("_part-gps.csv")}
    ref={x for x in lines if x.endswith("_part-reference-data.csv")}
    return {
        "original_study_ID_count":len(studies),
        "expected_study_IDs_complete":studies==PUBLISHED_STUDIES,
        "readme_GPS_files":len(gps),"readme_reference_files":len(ref),
        "published_manifest_accessible_reference_files":PUBLISHED_MANIFEST_REFERENCE_FILES,
        "readme_reference_files_exceed_manifest":
            len(ref)>PUBLISHED_MANIFEST_REFERENCE_FILES,
        "single_study_source":len(studies)==1,
    }


def run():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        new=root/"new.csv";old=root/"old.csv";readme=root/"readme.txt"
        verified={
            "new_reference":download_verified(REFERENCE,new),
            "new_readme":download_verified(README,readme),
            "old_reference":download_public_bitstream("reference",old),
        }
        rnew,rold=rows(new),rows(old)
        if len(rnew)!=EXPECTED_REFERENCE_ROWS:
            raise ValueError("Published 2021 14-row source reference changed")
        manifest=parse_readme(readme.read_text(encoding="utf-8-sig",errors="replace"))
        if not manifest["expected_study_IDs_complete"]:
            raise ValueError("Original 2021 Movebank Study IDs changed")
        overlap=subject_overlap(rnew,rold)
        incomplete=manifest["readme_reference_files_exceed_manifest"]
        return {
            "new_data_doi":DOI,"prior_data_doi":PRIOR_DOI,
            "original_source_checksums":verified,
            "publisher_reported_animals":20,
            "readme_and_manifest":manifest,
            "exact_old_source_identifier_overlap":overlap,
            "independent_replication_admission":
                "NOT_ADMITTED_EXACT_ANIMAL_OR_DEPLOYMENT_COLLISION"
                if overlap["exact_animal_ring_or_deployment_ID_collision"]
                else "NOT_ADMITTED_MULTISTUDY_REFERENCE_INCOMPLETE"
                if incomplete or not manifest["single_study_source"]
                else "COHORT_INDEPENDENCE_STILL_NOT_VERIFIED",
            "new_large_GPS_downloaded":False,
            "meteorology_or_behavioral_effects_opened":False,
            "original_animal_IDs_dates_locations_exported":False,
        }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=Path("outputs/payoff_b_goose_cohort_gate"))
    a=p.parse_args()
    receipt={"schema":"payoff_b_unopened_2021_multistudy_goose_reference_QC_v1"}
    try:
        receipt["result"]=run()
        receipt["status"]="SOURCE_ONLY_REFERENCE_INTEGRITY_COMPLETE"
    except (OSError,ValueError,TypeError) as e:
        receipt["status"]="SOURCE_ONLY_REFERENCE_GATE_FAILED"
        receipt["error"]=type(e).__name__+": "+str(e)[:300]
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"2021_vs_2016.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
    if receipt["status"]!="SOURCE_ONLY_REFERENCE_INTEGRITY_COMPLETE":
        raise SystemExit("Published 2021 goose reference check failed")

if __name__=="__main__":main()
