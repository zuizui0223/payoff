"""Synthetic only: not empirical support for provisioning conversion."""
import pytest
np=pytest.importorskip("numpy")
pytest.importorskip("openpyxl")
from scripts.payoff_b_little_owl_mass_per_visit_cv import (
    BAD_BROODS, MODELS, prepare, predict, crossvalidate, report
)

def synthetic_data():
    h=[]
    p=[]
    for idx in range(20):
        nest=f"N{idx:02}"
        brood=f"{nest}2019"
        place=["Germany","Czechia","Netherlands","Slovakia"][idx%4]
        h.append({"nestID":nest,"Grassland area":"20000","Garden area":"20000",
                  "Hedges area":"15000","Orchard area":"5000"})
        for d in range(8):
            visit=2.0+d%5
            q=2.5+.025*idx+.05*d
            p.append({"broodID":brood,"nestID":nest,"day":str(45000+d),
                "Year":"2019","age":str(6+d),"country":place,
                "prov_rate2":str(visit),"BM2":str(q*visit),
                "prop.day.monitored":"1","number_juv.x":"4",
                "temp":str(8+idx*.15),"wind":str(1+d*.2),
                "mammal":"0","bird":"0","insect":"2",
                "earthworms":"1","other":"0"})
    for i,brood in enumerate(sorted(BAD_BROODS)):
        nest=f"BAD{i}"
        h.append({"nestID":nest,"Grassland area":"20000","Garden area":"20000",
                  "Hedges area":"15000","Orchard area":"5000"})
        for j in range(3):
            p.append({"broodID":brood,"nestID":nest,"day":str(41000+j%2),
                "Year":"2012","age":str(4+j),"country":"Germany",
                "prov_rate2":"2","BM2":"6","prop.day.monitored":"1",
                "number_juv.x":"2","temp":"7","wind":"2",
                "mammal":"0","bird":"0","insect":"1",
                "earthworms":"1","other":"0"})
    return {"Littleowl.dat.JAB.csv":p,"all_hab_vars.csv":h}


def test_three_conflicting_broods_are_dropped_whole():
    rows,qc,admitted=prepare(synthetic_data())
    assert all(z["broodID"] not in BAD_BROODS for z in rows)
    assert qc["excluded_counts"]["all_rows_in_three_conflicting_broods"]==9
    assert qc["unique_units"]["nestID"]==20
    assert len(rows)==160
    assert admitted is False


def test_g_per_visit_and_grouped_predictor_cv():
    rows,_,_=prepare(synthetic_data())
    assert rows[0]["mass_per_visit_g"]==pytest.approx(2.5)
    x=crossvalidate(rows,"nestID")
    assert x["status"]=="GROUPED_CV_COMPLETE"
    assert x["n_source_folds"]==20
    assert set(x["equal_group_mse_g2"])==set(MODELS)
    assert x["n_admitted_days"]==160


def test_report_fails_closed_below_source_grain():
    rows,qa,flag=prepare(synthetic_data())
    r=report(rows,qa,flag)
    assert r["gate"]=="NO_GO_SOURCE_BROODDAY_SUPPORT"
    assert "cv" not in r


def test_an_unlisted_brood_duplicate_raises_source_drift():
    d=synthetic_data()
    x=dict(d["Littleowl.dat.JAB.csv"][0])
    d["Littleowl.dat.JAB.csv"].append(x)
    with pytest.raises(ValueError,match="inconsistent brood set drift"):
        prepare(d)
