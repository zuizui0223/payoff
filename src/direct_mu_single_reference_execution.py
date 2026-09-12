"""Quantitative execution receipt for one direct-mu D realization reference.

The existing reference-panel gate defines semantic qualification.  This module
adds a quantitative realization receipt so `realization_band_available=True`
cannot be supplied by declaration alone: the D realization band is derived from
closed 72 h and 120 h calibrated core-equivalent mass bands.

This is a realization-reference gate, not an architecture-mapping gate.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from src.direct_mu_reference_panel_qualification import (
    DReferenceCandidate,
    DReferenceQualification,
    qualify_d_reference,
)


REGISTERED_UNIT = "CALIBRATED_CORE_CHROMOSOME_EQUIVALENTS"
REGISTERED_START_H = 72.0
REGISTERED_END_H = 120.0


@dataclass(frozen=True)
class ClosedBand:
    lower: float
    upper: float

    def validate(self, name: str, *, strictly_positive: bool = False) -> "ClosedBand":
        if not math.isfinite(self.lower) or not math.isfinite(self.upper):
            raise ValueError(f"{name} endpoints must be finite")
        if self.lower > self.upper:
            raise ValueError(f"{name} must satisfy lower <= upper")
        if strictly_positive and self.lower <= 0:
            raise ValueError(f"{name} lower endpoint must be > 0")
        if not strictly_positive and self.lower < 0:
            raise ValueError(f"{name} lower endpoint must be >= 0")
        return self


@dataclass(frozen=True)
class DirectMuReferenceExecutionReceipt:
    reference_id: str
    deletion_class: str
    origin_cluster_id: str
    support_reference: str
    physical_stock_access_confirmed: bool
    marker_pattern_verified: bool
    core_reference_present: bool
    pre_existing_at_72h: bool
    same_medium_and_context: bool
    independently_derived_from_direct_mu_candidate_outcome: bool
    candidate_outcomes_used_for_selection: bool
    viable_at_72h: bool
    measurable_at_120h: bool
    gross_secondary_rearrangement_unresolved: bool
    measurement_unit: str
    interval_start_h: float
    interval_end_h: float
    context_id: str
    intact_comparator_id: str
    d_mass_72h: ClosedBand
    d_mass_120h: ClosedBand


@dataclass(frozen=True)
class DirectMuReferenceExecutionResult:
    reference_id: str
    deletion_class: str
    origin_cluster_id: str
    d_realization_band: ClosedBand | None
    semantic_qualification: DReferenceQualification
    quantitative_receipt_valid: bool
    qualified_reference: bool
    blockers: tuple[str, ...]
    claim_ceiling: str = (
        "one direct-mu D realization reference only; not full D panel, matched S, "
        "architecture mapping, architecture-specific frequency feedback, eta, or E1"
    )


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def ratio_band(numerator: ClosedBand, denominator: ClosedBand) -> ClosedBand:
    """Exact Cartesian projection for a positive ratio numerator/denominator."""
    n = numerator.validate("numerator", strictly_positive=True)
    d = denominator.validate("denominator", strictly_positive=True)
    return ClosedBand(n.lower / d.upper, n.upper / d.lower)


def adjudicate_reference_execution(
    receipt: DirectMuReferenceExecutionReceipt,
) -> DirectMuReferenceExecutionResult:
    reference_id = _text(receipt.reference_id, "reference_id")
    origin_cluster_id = _text(receipt.origin_cluster_id, "origin_cluster_id")
    _text(receipt.support_reference, "support_reference")
    _text(receipt.context_id, "context_id")
    _text(receipt.intact_comparator_id, "intact_comparator_id")

    blockers: list[str] = []
    if not receipt.physical_stock_access_confirmed:
        blockers.append("PHYSICAL_STOCK_ACCESS_NOT_CONFIRMED")
    if receipt.measurement_unit != REGISTERED_UNIT:
        blockers.append("MEASUREMENT_UNIT_NOT_REGISTERED_CORE_CHROMOSOME_EQUIVALENTS")
    if receipt.interval_start_h != REGISTERED_START_H or receipt.interval_end_h != REGISTERED_END_H:
        blockers.append("REALIZATION_INTERVAL_NOT_REGISTERED_72_TO_120_H")

    d_band: ClosedBand | None = None
    try:
        d_band = ratio_band(receipt.d_mass_120h, receipt.d_mass_72h)
    except ValueError:
        blockers.append("VALID_CLOSED_D_REALIZATION_BAND_NOT_DERIVABLE")

    realization_available = d_band is not None and receipt.physical_stock_access_confirmed
    semantic = qualify_d_reference(
        DReferenceCandidate(
            reference_id=reference_id,
            deletion_class=receipt.deletion_class,
            marker_pattern_verified=receipt.marker_pattern_verified,
            core_reference_present=receipt.core_reference_present,
            pre_existing_at_72h=receipt.pre_existing_at_72h,
            same_medium_and_context=receipt.same_medium_and_context,
            independently_derived=receipt.independently_derived_from_direct_mu_candidate_outcome,
            candidate_outcomes_used_for_selection=receipt.candidate_outcomes_used_for_selection,
            viable_at_72h=receipt.viable_at_72h,
            measurable_at_120h=receipt.measurable_at_120h,
            gross_secondary_rearrangement_unresolved=receipt.gross_secondary_rearrangement_unresolved,
            realization_band_available=realization_available,
        )
    )
    blockers.extend(semantic.blockers)

    quantitative_valid = not any(
        b in blockers
        for b in (
            "PHYSICAL_STOCK_ACCESS_NOT_CONFIRMED",
            "MEASUREMENT_UNIT_NOT_REGISTERED_CORE_CHROMOSOME_EQUIVALENTS",
            "REALIZATION_INTERVAL_NOT_REGISTERED_72_TO_120_H",
            "VALID_CLOSED_D_REALIZATION_BAND_NOT_DERIVABLE",
        )
    )
    qualified = bool(quantitative_valid and semantic.qualified)

    return DirectMuReferenceExecutionResult(
        reference_id=reference_id,
        deletion_class=receipt.deletion_class,
        origin_cluster_id=origin_cluster_id,
        d_realization_band=d_band,
        semantic_qualification=semantic,
        quantitative_receipt_valid=quantitative_valid,
        qualified_reference=qualified,
        blockers=tuple(dict.fromkeys(blockers)),
    )
