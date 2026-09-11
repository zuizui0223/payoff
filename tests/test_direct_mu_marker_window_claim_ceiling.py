import json
from pathlib import Path


MARKER = Path("validation/streptomyces_direct_mu_marker_window_v1.json")
ARCH = Path("validation/architecture_mapping_status_v1.json")


def test_marker_window_freeze_does_not_promote_streptomyces_architecture_status():
    marker = json.loads(MARKER.read_text())
    arch = json.loads(ARCH.read_text())
    strepto = next(row for row in arch["systems"] if row["system_id"] == "STREPTOMYCES_COELICOLOR")

    assert marker["adjudication"]["state_channel_frozen"]
    assert not marker["adjudication"]["direct_mu_fully_ready"]
    assert not marker["claim_ceiling"]["matched_s_certified"]
    assert not marker["claim_ceiling"]["architecture_mapping_certified"]
    assert not strepto["matched_generalist_shared_architecture_recovered"]
    assert not strepto["matched_s_promotion_licensed"]
    assert not strepto["mapping_certified"]
