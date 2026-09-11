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
    assert (
        gen["primary_assay_class_required"]
        == "DIRECT_DNA_LESION_OR_BREAK_READOUT_IN_STREPTOMYCES_COELICOLOR"
    )
    assert "SOS_OR_recA_LexA_RESPONSE" in gen["secondary_only_assay_classes"]
    assert "ROS_AMOUNT" in gen["secondary_only_assay_classes"]
    assert gen["candidate_outcomes_must_remain_blinded_during_qualification"]
    assert not gen["qualified"]


def test_direct_mu_state_and_realization_designs_are_frozen_but_panel_is_not_ready():
    data = json.loads(PATH.read_text())
    mu = data["direct_mu_scale"]
    assert mu["semantic_scale_frozen_preoutcome"]
    assert mu["exact_marker_panel_and_sampling_window_frozen"]
    assert mu["state_channel_frozen_preoutcome"]
    assert mu["primary_interval_hours"] == [72, 120]
    assert mu["registered_entry_marker"].startswith("SCO7662")
    assert mu["registered_severity_markers"] == ["SCO7350_loss", "SCO7036_argG_loss"]
    assert mu["preferred_identification_route"] == "ABSOLUTE_STATE_MASS_PLUS_INDEPENDENT_D_REALIZATION"
    assert mu["realization_design_frozen_preoutcome"]
    assert not mu["reference_panel_materialized"]
    assert not mu["reference_panel_qualified"]
    assert not mu["d_band_available"]
    assert not mu["direct_mu_realization_channel_ready"]
    assert mu["legacy_fraction_only_r_route_retained"]
    assert not mu["direct_mu_fully_ready"]
    assert not mu["qualified_for_outcome_opening"]


def test_scale_registry_and_outcome_opening_registry_are_synchronized():
    scale_data = json.loads(PATH.read_text())
    scale = scale_data["current_summary"]
    out_data = json.loads(OUTCOME.read_text())
    out = out_data["opening_gate_inputs"]
    mu = out_data["direct_mu_rule"]
    assert out["task_scale_frozen_preoutcome"] == scale["task_scale_frozen_preoutcome"]
    assert out["direct_mu_scale_frozen_preoutcome"] == scale["direct_mu_semantic_scale_frozen_preoutcome"]
    assert out["genotoxicity_scale_frozen_preoutcome"] == scale["genotoxicity_scale_frozen_preoutcome"]
    assert out["analysis_window_frozen_preoutcome"]
    assert mu["state_channel_frozen_preoutcome"]
    assert mu["realization_design_frozen_preoutcome"]
    assert not mu["independent_realization_channel_frozen_preoutcome"]
    assert not mu["reference_panel_materialized"]
    assert not mu["d_band_available"]
    assert not mu["direct_mu_fully_ready"]
    assert not scale["all_three_scales_ready_for_primary_outcome"]
    assert not scale["outcome_opening_allowed"]
