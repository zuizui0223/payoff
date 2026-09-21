#!/usr/bin/env python3
"""Quantify migration control permeability around industrial development.

Aikens et al. (2022) archived spring-migration GPS points plus small/large
development footprints. This analysis uses only those public source objects.

Primary descriptive quantity at individual-year grain:

    G = median migration step speed near the development boundary
        / median step speed far from the development boundary.

G < 1 indicates attenuation of realized movement near the development footprint.

A longitudinal contrast asks whether G declines more strongly through time in
the DCC population (large development footprint) than in WHB (small footprint).

This is an observational perturbation analysis, not a causal estimate of
development itself and not a direct phenological phase-retention lambda.
"""

from __future__ import annotations

import io
import json
import math
from pathlib import Path
import tempfile
import zipfile

import numpy as np
import pandas as pd
import shapefile
from shapely.geometry import Point, shape as shapely_shape
from shapely.ops import transform as shapely_transform
from pyproj import CRS, Transformer
import statsmodels.formula.api as smf


ARCHIVE = Path(
    "external/industrial_mule_deer/dryad_bulk_version_198581.zip"
)
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

INNER_NAME = "DryadDataFor_Aikens_etal_NatEcoEvo.zip"
ROOT = "DryadDataFor_Aikens_etal_NatEcoEvo"
GPS_BASE = f"{ROOT}/GPSdata/GPS_spring_migration"
SMALL_BASE = f"{ROOT}/DevelopmentFootprints/smallFootprint"
LARGE_BASE = f"{ROOT}/DevelopmentFootprints/largeFootprint"

PRIMARY_EDGE_KM = 2.0
PRIMARY_FAR_KM = 10.0
MAX_STEP_INTERVAL_H = 24.0
MIN_ZONE_STEPS = 3


def extract_nested_shapefiles(tmp: Path):
    if not ARCHIVE.exists():
        raise SystemExit(f"Missing downloaded Dryad version archive: {ARCHIVE}")

    with zipfile.ZipFile(ARCHIVE) as outer:
        names = outer.namelist()
        inner_candidates = [
            n for n in names
            if Path(n).name == INNER_NAME
        ]
        if not inner_candidates:
            raise SystemExit(
                f"Nested data zip {INNER_NAME} not found; members={names}"
            )
        inner_raw = outer.read(inner_candidates[0])

    with zipfile.ZipFile(io.BytesIO(inner_raw)) as inner:
        wanted_bases = (GPS_BASE, SMALL_BASE, LARGE_BASE)
        for name in inner.namelist():
            if any(name.startswith(base + ".") for base in wanted_bases):
                target = tmp / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(inner.read(name))

    paths = {
        "gps": tmp / f"{GPS_BASE}.shp",
        "small": tmp / f"{SMALL_BASE}.shp",
        "large": tmp / f"{LARGE_BASE}.shp",
    }
    for key, p in paths.items():
        if not p.exists():
            raise SystemExit(f"Missing extracted {key} shapefile: {p}")
    return paths


def read_crs(shp_path: Path) -> CRS:
    prj_path = shp_path.with_suffix(".prj")
    if not prj_path.exists():
        raise ValueError(f"Missing PRJ for {shp_path}")
    wkt = prj_path.read_text(encoding="utf-8", errors="ignore").strip()
    if not wkt:
        raise ValueError(f"Empty PRJ for {shp_path}")
    return CRS.from_wkt(wkt)


def read_polygon(shp_path: Path, target_crs: CRS):
    r = shapefile.Reader(str(shp_path))
    geoms = [shapely_shape(s.__geo_interface__) for s in r.shapes()]
    if not geoms:
        raise ValueError(f"No polygon geometry in {shp_path}")
    geom = geoms[0]
    for g in geoms[1:]:
        geom = geom.union(g)

    source_crs = read_crs(shp_path)
    if source_crs != target_crs:
        transformer = Transformer.from_crs(
            source_crs, target_crs, always_xy=True
        )
        geom = shapely_transform(transformer.transform, geom)
    return geom


