import json
from pathlib import Path


STATUS = Path("validation/streptomyces_direct_mu_first_reference_status_v1.json")
POOL = Path("validation/streptomyces_direct_mu_literature_candidate_pool_v1.json")


def test_zero_reference_status_hard_closes_architecture_specific_inference():
    data = json.loads(STATUS.read_text())
    assert data["qualified_d_reference_count"] == 0
    assert data["first_qualified_reference_recovered"] is False
    assert data["candidate_literature_expansion_paused"] is True
    assert data["candidate_search_restart_licensed"] is False
    assert data["minimum_d_reference_precondition_satisfied"] is False
    assert data["architecture_specific_inference_hard_closed"] is True
    assert data["primary_target_id"] == "M5_T0"
    assert data["next_action"] == "MATERIALIZE_AND_QUALIFY_M5_T0"


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
