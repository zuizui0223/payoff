import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_phase_retention_measurement_error_stress.py"


def test_stress_audit_identifies_wigeon_as_low_required_independent_error_ratio(
    tmp_path: Path,
):
    csv_output = tmp_path / "stress.csv"
    receipt = tmp_path / "stress.json"
    run = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--error-correlations",
            "0",
            "--csv-output",
            str(csv_output),
            "--receipt-output",
            str(receipt),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert run.returncode == 0, run.stderr

    with csv_output.open(
        newline="",
        encoding="utf-8",
    ) as handle:
        rows = list(csv.DictReader(handle))

    by_id = {row["system_id"]: row for row in rows}
    wigeon = by_id["eurasian_wigeon_staging_transition"]
    mule = by_id["mule_deer_whole_migration"]
    svalbard = by_id[
        "barnacle_svalbard_southern_norway_to_svalbard"
    ]

    assert abs(
        float(
            wigeon[
                "required_equal_error_sd_over_latent_phase_sd"
            ]
        )
        - 0.4035738201
    ) < 1e-9
    assert float(
        mule[
            "required_equal_error_sd_over_latent_phase_sd"
        ]
    ) > 2.8
    assert svalbard["finite_equal_error_solution"] == "False"
    assert (
        svalbard[
            "required_equal_error_sd_over_latent_phase_sd"
        ]
        == ""
    )

    payload = json.loads(
        receipt.read_text(encoding="utf-8")
    )
    assert "stress thresholds" in payload["claim_boundary"]
