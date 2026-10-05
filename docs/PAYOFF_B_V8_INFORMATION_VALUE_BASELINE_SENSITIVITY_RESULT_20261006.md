# PAYOFF-B V8 information-value baseline sensitivity result — 2026-10-06

Status: **POSTHOC BASELINE SENSITIVITY; FROZEN V8 PRIMARY UNCHANGED**

## Question

The main metric-scale diagnostic defines no-source prediction as a target-history linear trend. This sensitivity replaces that baseline with the window-specific target climatological mean and builds the source-informed forecast from source anomalies around its window mean.

## Result

Across all 166 unique source-destination pairs:

- early mean source predictive value = **-5.013 d^2**;
- late mean = **+17.357 d^2**;
- late-minus-early change = **+22.370 d^2**;
- pair-bootstrap 95% CI = **+18.127 to +26.780 d^2**;
- source-cell cluster CI = **+12.493 to +33.576 d^2**;
- target-cell cluster CI = **+16.775 to +29.323 d^2**;
- 5-degree block CI = **+15.288 to +29.671 d^2**;
- 10-degree block CI = **+14.322 to +35.361 d^2**;
- median pair change = **+17.589 d^2**;
- 10% trimmed mean change = **+19.080 d^2**;
- **136/166** pairs were positive.

The pairwise change under the climatological baseline correlated only moderately with the trend-baseline change (r = **0.409**), yet the aggregate direction remained strongly positive.

## Exact-complete subset

Among the 58 pairs with all 8 years present in both windows:

- early mean = **-2.683 d^2**;
- late mean = **+23.786 d^2**;
- change = **+26.468 d^2**;
- pair-bootstrap 95% CI = **+19.135 to +34.324 d^2**;
- **49/58** pairs were positive.

## Equal-species sensitivity

Across 28 species with equal species weighting:

- early mean = **-1.940 d^2**;
- late mean = **+19.359 d^2**;
- change = **+21.300 d^2**;
- pair-incidence bootstrap 95% CI = **+18.395 to +27.559 d^2**;
- **24/28** species were positive.

## Interpretation

The increase in marginal cross-validated source predictive value is not an artifact of choosing a linear target-history trend as the no-source baseline. It remains strong when the comparison is against a window-specific climatological mean.

This remains a posthoc diagnostic and does not identify bird cue use or fitness value.

## Provenance

- workflow run: 37390959199
- artifact: 11381412011
- artifact SHA256: a19f10b188bb853ff71f7308b639ad4e2727cd8546e14abc85c80440a2c7fe80

Script: analysis/movement_phenology/payoff_b_v8_information_value_baseline_sensitivity.R