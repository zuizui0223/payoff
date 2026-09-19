# Phenological migration as phase control: from broad-scale mismatch to feedback, strategy, and failure

Status: **manuscript architecture V0; not submission-ready**.

Candidate paper class: macroecological comparative research / synthesis with original reanalysis.

## One-sentence claim

Migratory tracking is better understood as **phase control** than as universal zero-lag or universal speed matching: migrants differ in target phase and strategy, and their ability to correct phase error depends on environmental predictability, behavioral control permeability, and whether the resource wave is exogenous.

## Why this paper exists

The movement–phenology literature already establishes green-wave surfing, jumping, migration-timing plasticity, environmental predictability effects, anthropogenic decoupling, and ecosystem engineering.

The unresolved synthesis problem is that these systems are usually analyzed with incompatible response variables:

~~~text
days from peak
arrival minus onset of spring
surfing score
migration speed
stopover duration
reaction-norm slopes
resource selection
~~~

The paper proposes a common phase-control representation.

## Core coordinates

Let

\[
E=T_a-T_e
\]

be signed phenological phase error and

\[
u=\frac{c_a}{c_e}
\]

be animal speed relative to the environmental front.

For a local controller

\[
\log u=\alpha+\kappa E,
\]

define

\[
E_*=-\frac{\alpha}{\kappa},
\qquad
\ell=\frac{c_e}{\kappa}.
\]

Interpretation:

~~~text
kappa  controller gain
E*     stable / target phase
ell    spatial correction scale
~~~

The framework explicitly allows \(E_*\neq0\).

## Result 1 — a universal natural speed optimum fails in broad bird data

Reanalysis of Amaral et al. (2025):

~~~text
5816 observations
55 migratory bird species
15 years
median animal/environment front-speed ratio = 1.263
median directional alignment = 0.948
~~~

Raw arrival–green-up mismatch has a flexible minimum far below the order-one PAYOFF-B benchmark.

After removing each species × cell's usual phase offset, point minima return to order-one values, but are shallow and highly uncertain.

Species-level optimum diagnostics are heterogeneous and are not explained by HWI, body mass, overwinter latitude, simple phenological sensitivity, route-direction concentration, alignment, or simple interannual timing variability.

Interpretation:

> There is no evidence here for one universal natural speed-ratio constant; the appropriate quantity is preservation of a system-specific phase relationship.

## Result 2 — mule deer show a strong phase-error controller

Official Ortega et al. (2023) source data:

~~~text
152 animal-years
72 individuals
8 years
~~~

Controller fit:

\[
\log u
=
\alpha+0.01830E_{\rm start}.
\]

Individual-clustered inference:

~~~text
kappa = 0.01830 d^-1
SE = 0.001223
p = 1.21e-50
positive slope in 8/8 years
~~~

Each additional day late is associated with approximately 1.85% higher relative movement speed.

Stopover response:

~~~text
-0.492 stopover days per +1 day late
cluster p = 6.07e-37
~~~

Absolute phase error declines strongly between migration start and end:

~~~text
mean start = 21.91 d
mean end   = 11.12 d
mean reduction = 10.79 ± 1.41 d
cluster p = 2.28e-14
~~~

Derived controller scales:

~~~text
E* ≈ 8.46 d
median c_e ≈ 5.61 km/d
ell ≈ 307 km
half-error distance ≈ 213 km
~~~

Interpretation:

> This system exhibits an observational closed-loop phase-correction signature rather than fixed-speed tracking.

## Result 3 — environmental predictability controls phase precision in barnacle geese

Kölzsch et al. (2015) provide independent Tier-C evidence across three flyways.

Spring predictability differs strongly among consecutive stopovers and across route barriers.

Arrival-phase precision improves under greater predictability, while a binary barrier label itself is not retained as the key predictor in the integrated mixed model.

Interpretation:

> Environmental information quality is a separate prerequisite for effective phase control.

## Result 4 — a preregistered third taxon contracts phase weakly without the same actuator

The Eurasian-wigeon lane prospectively tested whether the common phase-retention coordinate transports to a third taxon.

Movement reconstruction reproduces the published sample closely:

~~~text
33 reconstructed spring tracks versus 35 published
29 individuals versus 31 published
median endpoint distance 1911 km versus 1899 km
~~~

Independent TGS reconstruction also reproduces the published arrival-phase distribution:

~~~text
reconstructed median arrival phase = 20.93 d
published median                   = 22.5 d
~~~

