"""Contract tests: no biological effect or migration admission by assumption."""
from scripts.qc_payoff_b_unopened_gps_source import SOURCES,source_status

def summary(n,events,years,taxon):
    return {
        "classified_source_taxa":{taxon:{
            "animal_years_with_geovalid_days":n,
            "candidate_stationary_to_northward_events":events,
            "animal_years_with_one_or_more_candidates":years
        }}
    }

def test_original_CC0_source_pinned_and_biologically_distinct_species():
    assert set(SOURCES)=={"pinkfoot_goose","egyptian_vulture"}
    assert len({x["taxon"] for x in SOURCES.values()})==2
    for src in SOURCES.values():
        assert len(src["uuid"])==36 and len(src["md5"])==32
        assert src["size"]>1000000
        assert src["license"]=="CC0 1.0 Universal"

def test_source_label_admission_never_infers_actual_cue_use():
    taxon="Anser brachyrhynchus"
    assert source_status({},summary(20,18,11,taxon),taxon)=="CANDIDATE_STAGEWISE_MIGRATION_SOURCE_GEOMETRY"
    assert source_status({},summary(20,5,3,taxon),taxon).startswith("NOT_ADMITTED_")
    assert source_status({},summary(1,15,11,taxon),taxon).startswith("NOT_ADMITTED_")
    assert source_status({},summary(20,15,11,"Wrong bird"),taxon)=="NOT_ADMITTED_TAXON_MISMATCH"

def test_no_spring_sample_does_not_turn_into_zero_effect():
    assert source_status({},{"classified_source_taxa":{}},"Neophron percnopterus")=="NOT_ADMITTED_NO_SPRING_SOURCE_TRACKS"
