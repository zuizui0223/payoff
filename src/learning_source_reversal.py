"""Gaussian source-of-information reversal: a prospective PAYOFF-B toy null.

An actor that learned a reliable environmental relation in an earlier period
may lose its prediction advantage over a noisier but freshly calibrated cue
after the environment changes. This is elementary calibration-drift algebra,
not an empirical finding about cranes, learning, or evolutionary fitness.

All forecasts share the SAME unrestricted one-dimensional timing action set,
and have no additional intervention penalty. The fresh source adds an
exogenously specified independent prediction error and information access
cost in expected squared-timing-loss units. If actionability differs, use
the bounded-control model instead; do not read the forecast gap as fitness.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt


@dataclass(frozen=True)
class KnowledgeReversal:
    historical_correlation: float
    current_correlation: float
    seasonal_mean_drift: float
    fresh_source_error_variance: float
    fresh_source_acquisition_cost: float
    baseline_environmental_variance: float
    historical_rule_loss: float
    fresh_rule_loss: float
    net_fresh_advantage: float
    fresh_source_preferred: bool
    historical_rule_was_better_before_shift: bool


def _valid_float(name: str, x: float) -> float:
    try:
        x = float(x)
    except (TypeError, ValueError, OverflowError) as e:
        raise ValueError(f"{name} must be a finite number") from e
    if not isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def compare_learning_sources(
    *,
    historical_correlation: float,
    current_correlation: float,
    seasonal_mean_drift: float,
    fresh_source_error_variance: float,
    fresh_source_acquisition_cost: float = 0.0,
) -> KnowledgeReversal:
    """Compare two actions under H=delta+rho_new*X+sqrt(1-rho_new²)*eps.

    X and eps are independent N(0,1). Historical individual action:
        u_old=rho_old*X.
    Freshly calibrated, independent-noise source action:
        u_fresh=delta+rho_new*X+zeta, zeta~N(0,sigma²).
    The fresh decision incurs additional fixed cost c>=0, expressed in the
    *same squared-timing-loss units*. The information-source labels could
    refer to memory/social cues only IF an empirical study independently
    verifies the relevant mechanism, access dates and noise architecture.

    Loss_old=1-rho_new²+delta²+(rho_new-rho_old)²
    Loss_fresh=1-rho_new²+sigma²+c
    Net fresh advantage=delta²+(rho_new-rho_old)²-sigma²-c
    """
    old = _valid_float("historical_correlation", historical_correlation)
    new = _valid_float("current_correlation", current_correlation)
    drift = _valid_float("seasonal_mean_drift", seasonal_mean_drift)
    variance = _valid_float("fresh_source_error_variance", fresh_source_error_variance)
    cost = _valid_float("fresh_source_acquisition_cost", fresh_source_acquisition_cost)
    if abs(old) > 1 or abs(new) > 1:
        raise ValueError("correlations must lie in [-1, 1]")
    if variance < 0 or cost < 0:
        raise ValueError("source error variance and information cost must be nonnegative")

    noise = 1.0 - new * new
    historic = noise + drift * drift + (new - old) ** 2
    fresh = noise + variance + cost
    advantage = historic - fresh
    # Before the shift the correctly calibrated historical rule has zero
    # extra noise and the hypothetical fresh source still bears variance+cost.
    previous_advantage = variance + cost
    return KnowledgeReversal(
        historical_correlation=old,
        current_correlation=new,
        seasonal_mean_drift=drift,
        fresh_source_error_variance=variance,
        fresh_source_acquisition_cost=cost,
        baseline_environmental_variance=noise,
        historical_rule_loss=historic,
        fresh_rule_loss=fresh,
        net_fresh_advantage=advantage,
        fresh_source_preferred=(advantage > 0),
        historical_rule_was_better_before_shift=(previous_advantage > 0),
    )


def minimum_mean_drift_for_fresh_advantage(
    *,
    historical_correlation: float,
    current_correlation: float,
    fresh_source_error_variance: float,
    fresh_source_acquisition_cost: float = 0.0,
) -> float:
    """Infimum absolute mean drift at which a fresh source can win.

    If correlation drift alone exceeds source uncertainty+cost, return zero.
    At equality, strict preference requires |delta|>0; equality is not a win.
    """
    old = _valid_float("historical_correlation", historical_correlation)
    new = _valid_float("current_correlation", current_correlation)
    v = _valid_float("fresh_source_error_variance", fresh_source_error_variance)
    cost = _valid_float("fresh_source_acquisition_cost", fresh_source_acquisition_cost)
    if abs(old) > 1 or abs(new) > 1 or v < 0 or cost < 0:
        raise ValueError("invalid correlations, source uncertainty or cost")
    return sqrt(max(0.0, v + cost - (new-old)**2))
