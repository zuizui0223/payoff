"""Source-agnostic *potential prey* exposure; no fitted diet or fitness.

Input requires independently observed within-season resource sampling and a
source-verified nest hatch date. Counts/standardized beating and edible prey mass
are distinct currencies and must never be silently mixed.

For each site x year x prey guild:
  - original sampling dates and positive effort (n standardized beats)
  - raw count or measured mass; zeros are valid
  - within-day rate from sum(amount) / sum(effort)
  - only piecewise-linear interpolation across observed adjacent dates <=max_gap
  - absolutely NO extrapolation outside observation support
  - uniform hypothetical 14-day nestling demand (not measured energetic demand)

This module has no external library dependencies so minimal CI can test it.
"""
from collections import defaultdict
from datetime import date
import math


class ResourceContactNotAdmitted(ValueError):
    pass


def _integer_date(iso_date):
    if isinstance(iso_date, date):
        return iso_date.toordinal()
    if not isinstance(iso_date, str):
        raise ResourceContactNotAdmitted("Resource dates must be source-verifiable ISO dates")
    try:
        return date.fromisoformat(iso_date).toordinal()
    except ValueError as e:
        raise ResourceContactNotAdmitted("Resource dates must be YYYY-MM-DD") from e


def daily_resource_rates(samples):
    """Aggregate standardized sampling rates without creating inferred biomass.

    samples are from exactly one site/year/guild and must include:
      source_id, site_id, year, guild, observation_date,
      amount, effort_n_beats, currency.
    Return sorted (date ordinal, amount per beat) and one verified currency.
    """
    if not samples:
        raise ResourceContactNotAdmitted("No real resource observations")
    required = {"source_id", "site_id", "year", "guild", "observation_date",
                "amount", "effort_n_beats", "currency"}
    if any(not required.issubset(r) for r in samples):
        raise ResourceContactNotAdmitted("Missing required source/provenance/effort fields")
    for label in ("source_id", "site_id", "year", "guild", "currency"):
        if len({str(r[label]) for r in samples}) != 1:
            raise ResourceContactNotAdmitted("Cannot merge unlike " + label)
    currency = str(samples[0]["currency"])
    if currency not in ("count_per_beating", "measured_mg_per_beating"):
        raise ResourceContactNotAdmitted("Unsupported or inferred biological measurement currency")
    by_day = defaultdict(lambda: [0.0, 0.0])
    for row in samples:
        d = _integer_date(row["observation_date"])
        try:
            amount = float(row["amount"])
            effort = float(row["effort_n_beats"])
        except (ValueError, TypeError) as e:
            raise ResourceContactNotAdmitted("Non-numeric observation/effort") from e
        if (not math.isfinite(amount) or amount < 0
                or not math.isfinite(effort) or effort <= 0):
            raise ResourceContactNotAdmitted("Invalid abundance or sampling effort")
        by_day[d][0] += amount
        by_day[d][1] += effort
    if len(by_day) < 2:
        raise ResourceContactNotAdmitted("Need repeated within-season source measurements")
    return sorted((d, mass / effort) for d, (mass, effort) in by_day.items()), currency


def demand_window_contact(samples, *, hatch_date, duration_days=14,
                          max_observation_gap_days=8,
                          min_coverage_fraction=0.80):
    """Compute an explicitly *potential* consumer-demand-window supply proxy.

    Uniform day weights, not individual nestling intake. Gap-based missingness
    means a positive trend cannot be created by extrapolating data.
    """
    if not isinstance(duration_days, int) or not 1 <= duration_days <= 40:
        raise ValueError("Invalid pre-fixed demand-window length")
    if max_observation_gap_days < 1:
        raise ValueError("Invalid interpolation support")
    h = _integer_date(hatch_date)
    observations, currency = daily_resource_rates(samples)
    dates = [x[0] for x in observations]
    left = 0
    values = []
    unsupported = []
    for day in range(h, h + duration_days):
        while left + 1 < len(dates) and dates[left + 1] < day:
            left += 1
        if left + 1 >= len(dates) or day < dates[left]:
            unsupported.append(day)
            continue
        d0, y0 = observations[left]
        d1, y1 = observations[left + 1]
        if d1 - d0 > max_observation_gap_days:
            unsupported.append(day)
            continue
        value = y0 + (y1 - y0) * (day - d0) / (d1 - d0)
        values.append(value)
    coverage = len(values) / duration_days
    if coverage < min_coverage_fraction:
        raise ResourceContactNotAdmitted(
            f"Insufficient observed support: {coverage:.3f} < {min_coverage_fraction:.3f}"
        )
    return {
        "currency": currency,
        "hatch_date": str(hatch_date),
        "window_days": duration_days,
        "prey_mean_per_beating_during_demand_proxy": sum(values) / len(values),
        "prey_sum_per_beating_days": sum(values),
        "covered_days": len(values),
        "coverage_fraction": coverage,
        "unsupported_days": len(unsupported),
        "observed_peak_per_beating": max(x[1] for x in observations),
        "interpolation_only": True,
        "demand_is_uniform_proxy_not_measured": True,
        "real_food_intake_measured": False,
        "fitness_effect_fitted": False,
    }


def alternative_prey_contact(caterpillars, alternatives, *, hatch_date):
    """Separate guild outputs. Never add biomass and counts without a conversion."""
    c = demand_window_contact(caterpillars, hatch_date=hatch_date)
    a = demand_window_contact(alternatives, hatch_date=hatch_date)
    if c["currency"] != a["currency"]:
        return {"status": "SEPARATE_UNITS_NO_SUM", "caterpillars": c, "alternatives": a}
    return {
        "status": "SAME_CURRENCY_POTENTIAL_INDEX_ONLY",
        "caterpillars": c,
        "alternatives": a,
        "sum_raw_count_proxies": (
            c["prey_mean_per_beating_during_demand_proxy"]
            + a["prey_mean_per_beating_during_demand_proxy"]
        ),
        "equal_guild_weight_is_not_dietary_or_energetic_equivalence": True,
        "fitness_effect_fitted": False,
    }
