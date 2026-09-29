"""Fail-closed helpers for the prospective greater-snow-goose GPS cue-use lane."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt


FROZEN_Q_GRID = (
    0.500, 0.525, 0.550, 0.575, 0.600,
    0.625, 0.650, 0.675, 0.700,
)


@dataclass(frozen=True)
class CueUptakeEstimability:
    estimable: bool
    reasons: tuple[str, ...]
    individuals: int
    years: int
    contexts: int
    departure_events: int
    context_years: int
    predictive_connectivity_sd: float
    minimum_within_context_connectivity_sd: float


@dataclass(frozen=True)
class ThresholdAdjudication:
    status: str
    selected_threshold_q: float | None
    selected_mean_log_loss: float | None
    no_threshold_mean_log_loss: float | None
    lower_neighbor_q: float | None
    upper_neighbor_q: float | None
    lower_paired_mean_difference: float | None
    upper_paired_mean_difference: float | None
    lower_paired_se: float | None
    upper_paired_se: float | None
    reasons: tuple[str, ...]


def evaluate_estimability(
    *,
    individuals: int,
    years: int,
    contexts: int,
    departure_events: int,
    context_years: int,
    predictive_connectivity_sd: float,
    minimum_within_context_connectivity_sd: float,
) -> CueUptakeEstimability:
    """Apply the preregistered estimability gate exactly."""

    sd = float(predictive_connectivity_sd)
    within_sd = float(minimum_within_context_connectivity_sd)
    if not isfinite(sd) or sd < 0.0:
        raise ValueError("predictive_connectivity_sd must be finite and non-negative")
    if not isfinite(within_sd) or within_sd < 0.0:
        raise ValueError(
            "minimum_within_context_connectivity_sd must be finite and non-negative"
        )

    reasons = []
    if int(individuals) < 30:
        reasons.append("FEWER_THAN_30_INDIVIDUALS")
    if int(years) < 4:
        reasons.append("FEWER_THAN_4_YEARS")
    if int(contexts) < 3:
        reasons.append("FEWER_THAN_3_CONTEXTS")
    if int(departure_events) < 100:
        reasons.append("FEWER_THAN_100_DEPARTURES")
    if int(context_years) < 12:
        reasons.append("FEWER_THAN_12_CONTEXT_YEAR_CLUSTERS")
    if sd < 0.03:
        reasons.append("PREDICTIVE_CONNECTIVITY_SD_BELOW_0_03")
    if within_sd <= 0.0:
        reasons.append("NO_WITHIN_CONTEXT_CONNECTIVITY_VARIATION")

    return CueUptakeEstimability(
        estimable=not reasons,
        reasons=tuple(reasons),
        individuals=int(individuals),
        years=int(years),
        contexts=int(contexts),
        departure_events=int(departure_events),
        context_years=int(context_years),
        predictive_connectivity_sd=sd,
        minimum_within_context_connectivity_sd=within_sd,
    )


def gaussian_binary_q(rho: float) -> float:
    """Secondary Gaussian sign-agreement bridge q=0.5+asin(rho)/pi."""

    from math import asin, pi

    r = float(rho)
    if not isfinite(r) or not -1.0 <= r <= 1.0:
        raise ValueError("rho must lie in [-1, 1]")
    return 0.5 + asin(r) / pi


def threshold_active(q: float, threshold: float) -> bool:
    """Frozen secondary threshold indicator."""

    value = float(q)
    cut = float(threshold)
    if not all(isfinite(x) for x in (value, cut)):
        raise ValueError("q and threshold must be finite")
    if cut not in FROZEN_Q_GRID:
        raise ValueError("threshold is not on the frozen q grid")
    return value >= cut


def preoutcome_training_valid(
    *,
    focal_year: int,
    training_end_year: int,
    training_years: int,
) -> bool:
    """Historical predictive-connectivity data must end before focal year."""

    return int(training_end_year) <= int(focal_year) - 1 and int(training_years) >= 15


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _paired_difference_summary(
    worse_losses: list[float],
    selected_losses: list[float],
) -> tuple[float, float]:
    """Mean paired loss difference and its standard error."""

    if len(worse_losses) != len(selected_losses) or len(worse_losses) < 2:
        raise ValueError("paired fold losses must have equal length >= 2")
    diffs = [float(a) - float(b) for a, b in zip(worse_losses, selected_losses)]
    if any(not isfinite(x) for x in diffs):
        raise ValueError("fold losses must be finite")
    mean_diff = _mean(diffs)
    variance = sum((x - mean_diff) ** 2 for x in diffs) / (len(diffs) - 1)
    return mean_diff, sqrt(variance / len(diffs))


def adjudicate_threshold_folds(
    *,
    no_threshold_losses: list[float],
    candidate_losses: dict[float, list[float]],
) -> ThresholdAdjudication:
    """Apply the frozen secondary threshold support gate.

    All candidates must be estimable on the same leave-one-individual-out
    folds.  The selected candidate must:
      1. be an interior point of FROZEN_Q_GRID;
      2. have lower mean log loss than the no-threshold model; and
      3. beat each adjacent grid point by more than one standard error of the
         paired fold-loss difference.

    Otherwise the result fails closed as THRESHOLD_NOT_IDENTIFIED.
    """

    expected = set(FROZEN_Q_GRID)
    observed = {float(k) for k in candidate_losses}
    reasons: list[str] = []
    if observed != expected:
        reasons.append("INCOMPLETE_FROZEN_Q_GRID")
        return ThresholdAdjudication(
            status="THRESHOLD_NOT_IDENTIFIED",
            selected_threshold_q=None,
            selected_mean_log_loss=None,
            no_threshold_mean_log_loss=None,
            lower_neighbor_q=None,
            upper_neighbor_q=None,
            lower_paired_mean_difference=None,
            upper_paired_mean_difference=None,
            lower_paired_se=None,
            upper_paired_se=None,
            reasons=tuple(reasons),
        )

    n = len(no_threshold_losses)
    if n < 2 or any(not isfinite(float(x)) for x in no_threshold_losses):
        reasons.append("INVALID_NO_THRESHOLD_FOLDS")
    for q in FROZEN_Q_GRID:
        losses = candidate_losses[q]
        if (
            len(losses) != n
            or len(losses) < 2
            or any(not isfinite(float(x)) for x in losses)
        ):
            reasons.append("INCOMPLETE_OR_INVALID_CANDIDATE_FOLDS")
            break
    if reasons:
        return ThresholdAdjudication(
            status="THRESHOLD_NOT_IDENTIFIED",
            selected_threshold_q=None,
            selected_mean_log_loss=None,
            no_threshold_mean_log_loss=None,
            lower_neighbor_q=None,
            upper_neighbor_q=None,
            lower_paired_mean_difference=None,
            upper_paired_mean_difference=None,
            lower_paired_se=None,
            upper_paired_se=None,
            reasons=tuple(reasons),
        )

    means = {q: _mean(candidate_losses[q]) for q in FROZEN_Q_GRID}
    selected = min(FROZEN_Q_GRID, key=lambda q: (means[q], q))
    idx = FROZEN_Q_GRID.index(selected)
    no_mean = _mean([float(x) for x in no_threshold_losses])

    if idx == 0 or idx == len(FROZEN_Q_GRID) - 1:
        reasons.append("BEST_THRESHOLD_IS_GRID_ENDPOINT")
        return ThresholdAdjudication(
            status="THRESHOLD_NOT_IDENTIFIED",
            selected_threshold_q=selected,
            selected_mean_log_loss=means[selected],
            no_threshold_mean_log_loss=no_mean,
            lower_neighbor_q=None,
            upper_neighbor_q=None,
            lower_paired_mean_difference=None,
            upper_paired_mean_difference=None,
            lower_paired_se=None,
            upper_paired_se=None,
            reasons=tuple(reasons),
        )

    lower = FROZEN_Q_GRID[idx - 1]
    upper = FROZEN_Q_GRID[idx + 1]
    lower_diff, lower_se = _paired_difference_summary(
        candidate_losses[lower],
        candidate_losses[selected],
    )
    upper_diff, upper_se = _paired_difference_summary(
        candidate_losses[upper],
        candidate_losses[selected],
    )

    if not means[selected] < no_mean:
        reasons.append("DOES_NOT_BEAT_NO_THRESHOLD")
    if not lower_diff > lower_se:
        reasons.append("LOWER_ADJACENT_TIED_WITHIN_1SE")
    if not upper_diff > upper_se:
        reasons.append("UPPER_ADJACENT_TIED_WITHIN_1SE")

    return ThresholdAdjudication(
        status=(
            "SUPPORTED_BEHAVIORAL_THRESHOLD_LIKE"
            if not reasons
            else "THRESHOLD_NOT_IDENTIFIED"
        ),
        selected_threshold_q=selected,
        selected_mean_log_loss=means[selected],
        no_threshold_mean_log_loss=no_mean,
        lower_neighbor_q=lower,
        upper_neighbor_q=upper,
        lower_paired_mean_difference=lower_diff,
        upper_paired_mean_difference=upper_diff,
        lower_paired_se=lower_se,
        upper_paired_se=upper_se,
        reasons=tuple(reasons),
    )



def dual_cluster_direction_supported(
    estimate: float,
    individual_ci_low: float,
    context_year_ci_low: float,
) -> bool:
    """Primary directional support requires both clustered CIs above zero."""

    values = (
        float(estimate),
        float(individual_ci_low),
        float(context_year_ci_low),
    )
    if any(not isfinite(v) for v in values):
        raise ValueError("primary inference inputs must be finite")
    return values[0] > 0.0 and values[1] > 0.0 and values[2] > 0.0
