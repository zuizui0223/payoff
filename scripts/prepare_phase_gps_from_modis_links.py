#!/usr/bin/env python3
"""Convert frozen GPS-to-MODIS links into phase-environment GPS keys."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path


def parse_timestamp(value: str) -> datetime:
    token = value.strip().replace("Z", "+00:00")
    if not token:
        raise ValueError("timestamp must be non-empty")
    return datetime.fromisoformat(token)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("links_csv", type=Path)
    parser.add_argument(
        "--expected-observations",
        type=int,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/aikens_phase_gps_keys.csv"),
    )
    parser.add_argument(
        "--receipt-output",
        type=Path,
        default=Path("outputs/aikens_phase_gps_keys_receipt.json"),
    )
    args = parser.parse_args()

    required = {
        "observation_id",
        "animal_id",
        "animal_year",
        "group",
        "timestamp",
        "year",
        "cell_id",
    }
    rows: list[dict[str, str]] = []
    seen_observations: set[str] = set()
    groups: dict[str, int] = {}
    years: dict[int, int] = {}
    pixels: set[str] = set()

    with args.links_csv.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit("links CSV has no header row")
        missing = required.difference(reader.fieldnames)
        if missing:
            raise SystemExit(
                "links CSV missing required columns: "
                + ", ".join(sorted(missing))
            )

        for row_number, row in enumerate(reader, start=2):
            observation_id = str(row["observation_id"]).strip()
            animal_id = str(row["animal_id"]).strip()
            animal_year = str(row["animal_year"]).strip()
            group = str(row["group"]).strip()
            cell_id = str(row["cell_id"]).strip()
            try:
                timestamp = parse_timestamp(str(row["timestamp"]))
                declared_year = int(row["year"])
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid links row {row_number}: {exc}"
                ) from exc

            if not all(
                (observation_id, animal_id, animal_year, group, cell_id)
            ):
                raise SystemExit(
                    f"invalid links row {row_number}: empty identifier"
                )
            if observation_id in seen_observations:
                raise SystemExit(
                    f"duplicate observation_id in links: {observation_id}"
                )
            if timestamp.year != declared_year:
                raise SystemExit(
                    f"year mismatch at links row {row_number}: "
                    f"timestamp={timestamp.year} declared={declared_year}"
                )

            seen_observations.add(observation_id)
            groups[group] = groups.get(group, 0) + 1
            years[declared_year] = years.get(declared_year, 0) + 1
            pixels.add(cell_id)
            rows.append(
                {
                    "observation_id": observation_id,
                    "animal_id": animal_id,
                    "animal_year": animal_year,
                    "group": group,
                    "timestamp": timestamp.isoformat(),
                    "pixel_id": cell_id,
                }
            )

    if not rows:
        raise SystemExit("links CSV contains no observations")
    if (
        args.expected_observations is not None
        and len(rows) != args.expected_observations
    ):
        raise SystemExit(
            "unexpected observation count: "
            f"observed={len(rows)} "
            f"expected={args.expected_observations}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "observation_id",
                "animal_id",
                "animal_year",
                "group",
                "timestamp",
                "pixel_id",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    receipt = {
        "status": "phase_gps_pixel_keys_ready",
        "source_links": str(args.links_csv),
        "observations": len(rows),
        "unique_pixels": len(pixels),
        "groups": {
            key: groups[key]
            for key in sorted(groups)
        },
        "years": {
            str(key): years[key]
            for key in sorted(years)
        },
        "output": str(args.output),
        "lambda_outcome_opened": False,
        "claim_boundary": (
            "deterministic identity-preserving conversion of the frozen "
            "GPS-to-MODIS cell links; no environmental or lambda outcome"
        ),
    }
    args.receipt_output.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(args.receipt_output)
    print(
        "phase_gps_pixel_keys "
        f"observations={len(rows)} "
        f"pixels={len(pixels)} "
        f"groups={','.join(sorted(groups))}"
    )


if __name__ == "__main__":
    main()
