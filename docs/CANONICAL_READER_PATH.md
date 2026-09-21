# Canonical reader path for PAYOFF

PAYOFF is easiest to read as one estimand being carried through progressively richer population models.

The invariant upstream chain is

```text
shared functional conflict
        |
        v
L = compromise/conflict load
        |
        v
R = recovered loss from extra dimensionality
  = sL in the registered quadratic bridge
        |
        v
phi = R-K = sL-K
  = optimized frequency-independent architecture gap.
```

Everything after `phi` asks a different population question.

For the shortest cross-scale map, read

```text
theory/PAYOFF_TRANSPORT_PRINCIPLE.md
```

before or after this path.

---

## Part I — static ecology and architecture

### 1. `theory/THEOREMS.md`

Start here.

Core results:

```text
shared optimum,
L=[ab/(a+b)](theta1-theta2)^2,
n-function weighted-disagreement identity,
partial release with residual coupling,
R=sL,
phi=sL-K.
```

This is the direct mathematical bridge from SCH through BALANCE to BITA.

### 2. `theory/NETWORK_EXTENSION.md`

Generalizes trait integration itself to a graph of functional coordinates and proves monotone recovery as coupling weakens.

Read this if the biological problem has more than two functions or partial modularization rather than one binary shared/differentiated contrast.

---

## Part II — well-mixed evolutionary game

### 3. `theory/POTENTIAL_AND_RISK_DOMINANCE.md`

Introduces

```text
Delta(p)=phi+eta(2p-1)
```

for shared versus differentiated architecture frequency.

Core outcomes:

```text
architecture dominance,
stable coexistence,
coordination bistability,
risk-dominance role of phi=0,
potential function.
```

### 4. `theory/ENVIRONMENTAL_PHASE_DIAGRAM.md`

Turns the one static crossing into reciprocal invasion surfaces

```text
K=R-eta,
K=R+eta.
```

Read this for environment-dependent BALANCE/BITA transitions in a well-mixed population.

---

## Part III — finite populations

### 5. `theory/FINITE_POPULATION_MORAN.md`

Adds drift and exact Moran fixation.

Core distinctions:

```text
static architecture advantage,
deterministic rare invasion,
stochastic single-mutant fixation.
```

Key receipts:

```text
rho_D/rho_S=exp[beta phi(N-2)],
3phi>eta
```

for weak-selection D advantage above neutrality.

### 6. `theory/STOCHASTIC_ARCHITECTURE_BARRIER.md`

Generalizes fixation from one mutant to arbitrary starting count and defines stochastic critical mass.

---

## Part IV — recurrent mutation and long-run occupancy

### 7. `theory/RECURRENT_MUTATION_STATIONARY.md`

Replaces absorbing fixation with mutation-selection-drift balance.

Core result:

```text
log(Pi_N/Pi_0)
-> log(u_SD/u_DS)+beta(N-2)phi
```

in the rare-mutation limit.

### 8. `theory/NEUTRAL_MUTATION_BENCHMARK.md`

Mandatory negative control before interpreting stationary polymorphism as selection.

Neutral stationary law is beta-binomial; symmetric mutation shape changes at

```text
mu_c=1/(N+2).
```

### 9. `theory/STATIONARY_IDENTIFICATION.md`

Shows how multiple `N` or `beta` conditions identify mutation bias separately from architecture selection and creates the independent test

```text
phi_stationary ?= phi_bridge=sL-K.
```

---

## Part V — spatial structure

Two spatial models are intentionally separate.

### 10A. Patch migration model

Read in this order:

```text
theory/SPATIAL_METAPOPULATION.md
-> theory/SPATIAL_AGGREGATION_IDENTIFICATION.md
-> theory/ENVIRONMENT_MOSAIC_SOURCE_SINK.md
-> theory/SOURCE_TOPOLOGY_SENSITIVITY.md
-> theory/SPATIAL_ENVIRONMENTAL_THRESHOLDS.md
-> theory/GENERAL_GRAPH_HETEROGENEITY_SWITCH.md
-> theory/TWO_PATCH_HETEROGENEITY_COORDINATION_SWITCH.md.
```

Key exact results:

```text
symmetric migration cancels directly from global mean;
spatial covariance changes aggregate selection;
rare spatial invasion = principal eigenvalue;
source-sink rescue threshold;
low-migration source-degree dilution;
common environmental shift moves the whole spectrum exactly;
habitat contrast can overcome positive-frequency coordination;
migration can collapse that reciprocal-invasion window.
```

