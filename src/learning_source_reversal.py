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
        fresh_source_preferred=(drift * drift + (new - old) ** 2 > variance + cost),
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


@dataclass(frozen=True)
class RecalibrationComparison:
    """Partial seasonal policy recalibration; fraction=1 is the current optimum."""

    recalibration_fraction: float
    retained_historical_error_fraction: float
    recalibrated_memory_loss: float
    fresh_rule_loss: float
    fresh_advantage: float
    fresh_source_preferred: bool


def compare_recalibrating_memory(
    *,
    historical_correlation: float,
    current_correlation: float,
    seasonal_mean_drift: float,
    recalibration_fraction: float,
    fresh_source_error_variance: float,
    fresh_source_acquisition_cost: float = 0.0,
) -> RecalibrationComparison:
    """A stored cue model can be updated; old age does not imply stale knowledge.

    An actor's policy is a declared convex blend of old and *correct current*
    forecasts.  Its updated action is
      u_w=(1-w)*rho_old*X + w*(delta+rho_new*X).
    This is a hypothetical updating fraction, not a measured bird-learning
    rate, and knowing the current forecast may itself cost information.
    Fresh source shares the current climate but adds independent forecast
    noise and fixed cost.
    """
    w = _valid_float("recalibration_fraction", recalibration_fraction)
    if not 0 <= w <= 1:
        raise ValueError("recalibration fraction must be within [0,1]")
    frozen = compare_learning_sources(
        historical_correlation=historical_correlation,
        current_correlation=current_correlation,
        seasonal_mean_drift=seasonal_mean_drift,
        fresh_source_error_variance=fresh_source_error_variance,
        fresh_source_acquisition_cost=fresh_source_acquisition_cost,
    )
    retained = (1 - w) ** 2
    mismatch = (
        frozen.seasonal_mean_drift ** 2
        + (frozen.current_correlation - frozen.historical_correlation) ** 2
    )
    old_loss = frozen.baseline_environmental_variance + retained * mismatch
    fresh_loss = frozen.fresh_rule_loss
    advantage = old_loss - fresh_loss
    return RecalibrationComparison(
        recalibration_fraction=w,
        retained_historical_error_fraction=retained,
        recalibrated_memory_loss=old_loss,
        fresh_rule_loss=fresh_loss,
        fresh_advantage=advantage,
        fresh_source_preferred=(
            retained * mismatch
            > frozen.fresh_source_error_variance + frozen.fresh_source_acquisition_cost
        ),
    )
