"""Prospective PAYOFF-B decision-time source gate and blocked-year forecast audit.

Tests forecast availability and incremental held-out environmental prediction,
NOT actual cue uptake, plan revision, or fitness. The unit is one unique
spatial pair per seasonal year; replicating across species is forbidden.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite, sqrt
from typing import Sequence


@dataclass(frozen=True)
class TimedEnvironmentalRecord:
    pair_id: str
    seasonal_year: int
    origin_cue: float
    checkpoint_cue: float
    downstream_onset: float
    origin_available_at: str
    checkpoint_available_at: str
    action_decision_at: str
    downstream_onset_available_at: str
    origin_provenance: str
    checkpoint_provenance: str


@dataclass(frozen=True)
class BlockedForecastResult:
    train_years: tuple[int, ...]
    test_years: tuple[int, ...]
    n_train: int
    n_test: int
    n_spatial_pairs: int
    climatology_mse: float
    origin_mse: float
    refreshed_mse: float
    checkpoint_incremental_gain: float
    origin_mean_error: float
    refreshed_mean_error: float


def _timestamp(value: str) -> datetime:
    try:
        t = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, AttributeError) as exc:
        raise ValueError('timestamps must be parseable ISO-8601') from exc
    if t.tzinfo is None or t.utcoffset() is None:
        raise ValueError('timestamp must contain an explicit UTC offset')
    return t


def validate_decision_time_records(rows: Sequence[TimedEnvironmentalRecord]) -> None:
    """Reject look-ahead information and duplicated species-level pair-years.

    Timestamp means when the cue *value* became computable or delivered, not
    the time a retrospectively summarized season actually began. GDD-jerk
    onset peaks calculated after migration decisions cannot be live cues.
    """
    if not rows:
        raise ValueError('at least one environmental record is required')
    seen: set[tuple[str, int]] = set()
    for record in rows:
        if not isinstance(record.pair_id, str) or not record.pair_id.strip():
            raise ValueError('pair_id must be a nonempty source-defined spatial pair')
        if type(record.seasonal_year) is not int:
            raise ValueError('seasonal_year must be an integer')
        if not isinstance(record.origin_provenance, str) or not isinstance(record.checkpoint_provenance, str) or not record.origin_provenance.strip() or not record.checkpoint_provenance.strip():
            raise ValueError('both cues require stated observational provenance')
        ident = (record.pair_id, record.seasonal_year)
        if ident in seen:
            raise ValueError('duplicate pair-year: shared species rows are not independent')
        seen.add(ident)
        for x in (record.origin_cue, record.checkpoint_cue, record.downstream_onset):
            try:
                valid = isfinite(float(x))
            except (ValueError, TypeError):
                valid = False
            if not valid:
                raise ValueError('observed cue and target values must be finite')
        early = _timestamp(record.origin_available_at)
        next_cue = _timestamp(record.checkpoint_available_at)
        decision = _timestamp(record.action_decision_at)
        future = _timestamp(record.downstream_onset_available_at)
        if not early <= next_cue <= decision < future:
            raise ValueError('cue revealed after decision, invalid chronology, or target leakage')


def _linear_solve(matrix: list[list[float]], target: list[float]) -> list[float]:
    """Partial-pivot Gauss-Jordan solve for a tiny ridge-regularized design."""
    k = len(target)
    aug = [matrix[i][:] + [target[i]] for i in range(k)]
    for j in range(k):
        i_max = max(range(j, k), key=lambda i: abs(aug[i][j]))
        if abs(aug[i_max][j]) < 1e-12:
            raise ValueError('singular forecast fit; choose positive ridge penalty')
        aug[j], aug[i_max] = aug[i_max], aug[j]
        diag = aug[j][j]
        aug[j] = [v / diag for v in aug[j]]
        for i in range(k):
            if i != j:
                factor = aug[i][j]
                aug[i] = [x - factor * y for x, y in zip(aug[i], aug[j])]
    return [row[-1] for row in aug]


@dataclass(frozen=True)
class _FittedModel:
    means: tuple[float, ...]
    scales: tuple[float, ...]
    weights: tuple[float, ...]

    def predict(self, features: Sequence[float]) -> float:
        return self.weights[0] + sum(
            weight * ((value - mean) / scale)
            for weight, value, mean, scale in zip(
                self.weights[1:], features, self.means, self.scales
            )
        )


def _fit_linear(
    features: Sequence[Sequence[float]], target: Sequence[float], ridge: float
) -> _FittedModel:
    if not features or len(features) != len(target):
        raise ValueError('training design must be nonempty and aligned')
    n, p = len(features), len(features[0])
    if n < p + 2:
        raise ValueError('insufficient independent training records')
    means = tuple(sum(row[j] for row in features) / n for j in range(p))
    scales = tuple(
        max(1e-12, sqrt(sum((row[j] - means[j]) ** 2 for row in features) / n))
        for j in range(p)
    )
    z = [
        [1.0] + [(val - means[j]) / scales[j] for j, val in enumerate(row)]
        for row in features
    ]
    gram = [[sum(r[i] * r[j] for r in z) for j in range(p + 1)] for i in range(p + 1)]
    for j in range(1, p + 1):
        gram[j][j] += ridge
    rhs = [sum(r[i] * y for r, y in zip(z, target)) for i in range(p + 1)]
    return _FittedModel(means, scales, tuple(_linear_solve(gram, rhs)))


def heldout_incremental_forecast(
    rows: Sequence[TimedEnvironmentalRecord],
    *,
    train_years: Sequence[int],
    test_years: Sequence[int],
    ridge: float = 0.05,
) -> BlockedForecastResult:
    """Compare origin-only and origin+checkpoint on untouched future years.

    Unweighted unique spatial pair-years are the unit of inference. Paired
    year/pair dependence and uncertainty need independent replication in a
    natural study. Positive point estimates alone are NOT confirmation.
    """
    validate_decision_time_records(rows)
    penalty = float(ridge)
    if not isfinite(penalty) or penalty <= 0:
        raise ValueError('ridge must be a positive finite training-only penalty')
    tr = tuple(sorted(set(train_years)))
    te = tuple(sorted(set(test_years)))
    if not tr or not te or max(tr) >= min(te):
        raise ValueError('training years must strictly precede held-out years')
    train = [r for r in rows if r.seasonal_year in tr]
    test = [r for r in rows if r.seasonal_year in te]
    if len(train) < 6 or len(test) < 2:
        raise ValueError('too few source pair-years for a forecast audit')
    if ({r.seasonal_year for r in train} != set(tr)
            or {r.seasonal_year for r in test} != set(te)):
        raise ValueError('some registered years have zero admitted observations')
    y_train = [r.downstream_onset for r in train]
    y_test = [r.downstream_onset for r in test]
    baseline = sum(y_train) / len(y_train)
    origin_model = _fit_linear([[r.origin_cue] for r in train], y_train, penalty)
    refreshed_model = _fit_linear(
        [[r.origin_cue, r.checkpoint_cue] for r in train], y_train, penalty
    )
    origin_resid = [y - origin_model.predict([r.origin_cue]) for y, r in zip(y_test, test)]
    full_resid = [
        y - refreshed_model.predict([r.origin_cue, r.checkpoint_cue])
        for y, r in zip(y_test, test)
    ]
    origin_mse = sum(e * e for e in origin_resid) / len(test)
    new_mse = sum(e * e for e in full_resid) / len(test)
    baseline_mse = sum((y - baseline) ** 2 for y in y_test) / len(test)
    return BlockedForecastResult(
        train_years=tr, test_years=te,
        n_train=len(train), n_test=len(test),
        n_spatial_pairs=len({r.pair_id for r in train + test}),
        climatology_mse=baseline_mse,
        origin_mse=origin_mse, refreshed_mse=new_mse,
        checkpoint_incremental_gain=origin_mse - new_mse,
        origin_mean_error=sum(origin_resid) / len(test),
        refreshed_mean_error=sum(full_resid) / len(test),
    )


def gaussian_historical_policy_transfer(
    *, earlier_correlation: float, later_correlation: float, later_mean_shift: float
) -> tuple[float, float, float]:
    """Standard Gaussian example: early, transported, late-oracle MSE.

    Historical policy predicts old_rho*X and is frozen. New target is
    H = mean_shift + new_rho*X + sqrt(1-new_rho**2)*independent_noise.
    This illustrates climate calibration drift, NOT biological cue uptake.
    """
    old, new, shift = map(float, (earlier_correlation, later_correlation, later_mean_shift))
    if any(not isfinite(x) for x in (old, new, shift)) or abs(old) > 1 or abs(new) > 1:
        raise ValueError('finite correlations in [-1, 1] and mean shift required')
    early_opt = 1 - old * old
    historical_transferred = shift * shift + (new - old) ** 2 + (1 - new * new)
    new_opt = 1 - new * new
    return early_opt, historical_transferred, new_opt


def positive_connectivity_reversal_threshold(
    *, earlier_correlation: float, later_correlation: float
) -> float:
    """Critical |mean drift| for worse timing despite stronger connectivity.

    Only for 0 < rho_old < rho_new <= 1 and unit-variance Gaussian targets,
    with a historically calibrated forecast rho_old*X used without updating.
    Later-minus-earlier expected squared mismatch equals

        delta**2 - 2*rho_old*(rho_new - rho_old).

    It is strictly positive iff |delta| exceeds the returned threshold.
    """
    old, new = float(earlier_correlation), float(later_correlation)
    if any(not isfinite(x) for x in (old, new)) or not (0 < old < new <= 1):
        raise ValueError('requires 0 < earlier rho < later rho <= 1')
    return sqrt(2 * old * (new - old))
