"""Only the authors' printed 2015 source aggregates: no 2026 V7 biological fit."""
from copy import deepcopy

import pytest

from scripts.payoff_b_v7_fig3_published_aggregate_screen import (
    PRINTED_RMSD, _fig3_rows, run, readrows,
)


def test_original_published_figure_and_adjacent_q_join_exact():
    rows = _fig3_rows()
    assert len(rows) == 13
    assert sum(row["alias_clean"] for row in rows) == 11
    assert {(r["flyway"],r["target_code"]) for r in rows} == {
        ("Greenland","SIC"),("Greenland","NIC"),
        ("Greenland","SGR"),("Greenland","NGR"),
        ("Svalbard","SNO"),("Svalbard","NNO"),("Svalbard","SVA"),
        ("Barents Sea","SWE"),("Barents Sea","BALT"),
        ("Barents Sea","WS"),("Barents Sea","KAN"),
        ("Barents Sea","PEKO"),("Barents Sea","NSE"),
    }
    selected = next(row for row in rows if row["target_code"] == "WS")
    assert selected["q"] == pytest.approx(0.39)
    assert selected["rmsd_days_published_site_aggregate"] == pytest.approx(5.87)
    assert selected["ordinal_stage"] == pytest.approx(.4)
    assert selected["barrier"] is True


def test_fig3_printed_value_and_panel_are_immutable_source():
    rows = readrows(PRINTED_RMSD)
    forged = deepcopy(rows)
    forged[0]["published_figure3_rmsd_days"] = "19.21"
    with pytest.raises(ValueError,match="Printed original Fig3 RMSD"):
        _fig3_rows(forged)
    forged = deepcopy(rows)
    forged[0]["figure3_panel"] = "a"
    with pytest.raises(ValueError,match="Printed original Fig3 RMSD"):
        _fig3_rows(forged)


def test_fig3_duplicate_or_missing_source_regions_cannot_be_fitted():
    rows = readrows(PRINTED_RMSD)
    with pytest.raises(ValueError,match="Expected exactly"):
        _fig3_rows(rows[:-1])
    duplicate = deepcopy(rows)
    duplicate[-1] = deepcopy(duplicate[0])
    with pytest.raises(ValueError,match="Fig3 destination"):
        _fig3_rows(duplicate)


def test_published_aggregate_is_not_v7_individual_cohort_result():
    r = run()
    assert r["V7_PRIMARY_STATUS"] == "NOT_ESTIMABLE"
    assert r["frozen_V7_focal_q_times_U_estimated"] is False
    assert r["frozen_V7_geometry_only_U_available"] is False
    assert r["new_independent_natural_replication"] is False
    assert r["p_values_or_significant_biological_claims"] is False
    assert r["all_13_adjacent"]["n_fig3_published_region_rmsds"] == 13
    assert r["only_11_without_unresolved_source_alias"]["n_fig3_published_region_rmsds"] == 11


def test_13_source_aggregate_diagnostics_independently_crosschecked():
    r = run()["all_13_adjacent"]
    assert r["raw_Pearson_q_vs_published_RMSD"] == pytest.approx(
        -0.140177410, abs=1e-8)
    assert r["raw_Spearman_q_vs_published_RMSD"] == pytest.approx(
        0.074277924, abs=1e-8)
    o = r["descriptive_ols"]
    assert o["nominal_full_model_residual_df_if_independent"] == 6
    assert o["additive_SSE"] == pytest.approx(387.076580255,abs=1e-6)
    assert o["with_ordinal_product_SSE"] == pytest.approx(287.079292369,abs=1e-6)
    assert o["relative_in_sample_SSE_decrease"] == pytest.approx(
        0.258339804,abs=1e-8)
    assert o["product_model_ordinal_q_by_stage_beta"] == pytest.approx(
        -23.807258521,abs=1e-7)
    assert o["loocv_product_beta_positive_count"] == 0
    assert o["loocv_product_beta_negative_count"] == 13
    lofo = r["exploratory_cross_flyway_ridge"]
    assert lofo["ridge_alpha_not_tuned"] == 1.
    assert lofo["additive_heldout_MSE_days_squared"] == pytest.approx(
        138.451829895,abs=1e-5)
    assert lofo["product_heldout_MSE_days_squared"] == pytest.approx(
        183.293902423,abs=1e-5)


def test_11_unresolved_alias_exclusion_keeps_negative_or_uncertain_results():
    r = run()["only_11_without_unresolved_source_alias"]
    assert r["raw_Pearson_q_vs_published_RMSD"] == pytest.approx(
        -0.265036659,abs=1e-8)
    assert r["raw_Spearman_q_vs_published_RMSD"] == pytest.approx(
        -0.090909091,abs=1e-8)
    o = r["descriptive_ols"]
    assert o["nominal_full_model_residual_df_if_independent"] == 4
    assert o["additive_SSE"] == pytest.approx(246.947367481,abs=1e-5)
    assert o["with_ordinal_product_SSE"] == pytest.approx(205.270223319,abs=1e-5)
    assert o["relative_in_sample_SSE_decrease"] == pytest.approx(
        0.168769340,abs=1e-8)
    assert o["product_model_ordinal_q_by_stage_beta"] == pytest.approx(
        -17.143899159,abs=1e-7)
    assert o["loocv_product_beta_positive_count"] == 1
    lofo = r["exploratory_cross_flyway_ridge"]
    assert lofo["additive_heldout_MSE_days_squared"] == pytest.approx(
        119.590605810,abs=1e-5)
    assert lofo["product_heldout_MSE_days_squared"] == pytest.approx(
        182.569440870,abs=1e-5)
