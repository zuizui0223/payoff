"""Only synthetic arrays used in the posthoc influence-check tests."""
from scripts.payoff_b_2023_biomass_influence_audit import check
from scripts.payoff_b_2023_biomass_selection_gate import prepare
from tests.test_payoff_b_2023_biomass_selection_gate import fake_data


def test_leave_one_year_deletes_one_real_year_not_one_brood():
    panel, _ = prepare(fake_data(years=14, n_broods=12))
    out = check(panel)["results"]["Hoge Veluwe|Great Tit"]
    assert out["years"] == 14
    assert out["n_drop_one_year_checks"] == 14
    assert len({r["dropped_year"] for r in
                out["top_three_influential_years"]}) == 3
    assert out["fraction_drop_one_year_positive_increment"] is not None


def test_extreme_mismatch_is_flagged_not_deleted():
    data = fake_data(years=14, n_broods=12)
    data["resource"][0]["MidDate"] = 100
    panel, _ = prepare(data)
    out = check(panel)["results"]["Hoge Veluwe|Great Tit"]
    assert out["years"] == 14
    assert len(out["unexcluded_extreme_abs_mismatch_gt_30_days"]) >= 1
    assert out["n_drop_one_year_checks"] == 14
