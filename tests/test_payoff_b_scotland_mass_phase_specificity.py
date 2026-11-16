"""Synthetic-only seasonal-versus-hatch mass phase specificity contracts.

No original ecological outcomes are simulated as evidence. These tests check
exact validation grouping, record units, sample admission, and measurement bounds.
"""
import math
import pytest
np=pytest.importorskip("numpy")
pytest.importorskip("openpyxl")
from scripts.payoff_b_scotland_mass_phase_specificity import (
    MODELS, grouped_prediction, run, season_means
)


def source_row(day,mass,site="ABC",year=2019,beatings=1):
    return {"site":site,"year":str(year),"date":str(day),
            "caterpillars":"2","caterpillar.mass":mass,
            "mass.uncertain":""}


def test_season_mass_is_equal_date_measured_source_rate_not_integral():
    r=[source_row(120,"0.03"),source_row(124,"0.09"),
       source_row(128,"<0.02")]
    seasons,qa=season_means(r)
    s=seasons[("ABC",2019)]
    assert s["n_observed_mass_dates"]==3
    assert s["season_mass_mean_lower_g_per_beat"]==pytest.approx((.03+.09+0)/3)
    assert s["season_mass_mean_upper_g_per_beat"]==pytest.approx((.03+.09+.02)/3)
    assert qa["mass_source_season_not_time_integrated"] is True


def mock_siteyears():
    a=[]
    for year in (2018,2019,2020,2021):
        for i in range(24):
            theta=(year-2018)*.3+(i%7)*.25
            a.append({
                "site":f"T{i:03d}","year":year,"n_nests":4,
                "y_fledged_fraction":.5+.05*theta,
                "latitude":55+i*.09,"elevation":120+i*4,
                "hatch_doy":125+theta,"clutch_size":8.0+(i%3)*.2,
                "spring_temperature":7+.15*theta,
                "log_season_peak":math.log1p(3+i%5),
                "signed_peak_minus_hatch_days":2-theta,
                "log_hatch_window":math.log1p(2+theta),
                "log_mass_window_lower":math.log1p(.04+.01*theta),
                "log_mass_window_upper":math.log1p(.06+.01*theta),
                "log_season_mass_lower":math.log1p(.03+.005*theta),
                "log_season_mass_upper":math.log1p(.05+.005*theta),
            })
    return a


def test_entire_year_and_site_are_heldout():
    x=mock_siteyears()
    yearly=grouped_prediction(x,"year")
    sites=grouped_prediction(x,"site")
    assert yearly["n_folds"]==4
    assert sites["n_folds"]==24
    assert len(yearly["model_results"])==len(MODELS)==8
    assert all(v["n_siteyears"]==24
               for v in yearly["model_results"]["S0_count_plus_season_mass_lower"]["heldout_folds"].values())
    assert all(v["n_siteyears"]==4
               for v in sites["model_results"]["HS1_count_plus_hatch_and_season_upper"]["heldout_folds"].values())


def test_strict_frozen_sample_membership_no_fit_if_mismatched():
    out=run(mock_siteyears(),{"siteyear_nest_set_matches_frozen_measurement_era":False})
    assert out["admitted"] is False
    assert out["gate"]=="NO_GO_FROZEN_SOURCE_SAMPLE_MISMATCH"
    assert "primary" not in out


def test_missing_derived_season_mass_cannot_silently_pass():
    x=mock_siteyears()
    del x[0]["log_season_mass_lower"]
    with pytest.raises(KeyError,match="log_season_mass_lower"):
        grouped_prediction(x,"year")
