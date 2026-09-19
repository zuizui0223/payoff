#!/usr/bin/env python3
"""Normalize the public Eurasian-wigeon source data for controller reconstruction.

Provenance source:
  original Movebank ORIGINAL bundle for DOI 10.5441/001/1.dv5mm289

Canonical HMM-replication source:
  public Zenodo hourly union DOI 10.5281/zenodo.16940654

The paper Supplement loaded four tracking files and then regularized them to
one- or two-hour schedules. The current Movebank ORIGINAL bundle is a much
higher-frequency raw export and does not reproduce that analytical input when
used directly. Therefore the curated hourly Zenodo union is preferred for HMM
replication, while the original Movebank bundle is retained as source provenance
and a fallback only if the hourly union is unavailable.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ORIGINAL = Path("external/wigeon_original/wigeon_original_gps.csv")
ZENODO = Path("external/wigeon/250823_LNU_dabbling_ducks_hourly.csv")
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

TARGET_STUDY = "Eurasian wigeon (Mareca penelope) Netherlands Lithuania 2018-2019"
SUPPLEMENT_SOURCE_STUDY_TOKENS = (
    "Eurasian wigeon",
    "Dabbling duck migration Lithuania 2019",
)


def find_col(columns, candidates, *, required=True):
    lower = {str(c).lower(): c for c in columns}
    for name in candidates:
        hit = lower.get(name.lower())
        if hit is not None:
            return hit
    for c in columns:
        lc = str(c).lower()
        if any(name.lower() in lc for name in candidates):
            return c
    if required:
        raise ValueError(
            f"Missing column among candidates={candidates}; columns={list(columns)}"
        )
    return None


def normalize_original(df: pd.DataFrame) -> pd.DataFrame:
    """Map standard Movebank columns to the internal wigeon contract."""
    t = find_col(df.columns, ["timestamp", "eventDate", "event-date"])
    lon = find_col(
        df.columns,
        ["location-long", "location_long", "decimalLongitude", "longitude"],
    )
    lat = find_col(
        df.columns,
        ["location-lat", "location_lat", "decimalLatitude", "latitude"],
    )
    ind = find_col(
        df.columns,
        [
            "individual-local-identifier",
            "individual_local_identifier",
            "organismID",
            "individual.id",
            "individual",
        ],
    )
    speed = find_col(
        df.columns,
        ["ground-speed", "ground_speed", "ground.speed", "speed"],
    )
    taxon = find_col(
        df.columns,
        [
            "individual-taxon-canonical-name",
            "individual_taxon_canonical_name",
            "individual.taxon.canonical.name",
            "taxon-canonical-name",
        ],
        required=False,
    )
    study = find_col(
        df.columns,
        ["study-name", "study_name", "study.name"],
        required=False,
    )
    study_id = find_col(
        df.columns,
        ["study-id", "study_id", "study.id"],
        required=False,
    )

    out = pd.DataFrame(
        {
            "study.name": (
                df[study].astype(str)
                if study is not None
                else TARGET_STUDY
            ),
            "study.id": (
                df[study_id].astype(str)
                if study_id is not None
                else ""
            ),
            "individual.id": df[ind].astype(str),
            "individual.taxon.canonical.name": (
                df[taxon].astype(str)
                if taxon is not None
                else "Anas penelope"
            ),
            "timestamp": df[t],
            "location.long": df[lon],
            "location.lat": df[lat],
            "ground.speed": df[speed],
        }
    )
    return out


def normalize_zenodo(df: pd.DataFrame) -> pd.DataFrame:
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
        raise ValueError(f"Missing expected Zenodo columns: {missing}")

    taxon = df["individual.taxon.canonical.name"].astype(str).str.lower()
    study = df["study.name"].astype(str)
    study_mask = pd.Series(False, index=df.index)
    for token in SUPPLEMENT_SOURCE_STUDY_TOKENS:
        study_mask = study_mask | study.str.contains(
            token, case=False, regex=False, na=False
        )

    w = df[
        taxon.str.contains("penelope", regex=False, na=False)
        & study_mask
    ].copy()
    if w.empty:
        raise ValueError(
            "Published-source wigeon union not found in Zenodo release"
        )

    if "study.id" not in w.columns:
        w["study.id"] = ""
    return w[required + ["study.id"]].copy()


def clean_normalized(w: pd.DataFrame) -> pd.DataFrame:
    w = w.copy()
    w["timestamp"] = pd.to_datetime(
        w["timestamp"], errors="coerce", utc=True
    )
    for c in ("location.long", "location.lat", "ground.speed"):
        w[c] = pd.to_numeric(w[c], errors="coerce")
    w = w.dropna(
        subset=[
            "individual.id",
            "timestamp",
            "location.long",
            "location.lat",
            "ground.speed",
        ]
    ).copy()
    w["year"] = w["timestamp"].dt.year
    w["month"] = w["timestamp"].dt.month
    return w


def source_choice():
    """Prefer the hourly supplement-like union; retain original raw as audit."""
    original_error = None
    original_available = False
    if ORIGINAL.exists() and ORIGINAL.stat().st_size > 0:
        try:
            raw_original = pd.read_csv(ORIGINAL, low_memory=False, nrows=1000)
            _ = normalize_original(raw_original)
            original_available = True
        except Exception as exc:
            original_error = f"{type(exc).__name__}:{exc}"

    if ZENODO.exists() and ZENODO.stat().st_size > 0:
        raw = pd.read_csv(ZENODO, low_memory=False)
        w = clean_normalized(normalize_zenodo(raw))
        if len(w) > 0:
            return (
                "ZENODO_SUPPLEMENT_UNION_HOURLY",
                ZENODO,
                w,
                original_error,
                original_available,
            )

    if original_available:
        raw = pd.read_csv(ORIGINAL, low_memory=False)
        w = clean_normalized(normalize_original(raw))
        return (
            "ORIGINAL_MOVEBANK_FALLBACK",
            ORIGINAL,
            w,
            original_error,
            original_available,
        )

    raise SystemExit(
        f"Neither supplement-like hourly union nor usable original source exists. "
        f"Original error={original_error}; Zenodo exists={ZENODO.exists()}"
    )


def main():
    lane, source_path, w, original_error, original_available = source_choice()

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

    # Canonical normalized analysis input. Downstream code never needs to know
    # which acquisition lane succeeded.
    w.to_csv(OUT / "stage3_wigeon_raw_subset.csv", index=False)

    receipt = {
        "movebank_doi": "10.5441/001/1.dv5mm289",
        "zenodo_fallback_doi": "10.5281/zenodo.16940654",
        "source_lane": lane,
        "source_path": str(source_path),
        "original_source_available": bool(original_available),
        "original_source_error_if_any": original_error,
        "primary_study_name": TARGET_STUDY,
        "registered_source_study_tokens": list(
            SUPPLEMENT_SOURCE_STUDY_TOKENS
        ),
        "study_names_in_subset": sorted(
            str(x) for x in w["study.name"].dropna().unique()
        ),
        "study_ids": sorted(
            str(x) for x in w["study.id"].dropna().unique()
            if str(x) and str(x).lower() != "nan"
        ),
        "taxa": sorted(
            str(x)
            for x in w["individual.taxon.canonical.name"].dropna().unique()
        ),
        "n_rows": int(len(w)),
        "n_individuals": int(w["individual.id"].nunique()),
        "n_years": int(w["year"].nunique()),
        "years": sorted(int(x) for x in w["year"].dropna().unique()),
        "time_min": str(w["timestamp"].min()),
        "time_max": str(w["timestamp"].max()),
        "coordinate_complete_rows": int(
            (
                w["location.long"].notna()
                & w["location.lat"].notna()
            ).sum()
        ),
        "timestamp_complete_rows": int(w["timestamp"].notna().sum()),
        "ground_speed_nonmissing_rows": int(
            w["ground.speed"].notna().sum()
        ),
        "longitude_range": [
            float(w["location.long"].min()),
            float(w["location.long"].max()),
        ],
        "latitude_range": [
            float(w["location.lat"].min()),
            float(w["location.lat"].max()),
        ],
        "normalized_columns": [str(x) for x in w.columns],
        "claim_ceiling": (
            "Normalized supplement-like hourly analysis source; the original "
            "Movebank raw bundle is audited separately. Controller inference remains "
            "gated on replication of the published track/HMM/staging summaries "
            "and environmental TGS reconstruction."
        ),
    }
    (OUT / "stage3_wigeon_source_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, default=str))


if __name__ == "__main__":
    main()
