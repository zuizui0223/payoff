"""Wave 30: deterministic accessibility of reciprocal two-locus genetic gates."""
import argparse
import itertools
import json
import math
from pathlib import Path
import numpy as np

T=4000
RATES=((.005,.005),(.005,.02),(.02,.02),(.04,.04))
SETTINGS=list(itertools.product((.8,.85,.9),RATES,(False,True)))
LABELS=['00-00','00-11','11-00','11-11','unresolved']


def parameters(qb,rates,coupled):
    a=np.array([.4,qb-.5]);r=(a-.06)/.75
    g=np.array([[0.,-.06,-.375*ri**2-.06*ri,ai*ri-.375*ri**2-.06*ri-.06] for ai,ri in zip(a,r)])
    G=float(a.prod()*r.prod()) if coupled else 0.
    return r,g,G,np.array(rates)


def step(f,g,G,R):
    logw=np.broadcast_to(g,f.shape).copy()
    logw[...,3]+=G*f[...,::-1,3]
    s=f*np.exp(logw);s/=s.sum(axis=-1,keepdims=True)
    ld=s[...,0]*s[...,3]-s[...,1]*s[...,2]
    p=s+(R*ld)[...,None]*np.array([-1.,1.,1.,-1.])
    if np.min(p)<-1e-12:raise ArithmeticError('negative probability')
    p=np.maximum(p,0.);p/=p.sum(axis=-1,keepdims=True)
    return p


def corner_eigen(g,G,R,corner):
    vals=[]
    for i,j in ((0,1),(1,0)):
        gh=g[i,3]+G*corner[j]
        if corner[i]==0:
            vals.append([math.exp(g[i,1]),math.exp(g[i,2]),(1-R[i])*math.exp(gh)])
        else:
            vals.append([math.exp(g[i,1]-gh),math.exp(g[i,2]-gh),(1-R[i])*math.exp(-gh)])
    return vals


def numerical_jac(g,G,R,corner,eps=1e-7):
    f=np.zeros((2,4));f[np.arange(2),np.array(corner)*3]=1
    dims=[(i,h) for i in range(2) for h in range(4) if h!=corner[i]*3]
    A=np.empty((6,6))
    for col,(i,h) in enumerate(dims):
        v=f.copy();v[i,h]+=eps;v[i,corner[i]*3]-=eps
        out=step(v,g,G,R)
        A[:,col]=[(out[j,l]-f[j,l])/eps for j,l in dims]
    return np.sort(np.linalg.eigvals(A).real)


def analyze(qb,rates,coupled):
    r,g,G,R=parameters(qb,rates,coupled)
    corners=[];err=0.
    for corner in itertools.product((0,1),repeat=2):
        eig=corner_eigen(g,G,R,corner)
        v=np.sort(np.ravel(eig));w=numerical_jac(g,G,R,corner)
        err=max(err,float(np.max(abs(v-w))))
        corners.append({'corner':''.join(str(c) for c in corner),'eigenvalues':eig,'stable':bool(max(v)<1)})
    assert err<1e-6,err
    modes=[]
    for mode,grid in [('coupling',np.linspace(0,1,21)),('repulsion',np.linspace(0,.5,11))]:
        z=np.stack(np.meshgrid(grid,grid,indexing='ij'),axis=-1).reshape(-1,2)
        f=np.zeros((len(z),2,4))
        if mode=='coupling':f[...,0]=1-z;f[...,3]=z
        else:f[...,0]=1-2*z;f[...,1]=z;f[...,2]=z
        for t in range(T): f=step(f,g,G,R)
        residual=np.max(abs(step(f,g,G,R)-f),axis=(1,2))
        anc=f[...,0]>=.99;der=f[...,3]>=.99
        cls=np.full(len(z),4,dtype=int)
        valid=np.all(anc|der,axis=-1)
        cls[valid]=2*der[valid,0]+der[valid,1]
        assert np.allclose(f.sum(axis=-1),1)
        assert np.all(f[z[:,0]==0,0,0]==1) and np.all(f[z[:,1]==0,1,0]==1)
        shape=(len(grid),len(grid));C=cls.reshape(shape)
        diag=np.diag(C);hits=np.flatnonzero(diag==3)
        counts=np.bincount(cls,minlength=5).tolist()
        modes.append(dict(mode=mode,grid=grid.tolist(),classification=C.tolist(),counts=counts,
            residual_max=float(residual.max()),not_converged=int((residual>1e-9).sum()),
            corner_not_converged=int(((residual>1e-9)&valid).sum()),
            joint_hit_diagonal_min=float(grid[hits[0]]) if len(hits) else None,
            joint_hit_diagonal_previous=float(grid[hits[0]-1]) if len(hits) and hits[0]>0 else None,
            diagonal_labels=[LABELS[i] for i in diag],
            final_h11=f[...,3].reshape(*shape,2).tolist(),residual=residual.reshape(shape).tolist()))
    C=np.array(modes[0]['classification'])[:11,:11];P=np.array(modes[1]['classification'])
    matched=dict(n=C.size,coupling_joint=int((C==3).sum()),repulsion_joint=int((P==3).sum()),
        coupling_only=int(((C==3)&(P!=3)).sum()),repulsion_only=int(((P==3)&(C!=3)).sum()),
        both_joint=int(((C==3)&(P==3)).sum()),different_endpoint=int((C!=P).sum()))
    return dict(qB=qb,RA=rates[0],RB=rates[1],coupled=coupled,G=G,g11=g[:,3].tolist(),
        rare_log_margin=(g[:,3]+np.log1p(-R)).tolist(),
        critical_partner11=(-(g[:,3]+np.log1p(-R))/G).tolist() if G>0 else [None,None],
        corners=corners,numerical_eigen_error=err,modes=modes,matched=matched)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    rows=[]
    for qb,rates,coupled in SETTINGS:
        rows.append(analyze(qb,rates,coupled));print('done',qb,rates,coupled,rows[-1]['matched'],flush=True)
    out=dict(status='SYNTHETIC_ONLY',numpy=np.__version__,horizon=T,labels=LABELS,
        trajectories=sum(sum(m['counts']) for x in rows for m in x['modes']),settings=rows)
    args.out.write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
