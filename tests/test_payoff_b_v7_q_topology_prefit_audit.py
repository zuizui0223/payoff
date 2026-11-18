"""Published environmental q topology only: no bird outcome or geometry U."""
from copy import deepcopy

import pytest

from scripts.payoff_b_v7_q_topology_prefit_audit import audit
from scripts.payoff_b_v7_suppinfo_aggregate_gate import QP, REGIONS, readrows


def test_source_only_counts_and_no_primary_outcome():
    x = audit()
    assert x["original_source_30year_q_n"] == 23
    assert x["all_adjacent_published_q"]["n_independent_candidate_transitions"] == 13
    assert x["without_two_unresolved_source_label_aliases"]["n_independent_candidate_transitions"] == 11
    assert x["all_adjacent_published_q"]["n_flyways"] == 3
    assert x["all_adjacent_published_q"]["n_negative_signed_q"] == 2
    assert x["V7_REGISTERED_PRIMARY_GATE"] == "HOLD_NOT_ESTIMABLE"
    assert x["q_by_U_and_bird_response_fitted"] is False
    assert x["source_region_year_specific_S_jy_available"] is False


def test_q_ordinal_position_not_geometry_urgency():
    x = audit()
    allq = x["all_adjacent_published_q"]
    clean = x["without_two_unresolved_source_label_aliases"]
    assert allq["pooled_pearson_q_vs_ordinal_stage"] == pytest.approx(-0.056224901, abs=1e-8)
    assert allq["flyway_centered_pearson_q_vs_ordinal_stage"] == pytest.approx(-0.069172162, abs=1e-8)
    assert clean["pooled_pearson_q_vs_ordinal_stage"] == pytest.approx(0.050274904, abs=1e-8)
    assert clean["flyway_centered_pearson_q_vs_ordinal_stage"] == pytest.approx(0.061396210, abs=1e-8)
    assert x["q_stage_screen_only_not_geographic_urgency"] is True
    assert allq["ordinal_stage_is_registered_geometry_urgency_U"] is False


def test_source_published_barrier_difference_descriptive_only():
    x = audit()
    allq = x["all_adjacent_published_q"]
    clean = x["without_two_unresolved_source_label_aliases"]
    assert allq["published_barrier_n"] == 5
    assert allq["published_nonbarrier_n"] == 8
    assert allq["published_barrier_mean_q"] == pytest.approx(0.178, abs=1e-8)
    assert allq["published_nonbarrier_mean_q"] == pytest.approx(0.775, abs=1e-8)
    assert clean["published_nonbarrier_n"] == 6
    assert clean["published_nonbarrier_mean_q"] == pytest.approx(.796666667, abs=1e-8)
    assert clean["significance_test_or_biological_effect_fitted"] is False


def test_original_q_source_integrity_cannot_be_bypassed():
    q = readrows(QP)
    region = readrows(REGIONS)
    changed = deepcopy(q)
    changed[0]["q_30year_correlation"] = "1.5"
    with pytest.raises(ValueError, match="correlation"):
        audit(changed, region)


def test_uncertain_labels_not_promoted_to_geometry():
    x = audit()
    assert x["original_GPS_region_geometry_available"] is False
    assert x["source_region_year_specific_S_jy_available"] is False
    assert x["q_by_U_and_bird_response_fitted"] is False
    assert x["without_two_unresolved_source_label_aliases"]["by_flyway"]["Barents Sea"]["n_transitions"] == 4


def test_source_only_ordinal_interaction_structural_df_not_bird_effect():
    x = audit()
    all_design = x["all_adjacent_published_q"]["source_only_q_by_ordinal_stage_design"]
    clean_design = x["without_two_unresolved_source_label_aliases"]["source_only_q_by_ordinal_stage_design"]
    assert all_design["n_source_transition_rows"] == 13
    assert clean_design["n_source_transition_rows"] == 11
    assert all_design["n_columns_including_ordinal_interaction"] == 7
    assert clean_design["n_columns_including_ordinal_interaction"] == 7
    assert all_design["remaining_transition_level_df_if_independent"] == 6
    assert clean_design["remaining_transition_level_df_if_independent"] == 4
    assert all_design["coding_dependent_auxiliary_vif"] == pytest.approx(5.289422133, abs=1e-8)
    assert clean_design["coding_dependent_auxiliary_vif"] == pytest.approx(5.590631251, abs=1e-8)
    assert clean_design["ordinal_product_residual_variance_fraction"] == pytest.approx(.178870678, abs=1e-8)
    assert clean_design["registered_geographical_U_test_completed"] is False
    assert clean_design["p_value_or_bird_response_fitted"] is False
