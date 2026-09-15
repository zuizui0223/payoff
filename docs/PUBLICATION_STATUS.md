# Publication status

PAYOFF is split into one active short paper and several citable technical modules.

## Active paper: PAYOFF-B Brief Communication

Target:

**Theoretical Ecology — Brief Communication**

Canonical manuscript:

`manuscript/PAYOFF_B_THEORETICAL_ECOLOGY_BRIEF_V1.md`

Core claim:

**In the symmetric two-patch, two-season anti-phase model, the temporal growth premium has exactly one positive migration optimum for every nonzero environmental contrast.**

The dimensionless optimum

```text
u* = m* tau
```

lies on a one-parameter scaling curve in

```text
v = |x| tau,
```

with endpoint limits

```text
v -> 0:        u* -> 1.60611529880277...
v -> infinity: u* = 1 + 1/v + O(v^-2) -> 1.
```

### Prior-art boundary

The closed-form periodic/Floquet growth exponent for the closely corresponding anti-phase switched two-patch system is **not claimed as new**. Benaim et al. (2023) already give an explicit growth formula in this model class. PAYOFF-B owns only the narrower result built on that solvable case:

- the global uniqueness proof for the positive migration optimum for every `v>0`;
- the dimensionless scaling curve `u*(v)`;
- the weak-contrast constant `1.6061152988...` and maximum-premium coefficient `0.13248753945...`;
- the strong-contrast limit `u*(v) -> 1` and associated asymptotic expansion.

The paper does **not** claim that arbitrary periodic, asymmetric, stochastic, or multi-patch systems have a unique dispersal optimum.

### Submission state

The journal-facing package contains:

- a compact Brief Communication manuscript;
- two publication figures;
- an analytic proof source in `theory/EXACT_ANTI_PHASE_OPTIMUM.md`;
- executable numerical verification against the general two-season Floquet implementation;
- reproducible DOCX/PDF/page-PNG review-package CI.

The numerical receipt is an implementation audit, not a substitute for the analytic proof.

```text
ACTIVE_PUBLICATION_QUEUE = true
ROLE = ACTIVE_SHORT_PAPER
INTERNAL_SCIENTIFIC_BLOCKER = none
EXTERNAL_ACTIONS = author metadata + journal upload
```

The Brief should not carry the full PAYOFF hierarchy. In particular, do not make continuous architecture, general topology, generic spatial spectral theory, or rare-mutation occupancy co-equal storylines.

## DOI modules / dormant branches

### PAYOFF-A: continuous architecture

Retain continuous recovery, interior optima, branching threshold, endpoint-coexistence closure, and accessibility barriers.

```text
ACTIVE_PUBLICATION_QUEUE = false
ROLE = DOI_MODULE / DORMANT_PAPER_BRANCH
```

### Spatial spectral transport

Retain principal-eigenvalue transport, source-sink rescue, migration thresholds, and general metapopulation diagnostics.

```text
ACTIVE_PUBLICATION_QUEUE = false
ROLE = DOI_MODULE / DORMANT_PAPER_BRANCH
```

### Topology / edgewise modularization

Retain edgewise recovery derivatives, vertex solutions under additive linear decoupling cost, topology-state games, and path-accessibility barriers.

```text
ACTIVE_PUBLICATION_QUEUE = false
ROLE = DOI_MODULE / DORMANT_PAPER_BRANCH
```

## Relation to SLK

SLK owns the flagship transport spine

```text
L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy
```

and the registered fixation-occupancy invariant. PAYOFF retains the deeper mathematical machinery as provenance and reusable modules, but only the anti-phase exact optimum theorem is currently promoted as an independent paper.

## Reactivation rule

A dormant PAYOFF branch returns to the publication queue only when it acquires either a genuinely independent theorem family or a distinctive empirical target that cannot be presented more cleanly as an SLK extension.
