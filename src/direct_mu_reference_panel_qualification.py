"""Pre-outcome qualification gate for Streptomyces direct-mu D references.

This module does not materialize reference strains or measure realization.
It freezes which independently characterized pre-existing D references would
be admissible before any prodiginine-congener outcome is opened.
"""
from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_CLASSES = frozenset({"ENTRY_CLASS", "INTERMEDIATE_CLASS", "DEEP_CLASS"})


@dataclass(frozen=True)
class DReferenceCandidate:
    reference_id: str
    deletion_class: str
    marker_pattern_verified: bool
    core_reference_present: bool
    pre_existing_at_72h: bool
    same_medium_and_context: bool
    independently_derived: bool
    candidate_outcomes_used_for_selection: bool
    viable_at_72h: bool
    measurable_at_120h: bool
    gross_secondary_rearrangement_unresolved: bool
    realization_band_available: bool


@dataclass(frozen=True)
class DReferenceQualification:
    reference_id: str
    deletion_class: str
    qualified: bool
    blockers: tuple[str, ...]


def qualify_d_reference(candidate: DReferenceCandidate) -> DReferenceQualification:
    blockers: list[str] = []
    if not isinstance(candidate.reference_id, str) or not candidate.reference_id.strip():
        blockers.append("REFERENCE_ID_MISSING")
    if candidate.deletion_class not in _ALLOWED_CLASSES:
        blockers.append("DELETION_CLASS_NOT_PREDECLARED")
    if not candidate.marker_pattern_verified:
        blockers.append("REGISTERED_MARKER_PATTERN_NOT_VERIFIED")
    if not candidate.core_reference_present:
        blockers.append("CORE_REFERENCE_NOT_VERIFIED_PRESENT")
    if not candidate.pre_existing_at_72h:
        blockers.append("REFERENCE_NOT_PRE_EXISTING_AT_72H")
    if not candidate.same_medium_and_context:
        blockers.append("REFERENCE_CONTEXT_NOT_MATCHED")
    if not candidate.independently_derived:
        blockers.append("REFERENCE_NOT_INDEPENDENTLY_DERIVED")
    if candidate.candidate_outcomes_used_for_selection:
        blockers.append("CANDIDATE_OUTCOME_USED_FOR_REFERENCE_SELECTION")
    if not candidate.viable_at_72h:
        blockers.append("REFERENCE_NOT_MEASURABLE_AT_INTERVAL_START")
    if not candidate.measurable_at_120h:
        blockers.append("REFERENCE_NOT_MEASURABLE_AT_INTERVAL_END")
    if candidate.gross_secondary_rearrangement_unresolved:
        blockers.append("GROSS_SECONDARY_REARRANGEMENT_UNRESOLVED")
    if not candidate.realization_band_available:
        blockers.append("REALIZATION_BAND_NOT_AVAILABLE")
    return DReferenceQualification(
        reference_id=candidate.reference_id,
        deletion_class=candidate.deletion_class,
        qualified=not blockers,
        blockers=tuple(blockers),
    )


def adjudicate_reference_panel(
    candidates: tuple[DReferenceCandidate, ...], *, minimum_per_class: int = 2
) -> tuple[bool, tuple[str, ...], tuple[DReferenceQualification, ...]]:
    if minimum_per_class < 2:
        raise ValueError("minimum_per_class must be at least two")
    qualifications = tuple(qualify_d_reference(c) for c in candidates)
    qualified_counts = {name: 0 for name in _ALLOWED_CLASSES}
    for q in qualifications:
        if q.qualified:
            qualified_counts[q.deletion_class] += 1
    blockers = tuple(
        f"{class_id}_QUALIFIED_REFERENCE_COUNT_BELOW_{minimum_per_class}"
        for class_id in sorted(_ALLOWED_CLASSES)
        if qualified_counts[class_id] < minimum_per_class
    )
    return not blockers, blockers, qualifications
