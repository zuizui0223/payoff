import json
from pathlib import Path

from src.direct_mu_origin_independence import OriginTaggedReference, adjudicate_origin_independence


STATUS = Path("validation/streptomyces_direct_mu_materialization_priority_v1.json")


def load():
    return json.loads(STATUS.read_text())


def test_priority_order_prefers_stable_M5_then_independent_W3_then_M1():
    rows = load()["registered_materialization_order"]
    assert [x["candidate_id"] for x in rows] == ["M5_T0", "W3_POST_DELETION", "M1_T0"]
    assert [x["rank"] for x in rows] == [1, 2, 3]
    assert all(not x["qualified_reference"] for x in rows)


def test_M_lineages_share_one_origin_cluster():
    data = load()
    cluster = data["origin_clusters"]["ZHANG2022_SINGLE_MUTANT_PARENT"]
    assert set(cluster["members"]) == {"M1_T0", "M3_T0", "M4_T0", "M5_T0", "M6_T0"}
    assert cluster["independent_origin_count"] == 1
    assert data["panel_implication"]["two_named_M_lineages_must_not_be_counted_as_two_independent_references"]


def test_M5_plus_M1_cannot_satisfy_two_origin_rule_even_if_both_later_qualified():
    refs = (
        OriginTaggedReference("M5_T0", "ENTRY_CLASS", "ZHANG2022_SINGLE_MUTANT_PARENT", True),
        OriginTaggedReference("M1_T0", "ENTRY_CLASS", "ZHANG2022_SINGLE_MUTANT_PARENT", True),
    )
    entry = next(x for x in adjudicate_origin_independence(refs) if x.deletion_class == "ENTRY_CLASS")
    assert entry.qualified_reference_count == 2
    assert entry.independent_origin_count == 1
    assert not entry.origin_independence_pass


def test_M5_plus_W3_can_satisfy_origin_rule_only_if_both_later_qualify_same_class():
    refs = (
        OriginTaggedReference("M5_T0", "ENTRY_CLASS", "ZHANG2022_SINGLE_MUTANT_PARENT", True),
        OriginTaggedReference("W3_POST_DELETION", "ENTRY_CLASS", "ZHANG2022_W3_DE_NOVO", True),
    )
    entry = next(x for x in adjudicate_origin_independence(refs) if x.deletion_class == "ENTRY_CLASS")
    assert entry.independent_origin_count == 2
    assert entry.origin_independence_pass


def test_current_status_does_not_promote_claims():
    data = load()
    assert data["panel_implication"]["current_materialized_qualified_reference_count"] == 0
    assert not data["panel_implication"]["current_origin_independence_pass_for_any_registered_class"]
    assert all(value is False for value in data["claim_ceiling"].values())
