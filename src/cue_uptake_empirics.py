"""Fail-closed helpers for the greater-snow-goose cue-uptake lane.

These utilities implement only preregistered model-selection semantics.  They do
not infer PAYOFF-B delay cost D and must not be used to label a behavioral
threshold as q_wait(D).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class ThresholdCandidateScore:
    threshold_q: float
    mean_loio_log_loss: float
    se_loio_log_loss: float


@dataclass(frozen=True)
class ThresholdSelection:
    status: str
    selected_q: float | None
    best_mean_log_loss: float | None
    no_threshold_mean_log_loss: float
    reason: str


def mean_standard_error(values: Iterable[float]) -> tuple[float, float]:
    xs = [float(x) for x in values]
    if not xs:
        raise ValueError("at least one value is required")
    if any(not isfinite(x) for x in xs):
        raise ValueError("values must be finite")
    mean = sum(xs) / len(xs)
    if len(xs) == 1:
        return mean, 0.0
    variance = sum((x - mean) ** 2 for x in xs) / (len(xs) - 1)
    return mean, (variance / len(xs)) ** 0.5


def select_threshold_one_se(
    candidates: Iterable[ThresholdCandidateScore],
    *,
    no_threshold_mean_log_loss: float,
) -> ThresholdSelection:
    """Apply the frozen threshold support gate.

    A threshold is identified only when:
      1. the minimum-loss candidate is an interior grid point;
      2. it has lower mean LOIO log loss than the continuous no-threshold model;
      3. both immediately adjacent grid points have mean loss strictly greater
         than best_mean + best_SE.

    The third rule operationalises the preregistered phrase "adjacent grid
    points are not tied within 1 SE" before any outcome is opened.
    """

    rows = sorted(candidates, key=lambda x: x.threshold_q)
    if len(rows) < 3:
        raise ValueError("at least three ordered threshold candidates required")
    if any(
        (not isfinite(r.threshold_q))
        or (not 0.5 <= r.threshold_q <= 1.0)
        or (not isfinite(r.mean_loio_log_loss))
        or (not isfinite(r.se_loio_log_loss))
        or r.se_loio_log_loss < 0.0
        for r in rows
    ):
        raise ValueError("candidate scores contain invalid values")
    if not isfinite(no_threshold_mean_log_loss):
        raise ValueError("no-threshold loss must be finite")

    best_i = min(
        range(len(rows)),
        key=lambda i: (rows[i].mean_loio_log_loss, rows[i].threshold_q),
    )
    best = rows[best_i]

    if best_i == 0 or best_i == len(rows) - 1:
        return ThresholdSelection(
            status="THRESHOLD_NOT_IDENTIFIED",
            selected_q=None,
            best_mean_log_loss=best.mean_loio_log_loss,
            no_threshold_mean_log_loss=float(no_threshold_mean_log_loss),
            reason="best_candidate_on_grid_boundary",
        )

    if best.mean_loio_log_loss >= no_threshold_mean_log_loss:
        return ThresholdSelection(
            status="THRESHOLD_NOT_IDENTIFIED",
            selected_q=None,
            best_mean_log_loss=best.mean_loio_log_loss,
            no_threshold_mean_log_loss=float(no_threshold_mean_log_loss),
            reason="best_threshold_does_not_beat_no_threshold_model",
        )

    tie_limit = best.mean_loio_log_loss + best.se_loio_log_loss
    lower = rows[best_i - 1]
    upper = rows[best_i + 1]
    if (
        lower.mean_loio_log_loss <= tie_limit
        or upper.mean_loio_log_loss <= tie_limit
    ):
        return ThresholdSelection(
            status="THRESHOLD_NOT_IDENTIFIED",
            selected_q=None,
            best_mean_log_loss=best.mean_loio_log_loss,
            no_threshold_mean_log_loss=float(no_threshold_mean_log_loss),
            reason="adjacent_grid_point_tied_within_one_se",
        )

    return ThresholdSelection(
        status="BEHAVIORAL_THRESHOLD_IDENTIFIED",
        selected_q=best.threshold_q,
        best_mean_log_loss=best.mean_loio_log_loss,
        no_threshold_mean_log_loss=float(no_threshold_mean_log_loss),
        reason="interior_threshold_beats_no_threshold_and_adjacent_points",
    )
