#!/usr/bin/env python3
"""Build pre-outcome route phenological predictability for PAYOFF-B V7.

IMPORTANT
---------
This script builds the environmental predictor only. It never reads
phenological-lag/recovery response columns and never fits the focal V7 model.

Run only after the USA-NPN source gate is frozen as PASS and with an explicitly
selected source allowed by the pre-outcome source contract/amendment.

Inputs
------
A route-manifest CSV containing only:
motusTagID, species, year, site_id_r1, lon_r1, lat_r1,
site_id_r2, lon_r2, lat_r2, dist_km

Outputs
-------
site_year_first_leaf.csv
route_predictability.csv
source_manifest.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import rasterio
from rasterio.io import MemoryFile
from scipy.stats import spearmanr

WCS = "https://geoserver.usanpn.org/geoserver/si-x/wcs"

SOURCE = {
    "prism": {
        "coverage": "si-x:average_leaf_prism",
        "start": 1981,
        "mode": "individual_preoutcome",
        "bbox": (-125.0208333333, 24.0625, -66.4791666666, 49.9375),
    },
    "best": {
        "coverage": "si-x:average_leaf_best",
        "start": 1981,
        "end": 2013,
        "mode": "common_1981_2013",
        "bbox": (-180.0, 0.0, 0.0, 90.0),
    },
}


def wcs_params(coverage: str, year: int) -> dict[str, str]:
    timestamp = f'{year}-01-01T07:00:00.000Z'
    return {
        "service": "WCS",
        "version": "2.0.1",
        "request": "GetCoverage",
        "CoverageId": coverage,
        "srs": "EPSG:4269",
        "subset": f'http://www.opengis.net/def/axis/OGC/0/time("{timestamp}")',
        "format": "image/geotiff",
    }


def fetch_tiff(session: requests.Session, coverage: str, year: int, attempts: int = 5) -> tuple[bytes, str]:
    last = None
    for i in range(attempts):
        try:
            r = session.get(WCS, params=wcs_params(coverage, year), timeout=180)
            r.raise_for_status()
            b = r.content
            if len(b) < 1024:
                raise RuntimeError(f"unexpectedly small WCS payload ({len(b)} bytes)")
            if not (b[:4] in (b"II*\x00", b"MM\x00*")):
                ct = r.headers.get("content-type", "")
                raise RuntimeError(f"payload is not TIFF; content-type={ct!r}; prefix={b[:80]!r}")
            return b, hashlib.sha256(b).hexdigest()
        except Exception as e:
            last = e
            if i + 1 < attempts:
                time.sleep(2 ** i)
    raise RuntimeError(f"WCS fetch failed for {coverage} {year}: {last}")


def sample_points(tiff_bytes: bytes, coords: list[tuple[float, float]]) -> np.ndarray:
    with MemoryFile(tiff_bytes) as mem:
        with mem.open() as ds:
            vals = np.array([v[0] for v in ds.sample(coords)], dtype=float)
            nodata = ds.nodata
            if nodata is not None:
                vals[np.isclose(vals, nodata)] = np.nan
            vals[~np.isfinite(vals)] = np.nan
            return vals


def pearson_complete(a: np.ndarray, b: np.ndarray) -> tuple[float, int]:
    ok = np.isfinite(a) & np.isfinite(b)
    n = int(ok.sum())
    if n < 3:
        return math.nan, n
    aa, bb = a[ok], b[ok]
    if np.std(aa) == 0 or np.std(bb) == 0:
        return math.nan, n
    return float(np.corrcoef(aa, bb)[0, 1]), n


def spearman_complete(a: np.ndarray, b: np.ndarray) -> tuple[float, int]:
    ok = np.isfinite(a) & np.isfinite(b)
    n = int(ok.sum())
    if n < 3:
        return math.nan, n
    stat = spearmanr(a[ok], b[ok], nan_policy="omit")
    return float(stat.statistic), n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--routes", type=Path, required=True)
    ap.add_argument("--source", choices=sorted(SOURCE), required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()

    cfg = SOURCE[args.source]
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    routes = pd.read_csv(args.routes)
    required = [
        "motusTagID", "species", "year",
        "site_id_r1", "lon_r1", "lat_r1",
        "site_id_r2", "lon_r2", "lat_r2", "dist_km",
    ]
    miss = [c for c in required if c not in routes.columns]
    if miss:
        raise SystemExit(f"missing route-manifest columns: {miss}")

    # Explicit guard: no focal-response field may be supplied to this script.
    forbidden_patterns = ("lag_", "recovery", "detDay", "sos_best_act", "gw_rate")
    bad = [c for c in routes.columns if any(p.lower() in c.lower() for p in forbidden_patterns)]
    if bad:
        raise SystemExit(f"route manifest contains forbidden focal-response columns: {bad}")

    routes["year"] = routes["year"].astype(int)

    # Unique receiver coordinates.
    sites1 = routes[["site_id_r1", "lon_r1", "lat_r1"]].rename(
        columns={"site_id_r1": "site_id", "lon_r1": "lon", "lat_r1": "lat"}
    )
    sites2 = routes[["site_id_r2", "lon_r2", "lat_r2"]].rename(
        columns={"site_id_r2": "site_id", "lon_r2": "lon", "lat_r2": "lat"}
    )
    sites = pd.concat([sites1, sites2], ignore_index=True).drop_duplicates("site_id")
    coords = list(zip(sites["lon"].astype(float), sites["lat"].astype(float)))

    if args.source == "prism":
        years = list(range(cfg["start"], int(routes["year"].max())))
    else:
        years = list(range(cfg["start"], cfg["end"] + 1))

    session = requests.Session()
    session.headers.update({"User-Agent": "PAYOFF-B-V7-source-reanalysis/1.0"})

    rows = []
    source_files = []
    for year in years:
        b, sha = fetch_tiff(session, cfg["coverage"], year)
        vals = sample_points(b, coords)
        source_files.append({"year": year, "sha256": sha, "bytes": len(b)})
        for site_id, val in zip(sites["site_id"], vals):
            rows.append({"site_id": site_id, "year": year, "first_leaf_doy": val})

    sy = pd.DataFrame(rows)
    sy.to_csv(out / "site_year_first_leaf.csv", index=False)

    wide = sy.pivot(index="year", columns="site_id", values="first_leaf_doy")

    result = []
    for r in routes.itertuples(index=False):
        if args.source == "prism":
            allowed_years = [y for y in years if y < int(r.year)]
        else:
            allowed_years = years

        try:
            a = wide.loc[allowed_years, r.site_id_r1].to_numpy(dtype=float)
            b = wide.loc[allowed_years, r.site_id_r2].to_numpy(dtype=float)
        except KeyError:
            q, n = math.nan, 0
            qs, ns = math.nan, 0
        else:
            q, n = pearson_complete(a, b)
            qs, ns = spearman_complete(a, b)

        result.append({
            "motusTagID": r.motusTagID,
            "species": r.species,
            "year": int(r.year),
            "site_id_r1": r.site_id_r1,
            "site_id_r2": r.site_id_r2,
            "dist_km": float(r.dist_km),
            "predictability_pearson": q,
            "predictability_spearman": qs,
            "historical_n": min(n, ns),
            "source": args.source,
        })

    pred = pd.DataFrame(result)
    pred.to_csv(out / "route_predictability.csv", index=False)

    manifest = {
        "source": args.source,
        "coverage": cfg["coverage"],
        "years_requested": years,
        "route_rows": int(len(routes)),
        "unique_sites": int(len(sites)),
        "predictability_nonmissing": int(pred["predictability_pearson"].notna().sum()),
        "predictability_n_ge_20": int((pred["historical_n"] >= 20).sum()),
        "source_files": source_files,
        "response_values_read": False,
        "focal_model_fit": False,
    }
    (out / "source_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Gate is source/predictor completeness only; no outcome inspected.
    if int((pred["historical_n"] >= 20).sum()) < 50:
        raise SystemExit("predictability completeness gate failed: <50 bird routes with >=20 historical years")


if __name__ == "__main__":
    main()
