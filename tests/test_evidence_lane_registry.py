import json
from pathlib import Path

from src.evidence_lane_separation import (
    ArchitectureMappingReceipt,
    GenericGameReceipt,
    RawArchiveReceipt,
    adjudicate_evidence_lanes,
)


REGISTRY = Path("validation/evidence_lane_registry_v1.json")


def test_registry_entries_recompute_expected_architecture_specific_status():
    data = json.loads(REGISTRY.read_text())
    assert data["registry_id"] == "PAYOFF_EVIDENCE_LANE_REGISTRY_V1"
    assert data["systems"]

    for row in data["systems"]:
        raw = RawArchiveReceipt(**row["raw"]) if row["raw"] is not None else None
        game = GenericGameReceipt(**row["game"])
        architecture = ArchitectureMappingReceipt(**row["architecture"])
        result = adjudicate_evidence_lanes(
            game,
            architecture,
            raw=raw,
            pair_alignment_declared=row["alignment"]["declared"],
            pair_alignment_reference=row["alignment"]["reference"],
        )
        assert (
            result.architecture_specific_claim_licensed
            == row["expected_architecture_specific_claim_licensed"]
        ), row["name"]


def test_no_current_empirical_registry_entry_is_silently_promoted_to_e1():
    data = json.loads(REGISTRY.read_text())
    assert not any(
        row["expected_architecture_specific_claim_licensed"]
        for row in data["systems"]
    )


def test_pstutzeri_is_generic_game_positive_but_architecture_negative():
    row = json.loads(REGISTRY.read_text())["systems"][0]
    result = adjudicate_evidence_lanes(
        GenericGameReceipt(**row["game"]),
        ArchitectureMappingReceipt(**row["architecture"]),
        raw=RawArchiveReceipt(**row["raw"]),
        pair_alignment_declared=row["alignment"]["declared"],
        pair_alignment_reference=row["alignment"]["reference"],
    )
    assert result.generic_game_validation_certified
    assert not result.architecture_mapping_certified
    assert not result.architecture_specific_claim_licensed


def test_beck_r3_is_certified_raw_reconstruction_but_not_game_or_architecture():
    row = json.loads(REGISTRY.read_text())["systems"][-1]
    result = adjudicate_evidence_lanes(
        GenericGameReceipt(**row["game"]),
        ArchitectureMappingReceipt(**row["architecture"]),
        raw=RawArchiveReceipt(**row["raw"]),
        pair_alignment_declared=row["alignment"]["declared"],
        pair_alignment_reference=row["alignment"]["reference"],
    )
    assert result.raw_reconstruction_certified
    assert not result.raw_analysis_reproduction_certified
    assert not result.generic_game_validation_certified
    assert not result.architecture_mapping_certified
    assert not result.architecture_specific_claim_licensed
    assert "RAW_RECONSTRUCTION_NOT_CERTIFIED" not in result.blockers
    assert "GENERIC_GAME_VALIDATION_NOT_CERTIFIED" in result.blockers
    assert "ARCHITECTURE_MAPPING_NOT_CERTIFIED" in result.blockers
