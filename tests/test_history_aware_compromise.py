"""Synthetic mathematical checks, not Wurmbea data or evolutionary observations."""
import importlib
import importlib.util
from fractions import Fraction
from itertools import product
from math import isclose

import pytest


def api():
    name = 'src.history_aware_compromise'
    assert importlib.util.find_spec(name) is not None, 'History-aware audit is not implemented'
    return importlib.import_module(name)


def enumerated_moments(q, rho, memory):
    """Independent exact rational enumeration of latent AND observed sequences."""
    n = memory + 1
    weights = {}
    totals = {}
    for states in product((0, 1), repeat=n):
        p = Fraction(1, 2)
        for left, right in zip(states, states[1:]):
            p *= rho if left != right else 1-rho
        for cues in product((0, 1), repeat=n):
            joint = p
            for state, cue in zip(states, cues):
                joint *= q if state == cue else 1-q
            weights[cues] = weights.get(cues, Fraction(0)) + joint
            for word, state in ((cues[:-1], states[-2]), (cues[1:], states[-1])):
                # Each marginal is represented twice, which cancels in the ratio.
                key = (word, state)
                totals[key] = totals.get(key, Fraction(0)) + joint
    means = {}
    for word in product((0, 1), repeat=memory):
        p0, p1 = totals.get((word, 0), 0), totals.get((word, 1), 0)
        means[word] = (p1-p0)/(p0+p1) if p0+p1 else Fraction(0)
    r = sum(p * means[word[1:]]**2 for word, p in weights.items())
    variation = sum(p*abs(means[word[1:]]-means[word[:-1]]) for word,p in weights.items())
    return float(r), float(variation)


def test_one_cue_reproduces_original_witness():
    m = api()
    for rho, loss in ((0.1, 3.590316), (0.9, 3.871916)):
        r = m.memory_policy(m.Parameters(rho=rho), memory=1)
        assert isclose(r['expected_loss'], loss, abs_tol=2e-12)
        assert isclose(r['posterior_second_moment'], .64, abs_tol=2e-12)
        assert r['memory_length'] == 1


@pytest.mark.parametrize('q,rho,n', [(Fraction(9,10),Fraction(1,10),2),
    (Fraction(9,10),Fraction(9,10),3), (Fraction(3,5),Fraction(1,2),2)])
def test_joint_windows_against_independent_fraction_arithmetic(q,rho,n):
    m = api()
    expected_r, expected_variation = enumerated_moments(q,rho,n)
    actual = m.window_moments(float(q),float(rho),n)
    assert isclose(actual['probability_mass'], 1, abs_tol=5e-13)
    assert isclose(actual['posterior_second_moment'], expected_r, abs_tol=5e-13)
    assert isclose(actual['posterior_total_variation'], expected_variation, abs_tol=5e-13)


def test_iid_environment_cannot_gain_prediction_from_previous_cues():
    m = api()
    for n in (1,2,5):
        out = m.memory_policy(m.Parameters(rho=.5), n)
        assert isclose(out['posterior_second_moment'], .64, abs_tol=1e-12)
        assert isclose(out['expected_loss'], 3.7475, abs_tol=1e-12)


def test_perfect_cue_zero_switching_cost_reaches_simultaneous_floor():
    m = api()
    p = m.Parameters(q=1, running_cost=0, switch_cost=0)
    for n in (1,2,4):
        assert isclose(m.memory_policy(p,n)['expected_loss'],p.conflict_floor,abs_tol=1e-12)


def test_finite_memory_cost_is_explicit_not_free_by_default_claim():
    m = api()
    p = m.Parameters()
    a = m.memory_policy(p,2,memory_cost=0)
    b = m.memory_policy(p,2,memory_cost=.123)
    assert isclose(b['expected_loss']-a['expected_loss'],.123,abs_tol=1e-12)
    assert a['optimized_only_within_posterior_amplitude_class'] is True


def test_pair_bound_holds_pointwise_for_arbitrary_actions():
    m = api()
    for c in (0,.1,1,2,10):
        p = m.Parameters(switch_cost=c)
        w = p.a+p.b
        z0 = p.b*p.delta/w
        z1 = p.a*p.delta/w
        lower = m.pairwise_switch_floor(p)
        for x,y in product((-.7,0,.5,1,1.5,2,2.7), repeat=2):
            loss = .5*w*((x-z0)**2+(y-z1)**2)+c*abs(x-y)
            assert loss+1e-12 >= lower
        amount = min(c/w,p.optimum_distance/2)
        x,y=z0+amount,z1-amount
        achieved = .5*w*((x-z0)**2+(y-z1)**2)+c*abs(x-y)
        assert isclose(achieved,lower,abs_tol=1e-12)


def test_bound_respects_shared_architecture_with_no_plastic_running_cost():
    m = api()
    p=m.Parameters(running_cost=20)
    bounds=m.strategy_bounds(p,memories=(1,2))
    assert bounds['nonmodule_lower_bound'] <= p.shared_loss
    assert isclose(bounds['nonmodule_upper_bound'],p.shared_loss,abs_tol=1e-12)


