import csv
import json
import subprocess
import sys
from math import isclose
from pathlib import Path


def test_registered_hard_module_out_of_sample_validation(tmp_path: Path):
    output_dir = tmp_path / "hard_module_validation"
    subprocess.run(
        [
            sys.executable,
            "scripts/validate_hard_module_cost_out_of_sample.py",
            "--input",
            "examples/three_function/hard_module_worldlines_validation.csv",
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["fit_count"] == 1
    assert summary["holdout_count"] == 1
    assert isclose(summary["kappa_hat"], 1.0, rel_tol=1e-12, abs_tol=1e-12)
    assert summary["fit_weighted_sse"] < 1e-28
    assert summary["holdout_max_abs_residual"] < 1e-14
    assert summary["holdout_mean_abs_residual"] < 1e-14
    assert summary["holdout_architectures"] == ["three_module_111"]

    with (output_dir / "validation_receipts.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    holdout = next(row for row in rows if row["role"] == "holdout")
    assert holdout["architecture_id"] == "three_module_111"
    assert isclose(float(holdout["predicted_margin"]), 8.0 / 3.0, rel_tol=1e-12)
    assert abs(float(holdout["prediction_residual"])) < 1e-14
