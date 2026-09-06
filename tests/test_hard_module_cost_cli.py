import json
import subprocess
import sys
from math import isclose
from pathlib import Path


def test_registered_hard_module_cost_cli(tmp_path: Path):
    output_dir = tmp_path / "hard_module_cost"
    subprocess.run(
        [
            sys.executable,
            "scripts/identify_hard_module_cost.py",
            "--input",
            "examples/three_function/hard_module_worldlines.csv",
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["architecture_count"] == 2
    assert isclose(summary["kappa_hat"], 1.0, rel_tol=1e-12, abs_tol=1e-12)
    assert summary["weighted_sse"] < 1e-28
    assert summary["max_abs_bridge_residual"] < 1e-14
    assert isclose(summary["implied_kappa_min"], 1.0, rel_tol=1e-12)
    assert isclose(summary["implied_kappa_max"], 1.0, rel_tol=1e-12)
    assert summary["input_used_analysis_weights"] is True

    receipts = (output_dir / "cost_receipts.csv").read_text(encoding="utf-8")
    assert "two_module_011" in receipts
    assert "three_module_111" in receipts
    assert "bridge_residual" in receipts
