import json
from pathlib import Path


ARCH = Path("validation/architecture_mapping_status_v1.json")
PROBES = Path("validation/streptomyces_red_mechanism_probe_priority_v1.json")


def test_architecture_registry_links_positive_probe_recovery_without_promotion():
    arch = json.loads(ARCH.read_text())
    probes = json.loads(PROBES.read_text())
    row = next(x for x in arch["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")

    assert row["prospective_mechanism_probe_receipt"] == probes["registry_id"]
    assert row["prospective_mechanism_probe_ready_count"] == probes["mechanism_probe_ready_count"] == 2
    assert not row["matched_s_generation_suppression_identified"]
    assert not row["matched_generalist_only_comparator_recovered"]
    assert not row["mapping_certified"]
    assert not arch["any_mapping_certified"]


def test_ready_mechanism_probes_and_matched_s_are_distinct_statuses():
    probes = json.loads(PROBES.read_text())
    assert probes["mechanism_probe_ready_count"] > 0
    assert probes["matched_s_certified_count"] == 0
    assert probes["claim_status"] == "PROSPECTIVE_RED_MECHANISM_PROBES_RECOVERED_MATCHED_S_NOT_YET_CERTIFIED"
