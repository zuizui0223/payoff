"""Original reference join audit synthetic fixtures; no IDs emitted."""
from scripts.qc_payoff_b_stork_cohort_overlap import compare_refs,key,NEW_REF

def ref(animal,ring,tag,deploy):
    return {"animal-id":animal,"animal-ring-id":ring,
            "deployment-id":deploy,"tag-id":tag,
            "animal-life-stage":"adult","deployment-end-type":"dead",
            "animal-death-comments":"no export"}

def test_exact_animal_overlap_rejects_independent_claim():
    newer=[ref("a1","ring1","tag1","deploy1"),
           ref("a2","ring2","tag2","deploy2")]
    older=[ref("a1","ringX","tagZ","deployZ"),
           ref("a3","ring3","tag3","deploy3")]
    o=compare_refs(newer,older)
    assert o["original_identifier_overlap_by_field"]["animal-id"]["overlapping_identifier_values"]==1
    assert o["cohort_verdict"].startswith("DO_NOT_COUNT_AS_INDEPENDENT")
    assert not o["cohort_independence_proven"]
    assert "a1" not in str(o)
    assert "ring1" not in str(o)

def test_absence_of_identifier_matches_is_not_independence_proof():
    o=compare_refs([ref("a1","NA","T1","d1")],
                   [ref("b2","Unknown","T2","d2")])
    assert o["shared_exact_animal_or_ring_or_deployment_identifier"] is False
    assert o["cohort_verdict"].endswith("BIOLOGICAL_INDEPENDENCE_UNVERIFIED")
    assert key("Unknown")=="" and key("N/A")==""

def test_source_checksum_pinned():
    assert NEW_REF["size"]==43098 and len(NEW_REF["md5"])==32
