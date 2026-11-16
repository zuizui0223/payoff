"""Synthetic-only nestling first-visit gate tests, never empirical outcomes."""
import pytest
pytest.importorskip("numpy")
pytest.importorskip("openpyxl")
from scripts.payoff_b_scotland_nestling_v1_mass_admission import (
    admit_source_nests, link_nestlings
)


def bird(year,box,treatment="",species="bluti",hatch=138,clutch=8):
    return {"year":str(year),"site":"AAA","box":str(box),
            "clutch_swap_treatment":treatment,
            "species":species,"hatching_first_recorded":str(hatch),
            "cs":str(clutch),"suc":"-999"}


def chick(year,box,ring,v1date=144,mass=9.4):
    return {"year":str(year),"site":"AAA","box":str(box),
            "ring":ring,"v1date":str(v1date),
            "v1mass":str(mass)}


def test_verified_source_bird_and_treatment_without_fledge_selection():
    data=[bird(2019,1,""),bird(2019,2,"unmanipulated"),
          bird(2018,3,"odd"),bird(2014,4,""),
          bird(2021,5,""),bird(2020,6,"",species="coati")]
    x,qa=admit_source_nests(data)
    assert sorted(k[2] for k in x)==["2","5"]
    assert qa["no_fledged_outcome_conditioning"] is True


def test_source_v1mass_age_window_chicks_grouped_by_nest():
    x,_=admit_source_nests([bird(2021,1)])
    rows=[chick(2021,1,"B1"),chick(2021,1,"B2",v1date=145,mass=11),
          chick(2021,1,"B3",v1date=149),chick(2021,1,"B4",mass=0)]
    out,qa=link_nestlings(x,rows)
    k=("AAA",2021,"1")
    assert out[k]["n_chicks"]==2
    assert out[k]["mean_v1mass_g"]==pytest.approx(10.2)
    assert qa["excluded"]["v1_visit_outside_prespecified_day5_9"]==1
    assert qa["excluded"]["missing_or_nonpositive_v1_mass_date"]==1


def test_repeat_original_individual_id_fails_closed():
    x,_=admit_source_nests([bird(2021,1)])
    with pytest.raises(ValueError,match="Duplicate source nestling"):
        link_nestlings(x,[chick(2021,1,"A"),chick(2021,1,"A")])
