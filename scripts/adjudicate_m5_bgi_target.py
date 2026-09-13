from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.direct_mu_m5_bgi_target_gate import (  # noqa: E402
    FrozenCalibration,
    adjudicate_m5_target_opening,
)
from src.direct_mu_marker_reconstruction import (  # noqa: E402
    MarkerReconstructionInput,
    REGISTERED_MARKERS,
    reconstruct_registered_marker_pattern,
)

CORE_PANEL = (
    "SCO3000", "SCO3300", "SCO3600", "SCO3900", "SCO4200",
    "SCO4500", "SCO4800", "SCO5100", "SCO5400",
)
TARGET = "M5_T0"
TARGET_RUN = "SRR16954696"
REFERENCE = "NC_003888.3"
PANEL_ID = "FROZEN_CENTRAL_CORE_PANEL_V1"


def load_json(path: Path):
    return json.loads(path.read_text())


def load_depths(path: Path):
    with path.open(newline="") as h:
        rows = list(csv.DictReader(h, delimiter="\t"))
    expected = set(REGISTERED_MARKERS) | set(CORE_PANEL)
    got = {r["legacy_locus"] for r in rows}
    if got != expected or len(rows) != len(expected):
        raise ValueError(f"target locus set mismatch; missing={sorted(expected-got)}, extra={sorted(got-expected)}")
    out = {}
    for row in rows:
        locus = row["legacy_locus"]
        depth = float(row["mean_depth"])
        if depth < 0:
            raise ValueError(f"negative mean depth for {locus}")
        out[locus] = depth
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--calibration", type=Path, required=True)
    p.add_argument("--opening-registry", type=Path, required=True)
    p.add_argument("--sequence-map", type=Path, required=True)
    p.add_argument("--target-depths", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    cal = load_json(args.calibration)
    opening = load_json(args.opening_registry)
    seqmap = load_json(args.sequence_map)

    frozen = FrozenCalibration(
        receipt_id=cal["receipt_id"],
        calibration_qualified=cal["result"]["calibration_qualified"],
        target_candidate_id=cal["target_candidate"],
        target_bgi_ratios_opened_for_calibration=cal["target_bgi_run_opened"],
        absence_max_ratio=cal["result"]["absence_max_ratio"],
        presence_min_ratio=cal["result"]["presence_min_ratio"],
        core_panel=tuple(cal["frozen_rules"]["bgi_normalization_panel"]),
        absent_pair_count=cal["result"]["absent_pair_count"],
        present_pair_count=cal["result"]["present_pair_count"],
        absent_candidate_count=cal["result"]["absent_candidate_count"],
        present_candidate_count=cal["result"]["present_candidate_count"],
    )
    gate = adjudicate_m5_target_opening(frozen)
    if not gate.target_opening_allowed:
        raise SystemExit(f"M5 target opening not licensed: {gate.blockers}")
    if opening["status"] != "OPENING_LICENSED_TARGET_UNOPENED":
        raise SystemExit("opening registry is not in licensed-unopened state")
    if not opening["target_opening_allowed"] or opening["target_bgi_ratios_opened"]:
        raise SystemExit("opening registry violates licensed-unopened contract")
    if opening["target_bgi_run"] != TARGET_RUN:
        raise SystemExit("unexpected target run in opening registry")

    m5_rows = {r["candidate_id"]: r for r in seqmap["priority_candidates"]}
    m5 = m5_rows.get(TARGET)
    if not m5 or m5["runs"]["bgi"]["run"] != TARGET_RUN:
        raise SystemExit("qualified sequence map does not map M5_T0 to frozen BGI target")
    sequence_map_qualified = bool(
        seqmap["claim_boundary"]["sequence_sample_map_qualified"]
        and m5["sequence_marker_reconstruction_allowed"]
        and not m5["current_blockers"]
    )

    depths = load_depths(args.target_depths)
    core_depths = [depths[x] for x in CORE_PANEL]
    if any(x <= 0 for x in core_depths):
        raise SystemExit("at least one frozen core-panel locus has non-positive target depth")
    baseline = statistics.median(core_depths)
    ratios = {m: depths[m] / baseline for m in REGISTERED_MARKERS}

    rec = reconstruct_registered_marker_pattern(
        MarkerReconstructionInput(
            candidate_id=TARGET,
            sequence_sample_map_qualified=sequence_map_qualified,
            primary_short_read_run=TARGET_RUN,
            reference_accession=REFERENCE,
            normalization_panel_id=PANEL_ID,
            thresholds_frozen_preoutcome=True,
            absence_max_ratio=gate.absence_max_ratio,
            presence_min_ratio=gate.presence_min_ratio,
            normalized_marker_ratios=ratios,
        )
    )

    payload = {
        "receipt_id": "STREPTOMYCES_M5_BGI_TARGET_RESULT_V1",
        "candidate_id": TARGET,
        "target_bgi_run": TARGET_RUN,
        "reference_accession": REFERENCE,
        "normalization_panel_id": PANEL_ID,
        "target_bgi_ratios_opened": True,
        "opening_gate": {
            "target_opening_allowed": gate.target_opening_allowed,
            "calibration_receipt_id": cal["receipt_id"],
            "absence_max_ratio": gate.absence_max_ratio,
            "presence_min_ratio": gate.presence_min_ratio,
        },
        "target_measurement": {
            "core_panel_mean_depths": {x: depths[x] for x in CORE_PANEL},
            "core_median_depth": baseline,
            "marker_mean_depths": {x: depths[x] for x in REGISTERED_MARKERS},
            "normalized_marker_ratios": ratios,
            "marker_states": dict(rec.marker_states),
        },
        "result": {
            "marker_pattern_verified": rec.marker_pattern_verified,
            "registered_class": rec.registered_class,
            "blockers": list(rec.blockers),
        },
        "claim_boundary": {
            "primary_bgi_marker_class_known": rec.marker_pattern_verified,
            "pacbio_corroboration_is_independent_support_only": True,
            "r2_gross_structure_resolved": False,
            "physical_stock_access_confirmed": False,
            "realization_d_band_available": False,
            "qualified_d_reference": False,
            "qualified_d_reference_count_increment": 0,
            "architecture_specific_inference_open": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(args.output.read_text())


if __name__ == "__main__":
    main()
