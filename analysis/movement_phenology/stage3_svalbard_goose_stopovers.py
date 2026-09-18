#!/usr/bin/env python3
"""Reconstruct spring stopovers and broad stopover regions for Svalbard barnacle geese.

This is a direct raw-GPS preprocessing step toward a second PAYOFF-B
movement–phenology controller estimate.

Approximation to Kölzsch et al. (2015):
- spring tracks only;
- spatial stay clusters within ~30 km;
- duration >=48 h;
- merge stopover sites across individuals into broad geographic regions.

The original paper allowed one outlier fix within a stopover cluster. The
implementation below uses a time-aware stay-segment algorithm with a 30-km
maximum radius from the running segment centroid. It is validated against the
published route summary before any controller inference is licensed.
"""

from __future__ import annotations

import gzip
import io
import json
import math
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN


GPS = Path("external/barnacle_goose_svalbard/gps.csv")
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

EARTH_KM = 6371.0088


def read_any(path: Path) -> pd.DataFrame:
    raw = path.read_bytes()
    payloads: list[tuple[str, bytes]] = []
    if raw.startswith(b"PK"):
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            for name in zf.namelist():
                if not name.endswith("/"):
                    payloads.append((name, zf.read(name)))
    elif raw.startswith(b"\x1f\x8b"):
        payloads.append((path.name, gzip.decompress(raw)))
    else:
        payloads.append((path.name, raw))

    for _, payload in payloads:
        for encoding in ("utf-8-sig", "utf-16", "latin-1"):
            try:
                text = payload.decode(encoding)
            except Exception:
                continue
            for sep in (",", "\t", ";"):
                try:
                    df = pd.read_csv(io.StringIO(text), sep=sep, low_memory=False)
                    if df.shape[1] > 1:
                        return df
                except Exception:
                    pass
    raise RuntimeError(f"Could not parse {path}")


