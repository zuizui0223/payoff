import json
from pathlib import Path


PATH = Path("validation/streptomyces_m5_pacbio_marker_corroboration_v1.json")


def test_observed_pacbio_pattern_matches_deep_but_is_corroboration_only():
    data = json.loads(PATH.read_text())
    cov = data["registered_marker_coverage"]
    assert cov["SCO3879"]["coverage_percent"] == 100.0
    assert cov["SCO3879"]["mean_depth"] == 124.526
    for locus in ("SCO7036", "SCO7350", "SCO7662"):
        assert cov[locus]["coverage_percent"] == 0.0
        assert cov[locus]["mean_depth"] == 0.0
    adj = data["adjudication"]
    assert adj["pattern_matches_registered_deep_class"] is True
    assert adj["evidence_role"] == "INDEPENDENT_PACBIO_CORROBORATION"
    assert adj["primary_bgi_marker_gate_satisfied"] is False


def test_pacbio_corroboration_cannot_increment_qualified_reference_count():
    data = json.loads(PATH.read_text())
    assert data["adjudication"]["qualified_d_reference"] is False
    assert data["claim_ceiling"]["qualified_d_reference_count_increment"] == 0
    assert data["claim_ceiling"]["registered_deletion_class_qualified_by_primary_bgi_gate"] is False
    assert data["claim_ceiling"]["architecture_mapping_certified"] is False
    assert data["claim_ceiling"]["eta_architecture_specific"] is False
    assert data["claim_ceiling"]["e1"] is False
