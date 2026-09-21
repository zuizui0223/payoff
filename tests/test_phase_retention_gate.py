import pytest

from src.closed_loop_tracking import simulate_closed_loop_tracking
from src.phase_retention_gate import (
    ActuatorPrediction,
    PhaseRetentionPrediction,
    classify_phase_retention,
    estimate_phase_retention,
    evaluate_actuator_gate,
    evaluate_phase_retention_gate,
    reported_phase_retention_estimate,
    total_feedback_from_lambda,
)


def test_phase_retention_recovers_lambda_and_residual_forcing():
    pairs = [
        (-4.0, 1.0 + 0.4 * -4.0),
        (-2.0, 1.0 + 0.4 * -2.0),
        (0.0, 1.0),
        (2.0, 1.0 + 0.4 * 2.0),
        (4.0, 1.0 + 0.4 * 4.0),
    ]
    estimate = estimate_phase_retention(pairs)

    assert estimate.lambda_retention == pytest.approx(0.4)
    assert estimate.residual_forcing == pytest.approx(1.0)
    assert estimate.rmse == pytest.approx(0.0)
    assert estimate.r_squared == pytest.approx(1.0)
    assert estimate.retention_class == "restoring"


def test_phase_retention_gate_uses_only_lambda_coordinate():
    estimate = estimate_phase_retention(
        [
            (-3.0, -1.2),
            (-1.0, -0.4),
            (1.0, 0.4),
            (3.0, 1.2),
        ]
    )
    gate = evaluate_phase_retention_gate(
        estimate,
        PhaseRetentionPrediction(
            lambda_low=0.35,
            lambda_high=0.45,
            min_pairs=4,
            require_retention_class="restoring",
        ),
    )

    assert gate.passed
    assert gate.interval_passed
    assert gate.class_passed
    assert gate.reasons == ()


def test_wigeon_type_pattern_lambda_can_pass_while_actuator_gate_fails():
    # Synthetic structural witness for the interpretation:
    # common phase-retention prediction succeeds, while system-specific
    # speed/stopover/route-reset predictions do not.
    estimate = estimate_phase_retention(
        [
            (-4.0, -2.0),
            (-2.0, -1.0),
            (2.0, 1.0),
            (4.0, 2.0),
        ]
    )
    retention = evaluate_phase_retention_gate(
        estimate,
        PhaseRetentionPrediction(
            lambda_low=0.45,
            lambda_high=0.55,
            min_pairs=4,
            require_retention_class="restoring",
        ),
    )
    actuator = evaluate_actuator_gate(
        "wigeon_type_synthetic_witness",
        [
            ActuatorPrediction(
                name="speed",
                expected_direction="increase",
                observed_effect=-0.2,
                prospective=True,
            ),
            ActuatorPrediction(
                name="stopover",
                expected_direction="decrease",
                observed_effect=0.1,
                prospective=True,
            ),
            ActuatorPrediction(
                name="route_reset",
                expected_direction="increase",
                observed_effect=-0.3,
                prospective=True,
            ),
        ],
    )

    assert retention.passed
    assert not actuator.all_prospective_passed
    assert actuator.failed_predictions == 3


def test_actuator_gate_can_mix_pass_and_fail_without_changing_lambda():
    gate = evaluate_actuator_gate(
        "system_A",
        [
            ActuatorPrediction(
                name="speed",
                expected_direction="increase",
                observed_effect=0.4,
            ),
            ActuatorPrediction(
                name="stopover",
                expected_direction="decrease",
                observed_effect=0.2,
            ),
            ActuatorPrediction(
                name="route_reset",
                expected_direction="no_change",
                observed_effect=0.01,
                zero_tolerance=0.05,
            ),
        ],
    )

    assert gate.passed_predictions == 2
    assert gate.failed_predictions == 1
    assert not gate.all_prospective_passed


