import json
import subprocess
import sys
from pathlib import Path


def test_racing_information_absorption_cli(tmp_path):
    source = Path("examples/racing/racing_information_absorption_synthetic.csv")
    output = tmp_path / "out.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_racing_information_absorption.py",
            str(source),
            "--output",
            str(output),
            "--grid-points",
            "101",
        ],
        check=True,
    )
    payload = json.loads(output.read_text())
    assert payload["schema"] == "payoff_b_racing_information_absorption_v1"
    rows = {row["time_slice"]: row for row in payload["time_slices"]}
    assert set(rows) == {"T-60", "LAST"}
    assert rows["T-60"]["fitted_form_weight"] > rows["LAST"]["fitted_form_weight"]
    assert (
        rows["T-60"]["incremental_form_value_over_market"]
        > rows["LAST"]["incremental_form_value_over_market"]
    )
    assert rows["LAST"]["test_market_log_loss"] < rows["T-60"]["test_market_log_loss"]
