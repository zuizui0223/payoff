"""Behavioral safeguards for the original-data within-animal comparison."""

import importlib
import random

import pytest


def api():
    return importlib.import_module("scripts.payoff_b_ortega_within_animal")


def test_missing_stopover_is_not_zero_and_true_zero_is_retained():
    phase = [
        {"id_yr": "A_2011", "year": "2011", "DFP_Start": "1"},
        {"id_yr": "A_2012", "year": "2012", "DFP_Start": "2"},
        {"id_yr": "B_2011", "year": "2011", "DFP_Start": "3"},
        {"id_yr": "B_2012", "year": "2012", "DFP_Start": "4"},
    ]
    acts = [
        {"id_yr": "A_2011", "stopover.day": "0"},
        {"id_yr": "A_2012", "stopover.day": "NA"},
        {"id_yr": "B_2011", "stopover.day": "0"},
        {"id_yr": "B_2012", "stopover.day": "5"},
    ]
    rows = api().join_records(phase, acts)
    assert [r["stopover"] for r in rows] == [0.0, None, 0.0, 5.0]
    panel = api().repeated_panel(rows)
    assert len(panel) == 2
    assert [r["stopover"] for r in panel] == [0.0, 5.0]
    assert {r["animal"] for r in panel} == {"B"}


@pytest.mark.parametrize("duplicate_side", ["phase", "actuator"])
def test_duplicate_original_join_keys_are_rejected(duplicate_side):
    phase = [{"id_yr": "A_2011", "year": "2011", "DFP_Start": "1"}]
    acts = [{"id_yr": "A_2011", "stopover.day": "2"}]
    if duplicate_side == "phase":
        phase += phase.copy()
    else:
        acts += acts.copy()
    with pytest.raises(ValueError, match="duplicate"):
        api().join_records(phase, acts)


def test_equal_row_counts_do_not_hide_unmatched_original_ids():
    phase = [{"id_yr": "A_2011", "year": "2011", "DFP_Start": "1"}]
    acts = [{"id_yr": "B_2011", "stopover.day": "2"}]
    with pytest.raises(ValueError, match="keys do not match"):
        api().join_records(phase, acts)


def unbalanced_rows():
    # y = animal intercept (10, 30, 20) + year effect (-2, 5, 1) - 0.5*x.
    values = [
        ("A", 1, 1.0, 7.5), ("A", 2, 4.0, 13.0),
        ("A", 3, 2.0, 10.0), ("B", 1, 5.0, 25.5),
        ("B", 2, 3.0, 33.5), ("C", 2, 2.0, 24.0),
        ("C", 3, 6.0, 18.0),
    ]
    return [dict(animal=a, year=t, start=x, stopover=y) for a, t, x, y in values]


def test_exact_twfe_recovers_known_slope_in_unbalanced_panel():
    fitted = api().fit_twfe(unbalanced_rows())
    assert fitted["beta"] == pytest.approx(-0.5, abs=1e-12)
    assert fitted["nuisance_rank"] == 5
    assert fitted["residual_df"] == 1


def test_animal_and_year_confounded_exposure_is_not_fitted():
    rows = unbalanced_rows()
    for row in rows:
        row["start"] = {"A": 0, "B": 10, "C": 20}[row["animal"]] + row["year"]
    with pytest.raises(ValueError, match="no identifying"):
        api().fit_twfe(rows)


def test_bootstrap_keeps_histories_and_relabels_duplicate_animal_draws():
    rows = [
        dict(animal="A", year=1, start=1, stopover=4),
        dict(animal="A", year=2, start=2, stopover=3),
        dict(animal="B", year=1, start=10, stopover=8),
    ]
    sampled = api().resample_animals(rows, random.Random(1))
    assert len(sampled) == 4  # The fixed RNG draws the two-year A history twice.
    labels = {r["animal"] for r in sampled}
    assert len(labels) == 2
    for label in labels:
        assert sorted(r["year"] for r in sampled if r["animal"] == label) == [1, 2]
        assert sorted(r["start"] for r in sampled if r["animal"] == label) == [1, 2]
    assert [r["animal"] for r in rows] == ["A", "A", "B"]


def test_source_checksum_is_checked_before_workbook_parsing(tmp_path):
    source = tmp_path / "wrong.xlsx"
    source.write_bytes(b"not the authenticated original data")
    with pytest.raises(ValueError, match="SHA256"):
        api().load_source(source)


def test_disconnected_fixed_effects_identify_slope_without_cross_component_levels():
    values = [
        ("A", 1, 1, 119.5), ("A", 2, 3, 218.5),
        ("B", 1, 4, 148), ("B", 2, 2, 249),
        ("C", 3, 5, 507.5), ("C", 4, 8, 516),
        ("D", 3, 7, 606.5), ("D", 4, 6, 617),
    ]
    rows = [dict(animal=a, year=t, start=x, stopover=y) for a, t, x, y in values]
    contract = {"support_before_coefficient": {
        "minimum_repeated_animals": 2, "minimum_years": 2,
        "minimum_residual_degrees_of_freedom": 1,
        "minimum_residual_exposure_rms_days": 0.1,
        "require_one_connected_animal_year_component": False,
    }}
    support = api().support_summary(rows, contract)
    assert support["primary_panel"]["connected_components"] == 2
    assert support["status"] == "PASS"
    assert api().fit_twfe(rows)["beta"] == pytest.approx(-0.5, abs=1e-12)
    shifted = [{**r, "start": r["start"] + (300 if r["year"] > 2 else 0),
                "stopover": r["stopover"] + (1000 if r["year"] > 2 else 0)} for r in rows]
    assert api().fit_twfe(shifted)["beta"] == pytest.approx(-0.5, abs=1e-12)
    contract["support_before_coefficient"]["require_one_connected_animal_year_component"] = True
    assert api().support_summary(rows, contract)["status"] == "SUPPORT_NOT_MET"
