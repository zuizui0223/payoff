#!/usr/bin/env python3
"""Inventory the Eurasian-wigeon subset in the public Zenodo raw GPS release.

Zenodo DOI: 10.5281/zenodo.16940654
Original Movebank study DOI: 10.5441/001/1.dv5mm289

The Zenodo release is curated by the same research group and identifies the
study by its Movebank study name/ID. This audit isolates that subset without
changing or resampling fixes.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


SOURCE = Path("external/wigeon/250823_LNU_dabbling_ducks_hourly.csv")
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

TARGET_STUDY = "Eurasian wigeon (Mareca penelope) Netherlands Lithuania 2018-2019"
SUPPLEMENT_SOURCE_STUDY_TOKENS = (
    "Eurasian wigeon",
    "Dabbling duck migration Lithuania 2019",
)


def main():
    if not SOURCE.exists():
        raise SystemExit(f"Missing raw Zenodo source: {SOURCE}")

    df = pd.read_csv(SOURCE, low_memory=False)
    required = [
        "study.name",
        "individual.id",
        "individual.taxon.canonical.name",
        "timestamp",
        "location.long",
        "location.lat",
        "ground.speed",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing expected columns: {missing}")

    study_names = sorted(
        x for x in df["study.name"].dropna().astype(str).unique()
        if "wigeon" in x.lower() or "penelope" in x.lower()
    )

    # The published supplementary code imports four tracking files, including
    # "Dabbling duck migration Lithuania 2019.csv" in addition to the files
    # labelled explicitly as Eurasian wigeon. Reconstruct that source union by
    # taxon + registered study-name tokens rather than by one exact study name.
    taxon = df["individual.taxon.canonical.name"].astype(str).str.lower()
    study = df["study.name"].astype(str)
    study_mask = False
    for token in SUPPLEMENT_SOURCE_STUDY_TOKENS:
        study_mask = study_mask | study.str.contains(
            token, case=False, regex=False, na=False
        )
    w = df[
        taxon.str.contains("penelope", regex=False, na=False)
        & study_mask
    ].copy()
    if w.empty:
        raise SystemExit(
            f"Published-source wigeon union not found. Candidates: {study_names}"
        )

    w["timestamp"] = pd.to_datetime(w["timestamp"], errors="coerce", utc=True)
    for c in ("location.long", "location.lat", "ground.speed"):
        w[c] = pd.to_numeric(w[c], errors="coerce")
    w["year"] = w["timestamp"].dt.year
    w["month"] = w["timestamp"].dt.month

    coord_ok = w["location.long"].notna() & w["location.lat"].notna()
    time_ok = w["timestamp"].notna()

    individual_summary = (
        w.groupby("individual.id")
        .agg(
            n_fixes=("timestamp", "size"),
            first_time=("timestamp", "min"),
            last_time=("timestamp", "max"),
            n_years=("year", "nunique"),
            min_lon=("location.long", "min"),
            max_lon=("location.long", "max"),
            min_lat=("location.lat", "min"),
            max_lat=("location.lat", "max"),
        )
        .reset_index()
    )
    individual_summary.to_csv(
        OUT / "stage3_wigeon_individual_source_summary.csv", index=False
    )

    # Keep only the target-study source rows as a derived analysis input artifact.
    # This is a subset of the public Zenodo data, not a modified trajectory.
    w.to_csv(OUT / "stage3_wigeon_raw_subset.csv", index=False)

    receipt = {
        "zenodo_doi": "10.5281/zenodo.16940654",
        "movebank_doi": "10.5441/001/1.dv5mm289",
        "primary_study_name": TARGET_STUDY,
        "registered_source_study_tokens": list(SUPPLEMENT_SOURCE_STUDY_TOKENS),
        "study_names_in_subset": sorted(
            str(x) for x in w["study.name"].dropna().unique()
        ),
        "study_ids": (
            sorted(str(x) for x in w["study.ID"].dropna().unique())
            if "study.ID" in w.columns
            else []
        ),
        "taxa": sorted(
            str(x) for x in w["individual.taxon.canonical.name"].dropna().unique()
        ),
        "n_rows": int(len(w)),
        "n_individuals": int(w["individual.id"].nunique()),
        "n_years": int(w["year"].nunique()),
        "years": sorted(int(x) for x in w["year"].dropna().unique()),
        "time_min": str(w["timestamp"].min()),
        "time_max": str(w["timestamp"].max()),
        "coordinate_complete_rows": int(coord_ok.sum()),
        "timestamp_complete_rows": int(time_ok.sum()),
        "ground_speed_nonmissing_rows": int(w["ground.speed"].notna().sum()),
        "longitude_range": [
            float(w["location.long"].min()),
            float(w["location.long"].max()),
        ],
        "latitude_range": [
            float(w["location.lat"].min()),
            float(w["location.lat"].max()),
        ],
        "source_columns": [str(x) for x in w.columns],
        "study_id_column_present": bool("study.ID" in w.columns),
        "candidate_wigeon_study_names": study_names,
        "claim_ceiling": (
            "Raw-source inventory only. Analytical spring tracks and staging "
            "events must reproduce the published filtering/HMM contract before "
            "controller inference."
        ),
    }
    (OUT / "stage3_wigeon_source_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, default=str))


if __name__ == "__main__":
    main()
