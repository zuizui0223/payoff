"""Deterministic stopover detection for the public barnacle-goose reanalysis.

The detector operationalizes the Kölzsch et al. stopover definition:

- residence within a 30-km radius;
- longer than 48 h;
- maximally one outlier position.

The original paper did not publish a software implementation.  This module is a
frozen, conservative reconstruction for the PAYOFF-B public-data reanalysis.

To avoid splitting one 30-km-radius stay solely because different observed
anchor points are selected, temporally adjacent candidate stays are merged when
their centers are no more than 2 * radius apart.  The 60-km default is thus
geometrically derived from the declared 30-km site radius rather than tuned to
match published stop counts.
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
    maximum_outliers: int = 1,
    merge_gap_hours: float = 48.0,
) -> tuple[Stopover, ...]:
    """Detect stopovers with a frozen observed-anchor reconstruction.

    Candidate search
    ----------------
    At each unused track position, use that observed location as a conservative
    candidate site anchor. Extend forward until more than maximum_outliers
    positions fall outside radius_km. The candidate qualifies only when the
    first-to-last inlier interval reaches minimum_duration_hours.

    Adjacent-candidate merge
    ------------------------
    Two consecutive candidates are merged when:

    - the temporal gap is <= merge_gap_hours; and
    - candidate centers are <= 2 * radius_km apart.

    If both candidates can arise from one true 30-km-radius site, their centers
    can be at most 60 km apart. This merge prevents artificial subdivision
    caused by choosing a different observed anchor within the same site.

    This is an approximation to the published site determination, not a claim
    that it reproduces unpublished manual decisions exactly.
    """

    radius = float(radius_km)
    minimum = float(minimum_duration_hours)
    merge_gap = float(merge_gap_hours)
    outlier_limit = int(maximum_outliers)

    if not isfinite(radius) or radius <= 0.0:
        raise ValueError("radius_km must be finite and positive")
    if not isfinite(minimum) or minimum <= 0.0:
        raise ValueError("minimum_duration_hours must be finite and positive")
    if not isfinite(merge_gap) or merge_gap < 0.0:
        raise ValueError("merge_gap_hours must be finite and non-negative")
    if outlier_limit < 0:
        raise ValueError("maximum_outliers must be non-negative")

    ordered = _validate_points(points)
    if len(ordered) < 2:
        return ()

    candidates: list[Stopover] = []
    i = 0
    while i < len(ordered) - 1:
        anchor = ordered[i]
        outliers = 0
        last_inlier_index = i
        inliers = [anchor]

        for j in range(i + 1, len(ordered)):
            point = ordered[j]
            distance = haversine_km(
                anchor.latitude,
                anchor.longitude,
                point.latitude,
                point.longitude,
            )
            if distance > radius:
                outliers += 1
                if outliers > outlier_limit:
                    break
            else:
                last_inlier_index = j
                inliers.append(point)

        duration = (
            ordered[last_inlier_index].timestamp - anchor.timestamp
        ).total_seconds() / 3600.0

        if last_inlier_index > i and duration >= minimum:
            center_lat = sum(x.latitude for x in inliers) / len(inliers)
            center_lon = sum(x.longitude for x in inliers) / len(inliers)
            candidates.append(
                Stopover(
                    start=anchor.timestamp,
                    end=ordered[last_inlier_index].timestamp,
                    center_latitude=center_lat,
                    center_longitude=center_lon,
                    inlier_points=len(inliers),
                )
            )
            i = last_inlier_index + 1
        else:
            i += 1

    merged: list[Stopover] = []
    for current in candidates:
        if not merged:
            merged.append(current)
            continue

        previous = merged[-1]
        gap = (current.start - previous.end).total_seconds() / 3600.0
        center_distance = haversine_km(
            previous.center_latitude,
            previous.center_longitude,
            current.center_latitude,
            current.center_longitude,
        )

        if gap <= merge_gap and center_distance <= 2.0 * radius:
            total_points = previous.inlier_points + current.inlier_points
            center_lat = (
                previous.center_latitude * previous.inlier_points
                + current.center_latitude * current.inlier_points
            ) / total_points
            center_lon = (
                previous.center_longitude * previous.inlier_points
                + current.center_longitude * current.inlier_points
            ) / total_points
            merged[-1] = Stopover(
                start=previous.start,
                end=max(previous.end, current.end),
                center_latitude=center_lat,
                center_longitude=center_lon,
                inlier_points=total_points,
            )
        else:
            merged.append(current)

    return tuple(merged)
