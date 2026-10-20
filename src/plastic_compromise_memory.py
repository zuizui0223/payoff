"""Two-cue optimal plasticity and a policy-independent shared-coordinate bound.

Extends PAYOFF #338 without changing its memoryless model or source parameters.
Only the previous and current noisy cues are used; no true state is observed.
The convex, sign-symmetric two-cue problem is solved analytically by enumerating
its two quadratic regions and their common diagonal. No numerical optimizer or
new runtime dependency is needed. This is synthetic theory, not biological data.
"""
from __future__ import annotations
from math import isfinite, log2
from typing import Mapping

KEYS = ('a','b','delta','q','rho','plastic_running_cost',
        'plastic_switch_cost','module_cost')


def _validated(p: Mapping[str, float]) -> dict[str, float]:
    try:
        v = {k: float(p[k]) for k in KEYS}
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError('eight finite model parameters are required') from exc
    if not all(isfinite(x) for x in v.values()):
        raise ValueError('parameters must be finite')
    if not (v['a'] >= v['b'] > 0 and v['delta'] >= 0):
        raise ValueError('require a>=b>0 and delta>=0')
    if not (.5<=v['q']<=1 and 0<=v['rho']<=1):
        raise ValueError('require q in [0.5,1] and rho in [0,1]')
    if any(v[k]<0 for k in ('plastic_running_cost','plastic_switch_cost','module_cost')):
        raise ValueError('costs must be nonnegative')
    return v


def _moments(p):
    a,b,D,q,rho=(p[k] for k in ('a','b','delta','q','rho'))
    d=(a-b)*D/(a+b)
    C=a*b/(a+b)*D*D
    T=(a+b)*d*d/4
    g=2*q-1; r=1-2*rho
    out=dict(C=C,T=T,d=d,g=g,r=r,ps=(1+g*g*r)/2,
             pd=(1-g*g*r)/2,ks=g*(1-rho),kd=g*rho,
             w=(1-g*g*r*r)/4,t=(1-2*g*g*r+g*g*r*r)/4)
    if not all(isfinite(x) for x in out.values()):
        raise ValueError('derived values overflow; rescale parameters')
    return out


def _objective(p, z, u, v):
    # z.w = P(001)+P(110) = P(011)+P(100), by time reversal.
    # z.t = P(010)+P(101). Actions are -u,+v,-v,+u for 00,01,10,11.
    switch = p['plastic_switch_cost']*z['d']*(
        z['w']*(abs(u+v)+abs(u-v))/2+z['t']*abs(v))
    return (z['C']+z['T']*(1+z['ps']*u*u+z['pd']*v*v
                         -2*z['ks']*u-2*z['kd']*v)
            +p['plastic_running_cost']+switch)


def two_cue_loss(p: Mapping[str,float], same: float, different: float) -> float:
    """Exact expected loss of the symmetric map on two consecutive cues.

    Signed u/v in [-1,1] are accepted to validate the nonnegative optimum.
    Additional memory-specific maintenance cost is not charged here.
    """
    pp=_validated(p)
    u,v=float(same),float(different)
    if not all(isfinite(x) and -1<=x<=1 for x in (u,v)):
        raise ValueError('response amplitudes must be finite in [-1,1]')
    return _objective(pp,_moments(pp),u,v)


def _unit(value):
    return min(1.,max(0.,value))


def _ratio(num,den):
    # Zero-probability cue classes occur at deterministic endpoints only.
    return num/den if den>0 else 0.


def audit(p: Mapping[str,float], *, memory_cost: float=0.) -> dict:
    """Find the global two-cue stationary-policy optimum and compare strategies.

    The sign-symmetric restriction loses no optimum among deterministic maps
    of the last two cues: symmetrize complementary maps and apply convexity.
    Replacing signed amplitudes with their absolute values cannot raise loss.
    A randomized conditional action map cannot improve this convex objective.
    This does NOT optimize controllers with internal state or longer memory.
    """
    pp=_validated(p); z=_moments(pp)
    M=float(memory_cost)
    if not isfinite(M) or M<0:
        raise ValueError('memory_cost must be finite and nonnegative')
    T=z['T']; cd=pp['plastic_switch_cost']*z['d']
    if T==0:
        alpha=0.; candidates=[('no_environmental_amplitude',0.,0.)]
    else:
        alpha=_unit(z['g']-cd*z['pd']/(2*T))
        candidates=[('diagonal_memoryless',alpha,alpha)]
        u=_unit(_ratio(z['ks']-cd*z['w']/(2*T),z['ps']))
        v=_unit(_ratio(z['kd']-cd*z['t']/(2*T),z['pd']))
        if u>=v:
            candidates.append(('same_cue_amplitude_larger',u,v))
        u=_unit(_ratio(z['ks'],z['ps']))
        v=_unit(_ratio(z['kd']-cd*z['pd']/(2*T),z['pd']))
        if v>=u:
            candidates.append(('different_cue_amplitude_larger',u,v))
    scores=[(_objective(pp,z,u,v),region,u,v) for region,u,v in candidates]
    loss2,region,u,v=min(scores,key=lambda x:x[0])
    loss1=_objective(pp,z,alpha,alpha)
    S=z['C']+T; K=pp['module_cost']
    losses={'SHARED':S,'PLASTIC_MEMORYLESS':loss1,
            'PLASTIC_MEMORY':loss2+M,'FIXED_MODULES':K}
    if not all(isfinite(x) for x in losses.values()):
        raise ValueError('evaluated losses overflow; rescale parameters')
    minimum=min(losses.values())
    # Compare each alternative to the minimum on its own cost scale.
    # An unrelated enormous module cost must not turn other strategies into ties.
    winners=[name for name,x in losses.items()
             if x-minimum<=128*2.220446049250313e-16*max(abs(x),abs(minimum))]
    rho=pp['rho']
    H=0. if rho in (0.,1.) else -rho*log2(rho)-(1-rho)*log2(1-rho)
    return dict(
        schema='PAYOFF_TWO_CUE_MEMORY_ROBUSTNESS_V1',
        source_status='SYNTHETIC_CONDITIONAL_MODEL_NOT_EMPIRICAL',
        parameters=pp, extra_memory_cost=M,
        environmental_lag_one_correlation=z['r'],
        environmental_entropy_rate_bits=H,
        conflict_floor_C=z['C'], between_environment_mismatch_T=T,
        memoryless_loss=loss1, memoryless_amplitude=alpha,
        two_cue_loss_without_extra_memory_cost=loss2,
        two_cue_policy={'same':u,'different':v,'region':region},
        memory_gain_before_extra_cost=loss1-loss2,
        memory_beats_modules_budget=K-loss2,
        losses=losses, loss_minimizers=winners, best_strategy=winners[0],
        all_shared_policies_lower_bound=z['C'],
        modules_below_all_history_lower_bound=(K<z['C']),
        same_single_coordinate_constraint=True,
        optimized_over_arbitrary_history=False,
        historical_evolution_verified=False,
    )
