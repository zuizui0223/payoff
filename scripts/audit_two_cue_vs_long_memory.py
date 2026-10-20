#!/usr/bin/env python3
"""Audit nested cue-memory policy classes with exact 2-cue vs 1–6 cue optima.

Source-free synthetic consistency test; does not identify evolving
architectures, historical origin, or any Wurmbea model parameters.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from src.plastic_compromise_memory import audit as exact_two_cue
from src.history_aware_compromise import Parameters, optimal_window_policy, strategy_bounds


def run():
    parameters=dict(a=3., b=1., delta=2., q=.9,
                    plastic_running_cost=.05, plastic_switch_cost=1.,
                    module_cost=3.87)
    reports=[]
    for rho in (.90,.95,.99):
        a=exact_two_cue({**parameters,"rho":rho})
        b=Parameters(a=parameters["a"],b=parameters["b"],delta=parameters["delta"],
                     q=parameters["q"],rho=rho,
                     running_cost=parameters["plastic_running_cost"],
                     switch_cost=parameters["plastic_switch_cost"],
                     module_cost=parameters["module_cost"])
        options={}
        for m in (1,2,3,4,6):
            result=optimal_window_policy(b,m)
            options[str(m)]={
                "primal_loss":result["primal_loss"],
                "dual_lower_bound_on_window_class":result["dual_lower_bound_on_window_class"],
                "primal_dual_gap":result["primal_dual_gap"],
                "numerically_certified_to_2e_8":result["numerically_certified_to_2e_8"],
                "minimized_over_all_stationary_m_cue_action_maps":True,
            }
        if abs(a["memoryless_loss"]-options["1"]["primal_loss"])>1e-6:
            raise ArithmeticError("Original memoryless versus finite-window m=1 disagree")
        if abs(a["two_cue_loss_without_extra_memory_cost"]-options["2"]["primal_loss"])>1e-6:
            raise ArithmeticError("Exact 2-cue formula and independent convex m=2 optimizer disagree")
        for m,n in zip((1,2,3,4),(2,3,4,6)):
            if options[str(n)]["primal_loss"]>options[str(m)]["primal_loss"]+1e-6:
                raise ArithmeticError("More cue history unexpectedly worsened feasible optimum")
        bounds=strategy_bounds(b,memories=(1,2,4,8,12))
        fixed=parameters["module_cost"]
        longest=options["6"]["primal_loss"]
        reports.append({
            "rho":rho,
            "environmental_lag_one_correlation":1-2*rho,
            "fixed_module_cost":fixed,
            "exact_two_cue_loss":a["two_cue_loss_without_extra_memory_cost"],
            "restricted_two_cue_best_strategy":a["best_strategy"],
            "nested_optimal_window_losses":options,
            "best_six_cue_or_shared_cost":min(longest,b.shared_loss),
            "six_cue_feasible_policy_beats_fixed":longest<fixed,
            "finite_window_status": (
                "SIX_CUE_PLASTIC_BETTER" if longest<fixed else
                "FIXED_BETTER_THAN_OPTIMAL_SIX_CUE_ONLY" if longest>fixed else
                "NUMERICAL_TIE"
            ),
            "all_history_lower_bound":bounds["nonmodule_lower_bound"],
            "all_history_feasible_upper_bound":bounds["nonmodule_upper_bound"],
            "all_history_certificate":bounds["classification"],
            "never_claims_global_optimality_from_six_cues":True,
        })
    return{
        "schema":"PAYOFF_TWO_CUE_VS_LONGER_CUE_HISTORY_V1",
        "status":"POST_OPEN_SYNTHETIC_NESTED_POLICY_COMPARISON_NOT_EMPIRICAL",
        "source_relative_scope":"all models in payoff PR 338; no biological evidence or historical transition",
        "params_shared":parameters,
        "results":reports,
        "reentrant_two_cue_cost_K3_87_was_exploratory":True,
        "not_fitted_to_wurmbea_or_any_species":True,
        "memory_cost_assumed_zero_for_nested_comparison":True,
        "biological_causal_origin_established":False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    result=run()
    content=json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        with args.out.open("x",encoding="utf-8") as f:
            f.write(content)
    print(content,end="")


if __name__=="__main__":
    main()
