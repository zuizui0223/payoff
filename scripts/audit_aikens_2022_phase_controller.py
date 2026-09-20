#!/usr/bin/env python3
"""Freeze published Aikens et al. (2022) phase-controller evidence.

This receipt uses only coefficients explicitly reported in the article text.
It does not reconstruct unpublished individual regressions and does not convert
the published regression slopes to per-km units because the coefficient scale
should be confirmed from the source table/code before rescaling.

Reference:
Aikens EO, Wyckoff TB, Sawyer H, Kauffman MJ. 2022.
Industrial energy development decouples ungulate migration from the green wave.
Nature Ecology & Evolution 6:1733-1741.
DOI: 10.1038/s41559-022-01887-9
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.phase_error_controller import audit_phase_controller


PUBLISHED_CONDITIONS = (
    {
        "footprint": "large",
        "development": "low",
        "phase_state": "early",
        "phase_state_support": "mean intercept significantly below zero",
        "intercept": -13.1,
        "slope": 0.0008,
        "slope_detected": True,
        "slope_p": 0.02,
        "published_interpretation": "let the green wave catch up",
    },
    {
        "footprint": "small",
        "development": "low",
        "phase_state": "early",
        "phase_state_support": "mean intercept significantly below zero",
        "intercept": -7.6,
        "slope": None,
        "slope_detected": False,
        "slope_p": None,
        "published_interpretation": (
            "mismatch did not change detectably over migration"
        ),
    },
    {
        "footprint": "large",
        "development": "medium",
        "phase_state": "late",
        "phase_state_support": (
            "article reports medium/high/sustained-high means 8.5-22.4 days late"
        ),
        "intercept": None,
        "slope": -0.001,
        "slope_detected": True,
        "slope_p": "<0.0001",
        "published_interpretation": "reduced mismatch after development",
    },
    {
        "footprint": "small",
        "development": "medium",
        "phase_state": "late",
        "phase_state_support": (
            "article reports medium/high/sustained-high means 8.5-22.4 days late"
        ),
        "intercept": None,
        "slope": -0.0004,
        "slope_detected": True,
        "slope_p": "<0.0001",
        "published_interpretation": "reduced mismatch after development",
    },
    {
        "footprint": "large",
        "development": "high",
        "phase_state": "late",
        "phase_state_support": (
            "late point estimate; article reports intercept test P=0.06 here"
        ),
        "intercept": None,
        "slope": None,
        "slope_detected": False,
        "slope_p": None,
        "published_interpretation": "no detected mismatch reduction",
    },
    {
        "footprint": "small",
        "development": "high",
        "phase_state": "late",
        "phase_state_support": (
            "mean intercept significantly above zero"
        ),
        "intercept": None,
        "slope": None,
        "slope_detected": False,
        "slope_p": None,
        "published_interpretation": "no detected mismatch reduction",
    },
    {
        "footprint": "large",
        "development": "sustained_high",
        "phase_state": "late",
        "phase_state_support": (
            "mean intercept significantly above zero"
        ),
        "intercept": None,
        "slope": -0.001,
        "slope_detected": True,
        "slope_p": "<0.001",
        "published_interpretation": "reduced mismatch after development",
    },
    {
        "footprint": "small",
        "development": "sustained_high",
        "phase_state": "late",
        "phase_state_support": (
            "mean intercept significantly above zero"
        ),
        "intercept": None,
        "slope": None,
        "slope_detected": False,
        "slope_p": None,
        "published_interpretation": "no detected mismatch reduction",
    },
)


def main() -> None:
    output = Path(
        "outputs/payoff_b_aikens_2022_phase_controller.json"
    )

    rows = []
    for condition in PUBLISHED_CONDITIONS:
        audit = audit_phase_controller(
            phase_state=condition["phase_state"],
            slope=condition["slope"],
            slope_detected=condition["slope_detected"],
            intercept=condition["intercept"],
        )
        rows.append(
            {
                **condition,
                "controller_audit": asdict(audit),
            }
        )

    restoring = sum(
        row["controller_audit"]["controller_class"]
        == "restoring"
        for row in rows
    )
    no_change = sum(
        row["controller_audit"]["controller_class"]
        == "no_detected_change"
        for row in rows
    )

    receipt = {
        "source": {
            "citation": (
                "Aikens et al. 2022 Nature Ecology & Evolution 6:1733-1741"
            ),
            "doi": "10.1038/s41559-022-01887-9",
        },
        "estimand": (
            "signed Days-From-Peak response along distance from development"
        ),
        "distance_scale": (
            "published regression-native distance units; figure is displayed "
            "in km but coefficients are not rescaled here pending source-table "
            "confirmation"
        ),
        "conditions": rows,
        "summary": {
            "conditions": len(rows),
            "restoring_controller_detected": restoring,
            "no_detected_route_phase_change": no_change,
        },
        "retained_interpretation": (
            "development changes both mismatch at barrier encounter and the "
            "ability to reduce mismatch downstream; controller recovery is "
            "distinct from the independent PAYOFF-B phenology rate h"
        ),
        "not_identified": [
            "independent timing-axis phenology rate h",
            "fixed-interval movement kernel parameters",
            "fitness penalty coefficients",
        ],
        "claim_boundary": (
            "published aggregate regression evidence; no raw individual "
            "trajectory refit and no coefficient-unit rescaling"
        ),
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)
    for row in rows:
        audit = row["controller_audit"]
        print(
            "phase_controller "
            f"footprint={row['footprint']} "
            f"development={row['development']} "
            f"phase={row['phase_state']} "
            f"class={audit['controller_class']} "
            f"slope={row['slope']}"
        )


if __name__ == "__main__":
    main()
