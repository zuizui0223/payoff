import pytest

from analysis.movement_phenology.tgs import thermal_growing_season_onset


def test_exact_published_cumulative_minimum_rule():
    temp = [0.0] * 60 + [10.0] * 60
    fit = thermal_growing_season_onset(temp)
    assert fit.onset_day == 60


def test_rule_differs_from_first_single_day_above_five():
    temp = [0.0] * 20 + [6.0] + [0.0] * 19 + [10.0] * 60
    fit = thermal_growing_season_onset(temp)
    assert fit.onset_day > 21


def test_custom_day_labels_are_preserved():
    temp = [1.0] * 50 + [9.0] * 50
    doy = list(range(32, 132))
    fit = thermal_growing_season_onset(temp, doy)
    assert fit.onset_day == 81


def test_fail_closed_on_bad_series():
    with pytest.raises(ValueError):
        thermal_growing_season_onset([1, 2, 3])
    with pytest.raises(ValueError):
        thermal_growing_season_onset([1.0] * 40 + [float("nan")])
