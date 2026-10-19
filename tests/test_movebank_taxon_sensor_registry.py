"""Offline taxonomy-metadata census tests. No live animals or network."""
import pytest
from scripts.build_movebank_taxon_sensor_registry import (
    canonical_landing, doi_from_item, parse_item, summarise,
)


def row(doi="10.5441/001/1.testabc",tier="T1_CUE_AND_DECISION_METADATA"):
    return {
        "doi":doi,"title":"Migratory animal tracking",
        "linked_publication_dois":"10.1111/somepaper",
        "metadata_screen_tier":tier,
        "prior_payoff_source_flag":"UNREVIEWED",
    }


def item(doi="10.5441/001/1.testabc"):
    return {
        "id":"a0b0c0",
        "metadata":{
            "dc.identifier.doi":[{"value":"doi:"+doi}],
            "dwc.ScientificName":[{"value":"Ciconia ciconia"}],
            "sensor.name":[{"value":"GPS"},{"value":"Acceleration"}],
            "mdr.study.id":[{"value":"560041066"}],
            "mdr.animal.count":[{"value":"36"}],
            "mdr.location.count":[{"value":"1207130"}],
            "dc.rights":[{"value":"CC0 1.0 Universal"}],
        },
    }


def test_source_doi_and_publisher_metadata_parsing():
    r=parse_item(row(),item())
    assert r["doi_consistency"]=="MATCHED"
    assert r["n_published_animals"]==36
    assert r["n_published_locations"]==1207130
    assert r["taxon_scientific_names"]=="Ciconia ciconia"
    assert "GPS" in r["sensor_names"]
    assert not r["fitness_association_estimated"]


def test_doi_mismatch_rejected_not_silently_matched():
    with pytest.raises(ValueError,match="does not match"):
        parse_item(row(),item(doi="10.5441/001/1.other"))


def test_only_known_movebank_sources_allowed():
    url=canonical_landing("https://www.datarepository.movebank.org/handle/10255/move.791")
    assert url=="https://datarepository.movebank.org/handle/10255/move.791"
    with pytest.raises(ValueError,match="not on official"):
        canonical_landing("https://example.org/fake")


def test_source_metadata_not_misread_as_independent_cohorts():
    x=parse_item(row(),item())
    y=parse_item(row(doi="10.5441/001/1.other",tier="T2_DECISION_METADATA"),
                 item(doi="10.5441/001/1.other"))
    o=summarise([x,y])
    assert o["status"]=="COMPLETE"
    assert o["unique_scientific_name_strings"]==1
    assert o["study_id_shared_by_multiple_parent_dois"]==1
    assert o["independent_biological_studies_count"]=="NOT_ESTIMABLE"
    assert o["reported_location_count_distribution"]["count"]==2
