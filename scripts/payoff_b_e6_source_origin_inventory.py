#!/usr/bin/env python3
"""Audit original observation-source provenance, not phenology effect sizes.

Source-origin identified is NOT the same as certified eBird-free, and the
remaining unreviewed studies must not be silently converted to compliant.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import pandas as pd
from scripts.payoff_b_e6_known_ebird_exclusion import (
    SOURCE_STUDY_MARKER, read_verified_artifact
)

# Original journal/institution descriptions, never classified using an
# observed model coefficient or a confidence interval.
# marker, expected effect rows, observation origin, source public identifier
SOURCES = (
 ("Gordo, O. & Doi",130,"Japanese Meteorological Agency phenology stations","https://doi.org/10.3354/cr01099"),
 ("Murphy–Klassen",96,"Delta Marsh long-term local first-sighting series","https://doi.org/10.1093/auk/122.4.1130"),
 ("DeLeon, R.L.",93,"Buffalo Ornithological Society 1967-2008 first arrivals","https://doi.org/10.1525/cond.2011.100223"),
 ("Marra, P.P.",63,"Three North American mist-net and bird banding stations","https://pubmed.ncbi.nlm.nih.gov/15480801/"),
 ("Sokolov, L.V. (2006)",49,"Curonian Spit long-term migration and nesting monitoring","https://doi.org/10.1134/S0013873806010052"),
 ("Barrett, R.T.",42,"Northern Norway regional ornithological society arrival reports","https://doi.org/10.18710/4MCRQL"),
 ("Kolá?",40,"1828-1847 Bohemian Patriotic-Economic Society phenology stations","https://doi.org/10.3354/cr01290"),
 ("Hüppop, O. & Hüppop",24,"Helgoland bird trapping and ringing station","https://pmc.ncbi.nlm.nih.gov/articles/PMC1691241/"),
 ("Jenkins, D. & Sparks",22,"Aboyne local field observer David Jenkins phenology notes","https://nora.nerc.ac.uk/id/eprint/3392/"),
 ("Ellwood, E.R.",22,"Thoreau, Brewster, Griscom and Corey historical arrival logs to 2007","https://doi.org/10.1525/cond.2010.100006"),
 ("Jones, G.M.",2,"Project FeederWatch, distinct from eBird","https://feederwatch.org/explore/scientific-articles/the-early-bird-gets-earlier-a-phenological-shift-in-migration-timing-of-the-american-robin-turdus-migratorius-in-the-state-of-wisconsin/"),
 ("Askeyev, O.V.",26,"Kazan/Tatarstan 1988-2008 locally recorded first phenological events","https://doi.org/10.1111/j.1466-8238.2010.00566.x"),
 ("Nakata, M.",19,"Niigata coastal-forest bird-banding observations from 1989-2008","https://doi.org/10.3838/jjo.60.63"),
 ("Gunnarsson, T.G.",17,"Laugaras Iceland standardized daily first arrival field observation transect","https://doi.org/10.1080/00063657.2010.526999"),
 ("Christen, W.",12,"Solothurn Switzerland own constant-effort first-arrival field observation series 1981-2006","https://www.ala-schweiz.ch/images/stories/pdf/ob/2007_104/OrnitholBeob_2007_104_53_Christen.pdf"),
)

def inventory(d: pd.DataFrame) -> dict:
    if (len(d),d.Study.nunique(),d.Species.nunique())!=(944,28,279):
        raise ValueError("Original E6 effect, study or species count drift")
    mask=d.Study.astype(str).str.contains(SOURCE_STUDY_MARKER,regex=False,na=False)
    if mask.sum()!=264 or d.loc[mask,"Study"].nunique()!=1:
        raise ValueError("Already-proven eBird study identity changed")
    candidate=d.loc[~mask].copy()
    evidence=[]
    used=set()
    for marker,count,origin,url in SOURCES:
        matched=candidate.loc[candidate.Study.astype(str).str.contains(
            marker,regex=False,na=False)]
        if len(matched)!=count or matched.Study.nunique()!=1:
            raise ValueError("Original E6 source identifier or count changed: "+marker)
        study=str(matched.Study.iloc[0])
        if study in used:
            raise ValueError("Duplicate audit source class")
        used.add(study)
        evidence.append({
            "study":study,"source_marker":marker,
            "source_effect_rows":len(matched),
            "source_species":int(matched.Species.nunique()),
            "long_effect_rows":int((matched.Migration_distance=="long").sum()),
            "short_effect_rows":int((matched.Migration_distance=="short").sum()),
            "published_primary_observation_origin":origin,
            "independent_original_source_documentation":url,
            "classification":"ALTERNATIVE_PRIMARY_SOURCE_IDENTIFIED_NOT_FULLY_AUDITED",
        })
    unknown=candidate.loc[~candidate.Study.isin(used)]
    if (len(candidate),candidate.Study.nunique(),
        len(unknown),unknown.Study.nunique())!=(680,27,97,16):
        raise ValueError("Original 680-row source provenance partition changed")
    if sum(i["source_effect_rows"] for i in evidence)!=657:
        raise ValueError("Published source-origin coverage drift")
    return {
      "as_of":"2026-11-19",
      "status":"PARTIAL_ALTERNATIVE_PRIMARY_SOURCE_IDENTIFICATION_NOT_COMPLETE_EBIRD_AUDIT",
      "original_E6_effects":944,"original_studies":28,
      "known_eBird_study_effects_excluded":264,
      "remaining_after_forced_exclusion_effects":680,
      "remaining_after_forced_exclusion_studies":27,
      "studies_with_published_alternative_primary_observation_origin":11,
      "effects_with_published_alternative_primary_observation_origin":583,
      "fraction_of_remaining_effects_with_origin_documented":657/680,
      "studies_still_not_documented":16,
      "effects_still_not_documented":97,
      "source_specific_evidence":evidence,
      "unreviewed_study_bibliography":[str(s) for s in sorted(unknown.Study.unique())],
      "remaining_source_certified_fully_ebird_free":False,
      "no_new_temperature_effect_fit":True,
      "no_result_direction_based_source_selection":True,
      "no_new_independent_biological_confirmation":True,
    }

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--artifact-zip",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    ans=inventory(read_verified_artifact(args.artifact_zip))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(ans,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "origin_identified_effects":ans["effects_with_published_alternative_primary_observation_origin"],
      "origin_identified_studies":ans["studies_with_published_alternative_primary_observation_origin"],
      "unknown_effects":ans["effects_still_not_documented"],
      "unknown_studies":ans["studies_still_not_documented"],
      "certified_all_no_eBird":False
    },ensure_ascii=False))

if __name__=="__main__":
    main()
