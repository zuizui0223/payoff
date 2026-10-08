#!/usr/bin/env python3
"""PAYOFF-B exploratory goose staging-duration incremental fitness forecast.

The preread contract is
docs/PAYOFF_B_GOOSE_STAGING_ENERGY_FITNESS_PREDICTION_CONTRACT_20261008.md.
Not a causal model, not a new proof of Schindler et al. breeding mechanisms.

Input is pinned author-hosted source, checksum matched to Dryad v5. Five
out-of-year folds; no outcome-driven variables, lambda tuning or exclusions.
Only aggregated results are printed or saved, not individual animal records.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from urllib.request import Request, urlopen

COMMIT = "2171bcd36bf37022c8716e15c0f75412103b0f3f"
URL = (
    "https://raw.githubusercontent.com/aschindler23/"
    "Schindler_etal_2024_ProcB/" + COMMIT + "/spring_data.csv"
)
DRYAD_SHA = "9ef98e6b5e979e93476ed076a018db13bdf03aab6dcc5ca728b5fd866e79c1bd"
FEATURESETS = {
    "M0_calendar": ("year", "stage3", "stage6"),
    "M1_energy": ("year", "stage3", "stage6", "staging_feeding", "staging_odba"),
    "M2_duration": ("year", "stage3", "stage6", "staging_feeding",
                    "staging_odba", "staging_duration"),
}
RIDGE = 2.0
BOOT = 4000
SEED = 20261008


def _sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def _solve(a, b):
    n = len(b)
    aug = [a[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        i_max = max(range(col, n), key=lambda i: abs(aug[i][col]))
        aug[col], aug[i_max] = aug[i_max], aug[col]
        if abs(aug[col][col]) < 1e-9:
            raise ValueError("source fit underidentified despite penalty")
        divisor = aug[col][col]
        for j in range(col, n+1):
            aug[col][j] /= divisor
        for i in range(n):
            if i == col:
                continue
            fac = aug[i][col]
            for j in range(col, n+1):
                aug[i][j] -= fac * aug[col][j]
    return [aug[i][n] for i in range(n)]


def _ridge_logistic(x, outcomes, penalty=RIDGE):
    if len(x) < 15 or len(x) != len(outcomes) or len(set(outcomes)) != 2:
        raise ValueError("training fold insufficient to estimate binary success")
    p = len(x[0])
    coefs = [0.0] * p
    for _ in range(65):
        grad = [0.0]*p
        hess = [[0.0]*p for i in range(p)]
        for row, y in zip(x,outcomes):
            pred = _sigmoid(sum(b*v for b,v in zip(coefs,row)))
            wi = max(1e-10, pred*(1.0-pred))
            for j in range(p):
                grad[j] += row[j]*(pred-y)
                for k in range(j+1):
                    hess[j][k] += row[j]*row[k]*wi
        for j in range(p):
            if j>0:
                grad[j]+=penalty*coefs[j]
                hess[j][j]+=penalty
            for k in range(j):
                hess[k][j]=hess[j][k]
        delta=_solve(hess,grad)
        for j in range(p):
            coefs[j]-=delta[j]
        if max(abs(d) for d in delta)<1e-8:
            break
        if max(abs(b) for b in coefs)>100:
            raise ValueError("logistic coefficients diverged")
    return coefs


def _csv_rows(raw: bytes):
    canonical=raw.replace(b"\r\n",b"\n").replace(b"\n",b"\r\n")
    if hashlib.sha256(canonical).hexdigest()!=DRYAD_SHA:
        raise ValueError("author file did not match Dryad v5 SHA256")
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    fields={
        "id","year","sub_season","first_day","breeding_success",
        "breeding_outcome","num_feed_fixes","num_ACC_fixes","log_ODBA"
    }
    if not fields.issubset(set(reader.fieldnames or [])):
        raise ValueError("missing registered predictors or outcome columns")
    grouped=defaultdict(dict)
    lines=0
    for rec in reader:
        lines+=1
        try:
            bird=int(rec["id"])
            year=int(rec["year"])
            stage=int(rec["sub_season"])
            day=float(rec["first_day"])
            success=int(rec["breeding_success"])
            outcome=int(rec["breeding_outcome"])
            feed=int(rec["num_feed_fixes"])
            fixes=int(rec["num_ACC_fixes"])
            odba=float(rec["log_ODBA"])
        except (ValueError,TypeError) as exc:
            raise ValueError("source contains missing or mistyped registered fields") from exc
        if (not 1<=year<=5 or not 1<=stage<=6 or
            not 0<day<=366 or success not in (0,1) or
            not 1<=outcome<=3 or feed<0 or fixes<=0 or feed>fixes or
            not math.isfinite(odba)):
            raise ValueError("invalid source grain/outcome/energy range")
        if stage in grouped[(bird,year)]:
            raise ValueError("duplicate bird-year-stage")
        grouped[(bird,year)][stage]=(day,success,outcome,feed,fixes,odba)
    if lines!=642 or len(grouped)!=107 or len({k[0] for k in grouped})!=49:
        raise ValueError("source support drift")
    out=[]
    for (bird,year),stage in sorted(grouped.items()):
        if set(stage)!=set(range(1,7)):
            raise ValueError("incomplete bird-year")
        days=[stage[j][0] for j in range(1,7)]
        if any(days[i]>=days[i+1] for i in range(5)):
            raise ValueError("subseason dates not strictly increasing")
        success={stage[j][1] for j in stage}
        outcome={stage[j][2] for j in stage}
        if len(success)!=1 or len(outcome)!=1:
            raise ValueError("breeding labels conflict across stages")
        y=success.pop()
        o=outcome.pop()
        if (o==1)!=(y==1):
            raise ValueError("source binary and categorical fertility disagree")
        stage3,stage5,stage6=stage[3][0],stage[5][0],stage[6][0]
        feed_fraction=(stage[3][3]+stage[4][3])/(stage[3][4]+stage[4][4])
        out.append({
            "bird":bird,"year":year,"response":y,"category":o,
            "stage3":stage3,"stage6":stage6,
            "staging_duration":stage5-stage3,
            "staging_feeding":feed_fraction,
            "staging_odba":(stage[3][5]+stage[4][5])/2.0
        })
    return out


def _design(train,test,features):
    mus={}
    sds={}
    for feature in features:
        xs=[float(r[feature]) for r in train]
        m=sum(xs)/len(xs)
        sd=math.sqrt(sum((v-m)**2 for v in xs)/len(xs))
        if sd<1e-10 or not math.isfinite(sd):
            raise ValueError("source training feature has zero/invalid variance")
        mus[feature]=m
        sds[feature]=sd
    def build(rows):
        return [[1.0]+[(float(r[f])-mus[f])/sds[f] for f in features]
                for r in rows]
    return build(train),build(test)


def _loss(y,p):
    p=max(1e-9,min(1-1e-9,p))
    return -(y*math.log(p)+(1-y)*math.log(1-p))


def _mean(xs):
    return sum(xs)/len(xs)


def _percentile(xs,p):
    arr=sorted(xs)
    pos=(len(arr)-1)*p
    j=int(pos)
    k=min(j+1,len(arr)-1)
    return arr[j]*(1-(pos-j))+arr[k]*(pos-j)


def calculate(rows):
    preds=defaultdict(list)
    all_rows=[]
    for heldyear in range(1,6):
        train=[r for r in rows if r["year"]!=heldyear]
        test=[r for r in rows if r["year"]==heldyear]
        if len(train)<50 or len(test)<7 or len(set(r["response"] for r in train))!=2:
            raise ValueError("year-fold outcome support insufficient")
        fitted={}
        for name,features in FEATURESETS.items():
            xtrain,xtest=_design(train,test,features)
            beta=_ridge_logistic(xtrain,[r["response"] for r in train])
            fitted[name]=[_sigmoid(sum(b*v for b,v in zip(beta,x)))
                          for x in xtest]
        for i,row in enumerate(test):
            x={"bird":row["bird"],"year":heldyear,"y":row["response"]}
            for name in FEATURESETS:
                prob=fitted[name][i]
                x[name+"_loss"]=_loss(row["response"],prob)
                x[name+"_brier"]=(prob-row["response"])**2
                x[name+"_prob"]=prob
            all_rows.append(x)
    if len(all_rows)!=len(rows):
        raise ValueError("held-year predictions did not cover all supplied bird-years")
    compare={}
    for baseline,new,tag in [
        ("M0_calendar","M1_energy","energy_given_calendar"),
        ("M1_energy","M2_duration","duration_given_energy"),
    ]:
        diffs=[r[baseline+"_loss"]-r[new+"_loss"] for r in all_rows]
        briers=[r[baseline+"_brier"]-r[new+"_brier"] for r in all_rows]
        bybird=defaultdict(list)
        for r,d in zip(all_rows,diffs):
            bybird[r["bird"]].append(d)
        birds=list(bybird.keys())
        rng=random.Random(SEED+len(tag))
        boot=[]
        for _ in range(BOOT):
            samples=[bybird[rng.choice(birds)] for i in range(len(birds))]
            boot.append(_mean([z for x in samples for z in x]))
        years=[]
        for year in range(1,6):
            sub=[r for r in all_rows if r["year"]==year]
            years.append({
                "year_code":year,"bird_years":len(sub),
                "mean_oof_logloss_improvement":_mean([
                    r[baseline+"_loss"]-r[new+"_loss"] for r in sub])
            })
        compare[tag]={
            "baseline":baseline,
            "augmented":new,
            "positive_gain_means_augmented_model_better":True,
            "mean_oof_logloss_gain":_mean(diffs),
            "mean_oof_brier_gain":_mean(briers),
            "bird_cluster_validation_only_95_interval":[
                _percentile(boot,.025),_percentile(boot,.975)],
            "year_score_detail":years,
            "positive_calendar_years":sum(v["mean_oof_logloss_improvement"]>0 for v in years)
        }
    categories=defaultdict(int)
    for r in rows:
        categories[str(r["category"])]+=1
    return {
        "status":"POST_PUBLISHED_OUTCOME_EXPLORATORY_PREDICTION_NOT_CAUSAL",
        "source_commit":COMMIT,
        "verified_dryad_sha256":DRYAD_SHA,
        "bird_years":len(rows),
        "birds":len({r["bird"] for r in rows}),
        "success_count":sum(r["response"] for r in rows),
        "failure_or_deferral_count":sum(1-r["response"] for r in rows),
        "outcome_category_birdyears":dict(sorted(categories.items())),
        "original_article_total_reported":108,
        "unresolved_published_vs_source_birdyear_difference":1,
        "year_code_sample_size":{str(i):sum(r["year"]==i for r in rows)
                                  for i in range(1,6)},
        "ridge_penalty":RIDGE,
        "year_blocked_outcome_predictions":True,
        "features":{k:list(v) for k,v in FEATURESETS.items()},
        "oof_model_logloss":{
            model:_mean([r[model+"_loss"] for r in all_rows])
            for model in FEATURESETS},
        "oof_model_brier":{
            model:_mean([r[model+"_brier"] for r in all_rows])
            for model in FEATURESETS},
        "probability_range":{
            model:[min(r[model+"_prob"] for r in all_rows),
                   max(r[model+"_prob"] for r in all_rows)]
            for model in FEATURESETS},
        "paired_comparisons":compare,
        "claim_limit":"No action feasibility, cue perception, individual resource optimum or causal cost identified",
        "published_source_author_model_already_includes_arrival_and_energy":True
    }


def synthetic_test():
    # Known source-free toy, binary process shaped by a measured risk proxy.
    rng=random.Random(20261008)
    rows=[]
    for yr in range(1,6):
        for bird in range(1,26):
            f=(bird%9)*.03+.3+yr*.004
            o=(bird%7)*.05-.6
            st=90+((bird*11+yr)%17)
            dur=20+((bird*3+yr)%12)
            arrival=st+dur+5
            pr=_sigmoid(-1+.5*(f-.4)/.1-.8*(o+.5)/.2)
            y=int(rng.random()<pr)
            rows.append({
                "bird":bird,"year":yr,"response":y,"category":1 if y else 2,
                "stage3":st,"stage6":arrival,"staging_duration":dur,
                "staging_feeding":f,"staging_odba":o
            })
    result=calculate(rows)
    assert result["bird_years"]==125
    assert len(result["paired_comparisons"]["duration_given_energy"]["year_score_detail"])==5
    assert all(math.isfinite(x) for x in result["oof_model_logloss"].values())
    print("PAYOFF_B_GOOSE_STAGING_FITNESS_MODEL_SYNTHETIC_PASS")


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--output",default="outputs/payoff_b_goose_staging_energy_fitness_prediction.json")
    args=parser.parse_args()
    if args.self_test:
        synthetic_test()
    else:
        req=Request(URL,headers={"User-Agent":"PAYOFF-B/outcome-audit","Accept":"text/csv"})
        with urlopen(req,timeout=30) as response:
            data=response.read(200000)
        result=calculate(_csv_rows(data))
        dest=Path(args.output)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        print("PAYOFF_B_GOOSE_STAGING_ENERGY_FITNESS_EXPLORATORY_RESULT")
        print(json.dumps(result,sort_keys=True))
        print("NOT A DEMONSTRATION OF OPTIMAL CONTROL OR FITNESS CAUSATION")
