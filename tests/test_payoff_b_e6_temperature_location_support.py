"""Synthetic source-design tests only; no original Usui slope is modelled."""
import pytest
pd = pytest.importorskip("pandas", reason="Optional numerical dependency; dedicated E6 workflow tests with pandas")
pytest.importorskip("numpy")

from scripts.payoff_b_e6_temperature_location_support import (
    design_support, exact_e6_selection
)


def original_shape_fixture():
    rows=[]
    for study in ["A", "B", "C"]:
        for location in ["source_site", "destination_site"]:
            for distance in ["short","long"]:
                rows.append({
                    "Study":study,"Species":f"species_{study}_{location}_{distance}",
                    "Migration_distance":distance,
                    "Temperature_location":location,
                })
    return pd.DataFrame(rows)


def test_crossed_studies_are_counted_as_studies_not_rows():
    out=design_support(original_shape_fixture())
    assert out["frozen_bird_E6_rows"] == 12
    assert out["frozen_bird_E6_studies"] == 3
    assert out["frozen_bird_E6_species"] == 12
    assert out["n_level_pairs_meeting_5_fully_crossed_studies"] == 0
    one=out["all_unordered_location_level_pairs"][0]
    assert one["n_studies_with_all_four_cells"] == 3
    assert one["candidate_2x2_within_study_requirement_n5"] is False
    assert out["no_new_biological_interaction_fitted"] is True


def test_unbalanced_study_does_not_count_as_full_cross():
    d=original_shape_fixture()
    d=d.loc[~((d.Study=="C") & (d.Temperature_location=="source_site")
              & (d.Migration_distance=="long"))]
    out=design_support(d)
    assert out["all_unordered_location_level_pairs"][0][
        "n_studies_with_all_four_cells"] == 2
    assert out["frozen_bird_E6_rows"] == 11


def test_no_outcome_columns_required_in_support():
    d=original_shape_fixture()
    assert not {"Slope","SE"}.intersection(d.columns)
    assert design_support(d)["no_animal_cue_use_observed"] is True


def test_exact_original_E6_selection_rejects_short_changed_source():
    d=original_shape_fixture()
    d["Predictor"]="temperature"
    d["Slope"]=-1.
    d["SE"]=0.5
    with pytest.raises(ValueError,match="selection drift"):
        exact_e6_selection(d)


def test_missing_source_code_raises():
    d=original_shape_fixture().drop(columns=["Temperature_location"])
    with pytest.raises(ValueError,match="Missing design-only"):
        design_support(d)


def test_unregistered_distance_raises():
    d=original_shape_fixture()
    d.loc[d.index[0], "Migration_distance"]="transient"
    with pytest.raises(ValueError,match="short/long"):
        design_support(d)
