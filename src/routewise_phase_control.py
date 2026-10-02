"""Route-wise Bayesian phase control for seasonal movement.

Prospective PAYOFF-B extension.  This module does not alter the frozen Paper-2
submission.  It formalizes the "Shinkansen to Schroedinger's spring" intuition:
an organism moves through route checkpoints, updates an internal estimate of
seasonal phase error, and uses the remaining speed/stopover/route recourse to
correct that error before the next checkpoint.

The mathematics is standard scalar Bayesian filtering / feedback control.  The
PAYOFF-B contribution is the ecological decomposition and its connection to
phase-retention lambda, information quality, and shrinking actionability.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence


_TOL = 1e-12


@dataclass(frozen=True)
class GaussianPhaseBelief:
    """Posterior belief about signed seasonal phase error."""

    prior_mean: float
    prior_variance: float
    observation: float
    observation_variance: float
    kalman_gain: float
    posterior_mean: float
    posterior_variance: float


@dataclass(frozen=True)
class QuadraticCorrection:
    """One-checkpoint correction chosen from a posterior phase belief."""

    posterior_mean: float
    posterior_variance: float
    control_weight: float
    residual_weight: float
    unconstrained_gain: float
    unconstrained_correction: float
    correction: float
    expected_loss: float
    mode: str


@dataclass(frozen=True)
class PhaseStep:
    """One realized route step under proportional phase feedback."""

    phase_error: float
    estimated_phase_error: float
    control_gain: float
    correction: float
    residual_before_propagation: float
    passive_retention: float
    route_shift: float
    next_phase_error: float
    unclipped_closed_loop_lambda: float
    mode: str


@dataclass(frozen=True)
class RouteCheckpoint:
    """Recorded checkpoint state for a Gaussian feedback route."""

    stage: int
    true_phase_error: float
    prior_mean: float
    prior_variance: float
    observation: float
    observation_variance: float
    posterior_mean: float
    posterior_variance: float
    correction: float
    next_true_phase_error: float
    next_prior_mean: float
    next_prior_variance: float


def _finite(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _nonnegative(name: str, value: float) -> float:
    x = _finite(name, value)
    if x < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return x


def gaussian_phase_update(
    prior_mean: float,
    prior_variance: float,
    observation: float,
    observation_variance: float,
) -> GaussianPhaseBelief:
    """Exact scalar Gaussian update for signed phase error.

    The latent phase error is E ~ N(m, P), and the checkpoint cue is

        Z = E + noise,  noise ~ N(0, R).

    The posterior mean is the animal's control-relevant estimate of whether it
    is early (negative) or late (positive).  The formula is standard Bayesian
    filtering; it is not a new theorem.
    """

    m = _finite("prior_mean", prior_mean)
    p = _nonnegative("prior_variance", prior_variance)
    z = _finite("observation", observation)
    r = _nonnegative("observation_variance", observation_variance)

    if p <= _TOL:
        gain = 0.0
        post_mean = m
        post_var = 0.0
    elif r <= _TOL:
        gain = 1.0
        post_mean = z
        post_var = 0.0
    else:
        gain = p / (p + r)
        post_mean = m + gain * (z - m)
        post_var = (1.0 - gain) * p

    return GaussianPhaseBelief(
        prior_mean=m,
        prior_variance=p,
        observation=z,
        observation_variance=r,
        kalman_gain=gain,
        posterior_mean=post_mean,
        posterior_variance=post_var,
    )


def optimal_quadratic_phase_correction(
    posterior_mean: float,
    posterior_variance: float,
    *,
    control_weight: float,
    residual_weight: float,
    advance_capacity: float,
    delay_capacity: float,
) -> QuadraticCorrection:
    """Choose a bounded correction from the posterior phase belief.

    Conditional expected loss is

        kappa * u^2 + mu * E[(E-u)^2 | information]
      = kappa * u^2 + mu * [(m-u)^2 + P].

    Without bounds,

        u* = g m,
        g = mu / (kappa + mu).

    Thus the action depends on the posterior mean, while uncertainty remains as
    irreducible expected residual loss.  Positive u speeds up / compresses
    stopovers; negative u slows down / extends stopovers.
    """

    m = _finite("posterior_mean", posterior_mean)
    p = _nonnegative("posterior_variance", posterior_variance)
    kappa = _nonnegative("control_weight", control_weight)
    mu = _nonnegative("residual_weight", residual_weight)
    advance = _nonnegative("advance_capacity", advance_capacity)
    delay = _nonnegative("delay_capacity", delay_capacity)

    denom = kappa + mu
    gain = 0.0 if denom <= _TOL else mu / denom
    raw = gain * m
    correction = min(max(raw, -delay), advance)
    loss = kappa * correction**2 + mu * ((m - correction) ** 2 + p)

    if correction > _TOL:
        mode = "speed_up_or_compress"
    elif correction < -_TOL:
        mode = "slow_or_wait"
    else:
        mode = "none"

    return QuadraticCorrection(
        posterior_mean=m,
        posterior_variance=p,
        control_weight=kappa,
        residual_weight=mu,
        unconstrained_gain=gain,
        unconstrained_correction=raw,
        correction=correction,
        expected_loss=loss,
        mode=mode,
    )


def proportional_phase_step(
    phase_error: float,
    estimated_phase_error: float,
    *,
    control_gain: float,
    passive_retention: float = 1.0,
    route_shift: float = 0.0,
    advance_capacity: float,
    delay_capacity: float,
) -> PhaseStep:
    """Propagate one checkpoint of signed phase error.

    The controller is

        u_t = clip(g_t * ehat_t, -C_delay, C_advance)

    and route phase evolves as

        e_(t+1) = phi_t * (e_t - u_t) + w_t.

    Here phi_t is passive phase retention in the absence of active correction,
    while w_t is a shift in the local seasonal target between checkpoints.

    Under perfect estimation, no clipping, and w_t=0,

        e_(t+1) = lambda_t e_t,
        lambda_t = phi_t (1-g_t).

    This gives an exact decomposition of observed phase retention into passive
    carry-over and active feedback gain.  It also shows why lambda alone cannot
    identify recourse or control gain without additional information on phi.
    """

    e = _finite("phase_error", phase_error)
    est = _finite("estimated_phase_error", estimated_phase_error)
    gain = _nonnegative("control_gain", control_gain)
    phi = _finite("passive_retention", passive_retention)
    shift = _finite("route_shift", route_shift)
    advance = _nonnegative("advance_capacity", advance_capacity)
    delay = _nonnegative("delay_capacity", delay_capacity)

    raw = gain * est
    correction = min(max(raw, -delay), advance)
    residual = e - correction
    next_error = phi * residual + shift
    closed_lambda = phi * (1.0 - gain)

    if correction > _TOL:
        mode = "speed_up_or_compress"
    elif correction < -_TOL:
        mode = "slow_or_wait"
    else:
        mode = "none"

    return PhaseStep(
        phase_error=e,
        estimated_phase_error=est,
        control_gain=gain,
        correction=correction,
        residual_before_propagation=residual,
        passive_retention=phi,
        route_shift=shift,
        next_phase_error=next_error,
        unclipped_closed_loop_lambda=closed_lambda,
        mode=mode,
    )


def routewise_gaussian_phase_control(
    initial_true_error: float,
    initial_prior_mean: float,
    initial_prior_variance: float,
    observations: Sequence[float],
    observation_variances: Sequence[float],
    *,
    passive_retentions: Sequence[float],
    route_shifts: Sequence[float],
    process_variances: Sequence[float],
    control_weight: float,
    residual_weight: float,
    advance_capacities: Sequence[float],
    delay_capacities: Sequence[float],
) -> tuple[RouteCheckpoint, ...]:
    """Run sequential infer -> correct -> propagate control along a route.

    Each checkpoint:
      1. updates the internal estimate of phase error from a local cue;
      2. chooses a signed speed/stopover correction;
      3. propagates both true error and the belief to the next checkpoint.

    The observation sequence is supplied explicitly so empirical applications
    can use real checkpoint cues without treating model-generated noise as data.
    """

    n = len(observations)
    sequences = (
        observation_variances,
        passive_retentions,
        route_shifts,
        process_variances,
        advance_capacities,
        delay_capacities,
    )
    if any(len(xs) != n for xs in sequences):
        raise ValueError("all route sequences must have the same length")

    true_error = _finite("initial_true_error", initial_true_error)
    prior_mean = _finite("initial_prior_mean", initial_prior_mean)
    prior_var = _nonnegative("initial_prior_variance", initial_prior_variance)

    rows: list[RouteCheckpoint] = []
    for t in range(n):
        belief = gaussian_phase_update(
            prior_mean,
            prior_var,
            observations[t],
            observation_variances[t],
        )
        action = optimal_quadratic_phase_correction(
            belief.posterior_mean,
            belief.posterior_variance,
            control_weight=control_weight,
            residual_weight=residual_weight,
            advance_capacity=advance_capacities[t],
            delay_capacity=delay_capacities[t],
        )

        phi = _finite("passive_retention", passive_retentions[t])
        shift = _finite("route_shift", route_shifts[t])
        qvar = _nonnegative("process_variance", process_variances[t])

        next_true = phi * (true_error - action.correction) + shift
        next_mean = phi * (belief.posterior_mean - action.correction) + shift
        next_var = phi**2 * belief.posterior_variance + qvar

        rows.append(
            RouteCheckpoint(
                stage=t,
                true_phase_error=true_error,
                prior_mean=prior_mean,
                prior_variance=prior_var,
                observation=float(observations[t]),
                observation_variance=float(observation_variances[t]),
                posterior_mean=belief.posterior_mean,
                posterior_variance=belief.posterior_variance,
                correction=action.correction,
                next_true_phase_error=next_true,
                next_prior_mean=next_mean,
                next_prior_variance=next_var,
            )
        )

        true_error = next_true
        prior_mean = next_mean
        prior_var = next_var

    return tuple(rows)
