# PAYOFF empirical frequency-feedback recovery protocol

Status: prospective evidence-adjudication protocol for literature and existing-data recovery.

This protocol prevents a common category error: evidence that frequency-dependent selection exists somewhere in nature is not automatically evidence that PAYOFF's shared-versus-differentiated architecture pair has a nonzero `eta`.

## 1. Target estimand

PAYOFF's empirical frequency-feedback target is the relative reproductive/fitness margin of two heritable architectures as their frequencies change:

```text
Delta(p)=fitness_D(p)-fitness_S(p).
```

The canonical affine working model is

```text
Delta(p)=phi+eta(2p-1).
```

The empirical question is not merely whether two morphs coexist. It is whether the relative margin changes with architecture frequency on an interpretable outcome scale.

## 2. Evidence lanes

Every recovered study must be assigned to exactly one primary lane.

### Lane U — upstream architecture evidence

Evidence for conflict, compromise, recovery, architecture cost, separability, modularization or static architecture preference.

Examples:

```text
shared trait under opposing selection;
trait-axis separability;
static differentiated-versus-shared performance;
environment-dependent architecture crossing.
```

This can inform `L`, `R`, `K` or the static gap `phi`, but it does not identify `eta`.

### Lane A — frequency-feedback analogue evidence

Direct evidence that relative fitness/selection among biological alternatives changes with their frequency, but the alternatives are not yet shown to be the PAYOFF S/D architecture pair.

This lane demonstrates biological plausibility of a frequency-feedback layer and can identify candidate mechanisms or systems. It does not identify PAYOFF `eta` for the focal architecture contrast.

### Lane P — PAYOFF architecture-frequency evidence

The alternatives are explicitly the focal shared/integrated versus differentiated/released architectures, or a preregistered architecture pair mapped to them without post hoc relabeling.

Only Lane P can promote `EMPIRICAL_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED` toward identified PAYOFF frequency feedback.

## 3. Evidence tiers within Lane P

### P0 — static architecture contrast only

Requirements:

```text
S and D defined;
common outcome measured;
no architecture-frequency manipulation or natural frequency contrast adequate for frequency response.
```

Allowed claim: static architecture comparison only.

### P1 — frequency-feedback existence/sign

Requirements:

```text
S and D defined;
at least two architecture-frequency contexts;
relative D-minus-S outcome available or reconstructable;
frequency contrast precedes outcome measurement or is otherwise defensibly interpreted.
```

Allowed claim: relative performance changes with architecture frequency.

Not yet allowed: canonical `phi,eta` identification unless scale and endpoint requirements are met.

### P2 — reciprocal invasion phase

Requirements:

```text
rare D in S resident context -> margin u;
rare S in D resident context -> margin v;
strict signs separated from zero under the declared uncertainty semantics.
```

Allowed phase claims:

```text
u>0,v>0 -> reciprocal invasion / coexistence phase
u<0,v<0 -> mutual non-invasion / coordination phase
u>0,v<0 -> D dominance
u<0,v>0 -> S dominance.
```

Sign-only phase identification does not require a shared numerical assay scale, only preservation of sign by positive scale factors.

### P3 — numerical `phi,eta` identification

Additional requirement:

```text
u and v are on one common positive payoff/fitness scale.
```

Then

```text
phi=(u-v)/2,
eta=-(u+v)/2.
```

Allowed claim: pair-specific canonical PAYOFF coordinates under the declared mapping.

### P4 — affine frequency-response validation

Additional requirements:

```text
interior frequencies predeclared;
endpoint model frozen before interior outcomes are used;
interior D-minus-S outcomes on the same scale;
no refit using holdouts.
```

Allowed claim: affine PAYOFF frequency response remains compatible, or is rejected, over the measured frequency range.

Passing P4 does not eliminate every nonlinear alternative.

### P5 — finite-population test

Additional requirements depend on the stochastic process under test and must match the declared Moran or alternative process rather than borrowing its formulas automatically.

Allowed claim: empirical test of a specified finite-population PAYOFF prediction.

### P6 — recurrent-mutation/long-run occupancy test

Requires independent transition/mutation interpretation and process matching.

Allowed claim: empirical test of a specified recurrent-mutation or occupancy prediction.

## 4. Mandatory extraction fields

For every candidate record extract:

```text
study_id
doi_or_primary_source
system
alternative_1
alternative_2
architecture_mapping_status
mapping_predeclared_or_posthoc
frequency_variable
frequency_levels_or_range
frequency_manipulated
frequency_temporal_precedence
outcome_definition
outcome_common_scale
relative_margin_reconstructable
rare_D_margin_available
rare_S_margin_available
interior_holdout_available
uncertainty_type
selection_or_fitness_measure
finite_population_process_match
mutation_transition_information
primary_evidence_lane
PAYOFF_tier
claim_allowed
claim_forbidden
notes
```

## 5. Exclusion and non-promotion rules

Do not promote a study to Lane P solely because it contains:

```text
polymorphism;
coexistence;
negative frequency dependence;
rare-morph advantage;
modularity;
trait differentiation;
mutualist-antagonist trade-offs;
long-term frequency change.
```

The focal alternatives must first map to the declared architecture pair.

Do not infer reciprocal invasion from one observed stable polymorphism.

Do not infer `eta<0` from coexistence without a measured frequency response.

Do not infer `eta>0` from hysteresis when switching costs or environmental memory can generate path dependence without positive frequency dependence.

Do not infer historical splitting from a present-day differentiated architecture advantage.

## 6. Primary-source rule

A review or meta-analysis can locate candidates and summarize prior claims, but promotion to P1 or above should be based on primary-source evidence whenever accessible.

For re-analysis of an existing dataset, the data-generating design must be inspected rather than relying on the publication's narrative label.

## 7. Prospective design rule for literature recovery

Before screening a candidate family, freeze:

```text
architecture mapping rule;
frequency evidence rule;
outcome scale rule;
P-tier thresholds;
non-promotion rules.
```

A study may be biologically valuable while remaining Lane U or Lane A. The protocol is designed to preserve that information instead of forcing every useful paper into a PAYOFF-confirmatory label.

## 8. Current programme boundary

As of the current repository state:

```text
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
PAYOFF_AFFINE_FREQUENCY_RESPONSE_NOT_YET_EMPIRICALLY_VALIDATED
FINITE_POPULATION_EMPIRICAL_TEST_NOT_YET_EXECUTED
RECURRENT_MUTATION_EMPIRICAL_TEST_NOT_YET_EXECUTED
HISTORICAL_CAUSATION_NOT_IDENTIFIED
```

Existing sister-program evidence may populate Lane U or Lane A without changing these PAYOFF-specific labels.
