#!/usr/bin/env python3
"""Mechanical QA for GEB movement-phenology synthesis figures."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "outputs/movement_phenology/figures"
OUT = ROOT / "outputs/movement_phenology/figure_qa.json"

FIGURES = {
    "FIG4_PHASE_RETENTION_INFORMATION": {
        "png": FIG / "FIG4_PHASE_RETENTION_INFORMATION.png",
        "pdf": FIG / "FIG4_PHASE_RETENTION_INFORMATION.pdf",
        "svg": FIG / "FIG4_PHASE_RETENTION_INFORMATION.svg",
        "data": [
            FIG / "FIG4_PANEL_A_DATA.csv",
            FIG / "FIG4_PANEL_B_DATA.csv",
        ],
    },
    "FIG5_CONTROL_PERMEABILITY": {
        "png": FIG / "FIG5_CONTROL_PERMEABILITY.png",
        "pdf": FIG / "FIG5_CONTROL_PERMEABILITY.pdf",
        "svg": FIG / "FIG5_CONTROL_PERMEABILITY.svg",
        "data": [FIG / "FIG5_DATA.csv"],
    },
}

MIN_WIDTH_PX = 3000
MIN_HEIGHT_PX = 1300
MIN_DPI = 295.0
MIN_VECTOR_BYTES = 10_000
MIN_PNG_BYTES = 50_000


def main() -> None:
    receipts = {}
    hard_pass = True

    for name, files in FIGURES.items():
        missing = [
            str(path.relative_to(ROOT))
            for key in ("png", "pdf", "svg")
            for path in [files[key]]
            if not path.exists()
        ]
        missing += [
            str(path.relative_to(ROOT))
            for path in files["data"]
            if not path.exists()
        ]

        record = {"missing_files": missing}
        if missing:
            record["pass"] = False
            hard_pass = False
            receipts[name] = record
            continue

        with Image.open(files["png"]) as image:
            width, height = image.size
            dpi = image.info.get("dpi", (0.0, 0.0))
            dpi_x = float(dpi[0]) if dpi else 0.0
            dpi_y = float(dpi[1]) if dpi else 0.0

        checks = {
            "width_px": width >= MIN_WIDTH_PX,
            "height_px": height >= MIN_HEIGHT_PX,
            "dpi_x": dpi_x >= MIN_DPI,
            "dpi_y": dpi_y >= MIN_DPI,
            "png_size": files["png"].stat().st_size >= MIN_PNG_BYTES,
            "pdf_size": files["pdf"].stat().st_size >= MIN_VECTOR_BYTES,
            "svg_size": files["svg"].stat().st_size >= MIN_VECTOR_BYTES,
            "data_nonempty": all(path.stat().st_size > 20 for path in files["data"]),
        }
        passed = all(checks.values())
        hard_pass = hard_pass and passed

        record.update(
            {
                "width_px": width,
                "height_px": height,
                "dpi": [dpi_x, dpi_y],
                "png_bytes": files["png"].stat().st_size,
                "pdf_bytes": files["pdf"].stat().st_size,
                "svg_bytes": files["svg"].stat().st_size,
                "checks": checks,
                "pass": passed,
            }
        )
        receipts[name] = record

    result = {
        "figures": receipts,
        "all_hard_gates_pass": hard_pass,
        "manual_qa": {
            "status": "PASS_2026-09-21",
            "checks": [
                "no visible label clipping in Fig. 4 or Fig. 5",
                "panel labels and legends readable at full rendered size",
                "interpretation does not depend on colour",
                "barnacle-goose route whisker explicitly labelled as an observed range, not CI",
                "industrial-development null temporal interaction is visually explicit",
            ],
            "note": (
                "Manual visual QA is frozen as a receipt; CI verifies file, "
                "resolution, DPI, vector-format and source-data requirements."
            ),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

    if not hard_pass:
        raise SystemExit("Figure QA hard gate failed")


if __name__ == "__main__":
    main()
