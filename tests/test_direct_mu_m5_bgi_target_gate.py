from src.direct_mu_m5_bgi_target_gate import (
    CORE_PANEL,
    FrozenCalibration,
    adjudicate_m5_target_opening,
)


def make_cal(**overrides):
    values = dict(
        receipt_id="STREPTOMYCES_M5_BGI_MARKER_CALIBRATION_RESULT_V1",
        calibration_qualified=True,
        target_candidate_id="M5_T0",
        target_bgi_ratios_opened_for_calibration=False,
        absence_max_ratio=0.05,
        presence_min_ratio=0.90,
        core_panel=CORE_PANEL,
        absent_pair_count=4,
        present_pair_count=8,
        absent_candidate_count=2,
        present_candidate_count=4,
    )
    values.update(overrides)
    return FrozenCalibration(**values)


def test_target_opens_only_after_qualified_frozen_calibration():
    result = adjudicate_m5_target_opening(make_cal())
    assert result.target_opening_allowed
    assert result.target_bgi_run == "SRR16954696"
    assert result.absence_max_ratio == 0.05
    assert result.presence_min_ratio == 0.90
    assert result.blockers == ()


def test_failed_calibration_keeps_target_closed():
    result = adjudicate_m5_target_opening(make_cal(calibration_qualified=False))
    assert not result.target_opening_allowed
    assert "RESPONSE_BLIND_CALIBRATION_NOT_QUALIFIED" in result.blockers
    assert result.absence_max_ratio is None


def test_target_leakage_keeps_target_closed_even_if_numbers_separate():
    result = adjudicate_m5_target_opening(
        make_cal(target_bgi_ratios_opened_for_calibration=True)
    )
    assert not result.target_opening_allowed
    assert "TARGET_WAS_OPENED_DURING_CALIBRATION" in result.blockers


def test_threshold_or_core_panel_refit_is_not_allowed():
    bad_panel = tuple(x for x in CORE_PANEL if x != "SCO5400")
    result = adjudicate_m5_target_opening(make_cal(core_panel=bad_panel))
    assert not result.target_opening_allowed
    assert "CORE_NORMALIZATION_PANEL_MISMATCH" in result.blockers

    result = adjudicate_m5_target_opening(
        make_cal(absence_max_ratio=0.9, presence_min_ratio=0.8)
    )
    assert not result.target_opening_allowed
    assert "FROZEN_CALIBRATION_THRESHOLDS_NOT_SEPARATED" in result.blockers


def test_redundancy_floors_must_survive_into_target_receipt():
    result = adjudicate_m5_target_opening(
        make_cal(absent_candidate_count=1, present_pair_count=2)
    )
    assert not result.target_opening_allowed
    assert "CALIBRATION_PAIR_REDUNDANCY_FLOOR_NOT_MET" in result.blockers
    assert "CALIBRATION_CANDIDATE_REDUNDANCY_FLOOR_NOT_MET" in result.blockers
