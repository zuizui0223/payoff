# Cross-system movement–phenology controller framework

Status: macro-comparative scaffold. No pooled cross-system estimate is claimed yet.

## Why a controller comparison

The original PAYOFF-B theorem returns a fixed-rate optimum. The Stage-1 bird reanalysis and Stage-3 mule-deer analysis show that natural migrants may instead change movement behavior as their phenological phase error changes.

A useful cross-system question is therefore:

> **How strongly, around which phase offset, and over what distance do migrants correct phenological error?**

## Canonical comparative quantities

For each population/system, fit a local feedback law

\[
\log u = \alpha + \kappa E,
\]

where

- \(u=c_a/c_e\) is animal speed relative to environmental-wave speed;
- \(E=T_a-T_e\) is signed phenological phase error;
- \(\kappa\) is the controller gain.

### 1. Net phase-transfer coefficient

Across controller architectures, define

\[
\lambda
=
\frac{dE_{\rm after}}{dE_{\rm before}},
\]

where "after" means after one ecologically meaningful opportunity to correct phase error: a migration segment, stopover-to-stopover step, or full migration episode.

Interpretation:

~~~text
lambda = 1   no correction
0<lambda<1   partial correction
lambda = 0   complete phase reset
-1<lambda<0  stable overshoot
|lambda|>1   local phase amplification
~~~

This is the primary cross-architecture quantity because it can be estimated even when the actuator is speed in one system and stopover duration in another.

### 2. Actuator-specific gain

\[
\kappa=\frac{d\log u}{dE}.
\]

Interpretation:

~~~text
kappa > 0  stabilizing phase-error feedback
kappa = 0  no speed correction with phase error
kappa < 0  locally destabilizing feedback
~~~

For small changes, \(100\kappa\) is approximately the percent change in relative movement speed per day of phase error.

### 3. Stable phase offset

If \(\kappa>0\),

\[
E_*=-\frac{\alpha}{\kappa}.
\]

This is the phase at which \(u=1\): animal and environmental fronts move at the same speed.

Different taxa may have different \(E_*\). Capital breeders can rationally overtake a green wave, while other consumers may track near a food-quality peak. Therefore \(E_*=0\) is not a universal null.

### 4. Phase-correction distance

For environmental-wave speed \(c_e\),

\[
\ell=\frac{c_e}{\kappa}
\]

is the local e-folding distance for small phase perturbations around \(E_*\), with

\[
\ell_{1/2}=\frac{c_e\log 2}{\kappa}.
\]

This converts an abstract behavioral response into a spatial scale directly comparable with route length and barrier spacing.

## Secondary dimensions

Each system should also record:

~~~text
phase compression:
  slope of E_end on E_start

behavioral levers:
  speed adjustment
  stopover adjustment
  route switching
  departure-date adjustment

environmental predictability:
  autocorrelation / cross-site correlation in phenological anomalies

cue-resource coupling:
  direct food wave
  indirect vegetation proxy
  weak/unknown coupling

route geometry:
  continuous surfing
  stepping-stone stopovers
  barrier crossing
  jump migration

environment endogeneity:
  exogenous resource wave
  migrant modifies resource phenology
~~~

## Macro hypotheses

### M1 — predictability increases feedback gain

Where downstream phenology is predictable from current conditions, migrants can use current phase information to adjust subsequent speed or stopover.

Prediction: \(\kappa\) should increase as environmental predictability increases.

### M2 — barriers lengthen correction scale

Ecological barriers constrain speed/stopover adjustment and should reduce effective gain or increase the distance over which error is corrected.

Prediction: \(\ell\) should increase across barrier-dominated routes.

### M3 — cue relevance sharpens phase locking

When the measured environmental wave is closely coupled to the resource that determines performance, phase correction should be stronger and less noisy.

### M4 — strategy changes the equilibrium, not necessarily the gain

Capital breeders, income breeders, grazers, insectivores and jump migrants may have different stable phase offsets \(E_*\) even if all use stabilizing feedback.

Thus cross-taxon comparison should not standardize away \(E_*\) by forcing zero lag.

### M5 — endogenous waves break the exogenous controller model

If animals modify vegetation phenology, \(c_e\) is no longer independent of animal behavior. Such systems should be modeled as coupled animal–resource dynamics and used as an explicit boundary test.

## Evidence tiers

~~~text
Tier A
raw animal trajectories + environmental timing surface
-> direct u, E, kappa, E*, ell

Tier B
animal-year movement summaries + resource-wave propagation
-> population/controller estimates

Tier C
stopover arrival + local onset of spring + environmental predictability
-> phase-locking and predictability effects, but no direct continuous u

Tier D
published qualitative tracking classification only
-> hypothesis context, not pooled effect size
~~~

Only Tier A/B systems enter an initial quantitative controller meta-analysis.

For continuous controllers, report \(\kappa\), \(E_*\), and \(\ell\) where identifiable.

For discrete STEP/JUMP controllers, report actuator-specific gain and \(\lambda\).

For every direct system, \(\lambda\) is preferred when a defensible before/after phase pair exists.

## Current systems

~~~text
Amaral birds:
  population-front timing
  useful for broad heterogeneity / phase-centering
  not a direct individual controller estimate

Wyoming mule deer:
  Tier B
  direct movement-rate and annual green-wave speed
  strong positive phase-error feedback

Barnacle geese, three flyways:
  candidate Tier A/C
  strongest test of predictability and barriers

Eurasian wigeon:
  candidate Tier A
  migration-distance contrast

red deer:
  candidate Tier A/B
  jump versus surf strategy contrast

Yellowstone bison:
  boundary system with endogenous vegetation feedback
~~~

## Quantitative meta-analysis gate

Do not pool controller parameters until at least three independent Tier A/B systems have compatible definitions and uncertainty estimates.

The first cross-architecture pooled response should be a transformed phase-retention quantity based on \(\lambda\), with actuator-specific analyses retained separately.

For continuous controllers, a secondary hierarchical model can use:

\[
\kappa_i
=
\beta_0
+\beta_1 P_i
+\beta_2 B_i
+\beta_3 C_i
+u_{\rm taxon}
+u_{\rm study}
+\epsilon_i,
\]

where \(P\) is predictability, \(B\) barrier/route geometry and \(C\) cue-resource coupling.

The purpose is to explain controller variation, not estimate one global migration constant.
