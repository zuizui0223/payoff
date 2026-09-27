import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "payoff_b_hoge_veluwe_network_hysteresis_contract_20260927.json"


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_hoge_veluwe_network_lane_is_preoutcome_and_fixed():
    c = load_contract()
    assert c["status"] == "PREOUTCOME_ASSEMBLY_REGISTERED_SOURCE_FILES_UNOPENED"
    assert c["population"]["primary_overlap_years"] == [1985, 2015]
    assert c["population"]["primary_history_years_after_connectivity_construction"] == [1992, 2015]
    assert c["population"]["expected_primary_history_year_count"] == 24
    assert c["population"]["excluded_years"] == [1991]
    assert c["sources"]["precommitment_cue"]["no_window_retuning"] is True
    assert c["coordinates"]["cue_resource_predictive_connectivity"]["window_years"] == 8
    assert c["source_gate"]["require_at_least_24_history_years_after_connectivity_construction"] is True
    assert c["source_gate"]["require_expected_primary_history_span"] == [1992, 2015]
    assert c["information_reversal_gate"]["fail_state"] == "NO_CUE_RESOURCE_REVERSAL"
    assert c["information_reversal_gate"]["aicc_parameter_count"]["linear"] == 2
    assert c["information_reversal_gate"]["aicc_parameter_count"]["segmented"] == 5
    assert c["history_test_if_reversal_passes"]["covariance"] == "Newey-West HAC covariance, maxlags=2, finite-sample correction"
    assert c["history_test_if_reversal_passes"]["no_naive_iid_inference"] is True


def test_history_test_cannot_open_before_information_reversal():
    c = load_contract()
    gate = c["information_reversal_gate"]
    assert "focal and partner timing are not opened" in gate["rule"]
    assert gate["data_used"] == "cue-resource predictive-connectivity series only"
    assert c["history_test_if_reversal_passes"]["minimum_branch_years"] == 6


def test_contract_preserves_prior_negative_lane_and_claim_ceiling():
    c = load_contract()
    prior = c["relationship_to_prior_negative_lane"]
    assert prior["prior_result"] == "NO_CUE_DRIVER_REVERSAL"
    assert "anti_retuning_rule" in prior
    forbidden = " ".join(c["forbidden_moves"])
    assert "2000/2001" in forbidden
    assert "circa-2008" in forbidden
    ceiling = c["history_test_if_reversal_passes"]["interpretation_ceiling"]
    assert "does not identify the exact Nash mechanism" in ceiling
    assert "does not identify a natural rescue seed" in ceiling


def test_declared_public_sources_are_specific():
    c = load_contract()
    sources = c["sources"]
    assert sources["migrant_timing"]["paper_doi"] == "10.1111/gcb.14006"
    assert sources["resident_partner_timing"]["dataset_doi"] == "10.5061/dryad.f1vhhmgx6"
    assert sources["destination_resource_state"]["dataset_doi"] == "10.5061/dryad.f1vhhmgx6"
    assert sources["resident_partner_timing"]["file"].endswith(".xlsx")
    assert sources["destination_resource_state"]["file"].endswith(".xlsx")

def test_window_rule_yields_exact_registered_24_year_history_span():
    c = load_contract()
    source_start, source_end = c["population"]["primary_overlap_years"]
    excluded = set(c["population"]["excluded_years"])
    window = c["coordinates"]["cue_resource_predictive_connectivity"]["window_years"]
    min_pairs = c["coordinates"]["cue_resource_predictive_connectivity"]["min_pairs"]

    eligible = []
    for year in range(source_start, source_end + 1):
        prior = range(year - window, year)
        valid_pairs = sum(
            source_start <= prior_year <= source_end
            and prior_year not in excluded
            for prior_year in prior
        )
        if year not in excluded and valid_pairs >= min_pairs:
            eligible.append(year)

    assert eligible == list(range(1992, 2016))
    assert len(eligible) == 24

