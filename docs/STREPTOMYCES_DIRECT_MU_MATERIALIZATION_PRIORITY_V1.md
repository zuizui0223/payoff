# Streptomyces direct-mu materialization priority v1

Status: **pre-outcome material-recovery governance; first qualified-reference milestone active**.

## Main correction

The six 2022 mutant lineages M1-M6 are named lineages, but they are not six independent origins. The published methods state that one mutant colony was replated and six descendant colonies were chosen to found M1-M6. They therefore form one origin cluster for the direct-mu panel.

W3 is different: it began as a WT lineage and independently acquired terminal deletion during serial transfer. A post-deletion W3 archive can therefore contribute a second biological origin if it later passes the registered reference-qualification gate.

## Information-value decision

The repository has enough literature candidates to expose the current bottleneck. Additional candidate papers do not resolve the missing realization reference.

Therefore the active objective is now:

```text
qualified direct-mu matched-D reference count: 0 -> 1
```

rather than increasing the candidate list.

While the count remains zero and at least one frozen-priority candidate is still actionable:

```text
CANDIDATE_LITERATURE_EXPANSION = PAUSED
ARCHITECTURE_SPECIFIC_INFERENCE_HARD_CLOSED = TRUE
```

The stronger final panel target remains unchanged at two independent qualified references per registered deletion class. The first-reference milestone is an execution priority, not a relaxation of the panel.

## Frozen recovery order

1. **M5_T0** — archived, T0 sequenced, T0 competition available, and the only mutant lineage reported not to accumulate further large deletions during the transfer experiment. This is the primary first-reference target, not a qualified reference by declaration.
2. **W3_POST_DELETION** — prioritized second because it adds an independent de-novo deletion origin. The exact archived post-deletion timepoint must be frozen before assay.
3. **M1_T0** — archived, T0 sequenced, and T0 competition available, but it shares the M1-M6 founding-mutant origin and therefore does not supply a second independent origin if M5 is already used.

New candidate hunting resumes only if all three targets are terminally inaccessible or fail the registered qualification gate while the qualified-reference count is still zero.

## Required next steps for every candidate

Materialization does not equal qualification. Before a candidate can enter a reference class it still needs:

- physical stock access confirmed;
- exact registered marker class extracted/verified;
- core reference retained;
- same-context 72 h -> 120 h SFM realization assay against a matched intact comparator;
- gross secondary rearrangements resolved;
- closed realization uncertainty bands for deleted and intact material;
- independent `r=d/g` derived without using the direct-mu outcome;
- and the existing per-reference qualification receipt.

Panel-level independence is then checked separately. Two qualified descendants of one founding mutant still count as one independent origin.

## One reference is necessary, not sufficient

When the first D reference qualifies, PAYOFF may say that the direct-mu realization channel has an empirically anchored matched-D comparator.

It still may not claim:

```text
matched S recovered
full S:D architecture mapping
architecture-specific frequency feedback
architecture-specific eta
E1
```

until the independent downstream gates pass.

See `docs/STREPTOMYCES_FIRST_QUALIFIED_D_REFERENCE_GATE_V1.md`.

## Current status

```text
literature candidate pool recovered = TRUE
qualified D references = 0
primary first-reference target = M5_T0
candidate literature expansion = PAUSED
origin-independence pass = FALSE for every registered class
direct-mu outcome = unavailable
matched S = FALSE
architecture mapping = FALSE
architecture-specific inference = HARD CLOSED
eta architecture-specific = unavailable
E1 = FALSE
```
