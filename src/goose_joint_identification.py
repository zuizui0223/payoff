"""Joint identification of environmental predictability and observed recourse.

This prospective PAYOFF-B module is intentionally empirical and conservative.

It separates two quantities that must not be inferred from the same timing
outcome:

1. environmental predictive skill between consecutive seasonal stages;
2. remaining temporal recourse estimated from observed downstream component
   durations.

The motivating public system is the barnacle-goose flyway data associated with
Kölzsch et al. (2015), but the functions are generic.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Sequence


_TOL = 1e-12


def _finite_sequence(name: str, values: Sequence[float]) -> tuple[float, ...]:
    out = tuple(float(x) for x in values)
    if not out:
        raise ValueError(f"{name} must be non-empty")
    if any(not isfinite(x) for x in out):
        raise ValueError(f"{name} must contain finite values")
    return out


def _quantile(values: Sequence[float], probability: float) -> float:
    xs = sorted(float(x) for x in values)
    if not xs:
        raise ValueError("quantile requires non-empty values")
    p = float(probability)
    if not 0.0 <= p <= 1.0:
        raise ValueError("quantile probability must lie in [0, 1]")
    if len(xs) == 1:
        return xs[0]
    position = p * (len(xs) - 1)
    lo = int(position)
    hi = min(lo + 1, len(xs) - 1)
    weight = position - lo
    return xs[lo] * (1.0 - weight) + xs[hi] * weight


@dataclass(frozen=True)
class PredictiveLink:
    """Predictability of a later seasonal anomaly from the current stage."""

    n_years: int
    pearson_r: float
    regression_slope: float
    intercept: float
    loo_mse: float
    loo_climatology_mse: float
    loo_skill: float
    nonnegative_loo_skill: float


def climate_link_predictability(
    current_stage_anomalies: Sequence[float],
    next_stage_anomalies: Sequence[float],
) -> PredictiveLink:
    """Estimate correlation, slope and leave-one-year-out predictive skill.

    The first two quantities reproduce the type of link statistics used by
    Kölzsch et al. for consecutive stopover regions.

    The leave-one-out score asks a stricter forecasting question. For each
    held-out year, regress next-stage anomaly on current-stage anomaly using
    all other years. Compare squared prediction error with a training-only
    climatology predictor.

        skill = 1 - MSE_linear / MSE_climatology.

    Skill may be negative. nonnegative_loo_skill clips it to [0, 1] only for
    constructing a descriptive actionability coordinate; the raw skill is
    always retained.
    """

    x = _finite_sequence("current_stage_anomalies", current_stage_anomalies)
    y = _finite_sequence("next_stage_anomalies", next_stage_anomalies)
    if len(x) != len(y):
        raise ValueError("anomaly vectors must align")
    if len(x) < 4:
        raise ValueError("at least four years are required")

    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    sxx = sum((v - mean_x) ** 2 for v in x)
    syy = sum((v - mean_y) ** 2 for v in y)
    sxy = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))

    if sxx <= _TOL:
        slope = 0.0
        intercept = mean_y
    else:
        slope = sxy / sxx
        intercept = mean_y - slope * mean_x

    if sxx <= _TOL or syy <= _TOL:
        r = 0.0
    else:
        r = sxy / sqrt(sxx * syy)
        r = max(-1.0, min(1.0, r))

    prediction_errors = []
    climatology_errors = []
    n = len(x)
    for holdout in range(n):
        tx = [x[i] for i in range(n) if i != holdout]
        ty = [y[i] for i in range(n) if i != holdout]
        mx = sum(tx) / len(tx)
        my = sum(ty) / len(ty)
        xx = sum((v - mx) ** 2 for v in tx)
        xy = sum((a - mx) * (b - my) for a, b in zip(tx, ty))
        if xx <= _TOL:
            b1 = 0.0
        else:
            b1 = xy / xx
        b0 = my - b1 * mx
        predicted = b0 + b1 * x[holdout]
        prediction_errors.append((y[holdout] - predicted) ** 2)
        climatology_errors.append((y[holdout] - my) ** 2)

    mse = sum(prediction_errors) / n
    baseline = sum(climatology_errors) / n
    if baseline <= _TOL:
        skill = 0.0
    else:
        skill = 1.0 - mse / baseline

    return PredictiveLink(
        n_years=n,
        pearson_r=r,
        regression_slope=slope,
        intercept=intercept,
        loo_mse=mse,
        loo_climatology_mse=baseline,
        loo_skill=skill,
        nonnegative_loo_skill=max(0.0, min(1.0, skill)),
    )


@dataclass(frozen=True)
class ComponentRecourse:
    """Observed duration envelope for one downstream route component."""

    component_index: int
    component_name: str
    observations: int
    fast_duration: float
    typical_duration: float
    slow_duration: float
    advance_capacity: float
    delay_capacity: float


@dataclass(frozen=True)
class StageRecourse:
    """Remaining observed timing flexibility after one route stage."""

    stage_index: int
    remaining_components: int
    advance_capacity: float
    delay_capacity: float
    advance_fraction: float
    delay_fraction: float


@dataclass(frozen=True)
class RecourseEnvelope:
    """Component envelopes plus cumulative stagewise recourse."""

    lower_quantile: float
    reference_quantile: float
    upper_quantile: float
    components: tuple[ComponentRecourse, ...]
    stages: tuple[StageRecourse, ...]


def observed_recourse_envelope(
    component_duration_samples: Sequence[Sequence[float]],
    *,
    component_names: Sequence[str] | None = None,
    lower_quantile: float = 0.10,
    reference_quantile: float = 0.50,
    upper_quantile: float = 0.90,
) -> RecourseEnvelope:
    """Build a route-stage recourse budget from downstream duration envelopes.

    Each component is a flight leg, stopover, or other timing actuator whose
    duration has been observed repeatedly across tracks.

    For component k:

        advance capacity = typical duration - fast-envelope duration
        delay capacity   = slow-envelope duration - typical duration.

    At stage j, remaining capacity is the sum across components j..end.

    This is deliberately an *actuator-derived* quantity. It does not use final
    arrival-time retention or phenological mismatch, avoiding circular
    inference of recourse from the timing outcome it is meant to explain.

    Fractions are normalized to the total capacity available at stage zero.
    """

    lo = float(lower_quantile)
    mid = float(reference_quantile)
    hi = float(upper_quantile)
    if not (0.0 <= lo <= mid <= hi <= 1.0):
        raise ValueError(
            "quantiles must satisfy 0 <= lower <= reference <= upper <= 1"
        )
    if not component_duration_samples:
        raise ValueError("at least one route component is required")

    if component_names is None:
        names = tuple(f"component_{i}" for i in range(len(component_duration_samples)))
    else:
        names = tuple(str(x) for x in component_names)
        if len(names) != len(component_duration_samples):
            raise ValueError("component_names must align with duration samples")

    components = []
    for index, (name, raw) in enumerate(zip(names, component_duration_samples)):
        values = _finite_sequence(f"duration sample {index}", raw)
        if any(x < 0.0 for x in values):
            raise ValueError("component durations must be non-negative")
        fast = _quantile(values, lo)
        typical = _quantile(values, mid)
        slow = _quantile(values, hi)
        components.append(
            ComponentRecourse(
                component_index=index,
                component_name=name,
                observations=len(values),
                fast_duration=fast,
                typical_duration=typical,
                slow_duration=slow,
                advance_capacity=max(0.0, typical - fast),
                delay_capacity=max(0.0, slow - typical),
            )
        )

    total_advance = sum(row.advance_capacity for row in components)
    total_delay = sum(row.delay_capacity for row in components)

    stages = []
    for stage in range(len(components) + 1):
        remaining = components[stage:]
        advance = sum(row.advance_capacity for row in remaining)
        delay = sum(row.delay_capacity for row in remaining)
        advance_fraction = (
            advance / total_advance if total_advance > _TOL else 0.0
        )
        delay_fraction = delay / total_delay if total_delay > _TOL else 0.0
        stages.append(
            StageRecourse(
                stage_index=stage,
                remaining_components=len(remaining),
                advance_capacity=advance,
                delay_capacity=delay,
                advance_fraction=advance_fraction,
                delay_fraction=delay_fraction,
            )
        )

    return RecourseEnvelope(
        lower_quantile=lo,
        reference_quantile=mid,
        upper_quantile=hi,
        components=tuple(components),
        stages=tuple(stages),
    )


@dataclass(frozen=True)
class JointStageCoordinate:
    """Descriptive product of predictive skill and independent recourse."""

    stage_index: int
    predictive_skill: float
    recourse_fraction: float
    actionable_predictability: float


def joint_predictability_recourse_coordinate(
    predictive_skills: Sequence[float],
    recourse_fractions: Sequence[float],
) -> tuple[JointStageCoordinate, ...]:
    """Combine independent [0,1] predictive-skill and recourse estimates.

    This is a descriptive empirical coordinate

        A_j = Q_j R_j,

    not an assertion that Q_j equals the canonical binary cue accuracy q in
    PAYOFF-B.  Its purpose is to test the qualitative information × recourse
    geometry without forcing climate-correlation statistics onto the binary
    theorem's probability scale.
    """

    qs = tuple(float(x) for x in predictive_skills)
    rs = tuple(float(x) for x in recourse_fractions)
    if len(qs) != len(rs) or not qs:
        raise ValueError("predictive_skills and recourse_fractions must align")
    rows = []
    for stage, (q, r) in enumerate(zip(qs, rs)):
        if not isfinite(q) or not 0.0 <= q <= 1.0:
            raise ValueError("predictive skills must lie in [0, 1]")
        if not isfinite(r) or not 0.0 <= r <= 1.0:
            raise ValueError("recourse fractions must lie in [0, 1]")
        rows.append(
            JointStageCoordinate(
                stage_index=stage,
                predictive_skill=q,
                recourse_fraction=r,
                actionable_predictability=q * r,
            )
        )
    return tuple(rows)



@dataclass(frozen=True)
class RemainingDurationRecourse:
    """Observed recourse envelope from stage-to-destination elapsed durations."""

    stage_index: int
    observations: int
    fast_remaining_duration: float
    typical_remaining_duration: float
    slow_remaining_duration: float
    advance_capacity: float
    delay_capacity: float
    advance_fraction: float
    delay_fraction: float


def remaining_duration_recourse(
    stage_remaining_duration_samples: Sequence[Sequence[float]],
    *,
    lower_quantile: float = 0.10,
    reference_quantile: float = 0.50,
    upper_quantile: float = 0.90,
) -> tuple[RemainingDurationRecourse, ...]:
    """Estimate stagewise recourse from remaining elapsed-time envelopes.

    At stage j, each sample is the elapsed time from departure at that stage to
    arrival at the declared destination/breeding stage for one eligible track.

    This automatically includes realized downstream combinations of:

    - flight/transit duration;
    - stopover compression/extension;
    - stopover skipping;
    - route-specific downstream timing.

    The primary quantities are

        C_adv(j)   = P50(T_remaining,j) - P10(T_remaining,j)
        C_delay(j) = P90(T_remaining,j) - P50(T_remaining,j).

    Fractions are normalized to stage zero.

    Unlike the component-sum construction, the empirical stage capacities are
    not forced to decrease monotonically. Composition, route alternatives or a
    downstream bottleneck may produce local increases. This makes the function
    suitable as a direct empirical test rather than a built-in monotonicity
    assumption.

    Absolute arrival dates or phenological mismatch are not used; only elapsed
    downstream schedule duration enters the capacity estimate.
    """

    lo = float(lower_quantile)
    mid = float(reference_quantile)
    hi = float(upper_quantile)
    if not (0.0 <= lo <= mid <= hi <= 1.0):
        raise ValueError(
            "quantiles must satisfy 0 <= lower <= reference <= upper <= 1"
        )
    if not stage_remaining_duration_samples:
        raise ValueError("at least one stage is required")

    raw_rows = []
    for stage, raw in enumerate(stage_remaining_duration_samples):
        values = _finite_sequence(f"stage remaining durations {stage}", raw)
        if any(x < 0.0 for x in values):
            raise ValueError("remaining durations must be non-negative")
        fast = _quantile(values, lo)
        typical = _quantile(values, mid)
        slow = _quantile(values, hi)
        raw_rows.append(
            (
                stage,
                len(values),
                fast,
                typical,
                slow,
                max(0.0, typical - fast),
                max(0.0, slow - typical),
            )
        )

    base_advance = raw_rows[0][5]
    base_delay = raw_rows[0][6]

    return tuple(
        RemainingDurationRecourse(
            stage_index=stage,
            observations=n,
            fast_remaining_duration=fast,
            typical_remaining_duration=typical,
            slow_remaining_duration=slow,
            advance_capacity=advance,
            delay_capacity=delay,
            advance_fraction=(
                advance / base_advance if base_advance > _TOL else 0.0
            ),
            delay_fraction=(
                delay / base_delay if base_delay > _TOL else 0.0
            ),
        )
        for stage, n, fast, typical, slow, advance, delay in raw_rows
    )
