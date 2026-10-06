# PAYOFF-B V8 source-rank forecast-value sensitivity result — 2026-10-06

Status: **POSTHOC SOURCE-DEFINITION SENSITIVITY; FROZEN V8 PRIMARY UNCHANGED**

## Question

The frozen environmental mapping uses the nearest lower-latitude migratory-range
cell as the nonlocal source for each breeding target.

This sensitivity asks whether the increase in cross-validated forecast value is
specific to that nearest source or is equally present for the second- and
third-nearest lower-latitude migratory cells.

The analysis is restricted to a common sample in which ranks 1, 2 and 3 are all
estimable in both periods.

## Common sample

- **223 species-target rows**
- **22 species**

Mean source-target distance:
- rank 1: **469 km**
- rank 2: **614 km**
- rank 3: **732 km**

## Forecast-value change by source rank

Late-minus-early cross-validated squared-loss forecast-value change:

Pair/row mean:
- rank 1: **+37.23 d^2**
- rank 2: **+33.46 d^2**
- rank 3: **+29.13 d^2**

Median:
- rank 1: **+23.59 d^2**
- rank 2: **+23.08 d^2**
- rank 3: **+18.40 d^2**

Positive species-target rows:
- rank 1: **219/223**
- rank 2: **213/223**
- rank 3: **199/223**

Equal-species means:
- rank 1: **+34.26 d^2**
- rank 2: **+30.08 d^2**
- rank 3: **+23.57 d^2**

Thus the increase is not unique to one frozen source choice: all three nearby
lower-latitude sources show a strong positive temporal change.

## Paired rank contrasts

On the same species-target rows:

Rank 1 minus rank 2:
- equal-species contrast = **+4.18 d^2**
- 95% bootstrap CI = **-4.23 to +13.43 d^2**

Rank 1 minus rank 3:
- equal-species contrast = **+10.68 d^2**
- 95% bootstrap CI = **+2.46 to +18.96 d^2**

Therefore the nearest source has larger forecast-value gain than the
third-nearest source in this common-sample comparison, whereas the nearest
versus second-nearest contrast remains unresolved.

## Standardized correlation change

Mean delta-rho:
- rank 1: **+0.331**
- rank 2: **+0.385**
- rank 3: **+0.397**

Equal-species delta-rho:
- rank 1: **+0.362**
- rank 2: **+0.406**
- rank 3: **+0.417**

The ranking of delta-rho is therefore opposite the ranking of forecast-value
gain. This is another example of why standardized correlation change is not a
decision-scale forecast-value metric.

## Interpretation

Licensed:

> The temporal increase in marginal forecast value is a broader regional
> property of nearby lower-latitude source cells rather than an artefact of one
> frozen nearest-cell choice, although the nearest source shows greater gain
> than the third-nearest source on the common sample.

Not licensed:
- the nearest source is the true cue source used by birds;
- individuals traverse the rank-1 source cell;
- source rank estimates a biological route sequence;
- the rank comparison identifies information use.

The source cells remain reconstructed environmental predictors, not observed
individual cue locations.

## Role in V4.4

This sensitivity strengthens the environmental forecast result while narrowing
its biological interpretation.

The correct object is:
**regional nonlocal forecast structure**.

It should not be described as:
**a known cue encountered at the mapped source site**.

## Provenance

Workflow:
- run: 37402997832
- artifact: 11386570254
- artifact SHA256:
  f7750ef2abbf21c6d1be9cbfdd6bab7a7ec7f60ea1f07592e2fede5890d7f20e

Script:
analysis/movement_phenology/payoff_b_v8_source_rank_sensitivity.R
