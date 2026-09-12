import json
from pathlib import Path

ACCESS = Path("validation/streptomyces_direct_mu_material_access_v1.json")


def load():
    return json.loads(ACCESS.read_text())


def test_archived_stock_evidence_is_not_treated_as_public_material_access():
    data = load()
    assert data["primary_source_facts"]["lineages_archived_during_experiment"]
    assert data["primary_source_facts"]["stocks_maintained_at_minus_20C"]
    adjudication = data["material_access_adjudication"]
    assert not adjudication["public_culture_collection_accession_recovered_from_inspected_primary_source"]
    assert not adjudication["public_strain_repository_deposit_recovered_from_inspected_primary_source"]
    assert not adjudication["physical_stock_nonexistence_inferred"]
    assert adjudication["author_or_originating_lab_identity_confirmation_required"]


def test_material_access_does_not_promote_reference_or_architecture_claims():
    ceiling = load()["claim_boundary"]
    assert all(value is False for value in ceiling.values())


def test_priority_materials_have_predeclared_access_action():
    materials = load()["priority_materials"]
    assert [x["candidate_id"] for x in materials] == ["M5_T0", "M1_T0"]
    assert all(not x["public_accession_recovered"] for x in materials)
    assert all(
        x["next_access_action"]
        == "CONFIRM_STOCK_IDENTITY_AND_AVAILABILITY_WITH_ORIGINATING_AUTHORS_OR_LAB"
        for x in materials
    )
