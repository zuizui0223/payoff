from pathlib import Path
from scripts.qc_public_movebank_stork_breeding_2018 import (
    read_stork_breeding, FILES, DOI,
)


def test_source_identity_and_checksums_are_declared():
    assert DOI == "10.5441/001/1.v8d24552"
    assert len(FILES) == 3
    for uuid, md5, n in FILES.values():
        assert len(uuid) == 36 and len(md5) == 32 and n > 0


def test_reference_link_and_missingness_do_not_disclose_ids(tmp_path: Path):
    reference = tmp_path / "reference.csv"
    breeding = tmp_path / "breeding.csv"
    reference.write_text("deployment-id,animal-taxon\n123,Ciconia ciconia\n456,Ciconia ciconia\n")
    breeding.write_text(
        "id,Year,Sex,Fledglings,Breeding attempt,comment\n"
        "123,2014,F,2,1,\n123,2015,F,NA,1,\n999,2015,M,Unknown,0,\n"
    )
    result = read_stork_breeding(breeding, reference)
    assert result["reference_unique_deployments"] == 2
    assert result["breeding_individual_year_rows"] == 3
    assert result["breeding_distinct_individual_ids"] == 2
    assert result["breeding_rows_with_reference_deployment_match"] == 2
    assert result["breeding_unique_ids_without_reference_match"] == 1
    assert result["fledgling_count_numeric_rows"] == 1
    assert result["fledgling_missing_or_unknown_rows"] == 2
    assert result["mean_fledglings_among_numeric_rows"] == 2
    assert not result["movement_events_joined"]
    assert "individual_ids" not in result
