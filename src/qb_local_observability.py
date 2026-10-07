"""Local vegetation-phase observability for PAYOFF-B q_B.

This module is environment-only. It does not read goose phase error, stopover
duration, lambda, or actuator responses.

Primary q_B:
    local NDVI ~ year intercept + b * days_from_ERA5_spring

    J_B = b^2 / sigma^2
    Q_B = sample-z(log J_B) across the frozen origin-region panel.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import asin, atan2, cos, degrees, isfinite, log, radians, sin, sqrt
from statistics import median
from typing import Iterable, Mapping, Sequence


EARTH_RADIUS_KM = 6371.0088


@dataclass(frozen=True)
class RegionCenter:
    flyway: str
    region: str
    latitude: float
    longitude: float

    @property
    def region_key(self) -> str:
        return f"{self.flyway}:{self.region}"


@dataclass(frozen=True)
class LatticePoint:
    region_key: str
    point_id: str
    latitude: float
    longitude: float
    bearing_degrees: float | None
    distance_km: float


@dataclass(frozen=True)
class PixelNDVI:
    point_id: str
    region_key: str
    year: int
    doy: int
    ndvi: float
    quality_good: bool


@dataclass(frozen=True)
class RegionComposite:
    region_key: str
    year: int
    doy: int
    ndvi_median: float
    valid_points: int


@dataclass(frozen=True)
class LocalObservabilityFit:
    region_key: str
    admitted_years: int
    pooled_observations: int
    slope_ndvi_per_day: float
    residual_sd: float
    phase_resolution_sd_days: float
    fisher_information: float
    log_fisher_information: float
    q_b_z: float | None = None


def destination_point(
    latitude: float,
    longitude: float,
    *,
    bearing_degrees: float,
    distance_km: float,
) -> tuple[float, float]:
    """Move a point along a great-circle bearing by a fixed distance."""

    lat = float(latitude)
    lon = float(longitude)
    bearing = float(bearing_degrees)
    distance = float(distance_km)
    if not all(isfinite(v) for v in (lat, lon, bearing, distance)):
        raise ValueError("coordinates, bearing and distance must be finite")
    if not -90.0 <= lat <= 90.0 or not -180.0 <= lon <= 180.0:
        raise ValueError("input coordinates outside WGS84 bounds")
    if distance < 0.0:
        raise ValueError("distance_km must be non-negative")

    phi1 = radians(lat)
    lam1 = radians(lon)
    theta = radians(bearing % 360.0)
    delta = distance / EARTH_RADIUS_KM

    sin_phi2 = (
        sin(phi1) * cos(delta)
        + cos(phi1) * sin(delta) * cos(theta)
    )
    phi2 = asin(max(-1.0, min(1.0, sin_phi2)))
    y = sin(theta) * sin(delta) * cos(phi1)
    x = cos(delta) - sin(phi1) * sin(phi2)
    lam2 = lam1 + atan2(y, x)

    out_lon = ((degrees(lam2) + 180.0) % 360.0) - 180.0
    return degrees(phi2), out_lon


def build_region_lattice(
    region: RegionCenter,
    *,
    radial_distance_km: float = 4.0,
    bearings_degrees: Sequence[float] = (
        0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0
    ),
) -> tuple[LatticePoint, ...]:
    """Return deterministic center + radial points for one frozen region."""

    key = region.region_key
    points = [
        LatticePoint(
            region_key=key,
            point_id=f"{region.flyway}_{region.region}_C",
            latitude=float(region.latitude),
            longitude=float(region.longitude),
            bearing_degrees=None,
            distance_km=0.0,
        )
    ]
    for bearing in bearings_degrees:
        lat, lon = destination_point(
            region.latitude,
            region.longitude,
            bearing_degrees=float(bearing),
            distance_km=radial_distance_km,
        )
        label = f"B{int(round(float(bearing))) % 360:03d}"
        points.append(
            LatticePoint(
                region_key=key,
                point_id=f"{region.flyway}_{region.region}_{label}",
                latitude=lat,
                longitude=lon,
                bearing_degrees=float(bearing),
                distance_km=float(radial_distance_km),
            )
        )
    return tuple(points)


def build_appeears_manifest(
    regions: Iterable[RegionCenter],
    *,
    years: Sequence[int],
    radial_distance_km: float = 4.0,
) -> dict:
    """Build year-scoped MOD09Q1.061 point tasks for all frozen q_B regions."""

    region_rows = tuple(regions)
    if not region_rows:
        raise ValueError("at least one region is required")
    if not years:
        raise ValueError("at least one year is required")

    points: list[LatticePoint] = []
    for region in region_rows:
        points.extend(
            build_region_lattice(
                region,
                radial_distance_km=radial_distance_km,
            )
        )

    layers = [
        {"product": "MOD09Q1.061", "layer": "sur_refl_b01"},
        {"product": "MOD09Q1.061", "layer": "sur_refl_b02"},
        {"product": "MOD09Q1.061", "layer": "sur_refl_qc_250m"},
        {"product": "MOD09Q1.061", "layer": "sur_refl_state_250m"},
    ]

    tasks = []
    for year in sorted({int(y) for y in years}):
        coordinates = [
            {
                "id": p.point_id,
                "category": p.region_key,
                "latitude": p.latitude,
                "longitude": p.longitude,
            }
            for p in points
        ]
        tasks.append(
            {
                "year": year,
                "part": 1,
                "cell_count": len(points),
                "task": {
                    "task_type": "point",
                    "task_name": f"payoff_qb_mod09q1_{year}",
                    "params": {
                        "dates": [
                            {
                                "startDate": f"01-01-{year}",
                                "endDate": f"12-31-{year}",
                            }
                        ],
                        "layers": layers,
                        "coordinates": coordinates,
                    },
                },
            }
        )

    return {
        "status": "payoff_b_qb_appeears_manifest_v1",
        "environment_only": True,
        "product": "MOD09Q1.061",
        "years": sorted({int(y) for y in years}),
        "region_count": len(region_rows),
        "points_per_region": len(points) // len(region_rows),
        "total_points": len(points),
        "task_count": len(tasks),
        "layers": layers,
        "points": [
            {
                "region_key": p.region_key,
                "point_id": p.point_id,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "bearing_degrees": p.bearing_degrees,
                "distance_km": p.distance_km,
            }
            for p in points
        ],
        "tasks": tasks,
        "claim_boundary": (
            "environmental extraction only; no goose behavior or phase outcome"
        ),
    }


def aggregate_region_composites(
    rows: Iterable[PixelNDVI],
    *,
    min_valid_points: int = 5,
) -> tuple[RegionComposite, ...]:
    """Median NDVI across fixed lattice points for each region/date."""

    if min_valid_points < 1:
        raise ValueError("min_valid_points must be positive")
    grouped: dict[tuple[str, int, int], list[float]] = {}
    for row in rows:
        if not row.quality_good:
            continue
        value = float(row.ndvi)
        if not isfinite(value) or not -1.0 <= value <= 1.0:
            continue
        key = (str(row.region_key), int(row.year), int(row.doy))
        grouped.setdefault(key, []).append(value)

    output: list[RegionComposite] = []
    for (region_key, year, doy), values in sorted(grouped.items()):
        if len(values) < min_valid_points:
            continue
        output.append(
            RegionComposite(
                region_key=region_key,
                year=year,
                doy=doy,
                ndvi_median=float(median(values)),
                valid_points=len(values),
            )
        )
    return tuple(output)


def fit_region_observability(
    rows: Iterable[RegionComposite],
    spring_onset_doy: Mapping[tuple[str, int], float],
    *,
    phase_window_days: float = 24.0,
    min_dates_per_year: int = 4,
    min_years: int = 8,
    min_pooled_observations: int = 40,
) -> tuple[LocalObservabilityFit, ...]:
    """Fit year-FE local NDVI slope and convert it to phase information."""

    data = tuple(rows)
    region_keys = sorted({row.region_key for row in data})
    fits: list[LocalObservabilityFit] = []

    for region_key in region_keys:
        by_year: dict[int, list[tuple[float, float]]] = {}
        for row in data:
            if row.region_key != region_key:
                continue
            onset = spring_onset_doy.get((region_key, row.year))
            if onset is None or not isfinite(float(onset)):
                continue
            tau = float(row.doy) - float(onset)
            if abs(tau) > phase_window_days:
                continue
            by_year.setdefault(row.year, []).append(
                (tau, float(row.ndvi_median))
            )

        admitted = {
            year: values
            for year, values in by_year.items()
            if len(values) >= min_dates_per_year
        }
        if len(admitted) < min_years:
            raise ValueError(
                f"{region_key}: admitted years {len(admitted)} < {min_years}"
            )
        pooled_n = sum(len(values) for values in admitted.values())
        if pooled_n < min_pooled_observations:
            raise ValueError(
                f"{region_key}: pooled observations {pooled_n} "
                f"< {min_pooled_observations}"
            )

        numerator = 0.0
        denominator = 0.0
        centered: dict[int, list[tuple[float, float]]] = {}
        for year, values in admitted.items():
            mean_tau = sum(v[0] for v in values) / len(values)
            mean_y = sum(v[1] for v in values) / len(values)
            centered[year] = []
            for tau, y in values:
                tc = tau - mean_tau
                yc = y - mean_y
                centered[year].append((tc, yc))
                numerator += tc * yc
                denominator += tc * tc

        if denominator <= 0.0:
            raise ValueError(f"{region_key}: no within-year phase variation")
        slope = numerator / denominator
        if abs(slope) <= 1e-15:
            raise ValueError(f"{region_key}: local NDVI slope is zero")

        sse = 0.0
        for values in centered.values():
            for tc, yc in values:
                residual = yc - slope * tc
                sse += residual * residual

        df = pooled_n - len(admitted) - 1
        if df <= 0:
            raise ValueError(f"{region_key}: non-positive residual df")
        sigma = sqrt(sse / df)
        if not isfinite(sigma) or sigma <= 0.0:
            raise ValueError(f"{region_key}: residual SD must be positive")

        phase_sd = sigma / abs(slope)
        fisher = (slope * slope) / (sigma * sigma)
        fits.append(
            LocalObservabilityFit(
                region_key=region_key,
                admitted_years=len(admitted),
                pooled_observations=pooled_n,
                slope_ndvi_per_day=slope,
                residual_sd=sigma,
                phase_resolution_sd_days=phase_sd,
                fisher_information=fisher,
                log_fisher_information=log(fisher),
            )
        )

    if len(fits) < 2:
        raise ValueError("at least two fitted regions are required for z scaling")
    logs = [fit.log_fisher_information for fit in fits]
    mean_log = sum(logs) / len(logs)
    sample_var = sum((value - mean_log) ** 2 for value in logs) / (len(logs) - 1)
    if sample_var <= 0.0:
        raise ValueError("log Fisher information has zero between-region variance")
    sample_sd = sqrt(sample_var)

    return tuple(
        LocalObservabilityFit(
            **{
                **fit.__dict__,
                "q_b_z": (fit.log_fisher_information - mean_log) / sample_sd,
            }
        )
        for fit in fits
    )
