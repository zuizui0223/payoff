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

### Post-freeze Paper-2 development line

The frozen journal-facing V2 remains the submission/audit source above. It is
**not** silently replaced by later theory.

A post-freeze integrated development manuscript now exists at:

`manuscript/PAYOFF_B_INFORMATION_CONTROL_V3_POSTFREEZE.md`

Merged development lineage:

```text
PR 255  stagewise information + signed recourse
PR 257  continuous information-actionability balance
PR 258  route-wise Bayesian phase control + V3 integration
PR 260  phase-variance funnel + phase-sense inverse
```


The actor-to-interaction bridge is now exact in the declared linear mean
controller.  For two actors,

\[
\Delta_{t+1}
=
(\lambda_1-\lambda_2)m_t
+
\frac{\lambda_1+\lambda_2}{2}\Delta_t
+
\delta w_t.
\]

If the pair is currently synchronized and receives the same innovation,

\[
\Delta_{t+1}
=
(\lambda_1-\lambda_2)m_t.
\]

Under constant shared forcing \(w\) and stable controllers,

\[
\Delta^*
=
w\,
\frac{\lambda_1-\lambda_2}
{(1-\lambda_1)(1-\lambda_2)}.
\]

This closes the post-freeze mechanistic chain from information/control
heterogeneity to interaction mismatch.  Direct natural pairwise
parameterization remains prospective.

