# PAYOFF-B two-paper publication architecture — current state

Status: **adopted two-paper publication architecture; canonical publication state updated 2026-09-27**

> **2026-09-27 canonical amendment:** Paper 2 is
> `manuscript/PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md`.
> The earlier
> `manuscript/PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md`
> is frozen as provenance/rollback only and is not an active parallel submission.
> The authoritative V1/V2 rule is
> `docs/PAYOFF_B_V1_V2_PUBLICATION_RELATION_20260927.md`.

## Adopted publication decision

PAYOFF-B remains a **two-paper programme**.

### Paper 1 — exact benchmark

Canonical manuscript:

`manuscript/PAYOFF_B_THEORETICAL_ECOLOGY_BRIEF_V1.md`

Target:

**Theoretical Ecology**

Core contribution:

> In the symmetric two-patch, two-season anti-phase model, the temporal growth
> premium has exactly one positive migration optimum for every nonzero
> environmental contrast, and the optimum collapses onto a dimensionless
> seasonal-timescale curve.

Paper 1 remains a short exact theorem paper. It does not absorb the moving-
landscape, information-coordination or migration-empirical programmes.

### Paper 2 — information coordination in seasonal tracking

Canonical PREOUTCOME manuscript:

`manuscript/PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md`

Role:

**sole active integrated ecology manuscript**

Primary ecological conclusion:

> **Seasonal coordination can fail not because information is absent, but
> because interacting organisms begin using the same information at different
> decision thresholds; once an information-using convention collapses,
> restoring even perfect environmental information need not restore ecological
> coordination.**

Compact conceptual claim:

> **Information use, not information alone, is an ecological state variable.**

Current headline:

> **Theory predicts that environmental information can recover before ecological coordination does.**

## Analytic spine of Paper 2

The abstract and opening argument are intentionally restricted to the strongest
two-step theory.

### Core layer A — information deadlines

**T1.** Information has an action threshold.

**T2.** Effective decision deadlines determine the cue reliability at which
each actor begins using information.

The empirical cost is not raw elapsed delay but the total effective waiting
cost

`D_eff(delta)=J(delta)+min_c[K(c)+M(delta-c)]`,

or its total causal equivalent under a biologically faithful waiting
intervention.

**T3.** Heterogeneous effective deadlines create a finite range in which
improving the same cue increases mismatch because uptake is asynchronous.

The exact two-actor desynchronization width is

`Delta q = |D_eff,2-D_eff,1|/(A+L)`

for the fixed-cost declared binary model when both actors eventually use the
cue. Raw waiting duration does not generally rank `D_eff` and can even rank
information-use thresholds in the wrong order.

### Core layer B — recovery failure

**T7.** Under perfect environmental information, an obsolete uninformed timing
profile and a better informed timing profile can coexist as strict Nash
equilibria.

**T8.** Temporary cue degradation can collapse coordinated information use, and
restoration to perfect cue accuracy need not restore the informed state.

These two layers carry the abstract.

### Secondary theory retained in Results / Discussion

The following are important mechanistic extensions but do **not** receive equal
weight in the abstract:

- **T4:** asynchronous uptake forms a network cut;
- **T5:** deadline placement on the interaction network changes disruption;
- **T6:** private and joint value of waiting can diverge;
- **T9:** acquisition memory and topology-dependent memory are distinct;
- compensated/hidden-deadline refinements that define `D_eff`;
- dual-use information, where the focal cue can also inform downstream
  compensation and make `D_eff(q)` cue-dependent;
- exact decision-complexity/headroom scaling and threshold crowding near
  perfect information;
- rescue-coalition and temporary-seed results;
- topology-dependent rescue leverage;
- the older movement/phenology capacity programme.

This ordering is deliberate. Paper 2 should not read as a catalogue of
theorems.

## Natural evidence hierarchy

Natural evidence supports separate edges of the mechanism rather than one
complete natural hysteresis demonstration.

### E1 — broad migratory birds

