#!/usr/bin/env python3
"""Generate synthetic history robustness results; no network or empirical inputs."""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.history_aware_compromise import (
    Parameters, memory_policy, strategy_bounds, optimal_window_policy,
    predictable_endpoint_optimum,
)


def run():
    cases={}
    for name,rho,cost in (
        ('original_low_turnover',.1,3.8),('original_high_turnover',.9,3.8),
        ('memory_reverses_apparent_module_advantage',.1,3.55),
        ('memory_robust_slow_turnover',.1,3.6),
        ('memory_robust_fast_turnover',.9,3.6),
    ):
        p=Parameters(rho=rho,module_cost=cost)
        bounds=strategy_bounds(p,memories=(1,2,4,8,12))
        maps=[optimal_window_policy(p,n) for n in (1,2,3,4,6)]
        best_mapping=min(r['primal_loss'] for r in maps)
        cases[name]={'parameters':asdict(p),'bounds':bounds,
                     'optimized_finite_window_policies':maps,
                     'upper_bound_with_optimized_window':min(bounds['nonmodule_upper_bound'],best_mapping)}
    import numpy, scipy
    return {
        'schema':'PAYOFF_HISTORY_ROBUSTNESS_20261020_V1',
        'status':'SYNTHETIC_MATHEMATICAL_RESULTS_NOT_BIOLOGICAL_OBSERVATIONS',
        'original_pr':338,
        'original_head_read':'5993acd62d459d9403a90d1f5d3b591715b0f998',
        'original_code_blob_read':'e81cac684148cc08bace138deb69fc26417e3811',
        'cases':cases,
        'endpoint_original_cost':predictable_endpoint_optimum(Parameters(rho=1)),
        'robust_fast_turnover_sufficient_condition':{
            'module_cost':3.6,'rho_strictly_greater_than':(3.6-3-.05)/.75,
            'status':'SUFFICIENT_NOT_NECESSARY_BOUND_NOT_AN_EXACT_PHASE_TRANSITION'},
        'software':{'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__},
        'source_sha256':{
            str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (ROOT/'src/history_aware_compromise.py',ROOT/'tests/test_history_aware_compromise.py')},
        'claim_limits':[
            'Memoryless rho*=0.65625 is not an all-policy phase boundary.',
            'Finite-window convex optima are not unrestricted history optima.',
            'No additional memory cost is charged unless explicitly requested.',
            'The policy-independent lower bound grants even perfect future information.',
            'Fixed modules coexpress two coordinates within the same individual; not dioecy by default.',
            'No genetic heritability, rare invasion, fixation or historical structural origin is estimated.',
        ],
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    result=run()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf-8') as handle:
        json.dump(result,handle,indent=2,sort_keys=True)
        handle.write('\n')
    for name,case in result['cases'].items():
        bounds=case['bounds']
        print(name,bounds['classification'],
              f"all-policy lower={bounds['nonmodule_lower_bound']:.9f}",
              f"constructive upper={case['upper_bound_with_optimized_window']:.9f}")
    print('Endpoint rho=1:',result['endpoint_original_cost'])
    print('Synthetic only. No historical evolutionary origin tested.')


if __name__=='__main__':
    main()
