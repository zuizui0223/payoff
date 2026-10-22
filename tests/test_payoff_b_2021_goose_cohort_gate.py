"""Synthetic original subject ID comparison tests. No real bird data."""
from scripts.qc_payoff_b_2021_goose_cohort_gate import subject_overlap,parse_readme

def ref(animal,ring,deploy,tag):
    return {"animal-id":animal,"animal-ring-id":ring,"deployment-id":deploy,
            "tag-id":tag,"tag-serial-no":"NA"}

def test_animal_ID_overlap_blocks_independent_claim():
    r=subject_overlap([ref("a","r1","d1","tag1")],
                      [ref("a","r2","d2","tag2")])
    assert r["exact_animal_ring_or_deployment_ID_collision"]
    assert r["true_biological_independence_established"] is False
    assert "tag1" not in str(r)

def test_same_hardware_tag_not_equal_same_bird():
    r=subject_overlap([ref("a","r1","d1","tag1")],
                      [ref("b","r2","d2","tag1")])
    assert not r["exact_animal_ring_or_deployment_ID_collision"]

def test_readme_references_both_studies_and_both_reference_files():
    raw="""Movebank Study ID 9589196
Movebank Study ID 44083081
one_part-gps.csv
two_part-gps.csv
one_part-reference-data.csv
two_part-reference-data.csv"""
    a=parse_readme(raw)
    assert a["expected_study_IDs_complete"]
    assert a["readme_reference_files_exceed_manifest"]
    assert a["readme_GPS_files"]==2
    assert not a["single_study_source"]
