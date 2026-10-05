# PAYOFF-B V8 metric-scale diagnostic result — 2026-10-05

Status: **POSTHOC OUTCOME-INFORMED SCALE DIAGNOSTIC; FROZEN V8 PRIMARY UNCHANGED**

This receipt records the output of
`analysis/movement_phenology/payoff_b_v8_metric_scale_diagnostic.R`.

The diagnostic was designed after the V8 correlation outcome was known. It is
therefore exploratory/diagnostic and must not be described as preregistered or
confirmatory.

## Frozen primary retained

The script exactly reconstructs the frozen V8 correlation values:

- max absolute discrepancy in early rho = 0;
- max absolute discrepancy in late rho = 0.

The registered primary result remains:

- mean rho: **0.2838 -> 0.6528**;
- mean delta-rho: **+0.3690**.

The interpretation is narrowed from "predictability improved" to:

> standardized source-destination spring coupling strengthened.

## D1 — destination variability increased strongly

Across the same 166 unique spatial pairs, detrended destination green-up
variability increased:

- mean target residual SD: **2.412 d -> 4.662 d**;
- mean change: **+2.250 d**;
- pair bootstrap 95% CI: **+1.946 to +2.549 d**;
- source-cluster CI: **+1.715 to +2.746 d**;
- target-cluster CI: **+1.543 to +3.078 d**;
- 5-degree block CI: **+1.373 to +3.198 d**;
- 10-degree block CI: **+0.838 to +3.474 d**.

Thus the absolute interannual scale of destination phenology approximately
doubled between the two windows.

## D2 — standardized linear signal strengthened

The source-to-target anomaly relationship strengthened on standardized and
slope scales:

- mean R-squared: **0.290 -> 0.572**;
- mean change: **+0.282**;
- pair 95% CI: **+0.234 to +0.330**.

The fitted source-to-target slope also increased:

- mean slope: **0.399 -> 0.640**;
- mean change: **+0.241**;
- pair 95% CI: **+0.142 to +0.339**.

Both changes remain positive under source, target, 5-degree and 10-degree
cluster/block resampling.

Mean fitted explained MSE increased from:

- **1.714 d^2 -> 14.417 d^2**;
- mean change: **+12.703 d^2**;
- pair 95% CI: **+10.309 to +15.186 d^2**.

Thus the shared/predictable component increased strongly in absolute as well as
relative terms.

## D3 — in-window residual error increased, but the coarsest spatial block is uncertain

The fitted within-window residual RMSE increased:

- **1.821 d -> 2.494 d**;
- mean change: **+0.673 d**;
- pair 95% CI: **+0.460 to +0.891 d**;
- source-cluster CI: **+0.047 to +1.209 d**;
- target-cluster CI: **+0.325 to +1.058 d**;
- 5-degree block CI: **+0.113 to +1.294 d**;
- 10-degree block CI: **-0.257 to +1.598 d**.

Only **34.3%** of pairs had lower fitted RMSE in the late period.

This reproduces the qualitative scale reversal identified independently:
higher correlation does not imply lower absolute fitted error.

However, this in-window RMSE is optimistic because each 6-8 year window is
used both to fit and evaluate the linear relationship.

## D4 — leave-one-year-out forecast error did not clearly worsen

A stricter leave-one-calendar-year-out forecast recomputed source and target
trends and the anomaly relationship without the held-out year.

Source-informed LOO RMSE:

- **4.113 d -> 4.168 d**;
- mean change: **+0.055 d**;
- pair 95% CI: **-0.591 to +0.632 d**;
- source-cluster CI: **-1.282 to +1.252 d**;
- target-cluster CI: **-0.973 to +1.026 d**;
- 5-degree block CI: **-1.366 to +1.520 d**;
- 10-degree block CI: **-2.116 to +2.097 d**.

Only **46.4%** of pairs had lower LOO RMSE in the late period.

Therefore the stronger statement

> absolute out-of-sample forecast error worsened

is **not supported**.

The defensible statement is:

> absolute out-of-sample source-based forecast error did not clearly improve or
> worsen despite a large increase in destination phenological variability.

## D5 — without source information, out-of-sample error increased strongly

The trend-only LOO baseline, which does not use source green-up anomalies,
changed from:

- **3.182 d -> 5.865 d**;
- mean change: **+2.683 d**;
- pair 95% CI: **+2.342 to +3.013 d**;
- source-cluster CI: **+2.143 to +3.171 d**;
- target-cluster CI: **+1.889 to +3.593 d**;
- 5-degree block CI: **+1.790 to +3.621 d**;
- 10-degree block CI: **+1.228 to +3.868 d**.

Thus source information became much more valuable relative to the no-source
baseline. The late period combined:

- substantially greater destination volatility;
- stronger standardized source-destination coupling;
- much greater explained variation;
- approximately unchanged source-informed out-of-sample RMSE.

A concise interpretation is:

> strengthened cross-site information buffered, but did not eliminate, the
> forecasting consequences of rising destination variability.

This is descriptive and does not establish that birds perceived or used the
specific fitted source signal.

## D6 — bird arrival-green-up mismatch did not worsen on the day scale

Using exactly the 150 species-target rows / 72 unique pairs / 22 species
admitted to the frozen transfer lane, raw absolute mismatch in days was:

Unweighted row mean:
- early: **8.418 d**;
- late: **8.066 d**;
- change: **-0.352 d**;
- pair-bootstrap 95% CI: **-0.890 to +0.200 d**.

Equal-species change:
- **-0.627 d**;
- pair-bootstrap 95% CI: **-1.147 to -0.018 d**.

The frozen log-mismatch scale remains:
- unweighted change approximately **0**;
- equal-species log change with CI spanning zero.

Because the raw-day analysis is posthoc and the inference is scale-sensitive,
the manuscript should not claim proven mismatch improvement. It may state:

> bird arrival-green-up mismatch showed no corresponding deterioration as
> destination phenological variability increased.

The equal-species raw-day result can be reported as a posthoc sensitivity.

## Statistical interpretation

Correlation is scale invariant. The increase in destination SD did not itself
cause rho to increase.

For a continuous target Y and linear cue X under squared-error loss:

    residual risk = Var(Y) * (1 - rho^2)
    explained variation = Var(Y) * rho^2.

The V8 system changed in both terms:
- total destination variance increased strongly;
- the fraction associated with source variation also increased strongly.

Consequently, relative information and absolute uncertainty need not rank the
same way.

## Manuscript consequence

Retire the sentence:

> environmental predictability improved.

Replace it with a three-level distinction:

1. **standardized environmental coupling** strengthened;
2. **absolute out-of-sample forecast error** did not clearly change because
   rising coupling offset much of the increase in destination variability;
3. **realized bird mismatch** showed no corresponding deterioration.

The bird result still does not identify actionability or downstream correction
as the cause. The mule-deer evidence remains the independent natural anchor
showing that signed downstream correction exists.

## Provenance

Workflow run: 37305856291
Job: 111749247801
Artifact: 11343269670
Artifact SHA256:
4a12485c7653d8c904df53ccc50c049afb0dd3e607c704b221f616f0576b3a0d
