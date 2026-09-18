#!/usr/bin/env python3
"""Reconstruct van Toor et al. (2021) spring trajectories and staging sites.

This uses:
- the public Zenodo hourly relocation union corresponding to the four source
  files listed in the published Supplement;
- the published start/end and 50.184-km staging rules;
- the published fitted 4-state HMM parameters via wigeon_hmm.py.

The first goal is replication of published movement summaries. Controller
inference remains gated until that replication is adequate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import CRS, Geod, Transformer

from analysis.movement_phenology.wigeon_hmm import (
    STATE_NAMES,
    movement_streams,
    solar_time_hours,
    viterbi_published,
)


SOURCE = Path("outputs/movement_phenology/stage3_wigeon_raw_subset.csv")
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

MEAN_AIRSPEED_MS = 18.5
SD_AIRSPEED_MS = 2.28
THRESHOLD_V_MS = MEAN_AIRSPEED_MS - 2.0 * SD_AIRSPEED_MS
THRESHOLD_D_KM = THRESHOLD_V_MS * 3.6  # 50.184 km in one hour
ORIGINAL_DATA_FREEZE = pd.Timestamp("2020-06-01 23:59:59", tz="UTC")
GEOD = Geod(ellps="WGS84")


def geodesic_km(lon1, lat1, lon2, lat2):
    return GEOD.inv(float(lon1), float(lat1), float(lon2), float(lat2))[2] / 1000.0


def tpeqd_x(track: pd.DataFrame, subset: pd.DataFrame) -> np.ndarray:
    """Match the Supplement's per-track two-point-equidistant x coordinate."""
    minlat = float(track["lat"].min())
    maxlat = float(track["lat"].max())
    minlon = float(track["lon"].min())
    maxlon = float(track["lon"].max())
    if minlat == maxlat and minlon == maxlon:
        return np.zeros(len(subset), dtype=float)
    crs = CRS.from_proj4(
        f"+proj=tpeqd +lat_1={minlat} +lon_1={minlon} "
        f"+lat_2={maxlat} +lon_2={maxlon} "
        "+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
    )
    tr = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    x, _ = tr.transform(subset["lon"].to_numpy(), subset["lat"].to_numpy())
    return np.asarray(x, dtype=float)


def cumulative_track_distance_km(track: pd.DataFrame) -> float:
    if len(track) < 2:
        return 0.0
    values = 0.0
    lon = track["lon"].to_numpy()
    lat = track["lat"].to_numpy()
    for i in range(len(track) - 1):
        if np.all(np.isfinite([lon[i], lat[i], lon[i + 1], lat[i + 1]])):
            values += geodesic_km(lon[i], lat[i], lon[i + 1], lat[i + 1])
    return values


