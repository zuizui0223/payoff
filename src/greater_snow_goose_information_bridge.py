"""Published-input bridge for greater snow goose information deadlines.

The calculations are deliberately descriptive.  They reconstruct two ingredients
that exist in the same ecological lineage without pretending that captivity
duration is the PAYOFF-B opportunity cost D or that temperature correlation is
observed cue use.
"""

from __future__ import annotations

from math import asin, exp, isfinite, pi


def gaussian_binary_accuracy(rho: float) -> float:
    """Map a centered Gaussian correlation to binary sign agreement.

    q = 0.5 + asin(rho) / pi

    This is a model-conditional bridge used elsewhere in PAYOFF-B.  It is not
    an empirical classification accuracy unless the Gaussian/sign assumptions
    are justified.
    """

    r = float(rho)
    if not isfinite(r) or not -1.0 <= r <= 1.0:
        raise ValueError("rho must lie in [-1, 1]")
    return 0.5 + asin(r) / pi


def logistic_probability(intercept: float, slope: float, exposure: float) -> float:
    """Probability under a one-predictor logistic model."""

    eta = float(intercept) + float(slope) * float(exposure)
    if not isfinite(eta):
        raise ValueError("non-finite linear predictor")
    return 1.0 / (1.0 + exp(-eta))


def perturbation_cost_on_probability_scale(
    intercept: float,
    slope: float,
    *,
    baseline_days: float = 0.0,
    delayed_days: float = 4.0,
) -> tuple[float, float, float, float]:
    """Translate published logit coefficients to a descriptive probability drop.

    Returns baseline probability, delayed probability, absolute drop, and
    relative drop.  This is a perturbation-cost calibration, not PAYOFF-B D.
    """

    if delayed_days < baseline_days:
        raise ValueError("delayed_days must be >= baseline_days")
    p0 = logistic_probability(intercept, slope, baseline_days)
    p1 = logistic_probability(intercept, slope, delayed_days)
    absolute_drop = p0 - p1
    relative_drop = 0.0 if p0 == 0.0 else absolute_drop / p0
    return p0, p1, absolute_drop, relative_drop


def context_specific_wait_threshold(
    max_prior_action_loss: float,
    total_prior_loss: float,
    context_delay_cost: float,
) -> float:
    """Exact PAYOFF-B threshold if a context-specific D is independently known.

    This is a theory utility.  The snow-goose perturbation coefficients are not
    automatically valid inputs because captivity duration mixes delay and stress.
    """

    m = float(max_prior_action_loss)
    s = float(total_prior_loss)
    d = float(context_delay_cost)
    if not all(isfinite(x) for x in (m, s, d)):
        raise ValueError("inputs must be finite")
    if s <= 0.0 or m < 0.0 or d < 0.0:
        raise ValueError("loss scale must be positive and costs non-negative")
    q = (m + d) / s
    if not 0.0 <= q <= 1.0:
        raise ValueError("threshold falls outside [0,1]")
    return q


def threshold_shift_from_context_cost(
    lower_context_cost: float,
    higher_context_cost: float,
    total_prior_loss: float,
) -> float:
    """Exact threshold shift induced by a known context-dependent delay cost."""

    low = float(lower_context_cost)
    high = float(higher_context_cost)
    scale = float(total_prior_loss)
    if not all(isfinite(x) for x in (low, high, scale)):
        raise ValueError("inputs must be finite")
    if low < 0.0 or high < low or scale <= 0.0:
        raise ValueError("require 0 <= lower <= higher and positive loss scale")
    return (high - low) / scale
