"""Original public Rüppel 2023 Figshare RData source / SHA fail-closed tests."""
import hashlib
import os
from pathlib import Path
from zipfile import ZipFile

import pytest
pd = pytest.importorskip("pandas")
pytest.importorskip("pyreadr")

from scripts.payoff_b_ruppel_rdata_source_gate import (
    ZIP_NAME, ZIP_SHA256, MEMBERS, dataframe_schema,
    inspect_rdata_zip, validate_zip
)


def test_individual_identifier_count_not_values():
    source=pd.DataFrame({
        "Tag_ID":["SECRET_A","SECRET_A","SECRET_B"],
        "depart.time":["2020-04-12T20:00","2020-04-13T20:00","2020-04-13T22:00"],
        "wind_u":[1.,2.,3.],
        "landing":[0,1,0],
    })
    item=dataframe_schema(source,"synthetic.RData","bird_event")
    assert item["original_rows"]==3
    assert "Tag_ID" in item["candidate_individual_id_columns"]
    assert "depart.time" in item["candidate_time_columns"]
    assert "landing" in item["candidate_decision_columns"]
    assert "wind_u" in item["candidate_weather_columns"]
    assert item["aggregate_candidate_id_cardinality"]["Tag_ID"]["n_distinct_values"]==2
    assert "SECRET_A" not in str(item)
    assert item["unresolved_same_individual_weather_decision_join"] is True


def test_original_zip_requires_exact_member_inventory_size_and_sha(tmp_path):
    p=tmp_path/ZIP_NAME
    with ZipFile(p,"w") as z:
        for member in MEMBERS:
            z.writestr(member,b"SYNTHETIC TEST BINARY, NOT REAL RDATA")
        z.writestr("Rcode.Rmd",b"# synthetic input")
    data=p.read_bytes()
    with pytest.raises(ValueError,match="original 2023 Figshare ZIP|Original 2023 Figshare ZIP"):
        validate_zip(p)
    with validate_zip(p,source_size=len(data),
                      source_hash=hashlib.sha256(data).hexdigest()) as z:
        assert set(MEMBERS).issubset(set(z.namelist()))
    assert len(ZIP_SHA256)==64


def test_source_zip_wrong_provider_name_fails(tmp_path):
    p=tmp_path/"not_figshare_original.zip"
    p.write_bytes(b"nothing")
    with pytest.raises(ValueError,match="provider ZIP filename"):
        validate_zip(p,source_size=7,source_hash="0"*64)


def test_original_public_rdata_gate_only_when_ci_supply():
    p=os.getenv("PAYOFF_RUPPEL_2023_ORIGINAL_ZIP")
    if not p:
        pytest.skip("Source ZIP not committed; dedicated SHA-pinned GitHub Actions provides original")
    x=inspect_rdata_zip(Path(p))
    assert x["original_file_bytes_verified"] is True
    assert x["original_RMarkdown_audit"]["references_data_Event"] is True
    assert x["original_RMarkdown_audit"]["references_flights"] is True
    assert x["source_same_bird_three_decision_fit_admitted"] is False
    assert x["no_new_biological_effect"] is True
    assert x["direct_theoretical_information_deadline"]=="NOT_IDENTIFIED"
