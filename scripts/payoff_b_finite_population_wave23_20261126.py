"""Synthetic Wave 23: fixed-size two-species Wright-Fisher policy evolution."""
import argparse
import json
import math
from pathlib import Path

import numpy as np

S1, S2, J = .03, -.27, .29
THRESHOLD = -S2 / J
SIZES = (100, 1000, 10000)
MUTATION = (0., 1e-6, 1e-5, 1e-4)
SEED, REPS, HORIZON = 20261126, 1024, 4000


def update_probability(p, delta, mu):
    w = np.exp(delta)
    selected = p*w/(1-p+p*w)
    return mu+(1-2*mu)*selected


def proportion(mask):
    n = len(mask)
    count = int(np.count_nonzero(mask))
    if not n:
        return {'count': 0, 'n': 0, 'fraction': None, 'wilson95': None}
    p = count/n
    z = 1.959963984540054
    den = 1+z*z/n
    center = (p+z*z/(2*n))/den
    half = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return {'count': count, 'n': n, 'fraction': p,
            'wilson95': [max(0.,center-half),min(1.,center+half)]}


def simulate(n, mu, reps, horizon, seed):
    rng = np.random.default_rng(seed)
    x = np.full(reps,n//100,dtype=np.int64)
    y = x.copy()
    first_cross = np.full(reps,-1,dtype=np.int64)
    first_zero_b = first_cross.copy()
    first_joint = first_cross.copy()
    first_return_b = first_cross.copy()
    total_joint = np.zeros(reps,dtype=np.int64)
    for t in range(horizon+1):
        p,q = x/n,y/n
        hit = (first_cross<0)&(p>THRESHOLD)
        first_cross[hit] = t
        hit = (first_zero_b<0)&(y==0)
        first_zero_b[hit] = t
        hit = (first_return_b<0)&(first_zero_b>=0)&(y>0)
        first_return_b[hit] = t
        joint = (p>=.95)&(q>=.95)
        hit = (first_joint<0)&joint
        first_joint[hit] = t
        if t>0:
            total_joint += joint
        if t==horizon:
            break
        x = rng.binomial(n,update_probability(p,S1+J*q,mu))
        y = rng.binomial(n,update_probability(q,S2+J*p,mu))
    crossed = first_cross>=0
    vanished_before = (first_zero_b>=0)&(first_zero_b<first_cross)&crossed
    ever_joint = first_joint>=0
    p,q = x/n,y/n
    welfare = 2*(1-p)*(1-q)+1.78*p*(1-q)+1.48*(1-p)*q+1.84*p*q
    quant = lambda a: [float(v) for v in np.quantile(a,[.1,.5,.9])] if len(a) else None
    return {'N_each': n, 'mu_per_offspring': mu, 'seed': seed,
            'A_crossed': proportion(crossed),
            'B_zero_before_A_cross_given_cross': proportion(vanished_before[crossed]),
            'B_return_after_zero_given_zero': proportion((first_return_b>=0)[first_zero_b>=0]),
            'joint95_ever': proportion(ever_joint),
            'joint95_end': proportion((p>=.95)&(q>=.95)),
            'joint95_given_A_cross': proportion(ever_joint[crossed]),
            'joint95_given_B_zero_before_A_cross': proportion(ever_joint[vanished_before]),
            'B_zero_end': proportion(y==0),
            'joint95_first_time_quantiles_conditional_hit': quant(first_joint[ever_joint]),
            'A_cross_time_quantiles_conditional_hit': quant(first_cross[crossed]),
            'mean_joint95_occupancy': float(np.mean(total_joint/horizon)),
            'mean_terminal_joint_payoff': float(np.mean(welfare)),
            'mean_final_frequencies': [float(np.mean(p)),float(np.mean(q))]}


def deterministic(mu,horizon):
    p=q=.01
    first=None
    minimum=q
    for t in range(horizon+1):
        minimum=min(minimum,q)
        if first is None and min(p,q)>=.95:
            first=t
        if t<horizon:
            p,q=float(update_probability(p,S1+J*q,mu)),float(update_probability(q,S2+J*p,mu))
    return {'mu': mu,'B_min': minimum,'first_joint95': first,'final': [p,q]}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--seed',type=int,default=SEED)
    parser.add_argument('--reps',type=int,default=REPS)
    args=parser.parse_args()
    if args.reps<1:
        parser.error('--reps must be positive')
    assert update_probability(0.,.2,0.)==0.
    assert update_probability(1.,-.2,0.)==1.
    assert update_probability(0.,.2,1e-5)==1e-5
    assert abs(update_probability(.4,0.,0.)-.4)<1e-14
    assert abs(S2+J*THRESHOLD)<1e-14
    results=[simulate(n,mu,args.reps,HORIZON,args.seed+100*i+j)
             for i,n in enumerate(SIZES) for j,mu in enumerate(MUTATION)]
    for row in results:
        assert row['joint95_end']['count']<=row['joint95_ever']['count']<=row['A_crossed']['count']
        if row['mu_per_offspring']==0:
            assert row['B_return_after_zero_given_zero']['count']==0
            assert row['joint95_given_B_zero_before_A_cross']['count']==0
    out={'status':'SYNTHETIC_ONLY','model':'synchronous Wright-Fisher, exponential relative fitness, symmetric offspring mutation, fixed N per species','numpy_version':np.__version__,'base_seed':args.seed,'reps_per_cell':args.reps,'horizon_generations':HORIZON,'initial_frequency_each':.01,'s1':S1,'s2':S2,'J':J,'A_threshold':THRESHOLD,'deterministic_discrete':[deterministic(mu,HORIZON) for mu in MUTATION],'cells':results}
    args.out.write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':
    main()
