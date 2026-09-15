"""Fail-closed chromosome-scale audit for the M5 direct-mu reference lane.

The gate resolves whether gross secondary rearrangement remains *uncharacterized*.
It does not require a clean genome and it never qualifies a D reference by itself.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


TARGET = "M5_T0"
TARGET_PACBIO = "SRR16954720"
WT_PACBIO = "SRR16954715"


@dataclass(frozen=True)
class GrossEvent:
    event_id: str
    event_type: str
    size_bp: int
    source_channel: str
    breakpoint_or_interval_resolved: bool


@dataclass(frozen=True)
class GrossAuditEvidence:
    candidate_id: str
    target_pacbio_run: str
    wt_control_run: str
    reference_accession: str
    coverage_bin_bp: int
    gross_event_min_bp: int
    m5_central_depth: float
    wt_central_depth: float
    coverage_segmentation_completed: bool
    left_terminal_boundary_resolved: bool
    right_terminal_boundary_resolved: bool
    long_read_sv_calling_completed: bool
    wt_control_processed_same_pipeline: bool
    all_detected_gross_events_catalogued: bool
    events: tuple[GrossEvent, ...]


@dataclass(frozen=True)
class GrossAuditResult:
    gross_secondary_rearrangement_unresolved: bool
    audit_completed: bool
    event_count: int
    additional_gross_event_count: int
    blockers: tuple[str, ...]
    qualified_d_reference: bool = False


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _depth(value: object, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric")
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(out) or out < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return out


def adjudicate_gross_rearrangement_audit(
    evidence: GrossAuditEvidence,
    *,
    minimum_central_depth: float = 10.0,
) -> GrossAuditResult:
    if evidence.candidate_id != TARGET:
        raise ValueError(f"gross-audit v1 is frozen to {TARGET}")
    if evidence.target_pacbio_run != TARGET_PACBIO:
        raise ValueError("unexpected M5_T0 PacBio run")
    if evidence.wt_control_run != WT_PACBIO:
        raise ValueError("unexpected WT control PacBio run")
    _nonempty(evidence.reference_accession, "reference_accession")
    if evidence.coverage_bin_bp != 10_000:
        raise ValueError("coverage_bin_bp must remain frozen at 10000")
    if evidence.gross_event_min_bp != 50_000:
        raise ValueError("gross_event_min_bp must remain frozen at 50000")
    if minimum_central_depth <= 0:
        raise ValueError("minimum_central_depth must be positive")

    m5_depth = _depth(evidence.m5_central_depth, "m5_central_depth")
    wt_depth = _depth(evidence.wt_central_depth, "wt_central_depth")

    blockers: list[str] = []
    if m5_depth < minimum_central_depth:
        blockers.append("M5_CENTRAL_PACBIO_DEPTH_BELOW_FLOOR")
    if wt_depth < minimum_central_depth:
        blockers.append("WT_CONTROL_CENTRAL_PACBIO_DEPTH_BELOW_FLOOR")
    if not evidence.coverage_segmentation_completed:
        blockers.append("CHROMOSOME_WIDE_COVERAGE_SEGMENTATION_NOT_COMPLETED")
    if not evidence.left_terminal_boundary_resolved:
        blockers.append("LEFT_TERMINAL_BOUNDARY_UNRESOLVED")
    if not evidence.right_terminal_boundary_resolved:
        blockers.append("RIGHT_TERMINAL_BOUNDARY_UNRESOLVED")
    if not evidence.long_read_sv_calling_completed:
        blockers.append("LONG_READ_GROSS_SV_CALLING_NOT_COMPLETED")
    if not evidence.wt_control_processed_same_pipeline:
        blockers.append("WT_CONTROL_NOT_PROCESSED_THROUGH_SAME_PIPELINE")
    if not evidence.all_detected_gross_events_catalogued:
        blockers.append("DETECTED_GROSS_EVENTS_NOT_FULLY_CATALOGUED")

    ids: set[str] = set()
    additional = 0
    for event in evidence.events:
        event_id = _nonempty(event.event_id, "event_id")
        _nonempty(event.event_type, "event_type")
        _nonempty(event.source_channel, "source_channel")
        if event_id in ids:
            raise ValueError(f"duplicate gross event id {event_id!r}")
        ids.add(event_id)
        if isinstance(event.size_bp, bool) or not isinstance(event.size_bp, int):
            raise ValueError("gross event size_bp must be an integer")
        if event.size_bp < evidence.gross_event_min_bp:
            raise ValueError("events below the registered gross-event floor must not enter the catalog")
        if not event.breakpoint_or_interval_resolved:
            blockers.append(f"GROSS_EVENT_UNRESOLVED:{event_id}")
        if event.event_type not in {"LEFT_TERMINAL_LOSS", "RIGHT_TERMINAL_LOSS"}:
            additional += 1

    completed = not blockers
    return GrossAuditResult(
        gross_secondary_rearrangement_unresolved=not completed,
        audit_completed=completed,
        event_count=len(evidence.events),
        additional_gross_event_count=additional,
        blockers=tuple(blockers),
    )
