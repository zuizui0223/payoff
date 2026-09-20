"""Empirical inverse maps for PAYOFF-B migration--phenology tracking.

The tracking model uses transformed rates rather than raw movement distances or
calendar shifts. This module makes the observation-to-model map explicit for
the declared one-step kernel and first-order phenology response.

These are algebraic identifications under the declared model, not generic
estimators for arbitrary movement or phenology processes.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log1p


@dataclass(frozen=True)
class MovementKernelEstimate:
    migration_rate: float
    moving_fraction: float
    x_weight: float
    y_weight: float
    anisotropy_ratio_y_over_x: float | None
    anisotropy_identified: bool


@dataclass(frozen=True)
class TrackingParameterization:
    climate_velocity: float
    migration_rate: float
    dispersal_x_weight: float
    dispersal_y_weight: float
    phenology_rate: float
    phenology_scale: float
    max_abs_phenology_shift: float


def infer_movement_kernel_from_component_variances(
    variance_x: float,
    variance_y: float,
    patch_spacing: float,
) -> MovementKernelEstimate:
    """Invert the declared nearest-neighbor anisotropic movement kernel.

    For one generation, let f = 1-exp(-m) be the fraction that moves one patch.
    With x/y axis weights wx, wy,

        Var_x = f * wx/(wx+wy) * d^2
        Var_y = f * wy/(wx+wy) * d^2.

    Therefore

        f = (Var_x + Var_y)/d^2
        m = -log(1-f)

    and the normalized axis weights are identified from the variance shares
    whenever total movement variance is positive.

    The inverse is licensed only when 0 <= f < 1 because the model moves at
    most one patch per generation in this kernel.
    """

    for name, value in (
        ("variance_x", variance_x),
        ("variance_y", variance_y),
        ("patch_spacing", patch_spacing),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if variance_x < 0.0 or variance_y < 0.0:
        raise ValueError("component variances must be non-negative")
    if patch_spacing <= 0.0:
        raise ValueError("patch_spacing must be positive")

    total_variance = variance_x + variance_y
    moving_fraction = (
        total_variance / (patch_spacing * patch_spacing)
    )
    if moving_fraction >= 1.0:
        raise ValueError(
            "observed variance exceeds the one-step kernel support; "
            "use a wider or continuous movement kernel"
        )

    if moving_fraction == 0.0:
        return MovementKernelEstimate(
            migration_rate=0.0,
            moving_fraction=0.0,
            x_weight=1.0,
            y_weight=1.0,
            anisotropy_ratio_y_over_x=None,
            anisotropy_identified=False,
        )

    migration_rate = -log1p(-moving_fraction)
    x_share = variance_x / total_variance
    y_share = variance_y / total_variance

    # Only relative weights matter in the simulator. Normalizing to a sum of
    # one gives a unique receipt while preserving the exact transition law.
    if variance_x > 0.0:
        ratio = variance_y / variance_x
    else:
        ratio = None

    return MovementKernelEstimate(
        migration_rate=migration_rate,
        moving_fraction=moving_fraction,
        x_weight=x_share,
        y_weight=y_share,
        anisotropy_ratio_y_over_x=ratio,
        anisotropy_identified=True,
    )


def implied_component_variances(
    migration_rate: float,
    x_weight: float,
    y_weight: float,
    patch_spacing: float,
) -> tuple[float, float]:
    """Forward map for the declared nearest-neighbor movement kernel."""

    for name, value in (
        ("migration_rate", migration_rate),
        ("x_weight", x_weight),
        ("y_weight", y_weight),
        ("patch_spacing", patch_spacing),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    if x_weight < 0.0 or y_weight < 0.0:
        raise ValueError("movement weights must be non-negative")
    if x_weight + y_weight <= 0.0:
        raise ValueError("at least one movement weight must be positive")
    if patch_spacing <= 0.0:
        raise ValueError("patch_spacing must be positive")

    moving_fraction = 1.0 - __import__("math").exp(-migration_rate)
    total_weight = x_weight + y_weight
    variance_scale = moving_fraction * patch_spacing * patch_spacing
    return (
        variance_scale * x_weight / total_weight,
        variance_scale * y_weight / total_weight,
    )


def infer_tracking_rate_from_correction_fraction(
    correction_fraction: float,
) -> float:
    """Invert q = 1-exp(-rate) for migration or phenology response."""

    if not isfinite(correction_fraction):
        raise ValueError("correction_fraction must be finite")
    if not 0.0 <= correction_fraction < 1.0:
        raise ValueError(
            "correction_fraction must lie in [0,1); "
            "q=1 corresponds to an infinite rate"
        )
    return -log1p(-correction_fraction)


def infer_phenology_rate_from_residual_pair(
    residual_before: float,
    residual_after: float,
) -> float:
    """Infer h from one no-overshoot first-order residual correction.

    Under the declared phenology update with fixed spatial state,

        e_after = exp(-h) * e_before.

    The ratio must lie in (0,1] for this exact inverse. Sign reversal,
    amplification, or overshoot indicate that the simple first-order update is
    not an adequate description for that transition.
    """

    if not isfinite(residual_before) or not isfinite(residual_after):
        raise ValueError("residuals must be finite")
    if residual_before == 0.0:
        raise ValueError("residual_before must be non-zero")

    ratio = residual_after / residual_before
    if not 0.0 < ratio <= 1.0:
        raise ValueError(
            "residual pair is incompatible with monotone first-order correction"
        )
    return -__import__("math").log(ratio)


def climate_velocity_from_wave_speed(
    spatial_gradient: float,
    wave_speed: float,
) -> float:
    """Convert physical range-shift speed to climate-coordinate velocity."""

    if not isfinite(spatial_gradient) or not isfinite(wave_speed):
        raise ValueError("spatial_gradient and wave_speed must be finite")
    if spatial_gradient <= 0.0:
        raise ValueError("spatial_gradient must be positive")
    return spatial_gradient * wave_speed


def infer_quadratic_mismatch_strength(
    mismatch: float,
    growth_loss: float,
) -> float:
    """Invert growth_loss = 0.5 * strength * mismatch^2."""

    if not isfinite(mismatch) or not isfinite(growth_loss):
        raise ValueError("mismatch and growth_loss must be finite")
    if mismatch == 0.0:
        raise ValueError("mismatch must be non-zero")
    if growth_loss < 0.0:
        raise ValueError("growth_loss must be non-negative")
    return 2.0 * growth_loss / (mismatch * mismatch)


def infer_quadratic_architecture_cost(
    tracking_rate: float,
    growth_cost: float,
) -> float:
    """Invert growth_cost = c * tracking_rate^2 for one isolated axis."""

    if not isfinite(tracking_rate) or not isfinite(growth_cost):
        raise ValueError("tracking_rate and growth_cost must be finite")
    if tracking_rate <= 0.0:
        raise ValueError("tracking_rate must be positive")
    if growth_cost < 0.0:
        raise ValueError("growth_cost must be non-negative")
    return growth_cost / (tracking_rate * tracking_rate)


def build_tracking_parameterization(
    *,
    variance_x: float,
    variance_y: float,
    patch_spacing: float,
    spatial_gradient: float,
    wave_speed: float,
    phenology_correction_fraction: float,
    phenology_scale: float,
    max_abs_phenology_shift: float,
) -> TrackingParameterization:
    """Build the directly identified subset of a tracking scenario.

    This intentionally does not infer baseline growth, mismatch strengths,
    interaction strength, or architecture costs. Those require matched growth
    or fitness contrasts and must not be guessed from movement alone.
    """

    if not isfinite(phenology_scale) or phenology_scale <= 0.0:
        raise ValueError("phenology_scale must be positive and finite")
    if (
        not isfinite(max_abs_phenology_shift)
        or max_abs_phenology_shift < 0.0
    ):
        raise ValueError(
            "max_abs_phenology_shift must be non-negative and finite"
        )

    movement = infer_movement_kernel_from_component_variances(
        variance_x,
        variance_y,
        patch_spacing,
    )
    return TrackingParameterization(
        climate_velocity=climate_velocity_from_wave_speed(
            spatial_gradient,
            wave_speed,
        ),
        migration_rate=movement.migration_rate,
        dispersal_x_weight=movement.x_weight,
        dispersal_y_weight=movement.y_weight,
        phenology_rate=infer_tracking_rate_from_correction_fraction(
            phenology_correction_fraction
        ),
        phenology_scale=phenology_scale,
        max_abs_phenology_shift=max_abs_phenology_shift,
    )