def read_gps(shp_path: Path) -> pd.DataFrame:
    r = shapefile.Reader(str(shp_path))
    fields = [f[0] for f in r.fields[1:]]
    required = {"AID_Year", "Timestamp", "pop"}
    missing = required.difference(fields)
    if missing:
        raise ValueError(f"Missing GPS fields {sorted(missing)}; fields={fields}")

    rows = []
    for source_record_index, sr in enumerate(r.iterShapeRecords()):
        rec = dict(zip(fields, list(sr.record)))
        pts = sr.shape.points
        if not pts:
            continue
        x, y = pts[0]
        rows.append(
            {
                "source_record_index": int(source_record_index),
                "AID_Year": str(rec["AID_Year"]),
                "Timestamp": rec["Timestamp"],
                "pop": str(rec["pop"]).lower(),
                "x": float(x),
                "y": float(y),
            }
        )
    d = pd.DataFrame(rows)
    d["time"] = pd.to_datetime(d["Timestamp"], errors="coerce")
    d = d.dropna(subset=["time", "x", "y", "AID_Year", "pop"]).copy()

    # The README defines AID_Year as animal ID and year separated by underscore.
    parts = d["AID_Year"].str.rsplit("_", n=1, expand=True)
    if parts.shape[1] == 2:
        d["animal_id"] = parts[0].astype(str)
        d["year_from_id"] = pd.to_numeric(parts[1], errors="coerce")
    else:
        d["animal_id"] = d["AID_Year"].astype(str)
        d["year_from_id"] = np.nan
    d["year"] = d["time"].dt.year
    return d


def add_steps(d: pd.DataFrame, footprints: dict[str, object]) -> pd.DataFrame:
    rows = []
    for aid, x in d.groupby("AID_Year"):
        x = x.sort_values("time").reset_index(drop=True)
        if len(x) < 2:
            continue
        pop = str(x["pop"].mode().iloc[0]).lower()
        if pop == "whb":
            footprint = footprints["small"]
            dev_class = "small"
        elif pop == "dcc":
            footprint = footprints["large"]
            dev_class = "large"
        else:
            continue

        boundary = footprint.boundary
        for i in range(len(x) - 1):
            a = x.iloc[i]
            b = x.iloc[i + 1]
            dt_h = (b["time"] - a["time"]).total_seconds() / 3600.0
            if not np.isfinite(dt_h) or dt_h <= 0 or dt_h > MAX_STEP_INTERVAL_H:
                continue
            dx = float(b["x"] - a["x"])
            dy = float(b["y"] - a["y"])
            dist_km = math.hypot(dx, dy) / 1000.0
            speed_km_day = dist_km / (dt_h / 24.0)
            mx = (float(a["x"]) + float(b["x"])) / 2.0
            my = (float(a["y"]) + float(b["y"])) / 2.0
            mid = Point(mx, my)
            boundary_km = float(mid.distance(boundary)) / 1000.0
            inside = bool(footprint.contains(mid) or footprint.touches(mid))

            rows.append(
                {
                    "AID_Year": aid,
                    "animal_id": str(a["animal_id"]),
                    "year": int(a["year"]),
                    "pop": pop,
                    "development_class": dev_class,
                    "time_start": a["time"],
                    "time_end": b["time"],
                    "dt_hours": dt_h,
                    "step_distance_km": dist_km,
                    "speed_km_day": speed_km_day,
                    "log1p_speed": math.log1p(speed_km_day),
                    "boundary_distance_km": boundary_km,
                    "inside_footprint": inside,
                    "mid_x": mx,
                    "mid_y": my,
                }
            )
    return pd.DataFrame(rows)


def individual_year_permeability(
    steps: pd.DataFrame,
    edge_km: float,
    far_km: float,
):
    rows = []
    for aid, x in steps.groupby("AID_Year"):
        edge = x[x["boundary_distance_km"] <= edge_km]
        far = x[x["boundary_distance_km"] >= far_km]
        if len(edge) < MIN_ZONE_STEPS or len(far) < MIN_ZONE_STEPS:
            continue
        edge_speed = float(edge["speed_km_day"].median())
        far_speed = float(far["speed_km_day"].median())
        if not np.isfinite(edge_speed) or not np.isfinite(far_speed) or far_speed <= 0:
            continue
        g = edge_speed / far_speed
        first = x.iloc[0]
        rows.append(
            {
                "AID_Year": aid,
                "animal_id": first["animal_id"],
                "year": int(first["year"]),
                "pop": first["pop"],
                "development_class": first["development_class"],
                "edge_km": float(edge_km),
                "far_km": float(far_km),
                "n_edge_steps": int(len(edge)),
                "n_far_steps": int(len(far)),
                "median_edge_speed_km_day": edge_speed,
                "median_far_speed_km_day": far_speed,
                "control_permeability_G": g,
                "log_G": math.log(g) if g > 0 else np.nan,
            }
        )
    columns = [
        "AID_Year",
        "animal_id",
        "year",
        "pop",
        "development_class",
        "edge_km",
        "far_km",
        "n_edge_steps",
        "n_far_steps",
        "median_edge_speed_km_day",
        "median_far_speed_km_day",
        "control_permeability_G",
        "log_G",
    ]
    return pd.DataFrame(rows, columns=columns)