def test_bound_is_below_every_computed_policy():
    m=api()
    for rho,q,c in product((0,.1,.5,.9,1),(.5,.8,1),(0,1,10)):
        p=m.Parameters(rho=rho,q=q,switch_cost=c)
        out=m.strategy_bounds(p,memories=(1,2,3))
        assert out['nonmodule_lower_bound']<=out['nonmodule_upper_bound']+2e-12


def test_lower_cost_module_switch_is_certified_without_memory_restriction():
    m=api()
    slow=m.strategy_bounds(m.Parameters(rho=.1,module_cost=3.6),memories=(1,2,3))
    fast=m.strategy_bounds(m.Parameters(rho=.9,module_cost=3.6),memories=(1,2,3))
    assert slow['classification']=='NONMODULE_FEASIBLE_POLICY_BEATS_MODULE'
    assert fast['classification']=='MODULE_BEATS_ALL_SHARED_COORDINATE_POLICIES'
    assert isclose(fast['nonmodule_lower_bound'],3.725,abs_tol=1e-12)
    assert fast['minimum_module_advantage']>.124999999


def test_boundary_and_uninformative_cases_are_not_false_certificates():
    m=api()
    p=m.Parameters(a=2,b=2,delta=2,q=.5,running_cost=0,module_cost=4)
    out=m.strategy_bounds(p,memories=(1,2))
    assert isclose(out['nonmodule_lower_bound'],4,abs_tol=1e-12)
    assert out['classification']=='UNRESOLVED_OR_TIED'
    assert m.memory_policy(p,2)['attenuation']==0


@pytest.mark.parametrize('kwargs',[{'q':.4},{'rho':1.01},{'a':0},{'b':0},
    {'a':1,'b':2},{'running_cost':-1},{'switch_cost':float('nan')},{'delta':float('inf')}])
def test_invalid_inputs_raise(kwargs):
    with pytest.raises(ValueError): api().Parameters(**kwargs)


@pytest.mark.parametrize('n',[0,-1,True,1.5,13])
def test_invalid_memory_budgets_raise(n):
    with pytest.raises(ValueError): api().window_moments(.9,.1,n)


def test_optimized_window_policy_contains_memoryless_and_posterior_rules():
    pytest.importorskip('scipy')
    m=api()
    assert hasattr(m,'optimal_window_policy'), 'Cue-history mapping optimizer missing'
    p=m.Parameters(rho=.9)
    old=m.memory_policy(p,1)['expected_loss']
    previous=old
    for n in (1,2,3,4):
        solution=m.optimal_window_policy(p,n)
        assert solution['primal_loss'] <= previous+1e-8
        assert solution['primal_loss'] <= m.memory_policy(p,n)['expected_loss']+1e-8
        assert solution['primal_dual_gap']<2e-8
        assert solution['dual_lower_bound_on_window_class']<=solution['primal_loss']+1e-11
        previous=solution['primal_loss']


def test_optimized_window_one_cue_matches_analytic_result():
    pytest.importorskip('scipy')
    m=api()
    assert hasattr(m,'optimal_window_policy'), 'Cue-history mapping optimizer missing'
    for rho in (.1,.5,.9):
        p=m.Parameters(rho=rho)
        x=m.optimal_window_policy(p,1)
        assert isclose(x['primal_loss'],m.memory_policy(p,1)['expected_loss'],abs_tol=1e-8)


def test_memory_upper_bounds_do_not_exceed_global_future_oracle_floor():
    pytest.importorskip('scipy')
    m=api()
    assert hasattr(m,'optimal_window_policy'), 'Cue-history mapping optimizer missing'
    for rho in (.1,.5,.9):
        p=m.Parameters(rho=rho)
        solution=m.optimal_window_policy(p,3)
        lower=p.conflict_floor+p.running_cost+rho*m.pairwise_switch_floor(p)
        assert solution['primal_loss']>=lower-1e-9
        assert solution['certificate_scope']=='FINITE_CUE_WINDOW_ONLY_NOT_ALL_HISTORY'


def test_two_cues_reverse_apparent_module_advantage_with_positive_memory_budget():
    m=api()
    p=m.Parameters(rho=.1,module_cost=3.55)
    no_memory=m.memory_policy(p,1)['expected_loss']
    two_cues=m.memory_policy(p,2)['expected_loss']
    assert two_cues < p.module_cost < no_memory
    assert p.module_cost-two_cues>.05
    assert m.memory_policy(p,2,memory_cost=.04)['expected_loss']<p.module_cost


def test_predictable_environment_endpoints_have_policy_class_free_optima():
    m=api()
    assert hasattr(m,'predictable_endpoint_optimum'), 'Endpoint theorem missing'
    for q in (.51,.9,1):
        low=m.predictable_endpoint_optimum(m.Parameters(q=q,rho=0))
        high=m.predictable_endpoint_optimum(m.Parameters(q=q,rho=1))
        assert isclose(low['optimal_nonmodule_loss'],3.05,abs_tol=1e-12)
        assert isclose(high['optimal_nonmodule_loss'],3.8,abs_tol=1e-12)
        assert high['module_comparison']=='TIE'
    none=m.predictable_endpoint_optimum(m.Parameters(q=.5,rho=1))
    assert isclose(none['optimal_nonmodule_loss'],4,abs_tol=1e-12)
    with pytest.raises(ValueError):
        m.predictable_endpoint_optimum(m.Parameters(rho=.9))
