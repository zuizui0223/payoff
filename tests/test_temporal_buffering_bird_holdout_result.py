from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "payoff_b_temporal_buffering_bird_holdout_result_20260925.json"
DOC = ROOT / "docs" / "PAYOFF_B_TEMPORAL_BUFFERING_BIRD_HOLDOUT_RESULT_20260925.md"


def test_registered_bird_holdout_result_is_frozen_wrong_direction() -> None:
    x = json.loads(RESULT.read_text(encoding="utf-8"))
    assert x["scientific_status"] == "FAIL_WRONG_DIRECTION"
    assert x["retuning_permitted"] is False
    p = x["primary_registered_test"]
    assert p["expected_direction"] == "negative"
    assert abs(p["estimate"] - 0.03506263176814132) < 1e-12
    assert abs(p["p_value"] - 0.2249164339850812) < 1e-12
    assert p["classification"] == "FAIL_WRONG_DIRECTION"
    assert x["holdout"] == {"n_rows": 3268, "n_species": 39, "n_years": 8}


def test_secondary_timing_gain_is_not_promoted_to_primary() -> None:
    x = json.loads(RESULT.read_text(encoding="utf-8"))
    secondary = x["secondary_descriptive_terms"]["z_timing_gain"]
    assert secondary["estimate"] < 0
    assert secondary["p_value"] < 0.01
    assert "not the registered primary test" in secondary["role"]
    assert any(
        "secondary descriptive association" in line
        for line in x["claim_boundary"]
    )


def test_result_document_preserves_failed_test_and_no_retuning() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Result: **FAIL_WRONG_DIRECTION**" in text
    assert "failed" in text.lower()
    assert "cannot be promoted" in text
    assert "retuning_permitted = false" in text
