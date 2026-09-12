import pytest

from src.direct_mu_bgi_response_blind_calibration import (
    CalibrationPair,
    calibrate_bgi_marker_thresholds,
)


def pair(candidate, marker, pacbio, ratio, core=100.0):
    return CalibrationPair(candidate, marker, pacbio, core, ratio)


def test_separated_independent_controls_freeze_conservative_extrema():
    rows = [
        pair("WT_ancestor", "SCO7662", 100, 0.96),
        pair("WT_ancestor", "SCO7350", 100, 1.01),
        pair("WT_ancestor", "SCO7036", 100, 0.99),
        pair("M1_T0", "SCO7662", 0, 0.02),
        pair("M1_T0", "SCO7350", 0, 0.03),
        pair("M2_T0", "SCO7662", 0, 0.04),
        pair("M2_T0", "SCO3879", 100, 1.03),
    ]
    result = calibrate_bgi_marker_thresholds(rows)
    assert result.calibration_qualified
    assert result.absence_max_ratio == pytest.approx(0.04)
    assert result.presence_min_ratio == pytest.approx(0.96)
    assert result.absent_candidate_count == 2
    assert result.present_candidate_count == 2
    assert result.blockers == ()


def test_m5_target_data_are_rejected_even_if_values_are_clean():
    rows = [pair("M5_T0", "SCO7662", 0, 0.0)]
    with pytest.raises(ValueError, match="forbidden"):
        calibrate_bgi_marker_thresholds(rows)


def test_pacbio_gray_state_is_excluded_not_forced():
    rows = [
        pair("WT_ancestor", "SCO7662", 100, 0.95),
        pair("WT_ancestor", "SCO7350", 100, 0.98),
        pair("M1_T0", "SCO7662", 0, 0.02),
        pair("M1_T0", "SCO7350", 50, 0.45),
        pair("M2_T0", "SCO7662", 0, 0.03),
        pair("M2_T0", "SCO7036", 0, 0.04),
        pair("M2_T0", "SCO3879", 100, 1.0),
    ]
    result = calibrate_bgi_marker_thresholds(rows)
    assert result.unresolved_pair_count == 1
    assert result.calibration_qualified


def test_unresolved_or_absent_pacbio_core_blocks_control_label():
    rows = [
        pair("WT_ancestor", "SCO7662", 100, 0.95, core=99.0),
        pair("M1_T0", "SCO7662", 0, 0.01),
        pair("M2_T0", "SCO7662", 0, 0.02),
        pair("M3_T0", "SCO7662", 0, 0.03),
        pair("M1_T0", "SCO3879", 100, 1.0),
        pair("M2_T0", "SCO3879", 100, 1.0),
        pair("M3_T0", "SCO3879", 100, 1.0),
    ]
    result = calibrate_bgi_marker_thresholds(rows)
    assert result.unresolved_pair_count == 1
    assert result.calibration_qualified


def test_overlap_fails_closed():
    rows = [
        pair("M1_T0", "SCO7662", 0, 0.40),
        pair("M2_T0", "SCO7662", 0, 0.45),
        pair("M3_T0", "SCO7662", 0, 0.50),
        pair("WT_ancestor", "SCO7662", 100, 0.48),
        pair("WT_ancestor", "SCO7350", 100, 0.52),
        pair("M1_T0", "SCO3879", 100, 0.55),
    ]
    result = calibrate_bgi_marker_thresholds(rows)
    assert not result.calibration_qualified
    assert "ABSENT_PRESENT_BGI_CALIBRATION_SETS_TOUCH_OR_OVERLAP" in result.blockers


def test_calibration_requires_multiple_pairs_and_candidates_per_state():
    rows = [
        pair("M1_T0", "SCO7662", 0, 0.01),
        pair("M1_T0", "SCO7350", 0, 0.02),
        pair("M1_T0", "SCO7036", 0, 0.03),
        pair("WT_ancestor", "SCO7662", 100, 0.99),
        pair("WT_ancestor", "SCO7350", 100, 1.00),
        pair("WT_ancestor", "SCO7036", 100, 1.01),
    ]
    result = calibrate_bgi_marker_thresholds(rows)
    assert not result.calibration_qualified
    assert "ABSENT_CONTROL_CANDIDATE_COUNT_BELOW_FLOOR" in result.blockers
    assert "PRESENT_CONTROL_CANDIDATE_COUNT_BELOW_FLOOR" in result.blockers
