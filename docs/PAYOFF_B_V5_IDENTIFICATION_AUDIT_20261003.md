# PAYOFF-B V5 identification audit — 2026-10-03

Status: **PREOUTCOME IDENTIFICATION LOCK**

This audit fixes the interpretation of the V5 timing-propagation coefficient
before any focal comparative `beta_AB` outcome is calculated or inspected.

## 1. What beta_AB measures

For sequential timing events A and B,

[
d_B = a + eta_{AB} d_A + arepsilon.
]

The unstandardized slope (eta_{AB}) is a **descriptive conditional timing-
propagation coefficient** in days/day.

It answers:

> among the individuals or paired units represented by an eligible effect, how
> much later (or earlier) is event B associated with a one-day later (or
> earlier) event A?

It does **not**, from observational data alone, identify:
- a causal fraction of experimentally imposed delay retained;
- behavioral correction gain;
- physiological flexibility;
- the amount of delay an individual would have retained under a counterfactual
  no-correction trajectory.

Persistent individual schedule differences, shared environmental drivers,
selection, and measurement error can all contribute to an observational slope.

Accordingly, V5 may use "propagation", "attenuation", "association", and
"statistical reset". It may use "buffering" as an ecological interpretation
only at the transition-class level and must not equate (1-eta) with causal
buffering capacity.

## 2. Evidence tiers

Each effect is assigned before its numerical value is inspected.

### Tier A — perturbation or repeated-individual anomaly

Eligible when the design isolates within-individual or experimentally induced
timing deviation, for example:
- experimental timing/state perturbation followed through a later stage; or
- repeated individuals across years with year-centered timing anomalies and
  individual identity controlled.

This tier provides the strongest basis for interpreting attenuation as actual
schedule adjustment.

### Tier B — same-cycle individual propagation

The same individuals are measured at A and B in one annual cycle, dates are
within-year centered or year-adjusted, and the raw individual data or an
unstandardized individual-level slope are available.

This is the **primary observational tier**. It estimates timing propagation but
does not separate adjustment from persistent individual schedules.

### Tier C — cohort/population aggregate

Effects based on paired cohort or population-level timing summaries rather than
individual A/B observations.

These are retained for descriptive secondary synthesis only and do not enter
the primary H1 stationary-versus-active comparison.

## 3. Measurement-error boundary

Classical error in event A attenuates (eta_{AB}) toward zero. Therefore an
apparently strong "buffer" can be created by poorly measured upstream timing.

V5 will code, before effect values are inspected:
- tracking/observation method;
- nominal timing resolution where reported;
- whether dates are directly observed versus geolocator/model-derived;
- whether event-date uncertainty is reported.

Prespecified sensitivities:
1. directly observed / high-resolution dates only;
2. exclude effects for which upstream timing uncertainty is large or
   unquantified relative to the biological interval, where such a classification
   can be made without seeing (eta);
3. if event-date uncertainty is supplied, perform an errors-in-variables or
   SIMEX-style sensitivity without replacing the declared baseline estimator.

No measurement-quality threshold may be chosen by inspecting effect sizes.

## 4. H2 available-time moderator

The H2 moderator must not be the focal individual's own (B-A) interval in the
same regression used to estimate (eta_{AB}).

Allowed effect-level definitions, in priority order:
1. source-reported typical/mean duration for the biological stationary period;
2. independently reported population/year mean duration;
3. cohort mean duration derived from the raw A/B dates, labelled
   SAME_SAMPLE_DERIVED;
4. leave-one-individual-out mean duration when individual-level calculations are
   required.

The primary H2 analysis uses source-reported or independently reported
effect-level duration where available. SAME_SAMPLE_DERIVED duration is a
prespecified sensitivity because it shares sampling information with the
effect estimate.

No species-average duration from an unrelated source may be inserted after
effect values are known.

## 5. Unit of inference

Multiple transitions from the same individuals, population, study, or species
are not independent.

The primary model therefore retains random/grouping structure for:
- study;
- species;
- population/cohort;
- source sample / individual panel where multiple transitions come from the
  same tracked individuals.

When one annual-cycle dataset yields several consecutive transitions, the
effects remain separate transition observations but their shared source sample
must be represented in the covariance/grouping structure.

## 6. Interpretation of H1

H1 is:

[
eta_{m stationary} < eta_{m active}.
]

A supported H1 licenses:

> timing associations are attenuated more strongly across stationary intervals
> than across active migration transitions in the eligible corpus.

It does not by itself license:

> stationary periods causally absorb more experimental delay.

The stronger causal wording requires support in Tier A effects or convergence
between Tier A and the observational synthesis.

## 7. Failure conditions

V5 stops before focal outcome interpretation if:
- too few Tier A/B effects exist in either ACTIVE or STATIONARY classes for a
  meaningful comparison;
- transition class can only be assigned after seeing effect values;
- the primary corpus depends on converting correlations, standardized
  coefficients, or repeatabilities into raw slopes;
- effect uncertainty cannot be recovered for enough studies to support the
  declared multilevel synthesis.

The failure result is `INSUFFICIENT_IDENTIFIABLE_CORPUS`, not an invitation
to change the estimand.

## 8. Relation to Wang et al. 2024

The Wang et al. global tracking compilation is a potentially valuable source
because it records four major annual-cycle dates across a large number of
migratory bird records.

However:
- its published aim and SEM are not the V5 estimator;
- individual and population-mean records must not be pooled as if equivalent;
- source studies overlapping the V5 literature corpus must be deduplicated;
- V5 must not back-calculate raw propagation slopes from published standardized
  SEM coefficients.

If raw individual timing records support the declared V5 effect, they may enter
under the same eligibility and tier rules as any other source.

## 9. Freeze statement

This document constrains all subsequent V5 extraction and analysis.

The biological phenomenon of buffering is prior art. The only prospective V5
contribution remains comparative quantification on a common descriptive
day-for-day propagation scale, with explicit limits on causal interpretation.
