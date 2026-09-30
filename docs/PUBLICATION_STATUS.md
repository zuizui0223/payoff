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

## Paper 2: information coordination in seasonal tracking — ACCESS_BLOCKED submission state

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
-> T3  heterogeneous effective deadlines create a finite desynchronization window
-> T7  perfect information can support old and informed strict equilibria
-> T8  temporary cue degradation can collapse information use without recovery
```

T4–T6, T9 and the rescue/topology results remain important results and
mechanistic extensions, but they do not share equal weight in the abstract.

### Effective deadline cost — core T2/T3 interpretation, not a separate abstract spine

The empirical deadline variable is now explicitly the **effective fitness cost
of waiting**, not raw elapsed time:

```text
D_eff(delta)
= J(delta)
  + min_c [ K(c) + M(delta-c) ]
```

where `J` is direct nonrecoverable waiting cost, `K` is compensation cost,
and `M` is the fitness loss from residual timing delay.

Consequences already verified in code:

- raw waiting duration, migration distance and departure date need not rank
  `D_eff` and can even rank information thresholds in the wrong order;
- greater downstream compensatory capacity can reduce the cue reliability
  required for waiting to be worthwhile;
- complete timing recovery does not imply zero waiting cost when `J>0`;
- the direct natural target is
  `D_eff,2-D_eff,1 -> q2-q1 -> asynchronous cue use`, not
  `raw delay -> q`.

A further exact **dual-use information** extension applies when the same focal
cue also changes the downstream compensation decision. Then `D_eff` is
cue-dependent and the fixed-cost threshold must not be used mechanically:

```text
wait
iff
V_action(q) + V_compensation(q) > J + R_compensation,prior
```

The exact direct-cost rescue interval is

```text
J in [ max(0, R_A0 - R_C0), R_A0 )
```

where action information alone can never justify waiting but the same cue can
become worth waiting for because it also informs compensation.

This result is a closed-form ecological specialization of established
sequential value-of-information/recourse logic. Generic VOI, stopovers as
information sources and en-route compensation are not claimed as novel.
See `docs/PAYOFF_B_DUAL_USE_INFORMATION_NOVELTY_BOUNDARY_20260930.md`.

The fixed-`D_eff` definition and its ordering consequence are now part of the core T2–T3 interpretation and are stated in the abstract: **raw waiting time need not rank effective deadlines and can mis-rank information-use thresholds**. Hidden-state and dual-use refinements remain theory extensions and empirical-validation guards. None of these replace T1–T3/T7–T8 as the main manuscript spine.

GEB-facing science state after the 2026-10-01 information-deadline reframe:

```text
CANONICAL_TITLE = Information deadlines can desynchronize seasonal interactions under environmental change
CURRENT_SCIENCE_HEAD = d3b58c3d1fa036a59d4abe6b7d167d3f4a31f15d
STRUCTURED_ABSTRACT = YES
ABSTRACT_WORDS_LAST_VERIFIED = 283
MAIN_BODY_WORDS_CURRENT_CANONICAL_APPROX = 4904
REFERENCES_CURRENT = 25
CURRENT_GEB_TYPICAL_MAIN_BODY_GUIDE = ~5000 words
CURRENT_GEB_ABSTRACT_LIMIT = 300 words
PACKAGE_METRICS = REFRESH_PENDING
```

Natural evidence is deliberately modular:

- **broad birds:** preregistered pooled association between stronger
  pre-outcome predictive connectivity and smaller arrival–green-up mismatch;
  dependence-aware uncertainty prevents a universal species-level claim;
- **E6 information-distance triangulation:** a dependence-aware reconstruction
  of 944 temperature-response effects from 28 studies and 279 bird species
  gives long-minus-short migration distance = +0.421 d/°C (95% CI +0.121 to
  +0.722, p=0.0077), with 28/28 leave-one-study-out fits positive; an
  independent 1,763-species plant–pollinator benchmark reproduces all five
  published group means. This supports an information-distance axis but is
  not a causal bird-versus-pollinator ranking or a new cross-taxon meta-analysis;
- **pied flycatcher experiment:** heterospecific phenology was unavailable to
  an earlier settlement decision but affected later settlement;
- **wigeon:** the registered predictive-connectivity × incoming-phase
  interaction is NOT_SUPPORTED, separating pre-commitment information from
  post-error correction;
- **long-term flycatcher cue–driver lane:** NO_CUE_DRIVER_REVERSAL under the
  preregistered gate;
- **prospective Hoge Veluwe cue–resource lane:** NO_CUE_RESOURCE_REVERSAL;
  the environmental prerequisite failed before resident–migrant timing history
  was opened, so Gate C was NOT_RUN and no natural information-recovery
  hysteresis is claimed;
- **greater snow goose deadline-validation lane:** same-lineage evidence now
  anchors route predictability, perturbation carry-over cost, two-sided timing
  fitness and multi-stage buffering. A GPS departure cue-uptake lane and a
  downstream dual-use compensation screen are preregistered, but no focal GPS
  outcome has been opened. Natural `D_eff`, actor-level `q_wait`, and the
  pairwise asynchronous window remain unidentified.
- **American redstart compensation-with-cost bridge:** published tracking shows
  that birds departing about 10 days late migrated 43% faster while the
  compensatory pattern was associated with a reported 6.3% survival decrease.
  This is used only to show that temporal compensation can coexist with fitness
  cost; it does not identify natural `D_eff`, cue use or `q_wait`.

The earlier temporal-buffering conclusion remains valid as the **capacity
layer**, not the primary novelty claim.

Current state:

```text
ACTIVE_PUBLICATION_QUEUE = true
ROLE = INTEGRATED_BROAD_ECOLOGY_PAPER
CANONICAL_SOURCE = PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md
V1_STATUS = FROZEN_PROVENANCE_ONLY
FIRST_SHOT = Global Ecology and Biogeography / Research Article
SCIENTIFIC_STATE = ACCESS_BLOCKED_SUBMISSION_STATE_FROZEN
AIKENS_EXECUTION_STATE = ACCESS_BLOCKED_FROZEN_NONSCIENTIFIC
AIKENS_SCIENTIFIC_RESULT = unavailable
AIKENS_LAMBDA_OUTCOME_OPENED = false
ACCESS_BLOCKED_AUTHOR_DECISION = FROZEN_SUBMIT_WITH_ACCESS_BLOCKED
FUTURE_AUTHENTICATED_EXECUTION = permitted under original preregistration
RETUNING_AFTER_AIKENS = forbidden
E6_CAUSAL_INFORMATION_DISTANCE = NOT_IDENTIFIED
E6_PHOTOPERIOD_ENDOGENOUS_ALTERNATIVE = EXPLICIT
DEADLINE_EMPIRICAL_TARGET = D_EFF_NOT_RAW_DELAY
DUAL_USE_INFORMATION_THEOREM = EXACT_VERIFIED
FIXED_D_EFF_EXOGENEITY_SCREEN = PREREGISTERED_UNOPENED
GREATER_SNOW_GOOSE_SINGLE_ACTOR_DEADLINE_LANE = PREREGISTERED_UNOPENED
GREATER_SNOW_GOOSE_D_EFF = NOT_IDENTIFIED
GREATER_SNOW_GOOSE_Q_WAIT = NOT_IDENTIFIED
GREATER_SNOW_GOOSE_J_ROW_LANE = SOURCE_ACCESS_BLOCKED_ROW_UNOPENED
GREATER_SNOW_GOOSE_PUBLISHED_J_AUDIT = MULTICOMPONENT_DIRECT_COST_PATTERN
DUAL_USE_COMPLEXITY_SCALING = EXACT_VERIFIED
DUAL_USE_NOVELTY_BOUNDARY = VOI_COORDINATION_STOPPING_PRIOR_ART_EXPLICIT
PAIRWISE_DEADLINE_DIFFERENCE_NATURAL_TEST = NOT_YET_DIRECTLY_TESTED
PAIRWISE_RESPONSE_ASYMMETRY_BRIDGE = SUPPORTED_PUBLISHED
INTERACTION_RESPONSE_BRIDGE_V2 = TWO_INDEPENDENT_CONTEXTS
FIGURE_5_E6_INFORMATION_DISTANCE = INTEGRATED
ABSTRACT_EMPIRICAL_LAYERS = E1 -> E6 -> INTERACTION_0.94_D_PER_DECADE
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
CURRENT_V2_SCIENCE_HEAD = d3b58c3d1fa036a59d4abe6b7d167d3f4a31f15d
CURRENT_V2_PREOUTCOME_PACKAGE = REFRESH_PENDING_AFTER_SCIENCE_UPDATE
CURRENT_V2_PREOUTCOME_REFRESH_RUN = 36789640775
LAST_VERIFIED_V2_PREOUTCOME_BUILD_RUN = 36743782397
LAST_VERIFIED_V2_PREOUTCOME_ARTIFACT = 11112176156
LAST_VERIFIED_V2_PREOUTCOME_ARCHIVE_SHA256 = bc16f4b6e66af0e1936636b3f9fcb801b071ec5a8335ff1363565eef6504eea9
LAST_VERIFIED_V2_PREOUTCOME_HEAD = 41138e7856b4619c8e741da8b54fdef65ba2a2c7
CURRENT_V2_FINAL_SUBMISSION_PACKAGE = REFRESH_PENDING_SCIENCE_CLOSED_PORTAL_BLOCKED
OLD_V1_GEB_PACKAGE = PROVENANCE_ONLY
```

The anonymous reviewer archive is also built and audited from the canonical V2
source:

```text
CURRENT_V2_REVIEWER_ARCHIVE = REFRESH_PENDING_AFTER_SCIENCE_UPDATE
CURRENT_V2_REVIEWER_ARCHIVE_REFRESH_RUN = 36789641016
LAST_VERIFIED_V2_REVIEWER_ARCHIVE_RUN = 36743782496
LAST_VERIFIED_V2_REVIEWER_ARCHIVE_ARTIFACT = 11111193281
LAST_VERIFIED_V2_REVIEWER_ARCHIVE_INNER_SHA256 = 46465a0bfa2f3851ca3cddc5252d8e0436fa8a0d87686034768423540fa32d52
LAST_VERIFIED_V2_REVIEWER_ARCHIVE_HEAD = 41138e7856b4619c8e741da8b54fdef65ba2a2c7
LAST_VERIFIED_V2_REVIEWER_ARCHIVE_IDENTITY_SCAN = PASS
CURRENT_V2_REVIEWER_ARCHIVE_RAW_DATA_REDISTRIBUTED = false
CURRENT_V2_REVIEWER_ARCHIVE_DELIVERY = WAIT_FOR_REFRESH_THEN_ANONYMOUS_CHANNEL
```

The archive contains 76 files, including 27 Python source files and seven main
figures. It can be regenerated deterministically and can switch to
outcome-rendered Supporting Information after the registered Aikens result is
frozen without changing the blinded main text or main figures.

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
CURRENT_V2_PREOUTCOME_PACKAGE = REFRESH_PENDING_AFTER_SCIENCE_UPDATE
CURRENT_V2_PREOUTCOME_REFRESH_RUN = 36789640775
LAST_VERIFIED_V2_PREOUTCOME_BUILD_RUN = 36743782397
LAST_VERIFIED_V2_PREOUTCOME_ARTIFACT = 11112176156
LAST_VERIFIED_V2_PREOUTCOME_ARCHIVE_SHA256 = bc16f4b6e66af0e1936636b3f9fcb801b071ec5a8335ff1363565eef6504eea9
LAST_VERIFIED_V2_PREOUTCOME_HEAD = 41138e7856b4619c8e741da8b54fdef65ba2a2c7
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
Four scientific result classes (PASS, wrong-direction, insufficient-support and
NOT_ESTIMABLE) remain available for any future authenticated execution. The
separate `ACCESS_BLOCKED` external-access state is now explicitly frozen for
the current submission route. It is not a scientific result: no environmental
values or lambda outcome were opened, and no substitute source or analysis was
used. The original preregistration remains binding if authenticated execution
becomes possible later. All rendered Aikens states remain in Supporting
Information only.

```text
CURRENT_V2_POSTOUTCOME_GEB_PIPELINE = ACCESS_BLOCKED_STATE_FROZEN
CURRENT_V2_POSTOUTCOME_MAIN_TEXT_RETUNING = forbidden
CURRENT_V2_POSTOUTCOME_MAIN_FIGURE_RETUNING = forbidden
CURRENT_V2_POSTOUTCOME_RESULT_LOCATION = Supporting Information only
CURRENT_V2_ACCESS_BLOCKED_PACKAGE = REFRESH_PENDING_AFTER_SCIENCE_UPDATE
CURRENT_V2_ACCESS_BLOCKED_REFRESH_RUN = 36789640754
LAST_VERIFIED_V2_ACCESS_BLOCKED_BUILD_RUN = 36743782371
LAST_VERIFIED_V2_ACCESS_BLOCKED_ARTIFACT = 11111033416
LAST_VERIFIED_V2_ACCESS_BLOCKED_GEB_SHA256 = 31838962865f698d944293f4b30765c4a7d0a903c7aeaad9f10a30f6150656f9
LAST_VERIFIED_V2_ACCESS_BLOCKED_REVIEW_SHA256 = 91217d5fd55cfe4116164ad379d40f5be4e6a0319cfcf0a7be78ac98290f8a43
LAST_VERIFIED_V2_ACCESS_BLOCKED_HEAD = 41138e7856b4619c8e741da8b54fdef65ba2a2c7
LAST_VERIFIED_AIKENS_CREDENTIAL_PREFLIGHT = NOT_CONFIGURED_2026-09-28
LAST_VERIFIED_AIKENS_CREDENTIAL_PREFLIGHT_RUN = 36372973062
LAST_VERIFIED_AIKENS_CREDENTIAL_PREFLIGHT_ARTIFACT = 10950280495
CURRENT_CREDENTIAL_STATE = NOT_CONFIGURED_CONFIRMED_2026-09-28
```

The credential state above was freshly rechecked on 2026-09-28 without
recording secret values or opening environmental data. No usable AppEEARS token
or Earthdata username/password pair was configured in that run.

### Aikens gate

The preregistered Aikens fixed-24 h lambda outcome remains unopened. For the
current submission route, the external-access state is frozen as
`ACCESS_BLOCKED`. This does not count as a scientific null, a
`NOT_ESTIMABLE` result, or evidence for or against the registered prediction.

The V2 manuscript remains valid under PASS, wrong-direction,
insufficient-support and NOT_ESTIMABLE scientific outcomes if authenticated
execution occurs later. The original preregistration remains binding, and its
information-deadline and coordination conclusions do not depend on the Aikens
sign.

The deterministic ACCESS_BLOCKED GEB package and outcome-rendered reviewer
archive are built and reproduced. The remaining pre-submission tasks are:

1. deliver the already-built ACCESS_BLOCKED reviewer archive through the
   journal portal or a stable anonymous link;
2. complete author-controlled title-page and declaration metadata;
3. perform final human review of the generated package and portal metadata.

Authenticated Aikens execution is now a permitted future extension under the
original registration, not a blocker for this frozen submission state.


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
