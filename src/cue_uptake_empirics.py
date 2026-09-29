"""Fail-closed helpers for the greater-snow-goose cue-uptake lane.

These utilities implement preregistered model-selection semantics only. They do
not infer PAYOFF-B delay cost D and must not be used to label a behavioral
threshold as q_wait(D).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Iterable, Mapping, Sequence


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
    lower_neighbor_q: float | None = None
    upper_neighbor_q: float | None = None
    lower_paired_mean_difference: float | None = None
    upper_paired_mean_difference: float | None = None
    lower_paired_se: float | None = None
    upper_paired_se: float | None = None


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
    return mean, sqrt(variance / len(xs))


def paired_difference_standard_error(
    worse_losses: Sequence[float],
    selected_losses: Sequence[float],
) -> tuple[float, float]:
    """Mean paired LOIO loss difference and its standard error."""

    worse = [float(x) for x in worse_losses]
    selected = [float(x) for x in selected_losses]
    if len(worse) != len(selected) or len(worse) < 2:
        raise ValueError("paired fold losses must align and contain >=2 folds")
    diffs = [a - b for a, b in zip(worse, selected)]
    if any(not isfinite(x) for x in diffs):
        raise ValueError("paired fold differences must be finite")
    return mean_standard_error(diffs)


def select_threshold_paired_one_se(
    candidate_fold_losses: Mapping[float, Sequence[float]],
    *,
    no_threshold_fold_losses: Sequence[float],
    frozen_grid: Sequence[float],
) -> ThresholdSelection:
    """Apply the frozen paired-LOIO threshold support gate.

    Every candidate and the no-threshold comparator must be scored on the same
    held-out individuals. A behavioral threshold is identified only when:
      1. every frozen q-grid candidate is estimable on the same folds;
      2. the minimum mean-loss candidate is an interior grid point;
      3. it beats the no-threshold model in mean LOIO loss; and
      4. each adjacent q candidate has paired mean loss difference
         (adjacent - selected) greater than one SE of the paired differences.

    The paired comparison removes between-individual prediction difficulty from
    the 1-SE adjudication.
    """

    grid = tuple(float(q) for q in frozen_grid)
    if len(grid) < 3 or len(set(grid)) != len(grid):
        raise ValueError("frozen_grid must contain >=3 unique q values")
    if tuple(sorted(grid)) != grid:
        raise ValueError("frozen_grid must be strictly ordered")

    observed = {float(q) for q in candidate_fold_losses}
    if observed != set(grid):
        return ThresholdSelection(
            status="THRESHOLD_NOT_IDENTIFIED",
            selected_q=None,
            best_mean_log_loss=None,
            no_threshold_mean_log_loss=float("nan"),
            reason="incomplete_frozen_q_grid",
        )

    baseline = [float(x) for x in no_threshold_fold_losses]
    if len(baseline) < 2 or any(not isfinite(x) for x in baseline):
        return ThresholdSelection(
            status="THRESHOLD_NOT_IDENTIFIED",
            selected_q=None,
            best_mean_log_loss=None,
            no_threshold_mean_log_loss=float("nan"),
            reason="invalid_no_threshold_folds",
        )

    losses: dict[float, list[float]] = {}
    for q in grid:
        row = [float(x) for x in candidate_fold_losses[q]]
        if (
            len(row) != len(baseline)
            or len(row) < 2
            or any(not isfinite(x) for x in row)
        ):
            return ThresholdSelection(
                status="THRESHOLD_NOT_IDENTIFIED",
                selected_q=None,
                best_mean_log_loss=None,
                no_threshold_mean_log_loss=sum(baseline) / len(baseline),
                reason="incomplete_or_invalid_candidate_folds",
            )
        losses[q] = row

    means = {q: sum(losses[q]) / len(losses[q]) for q in grid}
    no_mean = sum(baseline) / len(baseline)
    best_i = min(range(len(grid)), key=lambda i: (means[grid[i]], grid[i]))
    best_q = grid[best_i]
    best_mean = means[best_q]

    if best_i == 0 or best_i == len(grid) - 1:
        return ThresholdSelection(
            status="THRESHOLD_NOT_IDENTIFIED",
            selected_q=None,
            best_mean_log_loss=best_mean,
            no_threshold_mean_log_loss=no_mean,
            reason="best_candidate_on_grid_boundary",
        )

    if best_mean >= no_mean:
        return ThresholdSelection(
            status="THRESHOLD_NOT_IDENTIFIED",
            selected_q=None,
            best_mean_log_loss=best_mean,
            no_threshold_mean_log_loss=no_mean,
            reason="best_threshold_does_not_beat_no_threshold_model",
        )

    lower_q = grid[best_i - 1]
    upper_q = grid[best_i + 1]
    lower_diff, lower_se = paired_difference_standard_error(
        losses[lower_q], losses[best_q]
    )
    upper_diff, upper_se = paired_difference_standard_error(
        losses[upper_q], losses[best_q]
    )

    tied = []
    if not lower_diff > lower_se:
        tied.append("lower")
    if not upper_diff > upper_se:
        tied.append("upper")
    if tied:
        return ThresholdSelection(
            status="THRESHOLD_NOT_IDENTIFIED",
            selected_q=None,
            best_mean_log_loss=best_mean,
            no_threshold_mean_log_loss=no_mean,
            reason="adjacent_grid_point_tied_within_paired_one_se:"
            + ",".join(tied),
            lower_neighbor_q=lower_q,
            upper_neighbor_q=upper_q,
            lower_paired_mean_difference=lower_diff,
            upper_paired_mean_difference=upper_diff,
            lower_paired_se=lower_se,
            upper_paired_se=upper_se,
        )

    return ThresholdSelection(
        status="BEHAVIORAL_THRESHOLD_IDENTIFIED",
        selected_q=best_q,
        best_mean_log_loss=best_mean,
        no_threshold_mean_log_loss=no_mean,
        reason="interior_threshold_beats_no_threshold_and_paired_adjacent_points",
        lower_neighbor_q=lower_q,
        upper_neighbor_q=upper_q,
        lower_paired_mean_difference=lower_diff,
        upper_paired_mean_difference=upper_diff,
        lower_paired_se=lower_se,
        upper_paired_se=upper_se,
    )


def select_threshold_one_se(
    candidates: Iterable[ThresholdCandidateScore],
    *,
    no_threshold_mean_log_loss: float,
) -> ThresholdSelection:
    """Legacy summary-only helper.

    New empirical execution must use select_threshold_paired_one_se().
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
            "THRESHOLD_NOT_IDENTIFIED", None, best.mean_loio_log_loss,
            float(no_threshold_mean_log_loss),
            "best_candidate_on_grid_boundary",
        )
    if best.mean_loio_log_loss >= no_threshold_mean_log_loss:
        return ThresholdSelection(
            "THRESHOLD_NOT_IDENTIFIED", None, best.mean_loio_log_loss,
            float(no_threshold_mean_log_loss),
            "best_threshold_does_not_beat_no_threshold_model",
        )

    tie_limit = best.mean_loio_log_loss + best.se_loio_log_loss
    lower = rows[best_i - 1]
    upper = rows[best_i + 1]
    if (
        lower.mean_loio_log_loss <= tie_limit
        or upper.mean_loio_log_loss <= tie_limit
    ):
        return ThresholdSelection(
            "THRESHOLD_NOT_IDENTIFIED", None, best.mean_loio_log_loss,
            float(no_threshold_mean_log_loss),
            "adjacent_grid_point_tied_within_one_se",
        )
    return ThresholdSelection(
        "BEHAVIORAL_THRESHOLD_IDENTIFIED", best.threshold_q,
        best.mean_loio_log_loss, float(no_threshold_mean_log_loss),
        "interior_threshold_beats_no_threshold_and_adjacent_points",
    )
