"""Audit literature-recovered Streptomyces D-reference candidates before qualification.

This layer is intentionally weaker than direct_mu_reference_panel_qualification.
It records whether a published strain/pool is worth carrying forward as a
candidate, but it must never promote a candidate into a qualified realization
reference without the full predeclared qualification gate.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LiteratureCandidate:
    candidate_id: str
    source_family: str
    named_or_traceable: bool
    archived_or_recoverable_material_declared: bool
    genome_or_marker_characterization_declared: bool
    fitness_or_realization_related_measurement_declared: bool
    exact_registered_marker_class_verified: bool
    same_72_120_context_realization_available: bool
    gross_secondary_rearrangement_resolved: bool
    independent_realization_band_available: bool


@dataclass(frozen=True)
class CandidateAudit:
    candidate_id: str
    carry_forward_candidate: bool
    qualified_reference_now: bool
    blockers: tuple[str, ...]


def audit_literature_candidate(candidate: LiteratureCandidate) -> CandidateAudit:
    blockers: list[str] = []
    carry = bool(
        isinstance(candidate.candidate_id, str)
        and candidate.candidate_id.strip()
        and candidate.named_or_traceable
        and candidate.genome_or_marker_characterization_declared
    )
    if not candidate.named_or_traceable:
        blockers.append("REFERENCE_NOT_INDIVIDUALLY_TRACEABLE")
    if not candidate.archived_or_recoverable_material_declared:
        blockers.append("MATERIAL_RECOVERY_NOT_DECLARED")
    if not candidate.genome_or_marker_characterization_declared:
        blockers.append("GENOME_OR_MARKER_CHARACTERIZATION_MISSING")
    if not candidate.fitness_or_realization_related_measurement_declared:
        blockers.append("REALIZATION_RELATED_MEASUREMENT_MISSING")
    if not candidate.exact_registered_marker_class_verified:
        blockers.append("REGISTERED_ENTRY_INTERMEDIATE_DEEP_CLASS_NOT_VERIFIED")
    if not candidate.same_72_120_context_realization_available:
        blockers.append("REGISTERED_72_120_CONTEXT_REALIZATION_NOT_AVAILABLE")
    if not candidate.gross_secondary_rearrangement_resolved:
        blockers.append("GROSS_SECONDARY_REARRANGEMENT_UNRESOLVED")
    if not candidate.independent_realization_band_available:
        blockers.append("INDEPENDENT_REALIZATION_BAND_NOT_AVAILABLE")

    qualified = bool(
        carry
        and candidate.archived_or_recoverable_material_declared
        and candidate.fitness_or_realization_related_measurement_declared
        and candidate.exact_registered_marker_class_verified
        and candidate.same_72_120_context_realization_available
        and candidate.gross_secondary_rearrangement_resolved
        and candidate.independent_realization_band_available
    )
    return CandidateAudit(candidate.candidate_id, carry, qualified, tuple(blockers))
