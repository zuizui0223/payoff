import json
from pathlib import Path


STATUS = Path("validation/streptomyces_direct_mu_first_reference_status_v1.json")
POOL = Path("validation/streptomyces_direct_mu_literature_candidate_pool_v1.json")
M5 = Path("validation/streptomyces_m5_first_reference_execution_v1.json")


def test_zero_reference_status_hard_closes_architecture_specific_inference():
    data = json.loads(STATUS.read_text())
    assert data["qualified_d_reference_count"] == 0
    assert data["first_qualified_reference_recovered"] is False
    assert data["candidate_literature_expansion_paused"] is True
    assert data["candidate_search_restart_licensed"] is False
    assert data["minimum_d_reference_precondition_satisfied"] is False
    assert data["architecture_specific_inference_hard_closed"] is True
    assert data["primary_target_id"] == "M5_T0"
    assert data["primary_execution_receipt"] == "STREPTOMYCES_M5_FIRST_REFERENCE_EXECUTION_V1"
    assert data["next_action"] == "CONFIRM_M5_STOCK_ACCESS_AND_RESOLVE_EXACT_M5_T0_SEQUENCE_ACCESSION_IN_PARALLEL"


def test_preferred_absolute_mass_route_requires_independent_d_not_g_or_r_from_reference():
    data = json.loads(STATUS.read_text())
    route = data["preferred_direct_mu_route"]
    assert route["route"] == "ABSOLUTE_STATE_MASS"
    assert route["independent_reference_quantity"] == "d"
    assert route["independent_g_required_from_d_reference"] is False
    assert route["independent_r_required_from_d_reference"] is False


def test_first_reference_milestone_does_not_relax_full_panel_requirement():
    data = json.loads(STATUS.read_text())
    panel = data["full_panel_requirement_unchanged"]
    assert panel["minimum_independent_qualified_references_per_class"] == 2
    assert set(panel["registered_classes"]) == {"ENTRY_CLASS", "INTERMEDIATE_CLASS", "DEEP_CLASS"}
    assert panel["first_reference_milestone_does_not_relax_panel"] is True


def test_candidate_pool_is_focused_on_first_reference_not_expansion():
    pool = json.loads(POOL.read_text())
    focus = pool["execution_focus"]
    assert pool["adjudication"]["qualified_reference_count"] == 0
    assert focus["active_milestone"] == "FIRST_QUALIFIED_MATCHED_D_REFERENCE"
    assert focus["primary_target_id"] == "M5_T0"
    assert focus["candidate_literature_expansion_paused"] is True
    assert focus["architecture_specific_inference_hard_closed_while_zero_qualified_references"] is True


def test_m5_current_receipt_is_prospective_and_unqualified():
    m5 = json.loads(M5.read_text())
    assert m5["reference_id"] == "M5_T0"
    assert m5["status"] == "PROSPECTIVE_PRELAB_EVIDENCE_RECOVERED_NOT_EXECUTED"
    assert m5["physical_stock_access_confirmed"] is False
    assert m5["derived_d_realization_band"] is None
    assert m5["qualified_reference"] is False
    assert m5["claim_ceiling"]["architecture_mapping_certified"] is False
