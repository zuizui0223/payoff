import json
from pathlib import Path

from src.response_blind_assay_qualification import CanonicalTaskScaleReceipt


PATH = Path("validation/streptomyces_congener_assay_scale_status_v1.json")
OUTCOME = Path("validation/streptomyces_congener_sof_outcome_preregistration_v1.json")


def test_task_scale_recomputes_as_qualified_and_is_canonical_function_readout():
    data = json.loads(PATH.read_text())
    row = data["task_scale"]
    receipt = CanonicalTaskScaleReceipt(
        scale_id=row["scale_id"],
        support_reference=row["support_reference"],
        focal_task=row["focal_task"],
        higher_is_better_declared=row["higher_is_better_declared"],
        direct_external_function_readout_declared=row["direct_external_function_readout_declared"],
        assay_protocol_preoutcome_frozen=row["assay_protocol_preoutcome_frozen"],
        candidate_outcomes_used_to_select_scale=row["candidate_outcomes_used_to_select_scale"],
        fitness_guardrail_kept_separate=row["fitness_guardrail_kept_separate"],
    )
    assert receipt.task_scale_qualified
    assert row["scale_id"] == "B_SUBTILIS_SOFT_AGAR_INHIBITION_ZONE_AREA_MM2"
    assert row["protocol_basis"]["indicator"] == "Bacillus_subtilis"


def test_spore_output_is_guardrail_not_silently_scalarized_into_task():
    data = json.loads(PATH.read_text())
    guard = data["fitness_guardrail"]
    assert guard["scale_id"] == "COLONY_SPORE_OUTPUT_CFU"
    assert guard["role"] == "guardrail_not_task_scalar"


def test_genotoxicity_scale_remains_unqualified_and_response_blind():
    data = json.loads(PATH.read_text())
    gen = data["genotoxicity_scale"]
    assert gen["primary_scale_id"] is None
    assert not gen["scale_frozen_preoutcome"]
    assert gen["qualification_mode"] == "response_blind_controls_before_congener_outcomes"
    assert gen["candidate_outcomes_must_remain_blinded_during_qualification"]
    assert not gen["qualified"]


def test_direct_mu_semantic_scale_is_frozen_but_assay_details_are_not():
    data = json.loads(PATH.read_text())
    mu = data["direct_mu_scale"]
    assert mu["semantic_scale_frozen_preoutcome"]
    assert not mu["exact_marker_panel_and_sampling_window_frozen"]
    assert not mu["qualified_for_outcome_opening"]


def test_scale_registry_and_outcome_opening_registry_are_synchronized():
    scale = json.loads(PATH.read_text())["current_summary"]
    out = json.loads(OUTCOME.read_text())["opening_gate_inputs"]
    assert out["task_scale_frozen_preoutcome"] == scale["task_scale_frozen_preoutcome"]
    assert out["direct_mu_scale_frozen_preoutcome"] == scale["direct_mu_semantic_scale_frozen_preoutcome"]
    assert out["genotoxicity_scale_frozen_preoutcome"] == scale["genotoxicity_scale_frozen_preoutcome"]
    assert not scale["all_three_scales_ready_for_primary_outcome"]
    assert not scale["outcome_opening_allowed"]
