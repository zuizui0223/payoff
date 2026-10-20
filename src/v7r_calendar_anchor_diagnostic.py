"""Post-outcome phase identity and calendar anchoring diagnostics for PAYOFF-B V7R.

This is NOT a preregistered endpoint. Neither an accounting identity nor
calendar departure synchronization identifies causal environmental cue use.
"""
from __future__ import annotations

from math import sqrt
from random import Random
from typing import Mapping, Sequence


def slope(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("slope needs equal-length vectors with >=2 observations")
    xx = [float(v) for v in x]
    yy = [float(v) for v in y]
    xbar, ybar = sum(xx) / len(xx), sum(yy) / len(yy)
    denominator = sum((v - xbar)**2 for v in xx)
    if denominator < 1e-12:
        raise ValueError("zero-variance predictor")
    return sum((a - xbar) * (b - ybar) for a, b in zip(xx, yy)) / denominator


def quantile(values: Sequence[float], p: float) -> float:
    ordered = sorted(float(v) for v in values)
    if not ordered or not 0.0 <= p <= 1.0:
        raise ValueError("quantile needs observations and p in [0, 1]")
    position = p * (len(ordered) - 1)
    lower = int(position)
    frac = position - lower
    return ordered[lower] * (1 - frac) + ordered[min(lower + 1, len(ordered) - 1)] * frac


def summarize_edge(
    rows: Sequence[Mapping[str, object]],
    *,
    draws: int = 4000,
    seed: int = 20261008,
) -> dict:
    """Summarize one transition with individual-cluster resampling.

    Required: e0, e1, a0, a1, stop_days, individual_id, year.
    """
    if len(rows) < 5:
        raise ValueError("at least five transition observations required")
    get = lambda field: [float(row[field]) for row in rows]
    e0, e1 = get("e0"), get("e1")
    arrival, next_arrival = get("a0"), get("a1")
    stay = get("stop_days")
    transit = [(b-a)-s for a,b,s in zip(arrival,next_arrival,stay)]
    spring_shift = [(a-x)-(b-y) for a,x,b,y in zip(arrival,e0,next_arrival,e1)]
    departure = [a+s for a,s in zip(arrival,stay)]
    years = [int(row["year"]) for row in rows]
    ids = [str(row["individual_id"]) for row in rows]
    unique_ids, unique_years = sorted(set(ids)), sorted(set(years))
    count_by_year = {year: years.count(year) for year in unique_years}
    arrival_mean_by_year = {
        year: sum(a for a,yr in zip(arrival,years) if yr==year)/count_by_year[year]
        for year in unique_years
    }
    departure_mean_by_year = {
        year: sum(a for a,yr in zip(departure,years) if yr==year)/count_by_year[year]
        for year in unique_years
    }
    a_center = [a-arrival_mean_by_year[yr] for a,yr in zip(arrival,years)]
    d_center = [d-departure_mean_by_year[yr] for d,yr in zip(departure,years)]
    den = sum(a*a for a in a_center)
    within_slope = sum(a*d for a,d in zip(a_center,d_center))/den if den>1e-12 else None
    within_ratio = (
        sqrt(sum(d*d for d in d_center)/den) if den>1e-12 else None
    )

    by_individual = {
        ident: [j for j,x in enumerate(ids) if x==ident]
        for ident in unique_ids
    }
    rng = Random(seed)
    sampled_stay, sampled_departure = [], []
    for _ in range(draws):
        sampled_indexes = [
            j for _ in unique_ids
            for j in by_individual[rng.choice(unique_ids)]
        ]
        try:
            sampled_stay.append(slope(
                [e0[j] for j in sampled_indexes],
                [stay[j] for j in sampled_indexes],
            ))
            sampled_departure.append(slope(
                [arrival[j] for j in sampled_indexes],
                [departure[j] for j in sampled_indexes],
            ))
        except ValueError:
            continue
    if len(sampled_stay) < draws*0.95:
        raise ValueError("too many degenerate bootstrap samples")

    year_leave_one = []
    for excluded in unique_years:
        included = [j for j,yr in enumerate(years) if yr!=excluded]
        try:
            year_leave_one.append(slope(
                [e0[j] for j in included], [stay[j] for j in included]
            ))
        except ValueError:
            continue

    b_stay = slope(e0,stay)
    b_transit = slope(e0,transit)
    b_spring = slope(e0,spring_shift)
    lam = slope(e0,e1)

    return {
        "n": len(rows),
        "n_individuals": len(unique_ids),
        "years": unique_years,
        "lambda": lam,
        "beta_stopover": b_stay,
        "beta_transit": b_transit,
        "beta_spring_shift": b_spring,
        "identity_residual": lam-(1+b_stay+b_transit+b_spring),
        "lambda_if_stopover_fixed_as_accounting": 1+b_transit+b_spring,
        "departure_on_arrival_calendar_slope": slope(arrival, departure),
        "departure_on_arrival_within_year_slope": within_slope,
        "departure_to_arrival_within_year_sd_ratio": within_ratio,
        "stopover_on_arrival_calendar_slope": slope(arrival,stay),
        "bootstrap_individual_cluster": {
            "draws": len(sampled_stay),
            "beta_stopover_q025": quantile(sampled_stay,0.025),
            "beta_stopover_q975": quantile(sampled_stay,0.975),
            "beta_stopover_fraction_below_zero": (
                sum(v<0 for v in sampled_stay)/len(sampled_stay)
            ),
            "departure_on_arrival_q025": quantile(sampled_departure,0.025),
            "departure_on_arrival_q975": quantile(sampled_departure,0.975),
        },
        "leave_one_year_out_beta_stopover_range": [
            min(year_leave_one), max(year_leave_one)
        ] if year_leave_one else [],
        "annual_arrival_departure": [
            {
                "year": year,
                "n": count_by_year[year],
                "origin_last_stop_arrival_range_days": (
                    max(a for a,yr in zip(arrival,years) if yr==year)
                    - min(a for a,yr in zip(arrival,years) if yr==year)
                ),
                "departure_range_days": (
                    max(d for d,yr in zip(departure,years) if yr==year)
                    - min(d for d,yr in zip(departure,years) if yr==year)
                ),
                "departure_mean_doy": departure_mean_by_year[year],
            }
            for year in unique_years
        ],
    }