### 10B. Microscopic regular graph model

Read

```text
theory/REGULAR_GRAPH_WEAK_SELECTION.md.
```

This is an Ohtsuki-Nowak weak-selection pair approximation, not the patch-migration model.

PAYOFF's special matrix gives

```text
phi_k=k phi/(k-2),
eta_k=eta.
```

---

## Part VI — temporal structure

### 11. `theory/COMMON_TEMPORAL_ENVIRONMENT.md`

Start temporal analysis here.

Exact null theorem:

```text
A(t)=A0+q(t)I
-> Lambda_temporal=Lambda0+mean(q).
```

Zero-mean common fluctuations have no long-run invasion effect.

### 12. `theory/TWO_PATCH_TEMPORAL_FLOQUET.md`

Use when relative patch quality changes through time.

The noncommutativity gate is

```text
[A_a,A_b]
propto
m[(r_1a-r_2a)-(r_1b-r_2b)].
```

This file introduces exact Floquet computation and the average-environment comparison.

### 13. `theory/TWO_SEASON_TEMPORAL_PREMIUM.md`

For exactly two seasons, read this next.

It closes the Floquet result analytically:

```text
Lambda_F
= center-average
  + acosh(C)/T,
```

and proves, for the declared symmetric two-patch operator,

```text
Lambda_F >= lambda_max(A_bar).
```

The rapid-switching premium is

```text
Lambda_F-lambda_max(A_bar)
=
T^2 w^2(1-w)^2 m^2(Delta patch contrast)^2
/[24 delta_bar]
+O(T^4).
```

### 14. `theory/ANTI_PHASE_SEASONAL_RESCUE.md`

Specializes to seasonal source switching:

```text
season A: (r_bar+x,r_bar-x)
season B: (r_bar-x,r_bar+x).
```

Exact result:

```text
Lambda_F
= r_bar-m
+(1/tau)asinh[
  m/sqrt(m^2+x^2)
  *sinh(tau sqrt(m^2+x^2))
].
```

The temporal premium is zero at both migration extremes and positive at finite intermediate migration, proving at least one intermediate migration optimum.

### 15. `theory/WEAK_CONTRAST_UNIVERSAL_MIGRATION_OPTIMUM.md`

Read this when

```text
|x|tau << 1.
```

Then

```text
tau P
= (x tau)^2 H(m tau)+O((x tau)^4)
```

with

```text
H(u)=[u-tanh u]/(2u^2).
```

The universal leading-order optimum is

```text
m_opt tau
=1.6061152988...
```

and

```text
P_max
~=0.13248753945 x^2 tau.
```

### 16. `theory/TEMPORAL_COORDINATION_INVERSION.md`

Reconnects temporal rescue to the original evolutionary game.

Both reciprocal architecture edges receive the same anti-phase premium:

```text
Lambda_D=phi_bar-eta+P,
Lambda_S=-phi_bar-eta+P.
```

Therefore

```text
eta_eff=eta-P.
```

At `phi_bar=0`:

```text
P<eta -> coordination,
P=eta -> reciprocal boundaries collapse,
P>eta -> reciprocal invasion.
```

Weak contrast yields the explicit threshold

```text
x^2 tau/eta
>7.54787962834...
```

for temporal source switching to overcome positive-frequency coordination.

### 17. `theory/TEMPORAL_PHASE_DIAGRAM.md`

This is the final temporal synthesis.

Use

```text
u=m tau,
v=x tau,
epsilon=eta tau,
psi=phi_bar tau.
```

The exact dimensionless premium `F(u,v)` gives

```text
ell_D=psi-epsilon+F,
ell_S=-psi-epsilon+F.
```

The four phases are

```text
reciprocal invasion,
mutual non-invasion,
D-only invasion,
S-only invasion.
```

At weak contrast the temporal inversion surface becomes

```text
v^2 H(u)=epsilon.
```

### 18. `docs/TEMPORAL_HANDOFF.md`

Use this before designing an experiment.

It freezes the preferred empirical order:

```text
seasonal L,s,K,eta first
-> construct seasonal architecture margins
-> freeze migration/Floquet prediction
-> test rare-architecture dynamics independently.
```

---

## Part VII — moving-environment tracking architecture

