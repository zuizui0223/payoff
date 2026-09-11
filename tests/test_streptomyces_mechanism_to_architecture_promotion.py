import json
from pathlib import Path

from src.mechanism_to_architecture_promotion import (
    MechanismToArchitecturePromotionReceipt,
    adjudicate_mechanism_to_architecture_promotion,
)


PATH = Path("validation/streptomyces_mechanism_to_architecture_promotion_v1.json")


def load_data():
    return json.loads(PATH.read_text())


def make_receipt(data):
    return MechanismToArchitecturePromotionReceipt(
        system_id=data["system_id"],
        mechanism_id=data["mechanism_id"],
        candidate_shared_id=data["candidate_shared_id"],
        candidate_differentiated_id=data["candidate_differentiated_id"],
        support_reference=data["support_reference"],
        **data["inputs"],
    )


def test_current_streptomyces_promotion_receipt_recomputes_expected_false_status():
    data = load_data()
    result = adjudicate_mechanism_to_architecture_promotion(make_receipt(data))
    expected = data["expected"]
    assert result.mechanism_support_certified == expected["mechanism_support_certified"]
    assert (
        result.task_matched_architecture_counterfactual_certified
        == expected["task_matched_architecture_counterfactual_certified"]
    )
    assert result.matched_s_promotion_licensed == expected["matched_s_promotion_licensed"]
    assert result.generic_game_promoted == expected["generic_game_promoted"]
    assert result.eta_identified == expected["eta_identified"]
    assert result.e1_promoted == expected["e1_promoted"]
    assert set(result.blockers) == set(data["current_blockers"])


def test_current_receipt_explicitly_keeps_prospective_and_architecture_status_separate():
    data = load_data()
    assert data["two_probe_triangulation_prospective"]
    assert not data["matched_generalist_shared_architecture_recovered"]
    assert not data["architecture_mapping_certified"]
    assert not data["architecture_frequency_feedback_identified"]


def test_hypothetical_positive_triangulation_alone_still_cannot_promote_matched_s():
    data = load_data()
    inputs = dict(data["inputs"])
    inputs["triangulated_generation_reduction_declared"] = True
    result = adjudicate_mechanism_to_architecture_promotion(
        MechanismToArchitecturePromotionReceipt(
            system_id=data["system_id"],
            mechanism_id=data["mechanism_id"],
            candidate_shared_id=data["candidate_shared_id"],
            candidate_differentiated_id=data["candidate_differentiated_id"],
            support_reference="HYPOTHETICAL_FUTURE_POSITIVE_TRIANGULATION_ONLY",
            **inputs,
        )
    )
    assert result.mechanism_support_certified
    assert not result.task_matched_architecture_counterfactual_certified
    assert not result.matched_s_promotion_licensed
    assert "NET_TASK_NOT_PRESERVED_OR_RESCUED" in result.blockers
    assert "MATCHED_SHARED_UNIT_NOT_RECOVERED" in result.blockers
    assert not result.generic_game_promoted
    assert not result.eta_identified
    assert not result.e1_promoted
