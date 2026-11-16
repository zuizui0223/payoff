"""Source contract tests only, no empirical effects."""
import hashlib
import io
import zipfile
import pytest
pytest.importorskip("openpyxl")
from scripts.payoff_b_little_owl_source_gate import (
    verify, summarise_csv, inspect
)

def test_fail_closed_checksum_and_valid_md5():
    raw=b"source,prey\nA,3\n"
    md5=hashlib.md5(raw).hexdigest()
    assert verify(raw,"md5:"+md5)["verified"]
    assert not verify(raw+b"x","md5:"+md5)["verified"]
    assert not verify(raw,None)["verified"]

def test_csv_schema_preserves_dates_and_prey_units():
    raw=b"nest_id,day,number_prey,estimated_biomass_g\nN1,8,2,5.1\n"
    x=summarise_csv(raw,"original.csv")
    assert x["n_rows_scanned"]==1
    assert x["columns"]==["nest_id","day","number_prey","estimated_biomass_g"]

def test_zip_nested_verifiable_source_csv():
    z=io.BytesIO()
    with zipfile.ZipFile(z,"w") as f:
        f.writestr("original/provisioning.csv",
                    "nest,visit,biomass_g\nB1,1,2.5\n")
    o=inspect(z.getvalue(),"study.zip")
    assert o["n_members"]==1
    assert o["members"][0]["schema"]["n_rows_scanned"]==1
