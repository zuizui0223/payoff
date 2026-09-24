#!/usr/bin/env python3
"""Build AppEEARS V061 point-task manifests from projected Aikens GPS data."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.appeears_modis_request import (
    ProjectedGPSObservation,
    build_appeears_v061_tasks,
    deduplicate_to_modis_250m_cells,
)


def parse_timestamp(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(
            f"timestamp is not valid ISO-8601: {value!r}"
        ) from exc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("gps_csv", type=Path)
    parser.add_argument(
        "--source-crs",
        default="EPSG:32613",
    )
    parser.add_argument(
        "--observation-id-column",
        default="observation_id",
    )
    parser.add_argument(
        "--animal-id-column",
        default="animal_id",
    )
    parser.add_argument(
        "--animal-year-column",
        default="animal_year",
    )
    parser.add_argument(
        "--group-column",
        default="group",
    )
    parser.add_argument(
        "--timestamp-column",
        default="timestamp",
    )
    parser.add_argument(
        "--x-column",
        default="x",
    )
    parser.add_argument(
        "--y-column",
        default="y",
    )
    parser.add_argument(
        "--task-prefix",
        default="aikens_mod09q1_v061",
    )
    parser.add_argument(
        "--max-points-per-task",
        type=int,
        default=1000,
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        default=Path(
            "outputs/aikens_appeears_v061_manifest.json"
        ),
    )
    parser.add_argument(
        "--cells-output",
        type=Path,
        default=Path(
            "outputs/aikens_modis250_cells.csv"
        ),
    )
    parser.add_argument(
        "--links-output",
        type=Path,
        default=Path(
            "outputs/aikens_gps_modis250_links.csv"
        ),
    )
    parser.add_argument(
        "--receipt-output",
        type=Path,
        default=Path(
            "outputs/aikens_appeears_v061_manifest_receipt.json"
        ),
    )
    args = parser.parse_args()

    with args.gps_csv.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit("GPS CSV has no header row")
        required = (
            args.observation_id_column,
            args.animal_id_column,
            args.animal_year_column,
            args.group_column,
            args.timestamp_column,
            args.x_column,
            args.y_column,
        )
        missing = [
            column
            for column in required
            if column not in reader.fieldnames
        ]
        if missing:
            raise SystemExit(
                "GPS CSV missing required columns: "
                + ", ".join(missing)
            )

        observations = []
        for row_number, row in enumerate(reader, start=2):
            try:
                observations.append(
                    ProjectedGPSObservation(
                        observation_id=str(
                            row[args.observation_id_column]
                        ),
                        animal_id=str(
                            row[args.animal_id_column]
                        ),
                        animal_year=str(
                            row[args.animal_year_column]
                        ),
                        group=str(
                            row[args.group_column]
                        ),
                        timestamp=parse_timestamp(
                            str(row[args.timestamp_column])
                        ),
                        x=float(row[args.x_column]),
                        y=float(row[args.y_column]),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid GPS row {row_number}: {exc}"
                ) from exc

    dedup = deduplicate_to_modis_250m_cells(
        observations,
        source_crs=args.source_crs,
    )
    manifest = build_appeears_v061_tasks(
        dedup,
        task_prefix=args.task_prefix,
        max_points_per_task=args.max_points_per_task,
    )

    args.manifest_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.manifest_output.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    args.cells_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with args.cells_output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        fieldnames = [
            "cell_id",
            "row",
            "column",
            "sinusoidal_x",
            "sinusoidal_y",
            "latitude",
            "longitude",
        ]
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        for cell in dedup.cells:
            writer.writerow(asdict(cell))

    args.links_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with args.links_output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        fieldnames = [
            "observation_id",
            "animal_id",
            "animal_year",
            "group",
            "timestamp",
            "year",
            "cell_id",
        ]
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        for link in dedup.links:
            row = asdict(link)
            row["timestamp"] = link.timestamp.isoformat()
            writer.writerow(row)

    receipt = {
        "status": "appeears_v061_request_manifest_ready",
        "source_gps_csv": str(args.gps_csv),
        "source_crs": args.source_crs,
        "gps_observations": dedup.gps_observations,
        "unique_modis250_cells": dedup.unique_cells,
        "unique_modis250_cell_years": (
            dedup.unique_cell_years
        ),
        "compression_ratio": dedup.compression_ratio,
        "manifest_output": str(args.manifest_output),
        "cells_output": str(args.cells_output),
        "links_output": str(args.links_output),
        "task_count": manifest["task_count"],
        "years": manifest["years"],
        "layers": manifest["layers"],
        "reconstruction_lane": (
            manifest["reconstruction_lane"]
        ),
        "lambda_outcome_opened": False,
        "claim_boundary": (
            "request construction only; no authenticated AppEEARS request "
            "was submitted and V061 remains a sensitivity lane"
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

    print(args.receipt_output)
    print(
        "appeears_manifest "
        f"gps={dedup.gps_observations} "
        f"cells={dedup.unique_cells} "
        f"cell_years={dedup.unique_cell_years} "
        f"tasks={manifest['task_count']} "
        f"years={','.join(str(year) for year in manifest['years'])} "
        "lane=v061_sensitivity_only"
    )


if __name__ == "__main__":
    main()
