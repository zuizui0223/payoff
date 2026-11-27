"""Wave 29: reciprocal two-locus coevolution (synthetic only)."""
import argparse
import itertools
import json
import math
from pathlib import Path
import numpy as np

T, REPS = 2000, 128
SEEDS = (20261127, 20361127)
MU, K, D = 1e-4, .5, .375
RATES = ((.005,.005),(.005,.02),(.02,.02),(.04,.04))
CELLS = list(itertools.product((.8,.85,.9),RATES,(1000,10000),('independent','paired'),(False,True)))


def parameters(qb, rates, coupled):
    a=np.array([.4,qb-.5]); r=(a-.06)/(2*D)
    g=np.array([[0.,-.06,-D*ri**2-.06*ri,ai*ri-D*ri**2-.06*ri-.06] for ai,ri in zip(a,r)])
    J=2*K*a.prod() if coupled else 0.
    G=J*r.prod(); R=np.array(rates)
    s0=g[:,3]+np.log1p(-R); s1=s0+G
    # full-11 corner: single derivatives and rare ancestor derivative
    gh=g[:,3]+G
    full_eigen=np.stack([np.exp(g[:,1]-gh),np.exp(g[:,2]-gh),(1-R)*np.exp(-gh)],axis=-1)
    thresh=[float(-s/G) if G>0 else None for s in s0]
    return a,r,g,J,G,R,s0,s1,full_eigen,thresh


def mutation(mode):
    if mode=='paired':return (1-MU)*np.eye(4)+MU*np.eye(4)[::-1]
    return np.array([[MU**((i^j).bit_count())*(1-MU)**(2-(i^j).bit_count()) for j in range(4)] for i in range(4)])


def update(f,g,G,R,M):
    # f[cell,rep,species,haplotype], both species observe old frequencies.
    logw=np.broadcast_to(g,f.shape).copy()
    logw[...,3]+=G*f[:,:,::-1,3]
    s=f*np.exp(logw);s/=s.sum(axis=-1,keepdims=True)
    ld=s[...,0]*s[...,3]-s[...,1]*s[...,2]
    p=s+(R*ld)[...,None]*np.array([-1.,1.,1.,-1.])
    p=np.einsum('crsi,cij->crsj',p,M)
    if p.min() < -1e-12:raise ArithmeticError('negative probability')
    p=np.maximum(p,0.);p/=p.sum(axis=-1,keepdims=True)
    return p


def validate():
    rng=np.random.default_rng(991)
    f=rng.dirichlet(np.ones(4),size=(1,1000,2))
    for rate in RATES:
        p=update(f,np.zeros((1,1,2,4)),np.zeros((1,1,1)),np.array(rate)[None,None,:],np.eye(4)[None,:,:])
        assert np.max(np.abs(p.sum(axis=-1)-1))<1e-12
        assert np.allclose(p[...,1]+p[...,3],f[...,1]+f[...,3],atol=1e-14)
        assert np.allclose(p[...,2]+p[...,3],f[...,2]+f[...,3],atol=1e-14)
        assert np.allclose(p[...,0]*p[...,3]-p[...,1]*p[...,2],(1-np.array(rate))*(f[...,0]*f[...,3]-f[...,1]*f[...,2]),atol=1e-14)
    for qb,rates,N,mode,coupled in CELLS:
        a,r,g,J,G,R,s0,s1,eigs,threshold=parameters(qb,rates,coupled)
        for i in (0,1):
            for fp in (0.,.1,.9,1.):
                f=np.zeros((1,1,2,4)); eps=1e-8
                f[0,0,i]=[1-eps,0,0,eps];f[0,0,1-i]=[1-fp,0,0,fp]
                out=update(f,g[None,None,:,:],np.array([[[G]]]),R[None,None,:],np.eye(4)[None,:,:])
                assert abs(out[0,0,i,3]/eps-math.exp(s0[i]+G*fp))<1e-7
        M=mutation(mode)
        assert np.allclose(M.sum(axis=1),1)
        for i in range(4):
            for bit in (1,2):assert abs(sum(M[i,j] for j in range(4) if (i^j)&bit)-MU)<1e-14


