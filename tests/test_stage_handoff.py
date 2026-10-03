import pytest

from src.stage_handoff import (
    downstream_timing_slope,
    handoff_from_interval_slope,
    interval_slope_from_retention,
)


def test_no_buffering_when_interval_is_independent_of_entry():
    r=handoff_from_interval_slope(0.0)
    assert r.timing_retention == pytest.approx(1.0)
    assert r.compensation_fraction == pytest.approx(0.0)
    assert r.regime == "no_buffering"


def test_partial_buffering():
    r=handoff_from_interval_slope(-0.53)
    assert r.timing_retention == pytest.approx(0.47)
    assert r.compensation_fraction == pytest.approx(0.53)
    assert r.regime == "partial_buffering"


def test_complete_buffering():
    r=handoff_from_interval_slope(-1.0)
    assert r.timing_retention == pytest.approx(0.0)
    assert r.regime == "complete_buffering"


def test_overcompensation():
    r=handoff_from_interval_slope(-1.2)
    assert r.timing_retention == pytest.approx(-0.2)
    assert r.regime == "overcompensation"


def test_amplification():
    r=handoff_from_interval_slope(0.25)
    assert r.timing_retention == pytest.approx(1.25)
    assert r.regime == "amplification"


def test_inverse_identity():
    for eta in (-0.2,0.0,0.47,1.0,1.3):
        b=interval_slope_from_retention(eta)
        assert downstream_timing_slope(b) == pytest.approx(eta)
