import json
import subprocess
import sys
from math import isclose
from pathlib import Path


def test_registered_three_function_hard_module_cli(tmp_path: Path):
    output_dir = tmp_path / "hard_modules"
    subprocess.run(
        [
            sys.executable,
            "scripts/predict_hard_module_partition.py",
            "--functions",
            "examples/three_function/functions.csv",
            "--extra-module-cost",
            "1.0",
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["function_count"] == 3
    assert summary["function_ids"] == ["F1", "F2", "F3"]
    assert isclose(summary["fully_shared_conflict_load"], 14.0 / 3.0, rel_tol=1e-12)
    assert summary["optimal_module_count"] == 2
    assert summary["optimal_modules"] == "{F1,F2}|{F3}"
    assert isclose(summary["within_loss"], 0.5, rel_tol=1e-12)
    assert isclose(summary["recovery"], 25.0 / 6.0, rel_tol=1e-12)
    assert isclose(summary["architecture_cost"], 1.0, rel_tol=1e-12)
    assert isclose(summary["net_gain"], 19.0 / 6.0, rel_tol=1e-12)

    assert isclose(
        summary["optimal_split_accessibility_threshold"],
        25.0 / 6.0,
        rel_tol=1e-12,
    )
    assert summary["optimal_split_accessible"] is True
    assert isclose(
        summary["optimal_split_tree_weakest_gain"], 25.0 / 6.0, rel_tol=1e-12
    )
    assert summary["greedy_final_modules"] == "{F1,F2}|{F3}"
    assert summary["greedy_steps"] == 1
    assert summary["greedy_matches_global_partition"] is True
    assert summary["supported_module_counts"] == [1, 2, 3]

    fixed = (output_dir / "fixed_module_counts.csv").read_text(encoding="utf-8")
    intervals = (output_dir / "module_count_intervals.csv").read_text(encoding="utf-8")
    greedy = (output_dir / "greedy_split_path.csv").read_text(encoding="utf-8")
    tree = json.loads(
        (output_dir / "optimal_split_tree.json").read_text(encoding="utf-8")
    )
    assert "{F1,F2}|{F3}" in fixed
    assert "25/6" not in intervals  # CSV uses numeric values, not symbolic text.
    assert "{F1,F2}|{F3}" in greedy
    assert isclose(tree["split_gain"], 25.0 / 6.0, rel_tol=1e-12)
