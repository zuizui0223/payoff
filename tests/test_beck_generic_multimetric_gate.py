import json
from pathlib import Path

from src.multimetric_game_scalarization import adjudicate_multimetric_sign


RECEIPT = Path("validation/beck_generic_multimetric_gate_v1.json")


def test_registered_contexts_recompute_tradeoff_non_dominance():
    data = json.loads(RECEIPT.read_text())
    for context in data["contexts"].values():
        r = adjudicate_multimetric_sign(
            context["metric_states"],
            support_reference=data["receipt_id"],
            orientation_frozen_declared=True,
        )
        assert r.pareto_relation == context["pareto_relation"]
        assert r.weight_invariant_scalar_sign == context["weight_invariant_scalar_sign"]
        assert r.scalarization_required == context["scalarization_required"]


def test_raw_r3_is_not_relabelled_as_raw_game_reproduction():
    data = json.loads(RECEIPT.read_text())
    assert data["raw_substrate"]["r_level"] == "R3"
    assert not data["raw_substrate"]["raw_numeric_game_analysis_reproduced"]


def test_no_frequency_or_architecture_claim_is_licensed():
    data = json.loads(RECEIPT.read_text())
    assert not data["frequency_support_declared"]
    assert not data["scalar_payoff_sign_identified"]
    assert not data["generic_frequency_game_identified"]
    assert not data["numerical_phi_identified"]
    assert not data["numerical_eta_identified"]
    assert not data["architecture_mapping_used"]
    assert not data["architecture_specific_claim_licensed"]


def test_comparable_biomass_per_glucose_is_not_encoded_as_exact_zero():
    data = json.loads(RECEIPT.read_text())
    weak = data["contexts"]["weak_buffer"]["metric_states"]
    assert weak["biomass_per_glucose"] == "unresolved"
