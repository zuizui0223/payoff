from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "payoff_b_pairwise_tracking_bridge_20260929.json"


def test_pairwise_tracking_bridge_is_source_backed_and_bounded():
    x = json.loads(RESULT.read_text(encoding="utf-8"))
    assert x["status"] == "SOURCE_BACKED_INTERACTION_RESPONSE_BRIDGE_V2_READY"
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


def test_second_interaction_system_is_resident_migrant_competitor_bridge():
    x = json.loads(RESULT.read_text(encoding="utf-8"))
    assert x["independent_interaction_systems"] == 2
    src = x["additional_source"]
    assert src["doi"] == "10.1111/gcb.14160"
    assert src["design"].startswith("10 European nest-box schemes")
    assert src["published_results"]["laying_date_divergence_days_per_decade"] == 0.94
    assert src["published_results"]["pied_flycatcher_difference_from_blue_tit_days_per_C"] > 0
    prohibited = " ".join(src["not_licensed"])
    assert "decision deadlines" in prohibited
    assert "D2-D1" in prohibited
