#!/usr/bin/env python3
"""Audit published mule-deer phase summaries against the PAYOFF-B h inverse.

The published Nature Communications group means use signed Days-From-Peak:
negative = ahead of peak IRG, positive = behind peak IRG.

This script intentionally does not estimate a per-generation phenology rate.
It only checks whether each whole-route start/end summary is mathematically
compatible with the simple monotone first-order residual map.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tracking_empirical_parameterization import (
    audit_residual_compression,
)


PUBLISHED_GROUP_MEANS = {
    "early": {
        "animal_years": 47,
        "start_days_from_peak": -30.0,
        "end_days_from_peak": 4.0,
    },
    "mid": {
        "animal_years": 58,
        "start_days_from_peak": -2.0,
        "end_days_from_peak": 7.0,
    },
    "late": {
        "animal_years": 47,
        "start_days_from_peak": 20.0,
        "end_days_from_peak": 11.0,
    },
}


def main() -> None:
    output = Path(
        "outputs/payoff_b_mule_deer_phase_summary_audit.json"
    )

    groups = {}
    for name, row in PUBLISHED_GROUP_MEANS.items():
        audit = audit_residual_compression(
            row["start_days_from_peak"],
            row["end_days_from_peak"],
        )
        groups[name] = {
            **row,
            "audit": asdict(audit),
            "per_step_h_licensed": False,
            "reason": (
                "published values summarize an entire migration, not one "
                "frozen PAYOFF-B decision interval"
                if audit.monotone_first_order_compatible
                else "published start/end means violate the monotone "
                "single-step residual inverse"
            ),
        }

    receipt = {
        "system": "Red Desert long-distance migratory mule deer",
        "source": {
            "article": (
                "Ortega et al. 2023, Nature Communications 14:2008"
            ),
            "doi": "10.1038/s41467-023-37750-z",
            "summary_scope": "published group means only",
        },
        "sign_convention": (
            "negative Days-From-Peak = ahead of peak IRG; "
            "positive = behind peak IRG"
        ),
        "groups": groups,
        "retained_conclusion": (
            "none of the published whole-route group means licenses direct "
            "insertion as a per-step PAYOFF-B phenology rate"
        ),
        "next_required_data": (
            "individual or fixed-interval residual transitions with the "
            "decision interval declared in advance"
        ),
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)
    for name, row in groups.items():
        audit = row["audit"]
        print(
            "mule_deer_phase_audit "
            f"group={name} "
            f"start={row['start_days_from_peak']} "
            f"end={row['end_days_from_peak']} "
            f"status={audit['status']} "
            f"compatible={int(audit['monotone_first_order_compatible'])} "
            "per_step_h_licensed=0"
        )


if __name__ == "__main__":
    main()