For 224 consecutive staging transitions from 28 individuals,

\[
\lambda=0.860\pm0.045
\]

and the no-correction null

\[
H_0:\lambda=1
\]

is rejected:

~~~text
p = 0.00190
~~~

Thus the preregistered primary prediction \(\lambda<1\) is supported.

However, the preregistered exploratory forecast

\[
|\lambda|<0.75
\]

is falsified.

The measured actuators are also unsupported:

~~~text
stopover slope:
  approximately 0
  p = 0.972

travel-speed phase response:
  p = 0.197
~~~

Interpretation:

> Wigeon validates the cross-taxon **phase-retention coordinate**, but does not validate a universal reactive speed/stopover feedback mechanism.

This is a useful prospective failure of the stronger hypothesis. Direct phase contraction ranges from near reset in some mule-deer / goose systems to weak contraction in wigeon.

## Result 5 — target phase and strategy can change without stronger feedback

The published wigeon study reports that longer-distance migrants arrive progressively closer to local spring phenology as migration proceeds.

The present direct reconstruction does not detect a corresponding migration-distance effect on \(\lambda\), so migration distance is treated as a target-phase / strategy context rather than a promoted feedback moderator.

Norwegian red deer show a different strategy entirely: rapid migration "jumps" the green wave, followed by smaller-scale phenological tracking.

Interpretation:

> Strategy can alter the target phase or the architecture of correction without implying stronger local feedback gain.

## Result 6 — tracking can fail for different reasons

### Actuation failure

Long-term industrial development in a mule-deer corridor caused deer to hold up at the developed area and reduced route-scale green-wave surfing by 38.65%.

Interpretation: the desired corrective response can be blocked even when environmental information exists.

### Environmental endogeneity

Yellowstone bison eventually allow the satellite green wave to pass while grazing feedback maintains forage quality and changes vegetation phenology itself.

Interpretation: the environmental wave cannot always be treated as an independent target.

## Three controller boundaries

The empirical synthesis motivates three axes:

\[
(P,G,\chi)
\]

where

~~~text
P   environmental predictability / information
G   behavioral control permeability / actuation
chi environmental endogeneity
~~~

High \(P\), high \(G\), low \(\chi\) is the clearest regime for classical phase locking.

Low \(P\), low \(G\), and high \(\chi\) represent biologically distinct failure modes and should not be collapsed into one "mismatch" variable.

## Movement-strategy taxonomy

~~~text
SURF      continuous phase control
STEP      stopover-to-stopover control
JUMP      rapid relocation then phase reacquisition
OVERTAKE  systematic target-phase change along route
ENGINEER  animal modifies the resource wave
~~~

The taxonomy is descriptive and uses established ecological phenomena; the contribution is to embed them within a common phase-control framework.

## Figure plan

### Figure 1 — phase-control geometry

Panels:

A. timing surfaces and nonzero constant phase offset  
B. \(u(E)\) crossing one at \(E_*\)  
C. stable phase-error flow  
D. \(\kappa, E_*, \ell\) definitions

### Figure 2 — broad bird falsification of a universal constant

A. raw mismatch versus speed ratio  
B. phase-centered mismatch versus speed ratio  
C. species-level supported vertices  
D. null moderator scan

Message: broad data reject one global natural constant and motivate phase centering.

### Figure 3 — mule-deer controller

A. start phase error versus log relative movement speed  
B. start phase error versus stopover duration  
C. absolute start versus end phase error  
D. year-specific \(\kappa\) estimates

Message: direct compensatory feedback is strong and temporally reproducible.

### Figure 4 — comparative phase-control regimes

Rows: bird population fronts, mule deer, barnacle geese, wigeon, red deer, industrial mule deer, bison.

Columns:

~~~text
direct controller estimate
predictability
actuation
environment endogeneity
strategy
target phase behavior
~~~

### Figure 5 — macro phase diagram

Conceptual \(P,G,\chi\) cube or slices locating empirical systems and generating predictions.

This figure can now remain as the main synthesis figure, but its axes must separate environmental innovation from phase retention and avoid treating related goose transitions as independent studies.

## Main hypotheses for the next data phase

### H1 — information

Higher environmental predictability reduces downstream phenological innovation. It need not increase behavioral feedback gain.

### H2 — actuation

Disturbance / barriers reduce effective control permeability and lengthen correction distance.

### H3 — strategy

Continuous resource corridors favor SURF/STEP control; discontinuous seasonal resources favor JUMP dynamics.

### H4 — target phase

