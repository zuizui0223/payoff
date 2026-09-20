# Flagship novelty audit — movement–phenology phase control

Status date: 2026-09-20.

Status: **claim-boundary audit, not proof of exhaustive literature novelty**.

## Purpose

The macro programme now has a broad bird falsification, direct phase-retention
reconstructions in three taxa, multi-flyway within-species replication, and
perturbation/endogeneity boundary systems.

That evidence is scientifically useful only if the manuscript does not relabel
established migration-phenology concepts as new.

This audit therefore separates:

1. ideas already established in the migration literature;
2. generic control/dynamical-systems algebra that is not an ecological
   discovery;
3. the narrower synthesis/measurement contribution that may remain novel.

## Established prior art — do not claim as new

### Environmental information reliability

Bauer, McNamara & Barta (2020), *Proceedings of the Royal Society B*,
DOI 10.1098/rspb.2020.0622, explicitly analyze environmental variability,
reliability of information, and migration timing.

Therefore the idea that migrants benefit from predictable downstream
conditions is established.

PAYOFF-B may use an environmental-information channel, but should not present
that concept itself as novel.

### Predictability along stopover chains

Kölzsch et al. (2015), *Journal of Animal Ecology*,
DOI 10.1111/1365-2656.12281, show that spring conditions across successive
stopovers differ in predictability and that predictable progression can support
closer spring tracking.

Therefore:

~~~text
predictable route
-> better migration timing
~~~

is prior art.

### Green-wave surfing and route geometry

The ungulate green-wave literature already establishes that migration can track
spatial phenology and that landscape phenology geometry alters surfing
performance.

The SURF/JUMP distinction is also established in the red-deer literature.

Do not claim either green-wave surfing or the existence of alternative
surf/jump strategies as new.

### Compensatory pace / stopover plasticity

Ortega et al. (2023), *Nature Communications*,
DOI 10.1038/s41467-023-37750-z, already show that mule deer starting migration
out of phase with spring green-up alter movement rate and stopover duration and
arrive substantially closer to the forage wave.

Thus:

~~~text
phenological mismatch
-> faster/slower migration or altered stopover
~~~

is established empirically.

The PAYOFF-B reanalysis adds a common controller coordinate; it does not
discover compensation itself.

### Migration distance and target phase

van Toor et al. (2021), *Movement Ecology*,
DOI 10.1186/s40462-021-00296-0, show that migration distance affects how
closely Eurasian wigeon follow spring phenology.

Therefore route length / migration strategy affecting phenological phase is
prior art.

### Individual reaction norms

Recent behavioral-reaction-norm work on ungulates demonstrates repeatable
individual migration timing and plasticity to green-up timing.

Therefore individual intercept/slope variation in migration timing is not a
PAYOFF-B discovery.

### Anthropogenic decoupling

Aikens et al. (2022), *Nature Ecology & Evolution*,
DOI 10.1038/s41559-022-01887-9, show that industrial development can cause
mule deer to hold up and become decoupled from the green wave.

Therefore infrastructure-induced loss of surfing is established.

### Environmental endogeneity

Geremia et al. (2019), *PNAS*, DOI 10.1073/pnas.1913783116, show that bison
grazing can alter vegetation phenology.

Thus animals modifying the resource wave is established.

## Generic mathematics — do not claim as new

The following are elementary or standard dynamical/control results:

~~~text
monotone negative feedback stabilizes a crossing

AR(1) recursion:
  V_next = lambda^2 V + sigma^2

stationary variance:
  sigma^2 / (1-lambda^2)

continuous local relaxation / Ornstein-Uhlenbeck analogues
~~~

These equations are useful organizational tools but are not candidate
mathematical discoveries.

## Candidate contribution 1 — common empirical phase-retention coordinate

The direct programme defines, for one ecologically meaningful correction
interval,

\[
E_{\rm next}
=
a+\lambda E_{\rm current}+\epsilon.
\]

The common cross-system response is

\[
R_\phi=|\lambda|.
\]

This is deliberately more abstract than any single behavioral actuator.

Current direct taxa:

~~~text
Odocoileus hemionus
  lambda ~ 0.107
  mixed speed + stopover actuator

Branta leucopsis
  route-stage lambda values spanning strong reset to moderate retention
  stopover-dominated STEP architecture

Mareca penelope
  lambda ~ 0.860
  significant contraction without detected stopover or travel-speed actuator
~~~

The prospective wigeon test is particularly important because it supports the
weak contraction prediction while falsifying the stronger near-reset forecast.

A targeted literature search has not yet identified an animal-migration paper
that estimates this same signed phase-transfer coefficient as a declared
cross-taxon migration-phenology coordinate.

This is a **candidate novelty**, not an asserted exhaustive-first claim until
the final systematic search is completed.

## Candidate contribution 2 — information and retention as separate channels

The programme distinguishes environmental innovation from behavioral phase
retention:

\[
e_{i+1}
=
\lambda_i e_i-\xi_i+\eta_i.
\]

