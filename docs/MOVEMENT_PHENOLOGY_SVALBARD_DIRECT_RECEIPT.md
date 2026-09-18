# Svalbard barnacle-goose direct STEP-controller receipt

Status: **second direct movement–phenology controller system; route-stage specific and environmentally reconstructed**.

Primary source: Kölzsch et al. (2015), *Journal of Animal Ecology*, DOI 10.1111/1365-2656.12281.

Raw GPS: Movebank Data Repository DOI 10.5441/001/1.5k6b1364.

## 1. Raw-data reconstruction

The public Movebank source contains:

~~~text
24,488 GPS locations
22 public individual identifiers
6 spring seasons, 2006–2011
complete coordinates for all retained rows
~~~

A 30-km / >=48-h stay reconstruction yields:

~~~text
26 spring track-years
104 stopover events
4 broad regions used by >=3 individuals
mean stopovers per track = 4.00
mean broad regions per track = 2.73
~~~

Published Svalbard-flyway references are:

~~~text
4.2 stopovers per track
3.0 successive regions
~2600 km total route
~930 km between successive regions
~~~

The spatial reconstruction therefore recovers the published route structure closely.

Recovered broad regions:

~~~text
R1  Scotland / Solway Firth
R2  southern Norway / Helgeland
R3  northern Norway / Vesterålen
R4  Svalbard
~~~

## 2. Environmental timing

Annual onset of spring is reconstructed with:

~~~text
NASA POWER daily T2M
latitude-dependent GDD base temperature
cumulative GDD
logistic sigmoid
positive early maximum of the third derivative (GDD jerk)
~~~

Raw POWER absolute onset is biased at high latitude, so the analysis uses POWER annual anomalies around region means and calibrates the mean phase.

Explicit article means:

~~~text
R1 Scotland  = 26 March ~ DOY 85
R4 Svalbard  = 16 June  ~ DOY 167
~~~

Norwegian means are visually calibrated from published Fig. 3 and propagated through a registered +/-5-day grid:

~~~text
R2 = 113, 118, 123
R3 = 125, 130, 135
~~~

The primary southern-Norway controller result is invariant to a constant shift in the R2 mean phase.

The 30-y POWER onset IQR at R2 is approximately 10.0 days, closely matching the published statement that the two Norwegian regions have 30-y onset variability of about 10 and 12 days.

## 3. Primary direct controller: southern Norway -> Svalbard

Primary transition:

~~~text
R2 -> R4
N transitions = 16
N individuals = 15
~~~

### Flight-pace actuator

Regression:

\[
\log(c_{\rm animal})
\sim E_{\rm departure}.
\]

Result:

~~~text
behavioral speed gain = +0.01532 per phase day
cluster SE = 0.01904
cluster p = 0.421
~~~

There is no detectable evidence that flight/transit pace itself is the main phase-error actuator.

### Stopover actuator

Regression:

\[
S_{\rm R2}
\sim E_{\rm arrival,R2}.
\]

Result:

~~~text
stopover slope S'(E) = -0.588996 day/day
cluster SE = 0.087603
cluster p = 1.77e-11
~~~

Thus a goose arriving one day later relative to local spring leaves after about **0.59 fewer stopover days**.

Define positive stopover controller gain

\[
g_S=-S'(E).
\]

Then

\[
g_S=0.589.
\]

Under a stopover-only linear controller, the predicted phase-transfer slope is

\[
\lambda_{\rm stop}=1-g_S=0.411.
\]

This lies in the stable partial-correction regime.

## 4. Direct arrival-to-arrival phase contraction

Fit

\[
E_{\rm R4,arrival}
=
a+\lambda E_{\rm R2,arrival}.
\]

Result:

~~~text
lambda = -0.1063
cluster SE = 0.2595
p versus lambda = 0 = 0.682
~~~

The estimate is statistically compatible with complete phase reset.

The biologically relevant no-correction null is

\[
H_0:\lambda=1.
\]

That null is strongly rejected:

~~~text
z versus lambda=1 = -4.264
p = 2.01e-5
~~~

The first-order correction fraction is

\[
1-\lambda=1.106,
\]

consistent with correction followed by overshoot/overtaking.

Because destination phase uses the high-latitude environmental reconstruction, this direct \(\lambda\) is a secondary result until year-specific Svalbard onset is validated against the original climate series. The R2 stopover gain is the primary direct result.

## 5. Strategy transition: STEP -> OVERTAKE

Central calibrated descriptives for transitions entering Svalbard show:

~~~text
median phase on departure from origin stopovers  ~ +21.7 d
median phase on arrival at Svalbard              ~ -24.7 d
median phase change across the Arctic step       ~ -48.1 d
median transit time                              ~ 2.21 d
~~~

This is not continuous green-wave surfing.

The data are more naturally interpreted as:

~~~text
southern Norway:
  STEP controller
  later relative to spring -> shorter stopover

then:
  rapid Arctic crossing

Svalbard:
  arrive before local spring
  -> OVERTAKE phase appropriate to capital breeding
~~~

This matches the published qualitative conclusion that barnacle geese overtake the green wave near breeding grounds.

## 6. Anchor sensitivity

Across all 9 registered Norwegian mean-onset scenarios:

~~~text
R2->R4 behavioral speed gain:
  +0.015316 in every scenario
  positive fraction = 1.0

R2->R4 relative-speed gain:
  range +0.04005 .. +0.04726
  positive fraction = 1.0
~~~

The mean-anchor uncertainty therefore does not reverse the sign of the controller diagnostics.

Relative-speed gain itself is only marginal in the central fit:

~~~text
estimate = +0.04315
cluster p = 0.056
~~~

and is not the primary claim.

## 7. Secondary R1 -> R2 diagnostic

The automated reconstruction also gives:

~~~text
N = 18 transitions
stopover slope = -0.910
cluster p = 2.06e-7
arrival-to-arrival lambda = 0.070
p versus no-correction lambda=1 = 1.44e-13
~~~

However, the original paper explicitly excluded initial-stopover arrival timing from its main timing analyses because many birds were tagged too late to determine initial arrival correctly.

Therefore R1 -> R2 is retained only as a secondary consistency diagnostic, not as the primary direct-controller estimate.

## 8. Cross-system meaning

Mule deer and Svalbard geese both correct phenological phase, but with different actuator architecture.

~~~text
mule deer:
  speed gain strongly positive
  stopover duration also decreases
  continuous / distributed compensation

Svalbard barnacle geese:
  flight-pace gain not detectable
  stopover duration strongly decreases
  discrete STEP controller followed by OVERTAKE
~~~

The common variable is not one universal migration speed.

It is the propagation of phase error after an ecologically meaningful opportunity to correct it.

## Claim ceiling

Licensed:

- raw public GPS independently reproduces the Svalbard route/stopover structure;
- southern-Norway stopover duration strongly decreases with later phenological phase;
- flight/transit pace shows no detectable phase response in the same transition;
- the no-correction phase-transfer null is rejected;
- results support a STEP-to-OVERTAKE controller interpretation.

Not licensed:

- exact reproduction of the original ECA/NOAA onset series;
- exact Table-S1 Norwegian mean onsets;
- a universal goose \(\kappa\), \(E_*\), or \(\ell\);
- a causal decision rule or fitness optimum;
- treating R1 initial-stopover timing as primary evidence.

The direct system counts as Tier A for **discrete phase control**, not as a replicate of the mule-deer continuous speed-gain parameter.
