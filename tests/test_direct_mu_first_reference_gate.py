from src.direct_mu_first_reference_gate import (
    FirstReferenceGateInput,
    adjudicate_first_reference_gate,
)


def _base(**overrides):
    data = dict(
        qualified_d_reference_count=0,
        primary_target_id="M5_T0",
        m5_state="STOCK_ACCESS_PENDING",
        w3_state="STOCK_ACCESS_PENDING",
        m1_state="STOCK_ACCESS_PENDING",
        direct_mu_outcome_available=False,
        matched_s_certified=False,
        architecture_mapping_certified=False,
    )
    data.update(overrides)
    return FirstReferenceGateInput(**data)


def test_zero_reference_pauses_candidate_hunting_and_hard_closes_architecture_inference():
    out = adjudicate_first_reference_gate(_base())
    assert out.first_qualified_reference_recovered is False
    assert out.candidate_literature_expansion_paused is True
    assert out.candidate_search_restart_licensed is False
    assert out.minimum_d_reference_precondition_satisfied is False
    assert out.architecture_specific_inference_hard_closed is True
    assert out.next_action == "MATERIALIZE_AND_QUALIFY_M5_T0"
    assert "ZERO_QUALIFIED_MATCHED_D_REFERENCES" in out.blockers


def test_one_qualified_reference_is_necessary_but_not_sufficient_for_architecture_inference():
    out = adjudicate_first_reference_gate(
        _base(
            qualified_d_reference_count=1,
            m5_state="QUALIFIED",
            direct_mu_outcome_available=True,
            matched_s_certified=False,
            architecture_mapping_certified=False,
        )
    )
    assert out.first_qualified_reference_recovered is True
    assert out.minimum_d_reference_precondition_satisfied is True
    assert out.candidate_literature_expansion_paused is False
    assert out.architecture_specific_inference_hard_closed is True
    assert out.next_action == "CONTINUE_REGISTERED_REFERENCE_PANEL_AND_MATCHED_S_ARCHITECTURE_GATES"


def test_architecture_specific_hard_close_lifts_only_when_all_minimum_preconditions_are_true():
    out = adjudicate_first_reference_gate(
        _base(
            qualified_d_reference_count=1,
            m5_state="QUALIFIED",
            direct_mu_outcome_available=True,
            matched_s_certified=True,
            architecture_mapping_certified=True,
        )
    )
    assert out.minimum_d_reference_precondition_satisfied is True
    assert out.architecture_specific_inference_hard_closed is False


def test_search_restarts_only_after_existing_priority_queue_is_terminally_exhausted():
    out = adjudicate_first_reference_gate(
        _base(
            m5_state="FINAL_QUALIFICATION_FAILURE",
            w3_state="TERMINALLY_INACCESSIBLE",
            m1_state="FINAL_QUALIFICATION_FAILURE",
        )
    )
    assert out.first_qualified_reference_recovered is False
    assert out.candidate_literature_expansion_paused is False
    assert out.candidate_search_restart_licensed is True
    assert out.architecture_specific_inference_hard_closed is True
    assert out.next_action == "RESUME_BOUNDED_D_REFERENCE_SEARCH"


def test_terminal_failure_of_m5_moves_to_w3_before_new_literature_search():
    out = adjudicate_first_reference_gate(
        _base(
            m5_state="FINAL_QUALIFICATION_FAILURE",
            w3_state="STOCK_ACCESS_PENDING",
            m1_state="STOCK_ACCESS_PENDING",
        )
    )
    assert out.candidate_literature_expansion_paused is True
    assert out.candidate_search_restart_licensed is False
    assert out.next_action == "MATERIALIZE_AND_QUALIFY_W3_POST_DELETION"