def prepare_track(x: pd.DataFrame):
    x = x.sort_values("time").drop_duplicates("time").copy()
    if len(x) < 3 or float(x["ground_speed"].max()) <= THRESHOLD_V_MS:
        return None, "NO_MIGRATORY_SPEED"

    spring_start = x[x["time"].dt.month.isin([2, 3, 4])]
    spring_end = x[x["time"].dt.month.isin([5, 6, 7])]
    if spring_start.empty:
        return None, "NO_FEB_APR"
    if spring_end.empty:
        return None, "NO_MAY_JUL"

    try:
        sx = tpeqd_x(x, spring_start)
        ex = tpeqd_x(x, spring_end)
    except Exception:
        return None, "PROJECTION_FAIL"

    start_row = spring_start.iloc[int(np.nanargmin(sx))]
    end_row = spring_end.iloc[int(np.nanargmax(ex))]
    endpoint_km = geodesic_km(
        start_row.lon, start_row.lat, end_row.lon, end_row.lat
    )
    if endpoint_km <= THRESHOLD_D_KM:
        return None, "ENDPOINT_DISTANCE"

    dstart = np.array(
        [
            geodesic_km(start_row.lon, start_row.lat, lo, la)
            for lo, la in zip(x.lon, x.lat)
        ]
    )
    dend = np.array(
        [
            geodesic_km(end_row.lon, end_row.lat, lo, la)
            for lo, la in zip(x.lon, x.lat)
        ]
    )
    near_start = x.loc[dstart < THRESHOLD_D_KM, "time"]
    near_end = x.loc[dend < THRESHOLD_D_KM, "time"]
    if near_start.empty or near_end.empty:
        return None, "NO_THRESHOLD_DAY"

    # Exact Supplement logic uses the last date within threshold of start and
    # first date within threshold of destination.
    start_day = near_start.dt.date.max()
    end_day = near_end.dt.date.min()
    if start_day > end_day:
        return None, "START_AFTER_END"

    x["d2start_km"] = dstart
    x["d2end_km"] = dend
    mig = x[
        (x["time"].dt.date >= start_day)
        & (x["time"].dt.date <= end_day)
    ].copy()
    if len(mig) < 3:
        return None, "TOO_FEW_MIGRATION_FIXES"

    meta = {
        "endpoint_distance_km": endpoint_km,
        "start_day": str(start_day),
        "end_day": str(end_day),
        "start_lon": float(start_row.lon),
        "start_lat": float(start_row.lat),
        "end_lon": float(end_row.lon),
        "end_lat": float(end_row.lat),
    }
    return (mig, meta), "PASS"


def classify_track(mig: pd.DataFrame) -> pd.DataFrame:
    mig = mig.sort_values("time").reset_index(drop=True).copy()
    step, angle = movement_streams(mig["lon"], mig["lat"])
    mig["step_km"] = step
    mig["step_sqrt"] = np.sqrt(step)
    mig["angle_rad"] = angle

    solar = []
    for t, lon in zip(mig["time"], mig["lon"]):
        solar.append(solar_time_hours(t.to_pydatetime(), float(lon)))
    mig["solar_time"] = solar
    mig["state"] = viterbi_published(
        mig["step_sqrt"], mig["angle_rad"], mig["solar_time"]
    )
    mig["state_name"] = [STATE_NAMES[int(s) - 1] for s in mig["state"]]
    return mig


def segment_staging(classified: pd.DataFrame) -> pd.DataFrame:
    # Exact supplement alternative: remove state 4, then start a new segment
    # whenever consecutive retained locations are > threshold.d apart.
    d = classified[classified["state"] != 4].copy()
    if d.empty:
        return pd.DataFrame()
    d = d.sort_values("time").reset_index(drop=True)
    gaps = np.zeros(len(d), dtype=float)
    for i in range(1, len(d)):
        gaps[i] = geodesic_km(
            d.lon.iloc[i - 1], d.lat.iloc[i - 1],
            d.lon.iloc[i], d.lat.iloc[i],
        )
    d["distance_from_prev_nonmigratory_km"] = gaps
    d["segment"] = 1 + np.cumsum(gaps > THRESHOLD_D_KM)

    rows = []
    for segment, s in d.groupby("segment"):
        s = s.sort_values("time")
        arrival = s["time"].min()
        last = s["time"].max()
        duration_days = (
            last.normalize() - arrival.normalize()
        ).total_seconds() / 86400.0
        rows.append(
            {
                "segment": int(segment),
                "arrival": arrival,
                "last_loc": last,
                "julian": int(arrival.dayofyear),
                "duration_days": duration_days,
                "lon": float(s["lon"].median()),
                "lat": float(s["lat"].median()),
                "d2start_km": float(s["d2start_km"].iloc[0]),
                "n_nonmigratory_fixes": int(len(s)),
            }
        )
    out = pd.DataFrame(rows)

    # Published arrival filter: staging site must be beyond threshold from the
    # starting location.
    out = out[out["d2start_km"] > THRESHOLD_D_KM].copy()

    # Published code manually removes one within-winter movement that sat just
    # outside the threshold (~52 km) in February. Current public release lacks
    # the original local identifier, so reproduce the biological condition
    # transparently rather than guessing the ID mapping.
    within_winter = (
        (pd.to_datetime(out["arrival"]).dt.month == 2)
        & (out["d2start_km"] <= 52.5)
    )
    out["manual_within_winter_exclusion"] = within_winter
    out = out[~within_winter].copy()
    return out


