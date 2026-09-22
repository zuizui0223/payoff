"""Front-velocity geometry for movement–phenology macroecology.

For a timing surface T(x, y) measured in days and spatial coordinates in km,
the local gradient grad(T) has units day/km. The normal velocity of the
isochrone T(x,y)=t is

    v = grad(T) / ||grad(T)||^2,

with speed 1/||grad(T)|| in km/day.

This is the continuous counterpart of the local planar timing regressions used
in the Amaral et al. bird/green-up analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from analysis.movement_phenology.metrics import (
    directional_alignment,
    normalized_vector_mismatch,
    speed_ratio,
)


@dataclass(frozen=True)
class FrontVelocity:
    vx: float
    vy: float
    speed: float
    angle_rad: float


def front_velocity_from_timing_gradient(
    dt_dx_days_per_km: float,
    dt_dy_days_per_km: float,
) -> FrontVelocity:
    """Convert a nonzero timing-surface gradient to its local front velocity."""
    gx = float(dt_dx_days_per_km)
    gy = float(dt_dy_days_per_km)
    if not math.isfinite(gx) or not math.isfinite(gy):
        raise ValueError("timing gradients must be finite")
    norm2 = gx * gx + gy * gy
    if norm2 <= 0.0:
        raise ValueError("timing gradient must be nonzero")
    vx = gx / norm2
    vy = gy / norm2
    speed = math.sqrt(vx * vx + vy * vy)
    angle = math.atan2(vy, vx)
    return FrontVelocity(vx=vx, vy=vy, speed=speed, angle_rad=angle)


@dataclass(frozen=True)
class FrontMatch:
    speed_ratio: float
    log_speed_ratio: float
    alignment: float
    vector_mismatch: float


def compare_timing_fronts(
    animal_dt_dx: float,
    animal_dt_dy: float,
    environment_dt_dx: float,
    environment_dt_dy: float,
) -> FrontMatch:
    """Compare animal and environment timing fronts on a common spatial scale."""
    a = front_velocity_from_timing_gradient(animal_dt_dx, animal_dt_dy)
    e = front_velocity_from_timing_gradient(environment_dt_dx, environment_dt_dy)
    ratio = speed_ratio(a.speed, e.speed)
    align = directional_alignment(a.angle_rad, e.angle_rad)
    mismatch = normalized_vector_mismatch(
        a.speed, e.speed, a.angle_rad, e.angle_rad
    )
    return FrontMatch(
        speed_ratio=ratio,
        log_speed_ratio=math.log(ratio),
        alignment=align,
        vector_mismatch=mismatch,
    )



def normalized_phase_drift_from_timing_gradients(
    animal_dt_dx: float,
    animal_dt_dy: float,
    environment_dt_dx: float,
    environment_dt_dy: float,
) -> float:
    """Return dimensionless spatial drift of the animal-environment phase lag.

    This is ||grad(T_animal)-grad(T_environment)|| / ||grad(T_environment)||.
    It is zero when animal and environment timing surfaces differ only by a
    constant phase offset.
    """
    ga_x = float(animal_dt_dx)
    ga_y = float(animal_dt_dy)
    ge_x = float(environment_dt_dx)
    ge_y = float(environment_dt_dy)
    vals = (ga_x, ga_y, ge_x, ge_y)
    if not all(math.isfinite(z) for z in vals):
        raise ValueError("timing gradients must be finite")
    env_norm = math.hypot(ge_x, ge_y)
    if env_norm <= 0.0:
        raise ValueError("environment timing gradient must be nonzero")
    return math.hypot(ga_x - ge_x, ga_y - ge_y) / env_norm


def normalized_phase_drift_from_speed_ratio(
    speed_ratio_value: float,
    alignment_value: float,
) -> float:
    """Equivalent phase-drift diagnostic from speed ratio and alignment."""
    u = float(speed_ratio_value)
    a = float(alignment_value)
    if not math.isfinite(u) or not math.isfinite(a):
        raise ValueError("speed ratio and alignment must be finite")
    if u <= 0.0:
        raise ValueError("speed ratio must be positive")
    if a < -1.0 or a > 1.0:
        raise ValueError("alignment must lie in [-1, 1]")
    value = 1.0 + 1.0 / (u * u) - 2.0 * a / u
    return math.sqrt(max(0.0, value))
