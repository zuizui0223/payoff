import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "payoff_b_snow_goose_prediction_compensation_classification_contract_20261002.json"


def load():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_classification_is_frozen_preoutcome():
    payload = load()
    assert payload["status"] == "PREOUTCOME_CLASSIFICATION_FROZEN"
    assert payload["outcome_data_opened"] is False


def test_parent_directions_are_not_rewritten():
    payload = load()
    parents = payload["parent_tests"]
    assert parents["cue_uptake"]["registered_direction"] == "positive"
    assert parents["downstream_compensation"]["registered_direction"] == (
        "negative on log transit duration"
    )


def test_both_supported_has_joint_stage_but_not_theorem_ceiling():
    payload = load()
    row = next(
        x for x in payload["classification_matrix"]
        if x["cue_uptake"] == "SUPPORTED"
        and x["compensation"] == "DUAL_USE_BEHAVIORAL_SIGNAL_SUPPORTED"
    )
    assert row["classification"] == (
        "BOTH_PRECOMMITMENT_AND_DOWNSTREAM_INFORMATION_CHANNELS_SUPPORTED"
    )
    assert "does not identify reduced-form r" in row["ceiling"]


def test_compensation_null_keeps_exogeneity_unresolved():
    payload = load()
    row = next(
        x for x in payload["classification_matrix"]
        if x["cue_uptake"] == "SUPPORTED"
        and x["compensation"] == "DUAL_USE_NOT_DEMONSTRATED_EXOGENEITY_UNRESOLVED"
    )
    assert "UNRESOLVED" in row["classification"]
    assert row["ceiling"] == "do not call compensation absent"


def test_substitution_cannot_be_inferred_from_transit_sign_alone():
    payload = load()
    boundary = payload["substitution_theory_boundary"]
    assert boundary["direct_test_from_existing_two_parent_tests"] is False
    assert "pre-correction mismatch risk R(q)" in boundary["reason"]
    assert any(
        "opposite-sign compensation coefficient" in x
        for x in payload["forbidden"]
    )
