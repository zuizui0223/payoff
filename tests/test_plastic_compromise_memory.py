"""Independent 64-path validation of a two-cue-memory architecture comparison."""
from itertools import product
from math import isclose
import importlib.util
from pathlib import Path
import random
import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "src/plastic_compromise_memory.py"


def api():
    assert MODULE.exists(), "two-cue optimizer has not been implemented"
    spec = importlib.util.spec_from_file_location("memory_audit", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def params(rho=.9, K=3.8, q=.9):
    return dict(a=3., b=1., delta=2., q=q, rho=rho,
                plastic_running_cost=.05, plastic_switch_cost=1., module_cost=K)


def enumerate_loss(p, same, different):
    """Enumerate 3 true states and 3 cues, not analytical joint moments."""
    a,b,D,q,rho=(p[k] for k in ('a','b','delta','q','rho'))
    d=(a-b)*D/(a+b)
    def phenotype(old, new):
        gain = same if old == new else different
        return D/2 + d/2 * gain * (2*new-1)
    loss=0.; mass=0.
    for e0,e1,e2,z0,z1,z2 in product((0,1), repeat=6):
        w=.5
        for last, current in ((e0,e1),(e1,e2)):
            w*=rho if last!=current else 1-rho
        for e,z in ((e0,z0),(e1,z1),(e2,z2)):
            w*=q if e==z else 1-q
        x=phenotype(z1,z2); previous=phenotype(z0,z1)
        aa,bb=(a,b) if e2==0 else (b,a)
        loss+=w*(aa*x*x+bb*(x-D)**2+p['plastic_running_cost']
                 +p['plastic_switch_cost']*abs(x-previous))
        mass+=w
    assert abs(mass-1)<2e-14
    return loss


@pytest.mark.parametrize('rho,q',[(0,.5),(0,1),(1,.5),(1,1),(.1,.9),(.5,.8),(.9,.9),(.99,.9)])
def test_two_cue_objective_equals_64_paths(rho,q):
    m=api(); p=params(rho=rho,q=q)
    for same,diff in ((0,0),(1,1),(.8,.2),(.1,.7),(-.4,.7)):
        assert isclose(m.two_cue_loss(p,same,diff), enumerate_loss(p,same,diff), abs_tol=3e-13)


@pytest.mark.parametrize('rho',[0,.1,.5,.65625,.85,.9,.95,.99,1])
def test_exact_optimum_contains_memoryless_policy(rho):
    m=api(); p=params(rho=rho)
    out=m.audit(p)
    one=4.05-(.71-.32*rho)**2
    assert isclose(out['memoryless_loss'],one,abs_tol=2e-13)
    assert out['two_cue_loss_without_extra_memory_cost'] <= one+2e-13
    same,diff=out['two_cue_policy']['same'],out['two_cue_policy']['different']
    assert isclose(enumerate_loss(p,same,diff),out['two_cue_loss_without_extra_memory_cost'],abs_tol=3e-13)


def test_finite_regions_cover_global_sign_symmetric_optimum():
    m=api(); rng=random.Random(20261020)
    for _ in range(15):
        p=params(rho=rng.random(),q=.5+.5*rng.random())
        p['plastic_switch_cost']=4*rng.random()
        out=m.audit(p); opt=out['two_cue_loss_without_extra_memory_cost']
        for i,j in product(range(11),repeat=2):
            assert opt <= m.two_cue_loss(p,i/10,j/10)+3e-13


def test_known_original_and_reentry_witnesses():
    m=api()
    assert m.audit(params(.1))['best_strategy']=='PLASTIC_MEMORY'
    assert m.audit(params(.9))['best_strategy']=='FIXED_MODULES'
    assert isclose(m.audit(params(.9))['two_cue_loss_without_extra_memory_cost'],1652087/427000,abs_tol=2e-13)
    for rho,winner in ((.9,'PLASTIC_MEMORY'),(.95,'FIXED_MODULES'),(.99,'PLASTIC_MEMORY')):
        assert m.audit(params(rho,K=3.87))['best_strategy']==winner
    assert isclose(m.audit(params(.99,K=3.87))['two_cue_loss_without_extra_memory_cost'],509108497/131645000,abs_tol=3e-13)


def test_positive_extra_memory_cost_and_affordable_memory_threshold():
    m=api(); p=params(.99,K=3.87)
    out=m.audit(p,memory_cost=.001)
    assert out['best_strategy']=='PLASTIC_MEMORY'
    assert out['memory_beats_modules_budget']==pytest.approx(.0027167989669187)
    assert m.audit(p,memory_cost=.004)['best_strategy']=='FIXED_MODULES'
    assert m.audit(params(.85,K=3.87),memory_cost=.001)['best_strategy']=='PLASTIC_MEMORYLESS'
    assert m.audit(params(.95,K=3.87),memory_cost=.001)['best_strategy']=='FIXED_MODULES'


def test_uniform_history_independent_conflict_floor():
    m=api(); p=params(.9,K=2.9)
    out=m.audit(p)
    assert out['conflict_floor_C']==3
    assert out['all_shared_policies_lower_bound']==3
    assert out['modules_below_all_history_lower_bound'] is True
    for rho in (.01,.1,.5,.9,.99):
        p['rho']=rho
        assert m.audit(p)['modules_below_all_history_lower_bound']
        for same,diff in product((0,.5,1),repeat=2):
            assert enumerate_loss(p,same,diff)>=3-1e-13


def test_perfect_cue_zero_cost_attains_floor_and_equal_weights():
    m=api(); p=params(q=1)
    p.update(plastic_running_cost=0.,plastic_switch_cost=0.)
    assert m.audit(p)['two_cue_loss_without_extra_memory_cost']==pytest.approx(3)
    p.update(a=2.,b=2.,module_cost=6.)
    assert m.audit(p)['two_cue_loss_without_extra_memory_cost']==pytest.approx(4)
    p.update(delta=0.)
    assert m.audit(p)['best_strategy']=='SHARED'


def test_boundary_model_remains_historical_unvalidated():
    out=api().audit(params())
    assert out['historical_evolution_verified'] is False
    assert out['optimized_over_arbitrary_history'] is False
    assert out['same_single_coordinate_constraint'] is True


@pytest.mark.parametrize('key,value',[('a',0),('b',0),('q',.4),('q',float('nan')),('rho',1.2),('delta',-1),('plastic_switch_cost',-1),('module_cost',float('inf'))])
def test_bad_parameter_rejected(key,value):
    p=params(); p[key]=value
    with pytest.raises(ValueError): api().audit(p)


def test_negative_memory_and_out_of_range_action_rejected():
    m=api()
    with pytest.raises(ValueError): m.audit(params(),memory_cost=-.01)
    with pytest.raises(ValueError): m.two_cue_loss(params(),1.1,0)
    with pytest.raises(ValueError): m.two_cue_loss(params(),0,float('nan'))


def test_scale_invariance_of_witness():
    m=api(); p=params(.99,K=3.87)
    ref=m.audit(p)
    for scale in (1e-9,1e9):
        pp=dict(p)
        for key in ('a','b','plastic_running_cost','plastic_switch_cost','module_cost'):
            pp[key]*=scale
        out=m.audit(pp)
        assert out['best_strategy']==ref['best_strategy']
        assert out['two_cue_loss_without_extra_memory_cost']/scale==pytest.approx(ref['two_cue_loss_without_extra_memory_cost'])


def enumerate_general_action_loss(p, actions):
    a,b,D,q,rho=(p[k] for k in ('a','b','delta','q','rho'))
    d=(a-b)*D/(a+b); ans=0.
    for e0,e1,e2,z0,z1,z2 in product((0,1),repeat=6):
        w=.5
        for left,right in ((e0,e1),(e1,e2)):
            w*=rho if left!=right else 1-rho
        for e,z in ((e0,z0),(e1,z1),(e2,z2)):
            w*=q if e==z else 1-q
        x=D/2+d*actions[2*z1+z2]/2
        old=D/2+d*actions[2*z0+z1]/2
        aa,bb=(a,b) if e2==0 else (b,a)
        ans+=w*(aa*x*x+bb*(x-D)**2+p['plastic_running_cost']
               +p['plastic_switch_cost']*abs(x-old))
    return ans


def test_any_two_cue_map_is_dominated_by_its_symmetrized_clipped_map():
    m=api(); rng=random.Random(617)
    for _ in range(30):
        p=params(rho=rng.random(),q=.5+.5*rng.random())
        raw=[rng.uniform(-2,2) for i in range(4)]
        clipped=[min(1,max(-1,x)) for x in raw]
        symmetric=[(clipped[i]-clipped[3-i])/2 for i in range(4)]
        rawcost=enumerate_general_action_loss(p,raw)
        symcost=enumerate_general_action_loss(p,symmetric)
        assert symcost<=rawcost+5e-13
        assert m.audit(p)['two_cue_loss_without_extra_memory_cost']<=symcost+5e-13


def test_trait_units_preserve_strategies_and_rates():
    m=api(); p=params(.99,K=3.87)
    ref=m.audit(p)
    for factor in (.001,1e3):
        pp=dict(p); pp['a']/=factor**2; pp['b']/=factor**2
        pp['delta']*=factor; pp['plastic_switch_cost']/=factor
        r=m.audit(pp)
        assert r['best_strategy']==ref['best_strategy']
        assert r['two_cue_loss_without_extra_memory_cost']==pytest.approx(ref['two_cue_loss_without_extra_memory_cost'])


def test_unused_large_cost_cannot_change_nearby_strategy_ranking():
    m=api(); p=params(.1,K=1e18)
    assert m.audit(p)['best_strategy']=='PLASTIC_MEMORY'


def test_cli_witness_is_reproducible_and_roots_bracketed():
    import json,subprocess,sys
    proc=subprocess.run([sys.executable,str(ROOT/'scripts/run_plastic_compromise_memory.py')],
                        capture_output=True,text=True,check=True)
    r=json.loads(proc.stdout)
    assert r['this_script_performs_git_writes'] is False
    assert [x['best_strategy'] for x in r['exploratory_K3_87_reentry']]==[
        'PLASTIC_MEMORY','FIXED_MODULES','PLASTIC_MEMORY']
    assert r['two_cue_K3_87_crossing_brackets'][0]['rho']==pytest.approx(.90662093830735)
    assert r['two_cue_K3_87_crossing_brackets'][1]['rho']==pytest.approx(.97654038180607)
