"""Synthetic fixture for source biomass construction; no new ecology."""
import pytest
pytest.importorskip("openpyxl")
from scripts.payoff_b_little_owl_biomass_construction_audit import (
    source_reconstruction
)
def row(m=1,b=0,i=2,e=3,o=4,f=.5,change=0):
    bm=25*m+33*b+.9*i+3.7*e+2.9*o+change
    return {"mammal":str(m),"bird":str(b),"insect":str(i),
            "earthworms":str(e),"other":str(o),
            "prov_rate":str(m+b+i+e+o),"BM":str(bm),
            "BM2":str(bm/f),"prop.day.monitored":str(f)}

def test_exact_source_weights_reproduce_bm_and_day_scaling():
    a=source_reconstruction([row(),row(m=0,e=0,o=0,f=1)])
    assert a["reconstructed_BM_match_n"]==2
    assert a["reconstructed_BM2_match_n"]==2
    assert a["category_count_matches_prov_rate_n"]==2
    assert a["n_discrepancies"]==0

def test_mass_not_a_biologically_independent_observation():
    a=source_reconstruction([row(change=.5)])
    assert a["reconstructed_BM_match_n"]==0
    assert a["n_discrepancies"]>0
    assert a["biomass_estimated_not_independently_weighed"]
