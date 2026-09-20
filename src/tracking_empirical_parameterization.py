"""Empirical inverse maps for PAYOFF-B migration--phenology tracking.

The tracking model uses transformed rates rather than raw movement distances or
calendar shifts. This module makes the observation-to-model map explicit for
the declared one-step kernel and first-order phenology response.

These are algebraic identifications under the declared model, not generic
estimators for arbitrary movement or phenology processes.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log, log1p


@dataclass(frozen=True)
class MovementKernelEstimate:
    migration_rate: float
    moving_fraction: float
    x_weight: float
    y_weight: float
    anisotropy_ratio_y_over_x: float | None
    anisotropy_identified: bool


@dataclass(frozen=True)
class DirectionalMovementKernelEstimate:
    migration_rate: float
    moving_fraction: float
    x_weight: float
    y_weight: float
    x_bias: float
    y_bias: float
    anisotropy_ratio_y_over_x: float | None


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

    moving_fraction = 1.0 - exp(-migration_rate)
    total_weight = x_weight + y_weight
    variance_scale = moving_fraction * patch_spacing * patch_spacing
    return (
        variance_scale * x_weight / total_weight,
        variance_scale * y_weight / total_weight,
    )



def infer_directional_movement_kernel_from_moments(
    mean_x: float,
    mean_y: float,
    second_moment_x: float,
    second_moment_y: float,
    patch_spacing: float,
) -> DirectionalMovementKernelEstimate:
    """Invert the biased one-step nearest-neighbor movement kernel.

    For movement fraction f, normalized axis shares s_x,s_y and directional
    biases b_x,b_y in [-1,1]:

        E[X]   = f s_x b_x d
        E[X^2] = f s_x d^2
        E[Y]   = f s_y b_y d
        E[Y^2] = f s_y d^2.

    Hence

        f = [E[X^2] + E[Y^2]] / d^2
        b_x = E[X] d / E[X^2]
        b_y = E[Y] d / E[Y^2].

    This exact inverse supports directional migration while preserving the
    previous symmetric kernel as b_x=b_y=0.
    """

    for name, value in (
        ("mean_x", mean_x),
        ("mean_y", mean_y),
        ("second_moment_x", second_moment_x),
        ("second_moment_y", second_moment_y),
        ("patch_spacing", patch_spacing),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if second_moment_x < 0.0 or second_moment_y < 0.0:
        raise ValueError("component second moments must be non-negative")
    if patch_spacing <= 0.0:
        raise ValueError("patch_spacing must be positive")

    total_second = second_moment_x + second_moment_y
    moving_fraction = total_second / (
        patch_spacing * patch_spacing
    )
    if moving_fraction >= 1.0:
        raise ValueError(
            "observed second moment exceeds one-step kernel support; "
            "use a wider or continuous movement kernel"
        )

    tolerance = 1e-12
    if total_second == 0.0:
        if abs(mean_x) > tolerance or abs(mean_y) > tolerance:
            raise ValueError(
                "non-zero mean displacement is incompatible with zero "
                "component second moments"
            )
        return DirectionalMovementKernelEstimate(
            migration_rate=0.0,
            moving_fraction=0.0,
            x_weight=1.0,
            y_weight=1.0,
            x_bias=0.0,
            y_bias=0.0,
            anisotropy_ratio_y_over_x=None,
        )

    x_share = second_moment_x / total_second
    y_share = second_moment_y / total_second

    if second_moment_x == 0.0:
        if abs(mean_x) > tolerance:
            raise ValueError(
                "non-zero x mean is incompatible with zero x second moment"
            )
        x_bias = 0.0
    else:
        x_bias = mean_x * patch_spacing / second_moment_x

    if second_moment_y == 0.0:
        if abs(mean_y) > tolerance:
            raise ValueError(
                "non-zero y mean is incompatible with zero y second moment"
            )
        y_bias = 0.0
    else:
        y_bias = mean_y * patch_spacing / second_moment_y

    for name, value in (("x_bias", x_bias), ("y_bias", y_bias)):
        if value < -1.0 - tolerance or value > 1.0 + tolerance:
            raise ValueError(
                f"identified {name} lies outside [-1,1]; "
                "the one-step directional kernel is incompatible with the "
                "observed moments"
            )

    x_bias = min(1.0, max(-1.0, x_bias))
    y_bias = min(1.0, max(-1.0, y_bias))

    return DirectionalMovementKernelEstimate(
        migration_rate=-log1p(-moving_fraction),
        moving_fraction=moving_fraction,
        x_weight=x_share,
        y_weight=y_share,
        x_bias=x_bias,
        y_bias=y_bias,
        anisotropy_ratio_y_over_x=(
            second_moment_y / second_moment_x
            if second_moment_x > 0.0
            else None
        ),
    )


def implied_directional_movement_moments(
    migration_rate: float,
    x_weight: float,
    y_weight: float,
    x_bias: float,
    y_bias: float,
    patch_spacing: float,
) -> tuple[float, float, float, float]:
    """Forward moments for the biased nearest-neighbor kernel."""

    for name, value in (
        ("migration_rate", migration_rate),
        ("x_weight", x_weight),
        ("y_weight", y_weight),
        ("x_bias", x_bias),
        ("y_bias", y_bias),
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
    if not -1.0 <= x_bias <= 1.0:
        raise ValueError("x_bias must lie in [-1,1]")
    if not -1.0 <= y_bias <= 1.0:
        raise ValueError("y_bias must lie in [-1,1]")
    if patch_spacing <= 0.0:
        raise ValueError("patch_spacing must be positive")

    moving_fraction = 1.0 - exp(-migration_rate)
    total_weight = x_weight + y_weight
    x_share = x_weight / total_weight
    y_share = y_weight / total_weight
    d = patch_spacing

    return (
        moving_fraction * x_share * x_bias * d,
        moving_fraction * y_share * y_bias * d,
        moving_fraction * x_share * d * d,
        moving_fraction * y_share * d * d,
    )

def deaggregate_directional_moments(
    mean_x: float,
    mean_y: float,
    second_moment_x: float,
    second_moment_y: float,
    latent_substeps: int,
) -> tuple[float, float, float, float]:
    """Recover one-step raw moments from an n-step aggregate.

    For iid one-step increments X with mean mu and raw second moment q,

        E[S_n] = n mu

        E[S_n^2]
        = n q + n(n-1) mu^2.

    Therefore

        mu = E[S_n] / n

        q = E[S_n^2]/n
            - (n-1) E[S_n]^2 / n^2.

    The same identity is applied independently to x and y components.
    """

    if not isinstance(latent_substeps, int) or latent_substeps <= 0:
        raise ValueError("latent_substeps must be a positive integer")
    for name, value in (
        ("mean_x", mean_x),
        ("mean_y", mean_y),
        ("second_moment_x", second_moment_x),
        ("second_moment_y", second_moment_y),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if second_moment_x < mean_x * mean_x - 1e-12:
        raise ValueError(
            "x aggregate second moment is smaller than mean squared"
        )
    if second_moment_y < mean_y * mean_y - 1e-12:
        raise ValueError(
            "y aggregate second moment is smaller than mean squared"
        )

    n = float(latent_substeps)
    step_mean_x = mean_x / n
    step_mean_y = mean_y / n
    step_second_x = (
        second_moment_x / n
        - (n - 1.0) * mean_x * mean_x / (n * n)
    )
    step_second_y = (
        second_moment_y / n
        - (n - 1.0) * mean_y * mean_y / (n * n)
    )
    tolerance = 1e-12
    if step_second_x < -tolerance or step_second_y < -tolerance:
        raise ValueError(
            "deaggregated one-step second moment is negative"
        )
    step_second_x = max(0.0, step_second_x)
    step_second_y = max(0.0, step_second_y)

    return (
        step_mean_x,
        step_mean_y,
        step_second_x,
        step_second_y,
    )


def infer_directional_movement_kernel_from_aggregated_moments(
    mean_x: float,
    mean_y: float,
    second_moment_x: float,
    second_moment_y: float,
    patch_spacing: float,
    latent_substeps: int,
) -> DirectionalMovementKernelEstimate:
    """Infer the one-step directional kernel from a fixed n-step interval."""

    (
        step_mean_x,
        step_mean_y,
        step_second_x,
        step_second_y,
    ) = deaggregate_directional_moments(
        mean_x,
        mean_y,
        second_moment_x,
        second_moment_y,
        latent_substeps,
    )
    return infer_directional_movement_kernel_from_moments(
        step_mean_x,
        step_mean_y,
        step_second_x,
        step_second_y,
        patch_spacing,
    )


def implied_aggregated_directional_movement_moments(
    migration_rate: float,
    x_weight: float,
    y_weight: float,
    x_bias: float,
    y_bias: float,
    patch_spacing: float,
    latent_substeps: int,
) -> tuple[float, float, float, float]:
    """Forward n-step moments under iid repetition of the one-step kernel."""

    if not isinstance(latent_substeps, int) or latent_substeps <= 0:
        raise ValueError("latent_substeps must be a positive integer")
    (
        step_mean_x,
        step_mean_y,
        step_second_x,
        step_second_y,
    ) = implied_directional_movement_moments(
        migration_rate,
        x_weight,
        y_weight,
        x_bias,
        y_bias,
        patch_spacing,
    )
    n = float(latent_substeps)
    return (
        n * step_mean_x,
        n * step_mean_y,
        n * step_second_x
        + n * (n - 1.0) * step_mean_x * step_mean_x,
        n * step_second_y
        + n * (n - 1.0) * step_mean_y * step_mean_y,
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
    return -log(ratio)


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



@dataclass(frozen=True)
class TrackingFitnessEstimate:
    baseline_growth: float
    abiotic_strength: float
    interaction_strength: float
    migration_cost: float
    phenology_cost: float
    joint_cost: float


def identify_tracking_fitness_from_matched_contrasts(
    *,
    baseline_growth: float,
    abiotic_growth: float,
    abiotic_mismatch: float,
    interaction_growth: float,
    interaction_mismatch: float,
    migration_growth: float,
    migration_rate: float,
    phenology_growth: float,
    phenology_rate: float,
    joint_growth: float,
    joint_migration_rate: float,
    joint_phenology_rate: float,
    require_nonnegative: bool = True,
) -> TrackingFitnessEstimate:
    """Identify the declared quadratic fitness terms from orthogonal contrasts.

    The exact design is:

        reference:
            e=M=m=h=0

        abiotic contrast:
            e != 0, M=m=h=0

        interaction contrast:
            M != 0, e=m=h=0

        migration-cost contrast:
            m != 0, e=M=h=0

        phenology-cost contrast:
            h != 0, e=M=m=0

        joint-cost contrast:
            m,h != 0, e=M=0.

    All observations must share the same payoff/growth scale and background
    ecology. This function identifies the declared algebraic model only; it
    does not verify those biological matching assumptions.
    """

    values = {
        "baseline_growth": baseline_growth,
        "abiotic_growth": abiotic_growth,
        "abiotic_mismatch": abiotic_mismatch,
        "interaction_growth": interaction_growth,
        "interaction_mismatch": interaction_mismatch,
        "migration_growth": migration_growth,
        "migration_rate": migration_rate,
        "phenology_growth": phenology_growth,
        "phenology_rate": phenology_rate,
        "joint_growth": joint_growth,
        "joint_migration_rate": joint_migration_rate,
        "joint_phenology_rate": joint_phenology_rate,
    }
    for name, value in values.items():
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")

    if abiotic_mismatch == 0.0:
        raise ValueError("abiotic_mismatch must be non-zero")
    if interaction_mismatch == 0.0:
        raise ValueError("interaction_mismatch must be non-zero")
    if migration_rate <= 0.0:
        raise ValueError("migration_rate must be positive")
    if phenology_rate <= 0.0:
        raise ValueError("phenology_rate must be positive")
    if joint_migration_rate <= 0.0 or joint_phenology_rate <= 0.0:
        raise ValueError(
            "joint migration and phenology rates must both be positive"
        )

    abiotic_strength = (
        2.0
        * (baseline_growth - abiotic_growth)
        / (abiotic_mismatch * abiotic_mismatch)
    )
    interaction_strength = (
        2.0
        * (baseline_growth - interaction_growth)
        / (interaction_mismatch * interaction_mismatch)
    )
    migration_cost = (
        (baseline_growth - migration_growth)
        / (migration_rate * migration_rate)
    )
    phenology_cost = (
        (baseline_growth - phenology_growth)
        / (phenology_rate * phenology_rate)
    )
    joint_numerator = (
        baseline_growth
        - joint_growth
        - migration_cost
        * joint_migration_rate
        * joint_migration_rate
        - phenology_cost
        * joint_phenology_rate
        * joint_phenology_rate
    )
    joint_cost = (
        joint_numerator
        / (joint_migration_rate * joint_phenology_rate)
    )

    estimate = TrackingFitnessEstimate(
        baseline_growth=baseline_growth,
        abiotic_strength=abiotic_strength,
        interaction_strength=interaction_strength,
        migration_cost=migration_cost,
        phenology_cost=phenology_cost,
        joint_cost=joint_cost,
    )

    if require_nonnegative:
        for name in (
            "abiotic_strength",
            "interaction_strength",
            "migration_cost",
            "phenology_cost",
            "joint_cost",
        ):
            if getattr(estimate, name) < 0.0:
                raise ValueError(
                    f"identified {name} is negative and incompatible "
                    "with the declared non-negative penalty model"
                )

    return estimate



@dataclass(frozen=True)
class ResidualCompressionAudit:
    residual_before: float
    residual_after: float
    status: str
    monotone_first_order_compatible: bool
    compression_ratio: float | None
    log_compression: float | None


def audit_residual_compression(
    residual_before: float,
    residual_after: float,
) -> ResidualCompressionAudit:
    """Classify whether an aggregated residual pair licenses the simple inverse.

    This checks mathematical compatibility only. Even a compatible pair does
    not identify a per-generation rate unless the before/after interval equals
    the model decision interval and spatial state is held appropriately fixed.
    """

    if not isfinite(residual_before) or not isfinite(residual_after):
        raise ValueError("residuals must be finite")

    if residual_before == 0.0:
        return ResidualCompressionAudit(
            residual_before=residual_before,
            residual_after=residual_after,
            status="zero_start_residual",
            monotone_first_order_compatible=False,
            compression_ratio=None,
            log_compression=None,
        )

    if residual_after == 0.0:
        return ResidualCompressionAudit(
            residual_before=residual_before,
            residual_after=residual_after,
            status="complete_correction_boundary",
            monotone_first_order_compatible=False,
            compression_ratio=0.0,
            log_compression=None,
        )

    if residual_before * residual_after < 0.0:
        return ResidualCompressionAudit(
            residual_before=residual_before,
            residual_after=residual_after,
            status="sign_crossing_or_overshoot",
            monotone_first_order_compatible=False,
            compression_ratio=None,
            log_compression=None,
        )

    ratio = abs(residual_after / residual_before)
    if ratio > 1.0:
        return ResidualCompressionAudit(
            residual_before=residual_before,
            residual_after=residual_after,
            status="mismatch_amplification",
            monotone_first_order_compatible=False,
            compression_ratio=ratio,
            log_compression=None,
        )
    if ratio == 1.0:
        return ResidualCompressionAudit(
            residual_before=residual_before,
            residual_after=residual_after,
            status="no_correction",
            monotone_first_order_compatible=True,
            compression_ratio=1.0,
            log_compression=0.0,
        )

    return ResidualCompressionAudit(
        residual_before=residual_before,
        residual_after=residual_after,
        status="monotone_compression",
        monotone_first_order_compatible=True,
        compression_ratio=ratio,
        log_compression=-log(ratio),
    )
