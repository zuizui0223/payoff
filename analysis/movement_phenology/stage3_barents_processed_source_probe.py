#!/usr/bin/env python3
"""Inventory Barents/Svalbard Barnacle Goose data in the Boom & Kissling processed tracking release."""

from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

SOURCE = Path("external/barnacle_processed/ProcessedTrackingData_MakingBeterUseOfTrackingData_2023.csv")
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = {
    "barents": "10.5441/001/1.ps244r11",
    "svalbard": "10.5441/001/1.5k6b1364",
}


def find_col(cols, candidates):
    lowered = {str(c).lower(): c for c in cols}
    for x in candidates:
        if x.lower() in lowered:
            return lowered[x.lower()]
    for c in cols:
        lc = str(c).lower()
        if any(x.lower() in lc for x in candidates):
            return c
    return None


def main():
    if not SOURCE.exists():
        raise SystemExit(f"Missing {SOURCE}")
    df = pd.read_csv(SOURCE, low_memory=False)

    dscol = find_col(df.columns, ["datasetID", "dataset.id", "datasetid"])
    if dscol is None:
        raise SystemExit(f"No datasetID-like column. Columns={list(df.columns)}")

    tcol = find_col(df.columns, ["eventDate", "timestamp", "eventdate"])
    idcol = find_col(df.columns, ["organismID", "individual", "organismid"])
    latcol = find_col(df.columns, ["decimalLatitude", "location.lat", "latitude"])
    loncol = find_col(df.columns, ["decimalLongitude", "location.long", "longitude"])

    receipt = {
        "source_rows": int(len(df)),
        "source_columns": [str(c) for c in df.columns],
        "dataset_id_column": str(dscol),
        "timestamp_column": None if tcol is None else str(tcol),
        "individual_column": None if idcol is None else str(idcol),
        "latitude_column": None if latcol is None else str(latcol),
        "longitude_column": None if loncol is None else str(loncol),
        "targets": {},
    }

    for name, doi in TARGETS.items():
        mask = df[dscol].astype(str).str.lower().str.contains(
            doi.lower(), regex=False, na=False
        )
        x = df[mask].copy()
        if x.empty:
            # Some Darwin Core exports use the DOI URL rather than bare DOI.
            token = doi.split("/")[-1].lower()
            x = df[
                df[dscol].astype(str).str.lower().str.contains(
                    token, regex=False, na=False
                )
            ].copy()

        if tcol is not None:
            ts = pd.to_datetime(x[tcol], errors="coerce", utc=True)
        else:
            ts = pd.Series(pd.NaT, index=x.index)

        rec = {
            "doi": doi,
            "n_rows": int(len(x)),
            "n_individuals": (
                int(x[idcol].nunique(dropna=True))
                if idcol is not None and len(x) else None
            ),
            "n_years": int(ts.dt.year.nunique()) if ts.notna().any() else None,
            "years": (
                sorted(int(y) for y in ts.dt.year.dropna().unique())
                if ts.notna().any() else []
            ),
            "time_min": str(ts.min()) if ts.notna().any() else None,
            "time_max": str(ts.max()) if ts.notna().any() else None,
        }
        if latcol is not None and loncol is not None and len(x):
            lat = pd.to_numeric(x[latcol], errors="coerce")
            lon = pd.to_numeric(x[loncol], errors="coerce")
            rec["coordinate_complete_rows"] = int((lat.notna() & lon.notna()).sum())
            rec["lat_range"] = [float(lat.min()), float(lat.max())]
            rec["lon_range"] = [float(lon.min()), float(lon.max())]
        receipt["targets"][name] = rec

        if len(x):
            x.to_csv(OUT / f"stage3_{name}_processed_tracking_subset.csv", index=False)

    (OUT / "stage3_barents_processed_source_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, default=str))


if __name__ == "__main__":
    main()
