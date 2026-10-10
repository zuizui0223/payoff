"""Generalization regression tests. Canonical V3 is NOT modified."""

from math import log, isclose
import pytest

from src.general_exponential_actionability import (
    general_exponential_timing, gross_actionable_value,
)


def calc(q_start=.75, cue_gain=.2, alpha=1., beta=1.,
         scale=1.6, base_loss=1.2):
    return general_exponential_timing(
        q_start=q_start, cue_gain=cue_gain,
        alpha=alpha, beta=beta,
        scale=scale, base_loss=base_loss,
    )


def test_original_canonical_threshold_case_remains_exact():
    x = calc()
    assert x.status == "INTERIOR_MAXIMUM"
    assert x.threshold_crossing_time == pytest.approx(0.)
    assert x.optimal_time == pytest.approx(log(2))
    assert x.optimal_cue_accuracy == pytest.approx(.85)


def test_initially_unusable_cue_adds_a_real_wait_to_cross_threshold():
    x = calc(q_start=.6, cue_gain=.35)
    assert x.threshold_crossing_time == pytest.approx(log(1.75))
    assert x.optimal_time == pytest.approx(log(1.75)+log(2))
    assert x.optimal_time > x.threshold_crossing_time > 0


def test_cue_initially_usable_moves_peak_earlier():
    x = calc(q_start=.8, cue_gain=.15)
    assert x.optimal_time == pytest.approx(log(1.5))
    assert x.optimal_time < log(2)


def test_cue_initially_good_enough_choose_immediately():
    x = calc(q_start=.95, cue_gain=.025)
    assert x.status == "IMMEDIATE_USE"
    assert x.optimal_time == 0
    assert x.maximal_actionable_value == pytest.approx(.32)


def test_infinitely_learned_cue_never_crosses_payoff_threshold():
    x = calc(q_start=.55, cue_gain=.15)
    assert x.status == "NEVER_ACTIONABLE"
    assert x.optimal_time is None
    assert x.threshold_crossing_time is None
    assert x.maximal_actionable_value == 0


def test_candidate_is_global_max_against_dense_objective_grid():
    cases = [
        (.75,.2,1.,1.,1.6,1.2),
        (.6,.35,1.,1.,1.6,1.2),
        (.8,.15,1.,1.,1.6,1.2),
        (.95,.025,1.,1.,1.6,1.2),
        (.55,.15,.5,.25,1.6,1.2),
        (.65,.3,2.,.4,1.6,1.2),
        (.7,.1,.7,3.,1.6,1.2),
    ]
    for q0,d,a,b,s,B in cases:
        outcome = calc(q0,d,a,b,s,B)
        if outcome.status == "NEVER_ACTIONABLE":
            continue
        tstar = outcome.optimal_time
        assert tstar is not None
        kw = dict(q_start=q0,cue_gain=d,alpha=a,beta=b,scale=s,base_loss=B)
        fstar = gross_actionable_value(tstar,**kw)
        max_grid = max(gross_actionable_value(i*.025,**kw) for i in range(1601))
        assert fstar >= max_grid - 1e-9
        assert fstar == pytest.approx(outcome.maximal_actionable_value)


def test_faster_lost_actionability_never_moves_optimum_later():
    slow=calc(q_start=.6,cue_gain=.35,beta=.2)
    fast=calc(q_start=.6,cue_gain=.35,beta=2.)
    assert fast.optimal_time < slow.optimal_time


def test_cue_gain_is_not_a_free_parameter_when_range_exceeds_one():
    with pytest.raises(ValueError):
        calc(q_start=.8,cue_gain=.3)
    with pytest.raises(ValueError):
        calc(beta=0)
    with pytest.raises(ValueError):
        calc(scale=0)
    with pytest.raises(ValueError):
        calc(q_start=float("nan"))
    with pytest.raises(ValueError):
        calc(q_start=.2, cue_gain=.7)
    with pytest.raises(ValueError):
        calc(scale=2, base_loss=.8)
    with pytest.raises(ValueError):
        gross_actionable_value(-.1,q_start=.75,cue_gain=.2,alpha=1,
                               beta=1,scale=1.6,base_loss=1.2)


def test_general_optimum_is_not_canonical_when_initial_value_nonzero():
    a = calc(q_start=.8,cue_gain=.15)
    assert not isclose(a.optimal_time, log(2), abs_tol=1e-4)
    b = calc(q_start=.6,cue_gain=.35)
    assert not isclose(b.optimal_time, log(2), abs_tol=1e-4)


def test_never_actionable_even_as_maximum_limit_equals_threshold():
    x=calc(q_start=.6,cue_gain=.15)
    assert x.status=="NEVER_ACTIONABLE"
