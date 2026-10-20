#!/usr/bin/env python3
"""Reproduce two-cue memory robustness; all results are synthetic model values."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.plastic_compromise_memory import audit

BASE = dict(a=3., b=1., delta=2., q=.9, rho=.9,
            plastic_running_cost=.05, plastic_switch_cost=1., module_cost=3.8)


def crossing(lo, hi, K=3.87):
    def f(rho):
        return audit(dict(BASE,rho=rho,module_cost=K))['two_cue_loss_without_extra_memory_cost']-K
    left=f(lo); right=f(hi)
    if left*right>=0:
        raise ValueError('need a strict sign-changing bracket')
    for _ in range(45):
        mid=(lo+hi)/2; value=f(mid)
        if value==0:
            lo=max(lo,mid-2e-14); hi=min(hi,mid+2e-14); break
        if left*value<0:
            hi=mid
        else:
            lo=mid; left=value
    return {'rho':(lo+hi)/2,'bracket':[lo,hi],'bracket_width':hi-lo}


def run():
    original=[audit(dict(BASE,rho=r)) for r in (.1,.65625,.9)]
    reentry=[audit(dict(BASE,rho=r,module_cost=3.87)) for r in (.9,.95,.99)]
    nonzero_memory=[audit(dict(BASE,rho=r,module_cost=3.87),memory_cost=.001)
                    for r in (.85,.95,.99)]
    assert [r['best_strategy'] for r in reentry]==[
        'PLASTIC_MEMORY','FIXED_MODULES','PLASTIC_MEMORY']
    assert original[0]['best_strategy']=='PLASTIC_MEMORY'
    assert original[-1]['best_strategy']=='FIXED_MODULES'
    return dict(
        status='SYNTHETIC_THEORY_NOT_EMPIRICAL_OR_HISTORICAL_EVOLUTION',
        original_payoff_pr=338,
        original_payoff_head='5993acd62d459d9403a90d1f5d3b591715b0f998',
        original_parameters=BASE,
        original_K3_8_two_cue_checks=original,
        exploratory_K3_87_reentry=reentry,
        positive_memory_cost_0_001_checks=nonzero_memory,
        two_cue_K3_87_crossing_brackets=[crossing(.9,.95),crossing(.95,.99)],
        crossing_polynomial_descending_coefficients=[131072,-193024,14720,47637],
        history_independent_witness=audit(dict(BASE,module_cost=2.9)),
        this_script_performs_git_writes=False,
        interpretation='fixed-module winners are relative to the declared strategy set; the C floor is independent of history under the same scalar-coordinate constraint',
    )


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    payload=json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n'
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        with args.out.open('x',encoding='utf-8') as handle:
            handle.write(payload)
    else:
        print(payload,end='')


if __name__=='__main__':
    main()
