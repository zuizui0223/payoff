"""Response-blind BGI marker calibration for the frozen M5 direct-mu lane.

The target M5_T0 is forbidden from this calibration.  Non-M5 controls are
labelled marker-by-marker from an independent PacBio channel using only exact
0% / 100% coverage states, then their BGI normalized ratios define conservative
absent/present extrema.  No M5 BGI ratio is accepted by this module.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


TARGET_CANDIDATE = "M5_T0"
REGISTERED_MARKERS = frozenset({"SCO7662", "SCO7350", "SCO7036", "SCO3879"})


@dataclass(frozen=True)
class CalibrationPair:
    candidate_id: str
    marker: str
    pacbio_marker_coverage_pct: float
    pacbio_core_coverage_pct: float
    bgi_normalized_ratio: float


@dataclass(frozen=True)
class CalibrationResult:
    calibration_qualified: bool
    absence_max_ratio: float | None
    presence_min_ratio: float | None
    absent_pair_count: int
    present_pair_count: int
    absent_candidate_count: int
    present_candidate_count: int
    unresolved_pair_count: int
    blockers: tuple[str, ...]


def _number(value: object, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric")
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(out) or out < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return out


def _control_state(marker_cov: float, core_cov: float) -> str:
    # A control contributes only if its independent PacBio core is completely
    # covered.  Exact 0/100 states avoid introducing a hidden post-target cutoff.
    if core_cov != 100.0:
        return "UNRESOLVED"
    if marker_cov == 0.0:
        return "ABSENT"
    if marker_cov == 100.0:
        return "PRESENT"
    return "UNRESOLVED"


def calibrate_bgi_marker_thresholds(
    pairs: Iterable[CalibrationPair],
    *,
    minimum_pairs_per_state: int = 3,
    minimum_candidates_per_state: int = 2,
) -> CalibrationResult:
    if minimum_pairs_per_state < 1 or minimum_candidates_per_state < 1:
        raise ValueError("minimum calibration floors must be positive")

    absent: list[tuple[str, float]] = []
    present: list[tuple[str, float]] = []
    unresolved = 0
    seen_rows: set[tuple[str, str]] = set()

    for pair in pairs:
        candidate = pair.candidate_id.strip()
        marker = pair.marker.strip()
        if not candidate:
            raise ValueError("candidate_id must be non-empty")
        if candidate == TARGET_CANDIDATE:
            raise ValueError("M5_T0 target data are forbidden in response-blind calibration")
        if marker not in REGISTERED_MARKERS:
            raise ValueError(f"unregistered marker {marker!r}")
        key = (candidate, marker)
        if key in seen_rows:
            raise ValueError(f"duplicate calibration pair {key}")
        seen_rows.add(key)

        marker_cov = _number(pair.pacbio_marker_coverage_pct, "pacbio_marker_coverage_pct")
        core_cov = _number(pair.pacbio_core_coverage_pct, "pacbio_core_coverage_pct")
        ratio = _number(pair.bgi_normalized_ratio, "bgi_normalized_ratio")
        if marker_cov > 100 or core_cov > 100:
            raise ValueError("coverage percentages must be <= 100")

        state = _control_state(marker_cov, core_cov)
        if state == "ABSENT":
            absent.append((candidate, ratio))
        elif state == "PRESENT":
            present.append((candidate, ratio))
        else:
            unresolved += 1

    blockers: list[str] = []
    absent_candidates = {x[0] for x in absent}
    present_candidates = {x[0] for x in present}
    if len(absent) < minimum_pairs_per_state:
        blockers.append("ABSENT_CONTROL_PAIR_COUNT_BELOW_FLOOR")
    if len(present) < minimum_pairs_per_state:
        blockers.append("PRESENT_CONTROL_PAIR_COUNT_BELOW_FLOOR")
    if len(absent_candidates) < minimum_candidates_per_state:
        blockers.append("ABSENT_CONTROL_CANDIDATE_COUNT_BELOW_FLOOR")
    if len(present_candidates) < minimum_candidates_per_state:
        blockers.append("PRESENT_CONTROL_CANDIDATE_COUNT_BELOW_FLOOR")

    absence_max = max((x[1] for x in absent), default=None)
    presence_min = min((x[1] for x in present), default=None)
    if absence_max is not None and presence_min is not None and absence_max >= presence_min:
        blockers.append("ABSENT_PRESENT_BGI_CALIBRATION_SETS_TOUCH_OR_OVERLAP")

    qualified = not blockers and absence_max is not None and presence_min is not None
    return CalibrationResult(
        calibration_qualified=qualified,
        absence_max_ratio=absence_max,
        presence_min_ratio=presence_min,
        absent_pair_count=len(absent),
        present_pair_count=len(present),
        absent_candidate_count=len(absent_candidates),
        present_candidate_count=len(present_candidates),
        unresolved_pair_count=unresolved,
        blockers=tuple(blockers),
    )
