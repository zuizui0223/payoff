"""Synthetic source-unit tests only, never treated as ecological evidence."""
import pytest
pytest.importorskip("numpy")
pytest.importorskip("openpyxl")

from scripts.payoff_b_scotland_censored_mass_audit import (
    mass_raw,dated_mass,peak_date
)


def row(*, site="S1",year="2020",date="120",count="2",mass="<0.02g",flag=""):
    return {"site":site,"year":year,"date":date,"caterpillars":count,
            "caterpillar.mass":mass,"mass.uncertain":flag}


def test_censored_not_zero_and_physical_mg_conversion():
    l,u,ok,kind=mass_raw(row())
    assert ok and (l,u)==(0.0,20.0)
    l,u,ok,kind=mass_raw(row(count="2",mass="0.14"))
    assert ok and l==pytest.approx(140)
    assert l==u
    assert mass_raw(row(count="0",mass=""))[2] is True
    assert mass_raw(row(count="2",mass=""))[2] is False
    assert mass_raw(row(count="2",mass="0.14",flag="1"))[2] is False


def test_mass_source_fails_closed_when_sample_effort_unreliable():
    rows=[row(count="1",mass="0.1"),row(count="3",mass="0.3",flag="1"),
          row(count="2",mass="0.1"),row(count="3",mass="0.1"),
          row(date="124",count="2",mass="0.2"),row(date="124",count="2",mass="0.2")]
    by,reasons,day=dated_mass(rows)
    assert day["mass_source_coverage_below_90pct"]==1
    assert len(by[("S1",2020)])==1
    assert reasons["source_flagged_mass_uncertain"]==1


def test_pre2017_unmeasured_mass_is_not_structural_zero():
    rows=[row(year="2014",count="0",mass=""),
          row(year="2017",count="0",mass="",date="121"),
          row(year="2017",count="0",mass="",date="121")]
    by,reasons,day=dated_mass(rows)
    assert reasons["pre2017_unmeasured_mass"]==1
    assert len(by[("S1",2017)])==1
    assert by[("S1",2017)][0][1:4]==(0,0,0)


def test_first_observed_source_peak_on_tie():
    p=[("2020-05-05",0,0,0,2),("2020-05-09",20,20,3,2),("2020-05-13",20,20,3,2)]
    assert peak_date(p,1)=="2020-05-09"
    assert peak_date(p,3)=="2020-05-09"
