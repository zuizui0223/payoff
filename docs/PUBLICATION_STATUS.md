# Publication status

PAYOFF-B is organized as a **two-paper publication programme**. The exact
anti-phase theorem remains independent. Paper 2 has advanced to the canonical
information-coordination V2 manuscript, which absorbs the earlier
temporal-buffering V1 generation as its capacity layer and retains V1 only as
provenance/rollback. See
`docs/PAYOFF_B_V1_V2_PUBLICATION_RELATION_20260927.md` and
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

## Paper 2: information coordination in seasonal tracking — PREOUTCOME

Canonical PREOUTCOME source:

`manuscript/PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md`

Authoritative V1/V2 publication relation:

`docs/PAYOFF_B_V1_V2_PUBLICATION_RELATION_20260927.md`

Primary ecological conclusion:

**Information use is an ecological coordination state. Interacting organisms can
begin using the same improving environmental information at different decision
thresholds, so better information can transiently worsen phenological
coordination; after coordinated information use collapses, even perfect
environmental information need not restore the informed state.**

Exact analytic spine:

```text
T1  cue information has an action threshold
-> T2  decision deadlines determine information uptake
-> T3  heterogeneous deadlines create a finite desynchronization window
-> T7  perfect information can support old and informed strict equilibria
-> T8  temporary cue degradation can collapse information use without recovery
```

T4–T6, T9 and the rescue/topology results remain important results and
mechanistic extensions, but they do not share equal weight in the abstract.

Natural evidence is deliberately modular:

- **broad birds:** preregistered pooled association between stronger
  pre-outcome predictive connectivity and smaller arrival–green-up mismatch;
  dependence-aware uncertainty prevents a universal species-level claim;
- **pied flycatcher experiment:** heterospecific phenology was unavailable to
  an earlier settlement decision but affected later settlement;
- **wigeon:** the registered predictive-connectivity × incoming-phase
  interaction is NOT_SUPPORTED, separating pre-commitment information from
  post-error correction;
- **long-term flycatcher cue–driver lane:** NO_CUE_DRIVER_REVERSAL under the
  preregistered gate; no natural information-recovery hysteresis is claimed.

The earlier temporal-buffering conclusion remains valid as the **capacity
layer**, not the primary novelty claim.

Current state:

```text
ACTIVE_PUBLICATION_QUEUE = true
ROLE = INTEGRATED_BROAD_ECOLOGY_PAPER
CANONICAL_SOURCE = PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md
V1_STATUS = FROZEN_PROVENANCE_ONLY
FIRST_SHOT = Global Ecology and Biogeography / Research Article
SCIENTIFIC_STATE = PREOUTCOME
OPEN_SCIENCE_GATE = registered Aikens lambda outcome
RETUNING_AFTER_AIKENS = forbidden
```

### V1/V2 rule

`manuscript/PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md` is frozen as
the temporal-buffering generation and rollback source. It is not submitted
separately while V2 is active.

The earlier source manuscripts and frozen Oikos/GEB artifacts remain
provenance sources only.

### Submission-package rule

Previous Paper 2 submission packages and audits built from V1 are retained for
provenance but are **not current journal-facing packages after the V2
promotion**.

The prior V1 GEB package remains provenance only. A fresh V2 PREOUTCOME package
has now been built and audited directly from the canonical V2 source. It is
ready for internal review but remains blocked from final journal upload.

```text
CURRENT_V2_PREOUTCOME_PACKAGE = READY
CURRENT_V2_PREOUTCOME_BUILD_RUN = 36313076476
CURRENT_V2_PREOUTCOME_ARTIFACT = 10930130067
CURRENT_V2_PREOUTCOME_ARCHIVE_SHA256 = cf1ada3fb67b603b972f6e3994f439292b3ed3b18f17d2f0c3407c0bc90288cd
CURRENT_V2_FINAL_SUBMISSION_PACKAGE = BLOCKED
OLD_V1_GEB_PACKAGE = PROVENANCE_ONLY
```

### Legacy V1 package provenance

The following identifiers are retained so the frozen V1 publication state
remains auditable. They do **not** describe the current V2 submission package.

