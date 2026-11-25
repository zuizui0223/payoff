// Wave 18: outcome-blind computational preparation. No original biological rows read.
// SPDX-License-Identifier: MIT
import {readFileSync} from "node:fs";
import {createHash} from "node:crypto";
import {join} from "node:path";
import {pathToFileURL} from "node:url";
const EXPECTED_FILES={
  "all.dat.nsbNov24.csv": [
    314569,
    "81e85cbe6d32d16b2cb17a2dcffc64a34b3e8c6e526b4a629a1d46ca642f1288"
  ],
  "all.dat.sbNov24.csv": [
    255167,
    "7c4347a512ee249d9a4ec3fa5f731f4526b8a57ce0127aa4461c7ea1b110a076"
  ],
  "README-all.dat.nsbNov24.csv": [
    4644,
    "230af6578f439461c463ad6006421c68173b97229a3ef666fb4b68806d9c2099"
  ],
  "README-all.dat.sbNov24.csv": [
    4648,
    "a8f13ffa1170f9dc948534b65ba6fdd2721cf927723fd4eef1d620dca50a70dd"
  ]
};
const DELAYS=[0,2,4,6], HOSTS=["birchii","sulfurigaster","mixture"], TEMPS=[24,28], FOODS=["low","high"], WASPS=["Asobara","Ganaspis"], COMPARATORS=["equal_density","birchii","sulfurigaster"];
const METRICS=["r0","r1","theta","beta","eta","logR","R","absoluteBenefit","absoluteResidual","additiveInteraction"];
function requireCondition(ok,message){if(!ok)throw new Error(message);}

function average(xs){requireCondition(xs.length>0,"empty mean");return xs.reduce((s,x)=>s+x,0)/xs.length;}

function logRatio(a,b){return a>0&&b>0?Math.log(a)-Math.log(b):null;}

function contrasts(w00,w10,w01,w11){
  requireCondition([w00,w10,w01,w11].every(x=>Number.isFinite(x)&&x>=0),"invalid arm mean");
  const r0=logRatio(w10,w00),r1=logRatio(w11,w01),beta=logRatio(w01,w00),eta=logRatio(w11,w10),logR=logRatio(w11,w00);
  const theta=r0===null||r1===null?null:r1-r0;
  return {w00,w10,w01,w11,r0,r1,theta,beta,eta,logR,R:w00>0?w11/w00:null,absoluteBenefit:w11-w10,absoluteResidual:w11-w00,additiveInteraction:(w11-w01)-(w10-w00),
    detrimentalReference:r0===null?null:r0<0,relativeAttenuation:r0===null||theta===null?null:r0<0&&theta>0,absoluteImprovement:w11>w10};
}

function validateAndGroup(rows){
  requireCondition(Array.isArray(rows)&&rows.length>0,"HOLD: no normalized vial rows");
  const seen=new Set(),blockSet=new Set(),groups=new Map();
  for(const r of rows){
    requireCondition(typeof r.block==="string"&&r.block.trim()&&typeof r.vial==="string"&&r.vial.trim(),"HOLD: missing verified block/vial identity");
    const vk=JSON.stringify([r.block,r.vial]);
    requireCondition(!seen.has(vk),"HOLD: duplicate canonical vial identity");seen.add(vk);
    requireCondition(TEMPS.includes(r.temperature)&&FOODS.includes(r.food)&&WASPS.includes(r.parasitoid)&&DELAYS.includes(r.delay)&&HOSTS.includes(r.host),"HOLD: unmapped treatment");
    requireCondition(Number.isSafeInteger(r.emerged)&&r.emerged>=0&&Number.isSafeInteger(r.females)&&r.females>0,"HOLD: missing/invalid actual counts or female denominator");
    const expected=r.host==="birchii"?[100,0]:r.host==="sulfurigaster"?[0,100]:[50,50];
    requireCondition(r.eggsB===expected[0]&&r.eggsS===expected[1],"HOLD: equal initial host density/composition not verified");
    blockSet.add(r.block);
    const k=JSON.stringify([r.temperature,r.food,r.parasitoid,r.block,r.delay,r.host]);
    if(!groups.has(k))groups.set(k,[]);
    groups.get(k).push(r.emerged/r.females);
  }
  const blocks=[...blockSet].sort();
  requireCondition(blocks.length===5,"HOLD: expected five documented time blocks; no post-outcome deletion");
  const support=[];
  for(const t of TEMPS)for(const f of FOODS)for(const p of WASPS)for(const b of blocks)for(const d of DELAYS)for(const h of HOSTS){
    const k=JSON.stringify([t,f,p,b,d,h]),v=groups.get(k);
    requireCondition(v&&v.length,"HOLD: incomplete factorial support "+k);
    support.push({temperature:t,food:f,parasitoid:p,block:b,delay:d,host:h,vials:v.length});
    groups.set(k,average(v));
  }
  return {blocks,groups,support};
}