def cluster_fit(formula: str, data: pd.DataFrame):
    m = smf.ols(formula, data=data).fit()
    if data["animal_id"].nunique() >= 4:
        return m.get_robustcov_results(
            cov_type="cluster",
            groups=data["animal_id"],
        )
    return m


def named_term(model, name):
    names = list(model.model.exog_names)
    i = names.index(name)
    params = np.asarray(model.params)
    bse = np.asarray(model.bse)
    pvalues = np.asarray(model.pvalues)
    return (
        float(params[i]),
        float(bse[i]),
        float(pvalues[i]),
    )


def fit_longitudinal_g(d: pd.DataFrame):
    if d.empty or "log_G" not in d.columns:
        return None
    x = d[np.isfinite(pd.to_numeric(d["log_G"], errors="coerce"))].copy()
    if len(x) < 12 or x["animal_id"].nunique() < 6 or x["year"].nunique() < 4:
        return None
    x["year_centered"] = x["year"] - x["year"].mean()
    x["large_dev"] = (x["development_class"] == "large").astype(int)
    model = cluster_fit(
        "log_G ~ year_centered * large_dev",
        x,
    )
    interaction = named_term(model, "year_centered:large_dev")
    year_main = named_term(model, "year_centered")
    large_main = named_term(model, "large_dev")
    return {
        "n": int(len(x)),
        "n_animals": int(x["animal_id"].nunique()),
        "n_years": int(x["year"].nunique()),
        "interaction_year_x_large_beta": interaction[0],
        "interaction_year_x_large_se": interaction[1],
        "interaction_year_x_large_p": interaction[2],
        "small_population_year_slope": year_main[0],
        "small_population_year_slope_se": year_main[1],
        "small_population_year_slope_p": year_main[2],
        "large_population_intercept_shift": large_main[0],
        "large_population_intercept_shift_se": large_main[1],
        "large_population_intercept_shift_p": large_main[2],
    }


def fit_step_edge_interaction(steps: pd.DataFrame, edge_km: float):
    x = steps[np.isfinite(steps["log1p_speed"])].copy()
    x["edge"] = (x["boundary_distance_km"] <= edge_km).astype(int)
    x["large_dev"] = (x["development_class"] == "large").astype(int)
    x["year_centered"] = x["year"] - x["year"].mean()
    if x["edge"].sum() < 20 or x["animal_id"].nunique() < 6:
        return None

    # Individual-year FE absorbs each migration's general pace; interactions
    # estimate whether edge-local attenuation differs by development class/time.
    model = smf.ols(
        "log1p_speed ~ edge + edge:large_dev + edge:year_centered "
        "+ edge:large_dev:year_centered + C(AID_Year)",
        data=x,
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": x["animal_id"]},
    )
    out = {}
    for term in (
        "edge",
        "edge:large_dev",
        "edge:year_centered",
        "edge:large_dev:year_centered",
    ):
        b, se, p = named_term(model, term)
        out[term + "_beta"] = b
        out[term + "_se"] = se
        out[term + "_p"] = p
    out["n_steps"] = int(len(x))
    out["n_edge_steps"] = int(x["edge"].sum())
    out["n_individual_years"] = int(x["AID_Year"].nunique())
    out["n_animals"] = int(x["animal_id"].nunique())
    return out


