#!/usr/bin/env python3
"""Fit annual peak IRG for pixel-year NDVI time series."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.irg_reconstruction import (
    NDVIObservation,
    fit_peak_irg,
    preprocess_ndvi,
)


def parse_bool(value: str) -> bool:
    token = value.strip().lower()
    if token in {"1", "true", "t", "yes", "y"}:
        return True
    if token in {"0", "false", "f", "no", "n"}:
        return False
    raise ValueError(
        "boolean field must be one of 1/0, true/false, yes/no"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument(
        "--modis-product",
        choices=("MOD09Q1.006", "MOD09Q1.061"),
        required=True,
    )
    parser.add_argument("--pixel-column", default="pixel_id")
    parser.add_argument("--year-column", default="year")
    parser.add_argument("--doy-column", default="doy")
    parser.add_argument("--ndvi-column", default="ndvi")
    parser.add_argument("--snow-free-column", default="snow_free")
    parser.add_argument("--quality-column", default="quality_good")
    parser.add_argument(
        "--baseline-quantile",
        type=float,
        default=0.025,
    )
    parser.add_argument(
        "--upper-quantile",
        type=float,
        default=0.925,
    )
    parser.add_argument(
        "--snow-search-start-doy",
        type=int,
        default=60,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_peak_irg_by_pixel_year.csv"
        ),
    )
    parser.add_argument(
        "--receipt-output",
        type=Path,
        default=Path(
            "outputs/payoff_b_peak_irg_reconstruction_receipt.json"
        ),
    )
    args = parser.parse_args()

    required = (
        args.pixel_column,
        args.year_column,
        args.doy_column,
        args.ndvi_column,
        args.snow_free_column,
    )
    grouped: dict[
        tuple[str, int],
        list[NDVIObservation],
    ] = {}

    with args.input_csv.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit("input CSV has no header row")
        missing = [
            column
            for column in required
            if column not in reader.fieldnames
        ]
        if missing:
            raise SystemExit(
                "missing required columns: "
                + ", ".join(missing)
            )

        quality_present = (
            args.quality_column in reader.fieldnames
        )
        for row_number, row in enumerate(
            reader,
            start=2,
        ):
            try:
                pixel_id = str(
                    row[args.pixel_column]
                ).strip()
                year = int(row[args.year_column])
                doy = int(row[args.doy_column])
                ndvi = float(row[args.ndvi_column])
                snow_free = parse_bool(
                    row[args.snow_free_column]
                )
                quality_good = (
                    True
                    if not quality_present
                    else parse_bool(
                        row[args.quality_column]
                    )
                )
                if not pixel_id:
                    raise ValueError(
                        "pixel_id must be non-empty"
                    )
                grouped.setdefault(
                    (pixel_id, year),
                    [],
                ).append(
                    NDVIObservation(
                        doy=doy,
                        ndvi=ndvi,
                        snow_free=snow_free,
                        quality_good=quality_good,
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid row {row_number}: {exc}"
                ) from exc

    if not grouped:
        raise SystemExit("input CSV contains no pixel-year groups")

    lane = (
        "study_faithful_v006"
        if args.modis_product == "MOD09Q1.006"
        else "v061_sensitivity_only"
    )

    rows = []
    for (pixel_id, year), observations in sorted(
        grouped.items()
    ):
        try:
            processed = preprocess_ndvi(
                observations,
                baseline_quantile=args.baseline_quantile,
                upper_quantile=args.upper_quantile,
                snow_search_start_doy=(
                    args.snow_search_start_doy
                ),
                require_snow_flags=True,
            )
            fit = fit_peak_irg(processed)
        except Exception as exc:
            raise SystemExit(
                "IRG reconstruction failed for "
                f"pixel={pixel_id}, year={year}: "
                f"{type(exc).__name__}: {exc}"
            ) from exc

        peak_date = (
            datetime(year, 1, 1)
            + timedelta(days=fit.peak_irg_doy - 1)
        )
        params = asdict(fit.parameters)
        rows.append(
            {
                "pixel_id": pixel_id,
                "year": year,
                "modis_product": args.modis_product,
                "reconstruction_lane": lane,
                "peak_irg_doy": fit.peak_irg_doy,
                "peak_irg_date": peak_date.date().isoformat(),
                "peak_irg_value": fit.peak_irg_value,
                "spring_scale_days": fit.spring_scale_days,
                "fit_rmse": fit.fit_rmse,
                "valid_observations": (
                    fit.processed.valid_observations
                ),
                "snow_release_doy": (
                    fit.processed.snow_release_doy
                ),
                "winter_baseline": (
                    fit.processed.winter_baseline
                ),
                "upper_scale_reference": (
                    fit.processed.upper_scale_reference
                ),
                **params,
            }
        )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with args.output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
        )
        writer.writeheader()
        writer.writerows(rows)

    receipt = {
        "status": "peak_irg_reconstruction_complete",
        "source_file": str(args.input_csv),
        "modis_product": args.modis_product,
        "reconstruction_lane": lane,
        "pixel_years": len(rows),
        "baseline_quantile": args.baseline_quantile,
        "upper_quantile": args.upper_quantile,
        "snow_search_start_doy": (
            args.snow_search_start_doy
        ),
        "output": str(args.output),
        "claim_boundary": (
            "environmental reconstruction only; no lambda "
            "outcome is estimated here. MOD09Q1.061 is a "
            "sensitivity lane and must not be labeled as "
            "study-faithful MOD09Q1.006 replication."
        ),
    }
    args.receipt_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(args.receipt_output)
    print(
        "peak_irg_reconstruction "
        f"lane={lane} "
        f"pixel_years={len(rows)}"
    )


if __name__ == "__main__":
    main()
