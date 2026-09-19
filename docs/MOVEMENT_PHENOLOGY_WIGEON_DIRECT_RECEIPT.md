# Eurasian-wigeon direct phase-retention receipt

Status: **third-taxon direct phase-retention reconstruction complete**.

Primary source: van Toor et al. (2021), *Movement Ecology* 9:61, DOI 10.1186/s40462-021-00296-0.

Tracking source: public Movebank DOI 10.5441/001/1.dv5mm289.

Environmental validation source: NASA POWER daily T2M, transformed with the published 5 °C thermal-growing-season rule.

This analysis was preregistered internally in docs/MOVEMENT_PHENOLOGY_WIGEON_CONTROLLER_PREREGISTRATION.md before a promoted direct estimate was available.

## 1. Movement reconstruction gate

The published study reports:

~~~text
35 spring trajectories
31 individuals
median endpoint distance = 1899 km
Q1 / Q3 = 1155 / 3130 km
maximum = 4184 km
median migration speed = 48.2 km/day
Q1 / Q3 = 30.0 / 60.9 km/day
~~~

The reconstructed original-Movebank lane gives:

~~~text
33 spring trajectories
29 individuals
median endpoint distance = 1911.0 km
Q1 / Q3 = 1153.0 / 3170.2 km
maximum = 4186.6 km

published-summary speed analogue:
median = 56.37 km/day
Q1 / Q3 = 39.00 / 85.53 km/day
~~~

All registered movement gates pass:

~~~text
track count within 4:             PASS
individual count within 4:        PASS
endpoint median within 25%:       PASS
speed median within 35%:          PASS
~~~

### Speed-estimator correction

An earlier internal reconstruction reported a median of about 74.6 km/day because it accumulated the full high-frequency HMM path.

The published Supplement computes its summary migration-speed quantity after HMM state 4 has been removed. The registered reconstruction was corrected to the same ecological object: cumulative geodesic distance through the non-state-4 sequence divided by its elapsed migration time.

The gate threshold was not relaxed.

## 2. Environmental validation gate

The direct analysis assigns local annual TGS onset to all reconstructed staging events using the published cumulative-minimum 5 °C rule.

Observed independent reconstruction:

~~~text
staging events total       = 256
events with TGS            = 256

arrival phase median       = 20.93 d
Q1 / Q3                    = 8.95 / 33.45 d
~~~

Published reference:

~~~text
environment-linked arrivals = 208
median                       = 22.5 d
Q1 / Q3                      = 13.0 / 35.3 d
~~~

Registered validation:

~~~text
event-count gate     PASS
median-phase gate    PASS
IQR-overlap gate     PASS
~~~

NASA POWER is an independent reconstruction, not the paper's original ERA5 grid.

## 3. Primary preregistered test W1 — phase contraction

For consecutive staging events, fit the progress-adjusted model

\[
E_{i+1}
=
a+\lambda E_i
+\text{route covariates}
+\epsilon.
\]

Equivalent fitted change coefficient:

\[
E_{i+1}-E_i
=
\beta_E E_i+\cdots
\]

with

\[
\lambda=1+\beta_E.
\]

Data:

~~~text
N transitions = 224
N individuals = 28
~~~

Result:

~~~text
beta_E = -0.14006
cluster SE = 0.04509
cluster p = 0.00442

lambda = 0.85994
SE = 0.04509

test of no correction:
H0: lambda = 1
p = 0.00190
~~~

Thus the registered primary prediction

\[
\lambda<1
\]

is supported.

The corresponding phase-retention and correction coordinates are

\[
R_\phi=|\lambda|=0.860,
\]

\[
C_\phi=1-|\lambda|=0.140.
\]

Approximately 14% of incoming phase deviation is removed per reconstructed staging-to-staging transition under this observational model.

## 4. Exploratory strong-contraction forecast — failed

Before the promoted result was available, the exploratory cross-system forecast was

\[
|\lambda|<0.75.
\]

Observed:

\[
|\lambda|=0.860.
\]

Therefore the strong-contraction forecast is **not supported**.

This is important: the third taxon broadens the direct-controller range rather than reproducing the near-reset behavior seen in the strongest mule-deer and barnacle-goose examples.

## 5. Preregistered W2 — stopover actuator not supported

Registered prediction:

\[
S'(E)<0.
\]

Observed:

~~~text
stopover slope = -0.000140 day/day
cluster SE = 0.003902
p = 0.972
~~~

The point sign is negative but the effect is essentially zero and unsupported.

The secondary predicted stopover-gain band

\[
0.3<g_S<0.8
\]

is therefore not supported.

## 6. Transit-speed actuator not supported

Observed travel-speed response:

~~~text
log travel-speed gain per phase day
= +0.00109

cluster SE = 0.000824
p = 0.197
~~~

There is no convincing evidence that late wigeons compensate through measured between-staging travel speed.

Therefore the observed net phase contraction should **not** be described as a replicated speed or stopover feedback mechanism.

## 7. Migration-distance moderation not detected in the direct controller

Preregistered strategy hypothesis W4 was motivated by the published result that long-distance migrants progressively approach spring phenology.

In the direct retention model:

~~~text
origin-phase × total-distance moderation
beta = -0.0253
SE = 0.0278
p = 0.371
~~~

The independent route-progress × endpoint-distance phase model is also unsupported in this reconstruction:

~~~text
p = 0.670
~~~

Thus the original literature result remains useful context, but the present direct-controller reconstruction does not promote a new distance-moderation effect.

## 8. Cross-system interpretation

The three directly reconstructed taxa now occupy different controller regimes.

~~~text
mule deer
  strong distributed correction
  speed + stopover actuators
  lambda ~ 0.107

barnacle goose
  strong route-stage STEP correction
  stopover actuator
  primary |lambda| ~ 0.106–0.494
  plus explicit route-stage amplification / overtake cases

Eurasian wigeon
  weak but significant phase contraction
  lambda ~ 0.860
  no detected stopover or travel-speed actuator
~~~

Therefore the cross-taxon result is **not**

> all migrants use the same behavioral feedback rule.

The licensed result is:

> **phase retention after an ecologically meaningful movement step can be placed on a common coordinate across taxa, while the strength and actuator architecture differ sharply.**

Wigeon is compatible with a more feed-forward / target-scheduling-dominated regime, but that mechanism is not directly identified by this analysis.

## 9. Gate consequence

~~~text
population / route direct replication:
  PASS

cross-taxon direct phase-retention gate:
  PASS
  taxa = 3

cross-taxon reactive-actuator gate:
  OPEN
  wigeon does not show the mule-deer / goose actuator signature
~~~

This distinction must be preserved in the manuscript.

## Claim ceiling

Licensed:

- the original Movebank/HMM movement reconstruction passes the registered movement gate;
- independent TGS reconstruction passes the registered environmental gate;
- wigeon phase retention is significantly below the no-correction value of one;
- the preregistered primary W1 phase-contraction prediction is supported;
- the stronger exploratory \(|\lambda|<0.75\) forecast is falsified;
- stopover and measured travel-speed actuator predictions are unsupported;
- the third taxon expands the common phase-retention coordinate without establishing a universal feedback actuator.

Not licensed:

- a causal behavioral-feedback interpretation of wigeon \(\lambda\);
- universal \(\lambda\), universal stopover gain, or universal correction fraction;
- claiming the published migration-distance mechanism was directly replicated;
- treating NASA POWER as the original ERA5 environmental dataset.
