import math
from datetime import datetime, timezone

import numpy as np
import pytest

from analysis.movement_phenology.wigeon_hmm import (
    INITIAL,
    STATE_NAMES,
    emission_log_prob,
    movement_streams,
    solar_time_hours,
    transition_matrix,
    viterbi_published,
)


def test_published_state_contract():
    assert STATE_NAMES == ("rest", "non-flight", "local", "migratory")
    assert len(INITIAL) == 4
    assert INITIAL.sum() == pytest.approx(1.0)


def test_transition_rows_are_probabilities_at_multiple_solar_times():
    for h in (0, 4, 8, 12, 16, 20, 23.5):
        m = transition_matrix(h)
        assert m.shape == (4, 4)
        assert np.all(m > 0)
        assert np.allclose(m.sum(axis=1), 1.0)


def test_migratory_emission_favors_long_straight_step():
    # State 4 fitted mean sqrt(step) is ~5.94 and angle mean is near zero.
    lp = emission_log_prob(5.94, 0.0)
    assert int(np.argmax(lp)) == 3


def test_rest_emission_favors_tiny_step():
    lp = emission_log_prob(0.13, math.pi)
    assert int(np.argmax(lp)) in (0, 1)


def test_movement_stream_alignment_matches_prepdata_contract():
    # Straight eastward sequence: step on rows 0/1, final step NA;
    # angle on middle row, first/final angle NA.
    step, ang = movement_streams([0, 0.1, 0.2], [0, 0, 0])
    assert np.isfinite(step[0])
    assert np.isfinite(step[1])
    assert np.isnan(step[2])
    assert np.isnan(ang[0])
    assert ang[1] == pytest.approx(0.0, abs=1e-8)
    assert np.isnan(ang[2])


def test_solar_time_is_close_to_noon_at_greenwich_utc_noon():
    t = datetime(2020, 3, 20, 12, 0, tzinfo=timezone.utc)
    h = solar_time_hours(t, 0.0)
    assert 11.5 < h < 12.5


def test_viterbi_identifies_long_straight_block_as_migratory():
    n = 20
    step = np.full(n, 5.94)
    angle = np.zeros(n)
    solar = np.full(n, 12.0)
    states = viterbi_published(step, angle, solar)
    assert np.mean(states == 4) > 0.8
