#!/usr/bin/env python3
"""Reconstruct spring stopovers for Greenland and Barents barnacle-goose flyways.

Uses the same conservative >=48 h / ~30 km stay logic already validated on the
Svalbard raw GPS. Broad regions are derived across individual stopovers with
haversine DBSCAN and are treated as reconstruction diagnostics until compared
with the published route descriptions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

from analysis.movement_phenology.stage3_svalbard_goose_stopovers import (
    EARTH_KM,
    circular_mean_lon,
    detect_stay_segments,
    read_any,
)


OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

PUBLISHED = {
    "greenland": {
        "paper_individuals": 7,
        "paper_full_tracks": 7,
        "route_note": "Ireland -> Iceland -> Greenland",
    },
    "barents": {
        "paper_individuals": 12,
        "paper_full_tracks": 26,
        "route_note": "Wadden/Central Europe -> Baltic -> White Sea/Kanin -> Barents breeding region",
    },
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--flyway", required=True, choices=sorted(PUBLISHED))
    p.add_argument("--gps", required=True)
    p.add_argument("--cluster-km", type=float, default=150.0)
    p.add_argument("--min-region-individuals", type=int, default=3)
    return p.parse_args()


def main():
    args = parse_args()
    gps = read_any(Path(args.gps))
    candidates = {
        "time": ["timestamp", "eventDate", "eventdate"],
        "lat": ["location-lat", "decimalLatitude", "latitude"],
        "lon": ["location-long", "decimalLongitude", "longitude"],
        "individual_id": [
            "individual-local-identifier",
            "organismID",
            "individual",
            "individual_id",
        ],
    }

    rename = {}
    for target, choices in candidates.items():
        hit = None
        lowered = {str(c).lower(): c for c in gps.columns}
        for choice in choices:
            if choice.lower() in lowered:
                hit = lowered[choice.lower()]
                break
        if hit is None:
            for c in gps.columns:
                lc = str(c).lower()
                if any(choice.lower() in lc for choice in choices):
                    hit = c
                    break
        if hit is None:
            raise SystemExit(
                f"Missing {target} column; candidates={choices}; "
                f"columns={list(gps.columns)}"
            )
        rename[hit] = target

    gps = gps.rename(columns=rename)
    gps["time"] = pd.to_datetime(gps["time"], errors="coerce", utc=True)
    gps["lat"] = pd.to_numeric(gps["lat"], errors="coerce")
    gps["lon"] = pd.to_numeric(gps["lon"], errors="coerce")
    gps = gps.dropna(subset=["time", "lat", "lon", "individual_id"]).copy()
    gps["year"] = gps["time"].dt.year
    gps["month"] = gps["time"].dt.month

    spring = gps[(gps["month"] >= 2) & (gps["month"] <= 6)].copy()

    rows = []
    for (ind, year), track in spring.groupby(["individual_id", "year"]):
        if len(track) < 10:
            continue
        stays = detect_stay_segments(track, radius_km=30.0, min_hours=48.0)
        for i, s in enumerate(stays, start=1):
            rows.append(
                {
                    "flyway": args.flyway,
                    "individual_id": str(ind),
                    "year": int(year),
                    "stop_index": i,
                    **s,
                }
            )
    stops = pd.DataFrame(rows)
    if stops.empty:
        raise SystemExit("No >=48 h stopovers reconstructed")

    stops["start_doy"] = pd.to_datetime(stops["start"]).dt.dayofyear
    stops["end_doy"] = pd.to_datetime(stops["end"]).dt.dayofyear

    coords = np.radians(stops[["lat", "lon"]].to_numpy())
    labels = DBSCAN(
        eps=args.cluster_km / EARTH_KM,
        min_samples=2,
        metric="haversine",
        algorithm="ball_tree",
    ).fit_predict(coords)
    stops["region_label_raw"] = labels

    rr = []
    for lab, d in stops[stops["region_label_raw"] >= 0].groupby("region_label_raw"):
        rr.append(
            {
                "region_label_raw": int(lab),
                "lat": float(d["lat"].mean()),
                "lon": circular_mean_lon(d["lon"]),
                "n_stop_events": int(len(d)),
                "n_individuals": int(d["individual_id"].nunique()),
                "n_years": int(d["year"].nunique()),
                "median_start_doy": float(d["start_doy"].median()),
                "median_duration_days": float(d["duration_hours"].median() / 24.0),
            }
        )
    regions = pd.DataFrame(rr)
    if regions.empty:
        raise SystemExit("No broad stopover regions reconstructed")
    regions = regions.sort_values(["lat", "lon"]).reset_index(drop=True)
    regions["region_id"] = [f"R{i+1}" for i in range(len(regions))]
    mapping = dict(zip(regions["region_label_raw"], regions["region_id"]))
    stops["region_id"] = stops["region_label_raw"].map(mapping)
    regions["published_region_eligible"] = (
        regions["n_individuals"] >= args.min_region_individuals
    )

    stops = stops.sort_values(["individual_id", "year", "start"]).copy()
    eligible = set(
        regions.loc[regions["published_region_eligible"], "region_id"].astype(str)
    )
    stops["eligible_region"] = stops["region_id"].isin(eligible)

    tracks = (
        stops.groupby(["individual_id", "year"])
        .agg(
            n_stops=("stop_index", "size"),
            n_region_stops=("eligible_region", "sum"),
            n_unique_regions=("region_id", lambda x: x.dropna().nunique()),
            first_stop_start=("start", "min"),
            last_stop_end=("end", "max"),
        )
        .reset_index()
    )

    transition_rows = []
    eligible_stops = stops[stops["eligible_region"]].copy()
    for (ind, year), d in eligible_stops.groupby(["individual_id", "year"]):
        d = d.sort_values("start").reset_index(drop=True)
        for i in range(len(d) - 1):
            a = d.iloc[i]
            b = d.iloc[i + 1]
            if a["region_id"] == b["region_id"]:
                continue
            transition_rows.append(
                {
                    "individual_id": str(ind),
                    "year": int(year),
                    "origin_region": str(a["region_id"]),
                    "destination_region": str(b["region_id"]),
                    "origin_arrival": a["start"],
                    "origin_departure": a["end"],
                    "origin_stopover_days": float(a["duration_hours"] / 24.0),
                    "destination_arrival": b["start"],
                }
            )
    transitions = pd.DataFrame(transition_rows)

    prefix = f"stage3_{args.flyway}_goose"
    stops.to_csv(OUT / f"{prefix}_stopovers.csv", index=False)
    regions.to_csv(OUT / f"{prefix}_regions.csv", index=False)
    tracks.to_csv(OUT / f"{prefix}_track_stopover_summary.csv", index=False)
    transitions.to_csv(OUT / f"{prefix}_transitions_raw.csv", index=False)

    pair_counts = []
    if not transitions.empty:
        for (a, b), d in transitions.groupby(["origin_region", "destination_region"]):
            pair_counts.append(
                {
                    "origin_region": str(a),
                    "destination_region": str(b),
                    "n": int(len(d)),
                    "n_individuals": int(d["individual_id"].nunique()),
                    "n_years": int(d["year"].nunique()),
                }
            )

    receipt = {
        "flyway": args.flyway,
        "gps_rows": int(len(gps)),
        "gps_individuals": int(gps["individual_id"].nunique()),
        "gps_years": sorted(int(x) for x in gps["year"].unique()),
        "n_track_years_with_stops": int(len(tracks)),
        "n_individuals_with_stops": int(stops["individual_id"].nunique()),
        "n_stop_events": int(len(stops)),
        "n_broad_regions_all": int(len(regions)),
        "n_broad_regions_ge_min_individuals": int(
            regions["published_region_eligible"].sum()
        ),
        "mean_stops_per_track": float(tracks["n_stops"].mean()),
        "mean_unique_regions_per_track": float(tracks["n_unique_regions"].mean()),
        "transition_counts": pair_counts,
        "published_reference": PUBLISHED[args.flyway],
        "claim_ceiling": (
            "Raw-GPS stopover reconstruction diagnostic. Controller inference "
            "requires year-specific environmental onset anomalies and fixed-transition "
            "support checks."
        ),
    }
    (OUT / f"{prefix}_stopover_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, default=str))
    print("\nREGIONS")
    print(regions.to_string(index=False))


if __name__ == "__main__":
    main()
