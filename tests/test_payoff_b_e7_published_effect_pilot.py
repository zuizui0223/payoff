from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "payoff_b_e7_published_effect_pilot_result_20260928.json"


def test_e7_screen_is_nonpromoted_and_heterogeneous():
    x = json.loads(RESULT.read_text(encoding="utf-8"))
    assert x["status"] == "SCREEN_COMPLETE_E7_NOT_PROMOTED"
    assert x["promotion_gate"]["common_unit_found"] is True
    assert x["promotion_gate"]["at_least_three_systems_found"] is True
    assert x["promotion_gate"]["covariance_safe_uncertainty_at_least_three"] is False
    assert x["promotion_gate"]["paper2_e7_promoted"] is False
    assert x["ecological_result"]["negative_systems"] == 3
    assert x["ecological_result"]["positive_systems"] == 1
    assert x["ecological_result"]["universal_partner_ordering_supported"] is False
    assert x["diagnostic_only_meta"]["I2_percent"] > 90
    assert x["diagnostic_only_meta"]["random_normal_ci95"][0] < 0
    assert x["diagnostic_only_meta"]["random_normal_ci95"][1] > 0


def test_e7_diagnostic_cannot_enter_canonical_claims():
    x = json.loads(RESULT.read_text(encoding="utf-8"))
    assert x["paper2_decision"]["manuscript_change"] is False
    assert x["paper2_decision"]["canonical_empirical_ceiling"].startswith("E6")
    prohibited = " ".join(x["prohibited_claims"])
    assert "valid E7 meta-analytic estimate" in prohibited
    assert "universally" in prohibited
