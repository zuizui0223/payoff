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


@dataclass(frozen=True)
class PopulationVarianceStep:
    """Across-individual phase-variance propagation for one checkpoint."""

    prior_variance: float
    observation_variance: float
    kalman_gain: float
    control_gain: float
    passive_retention: float
    process_variance: float
    posterior_error_variance: float
    posterior_mean_variance: float
    prepropagation_residual_variance: float
    closed_loop_variance_multiplier: float
    next_variance: float


@dataclass(frozen=True)
class StationaryPhaseVariance:
    """Positive stationary variance of the homogeneous Gaussian controller."""

    observation_variance: float
    control_gain: float
    passive_retention: float
    process_variance: float
    quadratic_a: float
    quadratic_b: float
    stationary_variance: float



@dataclass(frozen=True)
class PhaseSenseInverse:
    """Information weight inferred from mean and variance phase retention."""

    prior_variance: float
    next_variance: float
    process_variance: float
    passive_retention: float
    mean_phase_retention: float
    innovation_adjusted_variance_ratio: float
    inferred_information_weight: float
    inferred_observation_variance: float | None

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


def population_phase_variance_step(
    prior_variance: float,
    *,
    observation_variance: float,
    control_gain: float,
    passive_retention: float = 1.0,
    process_variance: float = 0.0,
) -> PopulationVarianceStep:
    """Propagate across-individual phase variance under individual feedback.

    Let latent incoming phase error have variance P and checkpoint observation

        Z = E + noise,   Var(noise)=R.

    The posterior mean is used for proportional correction

        u = g E[E | Z].

    For the scalar Gaussian model,

        K = P/(P+R),
        Var(E | Z) = (1-K)P,
        Var(E[E|Z]) = K P.

    The unconditional residual variance after individualized correction is

        P_res
          = (1-K)P + (1-g)^2 K P
          = P [1 - K g(2-g)].

    After passive propagation and independent process innovation Q,

        P_next
          = phi^2 P [1 - K g(2-g)] + Q.

    A common open-loop correction that does not depend on individual phase has
    no corresponding K*g(2-g) term, so its across-individual variance is simply
    phi^2 P + Q.  This makes excess variance contraction a functional
    fingerprint of individual state-dependent feedback.

    The formula assumes unclipped proportional control.  It is standard
    Gaussian feedback algebra, not a generic ecological theorem.
    """

    p = _nonnegative("prior_variance", prior_variance)
    r = _nonnegative("observation_variance", observation_variance)
    g = _nonnegative("control_gain", control_gain)
    phi = _finite("passive_retention", passive_retention)
    qvar = _nonnegative("process_variance", process_variance)

    if p <= _TOL:
        k = 0.0
        post_error = 0.0
        estimate_var = 0.0
        residual = 0.0
        multiplier = phi**2
        next_var = qvar
    else:
        k = 1.0 if r <= _TOL else p / (p + r)
        post_error = (1.0 - k) * p
        estimate_var = k * p
        residual = post_error + (1.0 - g) ** 2 * estimate_var
        multiplier = phi**2 * (1.0 - k * g * (2.0 - g))
        next_var = phi**2 * residual + qvar

    return PopulationVarianceStep(
        prior_variance=p,
        observation_variance=r,
        kalman_gain=k,
        control_gain=g,
        passive_retention=phi,
        process_variance=qvar,
        posterior_error_variance=post_error,
        posterior_mean_variance=estimate_var,
        prepropagation_residual_variance=residual,
        closed_loop_variance_multiplier=multiplier,
        next_variance=next_var,
    )


def open_loop_phase_variance_step(
    prior_variance: float,
    *,
    passive_retention: float = 1.0,
    process_variance: float = 0.0,
) -> float:
    """Across-individual variance after a common phase-independent correction."""

    p = _nonnegative("prior_variance", prior_variance)
    phi = _finite("passive_retention", passive_retention)
    qvar = _nonnegative("process_variance", process_variance)
    return phi**2 * p + qvar


