import fs from 'node:fs';
// Run against original authenticated IndividualData.csv, do not copy raw data into repository.
function sha1ASCII(s){
  const n=s.length,b=new Uint8Array(((n+72)>>6)*64);for(let i=0;i<n;i++){let c=s.charCodeAt(i);if(c>127)throw Error("NONASCII");b[i]=c;}b[n]=128;
  const dv=new DataView(b.buffer);dv.setUint32(b.length-8,Math.floor(n*8/4294967296));dv.setUint32(b.length-4,n*8>>>0);
  let a0=0x67452301,b0=0xefcdab89,c0=0x98badcfe,d0=0x10325476,e0=0xc3d2e1f0;const rot=(x,n)=>(x<<n)|(x>>>(32-n)),w=new Uint32Array(80);
  for(let i=0;i<b.length;i+=64){for(let j=0;j<16;j++)w[j]=dv.getUint32(i+4*j);for(let j=16;j<80;j++)w[j]=rot(w[j-3]^w[j-8]^w[j-14]^w[j-16],1);let a=a0,c=c0,d=d0,e=e0,bv=b0;for(let j=0;j<80;j++){let f,k;if(j<20){f=(bv&c)|(~bv&d);k=0x5a827999}else if(j<40){f=bv^c^d;k=0x6ed9eba1}else if(j<60){f=(bv&c)|(bv&d)|(c&d);k=0x8f1bbcdc}else{f=bv^c^d;k=0xca62c1d6}const tmp=(rot(a,5)+f+e+k+w[j])|0;e=d;d=c;c=rot(bv,30);bv=a;a=tmp}a0=(a0+a)|0;b0=(b0+bv)|0;c0=(c0+c)|0;d0=(d0+d)|0;e0=(e0+e)|0;}
  return [a0,b0,c0,d0,e0].map(x=>(x>>>0).toString(16).padStart(8,"0")).join("");
}
function sha256ASCII(s){
 const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
 const n=s.length,b=new Uint8Array(((n+72)>>6)*64);for(let i=0;i<n;i++){let c=s.charCodeAt(i);if(c>127)throw Error("NONASCII");b[i]=c;}b[n]=128;const dv=new DataView(b.buffer);dv.setUint32(b.length-8,Math.floor(n*8/4294967296));dv.setUint32(b.length-4,n*8>>>0);
 const H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],rr=(x,n)=>(x>>>n)|(x<<(32-n)),w=new Uint32Array(64);
 for(let off=0;off<b.length;off+=64){for(let j=0;j<16;j++)w[j]=dv.getUint32(off+4*j);for(let j=16;j<64;j++){const a=w[j-15],z=w[j-2];w[j]=(w[j-16]+(rr(a,7)^rr(a,18)^(a>>>3))+w[j-7]+(rr(z,17)^rr(z,19)^(z>>>10)))>>>0;}let [a,c,d,e,f,g,h,i]=H;for(let j=0;j<64;j++){let t1=(i+(rr(f,6)^rr(f,11)^rr(f,25))+((f&g)^(~f&h))+K[j]+w[j])|0,t2=((rr(a,2)^rr(a,13)^rr(a,22))+((a&c)^(a&d)^(c&d)))|0;i=h;h=g;g=f;f=(e+t1)|0;e=d;d=c;c=a;a=(t1+t2)|0;}[a,c,d,e,f,g,h,i].forEach((x,j)=>H[j]=(H[j]+x)|0);}
 return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("");
}
function analyze(s){
 const pin="a3eec02773b391fec7af8b4713a0fdca2f52743a",size=1585319;
 if(sha1ASCII("abc")!=="a9993e364706816aba3e25717850c26c9cd0d89d"||sha256ASCII("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("hash selftest");
 if(s.length!==size||sha1ASCII("blob "+s.length+"\0"+s)!==pin)throw Error("source hash");
 const hash=sha256ASCII(s),lines=s.trimEnd().split(/\r?\n/);
 if(lines.shift()!=='"row_number","Host","Parasitoid","Temp","Rep","Individuals","HPD","Vial"')throw Error("header");
 const hosts=["BIP","BIR","PAL","PSA","PST","RUB","SUL"],paras=["A","G","L","D"],temps=[20,24,28],G=new Map(),ids=new Set();
 const count=(a,k)=>a.filter(r=>r===k).length;
 for(const l of lines){const v=l.replaceAll('"','').split(",");if(v.length!==8)throw Error("row shape");const [id,h,p,tt,rep,ind,o,vi]=v,t=+tt;
  if(ids.has(id)||!hosts.includes(h)||![...paras,"C"].includes(p)||!temps.includes(t)||!Number.isInteger(+rep)||!Number.isInteger(+ind)||+ind<1||+ind>50||!["H","P","D",""].includes(o)||(p==="C"&&o==="P"))throw Error("source value");
  ids.add(id);const key=[h,p,t].join("|"),g=G.get(vi)||{h,p,t,rep,key,slots:new Map(),rows:0};
  if(g.key!==key||g.rep!==rep)throw Error("vial labels");const slot=g.slots.get(+ind)||[];slot.push(o);g.slots.set(+ind,slot);g.rows++;G.set(vi,g);
 }
 if(ids.size!==49950||G.size!==999)throw Error("source rows");
 const cells=new Map(),issues=[];let retained=0;
 for(const [vi,g] of G){
  if(g.rows!==50)throw Error("vial size");
  const repeated=[...g.slots].filter(([k,v])=>v.length!==1),missing=Array.from({length:50},(_,i)=>i+1).filter(x=>!g.slots.has(x)),blank=[...g.slots.values()].flat().filter(o=>o==="").length;
  const bad=repeated.length>0||missing.length>0||blank>0;
  if(bad){if(vi==="85"){if(g.key!=="PSA|A|20"||g.rep!=="2"||JSON.stringify(missing)!=="[6]"||repeated.length!==1||repeated[0][0]!==7||repeated[0][1].length!==2||blank!==0)throw Error("vial 85 changed");}
   else if(vi==="179"){if(g.key!=="SUL|A|28"||g.rep!=="10"||missing.length||repeated.length||blank!==19)throw Error("vial 179 changed");}else throw Error("new source issue");
   issues.push({vial:vi,cell:g.key,rep:g.rep,missing_slots:missing,duplicate_slots:repeated.map(([k,v])=>[k,v.length]),blank_outcomes:blank});
  }
  const c=cells.get(g.key)||{host:g.h,parasitoid:g.p,temperature:g.t,all:[],strict:[]};
  const bb={};for(const k of ["H","P"]){let lo=0,hi=0;for(let i=1;i<=50;i++){const os=g.slots.get(i);if(!os){hi++;continue;}let v=os.map(o=>o===k?[1,1]:o===""?[0,1]:[0,0]);lo+=Math.min(...v.map(z=>z[0]));hi+=Math.max(...v.map(z=>z[1]));}bb[k]=[lo,hi];}
  c.all.push(bb);
  if(!bad){const vals=[...g.slots.values()].flat();const row={H:count(vals,"H"),P:count(vals,"P"),D:count(vals,"D")};if(row.H+row.P+row.D!==50)throw Error("valid vial");c.strict.push(row);retained++;}
  cells.set(g.key,c);
 }
 if(retained!==997||issues.length!==2||cells.size!==105)throw Error("amendment support");
 const avg=a=>a.reduce((x,y)=>x+y,0)/a.length;
 const C={};
 for(const [k,c] of cells){if(c.strict.length<3)throw Error("cell support");let sH=c.strict.reduce((a,x)=>a+x.H,0),sP=c.strict.reduce((a,x)=>a+x.P,0);
 C[k]={host:c.host,parasitoid:c.parasitoid,temperature:c.temperature,vials_all:c.all.length,vials_strict:c.strict.length,strict_host_adults:sH,strict_parasitoid_adults:sP,strict_dead:c.strict.length*50-sH-sP,
 H_per_initial_egg:sH/(50*c.strict.length),P_per_initial_egg:sP/(50*c.strict.length),all_vial_H_bounds:[avg(c.all.map(v=>v.H[0]))/50,avg(c.all.map(v=>v.H[1]))/50],all_vial_P_bounds:[avg(c.all.map(v=>v.P[0]))/50,avg(c.all.map(v=>v.P[1]))/50]};
 }
 // R round() uses ties to even; reproduce the published code's integer control.
 const roundEven=x=>{const a=Math.floor(x),f=x-a;return Math.abs(f-.5)<1e-12?(a%2?a+1:a):Math.round(x);};
 for(const [k,c] of cells){if(c.p==="C")continue; if(c.parasitoid==="C")continue;const ctl=C[[c.host,"C",c.temperature].join("|")];if(!ctl)throw Error("control missing");const Hc=roundEven(50*ctl.H_per_initial_egg),valid=[];
 for(const v of c.strict){const den=Math.max(v.P,v.H,Hc);if(den>0)valid.push(v.P/den);}
 C[k].host_control_emergence=ctl.H_per_initial_egg;
 C[k].host_control_minus_exposed_emergence=ctl.H_per_initial_egg-C[k].H_per_initial_egg;
 C[k].author_normalized_parasitism_mean=valid.length?avg(valid):null;
 C[k].author_normalized_parasitism_valid_vials=valid.length;
 C[k].zero_denominator_vials=c.strict.length-valid.length;
 }
 const v=(p,h,t)=>C[[h,p,t].join("|")],maxHost=(p,t)=>[...hosts].sort((a,b)=>v(p,b,t).P_per_initial_egg-v(p,a,t).P_per_initial_egg||a.localeCompare(b))[0];
 const result={};
 for(const p of paras){const a=maxHost(p,24),base=v(p,a,24).P_per_initial_egg;let by={};
 for(const t of temps){const b=maxHost(p,t),fixed=v(p,a,t).P_per_initial_egg,upper=v(p,b,t).P_per_initial_egg;
 const loss=base-fixed;
 by[t]={best_host:b,best_tested_host_recruitment_per_initial_egg:upper,ambient_best_host_recruitment_per_initial_egg:fixed,mean_of_7_hosts:avg(hosts.map(h=>v(p,h,t).P_per_initial_egg)),observed_best_vs_ambient_best_difference:upper-base,best_retention:base>0?upper/base:null,
 hypothetical_reassignment_gain:upper-fixed,fraction_of_fixed_loss_recovered:loss>0?(upper-fixed)/loss:null,all_vial_best_envelope_bounds:[Math.max(...hosts.map(h=>v(p,h,t).all_vial_P_bounds[0])),Math.max(...hosts.map(h=>v(p,h,t).all_vial_P_bounds[1]))]};}
 const b0=by[24].all_vial_best_envelope_bounds,b1=by[28].all_vial_best_envelope_bounds;
 result[p]={ambient_best_host:a,temperature:by,all_vial_warm_minus_ambient_envelope_bounds:[b1[0]-b0[1],b1[1]-b0[0]],observed_links_declining_warm:hosts.filter(h=>v(p,h,28).P_per_initial_egg<v(p,h,24).P_per_initial_egg).length};
 }
 return {status:"SECONDARY_ABSOLUTE_RECRUITMENT_OPTION_CAPACITY_COMPLETE",source:{file:"IndividualData.csv",repo:"leorjorge/LueDietBreadth",tag:"v1.2.1",git_blob:pin,sha256:hash,bytes:size,rows:49950,vials:999,cells:105,metadata_blob:"1663436ba6ed02fb8713d34ea343280e2bb43bfb",model_script_blob:"6ac6d826584455725009cef660d3679ea09779ae",license:"CC BY 4.0",dataset_doi:"10.5281/zenodo.17951000",article_doi:"10.1111/ele.70322"},audit:{strict_vials:retained,strict_rows:retained*50,flagged_vials:issues,all_cells_retained:true,min_strict_vials:Math.min(...Object.values(C).map(x=>x.vials_strict)),total_parasitoid_emergence_strict:Object.values(C).reduce((a,x)=>a+x.strict_parasitoid_adults,0),total_host_emergence_strict:Object.values(C).reduce((a,x)=>a+x.strict_host_adults,0)},cells:C,parasitoids:result,scope:"Absolute emergences per 50 initial host eggs, reported as per-egg mean. Best observed host envelope is in-sample hypothetical reallocation, not causal field switching or biological upper bound. All-vial bounds handle source anomalies only, not sampling uncertainty. No true phenological delay manipulation, no primary theta, no cross-species independence or inferential CI.",primary_theta_added:0,meta_pooled:false};
}
const file=process.argv[2];if(!file)throw Error('Usage: node script.mjs /path/to/IndividualData.csv');console.log(JSON.stringify(analyze(fs.readFileSync(file,'utf8')),null,2));