function* allResamples(n){
  const ids=new Array(n).fill(0);
  for(let j=0;j<n**n;j++){
    yield ids.slice();
    for(let k=n-1;k>=0;k--){ids[k]++;if(ids[k]<n)break;ids[k]=0;}
  }
}

function quantile(xs,p){
  const v=xs.slice().sort((a,b)=>a-b),k=(v.length-1)*p,i=Math.floor(k);
  return v[i]+(v[Math.min(i+1,v.length-1)]-v[i])*(k-i);
}

function describeDraws(xs){
  const undef=xs.filter(x=>x===null||!Number.isFinite(x)).length;
  return {draws:xs.length,undefined:undef,interval:undef?null:[quantile(xs,.025),quantile(xs,.975)],status:undef?"HOLD_UNDEFINED_IN_RESAMPLING":"CONDITIONAL_BLOCK_RESAMPLING_SENSITIVITY"};
}

function jointCovariance(draws){
  if(!draws.length||draws.some(r=>r.some(x=>x===null||!Number.isFinite(x))))return null;
  const m=draws[0].map((_,i)=>average(draws.map(r=>r[i])));
  return m.map((a,i)=>m.map((b,j)=>average(draws.map(r=>(r[i]-a)*(r[j]-b)))));
}

function analyzeNormalized(rows){
  const {blocks,groups,support}=validateAndGroup(rows);
  const strata=[];
  for(const t of TEMPS)for(const f of FOODS)for(const p of WASPS){
    const specs=DELAYS.slice(1).flatMap(d=>COMPARATORS.map(c=>({delay:d,comparator:c})));
    function evaluate(indices){
      const mean=(d,h)=>average(indices.map(i=>groups.get(JSON.stringify([t,f,p,blocks[i],d,h]))));
      const comparator=(d,c)=>c==="equal_density"?(mean(d,"birchii")+mean(d,"sulfurigaster"))/2:mean(d,c);
      return specs.map(({delay:d,comparator:c})=>contrasts(comparator(0,c),comparator(d,c),mean(0,"mixture"),mean(d,"mixture")));
    }
    const point=evaluate(blocks.map((_,i)=>i));
    const draws=[...allResamples(blocks.length)].map(evaluate);
    const estimates=specs.map((s,i)=>({...s,primaryCandidate:s.comparator==="equal_density",point:point[i],
      sensitivity:Object.fromEntries(METRICS.map(k=>[k,describeDraws(draws.map(r=>r[i][k]))])),
      jointLogMetrics:["r0","r1","theta","beta","eta","logR"],
      jointLogCovariance:jointCovariance(draws.map(r=>["r0","r1","theta","beta","eta","logR"].map(k=>r[i][k])))}));
    const thetaDraws=draws.map(r=>r.map(x=>x.theta));
    strata.push({temperature:t,food:f,parasitoid:p,blockCount:blocks.length,bootstrapDraws:draws.length,estimates,
      thetaOrder:specs,thetaCovariance:jointCovariance(thetaDraws)});
  }
  return {status:"NORMALIZED_ESTIMATOR_ONLY_NOT_PRIMARY_ADMISSION",sourceOutcomeClaim:false,vialCount:rows.length,blockCount:blocks.length,support,strata,
    notes:["All five blocks weighted equally; vial rates equally weighted within block/cell.","All 5^5 block resamples, shared across contrasts within stratum; percentiles are conditional sensitivities, not calibrated confidence intervals.","No cross-stratum independence or population replication assumed.","Missing or zero arm means do not receive pseudocounts; undefined log intervals/covariance withheld. Absolute contrasts retained. Source normalization and design/eligibility require separate review."]};
}

function syntheticFixture(){
  const a=[];
  for(let i=1;i<=5;i++)for(const temperature of TEMPS)for(const food of FOODS)for(const parasitoid of WASPS)for(const delay of DELAYS)for(const host of HOSTS){
    const mixed=host==="mixture";
    let emerged=mixed?[4,3,2,0][delay/2]:[20,10,8,6][delay/2];
    const [eggsB,eggsS]=host==="birchii"?[100,0]:host==="sulfurigaster"?[0,100]:[50,50];
    a.push({block:"b"+i,vial:[temperature,food,parasitoid,delay,host].join("/"),temperature,food,parasitoid,delay,host,eggsB,eggsS,females:2,emerged});
  }
  return a;
}