\`\`\`text
TWO_CLOCK_ARCHITECTURE = DEVELOPMENTAL_PLUS_DECISION
MIKAWA_ANJO_CLOCK = DECISION_CONTROLLER_ONLY
TWO_CLOCK_IDENTIFICATION = K_AND_H_IDENTIFIED_PRIMITIVE_G_O_g_REQUIRE_EXTRA_DATA
TWO_CLOCK_COMPLEMENTARITY = MULTIPLICATIVE_G_TIMES_O_TIMES_g_TIMES_K
READINESS_GATE_G = OPENS
OPPORTUNITY_GATE_O = CLOSES
BEE_EMERGENCE_LABEL = DEVELOPMENTAL_PHYSIOLOGICAL_TIMER_NOT_UNIVERSAL_MOLECULAR_CLOCK
CONTROLLER_ASYMMETRY_MISMATCH = EXACT_POSTFREEZE
DIRECT_PAIRWISE_NATURAL_TEST = PROSPECTIVE
TWO_CLOCK_EVIDENCE_MATRIX = docs/PAYOFF_B_TWO_CLOCK_EVIDENCE_MATRIX_20261003.md
TWO_CLOCK_FULL_DECOMPOSITION = PROSPECTIVE
NETWORK_CONTROLLER_DISCORDANCE = EXACT_POSTFREEZE
BINARY_NETWORK_CUT_RECOVERED = YES
DIRECT_NETWORK_CONTROLLER_TEST = PROSPECTIVE
\`\`\`

The post-freeze ecological spine is:

```text
partly latent future seasonal state
-> checkpoint information acquisition
-> signed phase-error estimation
-> speed / stopover / route correction
-> residual error propagated to the next checkpoint
-> actionability declines while information can improve
-> interacting actors can follow different phase trajectories
-> physical or strategic recovery failure
```

Exact route-wise state representation:

```text
e_(t+1) = phi_t [e_t - u_t] + w_t
```

and, under perfect estimation, proportional feedback, no clipping and zero
target shift,

```text
lambda_t = phi_t (1 - g_t).
```

This is an identification bridge, not permission to relabel empirical
`lambda` as actionability `r` or feedback gain `g`.


The post-freeze population-variance extension gives

\[
P_{t+1}
=
\phi_t^2P_t[1-K_tg_t(2-g_t)]+Q_t,
\]

where \(K_t\) is the effective checkpoint-information weight and \(Q_t\) is
new process innovation. A common open-loop timing correction has no
state-dependent contraction term:

\[
P_{t+1}^{open}
=
\phi_t^2P_t+Q_t.
\]

Thus individualized feedback has a prospective **phase-variance funnel**
signature beyond a shared timing programme.

Under noisy individualized phase estimation, regression-scale mean retention is

\[
\lambda_t
=
\phi_t(1-g_tK_t),
\]

with \(\lambda_t=\phi_t(1-g_t)\) only as the perfect-information special case.
Define

\[
d_t=1-\frac{\lambda_t}{\phi_t}
\]

and

\[
v_t=
\frac{P_{t+1}-Q_t}
{\phi_t^2P_t}.
\]

When \(d_t\neq0\), the declared Gaussian controller gives

\[
K_t=
\frac{d_t^2}
{v_t-1+2d_t},
\qquad
g_t=
\frac{d_t}{K_t}.
\]

This phase-sense inverse is exact only under the declared Gaussian controller
and requires independent passive-retention and process-innovation references.
It must not be back-solved from the same transition used to define
\(\phi_t\) or \(Q_t\).

Mule-deer prior art is explicit. Ortega et al. (2023) already document large
initial phenological mismatch, bidirectional speed/stopover compensation and
resynchronization toward summer-range arrival, and explicitly discuss a
temporal cognitive/phase-sense interpretation. PAYOFF-B does not claim
discovery of that phenomenon.

The public Ortega Source Data workbook
\`41467_2023_37750_MOESM4_ESM.xlsx\` was downloaded and parsed in GitHub Actions
(HTTP 200; SHA256
\`2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364\`).
Its paired animal-year phase sheet contains 152 rows with \`DFP_Start\` and
\`DFP_End\`, and its actuator sheet contains matched movement-rate and stopover
summaries.

A schema-frozen post-freeze descriptive audit gives:

\`\`\`text
MULE_DEER_ANIMAL_YEARS = 152
MULE_DEER_INDIVIDUALS = 72
START_PHASE_SD_DAYS = 26.406
END_PHASE_SD_DAYS = 13.173
END_START_VARIANCE_RATIO = 0.2489
ANIMAL_CLUSTER_BOOTSTRAP_95 = [0.1667, 0.3617]
WITHIN_YEAR_VARIANCE_RATIO = 0.2940
WHOLE_ROUTE_LAMBDA = 0.10734
MOVEMENT_RATE_VS_START_PHASE = +0.06834 km d^-1 per phase day
STOPOVER_VS_START_PHASE = -0.4919 d per phase day
\`\`\`

These values quantify the published resynchronization and signed compensation
in continuous animal-year data. They do not identify latent \(K\), \(g\),
\(\phi\), \(r\) or \(D_{eff}\), and they do not alter the frozen V2 submission
or any preregistered result.

The post-freeze actionability theorem additionally gives

```text
N(t) = r(t)[S q(t)-B] - C(t)
```

and the declared exponential reduced model has

```text
t* = log(1 + alpha/beta) / alpha.
```

Generic dynamic programming, optimal migration, partial-information optimal
control, Bayesian filtering and feedback control are prior art. The novelty
boundary is recorded in
`docs/PAYOFF_B_ROUTEWISE_INFORMATION_CONTROL_NOVELTY_BOUNDARY_20261003.md`.

The evidence/claim boundary is recorded in
`docs/PAYOFF_B_V3_POSTFREEZE_CLAIM_AUDIT_20261003.md`.

The direct natural route-wise controller remains prospective: no existing
dataset is claimed to identify checkpoint cue quality, internal phase estimate,
feedback gain, passive retention and remaining actionability simultaneously.

```text
V2_SUBMISSION_STATUS = FROZEN_ACCESS_BLOCKED
V3_POSTFREEZE_STATUS = DEVELOPMENT_INTEGRATED
V3_SUBMISSION_STATUS = NOT_FROZEN_NOT_JOURNAL_FACING
V3_CORE_METAPHOR = SHINKANSEN_TO_SCHROEDINGERS_SPRING
V3_FORMAL_OBJECT = SEQUENTIAL_INFORMATION_AND_PHASE_CONTROL
V3_VARIANCE_FUNNEL = EXACT_REDUCED_MODEL
V3_PHASE_SENSE_INVERSE = NOISY_CUE_EXACT_CONDITIONAL_ON_INDEPENDENT_PHI_Q
MULE_DEER_PHASE_SENSE = PRIOR_ART_NOT_PAYOFF_NOVELTY
ORTEGA_VARIANCE_FUNNEL = POSTFREEZE_DESCRIPTIVE_SOURCE_DATA_AUDIT
ORTEGA_SOURCE_XLSX = PUBLIC_HTTP200_PARSED_SHA256_FROZEN
```

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
CURRENT_PACKAGE_HEAD = fb03cec738558b2fd8800a60c5d80c3ae609c237
STRUCTURED_ABSTRACT = YES
ABSTRACT_WORDS = 283
MAIN_BODY_WORDS = 4902
REFERENCES = 25
DISPLAY_PIECES = 7
CURRENT_GEB_TYPICAL_MAIN_BODY_GUIDE = ~5000 words
CURRENT_GEB_ABSTRACT_LIMIT = 300 words
PACKAGE_METRICS = PASS
FULL_TEST_RUN = 36807276341
EMPIRICAL_TEST_ENV_RUN = 36807276255
EMPIRICAL_LAMBDA_GATE = PASS_20_OF_20_NO_SKIPS
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
has now been built and audited directly from the canonical V2 source. It has passed the journal-facing audit and is current for the frozen submission route.

```text
CURRENT_V2_SCIENCE_HEAD = d3b58c3d1fa036a59d4abe6b7d167d3f4a31f15d
CURRENT_V2_PACKAGE_HEAD = fb03cec738558b2fd8800a60c5d80c3ae609c237
CURRENT_V2_PREOUTCOME_PACKAGE = READY
CURRENT_V2_PREOUTCOME_BUILD_RUN = 36807276298
CURRENT_V2_PREOUTCOME_ARTIFACT = 11138366353
CURRENT_V2_PREOUTCOME_ACTIONS_ARTIFACT_SHA256 = 5ad4ca0b5be5c9b888d71385d2a7e05f079a09026b45f50c55cfbf1fc5d4e3c3
CURRENT_V2_PREOUTCOME_ARCHIVE_SHA256 = 048e234b69363800d17de98401d288d78913bc994d130024ad9310d1db6557a1
CURRENT_V2_PREOUTCOME_VALIDATED_HEAD = fb03cec738558b2fd8800a60c5d80c3ae609c237
CURRENT_V2_FINAL_SUBMISSION_PACKAGE = ACCESS_BLOCKED_SCIENCE_CLOSED_PORTAL_READY_FOR_AUTHOR_METADATA
OLD_V1_GEB_PACKAGE = PROVENANCE_ONLY
```

The anonymous reviewer archive is also built and audited from the canonical V2
source:

```text
CURRENT_V2_REVIEWER_ARCHIVE = READY_PREOUTCOME
CURRENT_V2_REVIEWER_ARCHIVE_RUN = 36807276290
CURRENT_V2_REVIEWER_ARCHIVE_ARTIFACT = 11137374088
CURRENT_V2_REVIEWER_ARCHIVE_ACTIONS_ARTIFACT_SHA256 = 4b27f0502913bf3dd665303cc8b3b3821852912c15ffba09b5917f61b3af6c66
CURRENT_V2_REVIEWER_ARCHIVE_INNER_SHA256 = 95b815a62b024b3a0a3210552bc1e61f0eb3523dc6702bc567037553b797b294
CURRENT_V2_REVIEWER_ARCHIVE_VALIDATED_HEAD = fb03cec738558b2fd8800a60c5d80c3ae609c237
CURRENT_V2_REVIEWER_ARCHIVE_IDENTITY_SCAN = PASS
CURRENT_V2_REVIEWER_ARCHIVE_RAW_DATA_REDISTRIBUTED = false
CURRENT_V2_REVIEWER_ARCHIVE_FILE_COUNT = 78
CURRENT_V2_REVIEWER_ARCHIVE_PYTHON_SOURCE_COUNT = 28
CURRENT_V2_REVIEWER_ARCHIVE_FIGURE_COUNT = 7
CURRENT_V2_REVIEWER_ARCHIVE_DELIVERY = PENDING_ANONYMOUS_CHANNEL
```

Portal-facing editable files are also built from the same frozen science state:

```text
CURRENT_V2_PORTAL_FILES = READY_FOR_AUTHOR_METADATA
CURRENT_V2_PORTAL_FILES_RUN = 36807276327
CURRENT_V2_PORTAL_FILES_ARTIFACT = 11138137692
CURRENT_V2_PORTAL_FILES_ACTIONS_ARTIFACT_SHA256 = b76da056019b77827722f5cd0295cfced7cb711837f16364a72442ef62bce428
CURRENT_V2_PORTAL_FILES_VALIDATED_HEAD = fb03cec738558b2fd8800a60c5d80c3ae609c237
CURRENT_V2_PORTAL_MAIN_DOCX_SHA256 = 84fe857e8f03d6306f3d6cc0292aa09c7effbc54621648e138e1d98e502a0fb5
CURRENT_V2_PORTAL_MAIN_PDF_SHA256 = b461d5cd4df7e9be76af75e15dc363b2d13a8eb5925d0da02820f42b216204c6
CURRENT_V2_PORTAL_SI_DOCX_SHA256 = b3648cfd8877501212cab7c10e68a505efc4932b7f78322b210051b709a8d97c
CURRENT_V2_PORTAL_TITLE_DOCX_SHA256 = 0dde8cd6751f038095f93ab463ef61d16f3b004923d92f52d5a0c38dc7396a4b
CURRENT_V2_PORTAL_COVER_PDF_SHA256 = 0cfdb5d79a30b0c1ed90e1323db64b55b8c6fcf1b83454a4292ee35962d4b8da
CURRENT_V2_PORTAL_MAIN_PAGES = 28
CURRENT_V2_PORTAL_COVER_PAGES = 1
CURRENT_V2_PORTAL_TITLE_PAGES = 2
CURRENT_V2_PORTAL_SI_PAGES = 4
CURRENT_V2_PORTAL_EMBEDDED_FIGURES = 7
CURRENT_V2_PORTAL_QA = PASS
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
CURRENT_V2_PREOUTCOME_PACKAGE = READY
CURRENT_V2_PREOUTCOME_BUILD_RUN = 36807276298
CURRENT_V2_PREOUTCOME_ARTIFACT = 11138366353
CURRENT_V2_PREOUTCOME_ARCHIVE_SHA256 = 048e234b69363800d17de98401d288d78913bc994d130024ad9310d1db6557a1
CURRENT_V2_PREOUTCOME_VALIDATED_HEAD = fb03cec738558b2fd8800a60c5d80c3ae609c237
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
CURRENT_V2_ACCESS_BLOCKED_PACKAGE = READY
CURRENT_V2_ACCESS_BLOCKED_BUILD_RUN = 36807276328
CURRENT_V2_ACCESS_BLOCKED_ARTIFACT = 11138336737
CURRENT_V2_ACCESS_BLOCKED_ACTIONS_ARTIFACT_SHA256 = ebefd85ebd8ef38288e3bad093f33d7235f9022ca1fbffdd8a468efdf9c174b4
CURRENT_V2_ACCESS_BLOCKED_GEB_SHA256 = 3b0690ea7e2b914454f1aca132835bdb800c659b2e12918ec1c5faee4ca560f0
CURRENT_V2_ACCESS_BLOCKED_REVIEW_SHA256 = 15678fd57b3865fb099e80c265e03ef67315afb7a12eea14018b9f76e157062c
CURRENT_V2_ACCESS_BLOCKED_VALIDATED_HEAD = fb03cec738558b2fd8800a60c5d80c3ae609c237
CURRENT_V2_ACCESS_BLOCKED_DETERMINISTIC_REPRODUCTION = PASS_IN_WORKFLOW_TEST
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

The deterministic submission package, reviewer archive and portal-facing
DOCX/PDF files are built, rendered and QA-checked. The remaining external
pre-submission tasks are:

1. deliver the anonymous reviewer archive through the journal portal or a
   stable anonymous link;
2. complete author-controlled title-page and declaration metadata;
3. upload the validated portal files and complete the journal form.

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
