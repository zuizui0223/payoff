# PAYOFF-B V8 source-event observability boundary — 2026-10-06

Status: **POSTHOC OBSERVABILITY AUDIT; FROZEN V8 PRIMARY UNCHANGED**

## Question

The reconstructed nonlocal predictor is annual source-cell mid-green-up date.

Even if that variable predicts target green-up retrospectively, a biological
interpretation requires asking whether the realized source mid-green-up event
occurred early enough to have been directly observable by the same species'
migration front.

This audit uses the restricted stagewise subset with:
- 56 species-source-target units;
- 31 unique source-target pairs;
- 14 species;
- at least six annual arrival estimates at both source and target cells in both
  periods.

It does not establish individual routes.

## Event order at the year-row level

Define three possible orders for the realized source mid-green-up event:

1. before population-front arrival at the source;
2. after source-front arrival but before target-front arrival;
3. after target-front arrival.

### Early window

389 annual source-target-species rows:

- source mid-green-up before source arrival: **29.8%**;
- source mid-green-up between source and target front arrivals: **29.6%**;
- source mid-green-up after target arrival: **41.6%**.

Mean timing:
- source mid-green-up occurred **4.21 d after** source-front arrival;
- source mid-green-up occurred **2.18 d before** target-front arrival.

### Late window

432 annual rows:

- source mid-green-up before source arrival: **45.8%**;
- source mid-green-up between source and target front arrivals: **18.3%**;
- source mid-green-up after target arrival: **36.1%**.

Mean timing:
- source mid-green-up occurred **0.70 d after** source-front arrival;
- source mid-green-up occurred **3.83 d before** target-front arrival.

## Pair-weighted summary

Across 31 source-target pairs:

Fraction of years in which source mid-green-up preceded source-front arrival:
- early pair mean = **0.285**;
- late pair mean = **0.433**.

Fraction in which the event occurred between source and target front arrivals:
- early = **0.299**;
- late = **0.212**.

Mean source event relative to source-front arrival:
- early = **+4.56 d** after source-front arrival;
- late = **+1.06 d** after source-front arrival.

Mean source event relative to target-front arrival:
- early = **2.64 d before** target arrival;
- late = **4.64 d before** target arrival.

## Interpretation

The reconstructed source mid-green-up variable is a useful **statistical
predictor** of the target environment, but its realized annual date is not a
demonstrated online cue available to birds at the source stage.

In a majority of annual observations in both periods, the population front had
already reached the source cell before source mid-green-up occurred.

In a substantial minority of years, source mid-green-up occurred only after the
population front had already reached the target cell.

Therefore the V8 G_CV quantity must be interpreted as:

> **ideal-observer / analyst forecast value of a reconstructed environmental
> predictor**

rather than:

> **organismally available value of a cue observed at the mapped source cell**.

## Consequence for the framework

The seasonal information chain should separate at least four layers:

    environmental forecastability
        ->
    organismal accessibility / inference
        ->
    retained actionability
        ->
    realized correction.

The bird data estimate the first layer and some population-level timing
geometry. They do not directly estimate the second or third layers.

This distinction sharpens rather than weakens the motivation for a sequential
framework: a forecastable environment does not imply that the corresponding
information is available to the organism at the relevant decision time.

## Claim boundary

Licensed:
- source mid-green-up is a retrospectively reconstructed target-predictive
  environmental variable;
- it is target-preceding on average in the restricted stage subset;
- its realized event is not consistently earlier than source-front or
  target-front arrival.

Not licensed:
- source mid-green-up was directly observed by birds;
- G_CV is organismal information value;
- the mapped source is a true cue-use location;
- increased G_CV represents increased biological access to information.

## Provenance

Workflow:
- run: 37405605460
- artifact: 11387276704
- artifact SHA256:
  e4174eaebeded173d267fe47426d712ed7e0ebf219565ff41bd29b2ff4598e1e

Script:
analysis/movement_phenology/payoff_b_v8_source_event_observability_audit.R