function selfTest(){
  let passed=0;
  function check(ok,m){requireCondition(ok,"test failed: "+m);passed++;}
  function near(a,b){return Math.abs(a-b)<1e-11;}
  function throws(f){try{f();return false;}catch(e){return String(e).includes("HOLD");}}
  const c=contrasts(10,5,2,1.5);
  check(near(c.theta,Math.log(1.5)),"theta");
  check(near(c.eta,Math.log(.3))&&near(c.beta+c.theta,c.eta),"eta identity");
  check(near(c.R,.15)&&near(c.logR,c.r0+c.eta),"absolute retention");
  check(c.relativeAttenuation&&!c.absoluteImprovement,"attenuation not rescue");
  const z=contrasts(10,5,2,0);check(z.theta===null&&z.R===0&&z.absoluteBenefit===-5,"zero without pseudocount");
  const a=syntheticFixture(),out=analyzeNormalized(a);
  check(out.vialCount===480&&out.strata.length===8&&out.support.length===480,"complete design");
  check(out.strata.every(s=>s.bootstrapDraws===3125&&s.estimates.length===9),"exact joint resampling");
  const q=out.strata[0].estimates[0];
  check(near(q.point.theta,Math.log(1.5))&&near(q.point.eta,Math.log(.3)),"arm arithmetic");
  check(q.sensitivity.theta.undefined===0&&q.sensitivity.theta.interval.every(x=>near(x,q.point.theta)),"constant synthetic sensitivity");
  check(out.strata[0].estimates[6].sensitivity.theta.undefined===3125&&out.strata[0].estimates[6].sensitivity.R.interval[0]===0,"all-zero arm log hold");
  check(throws(()=>validateAndGroup(a.slice(1))),"incomplete cell");
  check(throws(()=>validateAndGroup([...a,a[0]])),"duplicate vial");
  check(throws(()=>validateAndGroup([{...a[0],females:0},...a.slice(1)])),"missing denominator");
  check(throws(()=>validateAndGroup([{...a[0],eggsB:99},...a.slice(1)])),"density mismatch");
  check(throws(()=>validateAndGroup([{...a[0],emerged:-1},...a.slice(1)])),"invalid count");
  const v=a.map(r=>r.host==="mixture"&&r.delay===4&&r.block==="b1"?{...r,emerged:0}:r);
  const o=analyzeNormalized(v);
  const e=o.strata[0].estimates[3];
  check(e.sensitivity.theta.undefined===1&&e.sensitivity.theta.interval===null&&e.jointLogCovariance===null,"one undefined block resample prevents conditional log interval");
  check(e.sensitivity.R.undefined===0&&e.sensitivity.R.interval!==null,"absolute ratio remains estimable");
  const varied=a.map(r=>r.host==="mixture"&&r.delay===2&&r.block==="b1"?{...r,emerged:5}:r);
  const vv=analyzeNormalized(varied).strata[0].estimates[0];
  check(vv.jointLogCovariance!==null&&vv.jointLogCovariance[2][2]>0,"joint uncertainty nonzero");
  check(near(vv.jointLogCovariance[2][4],vv.jointLogCovariance[2][2]),"joint covariance identity");
  return {status:"SYNTHETIC_ONLY",passed};
}

export function verifyOriginals(dir){
  const results=Object.entries(EXPECTED_FILES).map(([name,[bytes,digest]])=>{
    try{
      const raw=readFileSync(join(dir,name));
      const actual=createHash("sha256").update(raw).digest("hex");
      return {name,bytes:raw.length,sha256:actual,status:raw.length===bytes&&actual===digest?"VERIFIED":"HOLD_DIGEST_OR_SIZE_MISMATCH"};
    }catch(e){return {name,status:"HOLD_MISSING_OR_UNREADABLE"};}
  });
  return {status:results.every(x=>x.status==="VERIFIED")?"ORIGINAL_BYTES_VERIFIED_SCHEMA_REVIEW_REQUIRED":"HOLD_ORIGINAL_BYTES",files:results};
}
export {contrasts,analyzeNormalized,selfTest};
// Raw-to-vial mapping is deliberately not implemented until both original
// dictionaries and actual rows can be checked. Importing the helper is not
// authorization to promote any effect to the primary synthesis.
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
  const arg=process.argv[2];
  if(arg==="--self-test")console.log(JSON.stringify(selfTest(),null,2));
  else if(arg==="--check-source"&&process.argv[3]){
    const result=verifyOriginals(process.argv[3]);console.log(JSON.stringify(result,null,2));
    if(result.status.startsWith("HOLD"))process.exitCode=2;
  }else{console.error("Usage: node script.mjs --self-test | --check-source ORIGINAL_DIRECTORY");process.exitCode=2;}
}
