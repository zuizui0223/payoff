import math
import pytest
from src.readiness_window_mismatch import (
    pairwise_readiness_mismatch,
    phase_error_after_readiness,
    readiness_window_marginal_effect,
    readiness_window_peak,
)

def test_phase_error_is_unchanged_before_readiness():
    assert phase_error_after_readiness(
        10,4,readiness_time=5,correction_rate=.2
    ) == pytest.approx(10)

def test_phase_error_decays_after_readiness():
    assert phase_error_after_readiness(
        10,7,readiness_time=5,correction_rate=.2
    ) == pytest.approx(10*math.exp(-.4))

def test_equal_readiness_times_never_create_mismatch():
    for t in [0,2,5,10]:
        assert pairwise_readiness_mismatch(
            10,t,readiness_time_1=3,readiness_time_2=3,correction_rate=.4
        ) == pytest.approx(0)

def test_readiness_window_peak_matches_closed_form():
    r=readiness_window_peak(
        10,readiness_time_1=2,readiness_time_2=5,correction_rate=.4
    )
    expected=10*(1-math.exp(-1.2))
    assert r.window_duration == pytest.approx(3)
    assert r.max_abs_mismatch == pytest.approx(expected)
    assert abs(r.mismatch_at_late_readiness) == pytest.approx(expected)

def test_peak_is_global_for_step_gate_model():
    r=readiness_window_peak(
        10,readiness_time_1=2,readiness_time_2=5,correction_rate=.4
    )
    vals=[
        abs(pairwise_readiness_mismatch(
            10,t,readiness_time_1=2,readiness_time_2=5,correction_rate=.4
        ))
        for t in [0,2,3,4,5,6,8,12]
    ]
    assert max(vals) == pytest.approx(r.max_abs_mismatch)

def test_readiness_asynchrony_has_no_effect_without_active_correction():
    r=readiness_window_peak(
        10,readiness_time_1=2,readiness_time_2=20,correction_rate=0
    )
    assert r.max_abs_mismatch == pytest.approx(0)

def test_long_readiness_window_saturates_at_initial_error():
    a=readiness_window_peak(
        10,readiness_time_1=0,readiness_time_2=1,correction_rate=1
    )
    b=readiness_window_peak(
        10,readiness_time_1=0,readiness_time_2=20,correction_rate=1
    )
    assert b.max_abs_mismatch > a.max_abs_mismatch
    assert b.max_abs_mismatch == pytest.approx(10,rel=1e-8)

def test_marginal_window_effect_declines_with_window():
    a=readiness_window_marginal_effect(10,1,correction_rate=.5)
    b=readiness_window_marginal_effect(10,4,correction_rate=.5)
    assert a > b > 0
