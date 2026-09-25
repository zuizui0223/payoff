import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_MOVEMENT_PHENOLOGY_GEB_V3_PREOUTCOME.md"
AMENDMENT = ROOT / "data" / "payoff_b_geb_broad_test_primary_framing_20260925.json"


def test_geb_primary_claim_is_broad_55_species_falsification():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "No universal migration–phenology speed optimum" in text
    assert "Tier 1 was the primary macroecological test" in text
    assert "55-species test determines whether a universal speed rule survives" in text
    assert "The broad result is the absence of a universal speed rule" in text


def test_direct_taxa_are_mechanistic_not_meta_analytic_replication():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "mechanistic panel rather than a three-study meta-analysis" in text
    assert "mechanistic decomposition rather than independent meta-analytic replication" in text
    assert "not “one optimal speed” and not “one universal \\(\\lambda\\)”" in text


def test_framing_amendment_changes_no_scientific_result():
    payload = json.loads(AMENDMENT.read_text(encoding="utf-8"))
    assert payload["scientific_results_changed"] is False
    assert payload["registered_thresholds_changed"] is False
    assert payload["aikens_outcome_opened"] is False
    assert payload["revised_hierarchy"]["tier_1_primary"].startswith("55-species")
