"""Frozen climate helpers for the greater-snow-goose GPS lane."""

from __future__ import annotations

from datetime import date
from math import atan2, cos, isfinite, pi, radians, sin

CONTEXT_ORDER = (
    "southern_staging",
    "mid_arctic_staging",
    "northern_arctic_staging",
)

CONTEXT_WINDOWS = {
    "southern_staging": ((4, 1), (5, 15)),
    "mid_arctic_staging": ((5, 10), (5, 31)),
    "northern_arctic_staging": ((5, 20), (6, 5)),
}
TARGET_WINDOW = ((5, 30), (6, 15))


def training_years(focal_year: int, window_years: int = 20) -> tuple[int, ...]:
    """Calendar years strictly preceding the focal year."""

    focal = int(focal_year)
    window = int(window_years)
    if window < 15:
        raise ValueError("historical window must contain at least 15 years")
    return tuple(range(focal - window, focal))


def seasonal_window(context: str, year: int) -> tuple[date, date]:
    """Frozen route-context seasonal window."""

    if context not in CONTEXT_WINDOWS:
        raise ValueError("unknown frozen route context")
    (sm, sd), (em, ed) = CONTEXT_WINDOWS[context]
    return date(int(year), sm, sd), date(int(year), em, ed)


def target_window(year: int) -> tuple[date, date]:
    """Frozen Bylot target window."""

    (sm, sd), (em, ed) = TARGET_WINDOW
    return date(int(year), sm, sd), date(int(year), em, ed)


def initial_bearing_deg(
    lon1: float,
    lat1: float,
    lon2: float,
    lat2: float,
) -> float:
    """Great-circle initial bearing from point 1 to point 2."""

    values = [float(lon1), float(lat1), float(lon2), float(lat2)]
    if any(not isfinite(v) for v in values):
        raise ValueError("coordinates must be finite")
    lo1, la1, lo2, la2 = map(radians, values)
    dlon = lo2 - lo1
    x = sin(dlon) * cos(la2)
    y = cos(la1) * sin(la2) - sin(la1) * cos(la2) * cos(dlon)
    return (atan2(x, y) * 180.0 / pi + 360.0) % 360.0


def wind_support_ms(
    wind_speed_ms: float,
    wind_from_direction_deg: float,
    route_bearing_deg: float,
) -> float:
    """Project meteorological wind onto the route bearing.

    Meteorological direction is the direction *from* which wind blows.
    Therefore the wind-vector direction is +180 degrees from that value.
    Positive support is tailwind along the frozen next-route bearing.
    """

    speed = float(wind_speed_ms)
    direction_from = float(wind_from_direction_deg)
    bearing = float(route_bearing_deg)
    if not all(isfinite(v) for v in (speed, direction_from, bearing)):
        raise ValueError("wind inputs must be finite")
    if speed < 0.0:
        raise ValueError("wind speed must be non-negative")
    if not 0.0 <= direction_from <= 360.0:
        raise ValueError("wind direction must lie in [0, 360]")
    wind_to = (direction_from + 180.0) % 360.0
    delta = radians(wind_to - bearing)
    return speed * cos(delta)
