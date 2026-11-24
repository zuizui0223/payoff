"""Study-relative Movebank keys must never be treated as proven bird identity."""
import pytest
from scripts import payoff_b_stork_id_join_semantics_20261124 as s


def fabricated():
    rows={}
    for group,n in [("control",19),("delayed",40),("naturally_timed",153)]:
        rows[group]=[{"tag-id":group+"_tag_"+str(i),
                      "animal-id":group+"_animal_"+str(i),
                      "deployment-id":group+"_dep_"+str(i)} for i in range(n)]
    rows["delayed"][0]["tag-id"]=rows["control"][0]["tag-id"]  # 1 C-D
    rows["naturally_timed"][0]["tag-id"]=rows["control"][1]["tag-id"]
    rows["naturally_timed"][1]["tag-id"]=rows["control"][2]["tag-id"]  # 2 C-N
    for j in range(9):
        rows["naturally_timed"][2+j]["tag-id"]=rows["delayed"][1+j]["tag-id"]
    return rows


def test_individual_and_deployment_sources_not_collapsed_to_tag():
    row=[
        {"tag-id":"SENSITIVE_123","animal-id":"ANIMAL_X","deployment-id":"DEP_A"},
        {"tag-id":"SENSITIVE_123","animal-id":"ANIMAL_Y","deployment-id":"DEP_B"},
    ]
    z=s.same_source_profile(row)
    assert z["original_reference_rows"]==2
    assert z["source_id_fields"]["tag-id"]["distinct_nonblank_values"]==1
    assert z["source_id_fields"]["animal-id"]["distinct_nonblank_values"]==2
    assert z["source_id_fields"]["deployment-id"]["distinct_nonblank_values"]==2
    assert z["n_tag_strings_linked_to_multiple_distinct_deployment_strings"]==1
    assert "SENSITIVE_123" not in str(z)


def test_three_study_source_collisions_match_frozen_tag_counts():
    z=s.audit(fabricated())
    assert z["status"]=="SOURCE_IDS_MATCH_PREVIOUS_TAG_GATE_NO_CROSS_COHORT_IDENTITY"
    assert z["n_original_reference_rows"]==212
    assert z["n_studies"]==3
    assert z["identity_join_authorized"] is False
    assert z["same_tag_implies_same_bird"] is False
    assert z["original_tag_animal_deployment_ids_exported"] is False
    assert z["predeparture_information_q_or_recourse_r_estimated"] is False
    assert "control_tag_0" not in str(z)
    assert "delayed_animal_0" not in str(z)


def test_tag_benchmark_drift_does_not_silently_establish_join():
    data=fabricated()
    data["naturally_timed"][0]["tag-id"]="PRIVATE_CHANGE_UNRELATED"
    result=s.audit(data)
    assert result["status"]=="SOURCE_IDS_COLLISION_BENCHMARK_MISMATCH"
    assert result["identity_join_authorized"] is False


def test_csv_source_grain_and_field_schema_rejection():
    raw=(b"tag-id,animal-id,deployment-id,deploy-on-date,deploy-off-date\n"
         b"SENSITIVE_T,A,D,2019-09-01,2020-01-01\n")
    rows=s.read_reference_ids(raw,1)
    assert len(rows)==1
    assert "deploy-on-date" not in rows[0]
    with pytest.raises(ValueError,match="row identity grain"):
        s.read_reference_ids(raw,2)
