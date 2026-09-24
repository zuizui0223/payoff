#!/usr/bin/env python3
"""Assemble the source-backed Eurasian-wigeon PAYOFF-B gate bundle."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.wigeon_gate_bundle import assemble_wigeon_gate_bundle


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--primary-phase-json",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--strong-phase-json",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--stopover-actuator-json",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--secondary-diagnostics-json",
        type=Path,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_wigeon_gate_bundle.json"
        ),
    )
    args = parser.parse_args()

    diagnostics = (
        {}
        if args.secondary_diagnostics_json is None
        else load_json(args.secondary_diagnostics_json)
    )

    bundle = assemble_wigeon_gate_bundle(
        load_json(args.primary_phase_json),
        load_json(args.strong_phase_json),
        load_json(args.stopover_actuator_json),
        stopover_source_interpretation=diagnostics.get(
            "W2_stopover_source_interpretation"
        ),
        stopover_replication_diagnostic=diagnostics.get(
            "W2_ERA5_replication_diagnostic"
        ),
        travel_speed_diagnostic=diagnostics.get(
            "W3_travel_speed_diagnostic"
        ),
        distance_moderation_diagnostic=diagnostics.get(
            "W4_distance_moderation_diagnostic"
        ),
    )

    receipt = {
        "status": "source_backed_wigeon_two_gate_bundle",
        "primary_phase_source": str(args.primary_phase_json),
        "strong_phase_source": str(args.strong_phase_json),
        "stopover_actuator_source": str(
            args.stopover_actuator_json
        ),
        "secondary_diagnostics_source": (
            None
            if args.secondary_diagnostics_json is None
            else str(args.secondary_diagnostics_json)
        ),
        "bundle": asdict(bundle),
        "no_omnibus_score": True,
        "claim_boundary": (
            "W2 preregisters a directional stopover prediction and secondary "
            "gain band but no fixed p-value threshold. The formal POWER gate, "
            "source-level support interpretation, and independent ERA5 "
            "reconstruction robustness are reported separately. W3 travel "
            "speed and W4 distance moderation remain secondary diagnostics."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "wigeon_gate_bundle "
        f"lambda={bundle.lambda_retention:.12g} "
        f"primary_pass={int(bundle.primary_lambda_passed)} "
        f"strong_pass={int(bundle.strong_contraction_passed)} "
        f"stopover_direction_pass={int(bundle.stopover_direction_passed)} "
        f"stopover_source_supported={int(bundle.stopover_source_supported)} "
        f"stopover_reconstruction_robust={bundle.stopover_reconstruction_robust} "
        f"class={bundle.two_gate_class}"
    )


if __name__ == "__main__":
    main()
