import pytest

from src.direct_mu_origin_independence import (
    OriginTaggedReference,
    adjudicate_origin_independence,
)


def receipt(refs, class_id="ENTRY_CLASS"):
    result = adjudicate_origin_independence(tuple(refs))
    return next(x for x in result if x.deletion_class == class_id)


def test_two_named_lineages_from_same_origin_cluster_count_once():
    r = receipt(
        [
            OriginTaggedReference("M1_T0", "ENTRY_CLASS", "ZHANG2022_SINGLE_MUTANT_PARENT", True),
            OriginTaggedReference("M5_T0", "ENTRY_CLASS", "ZHANG2022_SINGLE_MUTANT_PARENT", True),
        ]
    )
    assert r.qualified_reference_count == 2
    assert r.independent_origin_count == 1
    assert not r.origin_independence_pass


def test_w3_de_novo_origin_can_supply_second_independent_origin():
    r = receipt(
        [
            OriginTaggedReference("M5_T0", "ENTRY_CLASS", "ZHANG2022_SINGLE_MUTANT_PARENT", True),
            OriginTaggedReference("W3_POST_DELETION", "ENTRY_CLASS", "ZHANG2022_W3_DE_NOVO", True),
        ]
    )
    assert r.independent_origin_count == 2
    assert r.origin_independence_pass


def test_unqualified_material_does_not_count_toward_origin_requirement():
    r = receipt(
        [
            OriginTaggedReference("M5_T0", "ENTRY_CLASS", "ZHANG2022_SINGLE_MUTANT_PARENT", True),
            OriginTaggedReference("W3_POST_DELETION", "ENTRY_CLASS", "ZHANG2022_W3_DE_NOVO", False),
        ]
    )
    assert r.qualified_reference_count == 1
    assert r.independent_origin_count == 1
    assert not r.origin_independence_pass


def test_origin_count_is_class_specific():
    refs = (
        OriginTaggedReference("A", "ENTRY_CLASS", "O1", True),
        OriginTaggedReference("B", "INTERMEDIATE_CLASS", "O2", True),
        OriginTaggedReference("C", "ENTRY_CLASS", "O3", True),
    )
    entry = receipt(refs, "ENTRY_CLASS")
    intermediate = receipt(refs, "INTERMEDIATE_CLASS")
    assert entry.origin_independence_pass
    assert not intermediate.origin_independence_pass


def test_invalid_origin_or_class_rejected():
    with pytest.raises(ValueError):
        adjudicate_origin_independence((OriginTaggedReference("A", "BAD", "O1", True),))
    with pytest.raises(ValueError):
        adjudicate_origin_independence((OriginTaggedReference("A", "ENTRY_CLASS", "", True),))
