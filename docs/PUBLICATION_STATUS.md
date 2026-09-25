# Publication status

PAYOFF-B is organized as a **two-paper publication programme**. The exact
anti-phase theorem remains independent, while the frozen tracking theory and
movement–phenology empirical programme are combined into one broad ecology
manuscript. See
`docs/PAYOFF_B_TWO_PAPER_PUBLICATION_ARCHITECTURE_20260925.md`.

## Paper 1: PAYOFF-B exact theorem


Target:

**Theoretical Ecology**

Portal routing:

```text
PREFERRED = Brief Communication, if the live portal offers that article type
FALLBACK = Original Paper, if Brief Communication is not offered
```

The current public submission guidance does not list Brief Communication as a separate article type, although the journal has historically published Brief Communications. The scientific paper should therefore not be blocked on that label: the same concise theorem manuscript is submitted as Original Paper if that is the live portal's available route.

Canonical science manuscript:

`manuscript/PAYOFF_B_THEORETICAL_ECOLOGY_BRIEF_V1.md`

Journal-facing submission overlay:

`scripts/build_payoff_b_submission_source.py`

Portal handoff contract:

`submission/THEORETICAL_ECOLOGY_PORTAL_HANDOFF_V1.md`

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

The journal-facing package now validates against the current portal-facing preparation constraints through a deterministic overlay while leaving the science source frozen. It contains:

- a compact theorem manuscript;
- two publication figures;
- title-page metadata placeholders;
- Statements and Declarations placeholders;
- a cover letter with five reviewer slots;
- an analytic proof source in `theory/EXACT_ANTI_PHASE_OPTIMUM.md`;
- executable numerical verification against the general two-season Floquet implementation;
- reproducible DOCX/PDF/page-PNG review-package CI.

The latest verified submission overlay has:

```text
ABSTRACT_WORDS = 154
KEYWORDS = 6
REVIEW_PAGES = 10
EMBEDDED_FIGURES = 2
INTERNAL_TARGET_LINE = REMOVED
DECLARATIONS = PRESENT
```

The numerical receipt is an implementation audit, not a substitute for the analytic proof.

```text
ACTIVE_PUBLICATION_QUEUE = true
ROLE = ACTIVE_SHORT_PAPER
INTERNAL_SCIENTIFIC_BLOCKER = none
EXTERNAL_ACTIONS = author metadata + funding/COI/contributions + AI disclosure approval + five reviewers + journal upload
```

The paper should not carry the full PAYOFF hierarchy. In particular, do not make continuous architecture, general topology, generic spatial spectral theory, or rare-mutation occupancy co-equal storylines.

## Paper 2: integrated tracking ecology — PREOUTCOME

Canonical PREOUTCOME source:

`manuscript/PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md`

Headline inference:

**Mismatch is an outcome, not a tracking architecture. Low mismatch can conceal a changing burden distributed across movement, timing, environmental information and actuation.**

The integrated sequence is:

```text
simple seasonal-timescale benchmark
-> local movement/timing non-identifiability
-> finite-capacity / fragmentation / coordination breakdown
-> 55-species rejection of one universal natural speed optimum
-> direct phase-control decomposition in mule deer, barnacle goose and wigeon
-> preregistered within-taxon Aikens actuation-to-retention test
```

Current state:

```text
ACTIVE_PUBLICATION_QUEUE = true
ROLE = INTEGRATED_BROAD_ECOLOGY_PAPER
SCIENTIFIC_STATE = PREOUTCOME_INTERNAL_READY
OPEN_SCIENCE_GATE = registered Aikens lambda outcome
RETUNING_AFTER_AIKENS = forbidden
```

The existing frozen sources remain intact as provenance and rollback sources:

- `manuscript/PAYOFF_B_TRACKING_THEORY_V1.md`;
- `manuscript/PAYOFF_B_MOVEMENT_PHENOLOGY_GEB_V3_PREOUTCOME.md`.

Those two sources are retained as provenance / rollback sources and are not
submitted as separate overlapping papers while the integrated architecture is
active. The frozen Oikos package remains a rollback artifact.

The integrated PREOUTCOME package has passed:

- full repository CI;
- six-figure deterministic rendering;
- broad-bird machine-provenance checks;
- reference completeness;
- anonymous-text scan;
- six-main-figure contract;
- universal-lambda claim ceiling;
- Aikens outcome-blind marker checks.

Current audited metrics are: abstract 231 words, main text 3,458 words,
21 references with zero uncited entries, 8 keywords, and 6 main figures.
The only remaining scientific blocker before outcome-rendered submission
preparation is the registered Aikens fixed-24 h lambda adjudication.


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
