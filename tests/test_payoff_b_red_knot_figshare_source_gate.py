"""Original experiment file-ID, archive structure and no bird-row leakage tests."""
import hashlib
import io
import zipfile

import pytest
pytest.importorskip("requests")

from scripts.payoff_b_red_knot_figshare_source_gate import (
    MAX_FILE, official_provider, schema, inspect_zip, original_file_metadata,
    audit
)


def test_only_original_bounded_public_Figshare_urls_allowed():
    assert official_provider("https://figshare.com/ndownloader/files/987654",987654)
    assert official_provider("https://ndownloader.figshare.com/files/987654",987654)
    assert not official_provider("https://figshare.com/ndownloader/files/987",987654)
    assert not official_provider("http://ndownloader.figshare.com/files/987654",987654)
    assert not official_provider("https://private.example.org/files/987654",987654)
    assert MAX_FILE == 8*1024*1024


def test_original_file_duplicate_ids_are_rejected():
    m={"files":[
        {"id":2,"name":"a.csv","size":20},
        {"id":2,"name":"b.csv","size":20},
    ]}
    with pytest.raises(ValueError,match="Duplicate Figshare"):
        original_file_metadata(m)


def test_original_aviary_and_treatment_schema_is_not_an_admitted_treatment_effect():
    text=(
        "Bird_ID,Year,Aviary,Treatment_hours,Body_mass,Release_date,Departure_date\n"
        "SECRET_A,2022,1,6,112,2022-04-30,2022-05-18\n"
        "SECRET_B,2022,1,6,108,2022-04-30,\n"
        "SECRET_C,2022,2,24,126,2022-04-30,2022-05-11\n"
    )
    out=schema(text.encode(),"original_2025.csv")
    assert out["n_original_rows"]==3
    assert "Bird_ID" in out["field_roles_by_name_only"]["individual"]
    assert "Aviary" in out["field_roles_by_name_only"]["aviary"]
    assert "Treatment_hours" in out["field_roles_by_name_only"]["treatment"]
    assert "Departure_date" in out["field_roles_by_name_only"]["departure"]
    assert out["candidate_field_aggregate_cardinality"]["treatment"]["Treatment_hours"]["n_unique_nonmissing"]==2
    assert "SECRET_A" not in str(out)
    assert "2022-05-18" not in str(out)
    assert out["individual_aviary_year_treatment_join_proven"] is False


def test_bounded_original_zip_schema_only_no_raw_values():
    txt="animal,aviary,treatment,release,departure\nSECRET_ID,A,6,0,20\n"
    raw=io.BytesIO()
    with zipfile.ZipFile(raw,"w") as z:
        z.writestr("data/staging_data.csv",txt.encode())
        z.writestr("src/analysis.R","library(survival)")
    out=inspect_zip(raw.getvalue(),"published.zip")
    assert len(out["members"])==2
    assert len(out["source_table_schemas"])==1
    assert out["source_table_schemas"][0]["n_original_rows"]==1
    assert "SECRET_ID" not in str(out)


class Response:
    def __init__(self,data,status=200):
        self.content=data
        self.status_code=status
        self.headers={"Content-Length":str(len(data))}
    def iter_content(self,size):
        yield self.content
    def close(self):pass


class FakeSession:
    def get(self,url,**kwargs):
        if url.endswith("/articles/28660718"):
            item={
                "title":"Synthetic experiment original metadata",
                "doi":"10.6084/m9.figshare.28660718",
                "version":1,"published_date":"2025-11-06",
                "files":[{
                    "id":123,"name":"original_data.csv","size":52,
                    "download_url":"https://ndownloader.figshare.com/files/123",
                }],
            }
            import json
            return Response(json.dumps(item).encode())
        if url.endswith("/files/123"):
            return Response(b"Bird_ID,Treatment_hours\nSECRET_A,6\nSECRET_B,12\n")
        return Response(b"not found",status=404)


def test_original_source_public_metadata_does_not_claim_aviary_randomization_join():
    got=audit(FakeSession())
    assert got["source_data_access_status"].startswith("ORIGINAL_TABULAR_SCHEMA_FOUND")
    assert got["n_original_plain_or_archived_tabular_schemas"]==1
    assert got["source_individual_aviary_year_departure_join_confirmed"] is False
    assert got["new_biological_effect_fitted"] is False
    assert "SECRET_A" not in str(got)
