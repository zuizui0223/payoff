"""Synthetic animal-cluster and leave-one-year-out test fixtures."""
from datetime import date
from scripts.audit_payoff_b_fullrisk_cluster_robustness import (
    weighted_gridmonth_contrast,uncertainty,VARS
)

def row(animal,year,day,label,anomaly):
    source=date(year,3,day)
    weather={name:anomaly for name in VARS}
    return (animal,source,(35,13),label,weather)

def synthetic_groups():
    rows=[]
    for year in (2017,2018,2019):
        for index in range(12):
            animal="animal"+str(index)
            rows.append(row(animal,year,5,"NORTHWARD_CANDIDATE",2.0))
            rows.append(row(animal,year,7,"STAYED_TWO_DAYS",1.0))
    return rows

def test_source_cluster_estimator_respects_gridmonth_weights():
    r=weighted_gridmonth_contrast(synthetic_groups())
    assert r["n_gridmonth_strata_with_both_labels"]==3
    assert r["source_case_weighted_contrasts"]["V10M_anomaly"]==1.0

def test_animal_cluster_bootstrap_and_year_loo_not_identity_output():
    o=uncertainty(synthetic_groups(),bootstrap=50,seed=100)
    assert o["bootstrap_valid"]==0 or o["status"].startswith("BOOTSTRAP")
    assert o["animal_cluster_units"]==12
    assert "animal1" not in str(o)
    assert len(o["leave_one_source_year_out_descriptive"])==3
    assert o["original_effect"]["source_case_weighted_contrasts"]["T2M_anomaly"]==1.
