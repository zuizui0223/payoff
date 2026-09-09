import json
from pathlib import Path

from src.matched_architecture_comparator import (
    MatchedArchitectureComparatorReceipt,
    adjudicate_matched_architecture_comparator,
)


PATH = Path("validation/streptomyces_matched_architecture_comparator_v1.json")


def test_streptomyces_receipt_recomputes_expected_blockers():
    data = json.loads(PATH.read_text())
    fields = {
        k: data[k]
        for k in MatchedArchitectureComparatorReceipt.__dataclass_fields__
    }
    result = adjudicate_matched_architecture_comparator(
        MatchedArchitectureComparatorReceipt(**fields)
    )
    assert not result.matched_comparator_certified
    assert set(result.blockers) == set(data["expected_blockers"])
    assert not result.generic_game_promoted
    assert not result.architecture_frequency_feedback_promoted


def test_large_genome_reduction_is_not_relabeled_as_generalist_only():
    data = json.loads(PATH.read_text())
    row = data["candidate_engineered_strains_reviewed"][
        "large_subtelomeric_deletion_or_circularized_M145_derivatives"
    ]
    assert not row["accepted_as_shared_comparator"]
    assert "does not isolate terminal differentiation suppression" in row["reason"]


def test_differentiated_candidate_strength_does_not_rescue_missing_s_pair():
    data = json.loads(PATH.read_text())
    assert data["differentiated_state_verified_declared"]
    assert not data["shared_generalist_only_state_verified_declared"]
    assert not data["expected_matched_comparator_certified"]
    assert not data["architecture_mapping_certified"]
