import numpy as np
import pytest

from analysis.movement_phenology.tgs import thermal_growing_season_onset


def test_exact_published_cumulative_minimum_rule():
    temp = np.r_[np.full(60, 0.0), np.full(60, 10.0)]
    fit = thermal_growing_season_onset(temp)
    # cumulative (T-5) declines through day 60 and rises afterward
    assert fit.onset_day == 60


def test_rule_differs_from_first_single_day_above_five():
    temp = np.r_[np.full(20, 0.0), [6.0], np.full(19, 0.0), np.full(60, 10.0)]
    fit = thermal_growing_season_onset(temp)
    # A lone warm day does not define onset; cumulative deficit keeps falling.
    assert fit.onset_day > 21


def test_custom_day_labels_are_preserved():
    temp = np.r_[np.full(50, 1.0), np.full(50, 9.0)]
    doy = np.arange(32, 132)
    fit = thermal_growing_season_onset(temp, doy)
    assert fit.onset_day == 81


def test_fail_closed_on_bad_series():
    with pytest.raises(ValueError):
        thermal_growing_season_onset([1, 2, 3])
    with pytest.raises(ValueError):
        thermal_growing_season_onset([1.0] * 40 + [float("nan")])
