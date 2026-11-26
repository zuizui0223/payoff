// Wave 26 continuous reaction norms, synthetic only.
function check(ok,msg){if(!ok)throw Error(msg)}

function params(qB,k,lambda,mode,cost){
  const q=[.9,qB],c=[.12,.12],p11=(1-lambda)*q[0]*q[1]+lambda*Math.min(...q),rho=4*p11-2*q[0]-2*q[1]+1;
  const centered=mode==="centered",base=(centered?.75:.5)+k;
  const l=q.map(v=>v-(centered?.5:0)),d=(1+k)/(centered?4:2),e=k/(centered?4:2),j=centered?k*rho/2:k*(1+rho)/2;
  const A=l.map((v,i)=>v-(cost==="linear"?c[i]:0)),D=c.map(v=>d+(cost==="quadratic"?v:0));
  return {q,c,p11,rho,k,lambda,mode,cost,base,l,d,e,j,A,D};
}

function fee(P,x,i){return P.c[i]*(P.cost==="linear"?x:P.cost==="quadratic"?x*x:x>0?1:0)}

function payoff(P,x){
  const [a,b]=x;
  return [0,1].map(i=>P.base+P.l[i]*x[i]-P.d*x[i]**2+P.j*a*b-P.e*x[1-i]**2-fee(P,x[i],i));
}

function enumPayoff(P,x){
  const [q1,q2]=P.q,p=P.p11,prob=[p,q1-p,q2-p,1-q1-q2+p],correct=[[1,1],[1,0],[0,1],[0,0]],u=[0,0];let mismatch=0;
  for(let h=0;h<2;h++)for(let z=0;z<4;z++){
    const a=correct[z].map((c,i)=>{const s=c?h:1-h;return P.mode==="anchored"?x[i]*s:.5+x[i]*(s-.5)});
    const w=prob[z]/2,mm=(a[0]-a[1])**2;
    mismatch+=w*mm;
    for(let i=0;i<2;i++)u[i]+=w*(1-(a[i]-h)**2+P.k*(1-mm));
  }
  return {u:u.map((v,i)=>v-fee(P,x[i],i)),mismatch};
}

function potential(P,x){
  return P.A[0]*x[0]+P.A[1]*x[1]-P.D[0]*x[0]**2-P.D[1]*x[1]**2+P.j*x[0]*x[1]-(P.cost==="fixed"?P.c.reduce((s,c,i)=>s+(x[i]>0?c:0),0):0);
}

function br(P,i,y){
  const v=P.A[i]+P.j*y,r=Math.min(1,Math.max(0,v/(2*P.D[i])));
  const g=(x)=>v*x-P.D[i]*x*x-(P.cost==="fixed"&&x>0?P.c[i]:0);
  return {x:r>0&&g(r)>0?r:0,best:Math.max(0,g(r)),gain:g};
}

function candidates(P){
  const a=[];
  for(const t0 of [0,1,2])for(const t1 of [0,1,2]){
    // 0=zero, 1=interior, 2=one. Fixed-cost zero is an inactive support.
    let x=[t0===2?1:0,t1===2?1:0];
    if(t0===1&&t1===1){
      const det=4*P.D[0]*P.D[1]-P.j**2;
      x=[(2*P.D[1]*P.A[0]+P.j*P.A[1])/det,(2*P.D[0]*P.A[1]+P.j*P.A[0])/det];
    }else if(t0===1)x[0]=(P.A[0]+P.j*x[1])/(2*P.D[0]);
    else if(t1===1)x[1]=(P.A[1]+P.j*x[0])/(2*P.D[1]);
    if([t0,t1].some((t,i)=>t===1&&!(x[i]>1e-12&&x[i]<1-1e-12)))continue;
    const reg=x.map((v,i)=>{const b=br(P,i,x[1-i]);return b.best-b.gain(v)});
    const e=enumPayoff(P,x);
    a.push({x,potential:potential(P,x),regret:reg,u:payoff(P,x),mismatch:e.mismatch});
  }
  return a;
}

function audit(){
  const out=[];let maxPay=0,maxPotential=0,maxGridExcess=0,maxRegret=0,nPay=0,nPotential=0,nEndpoint=0,nGrid=0;
  for(const qB of [.6,.8])for(const k of [.3,.5])for(const lambda of [0,.5,1])for(const mode of ["anchored","centered"])for(const cost of ["linear","quadratic","fixed"]){
    const P=params(qB,k,lambda,mode,cost),det=4*P.D[0]*P.D[1]-P.j**2;
    check(det>0,"strict concavity on positive support");
    const cs=candidates(P),mx=Math.max(...cs.map(c=>c.potential)),eq=cs.filter(c=>Math.max(...c.regret)<=1e-10),opt=cs.filter(c=>Math.abs(c.potential-mx)<=1e-10);
    check(eq.length>=1&&opt.every(c=>eq.includes(c)),"potential maximizers must be Nash");
    if(cost!=="fixed")check(eq.length===1,"unique smooth equilibrium");
    for(const c of eq)maxRegret=Math.max(maxRegret,...c.regret);
    const originRegret=[br(P,0,0).best,br(P,1,0).best],originGrad=P.A;
    const xgrid=[0,.01,.19,.5,.81,1];
    for(const x of xgrid)for(const y of xgrid){
      const a=[x,y],u=payoff(P,a),v=enumPayoff(P,a);
      maxPay=Math.max(maxPay,Math.abs(u[0]-v.u[0]),Math.abs(u[1]-v.u[1]));nPay+=2;
      for(let i=0;i<2;i++){
        const b=a.slice();b[i]=.37;
        const err=Math.abs((payoff(P,b)[i]-u[i])-(potential(P,b)-potential(P,a)));
        maxPotential=Math.max(maxPotential,err);nPotential++;
      }
      if(mode==="anchored"&&lambda===0&&[0,1].includes(x)&&[0,1].includes(y)){
        const m=.5-2*(P.q[0]-.5)*(P.q[1]-.5),w=x&&y?1-m:x||y?.5:1;
        // endpoint accuracy at historical C = .5, at F = q.
        for(let i=0;i<2;i++){
          const expected=(a[i]?P.q[i]-.12:.5)+k*w;
          check(Math.abs(u[i]-expected)<1e-12,"Wave22 endpoint");nEndpoint++;
        }
      }
    }
    let gridMax=-Infinity;
    for(let a=0;a<=100;a++)for(let b=0;b<=100;b++){gridMax=Math.max(gridMax,potential(P,[a/100,b/100]));nGrid++}
    maxGridExcess=Math.max(maxGridExcess,gridMax-mx);
    check(gridMax<=mx+1e-10,"discrete grid exceeds solution");
    const summarize=c=>({...c,deltaU:c.u.map(v=>v-P.base),deltaSum:c.u[0]+c.u[1]-2*P.base});
    out.push({qB,k,lambda,rho:P.rho,mode,cost,base:P.base,originGrad,originRegret,originNE:originRegret.every(v=>v<=1e-10),nNE:eq.length,equilibria:eq.map(summarize),potentialMax:opt.map(summarize),gridMax});
  }
  check(maxPay<1e-12&&maxPotential<1e-12,"enumeration or potential identity");
  return {status:"SYNTHETIC_ONLY",contexts:out.length,nPay,nPotential,nEndpoint,nGrid,maxPay,maxPotential,maxGridExcess,maxRegret,cells:out};
}
console.log(JSON.stringify(audit(),null,2));
