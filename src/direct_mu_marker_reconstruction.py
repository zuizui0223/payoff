"""Fail-closed reconstruction of registered terminal-deletion marker states.

This module sits strictly between a qualified candidate-to-sequence mapping and
the existing D-reference qualification gate.  It can assign the registered
ENTRY/INTERMEDIATE/DEEP marker class from precomputed normalized locus evidence,
but it cannot establish physical material identity, D realization, or a
qualified direct-mu reference.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping


REGISTERED_MARKERS = ("SCO7662", "SCO7350", "SCO7036", "SCO3879")
REGISTERED_CLASSES = {
    ("ABSENT", "PRESENT", "PRESENT"): "ENTRY_CLASS",
    ("ABSENT", "ABSENT", "PRESENT"): "INTERMEDIATE_CLASS",
    ("ABSENT", "ABSENT", "ABSENT"): "DEEP_CLASS",
}


@dataclass(frozen=True)
class MarkerReconstructionInput:
    candidate_id: str
    sequence_sample_map_qualified: bool
    primary_short_read_run: str
    reference_accession: str
    normalization_panel_id: str
    thresholds_frozen_preoutcome: bool
    absence_max_ratio: float
    presence_min_ratio: float
    normalized_marker_ratios: Mapping[str, float]


@dataclass(frozen=True)
class MarkerReconstructionReceipt:
    candidate_id: str
    marker_states: Mapping[str, str]
    registered_class: str | None
    marker_pattern_verified: bool
    blockers: tuple[str, ...]
    physical_material_identity_established: bool = False
    gross_rearrangement_audit_completed: bool = False
    realization_band_available: bool = False
    reference_qualified: bool = False


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _ratio(value: object, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric")
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(out) or out < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return out


def _state(value: float, *, absence_max: float, presence_min: float) -> str:
    if value <= absence_max:
        return "ABSENT"
    if value >= presence_min:
        return "PRESENT"
    return "UNRESOLVED"


def reconstruct_registered_marker_pattern(
    inp: MarkerReconstructionInput,
) -> MarkerReconstructionReceipt:
    _nonempty(inp.candidate_id, "candidate_id")
    _nonempty(inp.primary_short_read_run, "primary_short_read_run")
    _nonempty(inp.reference_accession, "reference_accession")
    _nonempty(inp.normalization_panel_id, "normalization_panel_id")

    absence_max = _ratio(inp.absence_max_ratio, "absence_max_ratio")
    presence_min = _ratio(inp.presence_min_ratio, "presence_min_ratio")
    if absence_max >= presence_min:
        raise ValueError("absence_max_ratio must be strictly below presence_min_ratio")

    if set(inp.normalized_marker_ratios) != set(REGISTERED_MARKERS):
        missing = sorted(set(REGISTERED_MARKERS) - set(inp.normalized_marker_ratios))
        extra = sorted(set(inp.normalized_marker_ratios) - set(REGISTERED_MARKERS))
        raise ValueError(f"registered marker mismatch; missing={missing}, extra={extra}")

    ratios = {
        marker: _ratio(inp.normalized_marker_ratios[marker], marker)
        for marker in REGISTERED_MARKERS
    }
    states = {
        marker: _state(ratios[marker], absence_max=absence_max, presence_min=presence_min)
        for marker in REGISTERED_MARKERS
    }

    blockers: list[str] = []
    if not inp.sequence_sample_map_qualified:
        blockers.append("SEQUENCE_SAMPLE_MAP_NOT_QUALIFIED")
    if not inp.thresholds_frozen_preoutcome:
        blockers.append("MARKER_CALL_THRESHOLDS_NOT_FROZEN_PREOUTCOME")
    if states["SCO3879"] != "PRESENT":
        blockers.append("CORE_SCO3879_NOT_VERIFIED_PRESENT")
    if any(states[m] == "UNRESOLVED" for m in REGISTERED_MARKERS):
        blockers.append("AT_LEAST_ONE_REGISTERED_MARKER_UNRESOLVED")

    right_arm_pattern = (states["SCO7662"], states["SCO7350"], states["SCO7036"])
    registered_class = REGISTERED_CLASSES.get(right_arm_pattern)
    if registered_class is None:
        blockers.append("RIGHT_ARM_PATTERN_NOT_A_REGISTERED_D_CLASS")

    verified = not blockers and registered_class is not None
    return MarkerReconstructionReceipt(
        candidate_id=inp.candidate_id,
        marker_states=states,
        registered_class=registered_class if verified else None,
        marker_pattern_verified=verified,
        blockers=tuple(blockers),
    )
