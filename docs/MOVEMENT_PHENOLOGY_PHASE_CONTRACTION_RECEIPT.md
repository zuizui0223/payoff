# Direct phase-retention synthesis receipt

Status: **three-taxon descriptive synthesis complete; no universal effect size claimed**.

## Common coordinate

Across continuous and stopover-based migration systems, define signed phase transfer over one ecologically meaningful correction interval as

\[
E_{\rm next}=a+\lambda E_{\rm current}+\epsilon.
\]

The common descriptive coordinate is

\[
R_\phi=|\lambda|,
\]

with contraction strength

\[
C_\phi=1-|\lambda|.
\]

Interpretation:

~~~text
|lambda| < 1
  stable contraction of incoming phase deviation

lambda < 0
  contraction with overshoot / sign reversal

lambda ~ 0
  near-complete reset

|lambda| > 1
  local phase amplification
~~~

This coordinate does **not** imply one behavioral mechanism.

## Direct taxon-level synthesis

The registry contains repeated barnacle-goose routes, so cross-taxon comparison is reduced to one descriptive record per taxon. Repeated routes contribute a within-taxon range rather than separate meta-analytic study weights.

### Odocoileus hemionus — mule deer

~~~text
direct rows = 1
lambda = 0.107
|lambda| = 0.107
correction strength = 0.893
~~~

Detected actuators:

~~~text
movement-speed response
+ stopover shortening
~~~

This is strong distributed phase correction over the spring migration interval.

### Branta leucopsis — barnacle goose

Highlighted direct route-stage estimates:

~~~text
Svalbard:   |lambda| = 0.106
Greenland:  |lambda| = 0.131
Barents:    |lambda| = 0.494
~~~

Taxon-level descriptive summary:

~~~text
median |lambda| = 0.131
range           = 0.106 .. 0.494

median correction strength = 0.869
range                      = 0.506 .. 0.894
~~~

The repeatable actuator in the highlighted stable transitions is stopover-duration adjustment. Other route stages include near-reset, overshoot, and local amplification, so there is no biologically defensible single flyway-wide lambda.

### Mareca penelope — Eurasian wigeon

Prospectively reconstructed result:

~~~text
N transitions = 224
N individuals = 28

lambda = 0.860
SE = 0.045
p versus no-correction lambda=1 = 0.00190

correction strength = 0.140
~~~

The preregistered contraction prediction is supported, but the stronger exploratory forecast

\[
|\lambda|<0.75
\]

is falsified.

Detected actuators:

~~~text
stopover response: unsupported
travel-speed response: unsupported
~~~

Thus wigeon contributes direct **phase-retention** replication without identifying the same reactive actuator seen in mule deer or barnacle geese.

## Cross-taxon result

Taxon-level median phase retention spans

\[
0.107\;\text{to}\;0.860.
\]

Taxon-level median correction strength spans

\[
0.140\;\text{to}\;0.893.
\]

Therefore the evidence rejects both of these stronger ideas:

> successful migrants all nearly reset phase error;

and

> successful migrants use one common speed/stopover controller.

The licensed common result is:

> **Phenological migration can be compared on a shared phase-retention coordinate across at least three taxa, while both correction strength and actuator architecture differ strongly.**

This makes heterogeneity part of the result rather than residual noise.

## Pseudoreplication rule

Do not pool the five primary registry rows as five independent studies.

The three barnacle-goose rows share:

~~~text
species
source paper
broad ecological design
partly shared route-level inference framework
~~~

For cross-taxon graphics and descriptive comparison:

~~~text
mule deer:
  point = direct estimate

barnacle goose:
  point = median across declared primary routes
  whisker = observed route range

wigeon:
  point = direct estimate
~~~

The whisker is an observed within-taxon range, **not** a confidence interval.

A conventional random-effects meta-analysis is not licensed at the current taxonomic sample size.

## Actuator architecture

The current direct systems separate into three regimes:

~~~text
MIXED reactive controller
  mule deer
  speed + stopover

STEP reactive controller
  barnacle goose
  stopover-dominated route-stage correction

PHASE RETENTION WITHOUT IDENTIFIED REACTIVE ACTUATOR
  Eurasian wigeon
  significant lambda < 1
  no detected speed or stopover response
~~~

This is central to the manuscript.

The ecological invariant candidate is no longer an actuator coefficient such as kappa or stopover gain.

It is the more abstract mapping:

\[
\text{incoming phase deviation}
\rightarrow
\text{retained phase deviation after a movement opportunity}.
\]

## Relation to environmental information

Behavioral phase retention and environmental predictability are different channels.

For a linearized step,

\[
e_{i+1}=\lambda_i e_i-\xi_i,
\]

with environmental innovation \(\xi_i\),

\[
V_{i+1}=\lambda_i^2V_i+\sigma_{\xi,i}^2.
\]

Thus precise timing can arise from:

~~~text
small environmental innovation
OR
strong feedback contraction
OR
both
~~~

The barnacle-goose multi-flyway screen does not support a simple positive predictability -> stronger-feedback relationship.

That negative result motivates the information-versus-retention plane used in the macro manuscript.

## PAYOFF-B connection

PAYOFF-B1 asks which **fixed movement rate** maximizes long-run growth in an exact periodic benchmark.

The empirical programme finds a different transferable object:

~~~text
PAYOFF-B1:
  fixed-rate timescale matching

natural migration:
  state- and route-dependent phase transformation
~~~

The bridge is not that all natural migrants should satisfy the exact PAYOFF-B optimum.

It is that temporal environmental change creates a measurable timescale/phase problem, and natural systems solve that problem with heterogeneous controller architectures.

## Publication gate consequence

~~~text
population / route replication:
  PASS

three-taxon direct phase-retention coordinate:
  PASS

three-taxon common reactive actuator:
  OPEN

universal phase-retention magnitude:
  REJECTED / NOT SUPPORTED
~~~

The next inferential target is not a pooled mean lambda. It is explaining where systems fall in the space of:

~~~text
environmental innovation
phase retention
actuator architecture
route strategy
control permeability
environmental endogeneity
~~~

## Claim boundary

Licensed:

- direct phase-retention estimates exist in three taxa;
- all declared primary taxon/route rows used for synthesis have \(|\lambda|<1\);
- phase-retention magnitude varies strongly;
- reactive actuator identity is not universal;
- wigeon prospectively confirms weak phase contraction while falsifying a stronger near-reset forecast.

Not licensed:

- one universal lambda;
- one universal correction fraction;
- three-taxon proof of one reactive feedback mechanism;
- conventional five-row meta-analysis;
- evolutionary optimality of the observed lambda values.
