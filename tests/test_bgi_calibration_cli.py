import json
import subprocess
import sys
from pathlib import Path


INPUT = Path("data/STREPTOMYCES_M5_BGI_CALIBRATION_CONTROL_EVIDENCE_V1.tsv")


def test_calibration_cli_runs_from_repo_root_and_reproduces_frozen_thresholds(tmp_path):
    out = tmp_path / "result.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/adjudicate_bgi_marker_calibration.py",
            str(INPUT),
            "--output",
            str(out),
        ],
        check=True,
    )
    data = json.loads(out.read_text())
    assert data["target_data_used"] is False
    assert data["m5_bgi_marker_class_opened"] is False
    assert data["calibration_qualified"] is True
    assert data["absence_max_ratio"] == 0.000818710126322
    assert data["presence_min_ratio"] == 0.40016549829
    assert data["absent_pair_count"] == 10
    assert data["present_pair_count"] == 14
    assert data["absent_candidate_count"] == 5
    assert data["present_candidate_count"] == 6
    assert data["unresolved_pair_count"] == 0
    assert data["qualified_d_reference_count_increment"] == 0
    assert data["architecture_specific_inference_open"] is False
