"""Original 53-season pilot tests with synthetic time data only."""
import math
from scripts.run_payoff_b_stork_stage_handoff_pilot import (
    normalize_365, slope_group_fe, run_pilot, shuffle_year_x,
    cluster_bootstrap, admitted_rows,
)

def test_day_of_year_leap_convention():
    assert normalize_365(61,2016)==60
    assert normalize_365(61,2015)==61
    assert normalize_365(59,2016)==59

def test_year_fixed_effect_slope_is_one_for_no_compensation():
    rows=[]
    for year in (2013,2014,2015,2016):
        for i in range(5):
            rows.append({"year":year,"animal":str(i),"x":float(60+i+year),
                         "y":float(82+i+year)})
    assert abs(slope_group_fe(rows)-1)<1e-12

def test_year_fe_recovers_partial_retention_without_year_confounding():
    rows=[]
    for year in (2013,2014,2015,2016):
        for i in range(5):
            rows.append({"year":year,"animal":str(i),"x":float(60+i+year),
                         "y":float(100+2*year+.35*i)})
    assert abs(slope_group_fe(rows)-.35)<1e-12

def test_cluster_sampling_preserves_individual_years_and_fixed_seed():
    rows=[{"year":2014+i%3,"animal":str(i//3),
           "x":float(70+i%3+i//3),"y":float(90+i//3)}
          for i in range(30)]
    a,err1=cluster_bootstrap(rows,replicates=30)
    b,err2=cluster_bootstrap(rows,replicates=30)
    assert a==b and err1==err2
    assert len(a)>25

def test_year_shuffle_returns_prescribed_replicates():
    rows=[{"year":2016,"animal":str(i),
           "x":float(60+i),"y":float(80+i)} for i in range(8)]
    assert len(shuffle_year_x(rows,replicates=25))==25

def test_no_frozen_n_gate_loosening_to_fit_a_model():
    rows=[{"year":2014,"animal":"synthetic","x":69.0,"y":95.0}]
    o=run_pilot(rows)
    assert o["status"]=="NOT_ESTIMABLE_ORIGINAL_SAMPLE_IDENTITY_CHANGED"
    assert "synthetic" not in str(o)

def test_only_frozen_original_progression_class_admitted():
    mapping={
        ("ID",2015):{"status":"NORTHWARD_PROGRESS_OBSERVED",
                     "first_20_percent_doy":61,
                     "first_80_percent_doy":81},
        ("other",2015):{"status":"WINTER_DAYS_INSUFFICIENT"},
    }
    rows=admitted_rows(mapping)
    assert len(rows)==1 and rows[0]["x"]==61
