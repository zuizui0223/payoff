from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "payoff_b_pairwise_tracking_bridge_20260929.json"


def test_pairwise_tracking_bridge_is_source_backed_and_bounded():
    x = json.loads(RESULT.read_text(encoding="utf-8"))
    assert x["status"] == "SOURCE_BACKED_PAIRWISE_BRIDGE_READY"
    assert len(x["interaction_pairs"]) == 3
    assert x["source_conclusions"]["all_three_temporal_slopes_below_one"] is True
    assert x["manuscript_decision"]["abstract_change"] is False
    assert x["manuscript_decision"]["figure_change"] is False


def test_all_pairwise_tracking_slopes_are_below_unity():
    x = json.loads(RESULT.read_text(encoding="utf-8"))
    for row in x["interaction_pairs"]:
        assert row["major_axis_slope"] < 1
        assert row["major_axis_ci95"][1] < 1
        assert row["tracking_deficit_1_minus_slope"] > 0
        assert row["added_mismatch_per_10d_resource_advance"] > 0


def test_deadline_mechanism_remains_prospective():
    x = json.loads(RESULT.read_text(encoding="utf-8"))
    prohibited = " ".join(x["not_licensed"])
    assert "D2-D1" in prohibited
    assert "q1 < q <= q2" in prohibited
    assert "causal mechanism" in prohibited
    assert x["manuscript_decision"]["claim_ceiling"].endswith("DEADLINE_MECHANISM_PROSPECTIVE")


def test_resident_migrant_bridge_links_sensitivity_to_interval():
    x = json.loads(RESULT.read_text(encoding="utf-8"))
    b = x["same_guild_resident_migrant_bridge"]
    slopes = b["temperature_slopes_days_per_C"]
    assert abs(slopes["blue_tit"]) > abs(slopes["pied_flycatcher"])
    assert abs(slopes["great_tit"]) > abs(slopes["collared_flycatcher"])
    assert b["interval_model"]["flycatcher_minus_tit_laying_interval_year_effect_days_per_year"] > 0
    assert b["interval_model"]["p"] < 0.01
    assert b["interval_model"]["equivalent_days_per_decade"] == 0.942
