import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "fit_peak_irg_from_ndvi.py"


def test_allow_unfit_pixel_years_records_failure_and_writes_empty_table(tmp_path: Path):
    source = tmp_path / "ndvi.csv"
    output = tmp_path / "peak.csv"
    receipt = tmp_path / "receipt.json"

    with source.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "pixel_id",
                "year",
                "doy",
                "ndvi",
                "snow_free",
                "quality_good",
            ],
        )
        writer.writeheader()
        for doy in (1, 9, 17, 25):
            writer.writerow(
                {
                    "pixel_id": "p1",
                    "year": 2020,
                    "doy": doy,
                    "ndvi": 0.2,
                    "snow_free": "true",
                    "quality_good": "true",
                }
            )

    run = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(source),
            "--modis-product",
            "MOD09Q1.061",
            "--v061-reconstruction-lane",
            "v061_primary_successor_after_v006_decommission",
            "--allow-unfit-pixel-years",
            "--output",
            str(output),
            "--receipt-output",
            str(receipt),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert run.returncode == 0, run.stderr

    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert payload["attempted_pixel_years"] == 1
    assert payload["pixel_years"] == 0
    assert payload["failed_pixel_years"] == 1
    assert payload["failed_pixel_year_details"][0]["pixel_id"] == "p1"
    assert payload["reconstruction_lane"] == (
        "v061_primary_successor_after_v006_decommission"
    )

    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == []
