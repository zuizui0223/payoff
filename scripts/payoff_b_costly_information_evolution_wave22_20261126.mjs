// Wave 22: exact two-population costly information strategy model. Synthetic only.
function assert(x,msg){if(!x)throw Error(msg)}

function calc(q1,q2,k,c1,c2){
 const a=q1-.5,b=q2-.5,m=.5-2*a*b,J=k*(1-m),s1=a-c1-k/2,s2=b-c2-k/2;
 return {a,b,m,J,s1,s2,baseline:[.5+k,.5+k],first:[q1-c1+k/2,.5+k/2],second:[.5+k/2,q2-c2+k/2],both:[q1-c1+k*(1-m),q2-c2+k*(1-m)]};
}

function direct(q1,q2,k,c1,c2,f1,f2){
 let v1=0,v2=0,m=0;
 for(let h=0;h<2;h++)for(let x=0;x<2;x++)for(let y=0;y<2;y++){
 const p=.5*(x===h?q1:1-q1)*(y===h?q2:1-q2),a=f1?x:0,b=f2?y:0;
 v1+=p*(+(a===h)+k*+(a===b)-f1*c1);
 v2+=p*(+(b===h)+k*+(a===b)-f2*c2);
 m+=p*+(a!==b);
 }
 return {u:[v1,v2],m};
}

function sigmoid(x){return x>=0?1/(1+Math.exp(-x)):Math.exp(x)/(1+Math.exp(x))}

function dynamics(q1,q2,k,c1,c2,dt=0.1,T=4000){
 const {s1,s2,J}=calc(q1,q2,k,c1,c2);
 let x=Math.log(.01/.99),y=x,min2=.01,tmin=0,points=[];
 const f=(x,y)=>[s1+J*sigmoid(y),s2+J*sigmoid(x)];
 const n=Math.round(T/dt);
 for(let i=0;i<=n;i++){
  if(i%Math.round(100/dt)===0||i===n)points.push({t:i*dt,p1:sigmoid(x),p2:sigmoid(y)});
  if(sigmoid(y)<min2){min2=sigmoid(y);tmin=i*dt}
  if(i===n)break;
  const a=f(x,y),b=f(x+dt*a[0]/2,y+dt*a[1]/2),c=f(x+dt*b[0]/2,y+dt*b[1]/2),d=f(x+dt*c[0],y+dt*c[1]);
  x+=dt*(a[0]+2*b[0]+2*c[0]+d[0])/6;y+=dt*(a[1]+2*b[1]+2*c[1]+d[1])/6;
 }
 return {dt,T,min2,tmin,points};
}

function audit(){
 const near=(a,b)=>Math.abs(a-b)<1e-10,E=1e-10;
 let n=0,paths=0,loss=0,bistable=0;
 for(let a=0;a<=10;a++)for(let b=0;b<=10;b++)for(let h=1;h<=10;h++)for(let i=0;i<=10;i++)for(let j=0;j<=10;j++){
 const q1=.5+a*.05,q2=.5+b*.05,k=h*.1,c1=i*.05,c2=j*.05,z=calc(q1,q2,k,c1,c2);
 const p=[direct(q1,q2,k,c1,c2,0,0),direct(q1,q2,k,c1,c2,1,0),direct(q1,q2,k,c1,c2,0,1),direct(q1,q2,k,c1,c2,1,1)];
 for(let l=0;l<4;l++)for(let x=0;x<2;x++)assert(near(p[l].u[x],[z.baseline,z.first,z.second,z.both][l][x]),"payoff");
 assert(near(p[3].m,z.m),"mismatch");
 assert(near(p[1].u[0]-p[0].u[0],z.s1)&&near(p[2].u[1]-p[0].u[1],z.s2),"rare invasion");
 assert(near(p[3].u[0]-p[2].u[0],z.s1+z.J)&&near(p[3].u[1]-p[1].u[1],z.s2+z.J),"frequency dependence");
 const sum=a=>a[0]+a[1];
 const w=sum(z.both)-sum(z.baseline);
 assert(near(w,z.s1+z.s2+2*z.J-k),"joint welfare"); // s1+s2=b1+b2-k; 2J-k = -2km+k -> actually s1+s2+2J = b1+b2+k-2km? check below
 n++;
 if(z.s1>E&&z.s2+z.J>E){paths++;if(w< -E){loss++;assert(z.both[0]>z.baseline[0]&&z.both[1]<z.baseline[1],"partner loss")}}
 if(z.s1< -E&&z.s2< -E&&z.s1+z.J>E&&z.s2+z.J>E)bistable++;
 }
 return {n,paths,loss,bistable};
}
const grid=audit();
const witness=calc(.9,.6,.5,.12,.12),simulation=dynamics(.9,.6,.5,.12,.12),fine=dynamics(.9,.6,.5,.12,.12,.05);
assert(simulation.points.at(-1).p1>.999&&simulation.points.at(-1).p2>.999,"convergence");
assert(Math.abs(simulation.min2-fine.min2)<1e-5&&Math.abs(simulation.tmin-fine.tmin)<.11,"step sensitivity");
console.log(JSON.stringify({status:"SYNTHETIC_ONLY",grid,witness,simulation,stepSensitivity:{dt:fine.dt,min2:fine.min2,tmin:fine.tmin,end:fine.points.at(-1)}},null,2));
