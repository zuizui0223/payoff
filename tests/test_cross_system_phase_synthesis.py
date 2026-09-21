import pytest

from src.cross_system_phase_synthesis import (
    CrossSystemEvidence,
    synthesize_cross_system_phase,
)
from src.phase_retention_gate import (
    ActuatorPrediction,
    PhaseRetentionPrediction,
    estimate_phase_retention,
    evaluate_actuator_gate,
    evaluate_phase_retention_gate,
)


def phase_gate(lam, low, high):
    pairs = [
        (-4.0, lam * -4.0),
        (-2.0, lam * -2.0),
        (2.0, lam * 2.0),
        (4.0, lam * 4.0),
    ]
    return evaluate_phase_retention_gate(
        estimate_phase_retention(pairs),
        PhaseRetentionPrediction(
            lambda_low=low,
            lambda_high=high,
            min_pairs=4,
        ),
    )


def actuator_gate(system_name, *, passes):
    observed = 0.5 if passes else -0.5
    return evaluate_actuator_gate(
        system_name,
        [
            ActuatorPrediction(
                name="speed",
                expected_direction="increase",
                observed_effect=observed,
                prospective=True,
            )
        ],
    )


def test_lambda_pass_actuator_fail_does_not_reduce_lambda_support():
    synthesis = synthesize_cross_system_phase(
        [
            CrossSystemEvidence(
                system_name="system_A",
                independent_test_id="A_heldout",
                forcing_regime="moderate",
                phase_gate=phase_gate(0.5, 0.45, 0.55),
                actuator_gate=actuator_gate(
                    "system_A",
                    passes=True,
                ),
            ),
            CrossSystemEvidence(
                system_name="wigeon_type",
                independent_test_id="W_heldout",
                forcing_regime="strong",
                phase_gate=phase_gate(0.5, 0.45, 0.55),
                actuator_gate=actuator_gate(
                    "wigeon_type",
                    passes=False,
                ),
            ),
        ]
    )

    assert synthesis.independent_lambda_tests == 2
    assert synthesis.lambda_passed == 2
    assert synthesis.lambda_failed == 0
    assert synthesis.all_lambda_predictions_passed
    assert synthesis.lambda_pass_actuator_fail_systems == (
        "wigeon_type",
    )
    wigeon = synthesis.actuator_by_system[1]
    assert wigeon.failed_predictions == 1
    assert wigeon.all_prospective_passed is False


def test_lambda_fail_actuator_pass_is_kept_as_separate_quadrant():
    synthesis = synthesize_cross_system_phase(
        [
            CrossSystemEvidence(
                system_name="system_B",
                independent_test_id="B_heldout",
                forcing_regime="edge",
                phase_gate=phase_gate(0.8, 0.4, 0.6),
                actuator_gate=actuator_gate(
                    "system_B",
                    passes=True,
                ),
            )
        ]
    )

    assert synthesis.lambda_passed == 0
    assert synthesis.lambda_failed == 1
    assert synthesis.lambda_fail_actuator_pass_systems == (
        "system_B",
    )
    assert synthesis.actuator_by_system[0].all_prospective_passed


def test_duplicate_independent_test_ids_are_rejected():
    rows = [
        CrossSystemEvidence(
            system_name="system_A",
            independent_test_id="same_data",
            forcing_regime="moderate",
            phase_gate=phase_gate(0.5, 0.4, 0.6),
        ),
        CrossSystemEvidence(
            system_name="system_A_relabelled",
            independent_test_id="same_data",
            forcing_regime="moderate",
            phase_gate=phase_gate(0.5, 0.4, 0.6),
        ),
    ]
    with pytest.raises(ValueError, match="unique"):
        synthesize_cross_system_phase(rows)


def test_actuator_gate_system_name_must_match_evidence_system():
    with pytest.raises(ValueError, match="must match"):
        CrossSystemEvidence(
            system_name="system_A",
            independent_test_id="A1",
            forcing_regime="moderate",
            phase_gate=phase_gate(0.5, 0.4, 0.6),
            actuator_gate=actuator_gate(
                "different_system",
                passes=True,
            ),
        )


def test_cross_system_synthesis_has_no_actuator_omnibus_score():
    synthesis = synthesize_cross_system_phase(
        [
            CrossSystemEvidence(
                system_name="A",
                independent_test_id="A1",
                forcing_regime="moderate",
                phase_gate=phase_gate(0.3, 0.2, 0.4),
                actuator_gate=actuator_gate("A", passes=True),
            ),
            CrossSystemEvidence(
                system_name="B",
                independent_test_id="B1",
                forcing_regime="strong",
                phase_gate=phase_gate(0.7, 0.6, 0.8),
                actuator_gate=actuator_gate("B", passes=False),
            ),
        ]
    )

    assert synthesis.lambda_values == pytest.approx((0.3, 0.7))
    assert synthesis.lambda_median == pytest.approx(0.5)
    assert synthesis.forcing_regimes == ("moderate", "strong")
    with pytest.raises(AttributeError, match="no cross-system actuator"):
        _ = synthesis.actuator_omnibus_score


def test_missing_actuator_gate_is_allowed_without_penalizing_lambda():
    synthesis = synthesize_cross_system_phase(
        [
            CrossSystemEvidence(
                system_name="C",
                independent_test_id="C1",
                forcing_regime="novel",
                phase_gate=phase_gate(0.4, 0.3, 0.5),
                actuator_gate=None,
            )
        ]
    )

    assert synthesis.lambda_passed == 1
    assert synthesis.actuator_by_system[0].actuator_gate_present is False
    assert (
        synthesis.actuator_by_system[0].all_prospective_passed
        is None
    )
