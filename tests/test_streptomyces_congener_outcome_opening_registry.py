import json
from pathlib import Path

from src.congener_outcome_opening_gate import (
    CongenerOutcomeOpeningReceipt,
    adjudicate_congener_outcome_opening,
)


PATH = Path("validation/streptomyces_congener_sof_outcome_preregistration_v1.json")


def test_current_registry_is_still_machine_blocked_after_window_freeze():
    data = json.loads(PATH.read_text())
    receipt = CongenerOutcomeOpeningReceipt(**data["opening_gate_inputs"])
    allowed, blockers = adjudicate_congener_outcome_opening(receipt)
    assert allowed is data["outcome_opening_allowed"] is False

    # Task, direct-mu semantic scale, candidate set, and primary analysis window are frozen.
    assert "TASK_SCALE_NOT_FROZEN" not in blockers
    assert "DIRECT_MU_SCALE_NOT_FROZEN" not in blockers
    assert "ANALYSIS_WINDOW_NOT_FROZEN" not in blockers
    assert "CANDIDATE_SET_NOT_FROZEN" not in blockers

    # Genotoxicity qualification, materiality thresholds, and uncertainty still block opening.
    assert "GENOTOXICITY_SCALE_NOT_FROZEN" in blockers
    assert "TASK_MATERIALITY_THRESHOLD_NOT_FROZEN" in blockers
    assert "GENOTOXICITY_MATERIALITY_THRESHOLD_NOT_FROZEN" in blockers
    assert "DIRECT_MU_MATERIALITY_THRESHOLD_NOT_FROZEN" in blockers
    assert "UNCERTAINTY_CONSTRUCTION_NOT_FROZEN" in blockers


def test_state_channel_freeze_still_does_not_equal_direct_mu_readiness_or_outcome_permission():
    data = json.loads(PATH.read_text())
    inputs = data["opening_gate_inputs"]
    mu = data["direct_mu_rule"]
    assert data["rule_frozen_before_outcome"]
    assert inputs["task_scale_frozen_preoutcome"]
    assert inputs["direct_mu_scale_frozen_preoutcome"]
    assert inputs["analysis_window_frozen_preoutcome"]
    assert mu["state_channel_frozen_preoutcome"]
    assert not mu["independent_realization_channel_frozen_preoutcome"]
    assert not mu["direct_mu_fully_ready"]
    assert not inputs["genotoxicity_scale_frozen_preoutcome"]
    assert not data["numeric_thresholds_frozen"]
    assert not data["outcome_data_opened"]
    assert not data["outcome_opening_allowed"]
