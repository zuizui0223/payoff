"""Fail-closed input gate for Japan multi-taxon climate/NDVI comparison.

This is an analysis-readiness validator, not a claim that environment data have
been downloaded. Keep station relocation, remote-sensing QA, and observation
process explicitly represented. Only join on station ID and calendar year.
"""
from __future__ import annotations

import datetime as dt
import math
from collections import Counter


class ClimateJoinNotAdmitted(ValueError):
    pass


def validate_environment_panel(rows: list[dict], *, min_site_years: int = 5) -> dict:
    required = {
        "source_file", "station_id", "year", "event_date", "day_of_year",
        "rm_original_code", "lat", "lon", "station_location_valid_for_year",
        "temperature_window_start", "temperature_window_end",
        "temperature_mean_c", "temperature_valid_days", "temperature_expected_days",
        "ndvi_window_start", "ndvi_window_end", "ndvi_qa_valid_fraction",
        "ndvi_value", "ndvi_product_version", "ndvi_pixel_area_m2",
        "source_station_metadata_id", "source_temperature_id",
        "source_ndvi_id",
    }
    keys = set()
    station_years = {}
    rm = Counter()
    for i, row in enumerate(rows):
        missing = required - row.keys()
        if missing:
            raise ClimateJoinNotAdmitted(f"row {i}: missing {sorted(missing)}")
        key = (str(row["source_file"]), str(row["station_id"]), int(row["year"]))
        if key in keys:
            raise ClimateJoinNotAdmitted(f"duplicate biological event key: {key}")
        keys.add(key)
        year = int(row["year"])
        event = dt.date.fromisoformat(row["event_date"])
        if event.year != year or event.timetuple().tm_yday != int(row["day_of_year"]):
            raise ClimateJoinNotAdmitted("event date/year/day-of-year mismatch")
        if row["station_location_valid_for_year"] is not True:
            raise ClimateJoinNotAdmitted("unverified station relocation/coordinate validity")
        lat, lon = float(row["lat"]), float(row["lon"])
        if not (24 <= lat <= 46.5 and 122 <= lon <= 154):
            raise ClimateJoinNotAdmitted("coordinate outside Japan coverage")
        if not all(str(row[k]).strip() for k in (
            "source_station_metadata_id", "source_temperature_id", "source_ndvi_id",
            "ndvi_product_version")):
            raise ClimateJoinNotAdmitted("missing source provenance")
        if not (float(row["ndvi_pixel_area_m2"]) > 0):
            raise ClimateJoinNotAdmitted("missing pixel area")
        t_start = dt.date.fromisoformat(row["temperature_window_start"])
        t_end = dt.date.fromisoformat(row["temperature_window_end"])
        n_start = dt.date.fromisoformat(row["ndvi_window_start"])
        n_end = dt.date.fromisoformat(row["ndvi_window_end"])
        if not (t_start <= t_end < event and n_start <= n_end < event):
            raise ClimateJoinNotAdmitted("future environmental information leakage")
        t_expected = int(row["temperature_expected_days"])
        t_valid = int(row["temperature_valid_days"])
        if t_expected != (t_end - t_start).days + 1 or not (0.9 * t_expected <= t_valid <= t_expected):
            raise ClimateJoinNotAdmitted("insufficient temperature coverage")
        if not (0.8 <= float(row["ndvi_qa_valid_fraction"]) <= 1):
            raise ClimateJoinNotAdmitted("insufficient NDVI QA")
        if not all(math.isfinite(float(row[k])) for k in ("temperature_mean_c", "ndvi_value")):
            raise ClimateJoinNotAdmitted("nonfinite predictor")
        if not (-0.2 <= float(row["ndvi_value"]) <= 1):
            raise ClimateJoinNotAdmitted("NDVI outside physical range")
        station_years.setdefault((row["source_file"], row["station_id"]), set()).add(year)
        rm[str(row["rm_original_code"])] += 1
    sites = {k: v for k, v in station_years.items() if len(v) >= min_site_years}
    if not sites:
        raise ClimateJoinNotAdmitted("no site/event with sufficient repeated years")
    return {
        "status": "ENVIRONMENTAL_JOIN_ADMITTED_FOR_PREDICTIVE_SCREEN",
        "joined_rows": len(rows),
        "distinct_source_station_year_keys": len(keys),
        "site_event_series_with_min_years": len(sites),
        "rm_codes_retained": dict(rm),
        "causal_information_use_identified": False,
        "bird_or_amphibian_fitness_identified": False,
    }
