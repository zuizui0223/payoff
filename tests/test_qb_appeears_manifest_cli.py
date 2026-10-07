import csv
import json
import subprocess
import sys
from pathlib import Path


def test_qb_manifest_cli(tmp_path):
    out = tmp_path / "manifest.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/build_qb_appeears_manifest.py",
            "--output",
            str(out),
        ],
        check=True,
    )
    payload = json.loads(out.read_text())
    assert payload["region_count"] == 9
    assert payload["points_per_region"] == 9
    assert payload["total_points"] == 81
    assert payload["task_count"] == 11
    assert payload["years"] == list(range(2001, 2012))
    assert all(row["cell_count"] == 81 for row in payload["tasks"])
    assert payload["environment_only"] is True
