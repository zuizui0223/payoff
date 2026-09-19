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
TARGET_TIME_SECONDS = 3600.0
SPECIAL_TARGET_TIME_SECONDS = 7200.0
REGULARISE_WIGGLE_SECONDS = 600.0
SPECIAL_TWO_HOUR_INDIVIDUAL_YEAR = "PP00456-2018"
GEOD = Geod(ellps="WGS84")


def geodesic_km(lon1, lat1, lon2, lat2):
    return GEOD.inv(float(lon1), float(lat1), float(lon2), float(lat2))[2] / 1000.0


def tpeqd_x(subset: pd.DataFrame) -> np.ndarray:
    """Match the Supplement's seasonal-subset two-point-equidistant x coordinate."""
    minlat = float(subset["lat"].min())
    maxlat = float(subset["lat"].max())
    minlon = float(subset["lon"].min())
    maxlon = float(subset["lon"].max())
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


def regularise_track_hourly(
    tmp: pd.DataFrame, individual_year: str | None = None
) -> pd.DataFrame:
    """Port the Supplement's explicit regularise.tracks calls.

    The published movement threshold is explicitly a one-hour flight distance
    (13.94 m/s * 3.6 = 50.184 km), and the fitted HMM discussion interprets
    state step lengths against 20 m/s * 3600 s. The public normalized source is
    hourly; this function still reapplies the exact nearest-target/wiggle rule
    so gaps are handled consistently.
    """
    tmp = tmp.sort_values("time").drop_duplicates("time").copy()
    if len(tmp) < 2:
        return tmp.iloc[0:0].copy()

    # The Supplement identifies PP00456-2018 as two-hourly. Public
    # harmonized releases can replace local identifiers with numeric IDs, so
    # infer the same schedule from the observed regular interval when the
    # original local ID is unavailable.
    positive_dt = (
        tmp["time"].sort_values().diff().dt.total_seconds().dropna()
    )
    schedule_dt = positive_dt[
        (positive_dt >= 1800.0) & (positive_dt <= 10800.0)
    ]
    median_schedule = (
        float(schedule_dt.median()) if len(schedule_dt) else TARGET_TIME_SECONDS
    )
    inferred_two_hour = median_schedule > 5400.0
    target_time = (
        SPECIAL_TARGET_TIME_SECONDS
        if (
            individual_year == SPECIAL_TWO_HOUR_INDIVIDUAL_YEAR
            or inferred_two_hour
        )
        else TARGET_TIME_SECONDS
    )

    # Pandas 3 can store timezone-aware datetimes at microsecond rather than
    # nanosecond resolution, so astype("int64") / 1e9 is not unit-stable.
    # Timestamp.timestamp() is explicitly seconds since the Unix epoch and
    # reproduces R difftime(..., units="secs") across pandas versions.
    observed = tmp["time"].map(
        lambda z: pd.Timestamp(z).timestamp()
    ).to_numpy(dtype=float)
    start = float(observed[0])
    end = float(observed[-1])
    targets = np.arange(start, end + 0.5 * target_time, target_time)

    chosen = []
    diffs = []
    for target in targets:
        pos = int(np.searchsorted(observed, target))
        candidates = []
        if pos < len(observed):
            candidates.append(pos)
        if pos > 0:
            candidates.append(pos - 1)
        if not candidates:
            continue
        j = min(candidates, key=lambda q: abs(observed[q] - target))
        chosen.append(j)
        diffs.append(abs(observed[j] - target))

    if not chosen:
        return tmp.iloc[0:0].copy()

    selected_times = observed[np.asarray(chosen, dtype=int)]
    t_prev = np.r_[np.nan, np.diff(selected_times)]
    diff_prev = np.abs(target_time - t_prev)
    check = (
        np.asarray(diffs) <= REGULARISE_WIGGLE_SECONDS
    ) | (
        diff_prev <= REGULARISE_WIGGLE_SECONDS
    )

    selected = np.asarray(chosen, dtype=int)[check]
    out = tmp.iloc[selected].copy()
    # R merge can repeat an observed row selected for adjacent targets. The
    # subsequent HMM requires one observation per timestamp, so keep one.
    return out.drop_duplicates("time").sort_values("time").reset_index(drop=True)


