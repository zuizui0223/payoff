"""Curlew original-source access, nesting grain and no-causal-cue safety gate."""
import io

import pytest
pytest.importorskip("requests", reason="Original Dryad HTTP audit has optional dependency; dedicated workflow installs it")

from scripts.payoff_b_curlew_dryad_source_gate import (
    AccessHold, RangeFile, _parse_year, discover, summarize_original_csv,
)

HEADER = ("ID_seas;Bird_ID;Sex;Non_gr;Br_gr;Nest_succ;"
          "Dist;Prebr;st_grass;st_wetland")
ROWS = [
    "A_2018;A;F;ATL-S;NE;0;1200;11;0.2;0.8",
    "A_2019;A;F;ATL-S;NE;1;1200;14;0.2;0.8",
    "B_2018;B;M;NSea;W;1;700;20;NA;0.5",
    "B_2019;B;M;NSea;W;1;700;22;NA;0.5",
    "C_2018;C;F;ATL-N;W;0;1500;10;0.5;0.5",
    "C_2020;C;F;ATL-N;W;0;1500;12;0.5;0.5",
]


def fixture(rows=ROWS,header=HEADER):
    return ("\n".join([header,*rows])+"\n").encode()


def test_record_grain_is_bird_season_not_independent_migration_fix():
    r=summarize_original_csv(fixture())
    assert r["n_original_derived_rows"]==6
    assert r["n_unique_Bird_ID"]==3
    assert r["n_unique_source_ID_seas"]==6
    assert r["n_birds_with_two_or_more_distinct_season_IDs"]==3
    assert r["n_repeated_birds_with_both_success_values"]==1
    assert r["n_repeated_birds_with_Prebr_change"]==3
    assert r["n_distinct_suffix_years_under_conservative_rule"]==3
    assert r["within_individual_observational_gate"]=="NOT_IDENTIFIABLE_UNDER_FROZEN_MINIMUM_SUPPORT"
    assert r["actual_predecision_cue_observed"] is False
    assert r["direct_PAYOFF_B_information_deadline"]=="NOT_ESTIMABLE"


def test_wrong_delimiter_or_omitted_source_column_fails():
    with pytest.raises(ValueError,match="semicolon schema"):
        summarize_original_csv(fixture(header=HEADER.replace(";",",")))


def test_negative_prebr_fails_with_no_causal_fill():
    invalid=ROWS.copy()
    invalid[1]=invalid[1].replace(";14;",";-3;")
    with pytest.raises(ValueError,match="Negative source Prebr"):
        summarize_original_csv(fixture(invalid))


def test_invalid_nest_status_and_out_of_range_habitat_detected():
    invalid=ROWS.copy()
    invalid[1]=invalid[1].replace(";1;1200",";2;1200")
    r=summarize_original_csv(fixture(invalid))
    assert r["n_invalid_source_nest_success_values"]==1
    assert r["within_individual_observational_gate"]=="NOT_IDENTIFIABLE_UNDER_FROZEN_MINIMUM_SUPPORT"
    invalid=ROWS.copy()
    invalid[0]=invalid[0].replace(";0.2;",";1.3;")
    with pytest.raises(ValueError,match="proportion out of bounds"):
        summarize_original_csv(fixture(invalid))


def test_undocumented_year_encoding_remains_unverified():
    assert _parse_year("B_2019")==2019
    assert _parse_year("B-2019")==2019
    assert _parse_year("B2019") is None
    invalid=ROWS.copy()
    invalid[0]=invalid[0].replace("A_2018","A2018")
    out=summarize_original_csv(fixture(invalid))
    assert out["year_suffix_fully_parseable"] is False


class FakeResponse:
    status_code=200
    headers={"Content-Length":"590990000"}
    def __enter__(self):
        return self
    def __exit__(self,*a):
        return False

class FakeClient:
    def get(self,*args,**kwargs):
        return FakeResponse()

def test_range_reader_refuses_server_full_download():
    with pytest.raises(AccessHold,match="RANGE_NOT_AVAILABLE"):
        RangeFile(FakeClient(),"https://datadryad.org/api/v2/files/123/download")


class FakeMetadataClient:
    def get(self,url,**kwargs):
        self.last=url
        class Resp:
            status_code=200
            headers={"Content-Type":"application/json"}
            def __init__(self,url):
                if url.endswith("/versions/82/files"):
                    self.content=b'{"_embedded":{"stash:files":[{"_links":{"self":{"href":"https://datadryad.org/api/v2/files/34"}},"path":"Curlew_COE_habitat.zip","size":590990000},{"_links":{"self":{"href":"https://datadryad.org/api/v2/files/35"}},"path":"README.md","size":14320}]}}'
                elif url.endswith("/versions"):
                    self.content=b'{"_embedded":{"stash:versions":[{"id":82,"versionNumber":1}]}}'
                else:
                    self.content=b'{"title":"Synthetic source metadata only","identifier":"doi:10.5061/dryad.31zcrjf22"}'
            def __enter__(self):return self
            def __exit__(self,*a):return False
        return Resp(url)


def test_original_api_file_list_is_not_data_access():
    got=discover(FakeMetadataClient())
    assert got["version_id"]==82
    assert {f["filename"] for f in got["file_manifest"]}=={
        "Curlew_COE_habitat.zip","README.md"
    }
    assert got["dataset_identifier"]=="doi:10.5061/dryad.31zcrjf22"
    assert "source_bird_rows" not in got
