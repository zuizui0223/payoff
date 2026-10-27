from scripts.classify_movebank_taxa_gbif import classify,enrich,summary
def match(class_name="Aves",type_name="EXACT",rank="SPECIES",confidence=99):
    return dict(matchType=type_name,rank=rank,confidence=confidence,
                kingdom="Animalia",**{"class":class_name})

def test_strict_gbif_class():
    assert classify("Ciconia ciconia",lambda n:match())["class_name"]=="Aves"
    for kw in [dict(type_name="FUZZY"),dict(rank="GENUS"),dict(confidence=78)]:
        assert classify("Ciconia ciconia",lambda n:match(**kw))["class_name"]==""
def test_failed_gbif_match_remains_unresolved():
    def fail(name):raise OSError("not reachable")
    assert classify("No such taxon",fail)["status"]=="UNRESOLVED"
def test_source_gps_child_hint_is_separate_from_sensor_hint():
    base=dict(metadata_screen_tier="T1_CUE_AND_DECISION_METADATA",
        source_status="PUBLIC_ITEM_METADATA_PARSED",n_published_animals="36",
        n_published_locations="12",dspace_study_ids="12",
        linked_publication_dois="10.1/x",prior_payoff_source_flag="UNREVIEWED")
    p=[dict(base,doi="one",title="Stork",taxon_scientific_names="Ciconia ciconia",sensor_names="Acceleration"),
       dict(base,doi="two",title="Bat",taxon_scientific_names="Nyctalus noctula",sensor_names="GPS")]
    c=[dict(parent_doi="one",title_hint="white-storks-gps"),
       dict(parent_doi="one",title_hint="JAE_meta_data")]
    t={"Ciconia ciconia":classify("Ciconia ciconia",lambda n:match()),
       "Nyctalus noctula":classify("Nyctalus noctula",lambda n:match("Mammalia"))}
    r=enrich(p,c,t);s=summary(r,list(t.values()))
    assert r[0]["class_scope"]=="AVES_ONLY"
    assert r[0]["gps_child_filename_hint"] and not r[0]["gps_sensor_hint"]
    assert r[0]["reproduction_child_filename_hint"]
    assert r[1]["class_scope"]=="NON_AVES"
    assert s["aves_gps_child_without_gps_sensor"]==1
    assert s["ecological_cue_action_effect"]=="NOT_TESTED"
