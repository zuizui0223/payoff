// Wave 27: exact conditional joint best responses, synthetic only.
const clip=x=>Math.max(0,Math.min(1,x));
const CI=.06,CR=.06,EPS=1e-10;
function requireOK(ok,msg){if(!ok)throw Error(msg)}

function setup(qB,k,p,v){return {qmax:[.9,qB],a:[.4,qB-.5],k,p,v,D:(1+k)/4,E:k/4,J:2*k*.4*(qB-.5),x0:clip(v/(2*CI)),d:(1+k)/4+(p===2?CR:0),l:p===1?CR:0}}

function term(P,i,x,r,zj){const A=P.a[i]+P.J*zj;return A*x*r-P.d*r*r-P.l*r-CI*x*x+P.v*x}

function bestX(P,i,r,zj){return clip(((P.a[i]+P.J*zj)*r+P.v)/(2*CI))}

function bestR(P,i,x,zj){return clip(((P.a[i]+P.J*zj)*x-P.l)/(2*P.d))}

function bestPair(P,i,zj){
 const A=P.a[i]+P.J*zj,kink=(2*CI-P.v)/A,rs=[0,1,clip(kink)];
 const lowerCurv=A*A/(4*CI)-P.d,lowerSlope=A*P.v/(2*CI)-P.l;
 if(Math.abs(lowerCurv)>1e-15){
   const r=-lowerSlope/(2*lowerCurv);
   if(r>0&&r<1&&r<=kink+1e-12)rs.push(r);
 }
 const r=(A-P.l)/(2*P.d);
 if(r>0&&r<1&&r>=kink-1e-12)rs.push(r);
 const candidates=rs.map(r=>{let x=bestX(P,i,r,zj);return {x,r,value:term(P,i,x,r,zj)}}).sort((a,b)=>b.value-a.value||a.r-b.r);
 const b=candidates[0],baseline=term(P,i,P.x0,0,zj);
 const slope=A*P.x0-P.l;
 let local;
 if(slope< -EPS)local="STRICT_LOCAL_BARRIER";
 else if(slope>EPS)local="INFINITESIMAL_RESPONSE_FAVORED";
 else if(P.x0<1-EPS){
   if(lowerCurv< -EPS)local="STRICT_LOCAL_MAX";
   else if(lowerCurv>EPS)local="JOINT_SMALL_STEP_FAVORED";
   else local="FLAT_OR_BOUNDARY";
 }else local="STRICT_LOCAL_MAX";
 return {...b,baseline,gain:b.value-baseline,local,slope,lowerCurv,kink};
}

function payoff(P,y){
 const z=y.map(o=>o.x*o.r);
 return y.map((o,i)=>.75+P.k+term(P,i,o.x,o.r,z[1-i])-P.E*y[1-i].r**2);
}

function enumerate(P,y){
 const q=y.map((o,i)=>.5+P.a[i]*o.x);let u=[0,0],mm=0;
 for(let h=0;h<2;h++)for(let sa=0;sa<2;sa++)for(let sb=0;sb<2;sb++){
  const w=.5*(sa===h?q[0]:1-q[0])*(sb===h?q[1]:1-q[1]),acts=[sa,sb].map((s,i)=>.5+y[i].r*(s-.5)),m=(acts[0]-acts[1])**2;mm+=w*m;
  for(let i=0;i<2;i++)u[i]+=w*(1-(acts[i]-h)**2+P.k*(1-m));
 }
 return {u:u.map((v,i)=>v-CI*y[i].x**2-CR*y[i].r**P.p+P.v*y[i].x),mismatch:mm};
}

function potential(P,y){
 const z=y.map(o=>o.x*o.r);
 return y.reduce((s,o,i)=>s+P.a[i]*z[i]-P.d*o.r**2-P.l*o.r-CI*o.x**2+P.v*o.x,0)+P.J*z[0]*z[1];
}

