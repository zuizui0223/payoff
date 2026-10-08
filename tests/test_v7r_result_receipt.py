import json
import subprocess
import sys
from pathlib import Path

import pytest


def test_v7r_frozen_result_is_reproducible(tmp_path):
    source = Path("data/payoff_b_v7r_transition_input_20261007.csv")
    output = tmp_path / "result.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_v7r_direct_recourse.py",
            str(source),
            "--output",
            str(output),
        ],
        check=True,
    )
    out = json.loads(output.read_text())
    assert out["status"] == "PRIMARY_NOT_SUPPORTED"
    assert out["primary"]["fit"]["beta_QR"] == pytest.approx(
        1.3733376461853433, abs=1e-10
    )
    assert out["primary"]["permutation"]["valid_permutations"] == 2880
    assert out["primary"]["permutation"]["one_sided_p"] == pytest.approx(
        0.5699409927108643, abs=1e-12
    )
    assert out["sensitivities"]["R_local_edge_width"]["beta_QR"] == pytest.approx(
        0.024497730599506037, abs=1e-10
    )
