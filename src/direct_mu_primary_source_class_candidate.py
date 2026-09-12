"""Adjudicate source-level deletion-class candidacy without qualifying a D reference.

This layer is intentionally weaker than direct_mu_reference_panel_qualification.
Primary-source marker phenotypes may narrow which registered severity class a
candidate probably occupies, but only direct scoring of the frozen marker panel
may satisfy the registered class gate.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceMarkerEvidence:
    entry_marker_loss_supported: bool
    deep_marker_loss_supported: bool
    terminal_deletion_context_supported: bool
    exact_registered_marker_pattern_verified: bool = False


@dataclass(frozen=True)
class SourceClassAdjudication:
    candidate_class: str | None
    candidate_supported: bool
    registered_class_qualified: bool
    blockers: tuple[str, ...]


def adjudicate_source_class(e: SourceMarkerEvidence) -> SourceClassAdjudication:
    blockers: list[str] = []

    # A supported deep marker loss implies that the source evidence is most
    # consistent with the deepest registered right-arm severity class, provided
    # the study also interprets the phenotype within a terminal-deletion context.
    deep_supported = bool(
        e.entry_marker_loss_supported
        and e.deep_marker_loss_supported
        and e.terminal_deletion_context_supported
    )

    candidate_class = "DEEP_CLASS" if deep_supported else None
    if not deep_supported:
        blockers.append("DEEP_CLASS_CANDIDATE_NOT_SUPPORTED_BY_SOURCE_EVIDENCE")

    # This source-level layer can never reconstruct an unmeasured intermediate
    # locus by implication. Exact registered pattern verification is an
    # independent requirement of the downstream reference qualification gate.
    if not e.exact_registered_marker_pattern_verified:
        blockers.append("EXACT_REGISTERED_MARKER_PATTERN_NOT_VERIFIED")

    return SourceClassAdjudication(
        candidate_class=candidate_class,
        candidate_supported=deep_supported,
        registered_class_qualified=(deep_supported and e.exact_registered_marker_pattern_verified),
        blockers=tuple(blockers),
    )
