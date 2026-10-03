import math
import pytest
from src.usable_action_window import (
    multi_prerequisite_peak,
    multi_prerequisite_value,
    usable_action_gate,
    usable_window_peak,
)

def test_usable_gate_is_zero_before_readiness_and_at_late_limit():
    assert usable_action_gate(0,readiness_rate=1,expiry_rate=.5) == pytest.approx(0)
    assert usable_action_gate(100,readiness_rate=1,expiry_rate=.5) < 1e-20

def test_usable_window_peak_closed_form_beats_neighbors():
    r=usable_window_peak(readiness_rate=1.2,expiry_rate=.4)
    assert r.peak_time == pytest.approx(math.log(1+1.2/.4)/1.2)
    left=usable_action_gate(r.peak_time-.1,readiness_rate=1.2,expiry_rate=.4)
    right=usable_action_gate(r.peak_time+.1,readiness_rate=1.2,expiry_rate=.4)
    assert r.usable_gate_at_peak > left
    assert r.usable_gate_at_peak > right

def test_faster_expiry_moves_window_peak_earlier():
    slow=usable_window_peak(readiness_rate=1,expiry_rate=.2)
    fast=usable_window_peak(readiness_rate=1,expiry_rate=2)
    assert fast.peak_time < slow.peak_time

def test_faster_readiness_moves_usable_peak_earlier():
    slow=usable_window_peak(readiness_rate=.3,expiry_rate=.5)
    fast=usable_window_peak(readiness_rate=2,expiry_rate=.5)
    assert fast.peak_time < slow.peak_time

def test_multi_prerequisite_peak_closed_form():
    r=multi_prerequisite_peak(opening_rate=1,expiry_rate=.5,prerequisite_count=2)
    assert r.peak_time == pytest.approx(math.log(1+2/.5))
    assert r.opening_level_at_peak == pytest.approx(2/(.5+2))
    left=multi_prerequisite_value(
        r.peak_time-.1,opening_rate=1,expiry_rate=.5,prerequisite_count=2
    )
    right=multi_prerequisite_value(
        r.peak_time+.1,opening_rate=1,expiry_rate=.5,prerequisite_count=2
    )
    assert r.objective_at_peak > left
    assert r.objective_at_peak > right

def test_more_prerequisites_shift_equal_rate_optimum_later():
    one=multi_prerequisite_peak(opening_rate=1,expiry_rate=.5,prerequisite_count=1)
    three=multi_prerequisite_peak(opening_rate=1,expiry_rate=.5,prerequisite_count=3)
    assert three.peak_time > one.peak_time
