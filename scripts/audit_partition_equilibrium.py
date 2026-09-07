#!/usr/bin/env python3
"""Reproduce the synthetic complete five-partition equilibrium audit."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.concave_partition_equilibrium import audit_partition_mixture, stable_negative_feedback_mixture
from src.full_partition_audit import exact_five_partition_frequencies, registered_five_partition_problem, restricted_three_partition_frequencies


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--h", type=float, nargs="+", default=[0.25, 0.5, 0.75, 1, 1.5, 2, 13 / 6, 3, 10])
    args = parser.parse_args()
    problem = registered_five_partition_problem()
    names = problem.pop("names")
    rows = []
    certificates = []
    for h in args.h:
        exact = exact_five_partition_frequencies(h)
        if h == 0:
            parser.error("the negative-feedback numerical solver requires h>0")
        solved = stable_negative_feedback_mixture(**problem, gamma=-h)
        audit = audit_partition_mixture(**problem, frequencies=restricted_three_partition_frequencies(h), gamma=-h)
        error = max(abs(p - q) for p, q in zip(exact, solved["frequencies"]))
        if error > 1e-8:
            raise RuntimeError("numerical equilibrium disagrees with closed form")
        certificates.append({"h": h, "numerically_unique": solved["numerically_unique"], "normalized_kkt_residual": solved["normalized_kkt_residual"], "max_formula_error": error, "restricted_three_is_invaded": bool(audit["invadable_candidate_indices"])})
        for i, name in enumerate(names):
            rows.append({"h": h, "strategy": name, "frequency": solved["frequencies"][i], "exact_frequency": exact[i], "invasion_margin_at_full_equilibrium": solved["invasion_margins"][i], "invasion_margin_at_restricted_equilibrium": audit["invasion_margins"][i]})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "five_partition_equilibria.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {"status": "SYNTHETIC_MODEL_AUDIT_NOT_EMPIRICAL", "candidate_count": 5, "includes_all_partitions": True, "exact_h_boundaries": [0.5, 1.0, 13 / 6], "certificates": certificates}
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, allow_nan=False))


if __name__ == "__main__":
    main()
