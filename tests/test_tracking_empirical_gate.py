import pytest

from src.tracking_empirical_gate import (
    TrackingValidationThresholds,
    evaluate_tracking_validation_gate,
)
from src.tracking_empirical_validation import (
    HeldOutMovementValidation,
    HeldOutPhaseValidation,
    HeldOutTrackingValidation,
)


def movement(rmse=0.0, intervals=20):
    return HeldOutMovementValidation(
        intervals=intervals,
        observed_mean_longitudinal=0.0,
        observed_mean_transverse=0.0,
        observed_second_longitudinal=0.5,
        observed_second_transverse=0.5,
        predicted_mean_longitudinal=0.0,
        predicted_mean_transverse=0.0,
        predicted_second_longitudinal=0.5,
        predicted_second_transverse=0.5,
        error_mean_longitudinal=0.0,
        error_mean_transverse=0.0,
        error_second_longitudinal=0.0,
        error_second_transverse=0.0,
        dimensionless_moment_rmse=rmse,
    )


def phase(
    *,
    licensed=True,
    intervals=20,
    error=0.0,
):
    return HeldOutPhaseValidation(
        intervals_with_phase=intervals,
        compatible_intervals=intervals if licensed else 0,
        incompatible_intervals=0 if licensed else intervals,
        observed_mean_log_compression=(
            0.5 if licensed else None
        ),
        observed_median_log_compression=(
            0.5 if licensed else None
        ),
        predicted_log_compression=0.5,
        mean_log_compression_error=(
            error if licensed else None
        ),
        validation_licensed=licensed,
        license_reason=(
            "licensed" if licensed else "not licensed"
        ),
    )


def test_validation_gate_passes_predeclared_movement_and_phase_criteria():
    validation = HeldOutTrackingValidation(
        movement=movement(rmse=0.03, intervals=30),
        phase=phase(licensed=True, intervals=20, error=0.02),
    )
    thresholds = TrackingValidationThresholds(
        max_movement_moment_rmse=0.05,
        min_held_out_intervals=20,
        require_phase_validation=True,
        max_abs_phase_log_error=0.05,
        min_phase_intervals=10,
    )
    gate = evaluate_tracking_validation_gate(
        validation,
        thresholds,
    )

    assert gate.passed
    assert gate.movement_passed
    assert gate.phase_passed
    assert gate.reasons == ()


def test_validation_gate_fails_when_movement_rmse_exceeds_threshold():
    validation = HeldOutTrackingValidation(
        movement=movement(rmse=0.08, intervals=30),
        phase=phase(licensed=True, intervals=20, error=0.01),
    )
    gate = evaluate_tracking_validation_gate(
        validation,
        TrackingValidationThresholds(
            max_movement_moment_rmse=0.05,
            min_held_out_intervals=20,
        ),
    )

    assert not gate.passed
    assert not gate.movement_passed
    assert any("RMSE" in reason for reason in gate.reasons)


def test_validation_gate_fails_when_required_phase_validation_is_unlicensed():
    validation = HeldOutTrackingValidation(
        movement=movement(rmse=0.01, intervals=30),
        phase=phase(licensed=False, intervals=20),
    )
    gate = evaluate_tracking_validation_gate(
        validation,
        TrackingValidationThresholds(
            max_movement_moment_rmse=0.05,
            min_held_out_intervals=20,
            require_phase_validation=True,
            max_abs_phase_log_error=0.05,
            min_phase_intervals=10,
        ),
    )

    assert not gate.passed
    assert gate.movement_passed
    assert not gate.phase_passed
    assert any(
        "timing-axis validation is not licensed" in reason
        for reason in gate.reasons
    )


def test_phase_error_threshold_is_absolute():
    validation = HeldOutTrackingValidation(
        movement=movement(rmse=0.01, intervals=30),
        phase=phase(licensed=True, intervals=20, error=-0.06),
    )
    gate = evaluate_tracking_validation_gate(
        validation,
        TrackingValidationThresholds(
            max_movement_moment_rmse=0.05,
            require_phase_validation=True,
            max_abs_phase_log_error=0.05,
        ),
    )
    assert not gate.passed
    assert gate.abs_phase_log_error == pytest.approx(0.06)


def test_thresholds_require_phase_error_bound_when_phase_is_required():
    with pytest.raises(ValueError):
        TrackingValidationThresholds(
            max_movement_moment_rmse=0.05,
            require_phase_validation=True,
        )
