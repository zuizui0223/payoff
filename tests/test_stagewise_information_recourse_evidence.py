import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data" / "payoff_b_stagewise_information_recourse_evidence_20261001.json"


def load():
    return json.loads(RECEIPT.read_text(encoding="utf-8"))


def test_receipt_is_prospective_and_does_not_retune_frozen_submission():
    payload = load()
    assert payload["status"] == "PROSPECTIVE_SOURCE_BACKED_BRIDGE_NOT_DIRECT_D_EFF_TEST"
    assert payload["frozen_submission_affected"] is False


def test_mule_deer_bridge_supports_both_signed_recourse_directions():
    payload = load()
    mule = next(
        row for row in payload["sources"]
        if row["system"] == "Red Desert long-distance migratory mule deer"
    )
    evidence = mule["evidence"]
    assert evidence["ahead_compensated_percent"] == 93
    assert evidence["ahead_mechanism"] == "decelerating movement"
    assert evidence["behind_compensated_percent"] == 90
    assert evidence["behind_mechanism"] == "accelerating movement"
    assert evidence["late_vs_early_speed_ratio"] == 2.5
    assert evidence["late_vs_early_stopover_reduction_percent"] == 72
    assert evidence["early_movement_rate_km_per_day"] == 2.9
    assert evidence["late_movement_rate_km_per_day"] == 7.1
    assert evidence["early_stopover_days"] == 36
    assert evidence["late_stopover_days"] == 10
    assert evidence["early_migration_duration_days"] == 72
    assert evidence["late_migration_duration_days"] == 31
    assert evidence["average_completion_window_days"] == 6
    assert "published summaries identify natural D_eff" in mule["prohibited_claims"]


def test_godwit_bridge_is_stagewise_but_not_an_information_intent_claim():
    payload = load()
    godwit = next(
        row for row in payload["sources"]
        if row["system"].startswith("bar-tailed godwit")
    )
    assert godwit["evidence"]["population_departure_advance_days_2008_2020"] == 6
    assert godwit["evidence"]["complete_tracks"] == 50
    assert godwit["evidence"]["individuals"] == 36
    assert godwit["evidence"]["yellow_sea_stopover_duration_trend_days_per_year"] == 0.693
    assert godwit["evidence"]["alaska_departure_arrival_trends_supported"] is False
    assert any(
        "intentionally depart early" in claim
        for claim in godwit["prohibited_claims"]
    )


def test_goose_bridge_supports_en_route_information_update_only():
    payload = load()
    goose = next(
        row for row in payload["sources"]
        if row["system"] == "pink-footed goose multi-site spring migration"
    )
    assert goose["evidence"]["cue_relevance_changes_en_route"] is True
    assert goose["evidence"]["stopover_accumulated_temperature_used"] is True
    assert goose["evidence"]["northward_progression_adjusted"] is True
    assert any(
        "common cue accuracy q" in claim
        for claim in goose["prohibited_claims"]
    )


def test_plant_butterfly_bridge_does_not_license_recourse_ranking():
    payload = load()
    local = next(
        row for row in payload["sources"]
        if row["system"].startswith("British Columbia butterfly")
    )
    evidence = local["evidence"]
    assert evidence["associations"] == 166
    assert evidence["butterfly_species_same_spring_comparison"] == 61
    assert evidence["plant_species_same_spring_comparison"] == 54
    assert evidence["plant_more_temperature_sensitive_spring_days_per_C"] == 5.70
    assert evidence["associations_with_plants_more_sensitive_percent"] == 87
    assert any(
        "lower recourse" in claim
        for claim in local["prohibited_claims"]
    )


def test_cross_system_ceiling_keeps_q_r_natural_validation_unidentified():
    payload = load()
    ceiling = payload["cross_system_ceiling"]
    assert "post-commitment timing recourse" in ceiling["supported"]
    assert "unequal phenological sensitivity" in ceiling["supported"]
    assert "natural validation of V(q,r)=r*W*(q-0.5)" in ceiling["not_supported"]
    assert "pre-commitment information is weak" in ceiling["prospective_prediction"]



def test_local_interaction_systems_are_not_assigned_zero_recourse_by_taxon():
    payload = load()
    viola = next(
        row for row in payload["sources"]
        if row["system"] == "eastern US Viola-bee phenology network"
    )
    assert viola["evidence"]["flowering_duration_used_in_mismatch_metric"] is True
    assert viola["evidence"]["longer_flowering_duration_identified_as_buffer_candidate"] is True
    ceiling = payload["cross_system_ceiling"]
    assert any(
        "uniformly low recourse" in claim
        for claim in ceiling["not_supported"]
    )



def test_receipt_records_canonical_actionability_deadline_bridge():
    payload = load()
    bridge = payload["theory_objects"]["canonical_deadline_bridge"]
    assert "V(q,r)=r*V_A(q)" in bridge
    assert "q_wait(r)=(B+D/r)/S" in bridge
    assert "D/r" in bridge
    assert any(
        "physical percentage of route" in claim
        for claim in payload["cross_system_ceiling"]["not_supported"]
    )
