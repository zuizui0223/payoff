"""Asymmetric ecological phase-cost controller for prospective PAYOFF-B.

The existing symmetric quadratic controller assumes that fitness loss for a
phase error of +d equals that for -d. This module uses the asymmetric
piecewise-linear pinball loss common in decision theory. That mathematics is
standard prior art; its ecological role is a counterexample and falsifiable
sensitivity, *not* a newly identified selection gradient.

Definition:
  e = event_date - FITNESS-optimal event_date.  Positive = late.
  u = calendar-phase correction. Positive u advances event timing (reduces e);
      negative u delays it (increases the remaining phase).
  e_post = e-u.
  C_early is fitness loss per day for e_post<0 (too early).
  C_late is fitness loss per day for e_post>0 (too late).
  Adjustment effort costs 0.5*kappa*u*u.

The posterior for e conditional on the animal's information is Gaussian with
mean mu and standard deviation sigma. The code computes ex-ante *expected
loss*, not survival probability or demonstrated animal cognition.

van Dis et al. (2023) reported mean relative fitness loss rates approximately
14%/day before the experimental peak and 6%/day after it in winter moths.
Those descriptive rates are not rigorously constant slopes or universal
selection coefficients and must not be silently treated as field estimates.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import erf, exp, isfinite, pi, sqrt
from statistics import NormalDist

_SQRT_TWO = sqrt(2.0)
_SQRT_TWO_PI = sqrt(2.0 * pi)


@dataclass(frozen=True)
class AsymmetricTimingResult:
    correction: float
    residual_mean_error: float
    no_correction_expected_loss: float
    chosen_expected_loss: float
    expected_gain: float
    quantile_without_effort: float | None
    early_cost: float
    late_cost: float
    effort_penalty: float


def _valid(name: str, value: float, *, strictly_positive: bool = False) -> float:
    value = float(value)
    if not isfinite(value) or (value <= 0.0 if strictly_positive else value < 0.0):
        raise ValueError(f"{name} must be finite and "
                         + ("positive" if strictly_positive else "nonnegative"))
    return value


def _cdf(z: float) -> float:
    return 0.5 * (1.0 + erf(z / _SQRT_TWO))


def _pdf(z: float) -> float:
    return exp(-z * z / 2.0) / _SQRT_TWO_PI


def expected_asymmetric_loss(
    *,
    phase_mean: float,
    phase_sd: float,
    correction: float,
    early_cost: float,
    late_cost: float,
    effort_penalty: float = 0.0,
) -> float:
    """E[c_early*(u-e)_+ + c_late*(e-u)_+] + kappa*u²/2.

    A resource-centred mean r must first be transformed to fitness phase
    mean r - (fitness-optimal date - resource-marker date).
    """
    mu, u = float(phase_mean), float(correction)
    if not isfinite(mu) or not isfinite(u):
        raise ValueError("phase_mean and correction must be finite")
    sd = _valid("phase_sd", phase_sd)
    ce = _valid("early_cost", early_cost)
    cl = _valid("late_cost", late_cost)
    k = _valid("effort_penalty", effort_penalty)

    if sd == 0.0:
        early = max(0.0, u - mu)
        late = max(0.0, mu - u)
    else:
        z = (u - mu) / sd
        prob = _cdf(z)
        density = _pdf(z)
        early = (u - mu) * prob + sd * density
        late = (mu - u) * (1.0 - prob) + sd * density

    return ce * max(0.0, early) + cl * max(0.0, late) + 0.5 * k * u * u


def optimal_asymmetric_timing(
    *,
    phase_mean: float,
    phase_sd: float,
    early_cost: float,
    late_cost: float,
    effort_penalty: float,
    max_delay: float,
    max_advance: float,
) -> AsymmetricTimingResult:
    """Solve a one-decision convex timing loss with asymmetric costs.

    Bounds are independently specified ACTUAL feasible seasonal corrections,
    not inferred from observed phase retention. Zero bounds mean no remaining
    seasonal adjustment. An organism is not assumed to observe the true phase.
    """
    mu = float(phase_mean)
    if not isfinite(mu):
        raise ValueError("phase_mean must be finite")
    sd = _valid("phase_sd", phase_sd)
    ce = _valid("early_cost", early_cost)
    cl = _valid("late_cost", late_cost)
    k = _valid("effort_penalty", effort_penalty)
    delay = _valid("max_delay", max_delay)
    advance = _valid("max_advance", max_advance)
    low, high = -delay, advance

    q = cl / (ce + cl) if ce + cl > 0.0 else None
    if (low == high) or (ce + cl == 0.0):
        action = 0.0
    elif sd == 0.0:
        if k == 0.0:
            action = max(low, min(high, mu))
        else:
            unconstrained = max(-ce / k, min(cl / k, mu))
            action = max(low, min(high, unconstrained))
    elif k == 0.0 and q is not None:
        if q <= 0.0:
            action = low
        elif q >= 1.0:
            action = high
        else:
            action = max(low, min(high, NormalDist(mu, sd).inv_cdf(q)))
    else:
        # Derivative: k*u + (ce+cl) F_e(u) - cl.
        # Strictly increasing for k>0 or for sd>0 with ce+cl>0.
        def derivative(u: float) -> float:
            return k * u + (ce + cl) * _cdf((u - mu) / sd) - cl

        if derivative(low) >= 0.0:
            action = low
        elif derivative(high) <= 0.0:
            action = high
        else:
            left, right = low, high
            for _ in range(90):
                mid = (left + right) / 2.0
                if derivative(mid) < 0.0:
                    left = mid
                else:
                    right = mid
            action = (left + right) / 2.0

    base = expected_asymmetric_loss(
        phase_mean=mu, phase_sd=sd, correction=0.0,
        early_cost=ce, late_cost=cl, effort_penalty=k,
    )
    risk = expected_asymmetric_loss(
        phase_mean=mu, phase_sd=sd, correction=action,
        early_cost=ce, late_cost=cl, effort_penalty=k,
    )
    if risk > base + 1e-10:
        raise ArithmeticError("optimal action worsens risk despite zero feasible")
    return AsymmetricTimingResult(
        correction=action,
        residual_mean_error=mu - action,
        no_correction_expected_loss=base,
        chosen_expected_loss=risk,
        expected_gain=max(0.0, base - risk),
        quantile_without_effort=q,
        early_cost=ce, late_cost=cl, effort_penalty=k,
    )


def resource_to_fitness_phase(resource_relative_phase: float,
                              fitness_target_offset: float) -> float:
    """Convert green-up-centred mismatch to the assumed fitness-centred error."""
    resource, offset = float(resource_relative_phase), float(fitness_target_offset)
    if not isfinite(resource) or not isfinite(offset):
        raise ValueError("phase and offset must be finite")
    return resource - offset
