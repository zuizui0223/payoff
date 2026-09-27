"""Registered Gate-B/C helpers for the Hoge Veluwe natural-history lane.

The Gate-B functions operate only on an already-normalized annual
cue-resource predictive-connectivity series. They do not read migrant or
resident timing. Gate C is exposed separately and refuses to run unless the
registered Gate-B status is INFORMATION_REVERSAL.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Iterable, Sequence


@dataclass(frozen=True)
class LineFit:
    intercept: float
    slope: float
    sse: float
    n: int
    k: int
    aicc: float


@dataclass(frozen=True)
class SegmentedFit:
    break_year: int
    split_index: int
    left: LineFit
    right: LineFit
    sse: float
    n: int
    k: int
    aicc: float
    delta_aicc_vs_linear: float
    predicted_start: float
    predicted_break_low: float
    predicted_final: float
    decline: float
    recovery: float
    recovery_fraction: float


def _aicc(sse: float, n: int, k: int) -> float:
    if n <= k + 1:
        return float("inf")
    sse = max(float(sse), 1e-15)
    aic = n * math.log(sse / n) + 2.0 * k
    return aic + (2.0 * k * (k + 1)) / (n - k - 1)


def _line_fit(x: Sequence[float], y: Sequence[float]) -> LineFit:
    if len(x) != len(y):
        raise ValueError("x/y length mismatch")
    n = len(x)
    if n < 3:
        raise ValueError("line fit requires >=3 rows")
    mx = sum(x) / n
    my = sum(y) / n
    sxx = sum((value - mx) ** 2 for value in x)
    if sxx <= 0.0:
        raise ValueError("line fit requires nonzero x variance")
    sxy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    slope = sxy / sxx
    intercept = my - slope * mx
    residuals = [
        yi - (intercept + slope * xi)
        for xi, yi in zip(x, y)
    ]
    sse = sum(value * value for value in residuals)
    return LineFit(
        intercept=float(intercept),
        slope=float(slope),
        sse=float(sse),
        n=n,
        k=2,
        aicc=_aicc(sse, n, 2),
    )


def _validate_series(
    years: Sequence[int],
    connectivity: Sequence[float],
) -> tuple[list[int], list[float]]:
    if len(years) != len(connectivity):
        raise ValueError("years/connectivity length mismatch")
    if len(years) < 3:
        raise ValueError("too few history years")
    rows = sorted(
        (int(year), float(value))
        for year, value in zip(years, connectivity)
    )
    ordered_years = [row[0] for row in rows]
    if len(set(ordered_years)) != len(ordered_years):
        raise ValueError("history years must be unique")
    values = [row[1] for row in rows]
    if not all(math.isfinite(value) for value in values):
        raise ValueError("connectivity must be finite")
    return ordered_years, values


def _best_segmented_fit(
    years: Sequence[int],
    connectivity: Sequence[float],
    *,
    min_segment_years: int,
    tie_tolerance: float = 1e-12,
) -> tuple[LineFit, SegmentedFit]:
    years, connectivity = _validate_series(years, connectivity)
    n = len(years)
    if n < 2 * min_segment_years:
        raise ValueError(
            "too few connectivity years for two registered segments"
        )

    x = [float(year) for year in years]
    linear = _line_fit(x, connectivity)
    candidates: list[SegmentedFit] = []

    for split in range(
        min_segment_years,
        n - min_segment_years + 1,
    ):
        left = _line_fit(x[:split], connectivity[:split])
        right = _line_fit(x[split:], connectivity[split:])
        sse = left.sse + right.sse
        k = 5  # two intercepts + two slopes + selected breakpoint
        aicc = _aicc(sse, n, k)
        left_start_year = x[0]
        left_end_year = x[split - 1]
        final_year = x[-1]
        predicted_start = (
            left.intercept + left.slope * left_start_year
        )
        predicted_low = (
            left.intercept + left.slope * left_end_year
        )
        predicted_final = (
            right.intercept + right.slope * final_year
        )
        decline = predicted_start - predicted_low
        recovery = predicted_final - predicted_low
        recovery_fraction = (
            recovery / decline
            if decline > 0.0
            else float("nan")
        )
        candidates.append(
            SegmentedFit(
                break_year=int(years[split]),
                split_index=split,
                left=left,
                right=right,
                sse=float(sse),
                n=n,
                k=k,
                aicc=float(aicc),
                delta_aicc_vs_linear=float(linear.aicc - aicc),
                predicted_start=float(predicted_start),
                predicted_break_low=float(predicted_low),
                predicted_final=float(predicted_final),
                decline=float(decline),
                recovery=float(recovery),
                recovery_fraction=float(recovery_fraction),
            )
        )

    best_aicc = min(row.aicc for row in candidates)
    tied = [
        row
        for row in candidates
        if abs(row.aicc - best_aicc) <= tie_tolerance
    ]
    best = min(tied, key=lambda row: row.break_year)
    return linear, best


def _geometry_passes(
    fit: SegmentedFit,
    *,
    min_delta_aicc: float,
    min_recovery_fraction: float,
) -> bool:
    return (
        fit.delta_aicc_vs_linear >= min_delta_aicc
        and fit.left.slope < 0.0
        and fit.right.slope > 0.0
        and math.isfinite(fit.recovery_fraction)
        and fit.recovery_fraction >= min_recovery_fraction
    )


def evaluate_information_reversal(
    years: Sequence[int],
    connectivity: Sequence[float],
    *,
    min_segment_years: int = 6,
    min_delta_aicc: float = 4.0,
    min_recovery_fraction: float = 0.50,
    stability_fraction: float = 0.80,
    breakpoint_tolerance_years: int = 2,
) -> dict:
    """Evaluate the frozen Gate-B reversal geometry.

    Leave-one-history-year-out non-estimable refits count as failures in the
    stability denominator. The stability gate is only evaluated when the
    full-sample geometry passes.
    """
    years, connectivity = _validate_series(years, connectivity)
    try:
        linear, best = _best_segmented_fit(
            years,
            connectivity,
            min_segment_years=min_segment_years,
        )
    except ValueError as exc:
        return {
            "status": "NOT_ESTIMABLE",
            "reason": str(exc),
        }

    full_geometry_pass = _geometry_passes(
        best,
        min_delta_aicc=min_delta_aicc,
        min_recovery_fraction=min_recovery_fraction,
    )

    result = {
        "status": "NO_CUE_RESOURCE_REVERSAL",
        "n_history_years": len(years),
        "linear": asdict(linear),
        "segmented": {
            **asdict(best),
            "left": asdict(best.left),
            "right": asdict(best.right),
        },
        "full_geometry_pass": full_geometry_pass,
        "registered_thresholds": {
            "min_segment_years": min_segment_years,
            "min_delta_aicc": min_delta_aicc,
            "min_recovery_fraction": min_recovery_fraction,
            "stability_fraction": stability_fraction,
            "breakpoint_tolerance_years": breakpoint_tolerance_years,
            "aicc_parameter_count_linear": 2,
            "aicc_parameter_count_segmented": 5,
        },
    }
    if not full_geometry_pass:
        result["stability"] = {
            "status": "NOT_EVALUATED_FULL_GEOMETRY_FAILED",
        }
        return result

    diagnostics = []
    sign_ok = 0
    break_ok = 0
    for omitted_index, omitted_year in enumerate(years):
        y_loo = [
            year
            for index, year in enumerate(years)
            if index != omitted_index
        ]
        c_loo = [
            value
            for index, value in enumerate(connectivity)
            if index != omitted_index
        ]
        try:
            _linear_loo, best_loo = _best_segmented_fit(
                y_loo,
                c_loo,
                min_segment_years=min_segment_years,
            )
            signs = (
                best_loo.left.slope < 0.0
                and best_loo.right.slope > 0.0
            )
            close = (
                abs(best_loo.break_year - best.break_year)
                <= breakpoint_tolerance_years
            )
            if signs:
                sign_ok += 1
            if close:
                break_ok += 1
            diagnostics.append(
                {
                    "omitted_year": omitted_year,
                    "estimable": True,
                    "break_year": best_loo.break_year,
                    "left_slope": best_loo.left.slope,
                    "right_slope": best_loo.right.slope,
                    "recovery_fraction": best_loo.recovery_fraction,
                    "slope_signs_preserved": signs,
                    "breakpoint_within_tolerance": close,
                }
            )
        except ValueError as exc:
            diagnostics.append(
                {
                    "omitted_year": omitted_year,
                    "estimable": False,
                    "reason": str(exc),
                    "slope_signs_preserved": False,
                    "breakpoint_within_tolerance": False,
                }
            )

    denominator = len(years)
    sign_fraction = sign_ok / denominator
    break_fraction = break_ok / denominator
    stability_pass = (
        sign_fraction >= stability_fraction
        and break_fraction >= stability_fraction
    )
    result["stability"] = {
        "status": "PASS" if stability_pass else "FAIL",
        "denominator": denominator,
        "slope_signs_preserved_n": sign_ok,
        "slope_signs_preserved_fraction": sign_fraction,
        "breakpoint_within_tolerance_n": break_ok,
        "breakpoint_within_tolerance_fraction": break_fraction,
        "diagnostics": diagnostics,
    }
    result["status"] = (
        "INFORMATION_REVERSAL"
        if stability_pass
        else "UNSTABLE_CUE_RESOURCE_REVERSAL"
    )
    return result


def fit_history_hac(
    records: Iterable[dict],
    *,
    break_year: int,
    reversal_status: str,
    min_branch_years: int = 6,
    maxlags: int = 7,
) -> dict:
    """Fit registered Gate C after a licensed Gate-B pass.

    Required record keys are year, connectivity and mismatch. The fit is
    restricted to the connectivity range observed on both branches, then
    centered at the mean of that overlap support. Calendar year is also
    centered and included as the preregistered secular-trend guard. Primary
    inference uses Newey-West HAC with maxlags=7 and finite-sample correction.
    """
    if reversal_status != "INFORMATION_REVERSAL":
        return {
            "status": "NOT_RUN",
            "reason": "Gate B did not license the history test",
        }

    try:
        import pandas as pd
        import statsmodels.formula.api as smf
    except ImportError as exc:
        raise RuntimeError(
            "Gate C requires pandas and statsmodels"
        ) from exc

    frame = pd.DataFrame(list(records)).copy()
    required = {"year", "connectivity", "mismatch"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"missing Gate-C columns: {missing}")
    frame = frame.dropna(
        subset=["year", "connectivity", "mismatch"]
    ).copy()
    frame["year"] = frame["year"].astype(int)
    if frame["year"].duplicated().any():
        raise ValueError("Gate C requires one annual record per year")
    frame = frame.sort_values("year").reset_index(drop=True)
    frame["branch"] = frame["year"].map(
        lambda year: "decline" if year < break_year else "recovery"
    )

    if set(frame["branch"]) != {"decline", "recovery"}:
        return {"status": "NOT_ESTIMABLE", "reason": "missing branch"}

    ranges = frame.groupby("branch")["connectivity"].agg(["min", "max"])
    lower = float(ranges["min"].max())
    upper = float(ranges["max"].min())
    if not lower <= upper:
        return {
            "status": "NOT_ESTIMABLE",
            "reason": "no overlapping connectivity support",
        }
    data = frame[
        (frame["connectivity"] >= lower)
        & (frame["connectivity"] <= upper)
    ].copy()
    counts = data["branch"].value_counts().to_dict()
    if any(counts.get(branch, 0) < min_branch_years for branch in ("decline", "recovery")):
        return {
            "status": "NOT_ESTIMABLE",
            "reason": "insufficient branch years after overlap restriction",
            "branch_counts": counts,
            "overlap_support": [lower, upper],
        }

    center = float(data["connectivity"].mean())
    year_center = float(data["year"].mean())
    data["centered_connectivity"] = data["connectivity"] - center
    data["centered_year"] = data["year"] - year_center
    formula = (
        "mismatch ~ centered_connectivity "
        "+ C(branch, Treatment(reference='decline')) "
        "+ centered_connectivity:C(branch, Treatment(reference='decline')) "
        "+ centered_year"
    )
    unadjusted_formula = (
        "mismatch ~ centered_connectivity "
        "+ C(branch, Treatment(reference='decline')) "
        "+ centered_connectivity:C(branch, Treatment(reference='decline'))"
    )
    model = smf.ols(formula, data=data)
    unadjusted_model = smf.ols(unadjusted_formula, data=data)
    hac = model.fit(
        cov_type="HAC",
        cov_kwds={
            "maxlags": maxlags,
            "use_correction": True,
        },
    )
    hac2 = model.fit(
        cov_type="HAC",
        cov_kwds={
            "maxlags": 2,
            "use_correction": True,
        },
    )
    hc3 = model.fit(cov_type="HC3")
    unadjusted_hac = unadjusted_model.fit(
        cov_type="HAC",
        cov_kwds={
            "maxlags": maxlags,
            "use_correction": True,
        },
    )

    branch_terms = [
        name
        for name in hac.params.index
        if name.startswith("C(branch")
        and ":centered_connectivity" not in name
    ]
    if len(branch_terms) != 1:
        return {
            "status": "NOT_ESTIMABLE",
            "reason": f"unexpected branch terms: {branch_terms}",
        }
    branch_term = branch_terms[0]

    interaction_terms = [
        name
        for name in hac.params.index
        if "centered_connectivity:C(branch" in name
        or (
            "C(branch" in name
            and ":centered_connectivity" in name
        )
    ]
    if len(interaction_terms) != 1:
        return {
            "status": "NOT_ESTIMABLE",
            "reason": f"unexpected interaction terms: {interaction_terms}",
        }
    interaction_term = interaction_terms[0]

    def extract(fit, term):
        estimate = float(fit.params[term])
        se = float(fit.bse[term])
        ci = fit.conf_int().loc[term]
        return {
            "estimate": estimate,
            "se": se,
            "ci_low_95": float(ci.iloc[0]),
            "ci_high_95": float(ci.iloc[1]),
            "p_value_two_sided": float(fit.pvalues[term]),
        }

    primary = extract(hac, branch_term)
    supported = (
        primary["ci_low_95"] > 0.0
        or primary["ci_high_95"] < 0.0
    )
    return {
        "status": "COMPLETE",
        "primary_supported": supported,
        "n": int(len(data)),
        "branch_counts": {
            key: int(value)
            for key, value in counts.items()
        },
        "overlap_support": [lower, upper],
        "connectivity_center": center,
        "year_center": year_center,
        "break_year": int(break_year),
        "time_trend_guard": {
            "required": True,
            "term": "centered_year",
            "primary_model_adjusted": True,
            "unadjusted_model_is_sensitivity_only": True,
        },
        "covariance": {
            "primary": f"HAC({maxlags}) finite-sample corrected",
            "secondary": ["HAC(2)", "HC3", "unadjusted HAC(7)"],
        },
        "branch_term": branch_term,
        "branch_at_mean_overlap": {
            "primary_hac7_year_adjusted": primary,
            "hac2_year_adjusted": extract(hac2, branch_term),
            "hc3_year_adjusted": extract(hc3, branch_term),
            "unadjusted_hac7": extract(unadjusted_hac, branch_term),
        },
        "interaction_term": interaction_term,
        "interaction": {
            "primary_hac7": extract(hac, interaction_term),
            "hac2": extract(hac2, interaction_term),
            "hc3": extract(hc3, interaction_term),
        },
    }
