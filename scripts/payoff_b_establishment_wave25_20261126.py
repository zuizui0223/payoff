"""Conditional finite-N establishment and time-dependent rare-lineage benchmark."""
import argparse, hashlib, itertools, json, math
from pathlib import Path
import numpy as np
from scipy.linalg import solve
from scipy.optimize import brentq
from scipy.special import expit
from scipy.stats import binom
HORIZON=4000
REPS=4096
SEEDS=(20261126,20361126)
MU=1e-5
SETTINGS=list(itertools.product((.6,.8),(.3,.5),(.25,1.,4.)))
def parameters(qb,k,beta):
    m=.5-2*.4*(qb-.5); j=k*(1-m)
    a=.28-k/2; b=qb-.5-.12-k/2
    return a,b,j,beta*(b+j)
def transition(n,s):
    x=np.arange(1,n)/n
    p=expit(np.log(x)-np.log1p(-x)+s)
    mat=binom.pmf(np.arange(n+1)[None,:],n,p[:,None])
    err=float(np.max(abs(mat.sum(axis=1)-1)))
    assert err<1e-10,err
    mat/=mat.sum(axis=1,keepdims=True)
    return mat,err
def absorb(mat,h):
    Q=np.ascontiguousarray(mat[:h-1,1:h]); r=mat[:h-1,h:].sum(axis=1)
    v=solve(np.eye(h-1)-Q,r,check_finite=False)
    residual=float(np.max(abs(v-Q@v-r)))
    assert residual<1e-10 and min(v)>-1e-10 and max(v)<1+1e-10
    return Q,r,v,residual
def poisson_est(s):
    if s<=0:return 0.
    lam=math.exp(s)
    return brentq(lambda x:-math.expm1(-lam*x)-x,1e-15,1.,xtol=1e-14)
def diffusion(n,s):
    return -math.expm1(-2*s)/(-math.expm1(-2*n*s)) if s else 1/n
def hit_cdf(Q,r,T):
    mass=np.zeros(len(r));mass[0]=1
    cum=total=0.;remaining=1.
    for t in range(1,T+1):
        cum+=float(mass@r); mass=mass@Q
        remaining=float(mass.sum())
        if t<T:total+=cum
        if remaining<1e-13:
            total+=max(0,T-1-t)*cum
            break
    assert -1e-12<=cum<=1+1e-12 and total<=T*cum+1e-9
    return cum,total,remaining,t
def benchmark(n,s):
    mat,rows=transition(n,s)
    _,_,fix,res=absorb(mat,n)
    Q,r,hit,hres=absorb(mat,math.ceil(.95*n))
    cdf,total,left,steps=hit_cdf(Q,r,HORIZON)
    assert cdf<=hit[0]+1e-10 and fix[0]<=hit[0]+1e-10
    return dict(N=n,log_selection=s,fixation=float(fix[0]),hit95_eventual=float(hit[0]),poisson=poisson_est(s),diffusion=diffusion(n,s),row_error=rows,fixation_residual=res,hit_residual=hres,hit95_by_4000=cdf,cdf_sum_0_to_3999=total,transient_mass_at_stop=left,computed_steps=steps,late_hit_approx=-math.expm1(-n*MU*total),eventual_fix_hazard_approx=-math.expm1(-n*MU*HORIZON*float(fix[0])))
def forced_A(a,b,j):
    path=[]
    for t in range(HORIZON+1):
        p=float(expit(math.log(.01/.99)+a*t))
        if p>-b/j:return np.array(path),t
        path.append(p)
    raise ValueError('threshold not crossed')
def early(qb,k,beta,n,seed_index):
    a,b,j,_=parameters(qb,k,beta);path,t=forced_A(a,b,j)
    logsel=beta*(b+j*path);v=1.
    for d in logsel[::-1]:v=-math.expm1(-math.exp(d)*v)
    survive=-math.expm1((n//100)*math.log1p(-v)) if v<1 else 1.
    rng=np.random.default_rng(SEEDS[seed_index]+1000*SETTINGS.index((qb,k,beta))+n)
    x=np.full(REPS,n//100,dtype=np.int64)
    for d in logsel:
        p=x/n;w=math.exp(d);x=rng.binomial(n,p*w/(1-p+p*w))
    return dict(qB=qb,k=k,betaB=beta,N=n,seed=SEEDS[seed_index],cross_generation=t,one_lineage_survival=v,pred_survival=survive,sim_survived=int(np.count_nonzero(x)),reps=REPS,terminal_mean_copies=float(x.mean()),branching_mean_copies=float(n//100*math.exp(float(logsel.sum()))))
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--wave24',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    raw=args.wave24.read_bytes();old=json.loads(raw);sha=hashlib.sha256(raw).hexdigest()
    assert sha=='acedabf896e8ac13649e018f1bcad9fb9a6db96d8fefd14680e48163d08fbe97'
    mat,_=transition(100,0.);_,_,v,_=absorb(mat,100)
    neutral_error=float(np.max(abs(v-np.arange(1,100)/100)));assert neutral_error<1e-10
    exact=[];early_rows=[]
    for qb,k,beta in SETTINGS:
        a,b,j,s=parameters(qb,k,beta)
        for n in (100,1000):
            row=benchmark(n,s);row.update(qB=qb,k=k,betaB=beta);exact.append(row)
        if b<0<b+j:
            for n in (1000,10000):
                es=[early(qb,k,beta,n,i) for i in (0,1)]
                oldrows=[r for key in ('main','repeat') for r in old[key] if (r['qB'],r['k'],r['betaB'],r['N'],r['mu'])==(qb,k,beta,n,0.)]
                assert len(oldrows)==2
                cross=sum(r['A_cross'] for r in oldrows);zero=sum(r['B_zero_before_A_cross'] for r in oldrows)
                early_rows.append(dict(qB=qb,k=k,betaB=beta,N=n,forced=es,coupled_cross=cross,coupled_zero_strictly_before_cross=zero,coupled_not_zero_strictly_before_cross=cross-zero,coupled_joint95=sum(r['joint95'] for r in oldrows)))
        print('completed',qb,k,beta,flush=True)
    result=dict(status='SYNTHETIC_ONLY',source_sha256=sha,numpy=np.__version__,horizon=HORIZON,mutation_rate=MU,neutral_max_error=neutral_error,exact=exact,early=early_rows)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
