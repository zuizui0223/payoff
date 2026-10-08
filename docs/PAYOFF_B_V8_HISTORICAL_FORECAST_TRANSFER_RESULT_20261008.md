# PAYOFF-B V8: historical environmental forecast transfer (first empirical result)

**Date:** 2026-10-08
**Status:** POST-V8-OUTCOME EXPLORATORY; source-only, no biological action inferred.
**Branch:** analysis/payoff-b-v8-historical-forecast-transfer-20261008
**Workflow:** GitHub Actions run 37742082525 (completed successfully), job 113194878578; four CSVs in artifact 11534400991, SHA256 e2b8420d7cff1a3940134baee45e06a7056e75261ccbaa9d74a338638b2c82dd.
**Input:** original Amaral source commit 62c58d77c2028bd863dfe3697b0d9cf29ceaeab0, through the unchanged V8 primary script and original source–target pair mapping.

## Why this matters

V8 established that *contemporaneously fitted* source–destination spring correlations increased (166 unique pairs, mean delta-rho +0.369), but its registered bird mismatch transfer test was not supported. The new, deliberately narrower environmental audit asks whether a forecast rule fitted **only to 2002–2009** still improves prediction of **2010–2017** spring relative to a calendar-year-only trend model.

This distinguishes one element of **environmental forecast calibration** from within-window correlation, but does NOT measure whether a migrant could perceive the source mid-greenup date before an irreversible decision, use the model, or act on the forecast. It is not independent confirmation because V8 outcomes had already been examined.

## Design and actual output

- Fixed spatial environmental pairs: 166 / 166 scoreable; exposure to 28 migratory species but no species-level replication of climate pairs.
- Training years: 2002–2009; holdout scoring years: 2010–2017.
- Both training-only ridge models include calendar year; origin-augmented model additionally includes the source-cell spring-greenup time. Penalty lambda=1 fixed beforehand; feature mean/SD computed from early years only.
- Score: pair mean of (MSE calendar-only minus MSE calendar + source) **divided by squared early-period target SD**, then mean across 166 unique pairs. This score is UNBOUNDED and NOT R-squared, percentage, or a bird fitness effect.
- Mean standardized pair score improvement **+2.22099196**; median **+0.51072562**; fraction positive **0.626506** (104/166).
- Pair-bootstrap 95% interval **+1.3361 to +3.1493** (descriptive; pairs share weather).
- 5-degree target-grid spatial block bootstrap (15 blocks): **+0.9053 to +3.8873**.
- 10-degree target-grid spatial block bootstrap (8 blocks): **+0.7321 to +5.1692**.
- All eight holdout **annual mean** scores positive; per-year means:
  - 2010 +5.5501, 2011 +0.8463, 2012 +7.0473, 2013 +0.1014,
  - 2014 +0.9258, 2015 +0.8253, 2016 +0.9690, 2017 +1.5028.
- Average early source–target correlation about +0.2838; late correlation about +0.6528; Delta-rho +0.3690, reproducing frozen V8 input.
- The change in contemporaneous correlation correlates **negatively**, not positively, with transferred historical forecast value across pairs (Pearson r = -0.37482; Spearman r about -0.474). These are exploratory paired-data descriptions, NOT independent tests of route biology or causal cue use.

## Non-obvious heterogeneity (identified AFTER result inspection)

| Detrended early/late environmental correlation sign | Unique pairs | Mean heldout historical forecast improvement | Fraction improved |
|---|---:|---:|---:|
| Negative -> positive | 44 | **-1.9593** | 7/44 (15.9%) |
| Positive -> positive | 108 | **+4.1276** | 86/108 (79.6%) |
| Positive -> negative | 7 | +1.7225 | 7/7 |
| Negative -> negative | 7 | -0.4210 | 4/7 |

The negative-to-positive group contributes strong apparent calibration reversal, even though the overall trend says the historic source cue generally **retains** forecast value. However, its early correlation has mean only -0.252 and training supports are often just 6–8 annual records. A negative estimate from that short interval can be noise/regression-to-the-mean. The group should NOT be labelled a demonstration of ecological learning traps, established sign change, or birds adopting obsolete beliefs without an independent sign-stability and behavioral test.

Additional **post-result descriptive** checks from the four archived CSVs:
- 2010 and 2012 are influential years. Dropping both from the descriptive late score average leaves +0.862 (same fitted models, not re-optimized).
- A 10%-per-tail trimmed unique-pair mean remains about +1.34.
- Among negative-to-positive pairs only 2/44 have early correlation below -0.5, despite several very positive later correlations.
These checks were performed after the result and cannot count as prospective confirmations.

## Crucial negative scientific message

The environmental test does **not** rescue the abandoned hypothesis that broadly worsening cross-site spring correlation caused migrant mismatch. It strengthens its failure: **an old source-based environmental forecast still adds some later-era predictive power**, on average, even though correlation gains do not have the registered bird-timing transfer.

But it ALSO does not prove that environmental information actually became more usable by birds, because the origin mid-greenup value is reconstructed retrospectively, mapped from species ranges rather than tracked paths, and may not be an available predecision cue. In addition, spring matching is not directly equivalent to reproductive or survival fitness.

Thus neither bird ignorance, inability to correct, nor rational costly undertracking is identified. Any statement that some individual migrants *rationally did not use* information needs an actual action and benefit/cost endpoint in a supported longitudinal biological dataset.

## Next warranted diagnostic / decisive ecological extension

1. Before using the negative-to-positive group as biology, quantify year-within-early sign stability and historical leave-one-year-out predictive value; a trained inverse relationship that was never predictive even in the earlier period cannot be called "formerly useful learning."
2. For an actual ecological payoff claim, obtain time-stamped cue availability on tracked migration paths, independently measured correction options, actual behavioral revision and downstream resource/fitness effects.
3. Do not tune or alter the frozen V8 environmental or bird analysis, report the source-only result as exploratory supplementary material only if interpretation survives basic dependence and prior-art checks.

**Interpretation ceiling:** Historical source-cell green-up information helped predict later target-cell spring on average under this fixed model contrast. No claim is made about individual cue uptake, fitness, social learning, cognitive updating, physical recourse, or interspecific coordination.