```text
LEGACY_V1_PREOUTCOME_BUILD_RUN = 36118090547
LEGACY_V1_PREOUTCOME_ARTIFACT = 10856440257
LEGACY_V1_PREOUTCOME_ARCHIVE_SHA256 = b5628da1383960bdbbb637960d78d4f9c71588269f0ddee3111be37bba3fffc8
LEGACY_V1_POSTOUTCOME_GEB_PIPELINE = READY_FOR_V1_ONLY
LEGACY_V1_POSTOUTCOME_READINESS = GEB_INTEGRATED_POSTOUTCOME_PIPELINE_READINESS_20260925.md
LEGACY_V1_CREDENTIAL_PREFLIGHT_RUN = 36113621057
LEGACY_V1_CREDENTIAL_PREFLIGHT_ARTIFACT = 10853764396
CURRENT_V2_PREOUTCOME_PACKAGE = READY
CURRENT_V2_PREOUTCOME_BUILD_RUN = 36313076476
CURRENT_V2_PREOUTCOME_ARTIFACT = 10930130067
CURRENT_V2_PREOUTCOME_ARCHIVE_SHA256 = cf1ada3fb67b603b972f6e3994f439292b3ed3b18f17d2f0c3407c0bc90288cd
CURRENT_V2_POSTOUTCOME_GEB_PIPELINE = READY_UNOPENED
```

The legacy V1 PREOUTCOME package had zero identity leaks in its anonymous main
text. The credential-only preflight opened no environmental values and left the
Aikens lambda outcome unopened. These statements are retained as provenance,
not inherited automatically by V2.

The legacy V1 package also retained the **Aikens fixed-24 h adjudication** as its
registered final science gate. That adjudication record remains provenance for
V1 only.

The canonical V2 postoutcome route has now been rebuilt and tested independently.
All four registered result classes (PASS, wrong-direction, insufficient-support
and NOT_ESTIMABLE) generate a science-ready V2 package while leaving the blinded
main text and seven main figures unchanged. The registered result is rendered
into Supporting Information only.

```text
CURRENT_V2_POSTOUTCOME_GEB_PIPELINE = READY_UNOPENED
CURRENT_V2_POSTOUTCOME_MAIN_TEXT_RETUNING = forbidden
CURRENT_V2_POSTOUTCOME_MAIN_FIGURE_RETUNING = forbidden
CURRENT_V2_POSTOUTCOME_RESULT_LOCATION = Supporting Information only
LAST_VERIFIED_AIKENS_CREDENTIAL_PREFLIGHT = NOT_CONFIGURED_2026-09-25
CURRENT_CREDENTIAL_STATE = RECHECK_REQUIRED_BEFORE_REAL_EXECUTION
```

The credential line is deliberately a last-verified state, not a claim about
the current secret configuration. GitHub secret values are not readable from
the repository audit surface.

### Aikens gate

The preregistered Aikens fixed-24 h lambda outcome remains unopened.

The V2 manuscript must remain coherent under PASS, wrong-direction,
insufficient-support and NOT_ESTIMABLE outcomes. Its information-deadline and
coordination conclusions do not depend on the Aikens sign.

The V2 PREOUTCOME package is now built and audited. The remaining
pre-submission tasks are therefore:

1. re-run credential preflight and, if authentication is configured, execute
   and freeze the registered Aikens outcome through the canonical V2-only
   workflow;
2. supply an anonymous stable reviewer archive link;
3. complete author-controlled title-page and declaration metadata;
4. perform final human review of the already automated outcome-rendered package
   and portal metadata.


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

and the registered fixation-occupancy invariant. PAYOFF retains the deeper mathematical machinery as provenance and reusable modules. Its active independent publication queue now contains the anti-phase exact theorem and the integrated tracking-ecology paper; the remaining architecture, spatial and topology branches stay dormant modules unless they satisfy the reactivation rule below.

## Reactivation rule

A dormant PAYOFF branch returns to the publication queue only when it acquires either a genuinely independent theorem family or a distinctive empirical target that cannot be presented more cleanly as an SLK extension.
