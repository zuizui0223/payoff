from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "payoff_b_e7_published_effect_pilot.py"
INPUT = ROOT / "data" / "payoff_b_e7_published_effect_pilot_input_20260928.json"
ELIGIBILITY = ROOT / "data" / "payoff_b_e7_source_eligibility_20260928.json"


def module():
    spec = importlib.util.spec_from_file_location("e7pilot", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


def test_e7_screen_is_fail_closed():
    x = json.loads(ELIGIBILITY.read_text(encoding="utf-8"))
    assert x["status"] == "SCREEN_COMPLETE_PROMOTION_GATE_NOT_PASSED"
    assert x["promotion_gate"]["passed"] is False
    assert x["paper2_decision"] == "KEEP_E6_AS_CANONICAL_CEILING"
    assert x["promotion_gate"]["independent_system_count_with_point_estimate"] == 4
    assert x["promotion_gate"]["independent_system_count_with_harmonized_inferential_variance"] < 3


def test_published_effect_input_is_explicitly_noninferential():
    x = json.loads(INPUT.read_text(encoding="utf-8"))
    assert x["status"] == "NONPROMOTABLE_DIAGNOSTIC"
    assert len(x["rows"]) == 4
    assert sum(row["inferential_variance_valid"] is True for row in x["rows"]) == 1
    assert any(row["inferential_variance_valid"] is False for row in x["rows"])
    assert "must not appear" in x["hard_boundary"]


def test_diagnostic_exposes_heterogeneity_without_promotion():
    m = module()
    x = json.loads(INPUT.read_text(encoding="utf-8"))
    out = m.dl_meta(x["rows"])
    assert out["k"] == 4
    assert out["I2_percent_diagnostic"] > 50
    effects = [row["effect"] for row in x["rows"]]
    assert min(effects) < 0 < max(effects)
