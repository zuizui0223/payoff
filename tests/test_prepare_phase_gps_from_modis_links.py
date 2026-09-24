import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "prepare_phase_gps_from_modis_links.py"


def write_links(path: Path, *, duplicate=False, year_mismatch=False):
    rows = [
        {
            "observation_id": "o1",
            "animal_id": "A",
            "animal_year": "A_2020",
            "group": "small",
            "timestamp": "2020-04-01T12:00:00",
            "year": "2020",
            "cell_id": "modis250_r1_c2",
        },
        {
            "observation_id": "o1" if duplicate else "o2",
            "animal_id": "B",
            "animal_year": "B_2020",
            "group": "large",
            "timestamp": "2020-04-02T12:00:00",
            "year": "2021" if year_mismatch else "2020",
            "cell_id": "modis250_r3_c4",
        },
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run_script(tmp_path: Path, *extra):
    source = tmp_path / "links.csv"
    output = tmp_path / "phase_gps.csv"
    receipt = tmp_path / "receipt.json"
    command = [
        sys.executable,
        str(SCRIPT),
        str(source),
        "--output",
        str(output),
        "--receipt-output",
        str(receipt),
        *extra,
    ]
    return source, output, receipt, command


def test_phase_gps_conversion_preserves_frozen_cell_identity(tmp_path):
    source, output, receipt, command = run_script(
        tmp_path,
        "--expected-observations",
        "2",
    )
    write_links(source)
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr

    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["pixel_id"] for row in rows] == [
        "modis250_r1_c2",
        "modis250_r3_c4",
    ]
    assert [row["observation_id"] for row in rows] == ["o1", "o2"]

    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert payload["observations"] == 2
    assert payload["unique_pixels"] == 2
    assert payload["groups"] == {"large": 1, "small": 1}
    assert payload["lambda_outcome_opened"] is False


def test_phase_gps_conversion_rejects_duplicate_observation_ids(tmp_path):
    source, _, _, command = run_script(tmp_path)
    write_links(source, duplicate=True)
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert "duplicate observation_id" in completed.stderr


def test_phase_gps_conversion_rejects_timestamp_year_mismatch(tmp_path):
    source, _, _, command = run_script(tmp_path)
    write_links(source, year_mismatch=True)
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert "year mismatch" in completed.stderr
