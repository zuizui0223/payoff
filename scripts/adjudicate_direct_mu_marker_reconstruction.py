from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.direct_mu_marker_reconstruction import (
    MarkerReconstructionInput,
    reconstruct_registered_marker_pattern,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Adjudicate a precomputed direct-mu registered-marker reconstruction receipt"
    )
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    inp = MarkerReconstructionInput(
        candidate_id=data["candidate_id"],
        sequence_sample_map_qualified=bool(data["sequence_sample_map_qualified"]),
        primary_short_read_run=data["primary_short_read_run"],
        reference_accession=data["reference_accession"],
        normalization_panel_id=data["normalization_panel_id"],
        thresholds_frozen_preoutcome=bool(data["thresholds_frozen_preoutcome"]),
        absence_max_ratio=data["absence_max_ratio"],
        presence_min_ratio=data["presence_min_ratio"],
        normalized_marker_ratios=data["normalized_marker_ratios"],
    )
    result = reconstruct_registered_marker_pattern(inp)
    payload = {
        "candidate_id": result.candidate_id,
        "marker_states": dict(result.marker_states),
        "registered_class": result.registered_class,
        "marker_pattern_verified": result.marker_pattern_verified,
        "blockers": list(result.blockers),
        "physical_material_identity_established": result.physical_material_identity_established,
        "gross_rearrangement_audit_completed": result.gross_rearrangement_audit_completed,
        "realization_band_available": result.realization_band_available,
        "reference_qualified": result.reference_qualified,
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
