"""Cross-system synthesis for PAYOFF-B phase retention.

The synthesis layer treats lambda tests as the cross-system evidence unit.
Actuator results remain attached to individual systems and are never pooled
into the lambda summary or converted into an omnibus score.

Each phase test requires a unique independent_test_id to make pseudo-
replication explicit.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from typing import Iterable, Literal

from src.phase_retention_gate import (
    ActuatorGate,
    PhaseRetentionGate,
    RetentionClass,
)


EvidenceTier = Literal["prospective", "retrospective"]


@dataclass(frozen=True)
class CrossSystemEvidence:
    system_name: str
    independent_test_id: str
    forcing_regime: str
    phase_coordinate_id: str
    segment_scale_id: str
    phase_gate: PhaseRetentionGate
    evidence_tier: EvidenceTier = "prospective"
    actuator_gate: ActuatorGate | None = None

    def __post_init__(self) -> None:
        if not self.system_name.strip():
            raise ValueError("system_name must be non-empty")
        if not self.independent_test_id.strip():
            raise ValueError("independent_test_id must be non-empty")
        if not self.forcing_regime.strip():
            raise ValueError("forcing_regime must be non-empty")
        if not self.phase_coordinate_id.strip():
            raise ValueError("phase_coordinate_id must be non-empty")
        if not self.segment_scale_id.strip():
            raise ValueError("segment_scale_id must be non-empty")
        if self.evidence_tier not in ("prospective", "retrospective"):
            raise ValueError(
                "evidence_tier must be 'prospective' or 'retrospective'"
            )
        if (
            self.actuator_gate is not None
            and self.actuator_gate.system_name != self.system_name
        ):
            raise ValueError(
                "actuator_gate.system_name must match system_name"
            )


@dataclass(frozen=True)
class SystemActuatorSummary:
    system_name: str
    independent_test_id: str
    actuator_gate_present: bool
    prospective_predictions: int
    passed_predictions: int
    failed_predictions: int
    all_prospective_passed: bool | None


@dataclass(frozen=True)
class CrossSystemPhaseSynthesis:
    systems: int
    independent_lambda_tests: int
    prospective_lambda_tests: int
    retrospective_lambda_tests: int
    phase_coordinate_id: str
    segment_scale_id: str
    lambda_passed: int
    lambda_failed: int
    prospective_lambda_passed: int
    prospective_lambda_failed: int
    lambda_values: tuple[float, ...]
    lambda_min: float
    lambda_median: float
    lambda_max: float
    retention_class_counts: tuple[tuple[RetentionClass, int], ...]
    lambda_pass_actuator_fail_systems: tuple[str, ...]
    lambda_fail_actuator_pass_systems: tuple[str, ...]
    actuator_by_system: tuple[SystemActuatorSummary, ...]
    forcing_regimes: tuple[str, ...]

    @property
    def all_lambda_predictions_passed(self) -> bool:
        return self.lambda_failed == 0

    @property
    def all_prospective_lambda_predictions_passed(self) -> bool:
        return (
            self.prospective_lambda_tests > 0
            and self.prospective_lambda_failed == 0
        )

    @property
    def actuator_omnibus_score(self):
        raise AttributeError(
            "PAYOFF-B intentionally defines no cross-system actuator "
            "omnibus score; inspect actuator_by_system instead"
        )


def synthesize_cross_system_phase(
    evidence: Iterable[CrossSystemEvidence],
) -> CrossSystemPhaseSynthesis:
    """Synthesize independent lambda tests without pooling actuator outcomes."""

    rows = tuple(evidence)
    if not rows:
        raise ValueError("at least one cross-system evidence row is required")

    ids = [row.independent_test_id for row in rows]
    if len(set(ids)) != len(ids):
        raise ValueError(
            "independent_test_id values must be unique; duplicate phase tests "
            "cannot be counted as independent cross-system evidence"
        )

    coordinate_ids = {row.phase_coordinate_id for row in rows}
    if len(coordinate_ids) != 1:
        raise ValueError(
            "cross-system lambda synthesis requires one predeclared common "
            "phase_coordinate_id"
        )
    scale_ids = {row.segment_scale_id for row in rows}
    if len(scale_ids) != 1:
        raise ValueError(
            "cross-system lambda synthesis requires one predeclared common "
            "segment_scale_id"
        )
    phase_coordinate_id = next(iter(coordinate_ids))
    segment_scale_id = next(iter(scale_ids))

    lambda_values = tuple(
        row.phase_gate.estimate.lambda_retention
        for row in rows
    )
    lambda_passed = sum(row.phase_gate.passed for row in rows)
    lambda_failed = len(rows) - lambda_passed

    prospective_rows = tuple(
        row for row in rows
        if row.evidence_tier == "prospective"
    )
    retrospective_rows = tuple(
        row for row in rows
        if row.evidence_tier == "retrospective"
    )
    prospective_lambda_passed = sum(
        row.phase_gate.passed for row in prospective_rows
    )
    prospective_lambda_failed = (
        len(prospective_rows) - prospective_lambda_passed
    )

    class_order: tuple[RetentionClass, ...] = (
        "sign_reversing",
        "restoring",
        "neutral_retention",
        "amplifying",
    )
    class_counts = tuple(
        (
            retention_class,
            sum(
                row.phase_gate.estimate.retention_class
                == retention_class
                for row in rows
            ),
        )
        for retention_class in class_order
    )

    actuator_rows: list[SystemActuatorSummary] = []
    lambda_pass_actuator_fail: list[str] = []
    lambda_fail_actuator_pass: list[str] = []

    for row in rows:
        actuator = row.actuator_gate
        if actuator is None:
            actuator_rows.append(
                SystemActuatorSummary(
                    system_name=row.system_name,
                    independent_test_id=row.independent_test_id,
                    actuator_gate_present=False,
                    prospective_predictions=0,
                    passed_predictions=0,
                    failed_predictions=0,
                    all_prospective_passed=None,
                )
            )
            continue

        actuator_rows.append(
            SystemActuatorSummary(
                system_name=row.system_name,
                independent_test_id=row.independent_test_id,
                actuator_gate_present=True,
                prospective_predictions=(
                    actuator.prospective_predictions
                ),
                passed_predictions=actuator.passed_predictions,
                failed_predictions=actuator.failed_predictions,
                all_prospective_passed=(
                    actuator.all_prospective_passed
                ),
            )
        )
        if (
            row.phase_gate.passed
            and not actuator.all_prospective_passed
        ):
            lambda_pass_actuator_fail.append(row.system_name)
        if (
            not row.phase_gate.passed
            and actuator.all_prospective_passed
        ):
            lambda_fail_actuator_pass.append(row.system_name)

    return CrossSystemPhaseSynthesis(
        systems=len(rows),
        independent_lambda_tests=len(rows),
        prospective_lambda_tests=len(prospective_rows),
        retrospective_lambda_tests=len(retrospective_rows),
        phase_coordinate_id=phase_coordinate_id,
        segment_scale_id=segment_scale_id,
        lambda_passed=lambda_passed,
        lambda_failed=lambda_failed,
        prospective_lambda_passed=prospective_lambda_passed,
        prospective_lambda_failed=prospective_lambda_failed,
        lambda_values=lambda_values,
        lambda_min=min(lambda_values),
        lambda_median=median(lambda_values),
        lambda_max=max(lambda_values),
        retention_class_counts=class_counts,
        lambda_pass_actuator_fail_systems=tuple(
            lambda_pass_actuator_fail
        ),
        lambda_fail_actuator_pass_systems=tuple(
            lambda_fail_actuator_pass
        ),
        actuator_by_system=tuple(actuator_rows),
        forcing_regimes=tuple(
            dict.fromkeys(row.forcing_regime for row in rows)
        ),
    )