def stationary_gaussian_phase_variance(
    *,
    observation_variance: float,
    control_gain: float,
    passive_retention: float = 1.0,
    process_variance: float,
) -> StationaryPhaseVariance:
    """Closed-form positive stationary variance for homogeneous checkpoints.

    With constant observation variance R, process innovation Q, passive
    retention phi and control gain g, the variance recursion is

        P_next
          = phi^2 [P - g(2-g) P^2/(P+R)] + Q.

    A finite positive stationary variance exists under the asymptotic
    closed-loop stability condition

        |phi(1-g)| < 1.

    The fixed point solves

        A P^2 + B P - Q R = 0,

    where

        A = 1 - phi^2(1-g)^2,
        B = R(1-phi^2) - Q.

    The returned root is the non-negative solution.
    """

    r = _nonnegative("observation_variance", observation_variance)
    g = _nonnegative("control_gain", control_gain)
    phi = _finite("passive_retention", passive_retention)
    qvar = _nonnegative("process_variance", process_variance)

    a = 1.0 - phi**2 * (1.0 - g) ** 2
    if a <= _TOL:
        raise ValueError(
            "finite stationary variance requires |passive_retention * "
            "(1-control_gain)| < 1"
        )
    b = r * (1.0 - phi**2) - qvar
    disc = b * b + 4.0 * a * qvar * r
    pstar = (-b + disc**0.5) / (2.0 * a)
    if pstar < 0.0 and pstar > -1e-10:
        pstar = 0.0

    return StationaryPhaseVariance(
        observation_variance=r,
        control_gain=g,
        passive_retention=phi,
        process_variance=qvar,
        quadratic_a=a,
        quadratic_b=b,
        stationary_variance=pstar,
    )


def variance_retention_from_mean_phase(
    *,
    passive_retention: float,
    mean_phase_retention: float,
    information_weight: float,
) -> float:
    """Return innovation-free population variance retention.

    Combining

        lambda = phi(1-g)

    with the variance-funnel recursion gives

        (P_next-Q)/P
          = phi^2 [1-K g(2-g)]
          = (1-K) phi^2 + K lambda^2.

    Thus variance retention is a convex combination of the passive squared
    retention and the squared closed-loop mean retention, weighted by the
    effective information weight K.
    """

    phi = _finite("passive_retention", passive_retention)
    lam = _finite("mean_phase_retention", mean_phase_retention)
    k = _finite("information_weight", information_weight)
    if not 0.0 <= k <= 1.0:
        raise ValueError("information_weight must lie in [0,1]")
    return (1.0 - k) * phi**2 + k * lam**2


def infer_phase_information_weight(
    prior_variance: float,
    next_variance: float,
    *,
    process_variance: float,
    passive_retention: float,
    mean_phase_retention: float,
    tolerance: float = 1e-10,
) -> PhaseSenseInverse:
    """Infer effective checkpoint information weight from a variance funnel.

    Under the unclipped Gaussian controller,

        rho_V = (P_next-Q)/P
              = (1-K) phi^2 + K lambda^2.

    If phi^2 != lambda^2,

        K = [phi^2-rho_V] / [phi^2-lambda^2].

    With K=P/(P+R), the equivalent observation variance is

        R = P(1-K)/K.

    The inverse requires an independently justified passive retention phi and
    process variance Q.  It must not be used by setting phi from the same
    closed-loop transition being explained.

    If the inferred K lies outside [0,1] beyond tolerance, the declared
    Gaussian feedback model is incompatible with the supplied moments.
    """

    p = _nonnegative("prior_variance", prior_variance)
    pnext = _nonnegative("next_variance", next_variance)
    qvar = _nonnegative("process_variance", process_variance)
    phi = _finite("passive_retention", passive_retention)
    lam = _finite("mean_phase_retention", mean_phase_retention)
    tol = _nonnegative("tolerance", tolerance)

    if p <= _TOL:
        raise ValueError("prior_variance must be positive for the inverse")

    rho = (pnext - qvar) / p
    denom = phi**2 - lam**2
    if abs(denom) <= tol:
        raise ValueError(
            "information weight is not identified when passive and mean "
            "squared retention are equal"
        )

    k = (phi**2 - rho) / denom
    if k < -tol or k > 1.0 + tol:
        raise ValueError(
            "supplied mean/variance moments imply information weight outside "
            "[0,1] under the declared model"
        )
    k = min(max(k, 0.0), 1.0)

    if k <= tol:
        obs_var = None
    else:
        obs_var = p * (1.0 - k) / k

    return PhaseSenseInverse(
        prior_variance=p,
        next_variance=pnext,
        process_variance=qvar,
        passive_retention=phi,
        mean_phase_retention=lam,
        innovation_adjusted_variance_ratio=rho,
        inferred_information_weight=k,
        inferred_observation_variance=obs_var,
    )
