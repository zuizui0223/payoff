"""Native-R source schema checks without exposing any bird/event observations."""
from pathlib import Path
import os

import pytest

from scripts.payoff_b_ruppel_native_schema_receipt import summarize


def fake_native_schema_csv(path:Path,corrupt=False):
    header=("original_RData_file,original_R_object_path,original_R_object_class,"
            "n_original_rows,n_original_columns,original_column_name,"
            "original_column_R_class,n_nonmissing_column_values,"
            "candidate_identifier_column,n_distinct_candidate_IDs,"
            "original_ID_values_exported\n")
    entries=[
        "data.Event.RData,data.Event,data.frame,3,2,Tag_ID,character,3,TRUE,2,FALSE",
        "data.Event.RData,data.Event,data.frame,3,2,sunset_time,POSIXct,3,FALSE,,FALSE",
        "flights.RData,flights,data.frame,2,2,Tag_ID,character,2,TRUE,2,FALSE",
        "flights.RData,flights,data.frame,2,2,landing,logical,2,FALSE,,FALSE",
    ]
    if corrupt:
        entries[0]=entries[0].replace(",FALSE",",TRUE")
    path.write_text(header+"\n".join(entries)+"\n",encoding="utf-8")


def test_native_schema_summary_keeps_unique_ID_counts_only(tmp_path):
    path=tmp_path/"meta.csv"
    fake_native_schema_csv(path)
    got=summarize(path)
    assert got["n_original_supported_R_dataframes"]==2
    assert got["original_RData_object_schemas"][0]["n_original_rows"]==3
    assert got["original_RData_object_schemas"][1]["n_original_rows"]==2
    assert got["possible_same_named_ID_columns_across_objects_not_an_authenticated_join"]=={
        "data.Event__flights":["Tag_ID"]
    }
    assert got["same_bird_depart_route_land_chronology_verified"] is False
    assert got["direct_information_deadline_qwait_D_eff"]=="NOT_IDENTIFIED"


def test_native_schema_detects_any_raw_identifier_export_flag(tmp_path):
    path=tmp_path/"meta.csv"
    fake_native_schema_csv(path,corrupt=True)
    with pytest.raises(ValueError,match="Raw original ID export flag"):
        summarize(path)


def test_source_schema_incompatible_column_count_fails(tmp_path):
    path=tmp_path/"meta.csv"
    fake_native_schema_csv(path)
    s=path.read_text()
    path.write_text(s.replace("data.Event,data.frame,3,2,","data.Event,data.frame,3,3,"))
    with pytest.raises(ValueError,match="Original ncols"):
        summarize(path)


def test_real_native_R_output_when_github_actions_supplies_it():
    source=os.getenv("PAYOFF_RUPPEL_NATIVE_SCHEMA_CSV")
    if not source:
        pytest.skip("Original 2023 native R source schema produced only in dedicated workflow")
    r=summarize(Path(source))
    assert r["original_ZIP_and_objects_verified_with_native_R"] is True
    assert r["n_original_supported_R_dataframes"]>=2
    assert r["no_source_animal_identifiers_or_weather_values_exported"] is True
    assert r["same_bird_depart_route_land_chronology_verified"] is False