Under the declared linear approximation,

\[
V_{i+1}
=
\lambda_i^2 V_i+\sigma_{\xi,i}^2+\sigma_{\eta,i}^2.
\]

The ecological contribution is not the variance formula.

It is using independently reconstructed migration and phenology data to place
systems on two separable axes:

~~~text
environmental channel
  innovation / predictability

phase-transformation channel
  |lambda|
~~~

The direct barnacle-goose analysis is informative because the initial
prediction

~~~text
higher predictability -> stronger feedback
~~~

was not supported.

This forces an information-versus-correction decomposition rather than one
generic "tracking ability" score.

A targeted search has not identified a migration-phenology synthesis that uses
this exact empirical decomposition with directly estimated phase retention
across taxa.

Again, retain a conservative "we introduce/use" phrasing until the final search
is complete.

## Candidate contribution 3 — actuator architecture below a common response

The empirical systems separate:

~~~text
MIXED
  speed + stopover

STEP
  stopover-to-stopover correction

PHASE RETENTION WITHOUT IDENTIFIED REACTIVE ACTUATOR
  wigeon

JUMP / OVERTAKE
  route-stage target changes

ENGINEER
  environmental wave becomes endogenous
~~~

The strategy labels themselves are not all new.

The candidate synthesis contribution is the hierarchy:

\[
\text{common response } R_\phi
\quad+\quad
\text{actuator-specific mechanism}.
\]

This avoids two opposite errors:

1. forcing heterogeneous systems into one universal behavioral coefficient;
2. treating every migration system as incomparable.

## Candidate contribution 4 — controller feasibility boundaries

The framework separates:

\[
(P,G,\chi)
\]

where

~~~text
P
  usable environmental information / predictability

G
  behavioral control permeability / ability to express correction

chi
  environmental endogeneity
~~~

These ingredients all have ecological precedent.

The candidate contribution is explicitly separating them as different reasons
for phenological mismatch within one phase-control framework.

## Strongest manuscript framing after novelty audit

Avoid:

> Animals adjust migration to phenology.

Avoid:

> Predictability causes stronger behavioral feedback.

Avoid:

> Successful migrants share one optimal speed ratio.

Avoid:

> We discover a new negative-feedback law.

Preferred:

> **Phenological migration can be represented by the fraction of incoming phase
> deviation retained after an ecologically meaningful movement opportunity.
> Across directly reconstructed taxa, phase retention is portable but highly
> heterogeneous, while environmental predictability and behavioral correction
> act as separable channels.**

A second sentence can add:

> **This distinction explains why precise migration timing can arise from
> predictable environments, strong error correction, or both, and why
> disturbance or environmental endogeneity create qualitatively different
> failure modes.**

## Flagship novelty gate

Before any Ecology Letters attempt, complete a systematic search covering:

~~~text
"phase retention" + migration
"phase transfer" + migration
"phase error" + phenology + migration
feedback/feed-forward + migration timing
control theory + green-wave surfing
state-space / AR models of migration mismatch
predictive vs reactive migration timing
~~~

and forward/backward citation searches from:

~~~text
Bauer et al. 2020
Kölzsch et al. 2015
Bischof et al. 2012
van Toor et al. 2021
Aikens et al. 2022
Ortega et al. 2023
recent migration reaction-norm papers
~~~

Promotion requires no prior paper already making the same combined empirical
claim:

~~~text
direct cross-taxon lambda
+ environmental innovation decomposition
+ actuator architecture
+ perturbation/endogeneity boundaries
~~~

Until that gate is complete, use:

~~~text
framework
common coordinate
direct comparative reconstruction
two-channel decomposition
prospective cross-taxon validation
~~~

rather than:

~~~text
first universal law
new control theorem
first demonstration that migrants compensate phenology
~~~


## 2026-09-20 structured search update

A dedicated structured web literature screen is now frozen in:

```text
docs/MOVEMENT_PHENOLOGY_SYSTEMATIC_NOVELTY_SEARCH_20260920.md
```

The most important new boundary identified is the older autoregressive
phenology literature. Post et al. (2001) and Forchhammer et al. (2002) already
use autoregressive coefficients to describe temporal dependence in phenological
timing, including migration arrival. Chronobiology also has a mature
phase/entrainment vocabulary.

Therefore neither autoregression nor "phase" terminology is a novelty claim.

The candidate contribution is narrower:

```text
within-migration animal-environment phase retention
+ direct cross-taxon reconstruction
+ environmental innovation separated from retained error
+ actuator-specific mechanism
+ perturbation/endogeneity boundaries
```

The structured search did not identify a prior migration paper combining this
full empirical package.

### Gate revision

For the GEB lane:

```text
structured targeted novelty search:
  PASS

conservative novelty language:
  PASS
```

For an Ecology Letters first-priority claim:

```text
formal bibliometric / citation-graph search:
  OPEN
```

Use "we introduce a common empirical coordinate" rather than "first" language.
