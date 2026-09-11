import json
from pathlib import Path

from src.direct_mu_realization_design import DirectMuRealizationDesignReceipt


PATH = Path("validation/streptomyces_direct_mu_realization_design_v1.json")


def test_registry_recomputes_frozen_design_but_not_ready_realization_channel():
    data = json.loads(PATH.read_text())
    rule = data["reference_panel_rule"]
    status = data["status"]
    receipt = DirectMuRealizationDesignReceipt(
        start_hour=data["interval_hours"][0],
        end_hour=data["interval_hours"][1],
        realization_unit=data["realization_unit"],
        pre_existing_D_verified_by_marker_panel=rule["pre_existing_D_verified_by_registered_marker_panel"],
        same_medium_and_context_as_state_channel=rule["same_medium_and_context_as_state_channel"],
        final_mixed_state_fraction_reused_to_estimate_d=rule["final_mixed_state_fraction_reused_to_estimate_d"],
        candidate_outcomes_used_to_select_reference_panel=rule["candidate_outcomes_used_to_select_reference_panel"],
        entry_class_predeclared=any(x["class_id"] == "ENTRY_CLASS" for x in rule["classes"]),
        intermediate_class_predeclared=any(x["class_id"] == "INTERMEDIATE_CLASS" for x in rule["classes"]),
        deep_class_predeclared=any(x["class_id"] == "DEEP_CLASS" for x in rule["classes"]),
        minimum_independent_references_per_class=rule["minimum_independent_references_per_class"],
        core_equivalent_fold_change_declared=True,
        reference_panel_materialized=status["reference_panel_materialized"],
        reference_panel_qualified=status["reference_panel_qualified"],
    )
    assert data["absolute_state_mass_unit"] == "CALIBRATED_CORE_CHROMOSOME_EQUIVALENTS"
    assert data["realization_unit"] == "CORE_CHROMOSOME_EQUIVALENT_FOLD_CHANGE"
    assert receipt.design_frozen_preoutcome is status["design_frozen_preoutcome"] is True
    assert receipt.realization_channel_ready is status["absolute_mass_route_ready"] is False


def test_registered_reference_classes_match_marker_severity_ladder():
    classes = json.loads(PATH.read_text())["reference_panel_rule"]["classes"]
    patterns = {row["class_id"]: row["marker_pattern"] for row in classes}
    assert patterns["ENTRY_CLASS"] == "SCO7662_absent__SCO7350_present__SCO7036_argG_present"
    assert patterns["INTERMEDIATE_CLASS"] == "SCO7662_absent__SCO7350_absent__SCO7036_argG_present"
    assert patterns["DEEP_CLASS"] == "SCO7662_absent__SCO7350_absent__SCO7036_argG_absent"


def test_realization_reference_selection_is_outcome_blind_and_independent():
    rule = json.loads(PATH.read_text())["reference_panel_rule"]
    assert not rule["final_mixed_state_fraction_reused_to_estimate_d"]
    assert not rule["candidate_outcomes_used_to_select_reference_panel"]
    assert rule["minimum_independent_references_per_class"] >= 2


def test_claim_ceiling_remains_unpromoted():
    ceiling = json.loads(PATH.read_text())["claim_ceiling"]
    assert not ceiling["direct_mu_outcome_available"]
    assert not ceiling["matched_generalist_shared_architecture_recovered"]
    assert not ceiling["matched_s_certified"]
    assert not ceiling["architecture_mapping_certified"]
    assert not ceiling["generic_game_promoted"]
    assert not ceiling["eta_promoted"]
    assert not ceiling["e1_promoted"]
