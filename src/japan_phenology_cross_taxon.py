"""Real JMA cross-taxon phenology coupling with station and event fixed effects.

No weather/NDVI/biomass coefficient. Pair animal first-call or first-sighting
against plant flowering in the same station-year. The statistic is an
association of interannual anomalies, not causation, fitness, or synchrony.
"""
from __future__ import annotations
from collections import defaultdict
import math

def paired_station_year_anomaly_correlation(events: list[dict], *,
                                             group_a: str, group_b: str,
                                             min_shared_years: int = 8) -> dict:
    if group_a == group_b:
        raise ValueError("Different event groups required")
    # For each source-event × station, center DOY across observed years.
    series = defaultdict(dict)
    for r in events:
        taxon = r["source_taxon_guess"]
        if taxon not in (group_a, group_b):
            continue
        key = (r["source_file"], r["station_id"], taxon)
        year = int(r["year"])
        if year in series[key]:
            raise ValueError("Duplicate source-event/station/year")
        series[key][year] = float(r["day_of_year"])
    centered = {}
    for key, annual in series.items():
        if len(annual) < min_shared_years:
            continue
        mean = sum(annual.values()) / len(annual)
        centered[key] = {y: v - mean for y, v in annual.items()}
    by_station = defaultdict(lambda: {group_a: [], group_b: []})
    for (source, station, taxon), annual in centered.items():
        by_station[station][taxon].append((source, annual))
    paired = []
    station_count = 0
    series_pairs = 0
    for station, groups in by_station.items():
        if not groups[group_a] or not groups[group_b]:
            continue
        station_had = False
        for _, a in groups[group_a]:
            for _, b in groups[group_b]:
                years = sorted(set(a) & set(b))
                if len(years) < min_shared_years:
                    continue
                series_pairs += 1
                station_had = True
                # Each source event pair contributes one pair of anomalies
                # per shared year; report pseudo-replication explicitly.
                paired.extend((a[y], b[y]) for y in years)
        station_count += station_had
    n = len(paired)
    if n < 3:
        return {"status": "INSUFFICIENT_SHARED_STATION_YEARS",
                "station_count": station_count, "event_series_pairs": series_pairs,
                "paired_station_year_cells_not_independent": n}
    xa = [p[0] for p in paired]
    xb = [p[1] for p in paired]
    am = sum(xa)/n
    bm = sum(xb)/n
    sxx = sum((v-am)**2 for v in xa)
    syy = sum((v-bm)**2 for v in xb)
    sxy = sum((x-am)*(y-bm) for x,y in paired)
    if sxx <= 0 or syy <= 0:
        return {"status": "ZERO_ANOMALY_VARIANCE",
                "station_count": station_count, "event_series_pairs": series_pairs,
                "paired_station_year_cells_not_independent": n}
    return {"status": "EXPLORATORY_ANOMALY_CORRELATION_ONLY",
            "group_a": group_a, "group_b": group_b,
            "station_count": station_count,
            "event_series_pairs": series_pairs,
            "paired_station_year_cells_not_independent": n,
            "pooled_anomaly_pearson_r": round(sxy/math.sqrt(sxx*syy), 6),
            "confidence_interval_or_p_value": None,
            "observation_quality_codes_screened": False,
            "independent_weather_or_ndvi_predictor_fitted": False,
            "fitness_or_biomass_effect_identified": False}
