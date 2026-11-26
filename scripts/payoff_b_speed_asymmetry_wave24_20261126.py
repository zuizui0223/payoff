"""Wave 24: registered synthetic finite-N speed-asymmetry experiment."""
import argparse
import itertools
import json
from pathlib import Path
import numpy as np

T = 4000
REPS = 256
SEEDS = (20261126, 20361126)
CELLS = list(itertools.product((.6, .8), (.3, .5), (.25, 1., 4.), (1000, 10000), (0., 1e-5)))


def parameters(cells):
    qb,k,beta,n,mu = np.array(cells).T
    a,b = np.full_like(qb,.4),qb-.5
    b1,b2 = a-.12,b-.12
    m = .5-2*a*b
    J = k*(1-m)
    s1,s2 = b1-k/2,b2-k/2
    return qb,k,beta,n.astype(int),mu,b1,b2,m,J,s1,s2


def select(p,d,mu):
    w = np.exp(d)
    return mu+(1-2*mu)*p*w/(1-p+p*w)


def metrics(p,q,k,b1,b2,m,J):
    mismatch = .5*(p+q)-(1-m)*p*q
    deficit = (k-b1)*p+(k-b2)*q-2*J*p*q
    return mismatch,deficit


def simulate(seed,reps=REPS,stochastic=True):
    qb,k,beta,n,mu,b1,b2,m,J,s1,s2 = [x[:,None] for x in parameters(CELLS)]
    rng = np.random.default_rng(seed)
    p = np.full((len(CELLS),reps),.01)
    q = p.copy()
    crossed = np.full(p.shape,-1,dtype=int)
    zero = crossed.copy()
    joint = crossed.copy()
    sums = np.zeros((5,*p.shape))
    threshold = -s2/J
    delayed = (s2<0)&(s2+J>0)
    assert np.all(s1>0) and np.all(s2+J>0)
    for t in range(T+1):
        crossed[(crossed<0)&(p>threshold)] = t
        zero[(zero<0)&(q==0)] = t
        joint[(joint<0)&(p>=.95)&(q>=.95)] = t
        if t>0:
            mm,dd = metrics(p,q,k,b1,b2,m,J)
            sums += np.array([mm,dd,np.abs(p-q),(p>=.95)&(q<.95),q==0])
        if t==T:
            break
        pp = select(p,s1+J*q,mu)
        qq = select(q,beta*(s2+J*p),mu)
        if stochastic:
            p,q = rng.binomial(n,pp)/n,rng.binomial(n,qq)/n
        else:
            p,q = pp,qq
    mm,dd = metrics(p,q,k,b1,b2,m,J)
    out=[]
    for i,(qb0,k0,beta0,n0,mu0) in enumerate(CELLS):
        hit = joint[i]>=0
        cr = crossed[i]>=0
        de = bool(delayed[i,0])
        z = (zero[i]>=0)&(zero[i]<crossed[i])&cr
        if de and mu0==0 and stochastic:
            assert not np.any(hit&z)
        row=dict(qB=qb0,k=k0,betaB=beta0,N=n0,mu=mu0,reps=reps,
                 s1=float(s1[i,0]),s2=float(s2[i,0]),J=float(J[i,0]),
                 endpoint_deficit=float(2*k[i,0]*m[i,0]-b1[i,0]-b2[i,0]),
                 joint95=int(hit.sum()),A_cross=int(cr.sum()) if de else None,
                 B_zero_before_A_cross=int(z.sum()) if de else None,
                 median_joint95=float(np.median(joint[i,hit])) if hit.any() else None,
                 mismatch=float(sums[0,i].mean()/T),deficit=float(sums[1,i].mean()/T),
                 frequency_gap=float(sums[2,i].mean()/T),A95_Bbelow95=float(sums[3,i].mean()/T),
                 B_zero_time=float(sums[4,i].mean()/T),terminal_deficit=float(dd[i].mean()),
                 pA=float(p[i].mean()),pB=float(q[i].mean()))
        out.append(row)
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    qb,k,beta,n,mu,b1,b2,m,J,s1,s2=parameters(CELLS)
    for p,q,exp_m,exp_d in [(0,0,0,0),(1,0,.5,k-b1),(0,1,.5,k-b2),(1,1,m,2*k*m-b1-b2)]:
        mm,dd=metrics(p,q,k,b1,b2,m,J)
        assert np.allclose(mm,exp_m) and np.allclose(dd,exp_d)
    assert np.allclose(select(np.array([0.,1.]),.1,0),[0,1])
    result=dict(status='SYNTHETIC_ONLY',numpy=np.__version__,horizon=T,seeds=SEEDS,reps=REPS,
                main=simulate(SEEDS[0]),repeat=simulate(SEEDS[1]),deterministic=simulate(0,1,False))
    args.out.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    main()
