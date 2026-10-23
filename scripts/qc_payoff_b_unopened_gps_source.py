#!/usr/bin/env python3
"""Verify two unopened migratory-bird CC0 GPS sources BEFORE cue-effect fitting.

These are original Movebank public bitstreams, pinned by exact byte length
and original MD5 before ANY position or timestamp is parsed. Report grouped
source-only coverage and spring source-departure eligibility, not ecological
responses, exact tracks, IDs, locations, or endangerment-sensitive sites.
"""
from __future__ import annotations
import argparse,csv,json,tempfile
from pathlib import Path

from scripts.qc_public_movebank_crossguild import download_verified,audit
from scripts.qc_payoff_b_predecision_candidates import (
    daily_source_positions, source_audit
)

SOURCES={
    "pinkfoot_goose": {
        "doi":"10.5441/001/1.s9s86319",
        "taxon":"Anser brachyrhynchus",
        "published_study_id":"49535504",
        "paper":"10.1111/jav.00899",
        "uuid":"7e1620db-de92-431a-bdf5-0148a5955684",
        "md5":"fe4fe726c7d4c31aadedbe9f067c41f2",
        "size":2102567,
        "study_context":"spring_stopover_fuel_accumulation_prior_art",
        "license":"CC0 1.0 Universal"
    },
    "egyptian_vulture": {
        "doi":"10.5441/001/1.385gk270",
        "taxon":"Neophron percnopterus",
        "published_study_id":"9651291",
        "paper":"10.1007/s10531-018-1538-6",
        "uuid":"63385ce4-d174-4f08-89cf-fa8d37785073",
        "md5":"578c45678d402d055000ea14e754b6da",
        "size":122069657,
        "study_context":"long_distance_summer_winter_range_and_conservation_prior_art",
        "license":"CC0 1.0 Universal"
    }
}

MIN_IDENTITIES_WITH_SPRING_FIXES=8
MIN_SOURCE_ANIMAL_YEARS_WITH_CANDIDATES=10
MIN_FROZEN_FIVE_DAY_SOURCE_CANDIDATES=10


def source_status(fix_summary, candidate_summary, original_taxon):
    taxa = candidate_summary["classified_source_taxa"]
    if set(taxa) and set(taxa)!={original_taxon}:
        return "NOT_ADMITTED_TAXON_MISMATCH"
    if not set(taxa):
        return "NOT_ADMITTED_NO_SPRING_SOURCE_TRACKS"
    tax=taxa[original_taxon]
    n=tax.get("animal_years_with_geovalid_days",0)
    c=tax.get("candidate_stationary_to_northward_events",0)
    a=tax.get("animal_years_with_one_or_more_candidates",0)
    if n<MIN_IDENTITIES_WITH_SPRING_FIXES:
        return "NOT_ADMITTED_FEW_SPRING_ANIMAL_YEARS"
    if c<MIN_FROZEN_FIVE_DAY_SOURCE_CANDIDATES or a<MIN_SOURCE_ANIMAL_YEARS_WITH_CANDIDATES:
        return "NOT_ADMITTED_INSUFFICIENT_FIXED_DEPARTURE_OPPORTUNITIES"
    return "CANDIDATE_STAGEWISE_MIGRATION_SOURCE_GEOMETRY"


def run_one(system):
    if system not in SOURCES:
        raise ValueError("Undeclared original public CC0 source")
    source=SOURCES[system]
    with tempfile.TemporaryDirectory() as directory:
        gps=Path(directory)/"original_published_source.csv"
        origin=download_verified(source,gps)
        total=audit(gps)
        groups,other,idcol=daily_source_positions(gps,source["taxon"])
        source_gate=source_audit(groups,other,idcol)
        return {
            "system":system,
            "original_doi":source["doi"],
            "publication_doi":source["paper"],
            "published_study_id":source["published_study_id"],
            "expected_taxon":source["taxon"],
            "license_metadata":source["license"],
            "original_movement_context":source["study_context"],
            "original_checksum_and_bytes":origin,
            "all_years_and_seasons_source_coverage":total,
            "fixed_feb_may_3day_stationary_then_2day_north_source_gate":source_gate,
            "biological_source_readiness":source_status(total,source_gate,source["taxon"]),
            "source_gate_thresholds":{
                "min_geovalid_spring_animal_years":MIN_IDENTITIES_WITH_SPRING_FIXES,
                "min_fixed_northward_source_events":MIN_FROZEN_FIVE_DAY_SOURCE_CANDIDATES,
                "min_animal_years_with_source_events":MIN_SOURCE_ANIMAL_YEARS_WITH_CANDIDATES
            },
            "actual_bird_departure_timestamp_verified":False,
            "actual_cue_available_before_decision":False,
            "independent_animal_cohort_overlap_verified":False,
            "downstream_timing_fitness_endpoint_measured":False,
            "individual_IDs_or_GPS_locations_exported":False,
            "status":"PUBLIC_SOURCE_GPS_QC_COMPLETE",
        }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--system",required=True,choices=sorted(SOURCES))
    parser.add_argument("--out",type=Path,default=Path("outputs/payoff_b_unopened_gps_qc"))
    args=parser.parse_args()
    record={
        "schema":"payoff_b_unopened_public_CC0_spring_source_qc_v1",
        "reporting":"AGGREGATE_ORIGINAL_SOURCE_COVERAGE_ONLY",
        "system":args.system,
    }
    try:record["result"]=run_one(args.system)
    except (ValueError,OSError,TypeError) as e:
        record["result"]={"status":"ORIGINAL_GPS_SOURCE_QC_ERROR",
                          "error":type(e).__name__+": "+str(e)[:280]}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/(args.system+".json")).write_text(json.dumps(record,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(record,indent=2,ensure_ascii=False))
    if record["result"]["status"]!="PUBLIC_SOURCE_GPS_QC_COMPLETE":
        raise SystemExit("Public source checksum or schema gate failed")

if __name__=="__main__":main()
