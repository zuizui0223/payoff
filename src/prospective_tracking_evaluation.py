"""Evaluate prospectively registered PAYOFF-B tracking predictions.

Registration and observation objects are intentionally separate. Evaluation
requires exact identity matching and complete actuator-name matching.

This module returns ordinary phase-retention and actuator gates, but only after
the prospective contract has been satisfied.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.phase_retention_gate import (
    ActuatorGate,
    ActuatorPrediction,
    PhaseRetentionGate,
    estimate_phase_retention,
    reported_phase_retention_estimate,
    evaluate_actuator_gate,
    evaluate_phase_retention_gate,
)
from src.prospective_tracking_registry import (
    ActuatorObservationSet,
    ActuatorRegistration,
    PhaseRetentionRegistration,
)


@dataclass(frozen=True)
class PhaseObservationSet:
    system_name: str
    independent_test_id: str
    phase_coordinate_id: str
    segment_scale_id: str
    pairs: tuple[tuple[float, float], ...]

    def __post_init__(self) -> None:
        for name in (
            "system_name",
            "independent_test_id",
            "phase_coordinate_id",
            "segment_scale_id",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")
        if len(self.pairs) < 3:
            raise ValueError(
                "at least three observed phase pairs are required"
            )


@dataclass(frozen=True)
class ReportedPhaseObservation:
    system_name: str
    independent_test_id: str
    phase_coordinate_id: str
    segment_scale_id: str
    pairs: int
    lambda_retention: float
    lambda_se: float | None = None
    p_vs_no_correction: float | None = None

    def __post_init__(self) -> None:
        for name in (
            "system_name",
            "independent_test_id",
            "phase_coordinate_id",
            "segment_scale_id",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")
        # Full numerical validation is centralized in the estimate builder.
        reported_phase_retention_estimate(
            pairs=self.pairs,
            lambda_retention=self.lambda_retention,
            lambda_se=self.lambda_se,
            p_vs_no_correction=self.p_vs_no_correction,
        )


@dataclass(frozen=True)
class ProspectivePhaseEvaluation:
    system_name: str
    independent_test_id: str
    forcing_regime: str
    phase_coordinate_id: str
    segment_scale_id: str
    gate: PhaseRetentionGate
    prospective_contract_satisfied: bool = True


@dataclass(frozen=True)
class ProspectiveActuatorEvaluation:
    system_name: str
    independent_test_id: str
    forcing_regime: str
    gate: ActuatorGate
    prospective_contract_satisfied: bool = True


def _check_phase_identity(
    registration: PhaseRetentionRegistration,
    *,
    system_name: str,
    independent_test_id: str,
    phase_coordinate_id: str,
    segment_scale_id: str,
) -> None:
    if registration.system_name != system_name:
        raise ValueError(
            "phase observation system_name does not match registration"
        )
    if registration.independent_test_id != independent_test_id:
        raise ValueError(
            "phase observation independent_test_id does not match registration"
        )
    if registration.phase_coordinate_id != phase_coordinate_id:
        raise ValueError(
            "phase observation coordinate does not match registered coordinate"
        )
    if registration.segment_scale_id != segment_scale_id:
        raise ValueError(
            "phase observation segment scale does not match registration"
        )


def evaluate_registered_reported_phase(
    registration: PhaseRetentionRegistration,
    observations: ReportedPhaseObservation,
) -> ProspectivePhaseEvaluation:
    """Evaluate a preregistered lambda prediction from a frozen summary estimate."""

    _check_phase_identity(
        registration,
        system_name=observations.system_name,
        independent_test_id=observations.independent_test_id,
        phase_coordinate_id=observations.phase_coordinate_id,
        segment_scale_id=observations.segment_scale_id,
    )
    estimate = reported_phase_retention_estimate(
        pairs=observations.pairs,
        lambda_retention=observations.lambda_retention,
        lambda_se=observations.lambda_se,
        p_vs_no_correction=observations.p_vs_no_correction,
    )
    gate = evaluate_phase_retention_gate(
        estimate,
        registration.prediction(),
    )
    return ProspectivePhaseEvaluation(
        system_name=registration.system_name,
        independent_test_id=registration.independent_test_id,
        forcing_regime=registration.forcing_regime,
        phase_coordinate_id=registration.phase_coordinate_id,
        segment_scale_id=registration.segment_scale_id,
        gate=gate,
    )


def evaluate_registered_phase(
    registration: PhaseRetentionRegistration,
    observations: PhaseObservationSet,
) -> ProspectivePhaseEvaluation:
    """Evaluate a frozen lambda prediction against later observations."""

    _check_phase_identity(
        registration,
        system_name=observations.system_name,
        independent_test_id=observations.independent_test_id,
        phase_coordinate_id=observations.phase_coordinate_id,
        segment_scale_id=observations.segment_scale_id,
    )

    estimate = estimate_phase_retention(observations.pairs)
    gate = evaluate_phase_retention_gate(
        estimate,
        registration.prediction(),
    )
    return ProspectivePhaseEvaluation(
        system_name=registration.system_name,
        independent_test_id=registration.independent_test_id,
        forcing_regime=registration.forcing_regime,
        phase_coordinate_id=registration.phase_coordinate_id,
        segment_scale_id=registration.segment_scale_id,
        gate=gate,
    )


def evaluate_registered_actuators(
    registration: ActuatorRegistration,
    observations: ActuatorObservationSet,
) -> ProspectiveActuatorEvaluation:
    """Evaluate only actuator names that were frozen prospectively.

    Missing or extra observations are rejected instead of being silently
    ignored. This prevents post-outcome relabeling or selective reporting.
    """

    if registration.system_name != observations.system_name:
        raise ValueError(
            "actuator observation system_name does not match registration"
        )
    if registration.independent_test_id != observations.independent_test_id:
        raise ValueError(
            "actuator observation independent_test_id does not match registration"
        )

    registered = {
        row.name: row
        for row in registration.predictions
    }
    observed = {
        row.name: row
        for row in observations.observations
    }
    registered_names = set(registered)
    observed_names = set(observed)
    if observed_names != registered_names:
        missing = sorted(registered_names - observed_names)
        extra = sorted(observed_names - registered_names)
        details: list[str] = []
        if missing:
            details.append("missing=" + ",".join(missing))
        if extra:
            details.append("extra=" + ",".join(extra))
        raise ValueError(
            "actuator observations must exactly match registered names"
            + (": " + "; ".join(details) if details else "")
        )

    predictions = tuple(
        ActuatorPrediction(
            name=spec.name,
            expected_direction=spec.expected_direction,
            observed_effect=observed[spec.name].observed_effect,
            zero_tolerance=spec.zero_tolerance,
            prospective=True,
        )
        for spec in registration.predictions
    )
    gate = evaluate_actuator_gate(
        registration.system_name,
        predictions,
    )
    return ProspectiveActuatorEvaluation(
        system_name=registration.system_name,
        independent_test_id=registration.independent_test_id,
        forcing_regime=registration.forcing_regime,
        gate=gate,
    )
