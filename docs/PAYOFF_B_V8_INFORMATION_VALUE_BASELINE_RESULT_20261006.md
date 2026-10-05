# PAYOFF-B V8 information-value baseline sensitivity result — 2026-10-06

Status: **POSTHOC BASELINE SENSITIVITY; FROZEN V8 PRIMARY UNCHANGED**

## Question

The main metric-scale diagnostic defined cross-validated nonlocal forecast value
relative to a target-history linear-trend baseline:

    G_CV = MSE(target trend only) - MSE(source informed).

Because information value is always relative to an alternative action or
forecast, this sensitivity asks whether the late-minus-early increase survives
when the baseline is changed to a window-specific climatological mean.

For each held-out year, the alternative analysis uses:
- target-only prediction = training-window target mean;
- source-informed prediction = target mean plus a linear response to the
  held-out source anomaly around its training-window mean.

No focal-year information enters the held-out fit.

## Pair-level result

Across the same 166 unique spatial pairs:

Climatology-baseline G_CV:
- early mean = **-5.013 d^2**;
- late mean = **+17.357 d^2**;
- late-minus-early change = **+22.370 d^2**.

Distributional robustness:
- median delta = **+17.589 d^2**;
- 10% trimmed mean delta = **+19.080 d^2**;
- **136/166** pairs positive;
- 30 negative.

Uncertainty:
- pair-bootstrap 95% CI = **+18.127 to +26.780 d^2**;
- source-cell cluster CI = **+12.493 to +33.576 d^2**;
- target-cell cluster CI = **+16.775 to +29.323 d^2**;
- 5-degree block CI = **+15.288 to +29.671 d^2**;
- 10-degree block CI = **+14.322 to +35.361 d^2**.

The late-minus-early pair values correlate only moderately with the
trend-baseline version:

- cor(delta G_climatology, delta G_trend) = **0.409**.

Thus the exact pair ranking is baseline-dependent, but the population-level
direction is not.

## Exact-complete sensitivity

Among the 58 pairs with all eight years in both periods:

- early mean = **-2.683 d^2**;
- late mean = **+23.786 d^2**;
- change = **+26.468 d^2**;
- pair-bootstrap 95% CI = **+19.135 to +34.324 d^2**;
- **49/58** pairs positive.

## Equal-species sensitivity

Across 28 species with equal species weighting:

- early mean = **-1.940 d^2**;
- late mean = **+19.359 d^2**;
- change = **+21.300 d^2**;
- pair-incidence bootstrap 95% CI = **+18.395 to +27.559 d^2**;
- **24/28 species** positive.

## Interpretation

The conclusion that contemporaneous nonlocal source information gained
out-of-sample forecast value between periods does not depend on using a
short-term linear target trend as the no-source comparator.

The magnitude and pair ranking are baseline-dependent, as expected for any
value-of-information quantity. The manuscript should therefore describe G_CV
as the **marginal forecast value relative to a declared target-history
baseline**, not as an intrinsic property of the source cue.

Licensed:

> The increase in marginal cross-validated forecast value remained positive
> when the no-source comparator was changed from a target-history trend to a
> target climatological mean.

Not licensed:
- an organismal fitness value of information;
- a unique baseline-free information-value number;
- bird perception or use of the reconstructed source signal.

## Provenance

Workflow:
- run: 37390959199
- artifact: 11381412011
- artifact SHA256:
  a19f10b188bb853ff71f7308b639ad4e2727cd8546e14abc85c80440a2c7fe80

Script:
analysis/movement_phenology/payoff_b_v8_information_value_baseline_sensitivity.R
