"""Synthetic-only tests; not evidence of real prey-bird matching."""
import pytest
from src.payoff_b_resource_contact import (
    ResourceContactNotAdmitted, alternative_prey_contact,
    daily_resource_rates, demand_window_contact,
)


def resource(values, *, source="public_TEST_ONLY", currency="count_per_beating",
             site="S1", guild="caterpillars"):
    days = ["2020-05-01", "2020-05-05", "2020-05-09",
            "2020-05-13", "2020-05-17", "2020-05-21"]
    assert len(values) == len(days)
    return [
        dict(source_id=source, site_id=site, year=2020, guild=guild,
             observation_date=d, amount=v, effort_n_beats=1, currency=currency)
        for d, v in zip(days, values)
    ]


def test_more_annual_peak_can_means_less_window_supply():
    synchronised = demand_window_contact(
        resource([0, 2, 4, 6, 2, 0]), hatch_date="2020-05-04")
    shifted = demand_window_contact(
        resource([12, 8, 2, 0, 0, 0]), hatch_date="2020-05-04")
    assert shifted["observed_peak_per_beating"] > synchronised["observed_peak_per_beating"]
    assert shifted["prey_mean_per_beating_during_demand_proxy"] < synchronised["prey_mean_per_beating_during_demand_proxy"]
    assert shifted["real_food_intake_measured"] is False


def test_sample_effort_weighted_not_pseudo_independent_replicates():
    vals = resource([0, 2, 4, 6, 2, 0])
    dupe = dict(vals[2])
    dupe["amount"] = 16
    dupe["effort_n_beats"] = 4
    vals.append(dupe)
    series, currency = daily_resource_rates(vals)
    assert currency == "count_per_beating"
    assert len(series) == 6
    assert series[2][1] == pytest.approx((4 + 16) / (1 + 4))


def test_no_out_of_support_extrapolation():
    with pytest.raises(ResourceContactNotAdmitted, match="Insufficient"):
        demand_window_contact(resource([0, 2, 4, 6, 2, 0]),
                              hatch_date="2020-05-16")


def test_gaps_over_eight_days_fail_closed():
    vals = resource([0, 2, 4, 6, 2, 0])
    vals = [v for i, v in enumerate(vals) if i not in (2, 3, 4)]
    with pytest.raises(ResourceContactNotAdmitted, match="Insufficient"):
        demand_window_contact(vals, hatch_date="2020-05-04")


def test_currency_blocked_not_interpreted_as_grams():
    prey = resource([0, 2, 4, 6, 2, 0])
    other = resource([1, 1, 1, 1, 1, 1], guild="beetles",
                     currency="measured_mg_per_beating")
    result = alternative_prey_contact(prey, other, hatch_date="2020-05-04")
    assert result["status"] == "SEPARATE_UNITS_NO_SUM"
    assert "sum_raw_count_proxies" not in result


def test_same_currency_sum_is_not_energy():
    prey = resource([0, 2, 4, 6, 2, 0])
    other = resource([1, 1, 1, 1, 1, 1], guild="beetles")
    result = alternative_prey_contact(prey, other, hatch_date="2020-05-04")
    assert result["status"] == "SAME_CURRENCY_POTENTIAL_INDEX_ONLY"
    assert result["equal_guild_weight_is_not_dietary_or_energetic_equivalence"] is True


def test_cross_site_or_year_pool_rejected():
    vals = resource([0, 2, 4, 6, 2, 0])
    vals[2]["site_id"] = "S2"
    with pytest.raises(ResourceContactNotAdmitted, match="site_id"):
        daily_resource_rates(vals)


def test_invalid_units_or_negative_count_rejected():
    vals = resource([0, 2, 4, 6, 2, 0])
    vals[0]["amount"] = -1
    with pytest.raises(ResourceContactNotAdmitted, match="Invalid"):
        daily_resource_rates(vals)
    vals = resource([0, 2, 4, 6, 2, 0], currency="index_from_NDVI")
    with pytest.raises(ResourceContactNotAdmitted, match="Unsupported"):
        daily_resource_rates(vals)
