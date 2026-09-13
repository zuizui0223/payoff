import json
from pathlib import Path


PATH = Path("validation/streptomyces_direct_mu_first_reference_status_v2.json")


def test_first_reference_count_remains_zero_after_primary_bgi_unresolved_result():
    data = json.loads(PATH.read_text())
    assert data["status"] == "M5_PUBLIC_PRIMARY_MARKER_UNRESOLVED__QUALIFIED_COUNT_ZERO"
    assert data["qualified_d_reference_count"] == 0
    assert data["first_qualified_reference_recovered"] is False
    assert data["minimum_d_reference_precondition_satisfied"] is False
    assert data["architecture_specific_inference_hard_closed"] is True

    m5 = data["primary_target"]
    assert m5["sequence_identity_resolved"] is True
    assert m5["pacbio_four_locus_deep_corroboration"] is True
    assert m5["response_blind_bgi_calibration_qualified"] is True
    assert m5["primary_bgi_target_opened"] is True
    assert m5["primary_bgi_marker_states"]["SCO7036"] == "UNRESOLVED"
    assert m5["primary_bgi_registered_class"] is None
    assert m5["cross_channel_post_hoc_rescue_allowed"] is False
    assert m5["reference_qualified"] is False


def test_next_action_keeps_candidate_search_paused_and_forbids_threshold_refit():
    data = json.loads(PATH.read_text())
    assert data["frozen_priority_queue"] == ["M5_T0", "W3_POST_DELETION", "M1_T0"]
    assert data["candidate_literature_expansion_paused"] is True
    assert data["candidate_search_restart_licensed"] is False
    policy = data["next_action_policy"]
    assert policy["primary_action"] == "CONFIRM_CURRENT_M5_T0_PHYSICAL_STOCK_ACCESS"
    assert policy["if_stock_access_unavailable_or_declined"].startswith("ADVANCE_TO_W3_POST_DELETION")
    assert "REFIT_BGI_THRESHOLDS_TO_M5" in policy["forbidden"]
    assert "CLASSIFY_M5_AS_DEEP_BY_SUBSTITUTING_PACBIO_FOR_THE_FROZEN_PRIMARY_BGI_RULE" in policy["forbidden"]
    assert "OPEN_ARCHITECTURE_SPECIFIC_INFERENCE" in policy["forbidden"]
