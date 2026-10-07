#!/usr/bin/env python3
"""Build the frozen AppEEARS manifest for PAYOFF-B q_B local observability."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.qb_local_observability import RegionCenter, build_appeears_manifest


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--regions-json",
        type=Path,
        default=Path("data/payoff_b_qb_origin_regions_20261008.json"),
    )
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    source = json.loads(args.regions_json.read_text(encoding="utf-8"))
    regions = [
        RegionCenter(
            flyway=row["flyway"],
            region=row["region"],
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
        )
        for row in source["regions"]
    ]
    manifest = build_appeears_manifest(
        regions,
        years=source["historical_years"],
        radial_distance_km=float(
            source["spatial_lattice"]["radial_distance_km"]
        ),
    )
    manifest["source_regions_json"] = str(args.regions_json)
    manifest["spatial_lattice"] = source["spatial_lattice"]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
