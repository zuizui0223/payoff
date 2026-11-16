"""Synthetic test fixture only; not a source-derived ecological effect."""
import pytest
np=pytest.importorskip("numpy")
pytest.importorskip("openpyxl")
from scripts.payoff_b_scotland_hatch_window_fitness_loyo import (
    audit,cross_validate,source_temperature
)


def mock_siteyears():
    rows=[]
    for yr in (2014,2018,2019,2020,2021):
        for i in range(20):
            x=(i+1)%5
            rows.append({
                "year":yr,"site":f"S{i:03d}","n_nests":3,
                "y_fledged_fraction":min(.99,max(.01,.38+.08*x-.005*(yr-2014))),
                "latitude":54+0.15*i,"elevation":i*12,
                "hatch_doy":133+x+.3*(yr-2014),"clutch_size":8+x,
                "spring_temperature":8+0.04*i+.1*(yr-2014),
                "log_season_peak":np.log1p(x+2),
                "signed_peak_minus_hatch_days":x-2,
                "log_hatch_window":np.log1p(x+.1*(yr-2014)),
            })
    return rows


def test_grouped_site_year_prediction_does_not_reuse_heldout_unit():
    rows=mock_siteyears()
    lo_year=cross_validate(rows,"year")
    lo_site=cross_validate(rows,"site")
    assert lo_year["n_folds"]==5 and lo_year["n_source_siteyears"]==100
    assert lo_site["n_folds"]==20
    assert all(p["test_siteyears"]==20 for p in
       lo_year["model_results"]["M3_plus_window_supply"]["heldout_folds"].values())
    assert all(p["test_siteyears"]==5 for p in
       lo_site["model_results"]["M3_plus_window_supply"]["heldout_folds"].values())


def test_no_claim_if_climate_panel_small():
    a=mock_siteyears()[:30]
    o=audit(a,{"synthetic":True})
    assert o["admitted_for_fitness_prediction"] is False
    assert o["gate"]=="NO_GO_INSUFFICIENT_CLIMATE_COMPLETE_SITEYEAR_PANEL"
    assert "loyo" not in o


def test_predefined_march_april_historical_temperature_window():
    # 5 days of hourly headers, plus >=100 total date columns; incomplete
    headers=[f"X{60+i/24:.12f}" for i in range(144)]
    rows=[{"site":"S001","year":"2019",**{key:"8.5" for key in headers}}]
    a,qc=source_temperature(rows)
    assert a[("S001",2019)]["spring_temperature"]==pytest.approx(8.5)
    assert qc["n_siteyears_with_valid_loggers"]==1


def test_different_temperature_logger_duplicate_rows_are_not_extra_siteyears():
    headers=[f"X{60+i/24:.12f}" for i in range(144)]
    r={"site":"S001","year":"2019",**{key:"8" for key in headers}}
    t={"site":"S001","year":"2019",**{key:"10" for key in headers}}
    a,qc=source_temperature([r,t])
    assert len(a)==1
    assert a[("S001",2019)]["spring_temperature"]==pytest.approx(9.0)
    assert a[("S001",2019)]["n_valid_loggers"]==2
