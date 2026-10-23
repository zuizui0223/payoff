#!/usr/bin/env python3
"""Read-only source availability audit for public CC0 duck/woodcock archives.

Curated *before* event access from the full Movebank parent/source inventory.
GPS and Argos files for woodcock remain separate rather than pooled or
counted as independent biological individuals.
"""
from __future__ import annotations
import argparse,hashlib,json,tempfile
from pathlib import Path
from scripts.qc_public_movebank_crossguild import download_verified,audit

SOURCE = {
 "dabbling_ducks": dict(
     doi="10.5441/001/1.3fv21n7m",
     taxon="Anas acuta; Anas platyrhynchos",
     paper="10.1098/rspb.2018.1734",
     context="waterfowl_virus_dispersal_migration_source",
     uuid="3b2a830b-27eb-471b-a1f3-8d7e1a0f41f1",
     md5="f1a104040111ba4aab992af7b612f494",
     size=128003020, original_sensor="GPS"),
 "woodcock_gps": dict(
     doi="10.5441/001/1.8764q39q",taxon="Scolopax minor",
     paper="SOURCE_PAPER_DOI_IN_ARCHIVE",
     context="woodcock_same_cohort_gps_sensor_stream",
     uuid="b5e83cf2-89fe-49c6-b57e-0774cf6dcc9f",
     md5="bac25a200462103a8208684fb3569364",
     size=51019, original_sensor="GPS"),
 "woodcock_argos": dict(
     doi="10.5441/001/1.8764q39q",taxon="Scolopax minor",
     paper="SOURCE_PAPER_DOI_IN_ARCHIVE",
     context="woodcock_same_cohort_argos_doppler_stream",
     uuid="e47ebe4e-dd6f-43d6-8daa-879b1b1d4700",
     md5="175c57d323b1dcbc673979c95bc61dcc",
     size=6124844, original_sensor="Argos Doppler Shift")
}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--system",required=True,choices=sorted(SOURCE))
    p.add_argument("--out",type=Path,default=Path("outputs/payoff_b_crossguild_v2"))
    args=p.parse_args()
    row=SOURCE[args.system]
    report={
        "system":args.system,"source_doi":row["doi"],
        "declared_publisher_taxa":row["taxon"],
        "sensor_stream":row["original_sensor"],
        "source_context":row["context"],
        "license":"CC0-1.0",
        "individuals_unique_across_GPS_and_Argos":"NOT_ESTIMATED",
        "published_tracking_phenology_effect":"PRIOR_ART_NOT_A_NEW_PAYOFF_RESULT",
        "information_actionability_fitness_hypothesis":"NOT_TESTED",
    }
    try:
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/"public_publisher_stream.csv"
            report["verified_source"]=download_verified(row,file)
            report["coverage"]=audit(file)
            report["status"]="SOURCE_COVERAGE_VERIFIED"
    except (OSError,ValueError) as e:
        report["status"]="SOURCE_ADMISSION_FAILED"
        report["error"]=type(e).__name__+": "+str(e)[:350]
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/(args.system+".json")).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    if report["status"]!="SOURCE_COVERAGE_VERIFIED":
        raise SystemExit("source admission failed")

if __name__=="__main__":main()
