"""History-aware plasticity audit and policy-independent loss certificates.

Extends the declared two-function, symmetric Markov model without changing its
fitness scale. Finite cue-window policies provide constructive UPPER bounds
on the best shared-coordinate loss. A pointwise two-period relaxation gives
LOWER bounds even for controllers that know all past and future states.

These are synthetic mathematical results, not observed structural origins,
genotype invasion, or a Wurmbea fit. A module is the same idealized individual
coexpressing two independent functional coordinates as in the original model.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from math import fsum, isfinite


@dataclass(frozen=True)
class Parameters:
    a: float = 3.0
    b: float = 1.0
    delta: float = 2.0
    q: float = 0.9
    rho: float = 0.9
    running_cost: float = 0.05
    switch_cost: float = 1.0
    module_cost: float = 3.8

    def __post_init__(self):
        for name in self.__dataclass_fields__:
            value = float(getattr(self, name))
            if not isfinite(value):
                raise ValueError(f'{name} must be finite')
            object.__setattr__(self, name, value)
        if not self.a >= self.b > 0:
            raise ValueError('require a >= b > 0')
        if not .5 <= self.q <= 1 or not 0 <= self.rho <= 1:
            raise ValueError('q must be in [.5,1] and rho in [0,1]')
        if min(self.delta, self.running_cost, self.switch_cost, self.module_cost) < 0:
            raise ValueError('distance and costs must be nonnegative')
        try:
            derived = (self.conflict_floor, self.temporal_loss, self.optimum_distance,
                       self.shared_loss, self.switch_cost*self.optimum_distance)
        except OverflowError as error:
            raise ValueError('derived parameter overflow; rescale inputs') from error
        if not all(isfinite(x) for x in derived):
            raise ValueError('derived parameter overflow; rescale inputs')

    @property
    def conflict_floor(self):
        return self.a*self.b/(self.a+self.b)*self.delta**2

    @property
    def temporal_loss(self):
        return (self.a-self.b)**2*self.delta**2/(4*(self.a+self.b))

    @property
    def optimum_distance(self):
        return (self.a-self.b)*self.delta/(self.a+self.b)

    @property
    def shared_loss(self):
        return self.conflict_floor+self.temporal_loss


def _validate_cue_inputs(q, rho, memory):
    if not isinstance(memory, int) or isinstance(memory, bool) or not 1 <= memory <= 12:
        raise ValueError('memory must be an integer in [1,12]')
    if not isfinite(q) or not .5 <= q <= 1 or not isfinite(rho) or not 0 <= rho <= 1:
        raise ValueError('invalid cue accuracy or environmental flip probability')


def _word_probability_and_mean(word, q, rho):
    """Unnormalized two-state forward recursion, initially stationary (1/2,1/2)."""
    p0 = p1 = .5
    for step, cue in enumerate(word):
        if step:
            p0, p1 = (1-rho)*p0+rho*p1, rho*p0+(1-rho)*p1
        p0 *= q if cue == 0 else 1-q
        p1 *= q if cue == 1 else 1-q
    prob = p0+p1
    return prob, (p1-p0)/prob if prob else 0.0


@lru_cache(maxsize=256)
def _moments(q, rho, memory):
    words = list(product((0,1), repeat=memory))
    means = [_word_probability_and_mean(w,q,rho)[1] for w in words]
    mask = (1 << memory)-1
    terms_mass, terms_r, terms_tv = [], [], []
    for index, word in enumerate(product((0,1), repeat=memory+1)):
        probability, _ = _word_probability_and_mean(word,q,rho)
        previous, current = means[index >> 1], means[index & mask]
        terms_mass.append(probability)
        terms_r.append(probability*current*current)
        terms_tv.append(probability*abs(current-previous))
    return fsum(terms_mass), fsum(terms_r), fsum(terms_tv)


def window_moments(q: float, rho: float, memory: int) -> dict:
    """Exact finite-state enumeration, evaluated in floating point, not simulation.

    m_t=E[2E_t-1 | most recent `memory` cues]. Adjacent windows overlap;
    their dependence is retained when computing E|m_t-m_(t-1)|.
    """
    _validate_cue_inputs(q,rho,memory)
    mass, r, variation = _moments(float(q),float(rho),memory)
    if abs(mass-1) > 1e-12:
        raise ArithmeticError('cue-word distribution does not sum to one')
    return {'memory_length': memory, 'probability_mass': mass,
            'posterior_second_moment': r, 'posterior_total_variation': variation,
            'cue_words_enumerated': 2**(memory+1)}


def memory_policy(params: Parameters, memory: int, memory_cost: float = 0.0) -> dict:
    """Feasible posterior-amplitude policy; NOT optimal among all history policies.

    x_t=Delta/2 + (d/2)*beta*m_t, 0<=beta<=1.
    Expected loss = C+T+B+M + TR(beta^2-2beta) + cd*beta*V/2.
    """
    if not isfinite(memory_cost) or memory_cost < 0:
        raise ValueError('memory_cost must be finite and nonnegative')
    moments=window_moments(params.q,params.rho,memory)
    r=moments['posterior_second_moment']
    v=moments['posterior_total_variation']
    t=params.temporal_loss
    beta = max(0.0, min(1.0, 1-params.switch_cost*params.optimum_distance*v/(4*t*r))) if t*r > 0 else 0.0
    mismatch=params.conflict_floor+t*(1+r*(beta*beta-2*beta))
    switching=params.switch_cost*params.optimum_distance*beta*v/2
    total=mismatch+switching+params.running_cost+memory_cost
    return {**moments, 'attenuation': beta, 'expected_mismatch': mismatch,
            'expected_switching_cost': switching, 'running_cost': params.running_cost,
            'extra_memory_cost': memory_cost, 'expected_loss': total,
            'optimized_only_within_posterior_amplitude_class': True,
            'is_feasible_policy_upper_bound_not_global_optimum': True}


def pairwise_switch_floor(params: Parameters) -> float:
    """Minimum pair loss when target changes, with HALF of each endpoint error.

    min_(x,y) w/2[(x-z0)^2+(y-z1)^2]+c|y-x| is
    cd-(cd)^2/(4T) when cd<=2T, and T otherwise. T=w*d^2/4.
    The minimization gives the controller both states, even future ones.
    """
    t=params.temporal_loss
    if t == 0:
        return 0.0
    cd=params.switch_cost*params.optimum_distance
    if cd >= 2*t:
        return t
    return cd*(1-cd/(4*t))


def strategy_bounds(params: Parameters, memories=(1,2,4,8,12), memory_cost: float=0.0) -> dict:
    """Bracket optimal nonmodule loss and report only logically certified signs.

    Lower: min(SHARED, C+B+rho*psi); valid for ANY shared-coordinate controller
    paying the declared nonnegative running and absolute switching costs.
    Upper: min(SHARED, evaluated finite-window feasible policies).
    """
    memories=tuple(memories)
    if not memories:
        raise ValueError('at least one finite-window policy required')
    policies=[memory_policy(params,n,memory_cost) for n in memories]
    psi=pairwise_switch_floor(params)
    dynamic_lower=params.conflict_floor+params.running_cost+params.rho*psi
    lower=min(params.shared_loss,dynamic_lower)
    upper=min(params.shared_loss,*(p['expected_loss'] for p in policies))
    tolerance=1e-10*max(1.0,abs(lower),abs(upper),params.module_cost)
    if lower > upper+tolerance:
        raise ArithmeticError('relaxation bound exceeds a feasible policy')
    if lower > params.module_cost+tolerance:
        label='MODULE_BEATS_ALL_SHARED_COORDINATE_POLICIES'
    elif upper < params.module_cost-tolerance:
        label='NONMODULE_FEASIBLE_POLICY_BEATS_MODULE'
    else:
        label='UNRESOLVED_OR_TIED'
    return {'classification': label, 'conflict_floor':params.conflict_floor,
            'temporal_loss':params.temporal_loss,'module_loss':params.module_cost,
            'shared_loss':params.shared_loss, 'pair_switch_penalty_floor':psi,
            'arbitrary_controller_loss_lower_bound':dynamic_lower,
            'nonmodule_lower_bound':lower,'nonmodule_upper_bound':upper,
            'minimum_module_advantage':lower-params.module_cost,
            'maximum_module_advantage':upper-params.module_cost,
            'finite_memory_policies':policies,
            'certificate_applies_even_with_perfect_future_information':True,
            'nonnegative_memory_cost_assumed_not_measured':True,
            'historical_causal_origin_tested':False}


def optimal_window_policy(params: Parameters, memory: int) -> dict:
    """Convex optimization over EVERY deterministic mapping of the last m cues.

    The weighted graph total-variation dual supplies a numerical lower bound
    for this finite-window class. Its feasible primal supplies an upper bound
    for the unrestricted history class. Do not confuse the two directions.
    Requires optional numpy/scipy; no simulation or biological parameters.
    """
    import numpy as np
    from scipy.optimize import minimize

    _validate_cue_inputs(params.q,params.rho,memory)
    if memory > 6:
        raise ValueError('convex window optimization is budgeted to memory <= 6')
    nodes=list(product((0,1),repeat=memory))
    observations=[_word_probability_and_mean(w,params.q,params.rho) for w in nodes]
    probability=np.array([p for p,_ in observations])
    means=np.array([v for _,v in observations])
    edge_probability=np.array([_word_probability_and_mean(w,params.q,params.rho)[0]
                               for w in product((0,1),repeat=memory+1)])
    codes=np.arange(2**(memory+1))
    source=codes >> 1
    target=codes & (2**memory-1)
    nonzero=(edge_probability>0)&(source!=target)
    source,target=source[nonzero],target[nonzero]
    capacities=params.switch_cost*params.optimum_distance*edge_probability[nonzero]/2
    t=params.temporal_loss
    base=params.conflict_floor+t+params.running_cost
    r=float(np.dot(probability,means*means))
    inverse=np.zeros_like(probability)
    if t>0:
        np.divide(1,2*t*probability,out=inverse,where=probability>0)

    def divergence(v):
        return (np.bincount(target,weights=v,minlength=len(nodes))
                -np.bincount(source,weights=v,minlength=len(nodes)))

    def objective(v):
        div=divergence(v)
        x=means-div*inverse
        negative_dual=float(.5*np.dot(div*inverse,div)-np.dot(div,means))
        gradient=-(x[target]-x[source])
        return negative_dual, gradient

    if t==0:
        actions=np.zeros_like(means)
        dual=base
        success=True
        iterations=0
    elif len(capacities)==0 or np.max(capacities)==0:
        actions=means.copy()
        dual=base-t*r
        success=True
        iterations=0
    else:
        result=minimize(objective,np.zeros(len(capacities)),jac=True,
                        method='L-BFGS-B',bounds=list(zip(-capacities,capacities)),
                        options={'ftol':1e-15,'gtol':1e-10,'maxiter':20000,'maxls':100,'maxcor':40})
        # Explicit clipping makes the dual point feasible even under roundoff.
        v=np.clip(result.x,-capacities,capacities)
        negative_dual,_=objective(v)
        dual=base-t*r-negative_dual
        actions=np.clip(means-divergence(v)*inverse,-1,1)
        success=bool(result.success)
        iterations=int(result.nit)
    primal=(base+t*float(np.dot(probability,actions*actions-2*actions*means))
            +float(np.dot(capacities,np.abs(actions[target]-actions[source]))))
    gap=primal-dual
    if gap < -1e-9:
        raise ArithmeticError('invalid primal/dual orientation')
    return {'memory_length':memory,'mapping_states':2**memory,
            'primal_loss':primal,'dual_lower_bound_on_window_class':dual,
            'primal_dual_gap':gap,'solver_success':success,'solver_iterations':iterations,
            'normalized_actions':actions.tolist(),
            'cue_words':[''.join(map(str,w)) for w in nodes],
            'numerically_certified_to_2e_8':gap<=2e-8,
            'certificate_scope':'FINITE_CUE_WINDOW_ONLY_NOT_ALL_HISTORY',
            'extra_memory_cost_assumed':0.0}


def predictable_endpoint_optimum(params: Parameters) -> dict:
    """Exact long-run optimum for rho=0 or 1, with cost-free cue accumulation.

    For q>1/2, parity-corrected repeated cues reveal the initial state with
    exponentially vanishing error. Learning transients vanish in time-average
    loss. rho=0 reaches C+B; rho=1 reaches the sharp pair bound C+B+psi.
    An informative reward/fitness observation is NOT assumed for q=1/2.
    """
    if params.rho not in (0,1):
        raise ValueError('endpoint theorem requires rho equal to 0 or 1')
    if params.q==.5:
        dynamic=params.shared_loss+params.running_cost
        assumption='cues only, no informative state or fitness feedback'
    else:
        dynamic=(params.conflict_floor+params.running_cost
                 +params.rho*pairwise_switch_floor(params))
        assumption='informative cues; accumulating phase evidence has zero additional cost'
    best=min(params.shared_loss,dynamic)
    tol=1e-10*max(1,abs(best),params.module_cost)
    comparison=('TIE' if abs(best-params.module_cost)<=tol else
                ('MODULE_BETTER' if params.module_cost<best else 'NONMODULE_BETTER'))
    return {'rho':params.rho,'optimal_dynamic_loss':dynamic,
            'optimal_nonmodule_loss':best,'module_comparison':comparison,
            'memory_cost_assumption':assumption,
            'asymptotic_learning_not_fixed_finite_window':True,
            'historical_causality_tested':False}
