"""Source-only integrity screening tests; no real tracking or outcomes."""
from scripts.shortlist_payoff_b_independent_movebank import build_queue,PREVIOUS

def rows():
    g={};s2={};s3={}
    for i in range(446):
        doi=f"10.5441/001/1.synthetic-{i:03d}"
        g[doi]=dict(doi=doi,title="Migration source",
                    taxa_original=f"Birdus species{i}",class_scope="AVES_ONLY",
                    source_status="PUBLIC_ITEM_METADATA_PARSED",
                    gps_child_filename_hint="True",source_animal_count="50",
                    source_location_count="100000",source_study_ids=f"study{i}",
                    source_publications=f"10.1111/doc{i}",
                    previous_payoff_use="UNREVIEWED",tier="T1_CUE_AND_DECISION_METADATA")
        s2[doi]=dict(doi=doi,metadata_rights="CC0 1.0 Universal")
        s3[doi]=dict(doi=doi,published_license="CC0 1.0 Universal",rights_uri="")
    return g,s2,s3

def test_all_446_screened_and_no_biological_promotion():
    a,b,c=rows()
    allrows,q,receipt=build_queue(a,b,c)
    assert len(allrows)==446 and len(q)==8
    assert receipt["publisher_GPS_source_metadata_admitted"]==446
    assert all(not x["actual_independent_animal_cohort_proven"] for x in q)

def test_previous_study_and_publication_overlap_excludes():
    a,b,c=rows()
    target="10.5441/001/1.synthetic-000"
    previous=next(iter(PREVIOUS))
    a[previous],b[previous],c[previous]=dict(
        a[target],doi=previous,source_study_ids="shared",
        source_publications="10.5555/shared"),dict(b[target],doi=previous),dict(c[target],doi=previous)
    a.pop("10.5441/001/1.synthetic-445")
    b.pop("10.5441/001/1.synthetic-445")
    c.pop("10.5441/001/1.synthetic-445")
    a[target]["source_study_ids"]="shared"
    a[target]["source_publications"]="10.5555/shared"
    allrows,q,_=build_queue(a,b,c)
    entry=next(x for x in allrows if x["doi"]==target)
    assert "SHARED_PRIOR_MOVEBANK_STUDY_ID" in entry["reasons"]
    assert "SHARED_PRIOR_PUBLICATION_DOI" in entry["reasons"]
    assert entry["admission"]=="SOURCE_NOT_ADMITTED"

def test_unknown_rights_and_missing_study_fail_closed():
    a,b,c=rows()
    key="10.5441/001/1.synthetic-005"
    a[key]["source_study_ids"]=""
    b[key]["metadata_rights"]="CC BY-NC"
    c[key]["published_license"]="CC BY-NC"
    allrows,q,_=build_queue(a,b,c)
    record=next(x for x in allrows if x["doi"]==key)
    assert "NO_RECORDED_STUDY_ID" in record["reasons"]
    assert "EXPLICIT_CC0_METADATA_ABSENT" in record["reasons"]
    assert key not in [x["doi"] for x in q]
