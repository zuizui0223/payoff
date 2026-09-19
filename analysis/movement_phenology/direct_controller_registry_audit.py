#!/usr/bin/env python3
"""Audit the direct movement–phenology controller registry.

The registry deliberately contains different actuator architectures. The common
cross-system output is phase retention |lambda| after one ecologically
meaningful correction opportunity. Actuator gains are reported separately.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


SOURCE = Path("data/MOVEMENT_PHENOLOGY_DIRECT_CONTROLLER_REGISTRY.csv")
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)


def main():
    d = pd.read_csv(SOURCE)

    required = [
        "system_id",
        "taxon",
        "controller_architecture",
        "phase_transfer_lambda",
        "phase_retention_abs",
        "controller_stability_class",
    ]
    missing = [x for x in required if x not in d.columns]
    if missing:
        raise SystemExit(f"Missing registry columns: {missing}")

    for c in ("phase_transfer_lambda", "phase_retention_abs"):
        d[c] = pd.to_numeric(d[c], errors="coerce")

    direct = d[d["status"].astype(str).str.contains("DIRECT_CONTROLLER")].copy()
    direct = direct[np.isfinite(direct["phase_transfer_lambda"])].copy()
    if direct.empty:
        raise SystemExit("No direct controllers with finite lambda")

    direct["correction_strength"] = 1.0 - direct["phase_retention_abs"]
    direct["stable_map"] = direct["phase_retention_abs"] < 1.0
    direct["overshoot"] = direct["phase_transfer_lambda"] < 0.0

    summary = {
        "n_direct_rows": int(len(direct)),
        "n_taxa": int(direct["taxon"].nunique()),
        "taxa": sorted(direct["taxon"].dropna().astype(str).unique()),
        "n_stable_maps": int(direct["stable_map"].sum()),
        "stable_fraction": float(direct["stable_map"].mean()),
        "n_overshoot_maps": int(direct["overshoot"].sum()),
        "median_abs_lambda": float(direct["phase_retention_abs"].median()),
        "median_correction_strength": float(direct["correction_strength"].median()),
        "min_abs_lambda": float(direct["phase_retention_abs"].min()),
        "max_abs_lambda": float(direct["phase_retention_abs"].max()),
        "population_route_replication_gate": bool(len(direct) >= 3),
        "cross_taxon_gate_three_taxa": bool(direct["taxon"].nunique() >= 3),
        "claim_ceiling": (
            "Descriptive registry audit. Rows can share species, paper, and "
            "individuals; do not treat them as independent effect sizes."
        ),
    }

    direct.to_csv(OUT / "direct_controller_registry_audit.csv", index=False)
    (OUT / "direct_controller_registry_audit.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps(summary, indent=2))
    print(direct[
        [
            "system_id",
            "taxon",
            "controller_architecture",
            "phase_transfer_lambda",
            "phase_retention_abs",
            "correction_strength",
            "controller_stability_class",
        ]
    ].to_string(index=False))


if __name__ == "__main__":
    main()
