#!/usr/bin/env python3
"""Evaluate whether a candidate taxon adds inferential value to PAYOFF-B."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.taxon_inclusion_gate import (
    TaxonInclusionProposal,
    evaluate_taxon_inclusion,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("proposal_json", type=Path)
    parser.add_argument(
        "--canonical-phase-coordinate-id",
        required=True,
    )
    parser.add_argument(
        "--canonical-segment-scale-id",
        required=True,
    )
    parser.add_argument(
        "--existing-test-ids-json",
        type=Path,
        help=(
            "optional JSON list of already-used independent_test_id values"
        ),
    )
    parser.add_argument(
        "--fail-on-exclusion",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_taxon_inclusion_gate.json"
        ),
    )
    args = parser.parse_args()

    proposal_payload = json.loads(
        args.proposal_json.read_text(encoding="utf-8")
    )
    proposal = TaxonInclusionProposal(**proposal_payload)

    existing: set[str] = set()
    if args.existing_test_ids_json is not None:
        payload = json.loads(
            args.existing_test_ids_json.read_text(
                encoding="utf-8"
            )
        )
        if not isinstance(payload, list):
            raise SystemExit(
                "--existing-test-ids-json must contain a JSON list"
            )
        existing = {str(value) for value in payload}

    gate = evaluate_taxon_inclusion(
        proposal,
        canonical_phase_coordinate_id=(
            args.canonical_phase_coordinate_id
        ),
        canonical_segment_scale_id=(
            args.canonical_segment_scale_id
        ),
        existing_independent_test_ids=existing,
    )

    receipt = {
        "status": (
            "taxon_inclusion_gate_pass"
            if gate.include
            else "taxon_inclusion_gate_fail"
        ),
        "proposal_source": str(args.proposal_json),
        "proposal": asdict(proposal),
        "gate": asdict(gate),
        "policy": (
            "raw-data availability alone never licenses taxon addition; "
            "at least one new inferential contribution is required"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "taxon_inclusion_gate "
        f"system={proposal.system_name} "
        f"include={int(gate.include)} "
        f"contributions={gate.scientific_contribution_count} "
        f"blockers={';'.join(gate.blockers) if gate.blockers else 'none'}"
    )

    if args.fail_on_exclusion and not gate.include:
        raise SystemExit(
            "candidate taxon does not add a licensed inferential contribution"
        )


if __name__ == "__main__":
    main()
