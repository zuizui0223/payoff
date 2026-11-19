"""Published independent observation-source inventory; no biological effect fit."""
from pathlib import Path
import os
import pytest

pytest.importorskip("pandas",reason="NumPy/pandas numerical source work is tested in dedicated CI")
pytest.importorskip("numpy")

from scripts.payoff_b_e6_known_ebird_exclusion import read_verified_artifact
from scripts.payoff_b_e6_source_origin_inventory import SOURCES,inventory


def test_metadata_partition_independent_sources_no_double_count():
    assert len(SOURCES)==26
    assert len(set(s[0] for s in SOURCES))==26
    assert sum(s[1] for s in SOURCES)==676
    assert 680-676==4
    assert all(s[3].startswith("https://") for s in SOURCES)


def test_immutable_previous_e6_source_when_archive_supplied():
    fp=os.environ.get("PAYOFF_E6_ARCHIVED_ARTIFACT_ZIP")
    if not fp:
        pytest.skip("Historical GitHub E6 artifact not checked in; dedicated workflow provides it")
    result=inventory(read_verified_artifact(Path(fp)))
    assert result["original_E6_effects"]==944
    assert result["known_eBird_study_effects_excluded"]==264
    assert result["remaining_after_forced_exclusion_effects"]==680
    assert result["studies_with_published_alternative_primary_observation_origin"]==26
    assert result["effects_with_published_alternative_primary_observation_origin"]==676
    assert result["studies_still_not_documented"]==1
    assert result["effects_still_not_documented"]==4
    assert result["remaining_source_certified_fully_ebird_free"] is False
    assert result["no_new_temperature_effect_fit"] is True
    assert result["no_result_direction_based_source_selection"] is True
