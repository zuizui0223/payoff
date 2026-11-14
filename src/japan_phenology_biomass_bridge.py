"""Source-faithful biomass versus greenness admission and integration.

No NDVI-to-biomass substitution. Biomass must be an independently measured
mass/area with dates, sampling effort and a named resource guild. No extrapolation
outside observed support; intervals and demand windows use calendar days.
"""
from __future__ import annotations

import datetime as dt
import math
from collections import defaultdict


class ResourceSourceNotAdmitted(ValueError):
    pass


def _date(x):
    return dt.date.fromisoformat(str(x))


def integrate_resource_biomass(samples: list[dict], *, window_start: str,
                               window_end: str, min_coverage_fraction: float = 0.8) -> dict:
    start, end = _date(window_start), _date(window_end)
    if start > end:
        raise ResourceSourceNotAdmitted("Demand window reversed")
    if len(samples) < 2:
        raise ResourceSourceNotAdmitted("Need repeated independent resource measurements")
    required = {"site_id", "resource_guild", "date", "biomass_g_m2",
                "sample_area_m2", "source_id", "sampling_effort_verified",
                "mass_basis", "independent_from_bird_outcome"}
    ids = set()
    points = []
    for r in samples:
        if required - r.keys():
            raise ResourceSourceNotAdmitted("Missing biomass source fields")
        if r["sampling_effort_verified"] is not True or r["independent_from_bird_outcome"] is not True:
            raise ResourceSourceNotAdmitted("Unverified effort or outcome-derived biomass")
        if r["mass_basis"] not in ("dry", "fresh"):
            raise ResourceSourceNotAdmitted("Unknown dry/fresh mass basis")
        if not str(r["source_id"]).strip() or not str(r["resource_guild"]).strip():
            raise ResourceSourceNotAdmitted("Unprovenanced resource")
        day = _date(r["date"])
        val = float(r["biomass_g_m2"])
        if not math.isfinite(val) or val < 0 or not (float(r["sample_area_m2"]) > 0):
            raise ResourceSourceNotAdmitted("Invalid biomass density or sample area")
        key = (r["site_id"], day)
        if key in ids:
            raise ResourceSourceNotAdmitted("Duplicate site-date resource record")
        ids.add(key)
        points.append((day, val, r))
    if len({(r["site_id"], r["resource_guild"], r["mass_basis"]) for _, _, r in points}) != 1:
        raise ResourceSourceNotAdmitted("Cannot pool sites, guilds or dry/fresh mass")
    points.sort()
    if points[0][0] > start or points[-1][0] < end:
        raise ResourceSourceNotAdmitted("Demand window not bracketed by biomass measurements")
    if any((b[0] - a[0]).days > 14 for a, b in zip(points, points[1:])):
        raise ResourceSourceNotAdmitted("Temporal sampling gaps >14 days")
    # Piecewise-linear interpolation, integrated only on the requested window.
    integral = 0.0
    observed_covered = 0
    for (d0, b0, _), (d1, b1, _) in zip(points, points[1:]):
        days = (d1 - d0).days
        if days <= 0:
            raise ResourceSourceNotAdmitted("Invalid temporal order")
        lo, hi = max(d0, start), min(d1, end)
        if lo >= hi:
            continue
        x0, x1 = (lo - d0).days / days, (hi - d0).days / days
        y0, y1 = b0 + (b1 - b0) * x0, b0 + (b1 - b0) * x1
        width = (hi - lo).days
        integral += width * (y0 + y1) / 2
        observed_covered += width
    window_days = (end - start).days
    if window_days <= 0 or observed_covered / window_days < min_coverage_fraction:
        raise ResourceSourceNotAdmitted("Insufficient demand-window coverage")
    return {
        "site_id": points[0][2]["site_id"],
        "resource_guild": points[0][2]["resource_guild"],
        "mass_basis": points[0][2]["mass_basis"],
        "source_id": points[0][2]["source_id"],
        "demand_window_start": start.isoformat(),
        "demand_window_end": end.isoformat(),
        "resource_exposure_g_day_m2": integral,
        "mean_resource_biomass_g_m2": integral / window_days,
        "sampling_dates": len(points),
        "interpolation": "piecewise_linear_no_extrapolation",
        "assimilated_energy_inferred": False,
        "fitness_effect_estimated": False,
    }


def biomass_source_gate(source: dict) -> str:
    if source.get("quantity_kind") == "NDVI":
        return "VEGETATION_GREENNESS_PROXY_NOT_BIOMASS"
    if source.get("quantity_kind") in ("count", "first_event_date", "peak_date"):
        return "NON_MASS_OBSERVATION"
    if source.get("quantity_kind") != "mass_per_area":
        return "UNCLASSIFIED_NOT_ADMITTED"
    required = ("units", "mass_basis", "sample_area", "sampling_dates",
                "source_id", "effort_verified", "raw_file_sha256")
    if any(not source.get(k) for k in required):
        return "MEASURED_BIOMASS_SOURCE_NOT_YET_VERIFIED"
    if source["units"] not in ("g/m2", "kg/ha") or source["mass_basis"] not in ("dry", "fresh"):
        return "UNSUPPORTED_BIOMASS_UNITS"
    return "MEASURED_BIOMASS_METADATA_ADMITTED"