@pytest.mark.parametrize(
    ("lam", "expected"),
    [
        (-0.2, "sign_reversing"),
        (0.0, "restoring"),
        (0.7, "restoring"),
        (1.0, "neutral_retention"),
        (1.2, "amplifying"),
    ],
)
def test_phase_retention_classes(lam, expected):
    assert classify_phase_retention(lam) == expected


def test_lambda_maps_to_total_feedback_without_actuator_decomposition():
    assert total_feedback_from_lambda(0.4) == pytest.approx(0.6)
    assert total_feedback_from_lambda(1.0) == pytest.approx(0.0)
    assert total_feedback_from_lambda(-0.2) == pytest.approx(1.2)


def test_closed_loop_multiplier_is_exact_phase_retention_lambda():
    result = simulate_closed_loop_tracking(
        residual_forcing=0.1,
        movement_feedback_gain=0.2,
        phenology_feedback_gain=0.3,
        steps=20,
        burn_in=5,
    )
    assert result.phase_retention_lambda == pytest.approx(0.5)
    assert total_feedback_from_lambda(
        result.phase_retention_lambda
    ) == pytest.approx(0.5)


def test_one_sided_lambda_prediction_allows_preregistered_lambda_less_than_one():
    estimate = reported_phase_retention_estimate(
        pairs=224,
        lambda_retention=0.85994,
        lambda_se=0.04509,
        p_vs_no_correction=0.00190,
    )
    gate = evaluate_phase_retention_gate(
        estimate,
        PhaseRetentionPrediction(
            lambda_low=None,
            lambda_high=1.0,
            min_pairs=30,
            require_retention_class="restoring",
        ),
    )

    assert gate.passed
    assert gate.interval_passed
    assert gate.class_passed
    assert gate.estimate.source_kind == "reported_summary"
    assert gate.estimate.residual_forcing is None
    assert gate.estimate.rmse is None
    assert gate.estimate.r_squared is None


def test_reported_summary_preserves_wigeon_uncertainty_fields():
    estimate = reported_phase_retention_estimate(
        pairs=224,
        lambda_retention=0.85994,
        lambda_se=0.04509,
        p_vs_no_correction=0.00190,
    )
    assert estimate.lambda_se == pytest.approx(0.04509)
    assert estimate.p_vs_no_correction == pytest.approx(0.00190)


def test_phase_prediction_requires_at_least_one_bound_or_class():
    with pytest.raises(ValueError):
        PhaseRetentionPrediction(
            lambda_low=None,
            lambda_high=None,
            min_pairs=3,
            require_retention_class=None,
        )


def test_actuator_matching_direction_can_fail_inferential_support():
    gate = evaluate_actuator_gate(
        "wigeon_style_stopover",
        [
            ActuatorPrediction(
                name="stopover",
                expected_direction="decrease",
                observed_effect=-0.000140,
                observed_p_value=0.972,
                max_p_value=0.05,
            )
        ],
    )
    result = gate.predictions[0]
    assert result.direction_passed
    assert not result.support_passed
    assert not result.passed
    assert gate.failed_predictions == 1


def test_actuator_requires_direction_and_registered_support_threshold():
    gate = evaluate_actuator_gate(
        "supported_speed",
        [
            ActuatorPrediction(
                name="speed",
                expected_direction="increase",
                observed_effect=0.20,
                observed_p_value=0.01,
                max_p_value=0.05,
            )
        ],
    )
    result = gate.predictions[0]
    assert result.direction_passed
    assert result.support_passed
    assert result.passed
    assert gate.all_prospective_passed


def test_actuator_direction_only_mode_remains_backward_compatible():
    gate = evaluate_actuator_gate(
        "direction_only",
        [
            ActuatorPrediction(
                name="speed",
                expected_direction="increase",
                observed_effect=0.20,
            )
        ],
    )
    result = gate.predictions[0]
    assert result.direction_passed
    assert result.support_passed
    assert result.passed
