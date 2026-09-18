#!/usr/bin/env python3
"""Inventory the official Nature Communications source-data workbook for the
mule-deer phenological-compensation study.

This is an evidence-discovery probe, not an inferential analysis. It emits only
sheet names, shapes, column names, and bounded head previews so we can register
which published source-data objects can support the PAYOFF-B phase-locking test.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


SOURCE = Path("external/mule_deer_ortega_2023/source_data.xlsx")
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)


def normalize_cell(value):
    if pd.isna(value):
        return None
    if isinstance(value, (int, float, bool)):
        return value
    text = str(value)
    return text[:200]


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source workbook: {SOURCE}")

    workbook = pd.ExcelFile(SOURCE)
    inventory = []

    for sheet in workbook.sheet_names:
        # Read without assuming the first row is the true header.
        raw = pd.read_excel(SOURCE, sheet_name=sheet, header=None)
        # Also attempt standard first-row header extraction for convenience.
        headed = pd.read_excel(SOURCE, sheet_name=sheet)

        preview = []
        for row in raw.head(8).itertuples(index=False, name=None):
            preview.append([normalize_cell(v) for v in row[:20]])

        inventory.append(
            {
                "sheet": sheet,
                "n_rows_raw": int(raw.shape[0]),
                "n_cols_raw": int(raw.shape[1]),
                "header_guess": [normalize_cell(x) for x in list(headed.columns)[:30]],
                "preview_first_8_rows_first_20_cols": preview,
            }
        )

    (OUT / "stage3_mule_deer_source_inventory.json").write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    rows = []
    for x in inventory:
        rows.append(
            {
                "sheet": x["sheet"],
                "n_rows_raw": x["n_rows_raw"],
                "n_cols_raw": x["n_cols_raw"],
                "header_guess": " | ".join(
                    "" if z is None else str(z) for z in x["header_guess"]
                ),
            }
        )
    pd.DataFrame(rows).to_csv(
        OUT / "stage3_mule_deer_source_inventory.csv", index=False
    )

    print("Mule-deer source-data inventory")
    for x in inventory:
        print(
            f"SHEET={x['sheet']!r} rows={x['n_rows_raw']} cols={x['n_cols_raw']}"
        )
        print("  HEADER_GUESS:", x["header_guess"])
        for row in x["preview_first_8_rows_first_20_cols"][:4]:
            print("  ROW:", row)


if __name__ == "__main__":
    main()
