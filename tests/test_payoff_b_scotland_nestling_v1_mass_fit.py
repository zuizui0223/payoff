"""Synthetic-only nestling first-visit body-mass CV tests; no source effect."""
import pytest
np=pytest.importorskip("numpy")
pytest.importorskip("openpyxl")
from scripts.payoff_b_scotland_nestling_v1_mass_fit import (
    MODELS, run, validate
)


def synthetic(rows_per_year=23, years=(2018,2019,2020,2021)):
    out=[]
    for year in years:
        for i in range(rows_per_year):
            t=(i+1)/20+(year-2018)*0.12
            out.append({
                "year":year,"site":f"T{i:03d}","n_nests":4,"n_chicks":20,
                "y_mean_v1mass_g":9.0+0.1*t,
                "latitude":55+i*.06,"elevation":150+i*3,
                "hatch_doy":126+t,"clutch_size":7.5,
                "v1_first_visit_age_proxy":6.0+(i%2)*.2,
                "spring_temperature":9.5+t,
                "log_season_peak":np.log1p(2+t),
                "signed_peak_minus_hatch_days":4-t,
                "log_count_window5":np.log1p(t),
                "log_mass_lower_window5":np.log1p(t/10),
                "log_mass_upper_window5":np.log1p((t+.02)/10),
            })
    return out


def test_fold_grouping_and_six_models():
    rows=synthetic()
    y=validate(rows,"year")
    s=validate(rows,"site")
    assert y["n_folds"]==4
    assert s["n_folds"]==23
    assert set(y["models"])==set(MODELS)
    assert all(z["n_siteyears"]==23
               for z in y["models"]["D0_count_plus_mass_lower5"]["heldout_folds"].values())
    assert all(z["n_siteyears"]==4
               for z in s["models"]["D0_count_plus_mass_lower5"]["heldout_folds"].values())


def test_no_fit_when_source_not_admitted():
    out=run(synthetic(rows_per_year=15),{"source_gate_pass":False})
    assert out["admitted_for_prediction"] is False
    assert out["gate"]=="NO_GO_EARLY_MASS_SOURCE_PANEL"
    assert "primary" not in out


def test_predictive_null_or_positive_report_is_not_causal():
    out=run(synthetic(),{"source_gate_pass":True})
    assert out["admitted_for_prediction"] is True
    assert out["not_caused_by_food_or_direct_feeding"] is True
    assert out["does_not_test_information_or_recourse"] is True
    assert out["primary"]["results"]["year"]["n_folds"]==4
