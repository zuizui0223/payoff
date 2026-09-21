"""Prospective registration for PAYOFF-B phase-retention and actuator gates.

Predictions are frozen separately from observations so that system-specific
actuator tests cannot be rewritten after seeing outcomes.

The registered objects contain no observed effects.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal

from src.phase_retention_gate import (
    ActuatorDirection,
    PhaseRetentionPrediction,
    RetentionClass,
)


@dataclass(frozen=True)
class PhaseRetentionRegistration:
    system_name: str
    independent_test_id: str
    forcing_regime: str
    phase_coordinate_id: str
    segment_scale_id: str
    lambda_low: float
    lambda_high: float
    min_pairs: int = 3
    require_retention_class: RetentionClass | None = None

    def __post_init__(self) -> None:
        for name in (
            "system_name",
            "independent_test_id",
            "forcing_regime",
            "phase_coordinate_id",
            "segment_scale_id",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")

        # Reuse the gate-level validation.
        PhaseRetentionPrediction(
            lambda_low=self.lambda_low,
            lambda_high=self.lambda_high,
            min_pairs=self.min_pairs,
            require_retention_class=self.require_retention_class,
        )

    def prediction(self) -> PhaseRetentionPrediction:
        return PhaseRetentionPrediction(
            lambda_low=self.lambda_low,
            lambda_high=self.lambda_high,
            min_pairs=self.min_pairs,
            require_retention_class=self.require_retention_class,
        )


@dataclass(frozen=True)
class ActuatorPredictionSpec:
    name: str
    expected_direction: ActuatorDirection
    zero_tolerance: float = 0.0

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("actuator name must be non-empty")
        if not isfinite(self.zero_tolerance) or self.zero_tolerance < 0.0:
            raise ValueError(
                "zero_tolerance must be non-negative and finite"
            )


@dataclass(frozen=True)
class ActuatorRegistration:
    system_name: str
    independent_test_id: str
    forcing_regime: str
    predictions: tuple[ActuatorPredictionSpec, ...]

    def __post_init__(self) -> None:
        for name in (
            "system_name",
            "independent_test_id",
            "forcing_regime",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")
        if not self.predictions:
            raise ValueError(
                "at least one prospective actuator prediction is required"
            )
        names = [row.name for row in self.predictions]
        if len(names) != len(set(names)):
            raise ValueError(
                "actuator prediction names must be unique within a system"
            )


@dataclass(frozen=True)
class ActuatorObservation:
    name: str
    observed_effect: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("actuator observation name must be non-empty")
        if not isfinite(self.observed_effect):
            raise ValueError("observed_effect must be finite")


@dataclass(frozen=True)
class ActuatorObservationSet:
    system_name: str
    independent_test_id: str
    observations: tuple[ActuatorObservation, ...]

    def __post_init__(self) -> None:
        if not self.system_name.strip():
            raise ValueError("system_name must be non-empty")
        if not self.independent_test_id.strip():
            raise ValueError("independent_test_id must be non-empty")
        if not self.observations:
            raise ValueError(
                "at least one actuator observation is required"
            )
        names = [row.name for row in self.observations]
        if len(names) != len(set(names)):
            raise ValueError(
                "actuator observation names must be unique within a system"
            )
