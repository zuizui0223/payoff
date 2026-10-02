import pytest

from src.actionability_calibration import calibrate_reduced_actionability


def test_exact_mixture_calibrates_scalar_actionability():
    result = calibrate_reduced_actionability(
        [0.6, 0.7, 0.8, 0.9],
        [0.1, 0.2, 0.3, 0.4],
        [0.04, 0.08, 0.12, 0.16],
    )
    assert result.status == "PASS_SEPARABLE_REDUCED_ACTIONABILITY"
    assert result.retained_actionability == pytest.approx(0.4)
    assert result.max_abs_ratio_deviation == pytest.approx(0.0)


def test_q_dependent_ratio_fails_scalar_recourse_model():
    result = calibrate_reduced_actionability(
        [0.6, 0.7, 0.8, 0.9],
        [0.1, 0.2, 0.3, 0.4],
        [0.02, 0.08, 0.18, 0.32],
        constancy_tolerance=0.05,
    )
    assert result.status == "FAIL_Q_DEPENDENT_ACTIONABILITY"
    assert result.retained_actionability is None
    assert result.ratio_min == pytest.approx(0.2)
    assert result.ratio_max == pytest.approx(0.8)


def test_stage_signal_value_exceeding_reference_fails_fraction_interpretation():
    result = calibrate_reduced_actionability(
        [0.6, 0.7, 0.8],
        [0.1, 0.2, 0.3],
        [0.15, 0.30, 0.45],
    )
    assert result.status == "FAIL_RATIO_OUTSIDE_UNIT_INTERVAL"
    assert result.retained_actionability is None
    assert result.ratio_min == pytest.approx(1.5)
    assert result.ratio_max == pytest.approx(1.5)


def test_zero_reference_information_points_are_excluded_not_divided():
    result = calibrate_reduced_actionability(
        [0.5, 0.6, 0.7],
        [0.0, 0.1, 0.2],
        [0.0, 0.05, 0.10],
    )
    assert result.status == "PASS_SEPARABLE_REDUCED_ACTIONABILITY"
    assert result.usable_cue_qualities == pytest.approx((0.6, 0.7))
    assert result.retained_actionability == pytest.approx(0.5)


def test_insufficient_positive_reference_information_fails_closed():
    result = calibrate_reduced_actionability(
        [0.5, 0.6],
        [0.0, 0.1],
        [0.0, 0.05],
        minimum_usable_points=2,
    )
    assert result.status == "NOT_IDENTIFIABLE_INSUFFICIENT_POSITIVE_REFERENCE_VOI"
    assert result.retained_actionability is None


def test_physical_route_fraction_cannot_enter_without_voi_values():
    with pytest.raises(ValueError):
        calibrate_reduced_actionability(
            [0.6, 0.7, 0.8],
            [0.1, 0.2],
            [0.5, 0.4, 0.3],
        )
