# Streptomyces first qualified direct-mu D-reference gate v1

Status: **ACTIVE EXECUTION HARD STOP / PRE-OUTCOME**.

## Decision

PAYOFF should not increase the number of literature candidates while the direct-mu realization channel still has zero qualified matched-D references.

The immediate information target is:

```text
qualified matched D reference count: 0 -> 1
```

not:

```text
candidate literature count: larger
```

The existing literature pool is already sufficient to expose the biological bottleneck. The current materialization queue is frozen as:

```text
1. M5_T0
2. W3_POST_DELETION
3. M1_T0
```

`M5_T0` is the primary target because it is archived, T0-sequenced, has T0 competition information, and was the only M1-M6 lineage reported not to accumulate another large deletion during the transfer experiment. This priority does not qualify M5 by declaration.

## What counts as the first qualified matched-D reference

A candidate counts only after the existing per-reference qualification gate returns `qualified=true` under the registered direct-mu realization context.

At minimum the candidate must have:

```text
physical / recoverable reference identity
registered deletion-class marker pattern verified
core reference present
pre-existing D material at the interval start
same medium and ecological context as the intact comparator
independent derivation from the direct-mu candidate outcome
viability / measurability at 72 h
measurability at 120 h
gross secondary rearrangement resolved
closed same-context realization band for d
and therefore an independently constrained r=d/g.
```

A named strain, sequenced mutant, published competition coefficient, or terminal-deletion phenotype is not a qualified direct-mu reference by itself.

## Zero-reference hard stop

While

```text
qualified_D_reference_count == 0
```

PAYOFF must retain:

```text
DIRECT_MU_REFERENCE_PRECONDITION = FALSE
ARCHITECTURE_SPECIFIC_INFERENCE_HARD_CLOSED = TRUE
CANDIDATE_LITERATURE_EXPANSION = PAUSED
```

The following cannot be promoted from Streptomyces direct-mu work:

```text
matched S:D architecture inference
architecture-specific frequency feedback
architecture-specific eta
finite-population architecture inference
E1
```

Generic game analogues and mechanism probes may remain available under their own claim ceilings, but they cannot be relabelled as architecture-specific evidence.

## What one qualified reference does and does not unlock

The first qualified matched-D reference is a **necessary milestone, not a sufficient architecture proof**.

One qualified reference allows PAYOFF to say that the direct-mu realization channel has at least one empirically anchored D comparator and to proceed with the registered reference-anchored measurement programme.

It does **not** by itself establish:

```text
a complete ENTRY / INTERMEDIATE / DEEP D panel
a matched generalist/shared S comparator
full S:D architecture mapping
frequency-dependent architecture payoff
eta
E1.
```

The existing full-panel requirement of two independent qualified references per registered class remains a stronger downstream requirement and is not relaxed by this milestone.

## Candidate-search restart rule

New literature candidate hunting remains paused while any member of the frozen queue is still materially actionable.

Search may resume only if:

```text
M5_T0 is terminally inaccessible or fails qualification
AND
W3_POST_DELETION is terminally inaccessible or fails qualification
AND
M1_T0 is terminally inaccessible or fails qualification
AND
qualified_D_reference_count remains 0.
```

A reversible blocker such as missing stock confirmation, unrun marker assay, or unrun 72-120 h realization assay is not a terminal failure and does not license another literature expansion round.

## Execution order for M5_T0

For the first target, the next evidence work should proceed in this order:

```text
A. confirm physical stock / archive access
B. freeze exact registered deletion class from sequence / marker evidence
C. verify core-reference retention and exclude gross secondary rearrangement relevant to the registered class
D. run same-context 72 h -> 120 h realization assay against matched intact reference
E. construct closed d and g uncertainty bands
F. derive r=d/g without using the direct-mu outcome
G. run direct_mu_reference_panel_qualification.qualify_d_reference
```

Only step G can create the first qualified-reference receipt.

## Machine-readable guard

The repository-level hard stop is implemented in:

```text
src/direct_mu_first_reference_gate.py
validation/streptomyces_direct_mu_first_reference_status_v1.json
```

The guard intentionally distinguishes:

```text
first qualified D reference recovered
!= full D panel qualified
!= matched S recovered
!= architecture mapping certified
!= architecture-specific inference opened.
```

## Current status

At the current source head:

```text
qualified D references = 0
primary target = M5_T0
candidate expansion hard stop = TRUE
minimum D-reference precondition for architecture-specific inference = FALSE
architecture-specific inference = HARD CLOSED
```
