import json
import subprocess
import sys
from math import isclose
from pathlib import Path


def test_generic_three_function_cli_reports_topology_and_reserves(tmp_path: Path):
    output_dir = tmp_path / "prediction"
    subprocess.run(
        [
            sys.executable,
            "scripts/predict_modular_topology.py",
            "--functions",
            "examples/three_function/functions.csv",
            "--edges",
            "examples/three_function/edges.csv",
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["highest_reference_pressure_edge"] == "F1-F3"
    assert summary["best_vertex_bits"] == "011"
    assert summary["best_vertex_modules"] == "{F1,F2}|{F3}"
    assert summary["runner_up_vertex_bits"] == "111"
    assert summary["greedy_matches_global_vertex"] is True
    assert summary["best_vertex_strict_local_stability"] is True
    assert isclose(summary["best_vertex_global_reserve"], 1.0 / 15.0, abs_tol=1e-12)
    assert isclose(summary["best_vertex_local_reserve"], 13.0 / 45.0, abs_tol=1e-12)

    assert (output_dir / "edge_pressures.csv").exists()
    assert (output_dir / "greedy_release_path.csv").exists()
    assert (output_dir / "vertex_topologies.csv").exists()
