#!/usr/bin/env python3
"""Forced source-provenance correction to pre-existing E6 meta-regression.

The Hurlbert & Liang 2012 effect rows are explicitly eBird-derived.
Exclude that entire study BEFORE the corrected fit; keep original 944-row
fit only to audit exact reproduction. Other source studies unaudited.
No original eBird checklists or new ecological causal effects.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from scripts.payoff_b_cross_system_information import (
    model_matrix, term_summary, two_way_cluster_wls,
)

ARTIFACT_SHA = "443cab62531d9b633aa6ee67da010fa66b6c230ef87e919d697269e77a7373f0"
DERIVED_ROW_SHA = "817a2d2d18931944103283c93e4d9bf80568906a21a92369ee168e4f8f203085"
SOURCE_SHA = "68816f6cbfccbb9b47b45be0df49f077db914c8e43e567d0ed2cac9bbafde56c"
SOURCE_STUDY_MARKER = "Hurlbert, A.H. & Liang, Z. (2012)"
KNOWN_EBIRD_STUDY_DOI = "10.1371/journal.pone.0031662"
REQUIRED = {
    "Study", "Species", "Migration_distance", "Slope", "SE",
    "Response_variable", "Temperature_location", "Arrival_location",
    "Data_source", "Continent",
}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_verified_artifact(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(path)
    if _sha(path.read_bytes()) != ARTIFACT_SHA:
        raise ValueError("Frozen E6 GitHub artifact ZIP digest changed")
    with zipfile.ZipFile(path) as z:
        rows = z.read("bird_temperature_short_long_rows.csv")
    if _sha(rows) != DERIVED_ROW_SHA:
        raise ValueError("Frozen E6 derived 944-row CSV digest changed")
    d = pd.read_csv(io.BytesIO(rows))
    if not REQUIRED.issubset(d.columns):
        raise ValueError("Frozen E6 source rows have missing model columns")
    if (len(d) != 944 or d["Study"].nunique() != 28
            or d["Species"].nunique() != 279):
        raise ValueError("Frozen E6 source unit count drift")
    return d


def refit(d: pd.DataFrame) -> dict:
    if len(d) < 15:
        raise ValueError("Insufficient original published E6 effect rows")
    X, terms = model_matrix(d, adjusted=True)
    weights = 1.0 / np.square(d["SE"].to_numpy(float))
    fit = two_way_cluster_wls(
        d["Slope"].to_numpy(float), X, weights,
        d["Study"].astype(str).to_numpy(),
        d["Species"].astype(str).to_numpy(),
    )
    summary = term_summary(fit, terms, "long_minus_short")
    return {
        "estimate_days_per_C_long_minus_short":summary["estimate"],
        "SE":summary["se"],
        "ci95":summary["ci95"],
        "p":summary["p"],
        "degrees_of_freedom":summary["df"],
        "n_effects":fit["n"],
        "studies":fit["clusters_study"],
        "species":fit["clusters_species"],
        "number_of_adjusted_model_columns":len(terms),
    }


def provenance_sensitivity(rows: pd.DataFrame) -> dict:
    if not REQUIRED.issubset(rows):
        raise ValueError("Original E6 reconstruction columns missing")
    if (len(rows) != 944 or rows.Study.nunique() != 28
            or rows.Species.nunique() != 279):
        raise ValueError("Original frozen E6 sample changed")
    baseline = refit(rows)
    if abs(baseline["estimate_days_per_C_long_minus_short"] -
           0.4214763799092083)>1e-9:
        raise ValueError("Original E6 WLS refit failed prior published estimate")
    expected_original_ci = (0.12132570573851081,0.7216270540799057)
    if any(abs(x-y)>1e-8 for x,y in zip(baseline["ci95"],expected_original_ci)):
        raise ValueError("Original E6 confidence interval refit failed")
    mask = rows["Study"].astype(str).str.contains(
        SOURCE_STUDY_MARKER, regex=False, na=False)
    matched_studies=rows.loc[mask,"Study"].unique()
    if len(matched_studies)!=1 or int(mask.sum())!=264:
        raise ValueError("Known eBird study identity/count not source-verified")
    n_long=int((rows.loc[mask,"Migration_distance"]=="long").sum())
    n_short=int((rows.loc[mask,"Migration_distance"]=="short").sum())
    if (n_long,n_short)!=(190,74):
        raise ValueError("Known eBird source migration class rows changed")
    remaining=rows.loc[~mask].copy()
    corrected=refit(remaining)
    if len(remaining)!=680 or remaining.Study.nunique()!=27:
        raise ValueError("Wrong source-policy panel after study exclusion")
    result={
        "status":"KNOWN_EBIRD_STUDY_EXCLUDED_FULL_REMAINING_SOURCE_AUDIT_PENDING",
        "as_of":"2026-11-19",
        "prior_e6_workflow_run":36383988920,
        "prior_e6_artifact_id":10953792024,
        "artifact_sha256":ARTIFACT_SHA,
        "derived_temperature_rows_sha256":DERIVED_ROW_SHA,
        "original_Usui_source_sha256":SOURCE_SHA,
        "model":"original E6 inverse variance WLS, Study x Species two-way clustered CI, 27/26 df",
        "original_E6_before_source_policy_correction":baseline,
        "excluded_study":{
            "source_marker":SOURCE_STUDY_MARKER,
            "original_study_DOI":KNOWN_EBIRD_STUDY_DOI,
            "verified_original_source_uses_eBird":True,
            "source_rows":264,
            "long_distance_rows":n_long,
            "short_distance_rows":n_short,
            "unique_species_in_excluded_study":int(rows.loc[mask,"Species"].nunique()),
            "excluded_for_sign_or_p_value":False,
        },
        "after_excluding_one_known_ebird_source":corrected,
        "no_eBird_free_panel_certified":True,
        "remaining_original_studies_needing_source_provenance_audit":27,
        "independent_new_discovery":False,
        "direct_information_distance_causation_identified":False,
        "V7_geographical_q_by_U_primary_outcome_opened":False,
    }
    return result


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--artifact-zip",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=provenance_sensitivity(read_verified_artifact(args.artifact_zip))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "full":result["original_E6_before_source_policy_correction"],
        "without_known_ebird":result["after_excluding_one_known_ebird_source"],
        "remaining_source_studies_not_yet_verified":27
    },ensure_ascii=False))


if __name__=="__main__":
    main()
