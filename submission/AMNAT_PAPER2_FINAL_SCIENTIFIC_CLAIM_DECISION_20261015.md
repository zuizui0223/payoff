# PAYOFF-B Paper 2 — final scientific claim and handoff decision (2026-10-15)

**Editorial decision:** retain the theory-led *The American Naturalist* Major Article, with preregistered V8 as the falsifying stress test and explicitly post-outcome S2/S3 as a mechanism-identification audit. **Do not promote an environmental correlation or source-forecast model score to evidence that an individual bird had, used, or ignored that information.**

## One publishable scientific statement

> Strengthening cross-site environmental correlations—and even a greater retrospective predictive advantage from including a source site—does not by itself identify an adjustment in bird arrival timing: an apparent environment-to-mismatch association also arises under a model that holds bird arrival fixed.

This is **theoretical scope plus observational/model-association evidence**, not a causal proof that information failed to influence behaviour. No fitness outcome or independently observed animal recourse was linked to the forecast metric in the V8 bird sample.

## Nonexchangeable outcomes

| Layer | Design status | Frozen or original-source result | Licensed interpretation |
|---|---|---|---|
| Detrended source–target green-up correlations | **Original preregistered V8** | n=166 unique pairs; Δrho **+0.36902**, pair CI **+0.29844 to +0.43648** | Registered broad degradation prediction NOT_SUPPORTED |
| Correlation-change to bird log-mismatch transfer | **Original registered V8** | 150 species-target rows; 72 unique environmental pairs; slope **+0.06244**, pair CI **−0.01411 to +0.13635** | Registered negative transfer prediction NOT_SUPPORTED |
| Fixed-arrival geometric comparator | Registered secondary structural audit | fixed arrival **+0.04742**; bird-specific increment **+0.01502** (CI **−0.05212 to +0.10273**) | Positive association is compatible with bird arrival held fixed; no detected bird-specific increment |
| Day-unit fitted RMSE and target volatility | **Post-outcome S2** | fitted RMSE **1.821→2.494 d**, target SD **2.412→4.662 d** | Correlation is not synonymous with lower absolute in-sample error |
| Day-unit holdout forecasting and source value | **Post-outcome S2** | source LOYO RMSE **4.113→4.168 d**; relative source skill **−0.931→+1.697 d** | Accuracy and *relative* value differ; these are retrospective statistical forecasts |
| LOYO RMSE to bird-only mismatch increment | **Post-outcome S3**, 6-model exploratory family | β **−0.06446**, pair CI **−0.13837 to +0.00766** | No detected increment; the interval does NOT prove no biological effect |
| Change in squared-loss source value to bird-only increment | **Post-outcome S3** | β **−0.05510**, pair CI **−0.16754 to +0.02120** | No detected increment; no cue/recourse/fitness mechanism identified |
| Same source-value exposure to **fixed-arrival null** | **Post-outcome S3** | β **+0.15040**, pair CI **+0.09407 to +0.23158** | Nominally nonzero *structural* association; NOT a detected bird timing response |
| After-outcome geographical sensitivity | **Second post-outcome exploratory layer** | 20 source clusters, 19 target clusters, 9 target-5° blocks preserve the S3 distinction; only 4 target-10° blocks: **NOT_ESTIMABLE** | Spatial dependence handled transparently, but neither causal identification nor multiplicity-corrected inference |

The original direct S3 exposure was standardized over **72 unique environmental pairs**, not 150 species-target rows. The complete **6 slopes, 24 geographical interval cells, and 564 omission slopes** are retained without choosing a favourable effect after inspection. No positive S3 test should be described as an independent preregistered result.

## What should *not* be added to the submitted claims

- **Do not say** the day-unit data proved biological adaptation failed. Stronger retrospective statistical skill is not demonstrated decision-time information.
- **Do not say** the RMSE-to-bird incremental effects are zero; pair/spatial bootstrap intervals include both zero and some nonzero effect sizes.
- **Do not say** high target variability *caused* Pearson rho to rise; rho is scale invariant.
- **Do not treat** 10° blocks as a successful negative sensitivity; four independent groups missed the precommitted minimum of five.
- **Do not fuse** the mule-deer phase-convergence and the bird forecast-skill results as the same individuals or fitness contrast.
- **Do not claim** the sign-dependent source-forecast result is original proof that competitive, social or migratory information becomes worthless; information/coexistence and cue-use prior art are substantial.

## Accepted manuscript layout

- **Main text:** retain the registered V8 evidence (rho and bird transfer), Fig. 2–3 with **actual archived pair/target points**, theory Fig. 1, published-source deer Fig. 4, and one concise *explicitly exploratory* S3 paragraph only.
- **Supplement S2:** day-scale SD, slope, fitted RMSE, LOYO RMSE, no-source LOYO baseline and squared-loss skill. The 95% *source-skill difference* CI follows the original R output (**+2.132 to +3.184 days**), not the conflicting legacy prose.
- **Supplement S3:** all six day-metric-to-bird slopes, structural null, dependence checks and missing 10° result. Never replace V8's registered correlation transfer in the Abstract or Conclusion with the S3 post hoc results.
- **Abstract and title:** keep the neutral title *Environmental predictability alone does not determine seasonal tracking*. Do not inflate stronger *correlation* into improved **perceived** predictive information.

## Completed technical checks and canonical reviewer package

- Source-pinned Amaral V8 scientific R replay and Ortega published Source Data reproduction both independently matched their original model outputs.
- **Completed successful S3 archive CI:** https://github.com/zuizui0223/payoff/actions/runs/38699554487
- GitHub internal artifact: https://github.com/zuizui0223/payoff/actions/runs/38699554487/artifacts/11955491813
- The **canonical** reviewer-content candidate, not an external reviewer delivery endpoint: **75 files**, **41-page double-anonymous editorial PDF**, **4 source-verified figures**, original V8/deer/S2/S3 code and inputs, 40,000 spatial resamples, 564 omissions. Deterministic *inner ZIP* SHA256: `8a72991d3cc93390ced829444f065f3069e4c511e55c0cea3ce70d12a0b6354a`. Full receipt: `submission/AMNAT_PAPER2_S3_20261015_VERIFIED_ANON_REPRO_ARCHIVE.md`.
- An alternative duplicate S3 packager briefly introduced on this branch was **withdrawn**; the successful canonical 75-file package above is the only recommended scientific-review source of record.

## Final external-submission blockers (not solved by another statistical model)

1. Human page-by-page examination of **all 41 full-resolution PDF pages**, equations, axis labels and citations.
2. Source-code author/license approval and third-party reuse check.
3. A true **owner-anonymous** external reviewer-accessible dataset/code sharing location, independent of GitHub Actions repo-owner URLs.
4. Author-verified affiliations, contributions, funding, competing interests and AI-assistance declaration in the editorial system.
5. Submit only after the actual final reviewer version is approved, using the journal's double-anonymous requirements.

**STOP/GO:** Computational reproducibility and content-anonymity package **GO for human review**. Independent biological causal identification **NOT ESTABLISHED**. Journal submission **HOLD**. Do not merge the manuscript branch or publish an unreviewed statistical mechanism claim as if confirmed.
