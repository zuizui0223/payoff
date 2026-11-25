import fs from 'node:fs';
// Post-outcome descriptive audit; no inference or refit.
function analyze(host,pardee){
  const mean=a=>a.reduce((s,v)=>s+v,0)/a.length;
  function subsets(a,k){if(k===0)return [[]];if(a.length<k)return [];return subsets(a.slice(1),k-1).map(x=>[a[0],...x]).concat(subsets(a.slice(1),k));}
  const pop=Object.entries(host.result.populations),alts=Object.keys(pop[0][1].host_counts_survived).filter(x=>x!=="Quercus").sort();
  if(pop.length!==4||alts.length!==8||host.audit.original_survival_total!==648)throw Error("source support changed");
  const profiles=[];
  for(const [p,v] of pop){
    const train=pop.filter(([q])=>q!==p);
    const rank=alts.map(h=>({h,n:train.reduce((a,[q,u])=>a+u.host_counts_survived[h],0)})).sort((a,b)=>b.n-a.n||a.h.localeCompare(b.h)).map(x=>x.h);
    if(JSON.stringify(rank)!==JSON.stringify(v.training_ranked_alternatives)||rank[0]!=="Salba")throw Error("ranking mismatch");
    const h=v.host_counts_survived,oak=h.Quercus/100,top=rank[0],val=ss=>h[rank.find(x=>ss.includes(x))]/100,oracle=ss=>Math.max(...ss.map(x=>h[x]/100));
    const fixed={};
    for(const k of [1,2,4]){
      const ss=subsets(alts,k),yes=ss.filter(x=>x.includes(top)),no=ss.filter(x=>!x.includes(top));
      const a=mean(yes.map(val)),b=mean(no.map(val)),m=mean(ss.map(val)),pYes=yes.length/ss.length;
      if(Math.abs(pYes-k/8)>1e-12||Math.abs(m-(pYes*a+(1-pYes)*b))>1e-12||Math.abs(m-host.result.option_policy[String(k)].per_population[p].train_ranked.survival)>1e-12)throw Error("subset arithmetic");
      fixed[k]={n_subsets:ss.length,n_top_present:yes.length,n_top_absent:no.length,top_present_survival:a,top_absent_survival:b,top_presence_difference:a-b,expected_survival:m,fraction_exceeding_oak_if_top_absent:mean(no.map(x=>+(val(x)>oak+1e-12)))};
    }
    const rm1=rank.slice(1),rm2=rank.slice(2);
    profiles.push({population:p,oak,training_top:top,training_second:rank[1],all8_ranked:val(alts),top_removed_ranked:val(rm1),top_removed_oracle:oracle(rm1),top_two_removed_ranked:val(rm2),top_two_removed_oracle:oracle(rm2),top_removed_gain_vs_oak:val(rm1)-oak,fixed_option_size:fixed});
  }
  const sums={};
  for(const k of [1,2,4]){const r=profiles.map(x=>x.fixed_option_size[k]);sums[k]={n_subsets_per_population:r[0].n_subsets,top_present_survival:mean(r.map(x=>x.top_present_survival)),top_absent_survival:mean(r.map(x=>x.top_absent_survival)),top_presence_difference:mean(r.map(x=>x.top_presence_difference)),fraction_exceeding_oak_if_top_absent:mean(r.map(x=>x.fraction_exceeding_oak_if_top_absent))};}
  const agg={};for(const k of ["oak","all8_ranked","top_removed_ranked","top_removed_oracle","top_two_removed_ranked","top_two_removed_oracle"])agg[k]=mean(profiles.map(x=>x[k]));
  agg.all8_gain_vs_oak=agg.all8_ranked-agg.oak;agg.top_removed_gain_vs_oak=agg.top_removed_ranked-agg.oak;agg.fraction_of_gain_lost_when_top_unavailable=(agg.all8_ranked-agg.top_removed_ranked)/agg.all8_gain_vs_oak;
  function diag(a,b,c,d){
    if(![a,b,c,d].every(x=>Number.isFinite(x)&&x>0))throw Error("positive means required");
    const r0=Math.log(c/a),r1=Math.log(d/b),theta=r1-r0,beta=Math.log(b/a),eta=Math.log(d/c),rho=d/a;
    if(Math.abs(eta-beta-theta)>1e-12||Math.abs(Math.log(rho)-r0-eta)>1e-12)throw Error("identity");
    return {means:{W00:a,W01:b,W10:c,W11:d},r0,r1,theta,beta,eta,recovery_relative_to_reference:rho,absolute_disturbed_gain_fraction:Math.expm1(eta),
      reference_perturbation_detrimental:r0<0,relative_attenuation_point:theta>0&&r0<0,absolute_disturbed_improvement_point:eta>0,
      point_category:r0>=0?"NO_BASELINE_LOSS_POINT":theta>0&&eta>0?"RELATIVE_AND_ABSOLUTE_GAIN_POINT":theta>0&&eta<=0?"RELATIVE_ATTENUATION_WITHOUT_ABSOLUTE_GAIN_POINT":theta<=0&&eta>0?"ABSOLUTE_GAIN_WITHOUT_RELATIVE_ATTENUATION_POINT":"NEITHER_GAIN_POINT"};
  }
  const flowers={};const mains={Claytonia:"unchanged",Delphinium:"literal_NA",Potentilla:"drop_conflict"};
  for(const [sp,modes] of Object.entries(pardee.species)){
    flowers[sp]={main:mains[sp],modes:{}};
    for(const [m,v] of Object.entries(modes)){
      const e=v.effects;
      const z=diag(e.natural_NP.estimate,e.natural_AP.estimate,e.removal_NP.estimate,e.removal_AP.estimate);
      if(Math.abs(z.theta-e.theta_snow.estimate)>1e-12)throw Error("prior contrast mismatch");
      z.prior_theta_interval=e.theta_snow.interval_95;
      flowers[sp].modes[m]=z;
    }
  }
  const synthetic=diag(.8,.1,.4,.08);
  if(!(synthetic.theta>0&&synthetic.eta<0&&synthetic.recovery_relative_to_reference<.2))throw Error("floor example");
  return {status:"POST_OUTCOME_DESCRIPTIVE_OPTION_CONCENTRATION_AND_FOUR_ARM_DIAGNOSTIC",primary_theta_added:0,meta_pooled:false,host_ablation:{profiles,aggregate:agg,same_option_count:sums,scope:"Post-outcome deterministic enumeration of the four already observed population × host survival matrices. Top host identified only in each training fold; all four folds rank Salix alba first. No bootstrap or new independence claim. Forced choice from remaining non-oak options; no timing treatment, behavior, cost or field availability."},diagnostic:{definitions:"W_db with D=reference/perturbed, B=reference/candidate buffer. beta=log(W01/W00); r0=log(W10/W00); r1=log(W11/W01); theta=r1-r0; eta=log(W11/W10)=beta+theta; rho=W11/W00. Positive theta alone does not imply absolute benefit eta>0. A baseline penalty beta<0 requires theta>−beta for absolute gain; an absolute reference target must be specified independently to diagnose functional collapse. Do not change frozen theta eligibility.",synthetic_counterexample:synthetic,secondary_snow_pollen:flowers,limits:"Point-level arithmetic on all previous Pardee species and source-quality sensitivity variants; one shared experimental study, snow removal also modifies abiotic exposure, external pollen not endogenous recourse. All original theta intervals include zero. No newly estimated uncertainty for beta, eta or rho because joint draws unavailable; do not classify statistical biological effects from signs."}};
}
const h=JSON.parse(fs.readFileSync("data/payoff_b_weir_host_option_transfer_wave15_result_20261125.json",'utf8'));
const p=JSON.parse(fs.readFileSync("data/payoff_b_pardee_source_amended_fit_result_20261125.json",'utf8'));
console.log(JSON.stringify(analyze(h,p),null,2));
