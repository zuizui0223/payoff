"""Offline source admission only; never an ecological effect test."""
import hashlib
import pytest
pytest.importorskip("openpyxl")
from scripts.payoff_b_dryad_official_public_stream_probe import (
    csv_report,PUBLIC_WEBSITE_PREFIX,DATASETS
)
from scripts.payoff_b_dryad_food_supplement_provisioning_probe import (
    validate_manifest_digest
)

def test_documented_public_link_prefix_is_not_private_api():
    assert PUBLIC_WEBSITE_PREFIX=="https://datadryad.org/downloads/file_stream/"
    assert "/api/v2/files/" not in PUBLIC_WEBSITE_PREFIX

def test_original_manifest_sha256_refuses_modified_bytes():
    raw=b"bird,year,Nesting_success\nBird1,2020,1\n"
    f={"digestType":"sha-256","digest":hashlib.sha256(raw).hexdigest()}
    assert validate_manifest_digest(raw,f)["verified"]
    assert not validate_manifest_digest(raw+b"tampered",f)["verified"]

def test_source_csv_columns_retain_breeding_endpoint():
    raw=b"Bird_ID,Year,Nesting_success,GDD_jerk\nA,2020,1,118\n"
    o=csv_report(raw)
    assert o["n_rows"]==1
    assert "Nesting_success" in o["columns"]
    assert o["individual_row_values_not_exposed"]

def test_expected_files_are_exact_public_manifest_targets():
    assert DATASETS["boom_goose_nest"]["file"]=="1.NestLocationData.csv"
    assert DATASETS["seress_great_tit_nests"]["file"].endswith(".xlsx")
