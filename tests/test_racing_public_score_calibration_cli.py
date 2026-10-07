import csv
import json
import subprocess
import sys
from pathlib import Path


def test_public_score_calibration_cli_fits_train_only_and_writes_probabilities(tmp_path):
    source = Path("examples/racing/previous_day_tm_scores_synthetic.csv")
    out_csv = tmp_path / "calibrated.csv"
    receipt = tmp_path / "receipt.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/calibrate_racing_public_scores.py",
            str(source),
            "--output-csv",
            str(out_csv),
            "--receipt-json",
            str(receipt),
            "--max-scale",
            "3",
            "--grid-points",
            "301",
        ],
        check=True,
    )

    meta = json.loads(receipt.read_text())
    assert meta["fit_scope"] == "train_only"
    assert meta["training_races"] == 4
    assert meta["test_races"] == 2
    assert meta["scale"] > 0.0

    with out_csv.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    by_race = {}
    for row in rows:
        by_race.setdefault(row["race_id"], []).append(row)
    for race_rows in by_race.values():
        total = sum(float(row["form_probability"]) for row in race_rows)
        assert total == pytest.approx(1.0)


import pytest
