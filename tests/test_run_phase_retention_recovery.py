import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_phase_retention_recovery.py"


def test_recovery_cli_writes_seeded_null_receipt(tmp_path: Path):
    output = tmp_path / "recovery.json"
    run = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--true-lambda",
            "1",
            "--latent-phase-sd",
            "10",
            "--predictor-error-sd",
            "10",
            "--outcome-error-sd",
            "10",
            "--error-correlation",
            "0",
            "--process-noise-sd",
            "0",
            "--n-pairs",
            "100",
            "--replicates",
            "50",
            "--seed",
            "123",
            "--observed-lambda",
            "0.86",
            "--output",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert run.returncode == 0, run.stderr

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["status"] == "lambda_recovery_complete"
    assert payload["design"]["true_lambda"] == 1.0
    assert payload["design"]["n_pairs"] == 100
    assert payload["summary"]["replicates"] == 50
    assert payload["summary"]["expected_naive_lambda"] == 0.5
    assert 0.0 < payload["lower_tail_null_probability"] <= 1.0
    assert "measurement-error calibration" in payload["claim_boundary"]
