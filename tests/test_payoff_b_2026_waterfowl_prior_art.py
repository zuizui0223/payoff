"""New 2026 original waterfowl literature claim boundaries (no data refit)."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/payoff_b_2026_waterfowl_prior_art_20261119.json"

def test_latest_source_publication_and_track_units_pinned():
    d=json.loads(SOURCE.read_text(encoding="utf-8"))
    jae=next(x for x in d["canonical_papers"] if x["source_id"]=="Liu2026_JAE_stopovers")
    mov=next(x for x in d["canonical_papers"] if x["source_id"]=="Liu2026_MovementEcology_individual_variance")
    assert jae["first_published"]=="2026-11-05"
    assert jae["n_spring_migration_paths"]==220
    assert jae["n_species"]==5
    assert jae["source_tracking_year_range"]==[2015,2023]
    assert mov["first_published"]=="2026-07-27"
    assert mov["n_tracks"]==323
    assert mov["n_tracked_individuals"]==172
    assert mov["n_species"]==4
    assert mov["source_tracking_year_range"]==[2015,2022]

def test_legacy_stopovers_and_variance_not_new_payoff_claims():
    d=json.loads(SOURCE.read_text(encoding="utf-8"))
    assert d["prior_art_boundaries"]["greater_number_of_stopovers_improves_phenological_sensitivity"].startswith("PUBLISHED_PRIOR_ART")
    assert d["prior_art_boundaries"]["interindividual_variation_affects_population_tracking"].startswith("PUBLISHED_PRIOR_ART")
    assert d["overlap"]["individual_track_overlap_identified"] is False
    assert d["overlap"]["treat_as_two_independent_study_replications"] is False
    assert d["scope_decision"]["no_new_ecological_effect_rerun"] is True

def test_original_information_deadline_not_backfilled_from_stopover_counts():
    d=json.loads(SOURCE.read_text(encoding="utf-8"))
    assert d["scope_decision"]["v7_goose_focal_qU_unopened"] is True
    assert d["scope_decision"]["no_raw_movebank_access_claimed"] is True
    assert d["scope_decision"]["no_eBird_occurrence_file_used"] is True
    assert d["scope_decision"]["manuscripts_unchanged"] is True
    for label in ("effective_cue_observable_before_specific_commitment",
                  "causal_downstream_recourse_budget_r_t",
                  "actual_partner_network_asynchronous_cue_uptake"):
        assert "NOT_" in d["prior_art_boundaries"][label]
