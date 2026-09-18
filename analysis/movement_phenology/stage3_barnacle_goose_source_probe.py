#!/usr/bin/env python3
"""Inventory the public Svalbard barnacle-goose Movebank Data Repository files.

The bitstream URLs are documented by the movepub package vignette for DOI
10.5441/001/1.5k6b1364. This probe does not infer stopovers or environmental
phase yet; it freezes the raw schema needed for a direct-controller rebuild.
"""

from __future__ import annotations

import gzip
import io
import json
from pathlib import Path
import zipfile

import pandas as pd


GPS = Path("external/barnacle_goose_svalbard/gps.csv")
REF = Path("external/barnacle_goose_svalbard/reference.csv")
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)


def read_any(path: Path) -> pd.DataFrame:
    """Parse plain, compressed, or oddly encoded Movebank tabular bitstreams."""
    raw = path.read_bytes()

    payloads: list[tuple[str, bytes]] = []
    if raw.startswith(b"PK"):
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            for name in zf.namelist():
                if not name.endswith("/"):
                    payloads.append((name, zf.read(name)))
    elif raw.startswith(b"\x1f\x8b"):
        payloads.append((path.name, gzip.decompress(raw)))
    else:
        payloads.append((path.name, raw))

    errors = []
    for name, payload in payloads:
        for encoding in ("utf-8-sig", "utf-16", "latin-1"):
            try:
                text = payload.decode(encoding)
            except Exception as exc:
                errors.append(f"{name}:{encoding}:decode:{exc}")
                continue
            for sep in (",", "\t", ";"):
                try:
                    df = pd.read_csv(
                        io.StringIO(text), sep=sep, low_memory=False
                    )
                    if df.shape[1] > 1:
                        return df
                except Exception as exc:
                    errors.append(f"{name}:{encoding}:{sep}:{exc}")

    magic = raw[:32].hex()
    raise RuntimeError(
        f"Could not parse {path}; size={len(raw)} magic={magic}; "
        + " | ".join(errors[-8:])
    )


def find_column(columns, candidates):
    lower = {str(c).lower(): c for c in columns}
    for cand in candidates:
        if cand.lower() in lower:
            return lower[cand.lower()]
    for c in columns:
        lc = str(c).lower()
        if any(cand.lower() in lc for cand in candidates):
            return c
    return None


def main() -> None:
    if not GPS.exists() or not REF.exists():
        raise SystemExit("Missing downloaded Movebank files")

    gps = read_any(GPS)
    ref = read_any(REF)

    tcol = find_column(gps.columns, ["timestamp", "event timestamp"])
    idcol = find_column(
        gps.columns,
        ["individual-local-identifier", "individual local identifier", "individual", "tag-local-identifier"],
    )
    latcol = find_column(gps.columns, ["location-lat", "latitude"])
    loncol = find_column(gps.columns, ["location-long", "longitude"])

    time_min = None
    time_max = None
    n_years = None
    if tcol is not None:
        ts = pd.to_datetime(gps[tcol], errors="coerce", utc=True)
        if ts.notna().any():
            time_min = str(ts.min())
            time_max = str(ts.max())
            n_years = int(ts.dt.year.nunique())

    n_individuals = None
    if idcol is not None:
        n_individuals = int(gps[idcol].nunique(dropna=True))

    coord_complete = None
    if latcol is not None and loncol is not None:
        coord_complete = int(
            (pd.to_numeric(gps[latcol], errors="coerce").notna()
             & pd.to_numeric(gps[loncol], errors="coerce").notna()).sum()
        )

    inventory = {
        "dataset_doi": "10.5441/001/1.5k6b1364",
        "gps_rows": int(len(gps)),
        "gps_columns": [str(c) for c in gps.columns],
        "reference_rows": int(len(ref)),
        "reference_columns": [str(c) for c in ref.columns],
        "timestamp_column": None if tcol is None else str(tcol),
        "individual_column": None if idcol is None else str(idcol),
        "latitude_column": None if latcol is None else str(latcol),
        "longitude_column": None if loncol is None else str(loncol),
        "n_individuals_from_gps": n_individuals,
        "n_years_from_gps": n_years,
        "time_min": time_min,
        "time_max": time_max,
        "coordinate_complete_rows": coord_complete,
        "gps_head": gps.head(5).astype(object).where(pd.notna(gps.head(5)), None).to_dict(orient="records"),
        "reference_head": ref.head(5).astype(object).where(pd.notna(ref.head(5)), None).to_dict(orient="records"),
    }

    (OUT / "stage3_barnacle_goose_svalbard_source_inventory.json").write_text(
        json.dumps(inventory, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    pd.DataFrame(
        [
            {
                "dataset_doi": inventory["dataset_doi"],
                "gps_rows": inventory["gps_rows"],
                "gps_ncols": len(inventory["gps_columns"]),
                "reference_rows": inventory["reference_rows"],
                "reference_ncols": len(inventory["reference_columns"]),
                "n_individuals_from_gps": inventory["n_individuals_from_gps"],
                "n_years_from_gps": inventory["n_years_from_gps"],
                "time_min": inventory["time_min"],
                "time_max": inventory["time_max"],
                "coordinate_complete_rows": inventory["coordinate_complete_rows"],
                "timestamp_column": inventory["timestamp_column"],
                "individual_column": inventory["individual_column"],
            }
        ]
    ).to_csv(
        OUT / "stage3_barnacle_goose_svalbard_source_inventory.csv",
        index=False,
    )

    print(json.dumps(inventory, indent=2, default=str))


if __name__ == "__main__":
    main()
