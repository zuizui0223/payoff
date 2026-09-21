import pytest

from src.phase_retention_gate import (
    ActuatorPrediction,
    PhaseRetentionPrediction,
    classify_phase_retention,
    estimate_phase_retention,
    evaluate_actuator_gate,
    evaluate_phase_retention_gate,
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
