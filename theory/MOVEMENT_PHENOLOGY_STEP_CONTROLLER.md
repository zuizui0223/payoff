# Discrete stopover phase control

Status: mathematical organization of the movement–phenology macro programme. The stability algebra is elementary and is not claimed as a literature-novel control theorem.

## Why a discrete controller is needed

The continuous phase-feedback model uses movement speed as the actuator.

The Svalbard barnacle-goose reconstruction shows a different architecture:

~~~text
arrive at stopover
-> adjust stopover duration
-> depart
-> rapid flight to next region
-> arrive with phase largely reset
~~~

Flight pace itself shows little phase-error dependence, while stopover duration responds strongly.

This motivates a discrete STEP controller.

## Route-stage map

Let

\[
E_i
=
A_i-T_i
\]

be phase error on arrival at stopover region \(i\), where \(A_i\) is animal arrival time and \(T_i\) is local environmental onset.

Let

\[
S_i(E_i)
\]

be stopover duration and

\[
F_i(E_i)
\]

the travel time to the next region.

Environmental onset advances by

\[
\Delta_i=T_{i+1}-T_i.
\]

Then

\[
E_{i+1}
=
E_i
+
S_i(E_i)
+
F_i(E_i)
-
\Delta_i.
\tag{S1}
\]

The local phase-transfer derivative is

\[
\lambda_i
=
\frac{dE_{i+1}}{dE_i}
=
1+S_i'(E_i)+F_i'(E_i).
\tag{S2}
\]

This is the directly comparable discrete controller quantity.

## Stopover-only corollary

If flight time does not respond detectably to phase error,

\[
F_i'(E)\approx0,
\]

then

\[
\lambda_i
=
1+S_i'(E).
\]

Define stopover gain

\[
g_{S,i}
=
-S_i'(E).
\]

Then

\[
\lambda_i=1-g_{S,i}.
\]

Interpretation:

~~~text
gS = 0
no phase correction through stopover

0 < gS < 1
partial correction

gS = 1
one-day-late arrival causes one-day-shorter stopover;
phase error is fully reset in one step if flight/environment terms are fixed

1 < gS < 2
stable overshoot / alternating correction

gS >= 2
locally unstable overshoot under the stopover-only map
~~~

For a repeated local map, stability requires

\[
|\lambda|<1
\]

or equivalently

\[
-2<S'(E_*)<0
\]

in the stopover-only case.

## Direct contraction estimator

Rather than infer contraction only from the stopover slope, fit

\[
E_{i+1}
=
a_i+\lambda_i E_i+\epsilon.
\tag{S3}
\]

The no-correction null is

\[
H_0:\lambda_i=1.
\]

A strong controller has

\[
|\lambda_i|\ll1.
\]

This estimator automatically includes all behavioral levers acting between the two arrival events, not only stopover duration.

## Svalbard barnacle-geese example

For the calibrated public-GPS reconstruction:

### Scotland / Solway -> southern Norway

Stopover response:

\[
S'(E)
\approx-0.910.
\]

Thus the stopover-only prediction is

\[
\lambda_{\rm stop}
\approx0.090.
\]

The direct arrival-to-arrival estimate is

\[
\hat\lambda
\approx0.070.
\]

This is striking agreement between the actuator-specific and net phase-transfer estimates.

### Southern Norway -> Svalbard

Stopover response:

\[
S'(E)
\approx-0.589,
\]

giving the stopover-only prediction

\[
\lambda_{\rm stop}
\approx0.411.
\]

The direct arrival-to-arrival estimate is near zero and slightly negative,

\[
\hat\lambda
\approx-0.106.
\]

The stronger-than-stopover-only correction is compatible with the known life-history transition from late stopover arrival to deliberate green-wave overtaking near the breeding grounds.

## Relation to continuous control

Two controller forms now share one phase concept.

### Continuous SURF controller

\[
\frac{dE}{ds}
=
\frac{1/u(E)-1}{c_e}.
\]

Local correction strength is summarized by a spatial relaxation scale.

### Discrete STEP controller

\[
E_{i+1}=M_i(E_i),
\qquad
\lambda_i=M_i'(E_i).
\]

Local correction strength is summarized by a per-step contraction factor.

Thus the macro programme should not force all taxa into one speed-gain parameter.

The general target is:

> **How strongly does phase error propagate after the animal has had one ecologically meaningful opportunity to correct it?**

## General actuator decomposition

For a stopover-to-stopover migrant,

\[
\lambda_i
=
1
+
\underbrace{S_i'(E)}_{\text{stopover actuator}}
+
\underbrace{F_i'(E)}_{\text{travel-time actuator}}.
\]

Other systems can add terms for departure date, route switching, or resource engineering.

This makes actuator differences biologically explicit while retaining a common output, \(\lambda\).

## Claim boundary

This derivation does not establish why the behavioral rule evolved or whether the resulting phase maximizes fitness.

The Svalbard empirical values depend on a reconstructed environmental timing surface. Their qualitative interpretation is licensed only after the registered climate-anchor sensitivity and source-data audits pass.
