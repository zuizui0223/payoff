"""Reciprocal architecture invasion under anti-phase temporal heterogeneity.

Assume patch static gaps swap anti-phase around one mean gap phi_bar while a
common frequency-feedback coefficient eta is held fixed. Both rare-D and
rare-S invasion problems receive the same anti-phase temporal premium P.

Then
    Lambda_D = phi_bar - eta + P
    Lambda_S =-phi_bar - eta + P.

Thus temporal source switching shifts the reciprocal-invasion geometry through
an effective coordination coefficient eta_eff=eta-P.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

from src.anti_phase_temporal import (
    anti_phase_temporal_premium,
    exact_max_premium,
    exact_optimal_migration,
    weak_contrast_max_premium_approx,
    weak_contrast_optimal_dimensionless_migration,
    weak_contrast_shape,
)


def reciprocal_exponents(
    mean_static_gap: float,
    eta: float,
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
) -> Tuple[float, float]:
    """Return exact (Lambda_D,Lambda_S) for anti-phase temporal switching."""

    premium = anti_phase_temporal_premium(
        contrast_half_amplitude, migration_rate, season_duration
    )
    return (
        mean_static_gap - eta + premium,
        -mean_static_gap - eta + premium,
    )


def effective_coordination_strength(
    eta: float,
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
) -> float:
    """Return eta_eff=eta-P.

    eta_eff>0 leaves a mutual-non-invasion coordination band.
    eta_eff=0 collapses the reciprocal boundaries.
    eta_eff<0 creates a reciprocal-invasion band.
    """

    premium = anti_phase_temporal_premium(
        contrast_half_amplitude, migration_rate, season_duration
    )
    return eta - premium


def classify_reciprocal_temporal_state(
    mean_static_gap: float,
    eta: float,
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
    tol: float = 1e-12,
) -> str:
    """Classify reciprocal rare-architecture invasibility."""

    lambda_d, lambda_s = reciprocal_exponents(
        mean_static_gap,
        eta,
        contrast_half_amplitude,
        migration_rate,
        season_duration,
    )
    d = lambda_d > tol
    s = lambda_s > tol
    if d and s:
        return "reciprocal_invasion"
    if not d and not s:
        if abs(lambda_d) <= tol or abs(lambda_s) <= tol:
            return "boundary"
        return "mutual_noninvasion"
    if d:
        return "d_only_invasion"
    return "s_only_invasion"


def temporal_middle_half_width(
    eta: float,
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
) -> float:
    """Return |eta-P|, the half-width around mean_static_gap=0."""

    return abs(
        effective_coordination_strength(
            eta,
            contrast_half_amplitude,
            migration_rate,
            season_duration,
        )
    )


def exact_reciprocal_invasion_capacity(
    eta: float,
    mean_static_gap: float,
    contrast_half_amplitude: float,
    season_duration: float,
) -> float:
    """Return max_m P - [eta+|phi_bar|].

    Positive capacity means one exact bounded migration interval exists in
    which both reciprocal architectures invade.
    """

    if eta < 0.0:
        raise ValueError("this coordination-capacity diagnostic requires eta>=0")
    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
    x = abs(contrast_half_amplitude)
    if x == 0.0:
        return -(eta + abs(mean_static_gap))
    return exact_max_premium(x, season_duration) - (
        eta + abs(mean_static_gap)
    )


def exact_reciprocal_switch_migrations(
    eta: float,
    mean_static_gap: float,
    contrast_half_amplitude: float,
    season_duration: float,
    tol: float = 1e-12,
) -> Optional[Tuple[float, float]]:
    """Return the two exact migration boundaries for reciprocal invasion.

    Reciprocal invasion requires
        P(m)>eta+|phi_bar|.
    The exact anti-phase premium is strictly increasing to one unique maximum
    and strictly decreasing afterward. Hence, when its maximum exceeds the
    target, exactly two positive roots exist and define one bounded interval.
    """

    if eta < 0.0:
        raise ValueError("exact reciprocal switch solver requires eta>=0")
    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
    if tol <= 0.0:
        raise ValueError("tol must be positive")
    x = abs(contrast_half_amplitude)
    if x == 0.0:
        return None

    target = eta + abs(mean_static_gap)
    m_star = exact_optimal_migration(x, season_duration)
    peak = anti_phase_temporal_premium(x, m_star, season_duration)
    if target <= 0.0:
        # At target zero, every finite positive migration has P>0, so there is
        # no finite two-boundary interval to return.
        return None
    if peak <= target:
        return None

    lower = _bisect_exact_premium_root(
        0.0, m_star, x, season_duration, target, tol, rising=True
    )

    upper_bound = max(2.0 * m_star, 1.0 / season_duration)
    while anti_phase_temporal_premium(x, upper_bound, season_duration) > target:
        upper_bound *= 2.0
        if upper_bound > 1e15:
            raise RuntimeError("failed to bracket upper exact temporal switch")
    upper = _bisect_exact_premium_root(
        m_star,
        upper_bound,
        x,
        season_duration,
        target,
        tol,
        rising=False,
    )
    return lower, upper


def exact_coordination_can_be_overcome(
    eta: float,
    contrast_half_amplitude: float,
    season_duration: float,
) -> bool:
    """Return whether exact anti-phase P_max exceeds eta at phi_bar=0."""

    if eta <= 0.0:
        raise ValueError("eta must be positive")
    x = abs(contrast_half_amplitude)
    if x == 0.0:
        return False
    return exact_max_premium(x, season_duration) > eta


def weak_contrast_coordination_can_be_overcome(
    eta: float,
    contrast_half_amplitude: float,
    season_duration: float,
) -> bool:
    """Leading-order test for whether any migration can make P>eta.

    Uses max P ~= H(u*) x^2 tau. Intended for |x|tau << 1 and eta>0.
    """

    if eta <= 0.0:
        raise ValueError("eta must be positive")
    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
    return (
        weak_contrast_max_premium_approx(
            contrast_half_amplitude, season_duration
        )
        > eta
    )


def weak_contrast_threshold_ratio() -> float:
    """Return 1/H(u*), about 7.54787962834.

    The leading-order criterion P_max>eta is equivalently
        x^2 tau / eta > 1/H(u*).
    """

    u_star = weak_contrast_optimal_dimensionless_migration()
    return 1.0 / weak_contrast_shape(u_star)


def weak_contrast_switch_migrations(
    eta: float,
    contrast_half_amplitude: float,
    season_duration: float,
    tol: float = 1e-12,
) -> Optional[Tuple[float, float]]:
    """Approximate lower/upper migration switches where weak-contrast P=eta.

    When the weak-contrast maximum exceeds eta, H(u)=eta/(x^2 tau) has
    exactly two positive roots because H has one positive maximum. They define
    an intermediate migration interval in which P>eta and the temporal game
    has reciprocal invasion at mean_static_gap=0.
    """

    if eta <= 0.0:
        raise ValueError("eta must be positive")
    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
    if tol <= 0.0:
        raise ValueError("tol must be positive")
    x = abs(contrast_half_amplitude)
    if x == 0.0:
        return None

    target = eta / (x * x * season_duration)
    u_star = weak_contrast_optimal_dimensionless_migration()
    peak = weak_contrast_shape(u_star)
    if target >= peak:
        return None

    lower_u = _bisect_shape_root(0.0, u_star, target, tol, rising=True)

    upper_bound = max(2.0 * u_star, 4.0)
    while weak_contrast_shape(upper_bound) > target:
        upper_bound *= 2.0
        if upper_bound > 1e12:
            raise RuntimeError("failed to bracket upper weak-contrast switch")
    upper_u = _bisect_shape_root(
        u_star, upper_bound, target, tol, rising=False
    )
    tau = season_duration
    return lower_u / tau, upper_u / tau


def reciprocal_temporal_summary(
    mean_static_gap: float,
    eta: float,
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
) -> Dict[str, float]:
    """Return the main reciprocal temporal diagnostics."""

    premium = anti_phase_temporal_premium(
        contrast_half_amplitude, migration_rate, season_duration
    )
    lambda_d, lambda_s = reciprocal_exponents(
        mean_static_gap,
        eta,
        contrast_half_amplitude,
        migration_rate,
        season_duration,
    )
    return {
        "mean_static_gap": mean_static_gap,
        "eta": eta,
        "temporal_premium": premium,
        "eta_effective": eta - premium,
        "lambda_d": lambda_d,
        "lambda_s": lambda_s,
        "middle_half_width": abs(eta - premium),
    }


def _bisect_shape_root(
    lower: float,
    upper: float,
    target: float,
    tol: float,
    rising: bool,
) -> float:
    while upper - lower > tol:
        mid = 0.5 * (lower + upper)
        value = weak_contrast_shape(mid)
        if rising:
            if value < target:
                lower = mid
            else:
                upper = mid
        else:
            if value > target:
                lower = mid
            else:
                upper = mid
    return 0.5 * (lower + upper)


def _bisect_exact_premium_root(
    lower: float,
    upper: float,
    x: float,
    tau: float,
    target: float,
    tol: float,
    rising: bool,
) -> float:
    while upper - lower > tol * max(1.0, upper):
        mid = 0.5 * (lower + upper)
        value = anti_phase_temporal_premium(x, mid, tau)
        if rising:
            if value < target:
                lower = mid
            else:
                upper = mid
        else:
            if value > target:
                lower = mid
            else:
                upper = mid
    return 0.5 * (lower + upper)
