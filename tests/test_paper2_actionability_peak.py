"""Paper 2 exact mathematical assumptions and counterexamples, no natural re-fit."""
import math

import pytest

from src.paper2_actionability_peak import (
    ActionabilityPeak, explicit_nonzero_wait_cost_stationarity,
    symmetric_threshold_peak, two_actor_mismatch,
)


def test_declared_symmetric_witness_and_q_at_the_peak():
    m=ActionabilityPeak(q0=.5,dq=.5,alpha=1,beta=1,
                        loss_scale=2,baseline_loss=1)
    r=m.optimum()
    assert r["regime"]=="INTERIOR_CHECKPOINT"
    assert r["threshold_normalization"]
    assert r["optimal_wait_time"]==pytest.approx(math.log(2))
    assert symmetric_threshold_peak(1,1)==pytest.approx(r["optimal_wait_time"])
    assert m.cue_accuracy(r["optimal_wait_time"])==pytest.approx(.75)
    assert m.derivative(r["optimal_wait_time"])==pytest.approx(0,abs=1e-12)


def test_general_parameters_disprove_threshold_only_claim():
    # q starts well above the action boundary. The original ln(2) formula
    # would choose too late; the true global optimum is immediate.
    m=ActionabilityPeak(q0=.6,dq=.3,alpha=1,beta=1,
                        loss_scale=10,baseline_loss=3)
    r=m.optimum()
    assert r["regime"]=="COMMIT_IMMEDIATELY"
    assert r["optimal_wait_time"]==pytest.approx(0)
    assert not r["threshold_normalization"]
    assert m.net(0)>m.net(math.log(2))


def test_interior_peak_in_general_depends_on_baseline_information():
    m=ActionabilityPeak(q0=.55,dq=.45,alpha=1,beta=1,
                        loss_scale=10,baseline_loss=5)
    r=m.optimum()
    expected=math.log(1.8)
    assert r["regime"]=="INTERIOR_CHECKPOINT"
    assert not r["threshold_normalization"]
    assert r["optimal_wait_time"]==pytest.approx(expected)
    assert r["optimal_wait_time"]!=pytest.approx(math.log(2))
    assert m.derivative(expected)==pytest.approx(0,abs=1e-12)


def test_no_positive_gross_payoff_blocks_witness_regime():
    m=ActionabilityPeak(q0=.5,dq=.1,alpha=1,beta=1,
                        loss_scale=4,baseline_loss=3)
    r=m.optimum()
    assert r["regime"]=="NO_POSITIVE_INFORMATION_RETURN"
    assert r["optimal_wait_time"] is None
    assert r["optimal_net_value"]==0
    assert all(m.net(k)<0 for k in (0,1,5,20))


def test_zero_information_improvement_cannot_induce_waiting():
    m=ActionabilityPeak(q0=.7,dq=0,alpha=.5,beta=2,
                        loss_scale=10,baseline_loss=3)
    assert m.optimum()["optimal_wait_time"]==0


def test_optimum_beats_all_finite_candidate_waits_under_many_parameters():
    for q0 in (.5,.6,.75):
        for dq in (0,.05,.15):
            if q0+dq>1:
                continue
            for base in (2.0,4.0,6.0):
                for alpha,beta in ((.5,1),(1,1),(3,.35)):
                    m=ActionabilityPeak(q0=q0,dq=dq,alpha=alpha,beta=beta,
                                        loss_scale=10,baseline_loss=base)
                    result=m.optimum()
                    claimed=result["optimal_net_value"]
                    grid=max([0.0]+[m.net(k/12) for k in range(0,241)])
                    assert claimed+1e-11>=grid
                    if result["optimal_wait_time"] is not None:
                        assert m.net(result["optimal_wait_time"])==pytest.approx(claimed)


def test_first_order_condition_with_positive_wait_cost_is_not_free_optimum():
    m=ActionabilityPeak(q0=.5,dq=.5,alpha=1,beta=1,
                        loss_scale=2,baseline_loss=1)
    peak=m.optimum()["optimal_wait_time"]
    assert explicit_nonzero_wait_cost_stationarity(peak,m,0)==pytest.approx(0,abs=1e-12)
    assert explicit_nonzero_wait_cost_stationarity(peak,m,.1)==pytest.approx(-.1)


def test_retention_decomposition_for_initially_different_and_equal_actors():
    for n in range(7):
        for e1,e2 in ((.6,.6),(-.3,.8),(-2,3),(0,0)):
            for a,b in ((.4,.7),(-.2,.8),(1.,1.)):
                got=two_actor_mismatch(e1,e2,a,b,n)
                assert got["direct"]==pytest.approx(got["decomposed"])
                assert got["direct"]==pytest.approx(
                    got["inherited"]+got["controller_asymmetry"]
                )
                if e1==e2:
                    assert got["inherited"]==pytest.approx(0)


def test_reject_outside_domain_and_nonintegral_steps():
    with pytest.raises(ValueError):
        ActionabilityPeak(.5,.7,1,1,2,1)
    with pytest.raises(ValueError):
        ActionabilityPeak(.5,.3,-1,1,2,1)
    with pytest.raises(ValueError):
        two_actor_mismatch(1,1,.5,.5,2.0)
