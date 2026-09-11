from src.congener_outcome_opening_gate import (
    CongenerOutcomeOpeningReceipt,
    adjudicate_congener_outcome_opening,
)


def make(**overrides):
    data = dict(
        task_scale_frozen_preoutcome=True,
        genotoxicity_scale_frozen_preoutcome=True,
        direct_mu_scale_frozen_preoutcome=True,
        task_materiality_threshold_frozen_preoutcome=True,
        genotoxicity_materiality_threshold_frozen_preoutcome=True,
        direct_mu_materiality_threshold_frozen_preoutcome=True,
        uncertainty_construction_frozen_preoutcome=True,
        analysis_window_frozen_preoutcome=True,
        candidate_set_frozen_preoutcome=True,
        outcome_data_already_opened=False,
    )
    data.update(overrides)
    return CongenerOutcomeOpeningReceipt(**data)


def test_full_preoutcome_freeze_allows_opening():
    allowed, blockers = adjudicate_congener_outcome_opening(make())
    assert allowed
    assert blockers == ()


def test_missing_any_threshold_blocks_opening():
    for field in (
        "task_materiality_threshold_frozen_preoutcome",
        "genotoxicity_materiality_threshold_frozen_preoutcome",
        "direct_mu_materiality_threshold_frozen_preoutcome",
    ):
        allowed, blockers = adjudicate_congener_outcome_opening(make(**{field: False}))
        assert not allowed
        assert blockers


def test_missing_measurement_semantics_blocks_opening():
    allowed, blockers = adjudicate_congener_outcome_opening(
        make(task_scale_frozen_preoutcome=False)
    )
    assert not allowed
    assert "TASK_SCALE_NOT_FROZEN" in blockers


def test_opening_before_full_freeze_is_flagged_not_retroactively_repaired():
    allowed, blockers = adjudicate_congener_outcome_opening(
        make(outcome_data_already_opened=True)
    )
    assert not allowed
    assert "OUTCOME_ALREADY_OPENED_BEFORE_FULL_FREEZE" in blockers


def test_current_programme_state_is_not_openable_without_numeric_thresholds():
    current = make(
        task_materiality_threshold_frozen_preoutcome=False,
        genotoxicity_materiality_threshold_frozen_preoutcome=False,
        direct_mu_materiality_threshold_frozen_preoutcome=False,
    )
    allowed, blockers = adjudicate_congener_outcome_opening(current)
    assert not allowed
    assert len(blockers) == 3