def trim_inactive_tail(x: pd.DataFrame) -> pd.DataFrame:
    """Remove only the terminal run of inactive ground-speed-zero fixes.

    van Toor et al. (2021) state that inactive locations (ground speed = 0)
    were removed from the end of each track. Interior zero-speed fixes are
    retained because they can represent real resting behavior.
    """
    x = x.sort_values("time").copy()
    speed = pd.to_numeric(x["ground_speed"], errors="coerce").to_numpy()
    active = np.where(np.isfinite(speed) & (speed != 0.0))[0]
    if len(active) == 0:
        return x.iloc[0:0].copy()
    return x.iloc[: int(active[-1]) + 1].copy()


def prepare_track(
    x: pd.DataFrame, individual_year: str | None = None
):
    x = trim_inactive_tail(x)
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
        sx = tpeqd_x(spring_start)
        ex = tpeqd_x(spring_end)
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
    x["migratory_window"] = (
        (x["time"].dt.date >= start_day)
        & (x["time"].dt.date <= end_day)
    )

    # The Supplement regularises the time series and then retains rows that
    # both pass the regularisation check and fall inside the migration window.
    reg = regularise_track_hourly(
        x, individual_year=individual_year
    )
    mig = reg[reg["migratory_window"]].copy()
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
        "n_migration_rows_before_regularise": int(x["migratory_window"].sum()),
        "n_migration_rows_after_regularise": int(len(mig)),
        "target_time_seconds": (
            SPECIAL_TARGET_TIME_SECONDS
            if (
                individual_year == SPECIAL_TWO_HOUR_INDIVIDUAL_YEAR
                or (
                    len(
                        x["time"].sort_values().diff().dt.total_seconds()
                        .dropna()
                        .loc[
                            lambda z: (z >= 1800.0) & (z <= 10800.0)
                        ]
                    )
                    and float(
                        x["time"].sort_values().diff().dt.total_seconds()
                        .dropna()
                        .loc[
                            lambda z: (z >= 1800.0) & (z <= 10800.0)
                        ]
                        .median()
                    ) > 5400.0
                )
            )
            else TARGET_TIME_SECONDS
        ),
        "regularise_wiggle_seconds": REGULARISE_WIGGLE_SECONDS,
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

    # Published arrival-event contract: no staging arrivals after June 30.
    arrival_ts = pd.to_datetime(out["arrival"], utc=True)
    out["arrival_before_july"] = arrival_ts.dt.month <= 6
    out = out[out["arrival_before_july"]].copy()

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
        individual_year = f"{ind}-{year}"
        prepared, status = prepare_track(
            x, individual_year=individual_year
        )
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

        # The published Supplement computes summary.speed *after* removing
        # HMM state 4 (migratory flight) from wigeon.df. The remaining sequence
        # connects successive staging/non-flight positions and divides their
        # cumulative geodesic distance by the full elapsed migration time.
        # Our earlier all-state path-length metric over-counted high-frequency
        # flight tortuosity and is retained only as a sensitivity diagnostic.
        total_path_dist = cumulative_track_distance_km(classified)
        duration_days = (
            classified.time.max() - classified.time.min()
        ).total_seconds() / 86400.0

        non_migratory = classified[classified["state"] != 4].copy()
        published_summary_dist = cumulative_track_distance_km(non_migratory)
        published_summary_duration = (
            (non_migratory.time.max() - non_migratory.time.min()).total_seconds()
            / 86400.0
            if len(non_migratory) >= 2
            else np.nan
        )
        published_summary_speed = (
            published_summary_dist / published_summary_duration
            if (
                np.isfinite(published_summary_dist)
                and np.isfinite(published_summary_duration)
                and published_summary_duration > 0
            )
            else np.nan
        )

        track_rows.append(
            {
                "individual_id": str(ind),
                "year": int(year),
                "endpoint_distance_km": meta["endpoint_distance_km"],
                "cumulative_migration_distance_km": total_path_dist,
                "migration_duration_days": duration_days,
                "all_state_path_speed_km_day": (
                    total_path_dist / duration_days
                    if duration_days > 0
                    else np.nan
                ),
                "published_summary_distance_km": published_summary_dist,
                "published_summary_duration_days": published_summary_duration,
                "migration_speed_km_day": published_summary_speed,
                "n_migration_fixes": int(len(classified)),
                "n_non_migratory_state_fixes": int(len(non_migratory)),
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
        "migration_speed_definition": (
            "Supplement summary.speed analogue: cumulative geodesic distance "
            "after excluding HMM state 4, divided by elapsed time of that "
            "non-state4 sequence; all-state path speed retained separately"
        ),
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
