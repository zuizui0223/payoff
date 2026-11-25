# Wave 15–16 — option value, dominant-host dependence and absolute-performance guard

2026-11-25. Draft PR #426. The frozen primary estimand and manuscript are unchanged. The original Weir host-option analysis completed; the subsequent ablation and four-arm arithmetic are explicitly post-outcome descriptive diagnostics. No pooled meta-analysis.

## Authenticated original host assay and transfer result

Weir (2024), Oecologia 206:225–239, DOI 10.1007/s00442-024-05629-5, https://link.springer.com/article/10.1007/s00442-024-05629-5; original CC BY 4.0 workbook data DOI 10.6084/m9.figshare.27679935.v1. MD5 cc97938880788705d34d69baf351954b, pinned SHA256 76992552871f727ccbe0d5718c1bc1a7a93aaddd57cb0a8f2cef669e74ee6598. All 3600 rows per sheet and 180 cultures (5 cultures of 20 larvae per population-host) checked; 648 pupations across the 3600 larvae. Survival totals agree at culture level across endpoint sheets; no individual-level endpoint join. The source paper already shows that birch and willow can support performance better than oak, so that alone is not new.

For each held-out population, rank eight non-oak hosts by equal-weight survival in the other three populations. Exhaustively enumerate equally weighted hypothetical accessible subsets (1/2/4/8 species). No actual switching, timing manipulation, field host availability, or larvae choice in this analysis.

| Number of non-oak options | Blind choice | Training-ranked choice | Held-out oracle | Ranked minus oak |
|---|---:|---:|---:|---:|
| 1 | 18.40625% | 18.40625% | 18.40625% | +3.65625 pp |
| 2 | 18.40625% | 26.24107% | 27.81250% | +11.49107 pp |
| 4 | 18.40625% | 34.72143% | 37.87143% | +19.97143 pp |
| 8 | 18.40625% | 46.75000% | 46.75000% | +32.00000 pp |

Oak survival 14.75%. The all-eight ranked minus oak conditional culture-bootstrap interval is [29.25,34.75] pp (10,000 draws, five cultures resampled within each population-host cell, rankings refit). No population-random-sampling or brood-independence guarantee. Blind-choice expectation is invariant to subset size by construction; it is a benchmark identity, not a newly discovered effect of richness. All 16 held-population × subset-size point estimates independently reproduced from integer cell counts. The four training folds use overlapping populations and do not constitute independent geographical replication. Source rank of Salix alba is first in each training fold. The same host is the held-out best or tied best in all four.

## Same-richness ablation: functional options are not equivalent

This deterministic post-outcome diagnostic compares subsets of the same size with vs without the top training-ranked host (S. alba, code Salba). No new variance estimate; selection of this diagnostic was motivated by the completed result. The full set of subsets is retained.

| Options | With top host | Without top host | Point difference |
|---|---:|---:|---:|
| 1 | 46.75% | 14.35714% | +32.39286 pp |
| 2 | 46.75% | 19.40476% | +27.34524 pp |
| 4 | 46.75% | 22.69286% | +24.05714 pp |

With all eight accessible, held-out trained choice gives 46.75%; remove only the top host and select from all seven remaining, 20.50%. Point gain relative to oak decreases from 32 to 5.75 pp, an 82.03% reduction of that gain. The held-out oracle among the seven would achieve 35.25%. In population S, the transported ranking selects apple (9% survival), worse than oak (29%), while birch would give 45%. The top-two training-host deletion gives 32.5% with six options; this nonmonotonic result is retained because the transferred ranking can misidentify the best option (training top two can differ by fold). It is not a claim that losing species benefits real populations. Identity, performance and information about host quality are separable from the count of available options. No evidence of actual phenological availability, switching costs, field fitness or a collapse threshold; no new causal richness manipulation.

## Exact guard: relative attenuation and absolute performance

Do not redefine the original theta. For positive arm means W_db, D=0/1 reference/perturbed and B=0/1 reference/candidate buffer:
- r0 = log(W10/W00), r1 = log(W11/W01), theta = r1-r0.
- beta = log(W01/W00), the candidate's reference-context performance contrast.
- eta = log(W11/W10) = beta + theta, the absolute disturbed-context benefit on the log scale.
- R = W11/W00 = exp(r0+eta), residual performance relative to the original undisturbed reference.

An attenuation interpretation requires r0<0. With beta<0, positive theta is insufficient for absolute improvement: eta>0 iff theta>−beta. For full recovery to a prespecified fraction tau of the original reference, R≥tau iff eta≥log(tau)−r0. Tau is an independent biological target; absent such a target, report R continuously and do not diagnose collapse just from a low level. A hypothetical bounded performance example (W00,W01,W10,W11)=(.8,.1,.4,.08) gives theta=.470, eta=−1.609, R=.10. Relative apparent attenuation coexists with 80% lower disturbed performance. This is algebra, not a new empirical mechanism, and no inference follows without joint uncertainty.

Point-level application to all previously frozen Pardee snow-removal × external pollen arms, not primary mismatch × endogenous recourse. Recomputed original theta exactly, all main and existing sensitivity variants retained.

| Species | r0 | theta | beta | eta | Disturbed AP vs NP change | R |
|---|---:|---:|---:|---:|---:|---:|
| Claytonia | −.350037 | −.066776 | .184360 | .117584 | +12.48% | .792587 |
| Delphinium | .201982 | −.432276 | .038800 | −.393476 | −32.53% | .825725 |
| Potentilla | −.127035 | .010042 | −.027402 | −.017360 | −1.72% | .865546 |

Claytonia has a positive disturbed-context improvement point without relative attenuation; Potentilla has a small positive relative attenuation point without absolute improvement. Delphinium has no detrimental snow perturbation point in NP and must not be labeled failed rescue. All original theta intervals include zero. No joint interval for beta/eta/R from saved summary means; no claim of statistically demonstrated collapse or compensation. Species share one plot experiment; external pollen and snow manipulation are secondary, not an independent test of actual resource-relative timing and endogenous recourse.

## Reproduction and next scientific gate

Weir run https://github.com/zuizui0223/payoff/actions/runs/45567146848, job 139044617068, artifact 15000054546; ZIP SHA256 c15baffbf92dfc78d51ba2896ab081fb3576e39056300a8476e64b2485447eea recorded from upload log, ZIP not separately downloaded. Exact original source checks and executed policy results saved at data/payoff_b_weir_host_option_transfer_wave15_result_20261125.json. New deterministic enumeration and four-arm identity calculation executed in JS on refetched repository result JSON, reproducible script scripts/payoff_b_option_concentration_and_absolute_guard_wave16_20261125.mjs; new result data/payoff_b_option_concentration_and_absolute_guard_wave16_result_20261125.json (includes source blob SHA receipts). No second raw-workbook fit or new CI claimed.

Pardikes et al. 2022 (DOI 10.1111/gcb.16195) final publisher data availability statement says data/code will be deposited to Dryad; publisher lists a supplementary ZIP. No authenticated original archive or signed vial-level effect retrieved. Prior paper already demonstrates community context and warming affect mismatch outcomes. Next primary gate: obtain original factorial vial-level recruitment data from legitimate archive/supplied source and estimate joint theta, beta, eta and R under the pre-existing admission rules, separating absolute experimental outcomes from simulated persistence. No primary theta added. Do not continue indefinite surrogate analyses as if they were the requested cross-system meta-analysis. No merge.
