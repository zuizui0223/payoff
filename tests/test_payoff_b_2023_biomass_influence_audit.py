"""Synthetic year-level influence checks; no original outcomes opened by tests."""
import pytest
pytest.importorskip("numpy")
pytest.importorskip("openpyxl")
import numpy as np
from scripts.payoff_b_2023_biomass_influence_audit import check


def panel():
    rows = []
    for j in range(14):
        mass = 1.0 + (j % 4) * 0.3
        rows.append({
            "year": 2000 + j, "n_broods": 12,
            "differential": -0.15 + 0.01 * j + (0.02 if j % 2 else -0.02),
            "mismatch_days": -5.0 + j * 1.1,
            "log_peak_biomass": float(np.log1p(mass)),
            "peak_biomass_g_per_day_m2": mass,
        })
    return {("Hoge Veluwe", "Great Tit"): rows}


def test_leave_one_year_deletes_one_year_not_one_brood():
    out = check(panel())["results"]["Hoge Veluwe|Great Tit"]
    assert out["years"] == 14
    assert out["n_drop_one_year_checks"] == 14
    assert len({r["dropped_year"] for r in
                out["top_three_influential_years"]}) == 3
    assert out["fraction_drop_one_year_positive_increment"] is not None


def test_extreme_mismatch_is_flagged_not_deleted():
    data = panel()
    data[("Hoge Veluwe", "Great Tit")][0]["mismatch_days"] = -45
    out = check(data)["results"]["Hoge Veluwe|Great Tit"]
    assert out["years"] == 14
    assert len(out["unexcluded_extreme_abs_mismatch_gt_30_days"]) == 1
    assert out["n_drop_one_year_checks"] == 14