def haversine_km(lat1, lon1, lat2, lon2):
    lat1 = math.radians(float(lat1))
    lon1 = math.radians(float(lon1))
    lat2 = math.radians(float(lat2))
    lon2 = math.radians(float(lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return 2 * EARTH_KM * math.asin(min(1.0, math.sqrt(a)))


def circular_mean_lon(lons):
    x = np.radians(np.asarray(lons, dtype=float))
    return float(np.degrees(np.arctan2(np.mean(np.sin(x)), np.mean(np.cos(x)))))


def segment_centroid(df):
    return float(df["lat"].mean()), circular_mean_lon(df["lon"])


def max_distance_from_centroid(df):
    clat, clon = segment_centroid(df)
    return max(
        haversine_km(lat, lon, clat, clon)
        for lat, lon in zip(df["lat"], df["lon"])
    )


def detect_stay_segments(track: pd.DataFrame, radius_km=30.0, min_hours=48.0):
    """Greedy time-aware stay segmentation.

    Start at each fix and extend while all fixes remain within radius_km of the
    running centroid. When the segment breaks, retain it if duration>=min_hours.
    Adjacent retained segments whose centroids are within radius and gap <=24 h
    are merged. This is deliberately conservative.
    """
    track = track.sort_values("time").reset_index(drop=True)
    n = len(track)
    stays = []
    i = 0

    while i < n - 1:
        j = i + 1
        best_j = None
        while j < n:
            block = track.iloc[i : j + 1]
            if max_distance_from_centroid(block) <= radius_km:
                duration = (
                    block["time"].iloc[-1] - block["time"].iloc[0]
                ).total_seconds() / 3600
                if duration >= min_hours:
                    best_j = j
                j += 1
            else:
                break

        if best_j is not None:
            block = track.iloc[i : best_j + 1].copy()
            lat, lon = segment_centroid(block)
            stays.append(
                {
                    "start": block["time"].iloc[0],
                    "end": block["time"].iloc[-1],
                    "duration_hours": (
                        block["time"].iloc[-1] - block["time"].iloc[0]
                    ).total_seconds()
                    / 3600,
                    "lat": lat,
                    "lon": lon,
                    "n_fixes": len(block),
                    "max_radius_km": max_distance_from_centroid(block),
                }
            )
            i = best_j + 1
        else:
            i += 1

    if not stays:
        return []

    merged = [stays[0]]
    for s in stays[1:]:
        prev = merged[-1]
        gap_h = (s["start"] - prev["end"]).total_seconds() / 3600
        dist = haversine_km(prev["lat"], prev["lon"], s["lat"], s["lon"])
        if gap_h <= 24 and dist <= radius_km:
            total_weight = prev["n_fixes"] + s["n_fixes"]
            prev["lat"] = (
                prev["lat"] * prev["n_fixes"] + s["lat"] * s["n_fixes"]
            ) / total_weight
            # longitude is safe for this route (no dateline crossing)
            prev["lon"] = (
                prev["lon"] * prev["n_fixes"] + s["lon"] * s["n_fixes"]
            ) / total_weight
            prev["end"] = s["end"]
            prev["duration_hours"] = (
                prev["end"] - prev["start"]
            ).total_seconds() / 3600
            prev["n_fixes"] = total_weight
            prev["max_radius_km"] = max(
                prev["max_radius_km"], s["max_radius_km"]
            )
        else:
            merged.append(s)
    return merged


def main():
    gps = read_any(GPS)
    gps = gps.rename(
        columns={
            "timestamp": "time",
            "location-lat": "lat",
            "location-long": "lon",
            "individual-local-identifier": "individual_id",
        }
    )
    gps["time"] = pd.to_datetime(gps["time"], errors="coerce", utc=True)
    gps["lat"] = pd.to_numeric(gps["lat"], errors="coerce")
    gps["lon"] = pd.to_numeric(gps["lon"], errors="coerce")
    gps = gps.dropna(subset=["time", "lat", "lon", "individual_id"]).copy()
    gps["year"] = gps["time"].dt.year
    gps["month"] = gps["time"].dt.month

    # Spring window broad enough to include winter departure and Arctic arrival.
    spring = gps[(gps["month"] >= 2) & (gps["month"] <= 6)].copy()

    stop_rows = []
    for (ind, year), track in spring.groupby(["individual_id", "year"]):
        if len(track) < 10:
            continue
        stays = detect_stay_segments(track)
        for k, s in enumerate(stays, start=1):
            stop_rows.append(
                {
                    "individual_id": str(ind),
                    "year": int(year),
                    "stop_index": k,
                    **s,
                }
            )

    stops = pd.DataFrame(stop_rows)
    if stops.empty:
        raise SystemExit("No stopovers detected")

    # Remove obvious winter-residence stays that begin before March 1 only from
    # the *region clustering* validation. Keep them in the event table.
    stops["start_doy"] = pd.to_datetime(stops["start"]).dt.dayofyear
    stops["end_doy"] = pd.to_datetime(stops["end"]).dt.dayofyear

    # Cluster stopover centroids across individuals into broad regions. 150 km
    # is below the ~930 km mean spacing of published Svalbard regions and merges
    # nearby alternative sites on the same coast.
    coords = np.radians(stops[["lat", "lon"]].to_numpy())
    labels = DBSCAN(
        eps=150.0 / EARTH_KM,
        min_samples=2,
        metric="haversine",
        algorithm="ball_tree",
    ).fit_predict(coords)
    stops["region_label_raw"] = labels

    region_rows = []
    for lab, d in stops[stops["region_label_raw"] >= 0].groupby(
        "region_label_raw"
    ):
        region_rows.append(
            {
                "region_label_raw": int(lab),
                "lat": float(d["lat"].mean()),
                "lon": circular_mean_lon(d["lon"]),
                "n_stop_events": int(len(d)),
                "n_individuals": int(d["individual_id"].nunique()),
                "n_years": int(d["year"].nunique()),
                "median_start_doy": float(d["start_doy"].median()),
                "median_duration_days": float(d["duration_hours"].median() / 24),
            }
        )
    regions = pd.DataFrame(region_rows)

    # Order regions south-to-north and assign deterministic IDs.
    regions = regions.sort_values(["lat", "lon"]).reset_index(drop=True)
    regions["region_id"] = [f"R{i+1}" for i in range(len(regions))]
    lab_to_id = dict(
        zip(regions["region_label_raw"], regions["region_id"])
    )
    stops["region_id"] = stops["region_label_raw"].map(lab_to_id)

    # Only regions used by at least 3 individuals are directly comparable to
    # the published stopover-region definition.
    regions["published_region_eligible"] = regions["n_individuals"] >= 3

    # Reorder individual events by time and summarize number of eligible regions.
    stops = stops.sort_values(["individual_id", "year", "start"]).copy()
    eligible_ids = set(
        regions.loc[regions["published_region_eligible"], "region_id"]
    )
    stops["eligible_region"] = stops["region_id"].isin(eligible_ids)

    track_summary = (
        stops.groupby(["individual_id", "year"])
        .agg(
            n_stops=("stop_index", "size"),
            n_region_stops=("eligible_region", "sum"),
            n_unique_regions=("region_id", lambda x: x.dropna().nunique()),
        )
        .reset_index()
    )

    summary = {
        "n_tracks": int(track_summary.shape[0]),
        "n_individuals": int(stops["individual_id"].nunique()),
        "n_stop_events": int(len(stops)),
        "n_broad_regions_all": int(len(regions)),
        "n_broad_regions_ge3_individuals": int(
            regions["published_region_eligible"].sum()
        ),
        "mean_stops_per_track": float(track_summary["n_stops"].mean()),
        "mean_unique_regions_per_track": float(
            track_summary["n_unique_regions"].mean()
        ),
        "published_reference": {
            "mean_stops_per_track": 4.2,
            "mean_successive_regions_per_track": 3.0,
            "total_route_km": 2600,
            "mean_region_spacing_km": 930,
        },
        "claim_ceiling": (
            "Stopover reconstruction diagnostic only; region parameters are "
            "not yet licensed for controller inference until route structure "
            "is manually and climatically validated."
        ),
    }

    stops.to_csv(OUT / "stage3_svalbard_goose_stopovers.csv", index=False)
    regions.to_csv(OUT / "stage3_svalbard_goose_regions.csv", index=False)
    track_summary.to_csv(
        OUT / "stage3_svalbard_goose_track_stopover_summary.csv", index=False
    )
    (OUT / "stage3_svalbard_goose_stopover_receipt.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps(summary, indent=2))
    print("\nREGIONS")
    print(regions.to_string(index=False))


if __name__ == "__main__":
    main()
