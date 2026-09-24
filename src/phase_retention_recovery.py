"""Measurement-error recovery diagnostics for PAYOFF-B phase retention.

The ecological tracking model leaves a fraction

    lambda = exp[-(m + h) * dt]

of a pre-existing mismatch after one local correction interval. Empirical phase
retention is estimated from the slope in

    E_next = a + lambda * E_current + error.

If E_current is itself measured with error, ordinary least squares attenuates
the slope toward zero. This module isolates that observation-layer problem from
the ecological tracking simulation.

For latent predictor variance Vx, predictor measurement-error variance Ve,
outcome measurement-error variance Vy_err, and covariance C_err between the
predictor and outcome measurement errors, the large-sample naive slope is

    E[lambda_hat]
      = (lambda * Vx + C_err) / (Vx + Ve).

Independent measurement error has C_err = 0 and therefore creates classical
regression dilution. Positive correlation between phase errors at consecutive
observations can reduce that attenuation.

This module is dependency-free, seed-explicit, and intended for preregistered
parameter-recovery and lambda=1 null simulations. It does not estimate
measurement-error SDs from empirical data and must not be used to invent them.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, sqrt
from random import Random
from statistics import mean, pstdev
from typing import Iterable


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _nonnegative(name: str, value: float) -> float:
    value = _finite(name, value)
    if value < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return value


def lambda_from_tracking_rates(
    migration_rate: float,
    phenology_rate: float,
    *,
    interval_scale: float = 1.0,
) -> float:
    """Return the exact local retained-mismatch fraction.

    This is the observation-layer bridge to the existing tracking model, whose
    correction fraction is 1-exp[-(m+h)] per model step.
    """

    migration_rate = _nonnegative(
        "migration_rate", migration_rate
    )
    phenology_rate = _nonnegative(
        "phenology_rate", phenology_rate
    )
    interval_scale = _finite(
        "interval_scale", interval_scale
    )
    if interval_scale <= 0.0:
        raise ValueError("interval_scale must be positive")
    return exp(
        -(migration_rate + phenology_rate)
        * interval_scale
    )


@dataclass(frozen=True)
class LambdaRecoveryDesign:
    """Frozen observation model for one parameter-recovery experiment."""

    true_lambda: float
    latent_phase_sd: float
    predictor_error_sd: float
    outcome_error_sd: float
    error_correlation: float = 0.0
    process_noise_sd: float = 0.0
    n_pairs: int = 200

    def __post_init__(self) -> None:
        true_lambda = _finite(
            "true_lambda", self.true_lambda
        )
        if abs(true_lambda) > 10.0:
            raise ValueError(
                "true_lambda outside supported diagnostic range"
            )
        if _nonnegative(
            "latent_phase_sd", self.latent_phase_sd
        ) <= 0.0:
            raise ValueError(
                "latent_phase_sd must be positive"
            )
        _nonnegative(
            "predictor_error_sd",
            self.predictor_error_sd,
        )
        _nonnegative(
            "outcome_error_sd",
            self.outcome_error_sd,
        )
        _nonnegative(
            "process_noise_sd",
            self.process_noise_sd,
        )
        correlation = _finite(
            "error_correlation",
            self.error_correlation,
        )
        if not -1.0 <= correlation <= 1.0:
            raise ValueError(
                "error_correlation must lie in [-1,1]"
            )
        if self.n_pairs < 3:
            raise ValueError("n_pairs must be at least 3")

    @property
    def latent_phase_variance(self) -> float:
        return self.latent_phase_sd**2

    @property
    def predictor_error_variance(self) -> float:
        return self.predictor_error_sd**2

    @property
    def error_covariance(self) -> float:
        return (
            self.error_correlation
            * self.predictor_error_sd
            * self.outcome_error_sd
        )

    @property
    def reliability_ratio(self) -> float:
        return (
            self.latent_phase_variance
            / (
                self.latent_phase_variance
                + self.predictor_error_variance
            )
        )


@dataclass(frozen=True)
class LambdaRecoverySummary:
    design: LambdaRecoveryDesign
    replicates: int
    seed: int
    expected_naive_lambda: float
    mean_naive_lambda: float
    sd_naive_lambda: float
    bias: float
    rmse: float
    q025: float
    q50: float
    q975: float
    fraction_below_true_lambda: float


def expected_naive_lambda(
    design: LambdaRecoveryDesign,
) -> float:
    """Large-sample expected naive OLS slope under the frozen error model."""

    denominator = (
        design.latent_phase_variance
        + design.predictor_error_variance
    )
    numerator = (
        design.true_lambda
        * design.latent_phase_variance
        + design.error_covariance
    )
    return numerator / denominator


def fit_naive_lambda(
    phase_before: Iterable[float],
    phase_after: Iterable[float],
) -> float:
    """OLS slope with an intercept, matching the basic lambda estimand."""

    x = tuple(float(value) for value in phase_before)
    y = tuple(float(value) for value in phase_after)
    if len(x) != len(y):
        raise ValueError(
            "phase_before and phase_after must have equal length"
        )
    if len(x) < 3:
        raise ValueError("at least three phase pairs are required")
    if any(not isfinite(value) for value in x + y):
        raise ValueError("phase values must be finite")

    x_bar = mean(x)
    y_bar = mean(y)
    sxx = sum(
        (value - x_bar) ** 2
        for value in x
    )
    if sxx <= 0.0:
        raise ValueError(
            "observed predictor phase has zero variance"
        )
    sxy = sum(
        (x_value - x_bar)
        * (y_value - y_bar)
        for x_value, y_value in zip(x, y)
    )
    return sxy / sxx


def simulate_naive_lambda_once(
    design: LambdaRecoveryDesign,
    *,
    seed: int,
) -> float:
    """Generate one paired dataset and fit the naive lambda slope."""

    rng = Random(seed)
    x_observed: list[float] = []
    y_observed: list[float] = []
    residual_scale = sqrt(
        max(
            0.0,
            1.0 - design.error_correlation**2,
        )
    )

    for _ in range(design.n_pairs):
        x_true = rng.gauss(
            0.0,
            design.latent_phase_sd,
        )
        y_true = (
            design.true_lambda * x_true
            + rng.gauss(
                0.0,
                design.process_noise_sd,
            )
        )

        z_predictor = rng.gauss(0.0, 1.0)
        z_outcome_independent = rng.gauss(
            0.0, 1.0
        )
        predictor_error = (
            design.predictor_error_sd
            * z_predictor
        )
        outcome_error = (
            design.outcome_error_sd
            * (
                design.error_correlation
                * z_predictor
                + residual_scale
                * z_outcome_independent
            )
        )

        x_observed.append(
            x_true + predictor_error
        )
        y_observed.append(
            y_true + outcome_error
        )

    return fit_naive_lambda(
        x_observed,
        y_observed,
    )


def _quantile(
    values: tuple[float, ...],
    probability: float,
) -> float:
    if not values:
        raise ValueError("quantile requires values")
    if not 0.0 <= probability <= 1.0:
        raise ValueError(
            "quantile probability must lie in [0,1]"
        )
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = probability * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return (
        ordered[lower] * (1.0 - fraction)
        + ordered[upper] * fraction
    )


def simulate_lambda_recovery(
    design: LambdaRecoveryDesign,
    *,
    replicates: int,
    seed: int,
) -> LambdaRecoverySummary:
    """Run a seed-explicit Monte Carlo parameter-recovery experiment."""

    if replicates <= 0:
        raise ValueError("replicates must be positive")

    estimates = tuple(
        simulate_naive_lambda_once(
            design,
            seed=seed + index * 1_000_003,
        )
        for index in range(replicates)
    )
    average = mean(estimates)
    bias = average - design.true_lambda
    rmse = sqrt(
        mean(
            (estimate - design.true_lambda) ** 2
            for estimate in estimates
        )
    )
    return LambdaRecoverySummary(
        design=design,
        replicates=replicates,
        seed=seed,
        expected_naive_lambda=(
            expected_naive_lambda(design)
        ),
        mean_naive_lambda=average,
        sd_naive_lambda=(
            pstdev(estimates)
            if len(estimates) > 1
            else 0.0
        ),
        bias=bias,
        rmse=rmse,
        q025=_quantile(estimates, 0.025),
        q50=_quantile(estimates, 0.5),
        q975=_quantile(estimates, 0.975),
        fraction_below_true_lambda=(
            sum(
                estimate < design.true_lambda
                for estimate in estimates
            )
            / len(estimates)
        ),
    )


def lower_tail_null_probability(
    observed_lambda_hat: float,
    null_estimates: Iterable[float],
) -> float:
    """Monte Carlo lower-tail probability with a plus-one correction.

    Use with a true-lambda=1 null distribution when the empirical alternative
    is contraction (lambda_hat smaller than the no-correction value).
    """

    observed = _finite(
        "observed_lambda_hat",
        observed_lambda_hat,
    )
    values = tuple(float(value) for value in null_estimates)
    if not values:
        raise ValueError(
            "null_estimates must contain at least one value"
        )
    if any(not isfinite(value) for value in values):
        raise ValueError(
            "null_estimates must be finite"
        )
    lower_or_equal = sum(
        value <= observed
        for value in values
    )
    return (
        lower_or_equal + 1
    ) / (len(values) + 1)


def corrected_lambda_from_known_error(
    *,
    naive_lambda: float,
    observed_predictor_variance: float,
    predictor_error_variance: float,
    predictor_outcome_error_covariance: float = 0.0,
) -> float:
    """Errors-in-variables correction when the error moments are calibrated.

    The function intentionally requires externally supplied error moments. It
    refuses cases in which the implied latent predictor variance is not
    positive.
    """

    naive_lambda = _finite(
        "naive_lambda", naive_lambda
    )
    observed_predictor_variance = _nonnegative(
        "observed_predictor_variance",
        observed_predictor_variance,
    )
    predictor_error_variance = _nonnegative(
        "predictor_error_variance",
        predictor_error_variance,
    )
    covariance = _finite(
        "predictor_outcome_error_covariance",
        predictor_outcome_error_covariance,
    )

    latent_variance = (
        observed_predictor_variance
        - predictor_error_variance
    )
    if latent_variance <= 0.0:
        raise ValueError(
            "calibrated predictor error leaves no positive latent variance"
        )

    observed_covariance = (
        naive_lambda
        * observed_predictor_variance
    )
    latent_covariance = (
        observed_covariance - covariance
    )
    return (
        latent_covariance
        / latent_variance
    )


def required_equal_error_sd_ratio(
    *,
    observed_naive_lambda: float,
    true_lambda: float = 1.0,
    error_correlation: float = 0.0,
) -> float | None:
    """Noise-to-signal SD ratio needed to produce an expected naive slope.

    Assumes equal predictor/outcome measurement-error SDs, both expressed as a
    ratio r to the latent predictor SD. Then

        beta_naive = (true_lambda + rho*r^2) / (1 + r^2).

    Returns r when a finite non-negative solution exists, otherwise None.
    This is a stress threshold, not an estimate of empirical error.
    """

    observed = _finite(
        "observed_naive_lambda",
        observed_naive_lambda,
    )
    latent = _finite(
        "true_lambda",
        true_lambda,
    )
    rho = _finite(
        "error_correlation",
        error_correlation,
    )
    if not -1.0 <= rho <= 1.0:
        raise ValueError(
            "error_correlation must lie in [-1,1]"
        )

    numerator = latent - observed
    denominator = observed - rho

    if abs(numerator) <= 1e-15:
        return 0.0
    if numerator < 0.0 or denominator <= 0.0:
        return None

    ratio_squared = numerator / denominator
    if ratio_squared < 0.0:
        return None
    return sqrt(ratio_squared)


def recovery_design_from_observed_predictor_sd(
    *,
    true_lambda: float,
    observed_predictor_sd: float,
    predictor_error_sd: float,
    outcome_error_sd: float,
    error_correlation: float = 0.0,
    process_noise_sd: float = 0.0,
    n_pairs: int,
) -> LambdaRecoveryDesign:
    """Construct a recovery design without guessing latent phase variance.

    Under the additive independent-of-signal measurement model,

        Var(E_obs) = Var(E_true) + Var(error_current).

    The implied latent phase SD is therefore recovered from the empirical
    predictor SD and an independently calibrated predictor-error SD.
    """

    observed_sd = _nonnegative(
        "observed_predictor_sd",
        observed_predictor_sd,
    )
    predictor_sd = _nonnegative(
        "predictor_error_sd",
        predictor_error_sd,
    )
    latent_variance = (
        observed_sd**2
        - predictor_sd**2
    )
    if latent_variance <= 0.0:
        raise ValueError(
            "predictor error SD leaves no positive latent phase variance"
        )
    return LambdaRecoveryDesign(
        true_lambda=true_lambda,
        latent_phase_sd=sqrt(latent_variance),
        predictor_error_sd=predictor_sd,
        outcome_error_sd=outcome_error_sd,
        error_correlation=error_correlation,
        process_noise_sd=process_noise_sd,
        n_pairs=n_pairs,
    )


def required_equal_error_sd_over_observed_predictor_sd(
    *,
    observed_naive_lambda: float,
    true_lambda: float = 1.0,
    error_correlation: float = 0.0,
) -> float | None:
    """Error SD divided by observed predictor SD needed to mimic a slope.

    Under the same equal-error additive model used by
    :func:`required_equal_error_sd_ratio`,

        beta_naive
        = true_lambda * (1-q^2) + rho * q^2,

    where

        q = error_sd / observed_predictor_sd.

    This observed-scale ratio is often easier to apply to an empirical phase
    series because its observed SD is directly available. The return value is a
    stress threshold, not an empirical error estimate.
    """

    observed = _finite(
        "observed_naive_lambda",
        observed_naive_lambda,
    )
    latent = _finite(
        "true_lambda",
        true_lambda,
    )
    rho = _finite(
        "error_correlation",
        error_correlation,
    )
    if not -1.0 <= rho <= 1.0:
        raise ValueError(
            "error_correlation must lie in [-1,1]"
        )

    denominator = latent - rho
    numerator = latent - observed

    if abs(numerator) <= 1e-15:
        return 0.0
    if numerator < 0.0 or denominator <= 0.0:
        return None

    q_squared = numerator / denominator
    if not 0.0 <= q_squared < 1.0:
        return None
    return sqrt(q_squared)
