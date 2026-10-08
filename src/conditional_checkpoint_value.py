"""Exact Gaussian cue increment and bounded quadratic control for PAYOFF-B.

Prospective extension to sequential_information_refresh; no analysis of
existing goose outcomes. The target seasonal state is N(0,1).

Z_0=X_0+noise_0 is known at initial commitment; Z_m=X_m+noise_m
is a fresh, independent-noise checkpoint observation. The latent X_j form a
standardized Gaussian Markov chain with neighboring correlations rho_j.

We compute the INCREMENTAL squared predictive correlation (posterior
variance reduction), not only the checkpoint's standalone correlation. A
quadratic payoff with costly, bounded timing adjustment then gives the
exact ex-ante benefit of the information that remains actionable.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import erf, erfc, exp, isfinite, pi, sqrt
from typing import Sequence


@dataclass(frozen=True)
class ConditionalCueValue:
    """All R-squared values are with respect to unit-variance terminal X_n."""

    origin_r2: float
    refreshed_r2: float
    incremental_r2: float
    standalone_checkpoint_r2: float


@dataclass(frozen=True)
class CommitmentComparison:
    """Expected gain of deferring timing commitment relative to acting now."""

    initial_optimal_gain: float
    later_optimal_gain: float
    direct_delay_cost: float
    net_waiting_gain: float
    defer_commitment: bool


def _numbers(rhos: Sequence[float]) -> tuple[float, ...]:
    vals = tuple(float(value) for value in rhos)
    if not vals or any(not isfinite(v) or abs(v) > 1 for v in vals):
        raise ValueError("rhos must contain finite link correlations in [-1, 1]")
    return vals


def _nonnegative_finite(name: str, value: float) -> float:
    v = float(value)
    if not isfinite(v) or v < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return v


def conditional_cue_information(
    rhos: Sequence[float],
    checkpoint: int,
    *,
    origin_noise_variance: float = 0.0,
    checkpoint_noise_variance: float = 0.0,
) -> ConditionalCueValue:
    """R²(X_n | Z_0), R²(X_n | Z_0,Z_m), and their difference.

    No biological use of these cues is assumed. Measurement noises are
    independent Gaussian, zero-mean, and independent of the Markov chain.
    m=0 is allowed, representing an additional *independent-noise* measurement
    of the same initial state. Singular perfect duplicates yield zero gain.
    """
    vals = _numbers(rhos)
    if type(checkpoint) is not int or not 0 <= checkpoint <= len(vals):
        raise ValueError("checkpoint must be an integer in [0, len(rhos)]")
    n0 = _nonnegative_finite("origin_noise_variance", origin_noise_variance)
    nm = _nonnegative_finite("checkpoint_noise_variance", checkpoint_noise_variance)

    a, b = 1.0, 1.0
    for v in vals[:checkpoint]:
        a *= v
    for v in vals[checkpoint:]:
        b *= v

    v0 = 1.0 + n0
    vm = 1.0 + nm
    # Posterior mean is a Gaussian projection. Incremental predictive R²
    # equals squared partial covariance / conditional cue variance.
    initial_r2 = (a * b) ** 2 / v0
    residual_cue_variance = vm - a * a / v0
    partial_covariance = b * (1.0 - a * a / v0)
    if residual_cue_variance < -1e-12:
        raise ArithmeticError("invalid conditional cue variance")
    if residual_cue_variance <= 1e-14:
        if abs(partial_covariance) > 1e-10:
            raise ArithmeticError("singular cue with nonzero partial covariance")
        added = 0.0
    else:
        added = partial_covariance ** 2 / residual_cue_variance
    refreshed_r2 = initial_r2 + added
    if refreshed_r2 > 1.0 + 1e-10:
        raise ArithmeticError("posterior explained variance exceeded one")
    return ConditionalCueValue(
        origin_r2=max(0.0, min(1.0, initial_r2)),
        refreshed_r2=max(0.0, min(1.0, refreshed_r2)),
        incremental_r2=max(0.0, added),
        standalone_checkpoint_r2=b * b / vm,
    )


def optimal_control_gain(
    predictive_r2: float,
    *,
    timing_adjustment_limit: float,
    effort_penalty: float = 0.0,
) -> float:
    """Exact ex-ante gain for loss (X_n - a)^2 + penalty*a^2.

    With a Gaussian conditional mean mu~N(0,predictive_r2), the optimal
    intervention is clip(mu/(1+penalty), -limit, limit).  The returned gain
    is reduction in expected loss versus a=0, before observing a cue.
    Timing units are standardized to the variance of the target seasonal
    state; 'limit' is a genuine feasible adjustment bound, not an R proxy.
    """
    v = float(predictive_r2)
    if not isfinite(v) or not 0.0 <= v <= 1.0:
        raise ValueError("predictive_r2 must lie in [0, 1]")
    limit = _nonnegative_finite("timing_adjustment_limit", timing_adjustment_limit)
    penalty = _nonnegative_finite("effort_penalty", effort_penalty)
    if v == 0.0 or limit == 0.0:
        return 0.0
    k = 1.0 + penalty
    s = sqrt(v)
    t = k * limit / s
    # For W~N(0,1), P(|W|>t)=erfc(t/sqrt(2)).
    tail = erfc(t / sqrt(2.0))
    phi = exp(-0.5 * t * t) / sqrt(2.0 * pi)
    gain = (v / k) * erf(t / sqrt(2.0)) + 2.0 * limit * s * phi - k * limit * limit * tail
    return max(0.0, min(v / k, gain))


def additional_cue_action_value(
    information: ConditionalCueValue,
    *,
    timing_adjustment_limit: float,
    effort_penalty: float = 0.0,
) -> float:
    """Added Bayes benefit of Z_m given Z_0 at identical control capacity."""
    before = optimal_control_gain(
        information.origin_r2,
        timing_adjustment_limit=timing_adjustment_limit,
        effort_penalty=effort_penalty,
    )
    after = optimal_control_gain(
        information.refreshed_r2,
        timing_adjustment_limit=timing_adjustment_limit,
        effort_penalty=effort_penalty,
    )
    if after + 1e-12 < before:
        raise ArithmeticError("additional information decreased Bayes value")
    return max(0.0, after - before)


def compare_commitment_times(
    information: ConditionalCueValue,
    *,
    initial_timing_adjustment_limit: float,
    later_timing_adjustment_limit: float,
    direct_delay_cost: float = 0.0,
    effort_penalty: float = 0.0,
) -> CommitmentComparison:
    """Compare commitment now (Z_0) versus later (Z_0,Z_m).

    Both options receive their respective exogenously feasible timing bounds;
    the focal action is selected only once. Delay cost is nonrecoverable and
    expressed in the same expected-loss units. Strict tie rule acts now.
    Does not infer actionability from observed birds' timing slopes.
    """
    delay = _nonnegative_finite("direct_delay_cost", direct_delay_cost)
    early = optimal_control_gain(
        information.origin_r2,
        timing_adjustment_limit=initial_timing_adjustment_limit,
        effort_penalty=effort_penalty,
    )
    late = optimal_control_gain(
        information.refreshed_r2,
        timing_adjustment_limit=later_timing_adjustment_limit,
        effort_penalty=effort_penalty,
    )
    net = late - early - delay
    return CommitmentComparison(early, late, delay, net, net > 0.0)


@dataclass(frozen=True)
class CheckpointUpdate:
    """A checkpoint forecast innovation and two *counterfactual* timing plans."""

    origin_prediction: float
    checkpoint_innovation: float
    innovation_sensitivity: float
    refreshed_prediction: float
    origin_plan: float
    refreshed_plan: float


def checkpoint_plan_update(
    rhos: Sequence[float],
    checkpoint: int,
    *,
    observed_origin: float,
    observed_checkpoint: float,
    origin_noise_variance: float = 0.0,
    checkpoint_noise_variance: float = 0.0,
    timing_adjustment_limit: float,
    effort_penalty: float = 0.0,
) -> CheckpointUpdate:
    """Posterior mean update from the *unexpected* part of a new cue.

    The two plans use the SAME feasible timing action set to isolate the cue
    update. They are not evidence that a wild bird actually changes course.
    Timing plan revisions require biological reversibility, to be evaluated
    independently at the checkpoint.
    """
    vals = _numbers(rhos)
    info = conditional_cue_information(
        vals, checkpoint,
        origin_noise_variance=origin_noise_variance,
        checkpoint_noise_variance=checkpoint_noise_variance,
    )
    z0 = float(observed_origin)
    zm = float(observed_checkpoint)
    if not isfinite(z0) or not isfinite(zm):
        raise ValueError("observed cues must be finite")
    limit = _nonnegative_finite("timing_adjustment_limit", timing_adjustment_limit)
    penalty = _nonnegative_finite("effort_penalty", effort_penalty)
    a, b = 1.0, 1.0
    for v in vals[:checkpoint]:
        a *= v
    for v in vals[checkpoint:]:
        b *= v
    v0 = 1.0 + origin_noise_variance
    vm = 1.0 + checkpoint_noise_variance
    innovation = zm - (a / v0) * z0
    residual_var = vm - a * a / v0
    cov = b * (1.0 - a * a / v0)
    if residual_var <= 1e-14:
        if abs(innovation) > 1e-10:
            raise ValueError("impossible innovation for identical perfect cues")
        slope = 0.0
    else:
        slope = cov / residual_var
    before = (a * b / v0) * z0
    after = before + slope * innovation
    if residual_var > 1e-14 and abs(slope * slope * residual_var - info.incremental_r2) > 1e-10:
        raise ArithmeticError("innovation variance does not match R² increment")
    def plan(mean: float) -> float:
        return min(limit, max(-limit, mean / (1.0 + penalty)))
    return CheckpointUpdate(before, innovation, slope, after, plan(before), plan(after))