def main():
    if not SOURCE.exists():
        raise SystemExit(f"Missing source union: {SOURCE}")
    raw = pd.read_csv(SOURCE, low_memory=False)
    ren = {
        "individual.id": "individual_id",
        "timestamp": "time",
        "location.long": "lon",
        "location.lat": "lat",
        "ground.speed": "ground_speed",
        "study.name": "study_name",
    }
    missing = [c for c in ren if c not in raw.columns]
    if missing:
        raise SystemExit(f"Missing source columns: {missing}")
    raw = raw.rename(columns=ren)
    raw["time"] = pd.to_datetime(raw["time"], errors="coerce", utc=True)
    for c in ("lon", "lat", "ground_speed"):
        raw[c] = pd.to_numeric(raw[c], errors="coerce")
    raw = raw.dropna(
        subset=["individual_id", "time", "lon", "lat", "ground_speed"]
    ).copy()

    # Reconstruct the paper's download freeze. Later public observations are
    # retained in the source audit but excluded from the replication lane.
    raw = raw[raw["time"] <= ORIGINAL_DATA_FREEZE].copy()
    raw["year"] = raw["time"].dt.year

    audits = []
    states_all = []
    staging_all = []
    track_rows = []

    for (ind, year), x in raw.groupby(["individual_id", "year"]):
        prepared, status = prepare_track(x)
        audit = {
            "individual_id": str(ind),
            "year": int(year),
            "n_source_rows": int(len(x)),
            "max_ground_speed_ms": float(x["ground_speed"].max()),
            "status": status,
        }
        if status != "PASS":
            audits.append(audit)
            continue

        mig, meta = prepared
        audit.update(meta)
        audit["n_migration_rows"] = int(len(mig))
        audits.append(audit)

        classified = classify_track(mig)
        classified["individual_id"] = str(ind)
        classified["year"] = int(year)
        states_all.append(classified)

        stages = segment_staging(classified)
        if not stages.empty:
            stages["individual_id"] = str(ind)
            stages["year"] = int(year)
            stages = stages.sort_values("arrival").reset_index(drop=True)
            # Between-staging distance and travel time as in Supplement.
            dist_btw = []
            time_btw = []
            speed = []
            for i in range(len(stages)):
                if i < len(stages) - 1:
                    dk = geodesic_km(
                        stages.lon.iloc[i], stages.lat.iloc[i],
                        stages.lon.iloc[i + 1], stages.lat.iloc[i + 1],
                    )
                    td = (
                        stages.arrival.iloc[i + 1]
                        - stages.last_loc.iloc[i]
                    ).total_seconds() / 86400.0
                    dist_btw.append(dk)
                    time_btw.append(td)
                    speed.append(dk / td if td > 0 else np.nan)
                else:
                    dist_btw.append(np.nan)
                    time_btw.append(np.nan)
                    speed.append(np.nan)
            stages["dist_btw_km"] = dist_btw
            stages["time_btw_days"] = time_btw
            stages["speed_btw_km_day"] = speed
            staging_all.append(stages)

        total_dist = cumulative_track_distance_km(classified)
        duration_days = (
            classified.time.max() - classified.time.min()
        ).total_seconds() / 86400.0
        track_rows.append(
            {
                "individual_id": str(ind),
                "year": int(year),
                "endpoint_distance_km": meta["endpoint_distance_km"],
                "cumulative_migration_distance_km": total_dist,
                "migration_duration_days": duration_days,
                "migration_speed_km_day": (
                    total_dist / duration_days if duration_days > 0 else np.nan
                ),
                "n_migration_fixes": int(len(classified)),
                "fraction_state4_migratory": float(
                    np.mean(classified["state"] == 4)
                ),
                "n_staging_sites": int(len(stages)) if not stages.empty else 0,
            }
        )

    audit_df = pd.DataFrame(audits)
    tracks = pd.DataFrame(track_rows)
    states = pd.concat(states_all, ignore_index=True) if states_all else pd.DataFrame()
    staging = (
        pd.concat(staging_all, ignore_index=True)
        if staging_all else pd.DataFrame()
    )

    audit_df.to_csv(OUT / "stage3_wigeon_track_filter_audit.csv", index=False)
    tracks.to_csv(OUT / "stage3_wigeon_track_summary.csv", index=False)
    if not states.empty:
        states.to_csv(OUT / "stage3_wigeon_hmm_states.csv", index=False)
    if not staging.empty:
        staging.to_csv(OUT / "stage3_wigeon_staging_sites.csv", index=False)

    def q(x, p):
        return float(np.nanquantile(pd.to_numeric(x, errors="coerce"), p))

    observed = {
        "n_tracks": int(len(tracks)),
        "n_individuals": int(tracks["individual_id"].nunique()) if len(tracks) else 0,
        "n_staging_events": int(len(staging)),
        "endpoint_distance_median_km": q(tracks["endpoint_distance_km"], 0.5) if len(tracks) else None,
        "endpoint_distance_q1_km": q(tracks["endpoint_distance_km"], 0.25) if len(tracks) else None,
        "endpoint_distance_q3_km": q(tracks["endpoint_distance_km"], 0.75) if len(tracks) else None,
        "endpoint_distance_max_km": float(tracks["endpoint_distance_km"].max()) if len(tracks) else None,
        "migration_speed_median_km_day": q(tracks["migration_speed_km_day"], 0.5) if len(tracks) else None,
        "migration_speed_q1_km_day": q(tracks["migration_speed_km_day"], 0.25) if len(tracks) else None,
        "migration_speed_q3_km_day": q(tracks["migration_speed_km_day"], 0.75) if len(tracks) else None,
    }
    published = {
        "n_tracks": 35,
        "n_individuals": 31,
        "endpoint_distance_median_km": 1899.0,
        "endpoint_distance_q1_km": 1155.0,
        "endpoint_distance_q3_km": 3130.0,
        "endpoint_distance_max_km": 4184.0,
        "migration_speed_median_km_day": 48.2,
        "migration_speed_q1_km_day": 30.0,
        "migration_speed_q3_km_day": 60.9,
        "arrival_events_with_environment": 208,
    }

    # Conservative replication gate. Exact event count is not expected before
    # environmental-coverage filtering, but track/distance/speed structure should
    # be recognisable.
    gates = {
        "track_count_within_4": abs(observed["n_tracks"] - 35) <= 4,
        "individual_count_within_4": abs(observed["n_individuals"] - 31) <= 4,
        "endpoint_median_within_25pct": (
            observed["endpoint_distance_median_km"] is not None
            and abs(observed["endpoint_distance_median_km"] / 1899.0 - 1.0) <= 0.25
        ),
        "migration_speed_median_within_35pct": (
            observed["migration_speed_median_km_day"] is not None
            and abs(observed["migration_speed_median_km_day"] / 48.2 - 1.0) <= 0.35
        ),
    }
    promotion_ready = all(gates.values())

    receipt = {
        "analysis": "wigeon_published_hmm_reconstruction_v1",
        "threshold_v_ms": THRESHOLD_V_MS,
        "threshold_d_km": THRESHOLD_D_KM,
        "source_freeze": str(ORIGINAL_DATA_FREEZE),
        "hmm": "published fitted 4-state parameters from Additional file 2",
        "observed": observed,
        "published_reference": published,
        "replication_gates": gates,
        "promotion_ready_for_environmental_controller": promotion_ready,
        "filter_status_counts": audit_df["status"].value_counts().to_dict(),
        "claim_ceiling": (
            "Movement reconstruction only. No wigeon controller estimate is "
            "licensed unless the replication gate passes and TGS is recreated."
        ),
    }
    (OUT / "stage3_wigeon_hmm_reconstruction_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, default=str))


if __name__ == "__main__":
    main()
