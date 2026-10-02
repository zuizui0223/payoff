import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "payoff_b_actionability_peak_empirical_contract_20261002.json"


def load():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_contract_is_prospective_and_does_not_retune_frozen_submission():
    x = load()
    assert x["status"] == "PROSPECTIVE_NO_OUTCOME_OPENED"
    assert x["frozen_geb_submission_affected"] is False


def test_primary_signature_is_intermediate_stage_response_peak():
    x = load()
    sig = x["primary_empirical_signature"]
    assert sig["name"] == "INTERMEDIATE_STAGE_CUE_RESPONSE_PEAK"
    assert "not maximized at the stage of maximal cue accuracy" in sig["prediction"]
    assert len(sig["required_ordering"]) == 3
    assert len(sig["falsifiers"]) >= 3


def test_greater_snow_goose_is_best_same_system_prospective_lane_but_blocked():
    x = load()
    goose = next(
        row for row in x["candidate_systems"]
        if row["system"] == "greater snow goose St Lawrence-Nunavik-Bylot"
    )
    assert goose["current_ceiling"] == "BEST_PROSPECTIVE_SAME_SYSTEM_ROUTE_ACCESS_BLOCKED"
    assert any("authorized Movebank" in row for row in goose["required_new_work"])
    assert any("predictive-connectivity" in row for row in goose["strengths"])


def test_recourse_is_not_identified_by_geometry_or_phase_retention_alone():
    x = load()
    blocked = x["recourse_identification"]["prohibited_direct_substitutions"]
    assert "remaining migration distance == theoretical r" in blocked
    assert "remaining stopover days == theoretical r" in blocked
    assert "flowering duration == theoretical r" in blocked
    assert "1-|lambda| == theoretical r without a prespecified loss/action mapping" in blocked


def test_preferred_direct_r_definition_is_value_ratio_on_common_loss_scale():
    x = load()
    definition = x["recourse_identification"]["preferred_direct_definition"]
    assert "V_restricted" in definition
    assert "V_full" in definition
    assert "common loss scale" in definition


def test_model_comparison_includes_q_only_and_q_by_recourse_focal_model():
    x = load()
    mc = x["model_comparison"]
    assert "cue quality only" in mc["null_models"]
    assert "cue-quality x recourse/actionability model" in mc["focal_model"]
    assert "intermediate response peak" in mc["focal_model"]
    assert "bounded information-use window" in mc["focal_model"]
    assert "held-out prediction" in mc["strongest_test"]


def test_claim_boundary_blocks_existing_natural_validation():
    x = load()
    blocked = x["claim_boundary"]["not_allowed"]
    assert "existing natural data already validate t*" in blocked
    assert "stage number itself is r" in blocked
    assert "generic optimal stopping or value of information is novel" in blocked



def test_contract_includes_bounded_information_use_prediction():
    x = load()
    assert "enter and later exit" in x["theory"]["finite_use_window"]
    sig = x["primary_empirical_signature"]
    assert "entry-peak-exit" in sig["secondary_prediction"]
    assert any(
        "retained recourse approaches zero" in row
        for row in sig["falsifiers"]
    )