This lane is distinct from the static architecture game above. Here migration
and phenological change are themselves heritable tracking axes.

Read in this order:

```text
theory/MIGRATION_PHENOLOGY_TRACKING.md
-> docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md
-> docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md
-> docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md
-> theory/CLOSED_LOOP_MOVEMENT_PHENOLOGY_TRACKING.md
-> docs/PAYOFF_B_CLOSED_LOOP_TRACKING_RESULTS_20260920.md
-> docs/PAYOFF_B_MOVEMENT_FEEDBACK_LANDSCAPE_RESULTS_20260920.md
-> docs/PAYOFF_B_AIKENS_2022_PHASE_CONTROLLER_RECEIPT.md
-> docs/PAYOFF_B_PHASE_RETENTION_ACTUATOR_GATES_20260921.md
-> docs/PAYOFF_B_WIGEON_PHASE_RETENTION_RECEIPT_20260921.md
-> docs/PAYOFF_B_THREE_TAXON_PHASE_RETENTION_RECEIPT_20260921.md
-> docs/PAYOFF_B_INDUSTRIAL_MULE_DEER_ACTUATOR_RECEIPT_20260921.md
-> docs/PAYOFF_B_AIKENS_LAMBDA_PERTURBATION_PREREGISTRATION_20260921.md
-> docs/PAYOFF_B_AIKENS_IRG_RECONSTRUCTION_HANDOFF_20260921.md
-> docs/PAYOFF_B_EMPIRICAL_PHASE_PANEL_STATUS_20260921.md
-> docs/PAYOFF_B_TRACKING_EMPIRICAL_PARAMETERIZATION.md
-> docs/PAYOFF_B_MULE_DEER_PARAMETERIZATION_READINESS_20260920.md.
```

The estimand hierarchy is:

```text
moving environmental demand
-> migration / phenology tracking allocation
-> partner matching
-> coordinated value versus unilateral accessibility
-> demographic persistence
-> finite-N barrier crossing
-> explicit route/connectivity effects.
```

The canonical explicit-landscape results now include:

- a finite phenological buffering window followed by re-entry of spatial
  tracking;
- coordination barriers that convert local extinction into coordinated
  persistence;
- robustness to mutation-step refinement, boundary leakage, integer patch
  demography, 2D route geometry, and explicit distributional overlap;
- an interaction regime that synchronizes partner tracking at moderate forcing
  but becomes maladaptive synchronization under stronger forcing.

These are synthetic mechanism results and should not be read as calibrated
natural climate-speed or corridor-width thresholds.

The empirical parameterization handoff then separates directly recoverable
tracking quantities from still-unidentified fitness terms. Under the declared
nearest-neighbor family:

- mean-zero projected component second moments identify migration rate and x/y
  movement weights for the symmetric kernel;
- projected fixed-interval means plus second moments additionally identify x/y
  directional biases for the biased kernel;
- environmental wave speed and spatial gradient identify model climate
  velocity.

A first-order phase-residual inverse identifies the independent phenology rate
only when the timing axis is isolated from spatial movement and other tracking
pathways. Generic Days-From-Peak compression is otherwise retained as a
controller diagnostic, not silently relabeled as h.

Baseline growth, mismatch strengths, interaction strength and tracking costs
require independent matched fitness contrasts and are deliberately not imputed
from movement data.

The closed-loop tracking layer adds an exact local controller beneath the
explicit landscape. If q_m is movement-mediated feedback and q_h is
timing-mediated feedback, local mismatch obeys

    e_(t+1) = (1-q_m-q_h)e_t + r.

For cross-system empirical synthesis, define

    lambda = 1-q_m-q_h,

so that

    e_out = r + lambda e_in.

The canonical empirical comparison is lambda. The decomposition into speed,
stopover, route reset, timing, or other actuators belongs to a separate
system-specific prospective gate.

The confirmatory path is now:

    freeze phase-coordinate + segment scale
    -> register lambda prediction
    -> register system-specific actuator predictions
    -> observe held-out system
    -> evaluate lambda and actuator gates separately
    -> synthesize prospective lambda tests only.

Retrospective lambda analyses can be retained as descriptive evidence, but they
are counted separately from prospective support. The synthesis layer refuses
mixed phase coordinates or segment scales and exposes no actuator omnibus
score.

