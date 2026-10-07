"""Deterministic stopover detection for the public barnacle-goose reanalysis.

This implementation follows the procedure described by van Wijk et al. (2012),
which is the method cited by Kölzsch et al. (2015):

- identify clusters of successive positions whose pairwise displacement does
  not exceed 30 km;
- retain clusters occupied for at least 48 h;
- allow one >30-km detour if the bird returns to the preceding cluster within
  a short interval;
- a second detour ends the site.

van Wijk et al. describe an 8-h return window; the closely related De Boer et
al. analysis of these barnacle-goose tracks describes 6 h.  The primary
PAYOFF reconstruction uses the original 8-h van-Wijk value and keeps the
window explicit for sensitivity analysis.

No flyway-specific threshold is permitted.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import asin, cos, isfinite, pi, sin, sqrt
from typing import Sequence


@dataclass(frozen=True)
class TrackPoint:
    timestamp: datetime
    latitude: float
    longitude: float


@dataclass(frozen=True)
class Stopover:
    start: datetime
    end: datetime
    center_latitude: float
    center_longitude: float
    inlier_points: int
    detour_points: int = 0

    @property
    def duration_hours(self) -> float:
        return (self.end - self.start).total_seconds() / 3600.0


def haversine_km(
    latitude_a: float,
    longitude_a: float,
    latitude_b: float,
    longitude_b: float,
) -> float:
    """Great-circle distance in kilometres."""

    values = (
        float(latitude_a),
        float(longitude_a),
        float(latitude_b),
        float(longitude_b),
    )
    if any(not isfinite(x) for x in values):
        raise ValueError("coordinates must be finite")

    lat1, lon1, lat2, lon2 = values
    radians = pi / 180.0
    p1 = lat1 * radians
    p2 = lat2 * radians
    dp = (lat2 - lat1) * radians
    dl = (lon2 - lon1) * radians
    a = (
        sin(dp / 2.0) ** 2
        + cos(p1) * cos(p2) * sin(dl / 2.0) ** 2
    )
    return 2.0 * 6371.0 * asin(min(1.0, sqrt(a)))


def _validate_points(points: Sequence[TrackPoint]) -> tuple[TrackPoint, ...]:
    if not points:
        return ()
    ordered = tuple(sorted(points, key=lambda x: x.timestamp))
    awareness = ordered[0].timestamp.tzinfo is not None
    for point in ordered:
        if (point.timestamp.tzinfo is not None) != awareness:
            raise ValueError("track timestamp timezone awareness must be consistent")
        if not isfinite(float(point.latitude)) or not isfinite(float(point.longitude)):
            raise ValueError("track coordinates must be finite")
    return ordered


def detect_stopovers(
    points: Sequence[TrackPoint],
    *,
    radius_km: float = 30.0,
    minimum_duration_hours: float = 48.0,
    maximum_detours: int = 1,
    maximum_detour_hours: float = 8.0,
) -> tuple[Stopover, ...]:
    """Detect stopovers from successive-position displacement clusters.

    Normal cluster continuation requires displacement <= radius_km from the
    previous in-cluster position.

    A detour is one position more than radius_km away.  It is absorbed into the
    same stopover only if:

    - the maximum_detours allowance has not already been used;
    - the following position returns within radius_km of the last in-cluster
      position; and
    - elapsed time from the last in-cluster position to that return is no more
      than maximum_detour_hours.

    The detour position itself is excluded from the site-center calculation.

    After a qualifying cluster is emitted, scanning resumes after its final
    returned/in-cluster point.  Clusters are not post-hoc merged.
    """

    radius = float(radius_km)
    minimum = float(minimum_duration_hours)
    detour_hours = float(maximum_detour_hours)
    detour_limit = int(maximum_detours)

    if not isfinite(radius) or radius <= 0.0:
        raise ValueError("radius_km must be finite and positive")
    if not isfinite(minimum) or minimum <= 0.0:
        raise ValueError("minimum_duration_hours must be finite and positive")
    if not isfinite(detour_hours) or detour_hours < 0.0:
        raise ValueError("maximum_detour_hours must be finite and non-negative")
    if detour_limit < 0:
        raise ValueError("maximum_detours must be non-negative")

    ordered = _validate_points(points)
    if len(ordered) < 2:
        return ()

    stops: list[Stopover] = []
    i = 0

    while i < len(ordered) - 1:
        inliers = [ordered[i]]
        detours_used = 0
        j = i + 1
        last_consumed = i

        while j < len(ordered):
            previous = inliers[-1]
            current = ordered[j]
            if (
                haversine_km(
                    previous.latitude,
                    previous.longitude,
                    current.latitude,
                    current.longitude,
                )
                <= radius
            ):
                inliers.append(current)
                last_consumed = j
                j += 1
                continue

            # Candidate single-position detour.
            if detours_used < detour_limit and j + 1 < len(ordered):
                returned = ordered[j + 1]
                elapsed = (
                    returned.timestamp - previous.timestamp
                ).total_seconds() / 3600.0
                returned_to_cluster = (
                    haversine_km(
                        previous.latitude,
                        previous.longitude,
                        returned.latitude,
                        returned.longitude,
                    )
                    <= radius
                )
                if returned_to_cluster and elapsed <= detour_hours:
                    detours_used += 1
                    inliers.append(returned)
                    last_consumed = j + 1
                    j += 2
                    continue

            break

        duration = (
            inliers[-1].timestamp - inliers[0].timestamp
        ).total_seconds() / 3600.0

        if len(inliers) >= 2 and duration >= minimum:
            center_lat = sum(x.latitude for x in inliers) / len(inliers)
            center_lon = sum(x.longitude for x in inliers) / len(inliers)
            stops.append(
                Stopover(
                    start=inliers[0].timestamp,
                    end=inliers[-1].timestamp,
                    center_latitude=center_lat,
                    center_longitude=center_lon,
                    inlier_points=len(inliers),
                    detour_points=detours_used,
                )
            )
            i = last_consumed + 1
        else:
            i += 1

    return tuple(stops)
