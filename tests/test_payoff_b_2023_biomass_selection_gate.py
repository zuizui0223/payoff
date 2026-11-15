"""Synthetic fixtures only; do not confuse these assertions with empirical support."""
import math
import pytest
pytest.importorskip("numpy")
pytest.importorskip("openpyxl")
import numpy as np

from scripts.payoff_b_2023_biomass_selection_gate import (
    MIN_BROODS, OFFSET_DAYS, audit, evaluate_stratum, prepare,
)


def fake_data(years=14, n_broods=12):
    food = []
    fitness = []
    for j in range(years):
        year = 2000 + j
        food.append({
            "AreaName": "Hoge Veluwe",
            "Year": year,
            "MidDate": 44.0 + j * 0.15,
            "MaxBiom": 1.0 + (j % 4) * 0.25,
        })
        for i in range(n_broods):
            fitness.append({
                "Area": "Hoge Veluwe", "Species": "Great Tit",
                "YearOfBreeding": year,
                "Mother": "M_" + str(year) + "_" + str(i),
                "LayDateApril": 12.0 + 0.4 * j + i,
                "NumberFledged": 11.0 - i * 0.7,
                "NumberFledgedDeviation": 0.0, "Include": 1,
            })
    return {"resource": food, "fitness": fitness}


def test_pre_registered_source_grain_and_signed_differential():
    panel, rejected = prepare(fake_data())
    years = panel[("Hoge Veluwe", "Great Tit")]
    assert len(years) == 14
    assert sum(x["n_broods"] for x in years) == 14 * 12
    assert all(x["differential"] < 0 for x in years)
    assert years[0]["mismatch_days"] == pytest.approx(
        np.mean(np.arange(12) + 12.0) + OFFSET_DAYS - 44.0)
    assert years[0]["log_peak_biomass"] == pytest.approx(math.log1p(1.0))
    assert not rejected


def test_all_years_holdout_and_no_false_primary_pass():
    panel, rejected = prepare(fake_data())
    x = evaluate_stratum(panel[("Hoge Veluwe", "Great Tit")])
    assert x["years"] == 14
    assert x["broods"] == 168
    assert x["fraction_years_earlier_laying_advantaged"] == 1.0
    assert sorted(x["loyo_mse"]) == [
        "I_intercept", "MBI_mismatch_biomass_interaction",
        "MB_mismatch_plus_biomass", "M_mismatch",
    ]
    obj = audit(panel, rejected)
    assert obj["primary_sites_all_admitted"] is False
    assert obj["primary_gate"] == "HOLD_NO_CONSISTENT_INCREMENT"
    assert obj["independent_unit"] == "site-species-year annual differential"


def test_manipulated_clutches_excluded_and_minimum_broods_gate():
    data = fake_data(years=13, n_broods=MIN_BROODS)
    data["fitness"][0]["Include"] = 0
    years, rejected = prepare(data)
    assert rejected["manipulated_or_not_included"] == 1
    assert rejected["site_species_year_too_few_broods"] == 1
    assert len(years[("Hoge Veluwe", "Great Tit")]) == 12


def test_duplicate_resource_site_year_fails_closed():
    data = fake_data()
    data["resource"].append(dict(data["resource"][0]))
    with pytest.raises(ValueError, match="Duplicate resource"):
        prepare(data)


def test_duplicate_female_first_clutch_fails_closed():
    data = fake_data()
    data["fitness"].append(dict(data["fitness"][0]))
    with pytest.raises(ValueError, match="Duplicate first brood"):
        prepare(data)


def test_blue_tit_offset_is_not_validated():
    data = fake_data()
    for row in data["fitness"]:
        row["Species"] = "Blue Tit"
    panel, rejected = prepare(data)
    result = audit(panel, rejected)
    assert "UNVALIDATED" in result["strata"]["Hoge Veluwe|Blue Tit"]["species_offset_validation"]
    assert result["primary_sites_all_admitted"] is False


def test_no_mistaking_peak_mass_for_food_exposure():
    data = fake_data()
    panel, rejected = prepare(data)
    result = audit(panel, rejected)
    assert result["food_demand_and_daily_biomass_observed"] is False
    assert result["not_total_fitness_or_causal_selection"] is True
    assert "not integrated" in result["resource_unit"]
