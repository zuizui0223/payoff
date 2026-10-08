#!/usr/bin/env python3
"""Audit individual self-inclusion in the frozen V7R recourse proxy.

This is post-outcome source-only diagnostic, not a new QxR test.

Example:
 python scripts/audit_v7r_recourse_loo.py \
   --multiflyway-zip barnacle_multiflyway_stage3.zip \
   --svalbard-zip svalbard_stage3.zip \
   --output-json outputs/v7r_recourse_loo_diagnostic.json
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.route_recourse_capacity import TransitionDuration
from src.v7r_recourse_loo import audit_individual_exclusion

MULTI_SHA = "8e720be44e0ef2e3e497786c9241c6625b4b14c46506fbb30ea027dcdf36749f"
SVAL_SHA = "29558f9b8b43a7375b3922118a77b74464558f4869d564f23bc01a555013825"
TERMINALS = {"greenland": "R4", "svalbard": "R4", "barents": "R7"}

def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _read_csv(archive: zipfile.ZipFile, name: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(
        archive.read(name).decode("utf-8-sig")
    )))

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--multiflyway-zip", type=Path, required=True)
    parser.add_argument("--svalbard-zip", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    args = parser.parse_args()

    actual_multi = _sha256(args.multiflyway_zip)
    actual_sval = _sha256(args.svalbard_zip)
    if actual_multi != MULTI_SHA or actual_sval != SVAL_SHA:
        raise ValueError("Stage-3 archive checksum mismatch")

    precheck = json.loads((
        ROOT / "data/payoff_b_v7r_source_precheck_20261007.json"
    ).read_text(encoding="utf-8"))
    focal = {
        (str(row["flyway"]), str(row["origin"]), str(row["destination"]))
        for row in precheck["focal_transitions"]
    }
    if len(focal) != 10:
        raise ValueError("focal set is not the frozen ten transitions")

    transitions: list[TransitionDuration] = []
    with zipfile.ZipFile(args.multiflyway_zip) as multi, zipfile.ZipFile(args.svalbard_zip) as sval:
        for flyway in ("greenland", "barents", "svalbard"):
            source = (
                _read_csv(sval, "stage3_svalbard_goose_transitions.csv")
                if flyway == "svalbard" else
                _read_csv(multi, f"stage3_{flyway}_goose_anomaly_phase_transitions.csv")
            )
            for row in source:
                duration = (
                    float(row["origin_stopover_days"]) + float(row["transit_days"])
                    if flyway == "svalbard" else
                    float(row["destination_arrival_doy"]) - float(row["origin_arrival_doy"])
                )
                transitions.append(TransitionDuration(
                    flyway=flyway,
                    origin_region=row["origin_region"],
                    destination_region=row["destination_region"],
                    duration_days=duration,
                    individual_id=row["individual_id"],
                ))

    results = audit_individual_exclusion(
        transitions, focal_edges=focal,
        terminal_by_flyway=TERMINALS,
        minimum_edge_rows=3,
    )
    by_edge = {(row.flyway, row.origin_region, row.destination_region): row for row in results}
    for original in precheck["focal_transitions"]:
        key = (original["flyway"], original["origin"], original["destination"])
        if abs(by_edge[key].full_recourse - float(original["R"])) > 1e-5:
            raise ValueError(f"full source R disagrees with frozen source precheck: {key}")

    total = sum(row.n_individuals for row in results)
    valid = sum(row.n_estimable for row in results)
    payload = {
        "schema": "payoff_b_v7r_recourse_individual_exclusion_v1",
        "status": "POST_OUTCOME_SOURCE_ONLY_PROXY_STABILITY_NOT_CONFIRMATORY",
        "source_sha256": {"multiflyway": actual_multi, "svalbard": actual_sval},
        "focal_transition_count": len(results),
        "total_exclusions": total,
        "estimable_exclusions": valid,
        "non_estimable_exclusions": total - valid,
        "maximum_absolute_recourse_change": max(
            row.max_absolute_difference or 0 for row in results
        ),
        "edges": [asdict(row) for row in results],
        "claim_boundary": (
            "Uses movement durations, not environmental predictability or phase outcomes. "
            "No V7R primary hypothesis is reopened. Even leave-one-animal-out group "
            "envelopes are observed behaviors, not exogenous physiological constraints."
        ),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
