import csv
import json
import subprocess
import sys
from math import isclose
from pathlib import Path


def test_registered_hard_module_end_to_end_pipeline(tmp_path: Path):
    output_dir = tmp_path / "end_to_end"
    subprocess.run(
        [
            sys.executable,
            "scripts/hard_module_end_to_end.py",
            "--functions",
            "examples/three_function/functions.csv",
            "--worldlines",
            "examples/three_function/hard_module_end_to_end_worldlines.csv",
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["function_ids"] == ["F1", "F2", "F3"]
    assert isclose(summary["fully_shared_conflict_load"], 14.0 / 3.0, rel_tol=1e-12)
    assert summary["fit_architecture_count"] == 1
    assert summary["holdout_architecture_count"] == 1
    assert isclose(summary["kappa_hat"], 1.0, rel_tol=1e-12, abs_tol=1e-12)
    assert summary["fit_weighted_sse"] < 1e-28
    assert summary["holdout_max_abs_residual"] < 1e-14

    assert summary["optimal_module_count"] == 2
    assert summary["optimal_modules"] == "{F1,F2}|{F3}"
    assert isclose(summary["optimal_recovery"], 25.0 / 6.0, rel_tol=1e-12)
    assert isclose(summary["optimal_release_fraction"], 25.0 / 28.0, rel_tol=1e-12)
    assert isclose(summary["optimal_architecture_cost"], 1.0, rel_tol=1e-12)
    assert isclose(summary["optimal_net_gain"], 19.0 / 6.0, rel_tol=1e-12)
    assert isclose(
        summary["optimal_split_accessibility_threshold"],
        25.0 / 6.0,
        rel_tol=1e-12,
    )
    assert summary["optimal_split_accessible"] is True
    assert summary["greedy_final_modules"] == "{F1,F2}|{F3}"
    assert summary["greedy_matches_global"] is True

    with (output_dir / "worldline_receipts.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))
    fit = next(row for row in rows if row["role"] == "fit")
    holdout = next(row for row in rows if row["role"] == "holdout")
    assert isclose(float(fit["recovery"]), 25.0 / 6.0, rel_tol=1e-12)
    assert isclose(float(holdout["recovery"]), 14.0 / 3.0, rel_tol=1e-12)
    assert isclose(float(holdout["predicted_margin"]), 8.0 / 3.0, rel_tol=1e-12)
    assert abs(float(holdout["prediction_residual"])) < 1e-14
