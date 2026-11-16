"""Synthetic-only tests of EIDC measured mass and full-holdout contracts.

Never treat fixture data or synthetic predictive signals as empirical findings.
"""
import pytest
np=pytest.importorskip("numpy")
pytest.importorskip("openpyxl")
from collections import Counter
from scripts.payoff_b_scotland_measured_mass_window import (
    original_mass_bounds, source_mass, result, cv, FEATURES
)


def row(c, mass, *, doy=130, site="AAA", year=2021, uncertain=""):
    return {"caterpillars":str(c), "caterpillar.mass":mass,
            "mass.uncertain":uncertain, "date":str(doy),
            "site":site, "year":str(year)}


def test_original_measurement_units_censor_and_structural_zero():
    qc=Counter()
    assert original_mass_bounds(row(2,"0.043"),qc)==pytest.approx((0.043,0.043))
    assert original_mass_bounds(row(2,"<0.02"),qc)==(0,0.02)
    assert original_mass_bounds(row(2,"<0.02g"),qc)==(0,0.02)
    assert original_mass_bounds(row(0,""),qc)==(0,0)
    assert original_mass_bounds(row(2,""),qc) is None
    assert original_mass_bounds(row(2,"0.51",uncertain="1"),qc) is None
    assert qc["censored_lt_0_02_g"]==2
    assert qc["structural_zero_from_count_zero"]==1
    assert qc["positive_count_missing_mass"]==1


def test_unknown_threshold_fails_closed():
    with pytest.raises(ValueError,match="Unknown source censor"):
        original_mass_bounds(row(2,"<0.05g"),Counter())


def test_bounded_mass_date_and_80pct_quality_gate():
    rows=[]
    for day in (125,129,133):
        rows += [row(1,"0.1",doy=day),row(1,"<0.02g",doy=day),
                 row(0,"",doy=day),row(3,"",doy=day)]
    lower,upper,qa=source_mass(rows)
    assert qa["mass_class_counts"]["positive_count_missing_mass"]==3
    assert qa["date_qa"]["date_below_80pct_mass_support"]==3
    assert lower=={} and upper=={}
    rows=[r for r in rows if r["caterpillar.mass"]!="" or r["caterpillars"]=="0"]
    low,hi,qa=source_mass(rows)
    assert len(low[("AAA",2021)])==3
    assert len(hi[("AAA",2021)])==3
    assert low[("AAA",2021)][0]["amount"]==pytest.approx(100/3)
    assert hi[("AAA",2021)][0]["amount"]==pytest.approx(120/3)


def mock_panel(years=(2018,2019,2020,2021),sites=25):
    x=[]
    for yr in years:
        for i in range(sites):
            signal=i/20+(yr-2018)*0.1
            x.append({
                "site":f"S{i:03d}","year":yr,"n_nests":3,
                "y_fledged_fraction":0.55+0.05*signal,
                "latitude":55+i/10,"elevation":i*9.0,
                "hatch_doy":130+signal,"clutch_size":7.5,
                "spring_temperature":8.0+signal,
                "log_season_peak":np.log1p(1+signal),
                "signed_peak_minus_hatch_days":3.0,
                "log_hatch_window":np.log1p(1+signal),
                "log_mass_window_lower":np.log1p(0.01+signal/10),
                "log_mass_window_upper":np.log1p(0.02+signal/10),
            })
    return x


def test_full_site_and_year_holdout_shapes():
    p=mock_panel()
    y=cv(p,"year")
    s=cv(p,"site")
    assert y["n_folds"]==4 and y["n_siteyears"]==100
    assert s["n_folds"]==25
    assert all(x["siteyears"]==25
           for x in y["models"]["D0_count_mass_lower"]["heldout_folds"].values())
    assert all(x["siteyears"]==4
           for x in s["models"]["D0_count_mass_lower"]["heldout_folds"].values())


def test_no_fit_below_frozen_minimum():
    p=mock_panel(years=(2019,2020),sites=25)
    out=result(p,{"fixture":"synthetic"})
    assert out["admitted"] is False
    assert out["gate"]=="NO_GO_INSUFFICIENT_MASS_COMMON_SUPPORT"
    assert "loyo" not in out


def test_source_models_use_same_siteyear_rows_with_no_fitness_claim():
    p=mock_panel()
    out=result(p,{"fixture":"synthetic"})
    assert out["admitted"] is True
    assert len(out["loyo"]["models"])==6
    assert out["source_mass_units"].startswith("g per standardized")
    assert out["causal_or_info_game_supported"] is False
    assert out["exploratory_after_previous_negative_result"] is True
    assert set(FEATURES)==set(out["loyo"]["models"])
