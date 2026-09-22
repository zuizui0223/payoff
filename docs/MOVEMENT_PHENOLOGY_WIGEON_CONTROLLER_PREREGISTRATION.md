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


## Frozen outcome

Status: direct reconstruction completed after this preregistration was written.

### Replication gates

~~~text
movement reconstruction:
  PASS

environmental TGS validation:
  PASS

minimum transition / individual support:
  PASS
~~~

Key validation receipts:

~~~text
33 reconstructed tracks / 29 individuals
versus 35 / 31 published

median endpoint distance:
  1911 km reconstructed
  1899 km published

median TGS-relative staging arrival:
  20.93 d reconstructed
  22.5 d published
~~~

### W1 — net phase contraction

Prediction:

\[
\lambda<1.
\]

Observed:

~~~text
lambda = 0.85994
SE = 0.04509
p versus lambda=1 = 0.00190
~~~

Outcome:

~~~text
PRIMARY W1:
  PASS
~~~

### Exploratory strong-contraction forecast

Prediction:

\[
|\lambda|<0.75.
\]

Observed:

\[
|\lambda|=0.860.
\]

Outcome:

~~~text
EXPLORATORY STRONG-CONTRACTION FORECAST:
  FAIL
~~~

### W2 — stopover actuator

Directional prediction:

\[
S'(E)<0.
\]

Observed:

~~~text
slope = -0.000140
SE = 0.003902
p = 0.972
~~~

The sign alone is not treated as support because the fitted effect is effectively zero.

Secondary magnitude forecast:

\[
0.3<g_S<0.8.
\]

Outcome:

~~~text
W2 STOPOVER ACTUATOR:
  NOT SUPPORTED

SECONDARY GAIN BAND:
  FAIL
~~~

### W3 — actuator decomposition

Measured transit-speed response:

~~~text
log-speed gain = +0.00109 per phase day
p = 0.197
~~~

Neither measured stopover duration nor between-staging travel speed explains the significant net phase contraction.

Outcome:

~~~text
COMMON PHASE-RETENTION COORDINATE:
  SUPPORTED

COMMON MULE-DEER / GOOSE ACTUATOR:
  NOT SUPPORTED
~~~

### W4 — migration-distance moderation

Observed moderation of phase retention:

~~~text
beta = -0.0253
p = 0.371
~~~

Outcome:

~~~text
DIRECT DISTANCE MODERATION:
  NOT SUPPORTED
~~~

The published migration-distance result remains valid literature context but is not promoted as a replicated controller moderator here.

## Prospective interpretation

The third-taxon result supports a weaker and more general claim than the strongest initial forecast:

> wigeons retain less than the full incoming phase deviation across consecutive staging transitions, but they do so much more weakly than the strongest mule-deer / goose examples and without a detected speed or stopover actuator.

This outcome is retained as a partial-success / partial-falsification result and must not be rewritten as full confirmation.
