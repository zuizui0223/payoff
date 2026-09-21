import pytest

from src.prospective_tracking_evaluation import (
    PhaseObservationSet,
    evaluate_registered_actuators,
    evaluate_registered_phase,
)
from src.prospective_tracking_registry import (
    ActuatorObservation,
    ActuatorObservationSet,
    ActuatorPredictionSpec,
    ActuatorRegistration,
    PhaseRetentionRegistration,
)


def phase_registration():
    return PhaseRetentionRegistration(
        system_name="system_A",
        independent_test_id="A_holdout",
        forcing_regime="moderate",
        phase_coordinate_id="signed_resource_phase_error",
        segment_scale_id="standardized_tracking_segment_v1",
        lambda_low=0.45,
        lambda_high=0.55,
        min_pairs=4,
        require_retention_class="restoring",
    )


def phase_observations():
    return PhaseObservationSet(
        system_name="system_A",
        independent_test_id="A_holdout",
        phase_coordinate_id="signed_resource_phase_error",
        segment_scale_id="standardized_tracking_segment_v1",
        pairs=(
            (-4.0, -2.0),
            (-2.0, -1.0),
            (2.0, 1.0),
            (4.0, 2.0),
        ),
    )


def actuator_registration():
    return ActuatorRegistration(
        system_name="system_A",
        independent_test_id="A_holdout",
        forcing_regime="moderate",
        predictions=(
            ActuatorPredictionSpec(
                name="speed",
                expected_direction="increase",
            ),
            ActuatorPredictionSpec(
                name="stopover",
                expected_direction="decrease",
            ),
            ActuatorPredictionSpec(
                name="route_reset",
                expected_direction="increase",
            ),
        ),
    )


def test_registered_phase_evaluation_passes_matching_contract():
    evaluation = evaluate_registered_phase(
        phase_registration(),
        phase_observations(),
    )

    assert evaluation.prospective_contract_satisfied
    assert evaluation.gate.passed
    assert evaluation.gate.estimate.lambda_retention == pytest.approx(0.5)


def test_registered_phase_rejects_coordinate_mismatch():
    observations = PhaseObservationSet(
        system_name="system_A",
        independent_test_id="A_holdout",
        phase_coordinate_id="arrival_date_residual",
        segment_scale_id="standardized_tracking_segment_v1",
        pairs=phase_observations().pairs,
    )
    with pytest.raises(ValueError, match="coordinate"):
        evaluate_registered_phase(
            phase_registration(),
            observations,
        )


def test_registered_phase_rejects_scale_mismatch():
    observations = PhaseObservationSet(
        system_name="system_A",
        independent_test_id="A_holdout",
        phase_coordinate_id="signed_resource_phase_error",
        segment_scale_id="whole_route",
        pairs=phase_observations().pairs,
    )
    with pytest.raises(ValueError, match="segment scale"):
        evaluate_registered_phase(
            phase_registration(),
            observations,
        )


def test_registered_phase_rejects_independent_test_id_mismatch():
    observations = PhaseObservationSet(
        system_name="system_A",
        independent_test_id="different_holdout",
        phase_coordinate_id="signed_resource_phase_error",
        segment_scale_id="standardized_tracking_segment_v1",
        pairs=phase_observations().pairs,
    )
    with pytest.raises(ValueError, match="independent_test_id"):
        evaluate_registered_phase(
            phase_registration(),
            observations,
        )


def test_registered_actuator_evaluation_uses_frozen_directions():
    observations = ActuatorObservationSet(
        system_name="system_A",
        independent_test_id="A_holdout",
        observations=(
            ActuatorObservation(
                name="speed",
                observed_effect=-0.2,
            ),
            ActuatorObservation(
                name="stopover",
                observed_effect=0.1,
            ),
            ActuatorObservation(
                name="route_reset",
                observed_effect=-0.3,
            ),
        ),
    )
    evaluation = evaluate_registered_actuators(
        actuator_registration(),
        observations,
    )

    assert evaluation.prospective_contract_satisfied
    assert evaluation.gate.failed_predictions == 3
    assert not evaluation.gate.all_prospective_passed


def test_registered_actuator_evaluation_rejects_missing_prediction():
    observations = ActuatorObservationSet(
        system_name="system_A",
        independent_test_id="A_holdout",
        observations=(
            ActuatorObservation(
                name="speed",
                observed_effect=0.2,
            ),
            ActuatorObservation(
                name="stopover",
                observed_effect=-0.2,
            ),
        ),
    )
    with pytest.raises(ValueError, match="missing=route_reset"):
        evaluate_registered_actuators(
            actuator_registration(),
            observations,
        )


def test_registered_actuator_evaluation_rejects_posthoc_extra_actuator():
    observations = ActuatorObservationSet(
        system_name="system_A",
        independent_test_id="A_holdout",
        observations=(
            ActuatorObservation(
                name="speed",
                observed_effect=0.2,
            ),
            ActuatorObservation(
                name="stopover",
                observed_effect=-0.2,
            ),
            ActuatorObservation(
                name="route_reset",
                observed_effect=0.3,
            ),
            ActuatorObservation(
                name="new_posthoc_actuator",
                observed_effect=1.0,
            ),
        ),
    )
    with pytest.raises(ValueError, match="extra=new_posthoc_actuator"):
        evaluate_registered_actuators(
            actuator_registration(),
            observations,
        )


def test_registered_actuator_evaluation_rejects_system_mismatch():
    observations = ActuatorObservationSet(
        system_name="different_system",
        independent_test_id="A_holdout",
        observations=(
            ActuatorObservation(
                name="speed",
                observed_effect=0.2,
            ),
            ActuatorObservation(
                name="stopover",
                observed_effect=-0.2,
            ),
            ActuatorObservation(
                name="route_reset",
                observed_effect=0.3,
            ),
        ),
    )
    with pytest.raises(ValueError, match="system_name"):
        evaluate_registered_actuators(
            actuator_registration(),
            observations,
        )
