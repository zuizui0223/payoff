#!/usr/bin/env python3
"""POST-OPEN provenance-tier sensitivities for existing Usui E6 effects.

Nested sample exclusions are determined by original observation-source
documentation, never the effect coefficient or its p-value. An identified
local source is NOT proof that all auxiliary streams were eBird-free. No
causal cue or migration deadline inference is licensed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from scripts.payoff_b_e6_known_ebird_exclusion import (
    read_verified_artifact, provenance_sensitivity, refit,
)
from scripts.payoff_b_e6_source_origin_inventory import inventory


LOWER_SOURCE_EVIDENCE_LEVEL = (
    "PUBLISHED_SITE_LEVEL_CONTEXT_BUT_RAW_OBSERVATION_CUSTODIAN_NOT_VERIFIED"
)

def provenance_tier_sensitivity(d: pd.DataFrame) -> dict:
    inv = inventory(d)
    prior = provenance_sensitivity(d)
    if (
        inv["remaining_after_forced_exclusion_effects"] != 680
        or inv["studies_with_published_alternative_primary_observation_origin"] != 26
        or inv["effects_with_published_alternative_primary_observation_origin"] != 676
        or inv["studies_still_not_documented"] != 1
        or inv["effects_still_not_documented"] != 4
    ):
        raise ValueError("Original provenance-tier source partition changed")
    described_studies = {item["study"] for item in inv["source_specific_evidence"]}
    strong_studies = {
        item["study"] for item in inv["source_specific_evidence"]
        if item.get("record_evidence_level") != LOWER_SOURCE_EVIDENCE_LEVEL
    }
    if len(described_studies) != 26 or len(strong_studies) != 24:
        raise ValueError("Source evidence tiers unexpectedly changed")
    named_source = d.loc[d["Study"].isin(described_studies)].copy()
    explicit_programme = d.loc[d["Study"].isin(strong_studies)].copy()
    if (
        len(named_source), named_source.Study.nunique(),
        len(explicit_programme), explicit_programme.Study.nunique()
    ) != (676, 26, 670, 24):
        raise ValueError("Source tiers have wrong original study membership")
    # The actual refit formula, weights and two-way clustering remain the
    # exact original E6 routines. The 944 original rows are used only to
    # certify reproduction; the effect is not promoted as eBird-independent.
    all_known_eBird_excluded = prior["after_excluding_one_known_ebird_source"]
    results = {
        "as_of":"2026-11-19",
        "status":"NESTED_POST_OPEN_SOURCE_PROVENANCE_SENSITIVITY_NOT_EBIRD_FREE_CERTIFICATION",
        "original_input":"Original GitHub E6 result artifact 10953792024, SHA256 verified by shared loader",
        "comparisons":{
            "original_published_E6_provenance_only":prior["original_E6_before_source_policy_correction"],
            "verified_known_eBird_study_removed_680":all_known_eBird_excluded,
            "published_local_source_described_676":refit(named_source),
            "more_explicit_observation_programme_670":refit(explicit_programme),
        },
        "excluded_known_eBird_effects":264,
        "additional_unattributed_original_source_effects_excluded_from_676":4,
        "additional_weak_original_log_custodian_effects_excluded_from_670":6,
        "unverified_Lithuanian_source":"Zalakevicius 2002 GeoJournal 57:183-193; 4 effects",
        "weaker_source_custodian_studies":["Rubolini et al. 2007","Ahola et al. 2004"],
        "other_original_source_streams_independently_fully_checked":False,
        "no_claim_of_fully_eBird_free_panel":True,
        "no_new_independent_biological_effect":True,
        "no_new_causal_information_access_or_deadline_estimate":True,
        "source_selection_based_on_coefficient_direction":False,
        "original_V7_goose_qxU_still_not_estimable":True,
        "interpretation":"Nested same-source E6 robustness to explicit source-provenance selection; not a new biological study, causation or complete eBird clearance.",
    }
    return results


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--artifact-zip",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    result=provenance_tier_sensitivity(read_verified_artifact(args.artifact_zip))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "model_676":result["comparisons"]["published_local_source_described_676"],
        "model_670":result["comparisons"]["more_explicit_observation_programme_670"],
        "ebird_free_certified":False,
    },ensure_ascii=False))

if __name__=="__main__":
    main()
