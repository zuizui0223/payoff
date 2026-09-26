#!/usr/bin/env python3
"""Long-term pied-flycatcher cue--driver information-history analysis.

Primary driver:
  annual standardized selection gradient from PLOS S1 Data, panel A.

Primary cue:
  NCEP/NCAR Reanalysis 1 daily near-surface air temperature over a fixed
  coarse-grid Ivory Coast proxy, averaged over a source-defined 20-day period
  beginning 18 February each year.

The timing outcome is never used to choose the cue window or connectivity
breakpoint.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import sys
import tempfile
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.predictive_connectivity import detrended_predictive_connectivity


ERDDAP = (
    "https://coastwatch.pfeg.noaa.gov/erddap/griddap/"
    "esrlNcepRe.csv"
)


@dataclass(frozen=True)
class LineFit:
    intercept: float
    slope: float
    sse: float
    n: int
    k: int
    aicc: float


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--s1", type=Path, required=True)
    p.add_argument("--start-year", type=int, default=1980)
    p.add_argument("--end-year", type=int, default=2010)
    p.add_argument("--window-years", type=int, default=8)
    p.add_argument("--min-pairs", type=int, default=6)
    p.add_argument("--min-segment-years", type=int, default=6)
    p.add_argument("--erddap", default=ERDDAP)
    p.add_argument(
        "--annual-output",
        type=Path,
        default=Path("outputs/cv24c_cue_driver_annual.csv"),
    )
    p.add_argument(
        "--connectivity-output",
        type=Path,
        default=Path("outputs/cv24c_cue_driver_connectivity.csv"),
    )
    p.add_argument(
        "--result-output",
        type=Path,
        default=Path("outputs/cv24c_cue_driver_result.json"),
    )
    return p.parse_args()


def _aicc(sse: float, n: int, k: int) -> float:
    if n <= k + 1:
        return float("inf")
    sse = max(float(sse), 1e-15)
    aic = n * math.log(sse / n) + 2.0 * k
    return aic + (2.0 * k * (k + 1)) / (n - k - 1)


def _line_fit(x, y) -> LineFit:
    import numpy as np

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 3:
        raise ValueError("line fit requires >=3 rows")
    X = np.column_stack([np.ones(len(x)), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    residual = y - X @ coef
    sse = float(np.sum(residual**2))
    return LineFit(
        intercept=float(coef[0]),
        slope=float(coef[1]),
        sse=sse,
        n=int(len(x)),
        k=2,
        aicc=_aicc(sse, len(x), 2),
    )


def _two_line_fit(x, y, split_index: int):
    import numpy as np

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    left = _line_fit(x[:split_index], y[:split_index])
    right = _line_fit(x[split_index:], y[split_index:])
    sse = left.sse + right.sse
    n = len(x)
    return {
        "left": left,
        "right": right,
        "sse": sse,
        "aicc": _aicc(sse, n, 4),
        "split_index": split_index,
        "break_year": int(x[split_index]),
    }


def _load_selection_gradient(path: Path):
    import pandas as pd

    frame = pd.read_excel(path, sheet_name="panel A")
    frame = frame.rename(
        columns={
            "year": "year",
            "standardised selection gradient": "selection_gradient",
            "standard error": "selection_se",
        }
    )
    frame = frame[["year", "selection_gradient", "selection_se"]].copy()
    frame["year"] = pd.to_numeric(frame["year"], errors="coerce")
    frame["selection_gradient"] = pd.to_numeric(
        frame["selection_gradient"],
        errors="coerce",
    )
    frame["selection_se"] = pd.to_numeric(
        frame["selection_se"],
        errors="coerce",
    )
    frame = frame.dropna().copy()
    frame["year"] = frame["year"].astype(int)
    return frame


def _ncep_query_url(base: str, year: int) -> str:
    start = date(year, 2, 18)
    end = start + timedelta(days=19)
    query = (
        "air"
        f"[({start.isoformat()}T00:00:00Z):1:"
        f"({end.isoformat()}T00:00:00Z)]"
        "[(10):1:(5)]"
        "[(352.5):1:(357.5)]"
    )
    return base + "?" + quote(
        query,
        safe="[]():,.-TZ",
    )


def _download_psl_fallback(session, year: int):
    import numpy as np
    import xarray as xr

    url = (
        "https://psl.noaa.gov/thredds/fileServer/"
        "Datasets/ncep.reanalysis.dailyavgs/surface/"
        f"air.sig995.{year}.nc"
    )
    response = session.get(url, timeout=180)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile(suffix=".nc") as handle:
        handle.write(response.content)
        handle.flush()
        with xr.open_dataset(handle.name, engine="netcdf4") as ds:
            start = date(year, 2, 18)
            end = start + timedelta(days=19)
            subset = ds["air"].sel(
                time=slice(start.isoformat(), end.isoformat()),
                lat=[10.0, 7.5, 5.0],
                lon=[352.5, 355.0, 357.5],
            )
            values = np.asarray(subset.values, dtype=float)
            finite = values[np.isfinite(values)]
            if finite.size < 100:
                raise ValueError(
                    f"unexpectedly few PSL NCEP values for {year}: "
                    f"{finite.size}"
                )
            cue_c = float(finite.mean() - 273.15)
    return {
        "year": year,
        "ivory_coast_temp_c": cue_c,
        "ncep_rows": int(finite.size),
        "grid_lat_min": 5.0,
        "grid_lat_max": 10.0,
        "grid_lon_min": 352.5,
        "grid_lon_max": 357.5,
        "source_url": url,
        "transport": "psl_http_fallback",
    }


def _download_annual_cue(session, base: str, year: int):
    import pandas as pd
    import requests

    url = _ncep_query_url(base, year)
    try:
        response = session.get(url, timeout=90)
        response.raise_for_status()
        frame = pd.read_csv(io.StringIO(response.text))
        if "air" not in frame.columns:
            raise ValueError(
                f"ERDDAP response missing air column for {year}: "
                f"{list(frame.columns)}"
            )
        frame["air"] = pd.to_numeric(frame["air"], errors="coerce")
        frame["latitude"] = pd.to_numeric(
            frame.get("latitude"),
            errors="coerce",
        )
        frame["longitude"] = pd.to_numeric(
            frame.get("longitude"),
            errors="coerce",
        )
        frame = frame.dropna(subset=["air"]).copy()
        if len(frame) < 100:
            raise ValueError(
                f"unexpectedly few NCEP rows for {year}: {len(frame)}"
            )
        cue_c = float(frame["air"].mean() - 273.15)
        return {
            "year": year,
            "ivory_coast_temp_c": cue_c,
            "ncep_rows": int(len(frame)),
            "grid_lat_min": float(frame["latitude"].min()),
            "grid_lat_max": float(frame["latitude"].max()),
            "grid_lon_min": float(frame["longitude"].min()),
            "grid_lon_max": float(frame["longitude"].max()),
            "source_url": url,
            "transport": "erddap",
        }
    except (requests.RequestException, ValueError):
        return _download_psl_fallback(session, year)


def _build_connectivity(annual, window_years: int, min_pairs: int):
    import pandas as pd

    rows = []
    years = sorted(annual["year"].unique())
    for target_year in years:
        history = annual[
            (annual["year"] >= target_year - window_years)
            & (annual["year"] < target_year)
        ].dropna(
            subset=["ivory_coast_temp_c", "selection_gradient"]
        )
        if len(history) < min_pairs:
            continue
        estimate = detrended_predictive_connectivity(
            history["year"].to_list(),
            history["ivory_coast_temp_c"].to_list(),
            history["selection_gradient"].to_list(),
            min_pairs=min_pairs,
        )
        rows.append(
            {
                "target_year": int(target_year),
                "training_n": int(estimate.n_pairs),
                "connectivity_rho": float(estimate.rho),
                "connectivity_r2": float(estimate.r_squared),
                "gaussian_binary_agreement": float(
                    estimate.gaussian_binary_agreement
                ),
            }
        )
    return pd.DataFrame(rows)


def _detect_reversal(connectivity, min_segment_years: int):
    import numpy as np

    data = connectivity.dropna(subset=["connectivity_rho"]).copy()
    data = data.sort_values("target_year")
    x = data["target_year"].to_numpy(dtype=float)
    y = data["connectivity_rho"].to_numpy(dtype=float)

    if len(data) < 2 * min_segment_years:
        return {
            "status": "NOT_ESTIMABLE",
            "reason": "too few connectivity years for two declared segments",
        }

    linear = _line_fit(x, y)
    candidates = []
    for split in range(
        min_segment_years,
        len(data) - min_segment_years + 1,
    ):
        candidates.append(_two_line_fit(x, y, split))
    best = min(candidates, key=lambda row: row["aicc"])

    left = best["left"]
    right = best["right"]
    delta_aicc = linear.aicc - best["aicc"]

    break_year = best["break_year"]
    left_start_year = float(x[0])
    left_end_year = float(x[best["split_index"] - 1])
    final_year = float(x[-1])
    predicted_start = left.intercept + left.slope * left_start_year
    predicted_low = left.intercept + left.slope * left_end_year
    predicted_final = right.intercept + right.slope * final_year

    decline = predicted_start - predicted_low
    recovery = predicted_final - predicted_low
    recovery_fraction = (
        recovery / decline
        if decline > 0.0
        else float("nan")
    )

    reversal = (
        delta_aicc >= 4.0
        and left.slope < 0.0
        and right.slope > 0.0
        and math.isfinite(recovery_fraction)
        and recovery_fraction >= 0.50
    )
    return {
        "status": (
            "INFORMATION_REVERSAL"
            if reversal
            else "NO_CUE_DRIVER_REVERSAL"
        ),
        "linear": {
            "slope": linear.slope,
            "aicc": linear.aicc,
            "sse": linear.sse,
        },
        "segmented": {
            "break_year": break_year,
            "left_slope": left.slope,
            "right_slope": right.slope,
            "aicc": best["aicc"],
            "sse": best["sse"],
            "delta_aicc_vs_linear": delta_aicc,
            "predicted_start_connectivity": predicted_start,
            "predicted_break_connectivity": predicted_low,
            "predicted_final_connectivity": predicted_final,
            "recovery_fraction": recovery_fraction,
        },
    }


def _fit_history_if_licensed(annual, connectivity, reversal):
    if reversal.get("status") != "INFORMATION_REVERSAL":
        return {
            "status": "NOT_RUN",
            "reason": "information reversal gate did not pass",
        }

    import numpy as np
    import pandas as pd
    import statsmodels.formula.api as smf

    break_year = int(reversal["segmented"]["break_year"])
    data = annual.merge(
        connectivity,
        left_on="year",
        right_on="target_year",
        how="inner",
    ).dropna(
        subset=["selection_gradient", "connectivity_rho"]
    )
    data["regime_direction"] = np.where(
        data["year"] < break_year,
        "degradation",
        "recovery",
    )
    if data["regime_direction"].nunique() < 2:
        return {"status": "NOT_ESTIMABLE"}

    model = smf.ols(
        "selection_gradient ~ connectivity_rho * C(regime_direction)",
        data=data,
    ).fit(cov_type="HC3")
    names = list(model.params.index)
    interaction_names = [
        name for name in names
        if "connectivity_rho:C(regime_direction)" in name
    ]
    if len(interaction_names) != 1:
        return {
            "status": "NOT_ESTIMABLE",
            "reason": f"unexpected interaction terms: {interaction_names}",
        }
    term = interaction_names[0]
    estimate = float(model.params[term])
    se = float(model.bse[term])
    return {
        "status": "COMPLETE",
        "rows": int(len(data)),
        "term": term,
        "estimate": estimate,
        "se_hc3": se,
        "ci_low_95": estimate - 1.96 * se,
        "ci_high_95": estimate + 1.96 * se,
        "p_value_two_sided": float(model.pvalues[term]),
    }


def main():
    args = parse_args()
    try:
        import pandas as pd
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
    except ImportError as exc:
        raise RuntimeError(
            "analysis requires pandas, requests, openpyxl, statsmodels, numpy"
        ) from exc

    selection = _load_selection_gradient(args.s1)
    session = requests.Session()
    session.headers.update(
        {"User-Agent": "PAYOFF-B-cue-driver/1.0"}
    )
    retry = Retry(
        total=8,
        connect=5,
        read=5,
        status=8,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=2,
        pool_maxsize=2,
    )
    session.mount("https://", adapter)
    cue_rows = [
        _download_annual_cue(session, args.erddap, year)
        for year in range(args.start_year, args.end_year + 1)
    ]
    cue = pd.DataFrame(cue_rows)

    annual = pd.DataFrame(
        {"year": list(range(args.start_year, args.end_year + 1))}
    ).merge(cue, on="year", how="left").merge(
        selection,
        on="year",
        how="left",
    )

    connectivity = _build_connectivity(
        annual,
        args.window_years,
        args.min_pairs,
    )
    reversal = _detect_reversal(
        connectivity,
        args.min_segment_years,
    )
    history = _fit_history_if_licensed(
        annual,
        connectivity,
        reversal,
    )

    args.annual_output.parent.mkdir(parents=True, exist_ok=True)
    annual.to_csv(args.annual_output, index=False)
    connectivity.to_csv(args.connectivity_output, index=False)

    result = {
        "result_id": "payoff_b_cv24c_cue_driver_v1",
        "contract_id": "payoff_b_cv24c_cue_driver_decoupling_v1_20260927",
        "status": reversal["status"],
        "source": {
            "selection_gradient": (
                "PLOS S1 Data panel A, DOI "
                "10.1371/journal.pbio.1002120.s001"
            ),
            "cue": "NCEP/NCAR Reanalysis 1 daily air.sig995",
            "transport_rule": (
                "ERDDAP primary; identical PSL yearly NetCDF fallback "
                "on transport failure"
            ),
            "cue_window": "20 calendar days beginning 18 February",
            "spatial_proxy": {
                "latitudes_deg_n": [10.0, 7.5, 5.0],
                "longitudes_deg_e": [352.5, 355.0, 357.5],
                "description": (
                    "fixed 3x3 coarse-grid bounding proxy for Ivory Coast"
                ),
            },
        },
        "selection_rows": int(
            annual["selection_gradient"].notna().sum()
        ),
        "cue_years": int(
            annual["ivory_coast_temp_c"].notna().sum()
        ),
        "connectivity_rows": int(len(connectivity)),
        "reversal_gate": reversal,
        "history_test": history,
        "claim_boundary": [
            "Tomotani et al. 2021 already proposed climate-driven cue-driver decoupling",
            "the Ivory Coast cue uses a fixed coarse-grid proxy and source-defined average calendar window",
            "no cue window or breakpoint was selected from the selection-gradient outcome",
            "this is a within-population cue-driver history lane, not interaction-network hysteresis",
        ],
    }
    args.result_output.parent.mkdir(parents=True, exist_ok=True)
    args.result_output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
