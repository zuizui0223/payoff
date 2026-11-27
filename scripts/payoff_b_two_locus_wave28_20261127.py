"""Synthetic two-locus realization of Wave 27's conditional payoff landscape."""
import argparse
import itertools
import json
import math
from pathlib import Path
import numpy as np

T=2000
REPS=256
SEEDS=(20261127,20361127)
RATES=(0.,.005,.02,.05,.1,.5)
REGIMES=('coupling','repulsion','independent_mutation','paired_mutation')
CELLS=list(itertools.product((.3,.5),(1000,10000),RATES,REGIMES))
MU=1e-4

def landscape(k):
    r=(.4-.06)/(2*((1+k)/4))
    g=np.array([.4*x*y-(1+k)/4*y*y-.06*y-.06*x*x for x,y in [(0,0),(1,0),(0,r),(1,r)]])
    return r,g

def mutation_matrix(regime):
    M=np.eye(4)
    if regime=='independent_mutation':
        for i in range(4):
            for j in range(4):
                d=(i^j).bit_count()
                M[i,j]=MU**d*(1-MU)**(2-d)
    elif regime=='paired_mutation':
        M=(1-MU)*np.eye(4)+MU*np.eye(4)[::-1]
    return M

def update(f,w,R,M):
    s=f*w
    s/=s.sum(axis=-1,keepdims=True)
    ld=s[...,0]*s[...,3]-s[...,1]*s[...,2]
    p=s+R*ld[...,None]*np.array([-1.,1.,1.,-1.])
    p=np.einsum('cri,cij->crj',p,M)
    if np.min(p)<-1e-12: raise ArithmeticError('negative probability')
    p=np.maximum(p,0.)
    p/=p.sum(axis=-1,keepdims=True)
    return p

def validate():
    rng=np.random.default_rng(1234)
    f=rng.dirichlet([1]*4,size=1000).reshape(1,1000,4)
    for R in RATES:
        p=update(f,np.ones((1,1,4)),np.array([[[R]]]),np.eye(4)[None,:,:])
        assert np.allclose(p[...,1]+p[...,3],f[...,1]+f[...,3],atol=1e-14)
        assert np.allclose(p[...,2]+p[...,3],f[...,2]+f[...,3],atol=1e-14)
        assert np.allclose(p.sum(axis=-1),1.)
        ld=lambda z:z[...,0]*z[...,3]-z[...,1]*z[...,2]
        assert np.allclose(ld(p),(1-R)*ld(f),atol=1e-14)
    for k in (.3,.5):
        _,g=landscape(k)
        assert g[3]>0 and g[1]<0 and g[2]<0
        for R in RATES:
            w=np.exp(g)[None,None,:];M=np.eye(4)[None,:,:]
            q=update(np.array([[[1.,0.,0.,0.]]]),w,np.array([[[R]]]),M)
            assert np.array_equal(q,np.array([[[1.,0.,0.,0.]]]))
            eps=1e-8
            p=update(np.array([[[1-eps,0.,0.,eps]]]),w,np.array([[[R]]]),M)
            assert abs(p[0,0,3]/eps-(1-R)*math.exp(g[3]))<1e-7
    for mode in REGIMES[2:]:
        M=mutation_matrix(mode)
        assert np.allclose(M.sum(axis=1),1.)
        for i in range(4):
            for bit in (1,2):
                assert abs(sum(M[i,j] for j in range(4) if (i^j)&bit)-MU)<1e-14

def simulate(seed,reps,stochastic):
    n=np.array([c[1] for c in CELLS])[:,None]
    R=np.array([c[2] for c in CELLS])[:,None,None]
    g=np.array([landscape(c[0])[1] for c in CELLS])[:,None,:]
    w=np.exp(g)
    M=np.array([mutation_matrix(c[3]) for c in CELLS])
    initial=np.array([[.9,0,0,.1] if c[3]=='coupling' else [.8,.1,.1,0] if c[3]=='repulsion' else [1,0,0,0] for c in CELLS])
    f=np.repeat(initial[:,None,:],reps,axis=1)
    rng=np.random.default_rng(seed)
    first11=np.full(f.shape[:2],-1,dtype=int)
    first95=first11.copy()
    sum11=np.zeros(f.shape[:2])
    for t in range(T+1):
        first11[(first11<0)&(f[...,3]>0)]=t
        first95[(first95<0)&(f[...,3]>=.95)]=t
        if t>0: sum11+=f[...,3]
        if t==T: break
        p=update(f,w,R,M)
        if stochastic:
            f=rng.multinomial(n,p)/n[...,None]
        else:
            f=p
    rows=[]
    for i,(k,N,rr,regime) in enumerate(CELLS):
        ever=first11[i]>=0;hit=first95[i]>=0
        assert np.all(~hit|ever)
        if regime=='repulsion' and rr==0: assert not np.any(ever)
        if regime=='coupling': assert np.all(ever)
        rr_star,g0=landscape(k)
        rows.append(dict(k=k,N=N,R=rr,regime=regime,reps=reps,ever11=int(ever.sum()),hit95=int(hit.sum()),
                         hit95_given_ever=float(hit.sum()/ever.sum()) if ever.any() else None,
                         median_first11=float(np.median(first11[i,ever])) if ever.any() else None,
                         median_first95=float(np.median(first95[i,hit])) if hit.any() else None,
                         terminal11=float(f[i,:,3].mean()),average11=float(sum11[i].mean()/T),
                         mean_terminal_log_fitness=float(np.mean(f[i]@g0))))
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    validate()
    results={'status':'SYNTHETIC_ONLY','numpy_version':np.__version__,'seeds':SEEDS,'reps_per_seed':REPS,'generations':T,'mu':MU,
             'landscapes':[{'k':k,'r_star':landscape(k)[0],'log_fitness':landscape(k)[1].tolist(),
                            'rare_double_Rc':-math.expm1(-landscape(k)[1][3])} for k in (.3,.5)]}
    for label,seed in zip(('main','repeat'),SEEDS):
        results[label]=simulate(seed,REPS,True)
        print('completed',label,flush=True)
    results['deterministic']=simulate(0,1,False)
    args.out.write_text(json.dumps(results,indent=2)+'\n')
    print('wrote',args.out,flush=True)

if __name__=='__main__': main()
