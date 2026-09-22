# Barnacle-goose multi-flyway direct-controller receipt

Status: **within-species multi-flyway direct replication complete**.

Primary biological source: Kölzsch et al. (2015), *Journal of Animal Ecology*, DOI 10.1111/1365-2656.12281.

Public tracking sources:

~~~text
Greenland  10.5441/001/1.5d3f0664
Svalbard   10.5441/001/1.5k6b1364
Barents    10.5441/001/1.ps244r11
~~~

The three flyways are analyzed with a common stopover reconstruction and annual
spring-onset anomaly pipeline. Fixed-transition controller slopes are invariant
to an unknown constant mean onset at a region, so absolute regional phase
anchors are not required for the primary \(\lambda\) estimates.

## Common direct quantity

For arrival phase \(E_i\) at one stopover and arrival phase \(E_{i+1}\) after
the next movement step,

\[
E_{i+1}=a+\lambda E_i+\epsilon.
\]

The no-correction null is

\[
H_0:\lambda=1.
\]

Define retained phase magnitude and correction strength as

\[
R_\phi=|\lambda|,
\qquad
C_\phi=1-|\lambda|.
\]

Interpretation:

~~~text
|lambda| < 1   stable contraction
lambda < 0     contraction with overshoot
lambda ~ 0     near-complete reset
|lambda| > 1   phase amplification
~~~

The actuator-specific stopover gain is

\[
g_S=-\frac{dS}{dE}.
\]

## Svalbard primary transition

Southern Norway -> Svalbard:

~~~text
N = 16 transitions
15 individuals

stopover slope = -0.589 day/day
cluster SE = 0.0876
p = 1.77e-11

lambda = -0.106
SE = 0.259
p versus no-correction lambda=1 = 2.01e-5

|lambda| = 0.106
correction strength = 0.894
~~~

Flight/transit pace itself does not show a detectable phase-error response:

~~~text
log-speed gain = +0.0153 per phase day
cluster p = 0.421
~~~

The main actuator is therefore stopover duration, followed by an Arctic
OVERTAKE transition.

## Greenland direct transition

The clearest adjacent reconstructed Greenland transition is R2 -> R3:

~~~text
N = 6 transitions
6 individuals

stopover slope = -0.5242 day/day
cluster SE = 0.1003
p = 0.00339

stopover gain = 0.524

lambda = 0.1307
SE = 0.08284
p versus no-correction lambda=1 = 9.31e-26

|lambda| = 0.131
correction strength = 0.869
~~~

This is strong stable phase contraction.

A separate Greenland transition R1 -> R2 gives \(\lambda\approx-1.08\) and is
not in the stable contraction regime. It is retained as route-stage
heterogeneity rather than averaged away.

## Barents direct transitions

A conservative adjacent transition R1 -> R2 gives:

~~~text
N = 12 transitions
8 individuals

stopover slope = -0.5915 day/day
cluster SE = 0.1091
p = 0.000988

stopover gain = 0.591

lambda = 0.4941
SE = 0.1294
p versus no-correction lambda=1 = 9.20e-5

|lambda| = 0.494
correction strength = 0.506
~~~

Other reconstructed Barents transitions show substantial route-stage
heterogeneity:

~~~text
R1 -> R5:
  lambda ~ -0.0086
  near-complete reset / slight overshoot

R2 -> R3:
  lambda ~ 0.538

R3 -> R5:
  lambda ~ 0.225

R4 -> R5:
  lambda ~ 1.249
  local phase amplification
~~~

Thus no single flyway-wide \(\lambda\) is biologically adequate.

## Direct conclusion

Across all three flyways, the data reject the idea that stopover migrants
simply carry their prior phase error unchanged through every route stage.

The common result is not one universal controller gain.

It is:

> **Phenological phase is actively transformed at discrete migration stages,
> but the amount and even sign of correction depends on route stage.**

The Svalbard, Greenland and Barents results independently show that
ecologically meaningful movement steps can have \(|\lambda|\ll1\), while some
other transitions amplify or deliberately reverse phase.

## Predictability hypothesis — revised

An initial direct-data hypothesis was

~~~text
higher environmental predictability
-> smaller |lambda|
-> stronger feedback correction
~~~

Across the currently matched Greenland/Barents transition screen:

~~~text
N transition pairs = 7

Spearman(
  phenology predictability r,
  1-|lambda|
)
= -0.464

p = 0.294
~~~

The leave-one-transition-out sign is non-positive throughout the registered
screen.

This small, non-independent sample does **not** establish a negative ecological
relationship.

It does show that the direct data do not support identifying environmental
predictability with feedback gain.

The updated framework therefore separates:

~~~text
feed-forward channel:
  how predictable is downstream environmental timing?

feedback channel:
  after phase error exists, how much is retained after one correction step?
  -> lambda
~~~

High predictability can improve timing precision by reducing environmental
innovation without requiring stronger behavioral feedback.

## Evidence-gate consequence

Direct-controller population/route replications now include:

~~~text
mule deer:
  continuous/distributed speed + stopover controller

Svalbard barnacle goose:
  STEP stopover controller -> OVERTAKE

Greenland barnacle goose:
  STEP controller replication

Barents barnacle goose:
  STEP controller replication
~~~

Therefore the **population-level replication gate is passed**.

However, the evidence represents only two taxa:

~~~text
Odocoileus hemionus
Branta leucopsis
~~~

So the stronger cross-taxon gate remains open. Eurasian wigeon is the current
priority third taxon.

## Claim boundary

Licensed:

- three barnacle-goose flyways contain direct route-stage estimates of phase
  transfer;
- multiple transitions strongly reject the no-correction null;
- stopover duration is a repeatable behavioral actuator in the stable
  transitions highlighted above;
- controller strength is route-stage specific;
- simple positive predictability -> feedback-gain coupling is not supported by
  the current direct transition screen.

Not licensed:

- independence of all transition-level estimates;
- a species-wide or universal goose \(\lambda\);
- a causal effect of predictability on feedback gain;
- pooling the three flyways as three independent taxa;
- claiming global macroecological generality before a third taxon is directly
  reconstructed.
