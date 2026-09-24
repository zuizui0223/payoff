import json
from dataclasses import asdict
from pathlib import Path

from src.cross_system_lambda_reliability import (
    evaluate_cross_system_lambda_reliability,
    systems_from_registry,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = (
    ROOT
    / "data"
    / "payoff_b_lambda_recovery_taxon_registry_20260922.json"
)
RECEIPT = (
    ROOT
    / "data"
    / "payoff_b_cross_system_lambda_reliability_gate_20260924.json"
)


def test_frozen_cross_system_reliability_receipt_matches_live_registry_gate():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    gate = evaluate_cross_system_lambda_reliability(
        systems_from_registry(registry)
    )
    assert receipt["gate"] == asdict(gate)


def test_current_receipt_keeps_coordinate_and_magnitude_claims_separate():
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert receipt["gate"]["estimator_scale_coordinate_licensed"]
    assert not receipt["gate"]["latent_magnitude_comparison_licensed"]
    assert "ranking taxa by corrected phase-retention strength" in (
        receipt["claim_boundary"]["hold"]
    )
