# PAYOFF-B V8: post hoc day-metric–bird-transfer direct result

**Date:** 2026-10-15  
**Classification:** POST-OUTCOME EXPLORATORY — six disclosed exploratory contrasts, not preregistered, not multiplicity-controlled.  
**Source-defined analysis plan:** docs/PAYOFF_B_V8_DAYMETRIC_BIRD_TRANSFER_EXPLORATORY_LOCK_20261015.md, committed **before** the six-slope CI was executed. Registered V8 windows, source mapping, and mismatch effect remains untouched.

## Source and execution status

GitHub Actions run: https://github.com/zuizui0223/payoff/actions/runs/38672782848 — **SUCCESS**.

Full original-row/10,000-bootstrap result artifact: https://github.com/zuizui0223/payoff/actions/runs/38672782848/artifacts/11945021036

Artifact ID: 11945021036; GitHub-reported ZIP digest SHA256 `7c088320768fd89b4ee3853467cb75ae2dc521fe5df418e495916cb22885e3e8`.

Read-only original inputs were restored from the independently re-executed 2026-10-05 post hoc day-scale source data and from the unchanged registered bird-transfer/fixed-arrival structural-null rows. Independent identity checks confirmed **166** environmental source-target pairs, **150** species-target bird rows, **72** bird-eligible spatial pairs and **22** species. The bird-day diagnostic's log response matched the original registered bird mismatch response for each row. All six fixed slopes, 10,000 complete unique-spatial-pair bootstrap rows, and the observed-minus-fixed-arrival algebraic identity passed mechanical checks. No fitting window, sample rule or outcome was changed.

## Full results — all six contrasts (no outcome selection)

Each slope is the equal-species-weighted change in bird log absolute arrival–green-up mismatch per **one SD of the environmental predictor**, where that SD was computed over the 72 unique bird-eligible spatial pairs before fitting. Intervals are 95% percentile bootstrap CIs resampling the 72 distinct environmental pairs while retaining all linked species rows.

| Post hoc environmental predictor | Bird log-mismatch outcome | Slope | 95% pair-bootstrap CI | CI excludes 0? |
|---|---|---:|---|:---:|
| Δ source-informed LOYO RMSE (days; larger = worse) | Observed | +0.009467 | −0.089423 to +0.098864 | No |
| Δ source-informed LOYO RMSE | Original fixed-arrival null | +0.073923 | −0.009811 to +0.159610 | No |
| Δ source-informed LOYO RMSE | Observed minus fixed-arrival | −0.064456 | −0.138373 to +0.007657 | No |
| Δ source squared-loss incremental predictive value (days²; larger = more value) | Observed | +0.095296 | −0.002578 to +0.162303 | No |
| Δ source squared-loss incremental predictive value | Original fixed-arrival null | **+0.150397** | **+0.094067 to +0.231582** | Yes |
| Δ source squared-loss incremental predictive value | Observed minus fixed-arrival | −0.055101 | −0.167542 to +0.021201 | No |

**All six outcomes are reported**, including a strong positive association of squared-error source-skill change with a **fixed-bird-arrival null**. This is an observed-model mathematical/structural association, not a demonstrated bird behavioral response.

The registered correlation-to-bird mismatch transfer had beta +0.06243969 (CI −0.01411178 to +0.13634889), originally in the *wrong sign* for the preregistered prediction and NOT SUPPORTED; it remains unchanged.

## What this adds and what it does not show

This directly addresses the reviewer objection raised by a correlation-only V8 account: a source's statistical predictive improvement can be measured on the actual day/loss scale rather than inferred from rho alone. The new exploratory point estimates for both day-scale predictors have intervals including zero after comparing bird mismatch changes to the fixed-arrival structural-null expectation. Thus **neither day-metric provided detected evidence for a bird-specific timing-response increment in this model/sample**.

However, it is **not valid** to equate this with proof that neither metric affects biological tracking. The CIs allow nonzero effects; there are only 72 distinct environmental pairs; repeated species-target rows share exposures; no individual migration routes, cues or recourse are measured. The exploratory evidence is consistent with a structural coupling explanation and is at most a **negative identification result**, not a demonstrated information-actionability mechanism.

The one nominally nonzero slope among six belongs to the **fixed-arrival null**, which supports the warning that apparently significant environment-to-mismatch correlations can arise without any bird timing adjustment. Because multiple exploratory contrasts were examined, the interval excluding zero must not be treated as independent confirmatory discovery.

There is also no contradiction between the earlier period's negative observed LOYO source-forecast skill and the standard theorem that **free, optional information cannot reduce optimal expected decision payoff** when feasible actions and other agents' strategies are fixed. The negative LOYO value evaluates a finite-sample fitted regression as a **specified forecasting procedure**; it does not give the actor the costless choice to disregard an unreliable added cue and revert optimally to the baseline. Model estimation, overfitting and forecast calibration can therefore make a particular held-out predictor worse while ideal optional information retains nonnegative value.

Critically, the predictors are based on retrospective leave-one-year-out forecasting using environmental data, **not demonstrated cues observed by a bird before departure**. The response is a phenological timing difference, **not survival, fecundity or fitness regret**. A fixed-arrival structural null controls one form of shared target-green-up geometry but not every unmeasured environmental or behavioral confounder.

## Publication decision

- Keep PR #332's registered V8 primary results, historical post hoc metric-scale diagnostics and 41-page anonymous science archive unchanged.
- Retain this **separately reviewed, post-outcome exploratory** result as a supplementary/model-identification audit unless journal manuscript editorial review judges an appropriately qualified summary useful.
- Do not change the title, preregistration status, species inclusion or Paper 2 causal claim ceiling.
- No new claim that animals did not use information, that additional accuracy worsened fitness, or that both information metrics have been causally falsified.
