"""Reliability gate for cross-system PAYOFF-B phase-retention claims.

The empirical programme has two distinct claim levels:

1. estimator-scale coordinate:
   different systems can be represented by a phase-retention slope lambda_hat;

2. latent biological magnitude comparison:
   differences in lambda across systems are interpreted after observation-error
   calibration.

The second claim requires substantially stronger evidence. A source-backed
sensitivity analysis is useful, but assumption-conditional replicate
disagreement does not become a gold-standard error distribution merely because
the simulation is complete.

This module keeps those licenses separate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class LambdaReliabilitySystem:
    system_id: str
    taxon: str
    observed_lambda: float
    calibration_status: str
    confirmatory_recovery_ready: bool

    @property
    def calibration_class(self) -> str:
        if not self.confirmatory_recovery_ready:
            return "PENDING"
        token = self.calibration_status.upper()
        if "ASSUMPTION_CONDITIONAL" in token:
            return "SENSITIVITY_ASSUMPTION_CONDITIONAL"
        if (
            "GOLD_STANDARD" in token
            or "SOURCE_SPECIFIC_IDENTIFIED" in token
        ):
            return "SOURCE_SPECIFIC_ERROR_IDENTIFIED"
        return "READY_UNCLASSIFIED"


@dataclass(frozen=True)
class CrossSystemLambdaReliabilityGate:
    estimator_scale_coordinate_licensed: bool
    unique_taxa: int
    direct_system_rows: int
    taxa_with_any_reliability_calibration: int
    taxa_with_source_specific_error_identification: int
    taxa_pending_reliability_calibration: int
    latent_magnitude_comparison_licensed: bool
    blockers: tuple[str, ...]
    system_classes: tuple[tuple[str, str, str], ...]


def systems_from_registry(payload: dict[str, Any]) -> tuple[LambdaReliabilitySystem, ...]:
    rows = payload.get("systems")
    if not isinstance(rows, list) or not rows:
        raise ValueError("lambda recovery registry has no systems")

    systems: list[LambdaReliabilitySystem] = []
    seen_ids: set[str] = set()
    for row in rows:
        system_id = str(row.get("system_id", "")).strip()
        taxon = str(row.get("taxon", "")).strip()
        if not system_id or not taxon:
            raise ValueError("registry systems require system_id and taxon")
        if system_id in seen_ids:
            raise ValueError(f"duplicate system_id: {system_id}")
        seen_ids.add(system_id)

        if row.get("observed_lambda") is None:
            raise ValueError(
                f"registry system {system_id} has no observed_lambda"
            )

        systems.append(
            LambdaReliabilitySystem(
                system_id=system_id,
                taxon=taxon,
                observed_lambda=float(row["observed_lambda"]),
                calibration_status=str(
                    row.get(
                        "error_calibration_status",
                        "PENDING_SOURCE_BACKED_CALIBRATION",
                    )
                ),
                confirmatory_recovery_ready=bool(
                    row.get("confirmatory_recovery_ready", False)
                ),
            )
        )
    return tuple(systems)


def evaluate_cross_system_lambda_reliability(
    systems: Iterable[LambdaReliabilitySystem],
    *,
    minimum_taxa_for_coordinate: int = 3,
) -> CrossSystemLambdaReliabilityGate:
    rows = tuple(systems)
    if not rows:
        raise ValueError("at least one direct system is required")
    if minimum_taxa_for_coordinate <= 0:
        raise ValueError("minimum_taxa_for_coordinate must be positive")

    taxa = sorted({row.taxon for row in rows})
    estimator_scale_coordinate_licensed = (
        len(taxa) >= minimum_taxa_for_coordinate
    )

    by_taxon: dict[str, list[LambdaReliabilitySystem]] = {}
    for row in rows:
        by_taxon.setdefault(row.taxon, []).append(row)

    any_calibrated_taxa = 0
    identified_taxa = 0
    pending_taxa = 0

    for taxon_rows in by_taxon.values():
        classes = {row.calibration_class for row in taxon_rows}
        if classes == {"SOURCE_SPECIFIC_ERROR_IDENTIFIED"}:
            identified_taxa += 1
            any_calibrated_taxa += 1
        elif "SOURCE_SPECIFIC_ERROR_IDENTIFIED" in classes:
            # Mixed calibrated/uncalibrated route rows cannot support a
            # taxon-wide magnitude comparison.
            any_calibrated_taxa += 1
            pending_taxa += 1
        elif any(
            cls in {
                "SENSITIVITY_ASSUMPTION_CONDITIONAL",
                "READY_UNCLASSIFIED",
            }
            for cls in classes
        ):
            any_calibrated_taxa += 1
            pending_taxa += 1
        else:
            pending_taxa += 1

    latent_magnitude_comparison_licensed = (
        estimator_scale_coordinate_licensed
        and identified_taxa == len(taxa)
    )

    blockers: list[str] = []
    if not estimator_scale_coordinate_licensed:
        blockers.append("INSUFFICIENT_TAXON_REPLICATION_FOR_COORDINATE")
    if identified_taxa < len(taxa):
        blockers.append(
            "SOURCE_SPECIFIC_MEASUREMENT_ERROR_NOT_IDENTIFIED_FOR_ALL_TAXA"
        )
    if any(
        row.calibration_class == "SENSITIVITY_ASSUMPTION_CONDITIONAL"
        for row in rows
    ):
        blockers.append(
            "ASSUMPTION_CONDITIONAL_SENSITIVITY_IS_NOT_CORRECTED_TRUTH"
        )
    if any(
        row.calibration_class == "PENDING"
        for row in rows
    ):
        blockers.append("DIRECT_SYSTEMS_PENDING_RELIABILITY_CALIBRATION")

    system_classes = tuple(
        sorted(
            (
                row.system_id,
                row.taxon,
                row.calibration_class,
            )
            for row in rows
        )
    )

    return CrossSystemLambdaReliabilityGate(
        estimator_scale_coordinate_licensed=(
            estimator_scale_coordinate_licensed
        ),
        unique_taxa=len(taxa),
        direct_system_rows=len(rows),
        taxa_with_any_reliability_calibration=any_calibrated_taxa,
        taxa_with_source_specific_error_identification=identified_taxa,
        taxa_pending_reliability_calibration=pending_taxa,
        latent_magnitude_comparison_licensed=(
            latent_magnitude_comparison_licensed
        ),
        blockers=tuple(dict.fromkeys(blockers)),
        system_classes=system_classes,
    )
