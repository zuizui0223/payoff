#!/usr/bin/env python3
"""Prepare V061 sensitivity IRG input from AppEEARS point-result CSVs."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.appeears_irg_ingest import (
    AppEEARSReflectanceRow,
    AppEEARSSnowRow,
    convert_appeears_v061_to_irg,
    parse_appeears_date,
    resolve_column,
)


def _float_or_nan(value: str) -> float:
    text = str(value).strip()
    if not text:
        return float("nan")
    try:
        return float(text)
    except ValueError:
        return float("nan")


def _int_or_fill(
    value: str,
    *,
    fill: int,
) -> int:
    text = str(value).strip()
    if not text:
        return fill
    try:
        number = float(text)
    except ValueError:
        return fill
    if not math.isfinite(number):
        return fill
    return int(number)


def load_reflectance(path: Path):
    with path.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit(
                f"MOD09Q1 result has no header: {path}"
            )
        headers = list(reader.fieldnames)
        pixel_col = resolve_column(
            headers,
            exact_aliases=("ID", "pixel_id"),
        )
        date_col = resolve_column(
            headers,
            exact_aliases=("Date", "date"),
        )
        red_col = resolve_column(
            headers,
            suffix_aliases=(
                "MOD09Q1_061_sur_refl_b01",
                "sur_refl_b01",
            ),
        )
        nir_col = resolve_column(
            headers,
            suffix_aliases=(
                "MOD09Q1_061_sur_refl_b02",
                "sur_refl_b02",
            ),
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

        rows = []
        for row_number, row in enumerate(
            reader,
            start=2,
        ):
            try:
                pixel_id = str(
                    row[pixel_col]
                ).strip()
                if not pixel_id:
                    raise ValueError(
                        "pixel ID must be non-empty"
                    )
                rows.append(
                    AppEEARSReflectanceRow(
                        pixel_id=pixel_id,
                        date=parse_appeears_date(
                            str(row[date_col])
                        ),
                        red_reflectance=_float_or_nan(
                            row[red_col]
                        ),
                        nir_reflectance=_float_or_nan(
                            row[nir_col]
                        ),
                        qc_250m=_int_or_fill(
                            row[qc_col],
                            fill=65535,
                        ),
                        state_250m=_int_or_fill(
                            row[state_col],
                            fill=65535,
                        ),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid MOD09Q1 row {row_number}: {exc}"
                ) from exc

    return rows, {
        "pixel": pixel_col,
        "date": date_col,
        "red": red_col,
        "nir": nir_col,
        "qc": qc_col,
        "state": state_col,
    }


def load_snow(path: Path):
    with path.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit(
                f"MOD10A2 result has no header: {path}"
            )
        headers = list(reader.fieldnames)
        pixel_col = resolve_column(
            headers,
            exact_aliases=("ID", "pixel_id"),
        )
        date_col = resolve_column(
            headers,
            exact_aliases=("Date", "date"),
        )
        snow_col = resolve_column(
            headers,
            suffix_aliases=(
                "MOD10A2_061_Maximum_Snow_Extent",
                "Maximum_Snow_Extent",
            ),
        )

        rows = []
        for row_number, row in enumerate(
            reader,
            start=2,
        ):
            try:
                pixel_id = str(
                    row[pixel_col]
                ).strip()
                if not pixel_id:
                    raise ValueError(
                        "pixel ID must be non-empty"
                    )
                rows.append(
                    AppEEARSSnowRow(
                        pixel_id=pixel_id,
                        date=parse_appeears_date(
                            str(row[date_col])
                        ),
                        maximum_snow_extent=_int_or_fill(
                            row[snow_col],
                            fill=-1,
                        ),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid MOD10A2 row {row_number}: {exc}"
                ) from exc

    return rows, {
        "pixel": pixel_col,
        "date": date_col,
        "maximum_snow_extent": snow_col,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mod09q1-results",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--mod10a2-results",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/aikens_v061_irg_input.csv"
        ),
    )
    parser.add_argument(
        "--receipt-output",
        type=Path,
        default=Path(
            "outputs/aikens_v061_irg_input_receipt.json"
        ),
    )
    args = parser.parse_args()

    reflectance, reflectance_columns = load_reflectance(
        args.mod09q1_results
    )
    snow, snow_columns = load_snow(
        args.mod10a2_results
    )
    converted = convert_appeears_v061_to_irg(
        reflectance,
        snow,
    )

    if (
        converted.duplicate_reflectance_keys > 0
        or converted.duplicate_snow_keys > 0
    ):
        raise SystemExit(
            "duplicate AppEEARS pixel/date keys detected; "
            "refuse ambiguous environmental join"
        )

    if converted.output_rows == 0:
        raise SystemExit(
            "AppEEARS conversion produced no usable IRG-input rows"
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
        fieldnames = [
            "pixel_id",
            "year",
            "doy",
            "ndvi",
            "snow_free",
            "quality_good",
        ]
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        for row in converted.rows:
            writer.writerow(
                {
                    "pixel_id": row.pixel_id,
                    "year": row.year,
                    "doy": row.doy,
                    "ndvi": f"{row.ndvi:.12g}",
                    "snow_free": (
                        "true"
                        if row.snow_free
                        else "false"
                    ),
                    "quality_good": (
                        "true"
                        if row.quality_good
                        else "false"
                    ),
                }
            )

    quality_good_rows = sum(
        row.quality_good
        for row in converted.rows
    )
    snow_free_rows = sum(
        row.snow_free
        for row in converted.rows
    )
    pixel_years = {
        (row.pixel_id, row.year)
        for row in converted.rows
    }

    receipt = {
        "status": "appeears_v061_irg_input_ready",
        "reconstruction_lane": "v061_sensitivity_only",
        "mod09q1_source": str(
            args.mod09q1_results
        ),
        "mod10a2_source": str(
            args.mod10a2_results
        ),
        "resolved_columns": {
            "MOD09Q1.061": reflectance_columns,
            "MOD10A2.061": snow_columns,
        },
        "conversion": asdict(converted)
        | {"rows": None},
        "pixel_years": len(pixel_years),
        "quality_good_rows": quality_good_rows,
        "snow_free_rows": snow_free_rows,
        "output": str(args.output),
        "reflectance_values": (
            "AppEEARS scale-applied physical reflectance"
        ),
        "quality_rule": (
            "strict V061 sensitivity screen: ideal MODLAND, highest b1/b2 "
            "quality, atmospheric correction, clear/no-shadow/no-internal-"
            "cloud/no-adjacent-cloud, non-high aerosol"
        ),
        "snow_rule": (
            "MOD10A2.061 Maximum_Snow_Extent 25=no snow, 200=snow; "
            "other codes omitted as unknown"
        ),
        "lambda_outcome_opened": False,
        "claim_boundary": (
            "current-product V061 sensitivity preprocessing only; "
            "not study-faithful V006 reconstruction"
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
        "appeears_v061_irg_input "
        f"reflectance={converted.reflectance_rows} "
        f"snow={converted.snow_rows} "
        f"matched={converted.matched_rows} "
        f"output={converted.output_rows} "
        f"pixel_years={len(pixel_years)} "
        f"quality_good={quality_good_rows} "
        f"unknown_snow={converted.unknown_snow_rows}"
    )


if __name__ == "__main__":
    main()
