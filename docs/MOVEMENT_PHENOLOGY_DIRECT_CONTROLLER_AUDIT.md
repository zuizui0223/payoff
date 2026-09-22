# Direct-controller registry audit

Status: descriptive synthesis of registered direct movement–phenology phase-control estimates.

## Common cross-system quantity

Actuator coefficients are not directly interchangeable.

~~~text
mule deer
  movement-speed response
  stopover response

barnacle geese
  discrete stopover response
  route-stage overtake / reset

Eurasian wigeon
  net staging-to-staging phase retention
  no detected stopover or travel-speed actuator
~~~

The common response is the fraction of incoming phase deviation retained after one ecologically meaningful movement/correction opportunity:

\[
R_\phi=|\lambda|.
\]

Define

\[
C_\phi=1-|\lambda|
\]

as phase-contraction strength.

This common coordinate does **not** imply that the same behavioral mechanism generates \(\lambda\) in every system.

## Registered primary direct rows

~~~text
mule deer, full spring migration
  lambda =  0.107
  |lambda| = 0.107
  actuator: speed + stopover

Svalbard barnacle goose, southern Norway -> Svalbard
  lambda = -0.106
  |lambda| = 0.106
  actuator: stopover + OVERTAKE

Greenland barnacle goose, R2 -> R3
  lambda =  0.131
  |lambda| = 0.131
  actuator: stopover

Barents barnacle goose, R1 -> R2
  lambda =  0.494
  |lambda| = 0.494
  actuator: stopover

Eurasian wigeon, consecutive staging transitions
  lambda =  0.860
  |lambda| = 0.860
  actuator: not identified
~~~

All five registered primary rows satisfy

\[
|\lambda|<1.
\]

However, the magnitude range is broad:

\[
0.106\lesssim |\lambda|\lesssim0.860.
\]

Thus the third taxon falsifies any emerging idea that successful migration generally requires near-complete phase reset.

## Preregistered wigeon outcome

The wigeon lane was frozen prospectively before promotion.

### Supported

Primary:

\[
H_0:\lambda=1
\]

is rejected in the contraction direction.

~~~text
lambda = 0.85994
SE = 0.04509
p versus lambda=1 = 0.00190
~~~

### Not supported

Exploratory strong-contraction forecast:

\[
|\lambda|<0.75
\]

was not met.

Stopover actuator:

~~~text
slope = -0.00014
p = 0.972
~~~

Travel-speed actuator:

~~~text
log-speed gain = +0.00109 per phase day
p = 0.197
~~~

Therefore wigeon counts as a direct **phase-retention** replication, not a replication of the mule-deer / barnacle-goose reactive actuator mechanism.

## Gate interpretation

Current direct evidence:

~~~text
registered primary direct rows = 5
taxa represented               = 3

Odocoileus hemionus
Branta leucopsis
Mareca penelope
~~~

Therefore:

~~~text
population / route replication gate:
  PASS

three-taxon phase-retention coordinate gate:
  PASS

three-taxon reactive-actuator gate:
  OPEN
~~~

The distinction is essential.

The data now support a common **measurement coordinate** across three taxa, while simultaneously showing that control architecture differs.

## What the five rows do and do not show

They support:

- phase can contract across continuous and discrete migration architectures;
- \(\lambda\) can be estimated on a common scale;
- correction strength varies strongly among systems and route stages;
- actuator identity is not universal;
- the third taxon prospectively confirms weak but significant phase contraction.

They do not support:

- one universal \(\lambda\);
- one universal stopover gain;
- a universal speed-response law;
- independence of the three goose rows;
- a conventional five-study meta-analysis;
- describing wigeon contraction as causal reactive feedback.

## Meta-analysis gate

A conventional random-effects meta-analysis remains inappropriate because three rows are from one taxon/source study and the five primary rows differ in observation interval and actuator architecture.

The next quantitative synthesis should be hierarchical and architecture-aware, or should aggregate to a declared taxon/population level before pooling.

The first useful cross-system comparison is therefore descriptive:

~~~text
phase retention:
  |lambda|

environmental information:
  innovation SD / predictability

actuator:
  speed / stopover / mixed / unidentified

strategy:
  SURF / STEP / OVERTAKE / other
~~~

## Claim boundary

The registered results establish three-taxon portability of the phase-retention coordinate.

They do **not** establish three-taxon portability of one behavioral feedback mechanism.
