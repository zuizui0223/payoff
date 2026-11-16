"""Synthetic-only post-open source-year sensitivity contract tests."""
import pytest
pytest.importorskip("numpy")
pytest.importorskip("openpyxl")
from scripts.payoff_b_scotland_mass_source_year_sensitivity import (
    evaluate, mass_reporting_by_year
)


def test_no_source_mass_measurement_not_a_positive_mass_observation():
    rows=[
        {"year":"2014","caterpillars":"2","caterpillar.mass":"",
         "mass.uncertain":""},
        {"year":"2018","caterpillars":"2","caterpillar.mass":"0.04",
         "mass.uncertain":""},
        {"year":"2018","caterpillars":"1","caterpillar.mass":"<0.02",
         "mass.uncertain":""}
    ]
    info=mass_reporting_by_year(rows)
    assert info["2014"]["positive_count_missing_mass"]==1
    assert info["2018"]["mass_bound_accepted_branch_rows"]==2
    assert info["2018"]["censored_lt_0_02_g"]==1


def test_unsupported_subpanel_cannot_fit():
    a=[{
      "year":2019,
      "site":"AA",
      "n_nests":4
    }]
    r=evaluate(a)
    assert r["admission"]=="NO_GO_SAMPLE_SUPPORT"
    assert r["fitted"] is False
