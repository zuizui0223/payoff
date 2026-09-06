import csv
import json
import subprocess
import sys
from math import isclose
from pathlib import Path


def test_registered_hard_partition_feedback_validation(tmp_path: Path):
    output_dir = tmp_path / "feedback_validation"
    subprocess.run(
        [
            sys.executable,
            "scripts/validate_hard_partition_feedback.py",
            "--functions",
            "examples/three_function/functions.csv",
            "--pairs",
            "examples/three_function/hard_partition_feedback_validation.csv",
            "--kappa",
            "1.0",
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["fit_pair_count"] == 1
    assert summary["holdout_pair_count"] == 1
    assert isclose(summary["kappa_frozen"], 1.0, rel_tol=1e-12)
    assert isclose(summary["gamma_hat"], -1.0, rel_tol=1e-12, abs_tol=1e-12)
    assert summary["fit_gamma_weighted_sse"] < 1e-28
    assert summary["fit_max_abs_phi_bridge_residual"] < 1e-14
    assert summary["holdout_max_abs_phi_bridge_residual"] < 1e-14
    assert summary["holdout_max_abs_delta0_residual"] < 1e-14
    assert summary["holdout_max_abs_delta1_residual"] < 1e-14
    assert summary["holdout_pairs"] == ["S_vs_M"]

    with (output_dir / "feedback_receipts.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))
    fit = next(row for row in rows if row["role"] == "fit")
    holdout = next(row for row in rows if row["role"] == "holdout")

    assert isclose(float(fit["partition_distance"]), 1.0, rel_tol=1e-12)
    assert isclose(float(fit["phi_arch"]), -0.5, rel_tol=1e-12)
    assert isclose(float(fit["eta_observed"]), -1.0, rel_tol=1e-12)

    assert isclose(float(holdout["partition_distance"]), 2.0, rel_tol=1e-12)
    assert isclose(float(holdout["phi_arch"]), 19.0 / 6.0, rel_tol=1e-12)
    assert isclose(float(holdout["eta_predicted"]), -2.0, rel_tol=1e-12)
    assert isclose(float(holdout["delta0_predicted"]), 31.0 / 6.0, rel_tol=1e-12)
    assert isclose(float(holdout["delta1_predicted"]), 7.0 / 6.0, rel_tol=1e-12)
