import json
import subprocess
import sys
from pathlib import Path


def test_registered_three_function_ensemble_support(tmp_path: Path):
    output_dir = tmp_path / "ensemble"
    subprocess.run(
        [
            sys.executable,
            "scripts/topology_uncertainty_ensemble.py",
            "--input",
            "examples/three_function/ensemble.json",
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads(
        (output_dir / "ensemble_summary.json").read_text(encoding="utf-8")
    )
    assert summary["draw_count"] == 5
    assert summary["context"]["context_id"] == "THREE_FUNCTION_SYNTHETIC_V1"
    assert summary["context"]["fitness_scale_id"] == "SYNTHETIC_COMMON_FITNESS"
    assert summary["population"] == {
        "gamma": -0.25,
        "population_size": 20,
        "beta": 0.4,
    }

    assert summary["first_pressure_edge_support"] == {"F1-F3": 1.0}
    assert summary["first_favorable_edge_support"] == {"F1-F3": 1.0}
    assert summary["best_topology_support"] == {"011": 0.8, "111": 0.2}
    assert summary["greedy_final_topology_support"] == {"011": 1.0}
    assert summary["consensus_best_topology"] == "011"
    assert summary["consensus_best_topology_fraction"] == 0.8
    assert summary["greedy_matches_global_fraction"] == 0.8
    assert summary["minimum_global_reserve"] > 0.0

    # Population-level transport is more robust than the orientation of the
    # intrinsic best topology in this registered fixture.
    assert summary["top_pair_unordered_support"] == {"011-111": 1.0}
    assert summary["top_pair_phase_support"] == {"stable_pairwise_coexistence": 1.0}
    assert summary["both_top_pair_invade_fraction"] == 1.0
    assert summary["best_has_larger_reciprocal_fixation_fraction"] == 1.0
    assert 0.0 < summary["mean_runner_over_best_fixation_ratio"] < 1.0

    receipts = (output_dir / "draw_receipts.csv").read_text(encoding="utf-8")
    assert "first_pressure_edge" in receipts
    assert "global_reserve" in receipts
    assert "local_reserve" in receipts
    assert "top_pair_class" in receipts
    assert "rho_runner_into_best" in receipts