def main():
    with tempfile.TemporaryDirectory() as td:
        paths = extract_nested_shapefiles(Path(td))
        gps = read_gps(paths["gps"])
        gps_crs = read_crs(paths["gps"])

        gps_export = gps.copy()
        gps_export["group"] = gps_export["pop"].map(
            {"whb": "small", "dcc": "large"}
        )
        gps_export["observation_id"] = gps_export[
            "source_record_index"
        ].map(lambda value: f"aikens_gps_{int(value):06d}")
        gps_export["animal_year"] = gps_export["AID_Year"].astype(str)
        gps_export["timestamp"] = gps_export["time"].dt.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        gps_export[
            [
                "observation_id",
                "source_record_index",
                "animal_id",
                "animal_year",
                "group",
                "pop",
                "year",
                "timestamp",
                "x",
                "y",
            ]
        ].to_csv(
            OUT / "stage3_industrial_mule_deer_gps.csv",
            index=False,
        )

        footprints = {
            "small": read_polygon(paths["small"], gps_crs),
            "large": read_polygon(paths["large"], gps_crs),
        }
        steps = add_steps(gps, footprints)

    if steps.empty:
        raise SystemExit("No valid migration steps reconstructed")

    steps.to_csv(
        OUT / "stage3_industrial_mule_deer_steps.csv",
        index=False,
    )

    sensitivity_rows = []
    primary_g = None
    primary_model = None
    primary_step = None

    for edge in (1.0, 2.0, 5.0):
        for far in (5.0, 10.0, 20.0):
            if far <= edge:
                continue
            g = individual_year_permeability(steps, edge, far)
            model = fit_longitudinal_g(g)
            row = {
                "edge_km": edge,
                "far_km": far,
                "n_individual_years": int(len(g)),
                "n_animals": int(g["animal_id"].nunique()) if len(g) else 0,
                "median_G": float(g["control_permeability_G"].median())
                if len(g)
                else np.nan,
                "median_G_small": float(
                    g.loc[
                        g["development_class"] == "small",
                        "control_permeability_G",
                    ].median()
                )
                if len(g)
                else np.nan,
                "median_G_large": float(
                    g.loc[
                        g["development_class"] == "large",
                        "control_permeability_G",
                    ].median()
                )
                if len(g)
                else np.nan,
            }
            if model:
                row.update(model)
            sensitivity_rows.append(row)

            if edge == PRIMARY_EDGE_KM and far == PRIMARY_FAR_KM:
                primary_g = g.copy()
                primary_model = model

    sens = pd.DataFrame(sensitivity_rows)
    sens.to_csv(
        OUT / "stage3_industrial_mule_deer_permeability_sensitivity.csv",
        index=False,
    )

    if primary_g is None:
        primary_g = pd.DataFrame()
    primary_g.to_csv(
        OUT / "stage3_industrial_mule_deer_individual_year_G.csv",
        index=False,
    )

    primary_step = fit_step_edge_interaction(steps, PRIMARY_EDGE_KM)

    years = (
        primary_g.groupby(["year", "development_class"])
        .agg(
            n=("AID_Year", "size"),
            median_G=("control_permeability_G", "median"),
            q25_G=("control_permeability_G", lambda z: z.quantile(0.25)),
            q75_G=("control_permeability_G", lambda z: z.quantile(0.75)),
        )
        .reset_index()
        if len(primary_g)
        else pd.DataFrame()
    )
    years.to_csv(
        OUT / "stage3_industrial_mule_deer_G_by_year_population.csv",
        index=False,
    )

    receipt = {
        "analysis": "industrial_mule_deer_control_permeability_v1",
        "source": "Aikens et al. 2022 Dryad version 198581",
        "gps_crs": gps_crs.to_string(),
        "gps_crs_wkt_name": gps_crs.name,
        "gps_points": int(len(gps)),
        "raw_gps_export": "stage3_industrial_mule_deer_gps.csv",
        "raw_gps_export_columns": [
            "observation_id",
            "source_record_index",
            "animal_id",
            "animal_year",
            "group",
            "pop",
            "year",
            "timestamp",
            "x",
            "y"
        ],
        "gps_individual_years": int(gps["AID_Year"].nunique()),
        "gps_animals": int(gps["animal_id"].nunique()),
        "gps_years": sorted(int(x) for x in gps["year"].unique()),
        "pop_counts_points": gps["pop"].value_counts().to_dict(),
        "valid_steps": int(len(steps)),
        "primary_edge_km": PRIMARY_EDGE_KM,
        "primary_far_km": PRIMARY_FAR_KM,
        "primary_individual_years": int(len(primary_g)),
        "primary_animals": int(primary_g["animal_id"].nunique())
        if len(primary_g)
        else 0,
        "primary_G_estimable": bool(len(primary_g) > 0),
        "median_G_overall": float(
            primary_g["control_permeability_G"].median()
        )
        if len(primary_g)
        else None,
        "median_G_small": float(
            primary_g.loc[
                primary_g["development_class"] == "small",
                "control_permeability_G",
            ].median()
        )
        if len(primary_g)
        else None,
        "median_G_large": float(
            primary_g.loc[
                primary_g["development_class"] == "large",
                "control_permeability_G",
            ].median()
        )
        if len(primary_g)
        else None,
        "longitudinal_G_model": primary_model,
        "step_edge_model": primary_step,
        "sensitivity_signs": (
            sens[
                [
                    "edge_km",
                    "far_km",
                    "interaction_year_x_large_beta",
                    "interaction_year_x_large_p",
                ]
            ]
            .replace({np.nan: None})
            .to_dict(orient="records")
            if "interaction_year_x_large_beta" in sens.columns
            else []
        ),
        "claim_ceiling": (
            "Observational GPS-based actuation/permeability test. G compares "
            "near-boundary versus far-route movement within individual-years. "
            "Population and time contrasts can be confounded by landscape and "
            "sampling differences; this is not a causal development effect and "
            "does not estimate phenological lambda directly. If the registered "
            "individual-year G contrast has insufficient support, it remains "
            "explicitly NOT_ESTIMABLE rather than triggering threshold changes."
        ),
    }
    (OUT / "stage3_industrial_mule_deer_permeability_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, default=str))


if __name__ == "__main__":
    main()