The preregistered 37-species / 3,311-row analysis gives pooled directional
support for stronger pre-outcome predictive connectivity being associated with
smaller arrival-green-up mismatch.

Dependence-aware uncertainty prevents a universal species-level coefficient
claim.

### E2 — pied flycatcher experiment

Manipulated resident-tit phenology was largely unavailable to an earlier male
settlement decision but affected later female settlement / pairing.

Licensed role:

**timing-dependent cue availability anchor**

Not licensed:

females deliberately waited in order to obtain information.

### E3 — wigeon

The registered predictive-connectivity x incoming-phase interaction is
**NOT_SUPPORTED**.

This separates information available before commitment from correction after
phase error has already appeared.

### E4 — long-term flycatcher cue-driver lane

The preregistered 1980-2010 lane is
**NO_CUE_DRIVER_REVERSAL**.

The path-dependence model was not opened.

Therefore no natural system is currently claimed to demonstrate
information-recovery network hysteresis.

### E5 — same-system cue–resource prospective gate

The preregistered Hoge Veluwe cue–resource gate is
**NO_CUE_RESOURCE_REVERSAL**. Because the environmental prerequisite failed,
resident–migrant history was not opened.

### E6 — cross-system information-distance triangulation

A dependence-aware reconstruction of 944 temperature-response effects from 28
studies and 279 bird species gives an adjusted long-minus-short migration
contrast of **+0.421 d / °C** (95% CI **+0.121 to +0.722**, p = **0.0077**).
All 28 leave-one-study-out fits retain positive effects and positive CI lower
bounds. An independent Freimuth et al. benchmark reproduces 1,763 local
plant/pollinator species slopes and all five published group means.

Licensed role: evidence consistent with an **information-distance axis**.

Not licensed: a causal bird-versus-pollinator coefficient, a universal
taxonomic ranking, or a claim that these two sources constitute a new
cross-taxon meta-analysis.

E6 interpretation is explicitly non-causal: photoperiodic/endogenous control is retained as a non-exclusive alternative explanation for the migration-distance gradient, and no current natural dataset estimates the pairwise theoretical effective-deadline difference `D_eff,2-D_eff,1` or observes the predicted desynchronization window directly.

Figure 5 carries the migration-distance reconstruction and independent local plant–pollinator benchmark with an explicit no-causal-taxon-contrast boundary.

### E6b — interaction-level response-asymmetry bridge

Burgess et al. (2018) provide published consumer--resource pair evidence:
temporal major-axis slopes of bird first-egg date on caterpillar peak are
0.510 (Blue Tit), 0.515 (Great Tit) and 0.348 (Pied Flycatcher), with all
95% credible intervals below the perfect-tracking value of one.

Licensed role: **actual interacting partners show response asymmetry that changes relative timing.** Burgess et al. provide the trophic resource bridge; Samplonius et al. (2018) provide an independent resident-tit versus migratory-flycatcher bridge in which differential temperature sensitivity widened the laying-date interval by 0.94 d/decade.

Not licensed: `D_eff,2-D_eff,1` has been measured, `q1 < q <= q2` has been
observed, or information distance is the causal mechanism for the deficits.

### E7 — greater snow goose effective-deadline bridge

The St. Lawrence -> Bylot lineage now supplies separate source-backed anchors
for route-to-breeding predictability, captivity carry-over cost, a two-sided
laying-date fitness surface, migration-stage timing compensation and
post-arrival buffering.

These pieces motivate

`D_eff = J + optimized downstream compensation/residual loss`

but do not identify natural `D_eff`. A GPS departure cue-uptake lane and a
one-way downstream dual-use compensation screen are preregistered and unopened.

The row-level FED physiological J lane remains source-access blocked; published
physiology instead supports a multicomponent direct-cost interpretation rather
than a single identified mediator.

Licensed role: **mechanistic bridge showing why effective waiting cost can have
recoverable timing and nonrecoverable carry-over components.**

Not licensed: natural information-waiting `J`, natural `D_eff`,
actor-specific `q_wait`, or a pairwise asynchronous window.

## Capacity layer inherited from V1

