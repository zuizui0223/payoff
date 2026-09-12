"""Gate M5_T0 BGI marker opening on a frozen qualified calibration receipt.

This module does not download or inspect M5 target reads. It only decides whether
the target lane is licensed to open and transports the frozen calibration
thresholds without allowing refit.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


TARGET = "M5_T0"
TARGET_BGI_RUN = "SRR16954696"
CORE_PANEL = (
    "SCO3000", "SCO3300", "SCO3600", "SCO3900", "SCO4200",
    "SCO4500", "SCO4800", "SCO5100", "SCO5400",
)


@dataclass(frozen=True)
class FrozenCalibration:
    receipt_id: str
    calibration_qualified: bool
    target_candidate_id: str
    target_bgi_ratios_opened_for_calibration: bool
    absence_max_ratio: float | None
    presence_min_ratio: float | None
    core_panel: tuple[str, ...]
    absent_pair_count: int
    present_pair_count: int
    absent_candidate_count: int
    present_candidate_count: int


@dataclass(frozen=True)
class TargetOpeningDecision:
    target_opening_allowed: bool
    target_bgi_run: str
    absence_max_ratio: float | None
    presence_min_ratio: float | None
    blockers: tuple[str, ...]


def _threshold(value: object, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric")
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(out) or out < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return out


def adjudicate_m5_target_opening(cal: FrozenCalibration) -> TargetOpeningDecision:
    blockers: list[str] = []
    if not cal.receipt_id.strip():
        raise ValueError("receipt_id must be non-empty")
    if cal.target_candidate_id != TARGET:
        blockers.append("CALIBRATION_TARGET_ID_MISMATCH")
    if cal.target_bgi_ratios_opened_for_calibration:
        blockers.append("TARGET_WAS_OPENED_DURING_CALIBRATION")
    if tuple(cal.core_panel) != CORE_PANEL:
        blockers.append("CORE_NORMALIZATION_PANEL_MISMATCH")
    if not cal.calibration_qualified:
        blockers.append("RESPONSE_BLIND_CALIBRATION_NOT_QUALIFIED")
    if cal.absent_pair_count < 3 or cal.present_pair_count < 3:
        blockers.append("CALIBRATION_PAIR_REDUNDANCY_FLOOR_NOT_MET")
    if cal.absent_candidate_count < 2 or cal.present_candidate_count < 2:
        blockers.append("CALIBRATION_CANDIDATE_REDUNDANCY_FLOOR_NOT_MET")

    absence = None
    presence = None
    if cal.absence_max_ratio is None or cal.presence_min_ratio is None:
        blockers.append("FROZEN_CALIBRATION_THRESHOLDS_MISSING")
    else:
        absence = _threshold(cal.absence_max_ratio, "absence_max_ratio")
        presence = _threshold(cal.presence_min_ratio, "presence_min_ratio")
        if absence >= presence:
            blockers.append("FROZEN_CALIBRATION_THRESHOLDS_NOT_SEPARATED")

    allowed = not blockers
    return TargetOpeningDecision(
        target_opening_allowed=allowed,
        target_bgi_run=TARGET_BGI_RUN,
        absence_max_ratio=absence if allowed else None,
        presence_min_ratio=presence if allowed else None,
        blockers=tuple(blockers),
    )