Life history and migration distance shift \(E_*\) even when feedback remains stabilizing.

### H5 — endogeneity

Strong ecosystem engineering weakens the correspondence between remotely sensed phase mismatch and realized resource quality.

## Journal route

### Current realistic route

**Global Ecology and Biogeography** is now the active realistic target.

The evidence base includes a 55-species broad-scale test, direct phase-retention estimates in three taxa, multi-flyway replication within barnacle geese, and explicit perturbation / endogeneity boundary systems. Remaining work is synthesis, robustness, figures and novelty positioning rather than acquisition of a third taxon.

### Higher-risk route

**Ecology Letters** becomes reasonable only if the programme obtains multiple independent quantitative controller estimates and demonstrates a genuinely general principle beyond re-expression of established green-wave plasticity.

A likely gate is:

~~~text
>= 3 independent Tier A/B systems
+ quantitative moderator result
+ one successful perturbation/failure prediction
+ novelty audit showing controller-coordinate synthesis is not already published
~~~

Without those, an Ecology Letters submission would be premature.

## What would falsify the framework

The framework becomes weak if, across independent Tier-A systems:

1. directly reconstructed phase retention is indistinguishable from no retention structure across additional taxa;
2. environmental innovation and phase retention fail to explain any variation in phase precision;
3. actuator-specific results do not survive source / calibration robustness checks;
4. route disturbance does not alter the relevant control or precision quantities in quantitative tests;
5. the strategy / boundary categories add no explanatory value beyond descriptive relabeling.

These are genuine empirical failure conditions, not post-hoc escape clauses.

## Current status

~~~text
BROAD 55-SPECIES BIRD TEST           COMPLETE
MULE-DEER DIRECT CONTROLLER          COMPLETE
SVALBARD GOOSE DIRECT STEP           COMPLETE
GREENLAND GOOSE DIRECT STEP          COMPLETE
BARENTS GOOSE DIRECT STEP            COMPLETE
WIGEON THIRD-TAXON PHASE RETENTION   COMPLETE

THREE-TAXON PHASE-RETENTION GATE     PASS
THREE-TAXON COMMON ACTUATOR GATE     OPEN

RED-DEER STRATEGY BOUNDARY           REGISTERED
INDUSTRIAL PERTURBATION              REGISTERED
BISON ENDOGENEITY BOUNDARY           REGISTERED
PRIOR-ART BOUNDARY                   REGISTERED

INFORMATION × RETENTION SYNTHESIS     ACTIVE
HARMONIZED PERTURBATION TEST          OPEN
GLOBAL EBIRD TEST                     ACCESS-KEY GATED
~~~


## Revised synthesis — information and feedback are not the same axis

The multi-flyway direct analysis changes the causal architecture of the paper.

The paper should no longer state:

> greater environmental predictability produces stronger behavioral feedback.

Instead, distinguish two control channels:

\[
\text{environmental prediction}
\quad\perp\quad
\text{behavioral phase correction}.
\]

A compact STEP representation is

\[
E_{i+1}
=
a+\lambda E_i+\zeta_i+\eta_i,
\]

where:

~~~text
lambda
= fraction/sign of incoming phase error retained after correction

zeta
= downstream environmental innovation not predicted from current conditions

eta
= remaining behavioral / measurement noise
~~~

For stable repeated steps,

\[
\operatorname{Var}(E)
=
\frac{\sigma_\zeta^2+\sigma_\eta^2}{1-\lambda^2}.
\]

This gives the paper a clearer ecological result:

> **Migration timing can remain precise either because the future environment
> is predictable, because animals strongly correct realized errors, or through
> a combination of both.**

The direct barnacle-goose transition screen does not show a positive monotonic
relationship between environmental predictability and feedback correction.
That negative result is informative because it separates the mechanisms rather
than forcing both into one "tracking ability" variable.

### Revised figure logic

Figure 4 should become a two-channel comparison:

~~~text
x-axis:
  environmental innovation / predictability

y-axis:
  phase retention |lambda|

symbol / facet:
  actuator architecture

annotation:
  SURF / STEP / JUMP / OVERTAKE / ENGINEER
~~~

Interpretive quadrants:

~~~text
low innovation + low |lambda|
  predictable environment + strong correction

low innovation + high |lambda|
  feed-forward dominated

high innovation + low |lambda|
  feedback dominated

high innovation + high |lambda|
  high mismatch risk
~~~

This is stronger than a one-dimensional ranking of migration "tracking
quality".
