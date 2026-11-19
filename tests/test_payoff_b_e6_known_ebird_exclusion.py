"""Study-level source policy, never select by sign of the ecological effect."""
from pathlib import Path
import pytest
pd = pytest.importorskip("pandas", reason="Optional numerical dependency; dedicated E6 workflow tests with pandas")
pytest.importorskip("numpy")

from scripts.payoff_b_e6_known_ebird_exclusion import (
    SOURCE_STUDY_MARKER, read_verified_artifact, provenance_sensitivity
)


def test_non_original_artifact_fails_closed(tmp_path):
    wrong=tmp_path/"a.zip"
    wrong.write_bytes(b"not a valid official archive")
    with pytest.raises(ValueError,match="ZIP digest changed"):
        read_verified_artifact(wrong)


def test_source_pseudopanel_is_never_admitted():
    incomplete=pd.DataFrame({
        "Study":["fake","Hurlbert, A.H. & Liang, Z. (2012)"],
        "Species":["a","b"],
    })
    with pytest.raises(ValueError,match="Original E6 reconstruction columns missing"):
        provenance_sensitivity(incomplete)


def test_source_selection_requires_complete_previous_E6():
    d=pd.DataFrame({
        "Study":["Hurlbert, A.H. & Liang, Z. (2012)"],
        "Species":["X"],
        "Migration_distance":["short"],
        "Slope":[-1.],
        "SE":[0.5],
        "Response_variable":["first arrival"],
        "Temperature_location":["breeding"],
        "Arrival_location":["breeding"],
        "Data_source":["archive"],
        "Continent":["NA"]
    })
    with pytest.raises(ValueError,match="Original frozen E6 sample changed"):
        provenance_sensitivity(d)


def test_source_policy_marker_is_specific_to_published_study():
    assert SOURCE_STUDY_MARKER=="Hurlbert, A.H. & Liang, Z. (2012)"


def test_exact_prior_archive_when_explicitly_supplied(monkeypatch):
    import os
    p=os.environ.get("PAYOFF_E6_ARCHIVED_ARTIFACT_ZIP")
    if not p:
        pytest.skip("Original E6 GitHub artifact is not part of repository; workflow supplies it")
    r=provenance_sensitivity(read_verified_artifact(Path(p)))
    before=r["original_E6_before_source_policy_correction"]
    after=r["after_excluding_one_known_ebird_source"]
    assert before["n_effects"]==944
    assert after["n_effects"]==680
    assert before["studies"]==28
    assert after["studies"]==27
    assert after["species"]==279
    assert abs(before["estimate_days_per_C_long_minus_short"]-.4214763799092083)<1e-8
    assert abs(after["estimate_days_per_C_long_minus_short"]-.6083890673642456)<1e-8
    assert r["excluded_study"]["source_rows"]==264
    assert r["excluded_study"]["long_distance_rows"]==190
    assert r["excluded_study"]["short_distance_rows"]==74
    assert r["no_eBird_free_panel_certified"] is True