The earlier V1 conclusion remains scientifically valid:

> Temporal adjustment can buffer spatial tracking demand, but cannot replace
> movement indefinitely under sustained directional environmental change.

V2 retains that result as the **capacity layer**, together with:

- local movement/timing substitutability;
- finite temporal buffering;
- spatial re-entry;
- fragmentation exposure;
- phase-retention / actuator decomposition;
- direct migration-system evidence;
- the unopened Aikens within-taxon perturbation gate.

These results support Paper 2 but do not define its primary novelty.

## V1/V2 publication rule

The previous Paper 2 generation

`manuscript/PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md`

has status:

`FROZEN_PROVENANCE_ONLY`

It is not an independent submission candidate while V2 is active.

No V1/V2 dual submission is allowed.

V1 may be changed only for factual errata or provenance metadata. New science,
framing and journal-facing edits belong in V2.

## Submission-package rule

Any Paper 2 journal package built from V1 is provenance only.

Current state:

```text
PAPER_2_CANONICAL_SOURCE = PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md
V1_STATUS = FROZEN_PROVENANCE_ONLY
CURRENT_V2_PREOUTCOME_PACKAGE = READY
CURRENT_V2_PREOUTCOME_BUILD_RUN = 36508668487
CURRENT_V2_PREOUTCOME_ARTIFACT = 11007724762
CURRENT_V2_PREOUTCOME_ARCHIVE_SHA256 = f0d006e1015d76b13ba059dcc21ef5ff9c9b6b7b314cf37df8c04ea522da5848
CURRENT_V2_FINAL_SUBMISSION_PACKAGE = ACCESS_BLOCKED_SCIENCE_CLOSED_PORTAL_BLOCKED
CURRENT_V2_ACCESS_BLOCKED_GEB_SHA256 = b10d00dc8252c8b7efafbeafffaf3c32480eb199236b529979e7a122ef0fe8ec
CURRENT_V2_ACCESS_BLOCKED_REVIEW_SHA256 = e826d500310f2d884a62c3913fc3798ec2ec762cd776b6b89252ec26891327bd
OLD_V1_GEB_PACKAGE = PROVENANCE_ONLY
```

The V2 PREOUTCOME package has completed fresh word-count, display-piece,
reference, anonymity, citation and journal-facing package audits.

The current submission route is frozen as non-scientific `ACCESS_BLOCKED`.
The Aikens lambda outcome remains unopened, but authenticated execution is now
a permitted future extension rather than a current submission blocker.

Before final submission, V2 still requires:

- delivery of the ACCESS_BLOCKED anonymous reviewer archive through the journal
  portal or a stable anonymous review link;
- author-controlled title-page and declaration metadata;
- final human review of the outcome-rendered package and portal metadata.

## Journal routing

Current first shot remains:

**Global Ecology and Biogeography / Research Article**

Journal routing may be reconsidered only as a publication decision, not by
retuning scientific claims to fit an outlet.

## Aikens gate

The preregistered Aikens lambda outcome remains unopened.

For the current submission route, Paper 2 is **ACCESS_BLOCKED
science-closed** rather than PREOUTCOME. The registered Aikens scientific
outcome remains unopened and may still be executed later under the original
frozen contract.

The V2 information-deadline and recovery-failure conclusions must remain
coherent under:

- supported;
- wrong-direction;
- insufficient-support;
- NOT_ESTIMABLE

Aikens outcomes.

No title, abstract spine or main information-coordination conclusion may be
retuned based on the Aikens sign.

## Active publication queue

```text
PAPER 1
    PAYOFF-B exact anti-phase theorem
    target: Theoretical Ecology
    status: active independent paper

PAPER 2
    PAYOFF-B information coordination in seasonal tracking
    canonical source: PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md
    status: active ACCESS_BLOCKED science-closed broad-ecology paper

V1 integrated tracking manuscript
    status: frozen provenance / rollback only
```

All older standalone tracking-theory, GEB movement-phenology and V1 integrated
packages remain source/provenance material rather than overlapping submission
candidates.
