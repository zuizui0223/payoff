from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
THEORY = ROOT / "theory" / "DUAL_USE_INFORMATION_VALUE.md"
DOC = ROOT / "docs" / "PAYOFF_B_DUAL_USE_NOVELTY_BOUNDARY_20260930.md"
RECEIPT = ROOT / "data" / "payoff_b_dual_use_novelty_boundary_20260930.json"


def test_dual_use_novelty_boundary_rejects_generic_voi_claim():
    theory = THEORY.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")

    assert "generic **value of information** is not new" in theory
    assert "generally **non-additive**" in theory
    assert "declared additive separability" in theory
    assert "Avoid:" in doc
    assert "We introduce value of information to ecology or migration." in doc


def test_novelty_receipt_limits_claim_to_deadline_geometry():
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))

    assert receipt["status"] == "LITERATURE_SCREEN_COMPLETE_NONEXHAUSTIVE"
    assert "generic value of information" in receipt["non_novel"]
    assert "information-quality thresholds in stopping problems" in receipt["non_novel"]
    assert "stopping_problems" in receipt["critical_prior_boundary"]
    assert (
        "PAYOFF-B V_A+V_C decomposition is licensed only under declared additive separability"
        == receipt["critical_prior_boundary"]["implication"]
    )
    assert "candidate novelty" in receipt["claim_strength"]
    assert any(
        "cue-dependent effective deadline cost" in item
        for item in receipt["candidate_contributions"]
    )
