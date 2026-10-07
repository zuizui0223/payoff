#!/usr/bin/env python3
"""Fit frozen q_B local vegetation-phase observability from AppEEARS results."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.appeears_irg_ingest import (
    mod09q1_v061_quality_good,
    ndvi_from_scaled_reflectance,
    parse_appeears_date,
    resolve_column,
)
from src.qb_local_observability import (
    PixelNDVI,
    aggregate_region_composites,
    fit_region_observability,
)


def _float(value):
    try:
        return float(str(value).strip())
    except Exception:
        return float("nan")


def _int(value, fill=65535):
    try:
        x = float(str(value).strip())
        return int(x) if math.isfinite(x) else fill
    except Exception:
        return fill


def load_mod09_csv(path: Path, point_to_region: dict[str, str]):
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            return rows, False
        headers = list(reader.fieldnames)
        try:
            point_col = resolve_column(
                headers,
                exact_aliases=("ID", "pixel_id"),
            )
            date_col = resolve_column(
                headers,
                exact_aliases=("Date", "date"),
            )
            red_col = resolve_column(
                headers,
                suffix_aliases=("MOD09Q1_061_sur_refl_b01", "sur_refl_b01"),
            )
            nir_col = resolve_column(
                headers,
                suffix_aliases=("MOD09Q1_061_sur_refl_b02", "sur_refl_b02"),
            )
            qc_col = resolve_column(
                headers,
                suffix_aliases=(
                    "MOD09Q1_061_sur_refl_qc_250m",
                    "sur_refl_qc_250m",
                ),
            )
            state_col = resolve_column(
                headers,
                suffix_aliases=(
                    "MOD09Q1_061_sur_refl_state_250m",
                    "sur_refl_state_250m",
                ),
            )
        except ValueError:
            return rows, False

        for line, row in enumerate(reader, start=2):
            point_id = str(row[point_col]).strip()
            if point_id not in point_to_region:
                raise ValueError(
                    f"unknown AppEEARS point id {point_id!r} in {path}:{line}"
                )
            date = parse_appeears_date(str(row[date_col]))
            red = _float(row[red_col])
            nir = _float(row[nir_col])
            qc = _int(row[qc_col])
            state = _int(row[state_col])
            ndvi = ndvi_from_scaled_reflectance(red, nir)
            quality = mod09q1_v061_quality_good(qc, state)
            if ndvi is None:
                quality = False
                ndvi = float("nan")
            rows.append(
                PixelNDVI(
                    point_id=point_id,
                    region_key=point_to_region[point_id],
                    year=date.year,
                    doy=int(date.strftime("%j")),
                    ndvi=ndvi,
                    quality_good=quality,
                )
            )
    return rows, True


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--appeears-dir", type=Path, required=True)
    p.add_argument("--era5-onsets", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--composites-output", type=Path, required=True)
    p.add_argument("--receipt", type=Path, required=True)
    args = p.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    point_to_region = {
        str(row["point_id"]): str(row["region_key"])
        for row in manifest["points"]
    }
    expected_regions = sorted(set(point_to_region.values()))
    if len(expected_regions) != 9:
        raise ValueError(f"expected nine frozen origin regions, got {len(expected_regions)}")

    pixel_rows = []
    source_files = []
    seen_keys = set()
    for path in sorted(args.appeears_dir.rglob("*.csv")):
        loaded, matched = load_mod09_csv(path, point_to_region)
        if not matched:
            continue
        source_files.append(str(path))
        for row in loaded:
            key = (row.point_id, row.year, row.doy)
            if key in seen_keys:
                raise ValueError(f"duplicate AppEEARS point/date key {key}")
            seen_keys.add(key)
            pixel_rows.append(row)

    if not source_files:
        raise ValueError("no MOD09Q1 AppEEARS CSVs were found")
    if not pixel_rows:
        raise ValueError("MOD09Q1 extraction yielded no point rows")

    composites = aggregate_region_composites(
        pixel_rows,
        min_valid_points=5,
    )

    onset = {}
    with args.era5_onsets.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        required = {"region_key", "year", "onset_doy"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("ERA5 onset CSV missing required columns")
        for row in reader:
            onset[(str(row["region_key"]), int(row["year"]))] = float(row["onset_doy"])

    fits = fit_region_observability(
        composites,
        onset,
        phase_window_days=24.0,
        min_dates_per_year=4,
        min_years=8,
        min_pooled_observations=40,
    )
    by_region = {fit.region_key: fit for fit in fits}
    if sorted(by_region) != expected_regions:
        missing = sorted(set(expected_regions) - set(by_region))
        raise ValueError("q_B primary NOT_ESTIMABLE missing regions: " + ",".join(missing))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "region_key",
        "admitted_years",
        "pooled_observations",
        "slope_ndvi_per_day",
        "residual_sd",
        "phase_resolution_sd_days",
        "fisher_information",
        "log_fisher_information",
        "q_b_z",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for fit in sorted(fits, key=lambda row: row.region_key):
            writer.writerow(
                {
                    field: getattr(fit, field)
                    for field in fields
                }
            )

    args.composites_output.parent.mkdir(parents=True, exist_ok=True)
    with args.composites_output.open("w", newline="", encoding="utf-8") as fh:
        fields_c = ["region_key", "year", "doy", "ndvi_median", "valid_points"]
        writer = csv.DictWriter(fh, fieldnames=fields_c)
        writer.writeheader()
        for row in composites:
            writer.writerow({field: getattr(row, field) for field in fields_c})

    good_rows = sum(row.quality_good for row in pixel_rows)
    receipt = {
        "schema": "payoff_b_qb_local_observability_environment_result_v1",
        "status": "QB_ENVIRONMENT_SOURCE_GATE_PASS",
        "behavior_outcome_opened": False,
        "manifest": str(args.manifest),
        "source_mod09_files": source_files,
        "raw_point_rows": len(pixel_rows),
        "quality_good_point_rows": good_rows,
        "quality_good_fraction": good_rows / len(pixel_rows),
        "region_date_composites": len(composites),
        "fitted_regions": len(fits),
        "expected_regions": expected_regions,
        "phase_window_days": 24.0,
        "minimum_valid_lattice_points": 5,
        "minimum_dates_per_year": 4,
        "minimum_years": 8,
        "minimum_pooled_observations": 40,
        "q_b_rows": [
            {
                "region_key": fit.region_key,
                "admitted_years": fit.admitted_years,
                "pooled_observations": fit.pooled_observations,
                "phase_resolution_sd_days": fit.phase_resolution_sd_days,
                "fisher_information": fit.fisher_information,
                "q_b_z": fit.q_b_z,
            }
            for fit in sorted(fits, key=lambda row: row.region_key)
        ],
        "claim_boundary": (
            "local environmental observability only; no goose phase, stopover, "
            "lambda, or actuator response was used to estimate q_B"
        ),
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(args.receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