Before adding another evidence unit, run the inclusion gate. Raw-data
availability and a new forcing regime are context, not endpoints. A lambda test
must add a registered lambda prediction on the common coordinate/scale. An
actuator-only perturbation can enter separately without a lambda coordinate,
but it adds zero cross-system lambda support.

The industrial mule-deer perturbation first entered as source-backed
actuator-permeability evidence in a new forcing regime without adding a taxon
or a lambda test.

A prospective within-taxon lambda perturbation is now frozen separately:

    lambda_large-development
    >
    lambda_small-development

on the signed local peak-IRG phase coordinate and a fixed 24-hour segment.
The movement archive is already reconstructed. The offline environmental
pipeline now implements MODIS-like NDVI preprocessing, annual double-logistic
fitting, peak-IRG extraction, explicit GPS environmental joining, and fixed-24h
phase-pair construction. The downstream statistical layer is also frozen:
animal-year fixed effects, animal-clustered uncertainty, support gating, lambda
estimation, and preregistered contrast evaluation are implemented end to end.
The lambda outcome remains unopened because the required empirical MODIS NDVI
plus snow/quality source table has not yet been materialized.

Taxon count is therefore secondary to the number and diversity of independent
prospective lambda tests and mechanism-discriminating actuator tests.

Thus movement and timing feedback are exactly substitutable in the local linear
null through their total restoring gain K=q_m+q_h. Stability requires 0<K<2;
quadratic controller costs determine how the required gain is allocated between
the two channels. This is the analytic null against which route geometry,
finite timing capacity, and partner interaction break exact substitutability.

The explicit movement-feedback landscape then shows where the local
substitutability null breaks. Under strong forcing, mismatch-dependent movement
alone reduces error but remains non-persistent in the sampled high-forcing
slices. Adding an independent timing response crosses the persistence boundary
and sharply reduces the movement effort demanded by the controller. This is
retained as forcing-dependent complementarity, not as a universal rescue rule.

The Aikens 2022 controller receipt adds a different empirical layer before
full parameterization. It separates

    mismatch when a barrier is encountered

from

    downstream ability to reduce phase mismatch.

Across the eight published footprint x development conditions, restoring
route-distance controllers are detected in four conditions and no downstream
phase change is detected in four. This controller evidence is explicitly
movement/stopover mediated and is not relabeled as the independent timing-axis
phenology rate h.

The mule-deer readiness receipt then applies that refusal logic to a named
public system. The published Ortega et al. group summaries establish strong
en-route behavioral compensation, but they do not by themselves license the
current per-step kernel parameters. The interval pipeline now has a directional
movement inverse suitable for raw projected GPS moments, but the public summary
does not contain those fixed-interval means and second moments.

Early and mid group Days-From-Peak means cross the sign boundary; the late group
is monotone but spans a whole migration rather than one frozen decision
interval. Because the observed compensation is itself partly mediated by
movement speed and stopover behavior, none of those group summaries is inserted
as the independent timing-axis h. The repository therefore keeps the
named-system status at source-file ingestion pending instead of turning
published summaries into a pseudo-calibration.

---

## Boundary atlas

Before writing a manuscript result, consult

```text
theory/BOUNDARY_ATLAS.md.
```

It separates:

```text
static architecture boundary,
deterministic invasion boundary,
finite fixation boundary,
stationary occupancy boundary,
regular-graph boundary,
spatial migration boundary,
environment-mosaic spectral boundary,
periodic Floquet invasion boundary.
```

Do not call them all an "architecture threshold" without specifying the estimand.

---

## Claim boundaries

Use together:

```text
docs/CLAIM_BOUNDARY.md
docs/PRIOR_ART_BOUNDARY.md
docs/SPATIAL_PRIOR_ART_BOUNDARY.md
docs/ENVIRONMENT_MOSAIC_CLAIM_BOUNDARY.md
docs/TEMPORAL_PRIOR_ART_BOUNDARY.md.
```

The recurring novelty rule is:

```text
component population theory may be prior art;
PAYOFF's candidate contribution is the explicit estimand bridge
L -> R=sL -> phi=sL-K
into invasion, fixation, occupancy, spatial, and temporal predictions.
```

---

## One-line programme

```text
SCH asks where one-coordinate conflict settles.
BALANCE asks why the shared architecture can remain optimal despite conflict.
BITA asks when dimensional release pays and by what mechanism.
PAYOFF asks what population dynamics follow from those measured architecture payoffs under frequency dependence, drift, mutation, space, and time.
```
