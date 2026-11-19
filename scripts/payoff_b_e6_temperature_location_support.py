#!/usr/bin/env python3
"""Published Usui E6 source-only support: no migration slope modeling.

The only use of source Slope and SE is to select the exact 944 rows from the
pre-existing, already published E6 contract. No new outcome coefficients or
per-row temperature responses are emitted. This is NOT an animal cue-use test.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

SOURCE_SHA256 = "68816f6cbfccbb9b47b45be0df49f077db914c8e43e567d0ed2cac9bbafde56c"
EXPECTED = {"rows": 944, "studies": 28, "species": 279}
FROZEN_SOURCE = "https://zenodo.org/records/4970634"
COLUMNS = (
    "Study", "Species", "Migration_distance", "Predictor",
    "Slope", "SE", "Temperature_location"
)


def source_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1024*1024), b""):
            h.update(part)
    return h.hexdigest()


def exact_e6_selection(data: pd.DataFrame) -> pd.DataFrame:
    missing = set(COLUMNS) - set(data.columns)
    if missing:
        raise ValueError(f"Missing original E6 columns: {sorted(missing)}")
    x = data.copy()
    x["Predictor"] = x["Predictor"].astype(str).str.lower()
    x["Migration_distance"] = x["Migration_distance"].astype(str).str.lower()
    x["Slope"] = pd.to_numeric(x["Slope"], errors="coerce")
    x["SE"] = pd.to_numeric(x["SE"], errors="coerce")
    x = x.loc[
        x["Predictor"].eq("temperature")
        & x["Migration_distance"].isin(["short", "long"])
        & np.isfinite(x["Slope"]) & np.isfinite(x["SE"])
        & (x["SE"] > 0)
    ].copy()
    if (
        len(x) != EXPECTED["rows"]
        or x["Study"].nunique() != EXPECTED["studies"]
        or x["Species"].nunique() != EXPECTED["species"]
    ):
        raise ValueError(
            "Exact frozen E6 source selection drift: "
            f"rows={len(x)}, studies={x['Study'].nunique()}, "
            f"species={x['Species'].nunique()}"
        )
    return x


def design_support(x: pd.DataFrame) -> dict:
    """Audit literal source temperature-location levels without a fitted slope."""
    if any(c not in x for c in ("Study","Species","Migration_distance","Temperature_location")):
        raise ValueError("Missing design-only fields")
    d = x[["Study","Species","Migration_distance","Temperature_location"]].copy()
    d["Temperature_location"] = d["Temperature_location"].fillna(
        "(original_missing_value)"
    ).astype(str)
    d["Migration_distance"] = d["Migration_distance"].astype(str)
    if not d["Migration_distance"].isin(["short","long"]).all():
        raise ValueError("Only frozen short/long classes admitted")
    raw_levels = sorted(d["Temperature_location"].unique().tolist())
    if len(raw_levels) > 32:
        raise ValueError("Unexpected location code proliferation")
    by_level=[]
    for level in raw_levels:
        z=d.loc[d["Temperature_location"] == level]
        by_dist={}
        for distance in ("short","long"):
            sub=z.loc[z["Migration_distance"] == distance]
            by_dist[distance]={
                "rows":int(len(sub)),
                "studies":int(sub["Study"].nunique()),
                "species":int(sub["Species"].nunique()),
            }
        mixed=[]
        for st,g in z.groupby("Study"):
            if {"short","long"}.issubset(set(g["Migration_distance"])):
                mixed.append(str(st))
        by_level.append({
            "verbatim_source_Temperature_location":level,
            "rows":int(len(z)),
            "studies":int(z["Study"].nunique()),
            "species":int(z["Species"].nunique()),
            "by_migration_distance":by_dist,
            "n_studies_containing_both_distances_at_location":len(mixed),
            # No study names nor species identities are published in this audit.
        })
    two_loc_support=[]
    for first,second in itertools.combinations(raw_levels,2):
        eligible=[]
        for st,g in d.groupby("Study"):
            cells=set(zip(g["Temperature_location"],g["Migration_distance"]))
            required={(first,"short"),(first,"long"),
                      (second,"short"),(second,"long")}
            if required.issubset(cells):
                eligible.append(st)
        z=d.loc[d["Temperature_location"].isin([first,second])]
        shares=z["Study"].value_counts(normalize=True)
        two_loc_support.append({
            "source_level_a":first,
            "source_level_b":second,
            "n_studies_with_all_four_cells":len(eligible),
            "n_studies_any_of_two_levels":int(z["Study"].nunique()),
            "largest_one_study_fraction_rows_at_two_levels":(
                float(shares.iloc[0]) if not shares.empty else None
            ),
            "candidate_2x2_within_study_requirement_n5":len(eligible)>=5,
        })
    return {
        "source":FROZEN_SOURCE,
        "analysis":"SOURCE_DESIGN_ONLY_NO_SLOPE_OR_SE_RESULTS_OPENED",
        "frozen_bird_E6_rows":len(x),
        "frozen_bird_E6_studies":int(x["Study"].nunique()),
        "frozen_bird_E6_species":int(x["Species"].nunique()),
        "original_literal_temperature_location_levels":by_level,
        "all_unordered_location_level_pairs":two_loc_support,
        "n_level_pairs_meeting_5_fully_crossed_studies":sum(
            v["candidate_2x2_within_study_requirement_n5"] for v in two_loc_support),
        "no_location_near_vs_far_recode_selected":True,
        "no_animal_cue_use_observed":True,
        "no_new_biological_interaction_fitted":True,
        "do_not_claim_information_distance_causality":True,
        "gate_status":"SOURCE_SUPPORT_ONLY_NOT_PROSPECTIVE_CAUSAL_TEST",
    }


def audit(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    digest=source_sha(path)
    if digest != SOURCE_SHA256:
        raise ValueError(f"Source original SHA256 mismatch: {digest}")
    try:
        raw=pd.read_csv(path,encoding="utf-8")
    except UnicodeDecodeError:
        raw=pd.read_csv(path,encoding="cp1252")
    out=design_support(exact_e6_selection(raw))
    out["source_verified_sha256"]=digest
    out["raw_source_total_rows"]=len(raw)
    return out


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",required=True,type=Path)
    ap.add_argument("--output",required=True,type=Path)
    args=ap.parse_args()
    result=audit(args.input)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",
        encoding="utf-8"
    )
    print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))


if __name__=="__main__":
    main()
