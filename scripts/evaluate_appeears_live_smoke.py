#!/usr/bin/env python3
"""Evaluate whether one live AppEEARS task is structurally usable for V061 IRG."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.appeears_smoke_gate import evaluate_appeears_smoke_gate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("irg_receipt_json", type=Path)
    parser.add_argument(
        "--fail-on-gate-failure",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/aikens_appeears_live_smoke_gate.json"
        ),
    )
    args = parser.parse_args()

    receipt = json.loads(
        args.irg_receipt_json.read_text(encoding="utf-8")
    )
    gate = evaluate_appeears_smoke_gate(receipt)
    output = {
        "status": (
            "APPEEARS_LIVE_SMOKE_GO"
            if gate.passed
            else "APPEEARS_LIVE_SMOKE_NO_GO"
        ),
        "irg_receipt_source": str(args.irg_receipt_json),
        "gate": asdict(gate),
        "licensed_next_step": (
            "full_exact_manifest_environmental_extraction"
            if gate.passed
            else None
        ),
        "lambda_outcome_opened": False,
        "claim_boundary": (
            "structural live-product usability only; downstream IRG seasonal "
            "fit gates remain independent"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(
        "appeears_live_smoke_gate "
        f"passed={int(gate.passed)} "
        f"matched={gate.matched_rows} "
        f"output={gate.output_rows} "
        f"pixel_years={gate.pixel_years} "
        f"quality_good={gate.quality_good_rows} "
        f"snow_free={gate.snow_free_rows} "
        f"reasons={';'.join(gate.reasons) if gate.reasons else 'none'}"
    )
    if args.fail_on_gate_failure and not gate.passed:
        raise SystemExit("AppEEARS live smoke structural gate failed")


if __name__ == "__main__":
    main()
