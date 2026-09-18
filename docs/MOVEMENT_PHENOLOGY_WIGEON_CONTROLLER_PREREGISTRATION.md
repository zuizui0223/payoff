# Eurasian-wigeon direct controller preregistration

Status: **frozen before the direct TGS/controller workflow returns a promoted wigeon estimate**.

This document converts patterns already observed in the mule-deer and barnacle-goose systems into prospective predictions for a third taxon.

## Data and reconstruction gates

The wigeon direct analysis is promoted only if all of the following pass.

### Movement gate

The reconstruction must reproduce the published spring-migration sample closely enough to support the same ecological object:

~~~text
published:
  35 spring trajectories
  31 individuals
  median endpoint distance = 1899 km
  median migration speed = 48.2 km/day
~~~

Primary replication tolerances remain those encoded in the HMM receipt. Failure of track/individual count blocks controller promotion even if downstream regressions look favorable.

### Environmental gate

The independently reconstructed TGS response must recover the published arrival-phase distribution at least approximately:

~~~text
published arrival events with environment = 208
published median arrival after TGS onset  = 22.5 d
published Q1 / Q3                         = 13 / 35.3 d
~~~

The registered POWER validation requires sufficient events, a median within the predeclared tolerance, and IQR overlap.

### Transition-support gate

At least 30 consecutive staging-to-staging transitions from at least 10 individuals are required for the direct phase-retention model.

## Primary hypothesis W1 — phase contraction

For consecutive staging events,

\[
E_{i+1}
=
a+\lambda E_i+\text{route covariates}+\epsilon.
\]

The no-correction null is

\[
H_0:\lambda=1.
\]

Prospective prediction:

\[
\boxed{\lambda<1}
\]

with the stronger descriptive expectation

\[
|\lambda|<1.
\]

This is the primary third-taxon test.

No specific point value of \(\lambda\) is preregistered.

## Primary hypothesis W2 — stopover compensation

Existing direct systems with comparable stopover responses show:

~~~text
mule deer:
  gS = 0.492

Svalbard barnacle goose R2 -> R4:
  gS = 0.589

Greenland barnacle goose R2 -> R3:
  gS = 0.524

Barents barnacle goose R1 -> R2:
  gS = 0.591
~~~

where

\[
g_S=-\frac{dS}{dE}.
\]

The primary wigeon prediction is therefore directional:

\[
\boxed{S'(E)<0}.
\]

A late wigeon should, on average, spend less time at the next corrective staging opportunity.

### Prospective magnitude band

Before observing a promoted wigeon controller estimate, register the broad predictive band

\[
0.3<g_S<0.8.
\]

This band is **secondary**. The scientific test is the negative stopover slope; failure to land inside 0.3–0.8 does not invalidate phase control if net phase contraction is present through another actuator.

The narrow 0.49–0.59 range in the current systems is treated as hypothesis-generating, not as a universal half-correction law.

## Secondary hypothesis W3 — actuator decomposition

Write

\[
\lambda
=
1+S'(E)+F'(E),
\]

where \(F'(E)\) collects travel-time / route-progress correction not explained by stopover duration.

Estimate the implied non-stopover component

\[
F'(E)
=
\lambda-1-S'(E).
\]

Prediction:

- if stopover is the dominant actuator, \(F'(E)\) should be near zero;
- if wigeons also compensate through transit pace or route scheduling, \(F'(E)<0\);
- \(F'(E)>0\) would mean transit behavior counteracts stopover correction.

This is an actuator diagnostic, not a causal decomposition unless joint uncertainty is supported by cluster bootstrap.

## Secondary hypothesis W4 — migration distance shifts target phase

The published study already shows that longer-distance wigeons arrive progressively closer to spring phenology as migration proceeds.

The direct reconstruction therefore predicts a route-progress × total-distance effect on phase.

This is treated as a **target-phase / strategy effect**, not as evidence that long-distance birds necessarily have stronger feedback gain.

## Cross-system prospective test

The current primary direct systems have absolute phase retention:

~~~text
mule deer:               |lambda| ~ 0.107
Svalbard barnacle goose: |lambda| ~ 0.106
Greenland barnacle goose:|lambda| ~ 0.131
Barents barnacle goose:  |lambda| ~ 0.494
~~~

Thus every current primary system removes at least about half of incoming phase deviation per ecologically meaningful correction opportunity.

Prospective third-taxon prediction:

\[
\boxed{|\lambda|<0.75}
\]

is recorded as an exploratory cross-system forecast.

The formal primary null remains \(\lambda=1\), not the 0.75 threshold.

## Failure interpretations frozen in advance

If the promoted wigeon estimate gives:

~~~text
lambda ~ 1:
  little net phase correction despite staging

|lambda| > 1:
  phase amplification / route-stage instability

stopover slope >= 0 but |lambda| < 1:
  correction occurs through transit / route / departure timing rather than stopover

movement gate fails:
  no ecological controller interpretation

environment gate fails:
  movement result can be retained, but phenological controller inference is blocked
~~~

## Claim boundary

This preregistration does not claim that the current stopover-gain similarity is a new law.

A universal actuator-gain claim requires prospective replication in wigeon or another independent taxon plus a mechanism excluding trivial time-budget compression.
