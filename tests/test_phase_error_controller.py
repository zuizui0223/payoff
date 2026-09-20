import pytest

from src.phase_error_controller import (
    audit_phase_controller,
    phase_state_from_intercept,
)


def test_phase_state_from_intercept():
    assert phase_state_from_intercept(-2.0) == "early"
    assert phase_state_from_intercept(3.0) == "late"
    assert phase_state_from_intercept(0.0) == "matched"


def test_early_positive_slope_is_restoring():
    audit = audit_phase_controller(
        intercept=-13.1,
        phase_state="early",
        slope=0.0008,
        slope_detected=True,
    )
    assert audit.controller_class == "restoring"
    assert audit.restoring
    assert audit.local_squared_error_recovery == pytest.approx(
        0.01048
    )
    assert audit.local_fractional_relaxation == pytest.approx(
        0.0008 / 13.1
    )
    assert audit.linear_zero_crossing_distance == pytest.approx(
        13.1 / 0.0008
    )
    assert audit.linear_half_error_distance == pytest.approx(
        0.5 * 13.1 / 0.0008
    )


def test_late_negative_slope_is_restoring_with_sign_only():
    audit = audit_phase_controller(
        phase_state="late",
        slope=-0.001,
        slope_detected=True,
    )
    assert audit.controller_class == "restoring"
    assert audit.restoring
    assert audit.local_fractional_relaxation is None


def test_late_positive_slope_is_diverging():
    audit = audit_phase_controller(
        intercept=10.0,
        slope=0.2,
        slope_detected=True,
    )
    assert audit.controller_class == "diverging"
    assert not audit.restoring
    assert audit.local_squared_error_recovery == pytest.approx(-2.0)


def test_nondetected_slope_is_not_promoted_to_restoring():
    audit = audit_phase_controller(
        phase_state="late",
        slope=-0.001,
        slope_detected=False,
    )
    assert audit.controller_class == "no_detected_change"
    assert not audit.restoring


def test_intercept_state_conflict_is_rejected():
    with pytest.raises(ValueError):
        audit_phase_controller(
            phase_state="late",
            intercept=-2.0,
            slope=0.1,
            slope_detected=True,
        )
