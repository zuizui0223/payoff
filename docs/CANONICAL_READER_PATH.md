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

Use only when relative patch quality changes through time.

The noncommutativity gate is

```text
[A_a,A_b]
propto
m[(r_1a-r_2a)-(r_1b-r_2b)].
```

Then compute the exact principal Floquet exponent rather than replacing the environment by its time average.

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
environment-mosaic spectral boundary.
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