def simulate(seed,reps,stochastic):
    pars=[parameters(qb,rr,coupled) for qb,rr,N,mode,coupled in CELLS]
    n=np.array([c[2] for c in CELLS])[:,None,None]
    g=np.array([p[2] for p in pars])[:,None,:,:]
    G=np.array([p[4] for p in pars])[:,None,None]
    R=np.array([p[5] for p in pars])[:,None,:]
    s0=np.array([p[6] for p in pars])[:,None,:]
    rr=np.array([p[1] for p in pars])[:,None,:]
    a=np.array([p[0] for p in pars])[:,None,:]
    M=np.array([mutation(c[3]) for c in CELLS])
    f=np.zeros((len(CELLS),reps,2,4));f[...,0]=1.
    rng=np.random.default_rng(seed)
    first=np.full(f.shape[:-1],-1,dtype=int)
    switch=first.copy(); emergence=first.copy(); first_joint=np.full(f.shape[:2],-1,dtype=int)
    switch_with11=first.copy()
    accum=np.zeros(f.shape[:-1]); mm_sum=np.zeros(f.shape[:2]);
    for t in range(T+1):
        h=f[...,3]; positive=s0+G*h[:,:,::-1]>1e-12
        switch[(switch<0)&positive]=t
        switch_with11[(switch_with11<0)&positive&(h>0)]=t
        emergence[(emergence<0)&(h>0)]=t
        first[(first<0)&(h>=.95)]=t
        first_joint[(first_joint<0)&np.all(h>=.95,axis=-1)]=t
        if t>0:
            accum+=h
            # Expected squared timing difference of the actual two cue-driven traits, also in J=0 selection control.
            mm_sum+=np.sum(rr**2*(f[...,2]+h),axis=-1)/4-2*np.prod(a*rr*h,axis=-1)
        if t==T:break
        p=update(f,g,G,R,M)
        f=rng.multinomial(n,p)/n[...,None] if stochastic else p
    rows=[]
    for i,(qb,rates,N,mode,coupled) in enumerate(CELLS):
        a0,r0,g0,J,G0,R0,s0i,s1i,eigs,threshold=pars[i]
        fi=first[i];sw=switch[i]; em=emergence[i];hit=fi>=0; joint=first_joint[i]>=0
        assert np.all(~joint|np.all(hit,axis=-1));assert np.all(~hit|(em>=0))
        initially_negative=s0i< -1e-12
        b_switched=initially_negative[1]&(sw[:,1]>=0)
        b_hits_after_switch=b_switched&hit[:,1]&(sw[:,1]<fi[:,1])
        # Not a proof of mediation; event sequence only.
        cnt=lambda z:int(np.count_nonzero(z))
        med=lambda v:float(np.median(v[v>=0])) if np.any(v>=0) else None
        rows.append(dict(qB=qb,RA=rates[0],RB=rates[1],N=N,mutation=mode,coupled=coupled,reps=reps,
          ever11=[cnt(em[:,j]>=0) for j in (0,1)],hit95=[cnt(hit[:,j]) for j in (0,1)],joint95=cnt(joint),
          positive_margin_ever=[cnt(sw[:,j]>=0) for j in (0,1)],
          positive_margin_with11_ever=[cnt(switch_with11[i,:,j]>=0) for j in (0,1)],
          switch_before_B_hit=cnt(b_hits_after_switch),B_switch_count=cnt(b_switched),
          A_hit_before_B_hit=cnt(hit[:,0]&hit[:,1]&(fi[:,0]<fi[:,1])),
          B_hit_before_A_hit=cnt(hit[:,0]&hit[:,1]&(fi[:,1]<fi[:,0])),
          median_first_positive=[med(sw[:,j]) for j in (0,1)],median_first95=[med(fi[:,j]) for j in (0,1)],median_joint95=med(first_joint[i]),
          final11=f[i,:, :,3].mean(axis=0).tolist(),mean11=(accum[i].mean(axis=0)/T).tolist(),mean_squared_timing_difference=float(mm_sum[i].mean()/T)))
    return rows


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True,type=Path);parser.add_argument('--label',choices=('main','repeat','deterministic','all'),default='all');args=parser.parse_args()
    validate()
    theory=[]
    for qb,rates in itertools.product((.8,.85,.9),RATES):
        a,r,g,J,G,R,s0,s1,eigs,thresh=parameters(qb,rates,True)
        theory.append(dict(qB=qb,RA=rates[0],RB=rates[1],r=r.tolist(),g11=g[:,3].tolist(),coupling_gain=G,
            rare_log_margin_no_partner=s0.tolist(),rare_log_margin_full_partner=s1.tolist(),critical_partner11=thresh,
            ancestral_corner_locally_attracting=bool(np.all(s0<0)),full_double_corner_locally_attracting=bool(np.all(eigs<1)),full_double_eigenvalues=eigs.tolist()))
    out=dict(status='SYNTHETIC_ONLY',numpy=np.__version__,horizon=T,reps_per_seed=REPS,seeds=SEEDS,mutation=MU,theory=theory)
    for label,seed in zip(('main','repeat'),SEEDS):
        if args.label in (label,'all'):
            out[label]=simulate(seed,REPS,True);print('completed',label,flush=True)
    if args.label in ('deterministic','all'):
        out['deterministic']=simulate(0,1,False);print('completed deterministic',flush=True)
    args.out.write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
