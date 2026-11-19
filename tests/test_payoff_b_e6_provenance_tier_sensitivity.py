"""Full source provenance tier check is executed only with verified E6 artifact."""
from pathlib import Path
import os
import pytest

pytest.importorskip("pandas")
pytest.importorskip("numpy")
from scripts.payoff_b_e6_source_origin_inventory import SOURCES,inventory
from scripts.payoff_b_e6_known_ebird_exclusion import read_verified_artifact
from scripts.payoff_b_e6_provenance_tier_sensitivity import (
    provenance_tier_sensitivity,
    LOWER_SOURCE_EVIDENCE_LEVEL,
)


def test_predeclared_source_lists_have_nonoverlapping_metadata():
    assert len(SOURCES)==26
    assert len(set(item[0] for item in SOURCES))==26
    assert sum(item[1] for item in SOURCES)==676
    assert set(["Rubolini, D.","Ahola, M."]).issubset(set(x[0] for x in SOURCES))


def test_original_source_reconstruction_produces_nested_qualifying_tiers():
    f=os.environ.get("PAYOFF_E6_ARCHIVED_ARTIFACT_ZIP")
    if not f:
        pytest.skip("Original historical E6 artifact provided by dedicated workflow")
    original=read_verified_artifact(Path(f))
    source=inventory(original)
    assert source["remaining_after_forced_exclusion_effects"]==680
    assert source["effects_with_published_alternative_primary_observation_origin"]==676
    assert source["studies_with_published_alternative_primary_observation_origin"]==26
    assert source["studies_still_not_documented"]==1
    result=provenance_tier_sensitivity(original)
    c=result["comparisons"]
    assert c["original_published_E6_provenance_only"]["n_effects"]==944
    assert c["verified_known_eBird_study_removed_680"]["n_effects"]==680
    assert c["published_local_source_described_676"]["n_effects"]==676
    assert c["published_local_source_described_676"]["studies"]==26
    assert c["more_explicit_observation_programme_670"]["n_effects"]==670
    assert c["more_explicit_observation_programme_670"]["studies"]==24
    assert c["published_local_source_described_676"]["estimate_days_per_C_long_minus_short"]==pytest.approx(
        0.6018495000866944,abs=1e-7)
    assert c["more_explicit_observation_programme_670"]["estimate_days_per_C_long_minus_short"]==pytest.approx(
        0.6238827646228353,abs=1e-7)
    assert result["no_claim_of_fully_eBird_free_panel"] is True
    assert result["no_new_independent_biological_effect"] is True
    assert result["source_selection_based_on_coefficient_direction"] is False
