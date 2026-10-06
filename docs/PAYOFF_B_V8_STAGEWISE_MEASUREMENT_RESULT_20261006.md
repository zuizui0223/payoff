# PAYOFF-B V8 stagewise measurement-uncertainty result — 2026-10-06

Status: **POSTHOC MEASUREMENT SENSITIVITY; STAGEWISE RESULT SUPPORTING ONLY**

## Question

The stagewise population-front diagnostic found a more negative late-period
source-to-target phase transformation in the restricted 31-pair / 14-species
subset.

Arrival posterior SD changed markedly between periods, however:

- source arrival SD: about 2.89 d early -> 0.91 d late;
- target arrival SD: about 2.85 d early -> 0.93 d late.

This audit asks whether the stagewise contrast survives explicit propagation of
the reported arrival-date uncertainty.

## Baseline stagewise contrast

Using posterior mean arrival dates and equal weighting of years:

- pair-mean late-minus-early phase-transformation change = **-1.373 d**;
- equal-species change = **-1.929 d**.

Negative values mean that the source-to-target population-front phase
transformation became more negative in the late period.

## Posterior-normal uncertainty propagation

Each annual source and target arrival date was independently drawn from a Normal
distribution with the reported posterior mean and posterior SD. Green-up dates
were held at their reported means.

Across 5,000 Monte Carlo replicates:

Pair-level mean:
- median = **-1.367 d**;
- 95% Monte Carlo interval = **-2.036 to -0.706 d**;
- fraction of replicates below zero = **1.000**.

Equal-species mean:
- median = **-1.929 d**;
- 95% interval = **-2.601 to -1.310 d**;
- fraction below zero = **1.000**.

Thus the reported arrival-date uncertainty, propagated around the posterior
means under this independent-Normal approximation, does not remove the
direction of the stagewise contrast.

This simulation does not model covariance among arrival estimates and does not
correct unknown systematic bias.

## Inverse-variance weighted sensitivity

As a separate sensitivity, annual phase transformations were weighted by the
inverse of the approximate arrival variance

    Var(target arrival - source arrival)
      ~= sd_target^2 + sd_source^2,

ignoring covariance.

Results:

Pair-weighted:
- delta = **-0.921 d**;
- pair-incidence bootstrap 95% CI = **-1.910 to +0.124 d**.

Equal-species:
- delta = **-1.525 d**;
- 95% CI = **-2.344 to +0.146 d**.

The point estimate remains negative, but both intervals cross zero.

This weighting changes the ecological estimand by giving greater influence to
years with more precise arrival estimates; it is therefore not a replacement
for the equal-year stagewise mean. It nevertheless shows that the strength of
the stagewise contrast is sensitive to how heterogeneous observation precision
is weighted.

## Interpretation

The strongest defensible statement is:

> **The more-negative late-period population-front phase transformation survives
> explicit propagation of reported arrival-date uncertainty around the
> posterior means, but is not fully robust to inverse-variance reweighting.**

Therefore the stagewise result should be used as a **same-system supporting
bridge**, not as a headline causal result.

Licensed:
- population-level relative timing changes across the mapped source and target
  stages;
- the direction of the late-minus-early phase transformation is robust to
  posterior-normal uncertainty propagation;
- observation precision differs strongly between periods.

Not licensed:
- individual birds corrected signed phase error;
- the stagewise contrast is invariant to all measurement-error treatments;
- the result identifies controller gain or actionability;
- the restricted subset represents the full 166-pair environmental network.

## Provenance

Workflow:
- run: 37400881101
- artifact: 11385420543
- artifact SHA256:
  65db0bc4499044dd8a016f07aae83fdd0b0ac99b75c5aa33a4d0388ae1479ab5

Script:
analysis/movement_phenology/payoff_b_v8_stagewise_measurement_uncertainty.R
