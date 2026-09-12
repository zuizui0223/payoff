import json
from pathlib import Path

from src.direct_mu_origin_provenance_gate import (
    OriginProvenanceCandidate,
    certify_origin_provenance,
)

REGISTRY = Path("validation/zhang2020_direct_mu_origin_candidate_registry_v1.json")


def test_name_pattern_never_certifies_independent_origin():
    r = certify_origin_provenance(
        OriginProvenanceCandidate(
            "9H1A", "ZHANG2020", False, False, False, True
        )
    )
    assert not r.independent_origin_certified
    assert "INDEPENDENCE_INFERRED_FROM_STRAIN_NAME" in r.blockers


def test_explicit_complete_provenance_can_certify_origin():
    r = certify_origin_provenance(
        OriginProvenanceCandidate(
            "X", "REGISTERED_SOURCE", True, True, True, False
        )
    )
    assert r.independent_origin_certified
    assert r.blockers == ()


def test_zhang2020_registry_has_30_unique_mutant_ids_but_zero_certified_origins():
    data = json.loads(REGISTRY.read_text())
    ids = data["candidate_ids"]
    assert len(ids) == 30
    assert len(set(ids)) == 30
    assert data["origin_provenance_status"]["candidate_id_count"] == 30
    assert data["origin_provenance_status"]["explicit_origin_provenance_count"] == 0
    assert data["origin_provenance_status"]["independent_origin_certified_count"] == 0
    assert data["origin_provenance_status"]["origin_clusters_certified"] == 0


def test_four_competition_candidates_are_high_information_not_origin_certified():
    data = json.loads(REGISTRY.read_text())
    high = data["high_information_candidates"]
    assert set(high) == {"2H1A", "8H1B", "9H1B", "9H1A"}
    assert "broad_frequency_competition_reported" in high["9H1A"]
    assert data["origin_provenance_status"]["independent_origin_certified_count"] == 0


def test_origin_recovery_does_not_promote_claims():
    data = json.loads(REGISTRY.read_text())
    assert all(value is False for value in data["claim_ceiling"].values())
