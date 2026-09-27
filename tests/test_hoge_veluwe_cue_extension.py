from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "payoff_b_hoge_veluwe_cue_extension.py"
BASELINE = ROOT / "data" / "payoff_b_cv24c_frozen_cue_prefix_1980_2010.json"


def load_module():
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location("hv_cue_extension", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeFrame:
    def __init__(self, rows):
        self.rows = rows

    def itertuples(self, index=False):
        assert index is False
        for row in self.rows:
            yield SimpleNamespace(**row)


def test_frozen_prefix_receipt_matches_recovered_cv24c_artifact():
    module = load_module()
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))

    assert baseline["source_workflow_run_id"] == 36270835505
    assert baseline["source_artifact_id"] == 10915252374
    assert len(baseline["rows"]) == 31
    assert baseline["rows"][0]["year"] == 1980
    assert baseline["rows"][-1]["year"] == 2010
    assert module.canonical_hash(
        baseline["rows"],
        12,
    ) == baseline["canonical_round_12_sha256"]


def test_source_faithful_prefix_gate_passes_exact_reconstruction():
    module = load_module()
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    observed = FakeFrame(
        [
            {
                "year": row["year"],
                "ivory_coast_temp_c": row["ivory_coast_temp_c"],
            }
            for row in baseline["rows"]
        ]
    )

    result = module.validate_frozen_prefix(observed, baseline)

    assert result["passed"] is True
    assert result["max_abs_difference_c"] == 0.0
    assert result["expected_round9_sha256"] == result["observed_round9_sha256"]


def test_source_faithful_prefix_gate_fails_on_retuned_value():
    module = load_module()
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    rows = [
        {
            "year": row["year"],
            "ivory_coast_temp_c": row["ivory_coast_temp_c"],
        }
        for row in baseline["rows"]
    ]
    rows[-1]["ivory_coast_temp_c"] += 0.01

    result = module.validate_frozen_prefix(FakeFrame(rows), baseline)

    assert result["passed"] is False
    assert result["max_abs_difference_c"] > result["tolerance_c"]