function iterate(P,start,order,kind){
 const y=start==="baseline"?[0,1].map(()=>({x:P.x0,r:0})):[0,1].map(()=>({x:1,r:1}));
 let last=potential(P,y),n=0,converged=false,maxDrop=0;
 for(n=1;n<=2000;n++){
  let change=0;
  for(const i of order){
   const z=y[1-i].x*y[1-i].r,prev={...y[i]};
   if(kind==="joint"){const b=bestPair(P,i,z);y[i]={x:b.x,r:b.r}}
   else{y[i].x=bestX(P,i,y[i].r,z);y[i].r=bestR(P,i,y[i].x,z)}
   change=Math.max(change,Math.abs(y[i].x-prev.x),Math.abs(y[i].r-prev.r));
   const next=potential(P,y);maxDrop=Math.max(maxDrop,last-next);last=next;
  }
  if(change<1e-12){converged=true;break}
 }
 requireOK(maxDrop<1e-10,"potential decreased");
 const u=payoff(P,y),base=.75+P.k-CI*P.x0**2+P.v*P.x0,regret=y.map((o,i)=>{const z=y[1-i].x*y[1-i].r;return Math.max(0,bestPair(P,i,z).value-term(P,i,o.x,o.r,z))});
 return {kind,start,order,y,q:y.map((o,i)=>.5+P.a[i]*o.x),u,deltaU:u.map(v=>v-base),deltaSum:u[0]+u[1]-2*base,mismatch:enumerate(P,y).mismatch,potential:potential(P,y),regret,n,converged,maxDrop};
}

function audit(){
 const cells=[];let comparisons=0,potentialChecks=0,gridChecks=0,maxPayErr=0,maxPotentialErr=0,maxGridExcess=0;
 for(const qB of [.6,.8])for(const k of [.3,.5])for(const p of [1,2])for(const v of [0,.03,.06,.12]){
  const P=setup(qB,k,p,v),conditional=[];
  for(const zj of [0,.25,.5,.75,1])for(const i of [0,1]){
   const b=bestPair(P,i,zj);let grid=-Infinity;
   for(let x=0;x<=100;x++)for(let r=0;r<=100;r++){grid=Math.max(grid,term(P,i,x/100,r/100,zj));gridChecks++}
   maxGridExcess=Math.max(maxGridExcess,grid-b.value);requireOK(grid<=b.value+1e-10,"grid dominates best pair");
   conditional.push({species:i===0?"A":"B",zj,...b});
  }
  for(const x of [0,.31,1])for(const r of [0,.53,1])for(const y of [0,.37,1])for(const s of [0,.69,1]){
   const pair=[{x,r},{x:y,r:s}],u=payoff(P,pair),w=enumerate(P,pair).u;
   for(let i=0;i<2;i++){
    maxPayErr=Math.max(maxPayErr,Math.abs(u[i]-w[i]));comparisons++;
    const alt=pair.map(o=>({...o}));alt[i]={x:.71,r:.29};
    maxPotentialErr=Math.max(maxPotentialErr,Math.abs((payoff(P,alt)[i]-u[i])-(potential(P,alt)-potential(P,pair))));potentialChecks++;
   }
  }
  const eq=[];
  for(const kind of ["joint","coordinate"])for(const start of ["baseline","full"])for(const order of [[0,1],[1,0]])eq.push(iterate(P,start,order,kind));
  for(const e of eq.filter(e=>e.kind==="joint"&&e.converged))requireOK(Math.max(...e.regret)<1e-9,"joint converged with positive regret");
  cells.push({qB,k,p,v,x0:P.x0,conditional,eq});
 }
 requireOK(maxPayErr<1e-12&&maxPotentialErr<1e-12,"identity error");
 return {status:"SYNTHETIC_ONLY",contexts:cells.length,comparisons,potentialChecks,gridChecks,maxPayErr,maxPotentialErr,maxGridExcess,cells};
}
console.log(JSON.stringify(audit(),null,2));
