# Streptomyces prodiginine congener separation-of-function handoff v1

Lane: **A mechanism/task-match sublane only**.

Current headline:

```text
Two biochemical congener probes are now frozen before direct-mu outcomes,
but zero separation-of-function interventions are certified.
```

This document does not recover the missing matched generalist/shared architecture.

## 1. Why congener-level probes are useful

The existing RED-deficient primary probes are valuable for testing whether prodiginines contribute to terminal-genomic-specialist generation, but they also remove or strongly reduce the focal RED output. That creates a mediator-task entanglement: a positive direct-mu result would support a mechanism while still failing to provide a task-matched shared/generalist counterfactual.

A more informative separation-of-function route is to change **which prodiginine congener is produced** without abolishing the entire upstream prodiginine pathway.

The pre-outcome question is therefore:

```text
Can congener identity be changed while keeping the focal colony-level task
sufficiently matched, and does that change DNA-damaging activity and direct mu?
```

Those three pieces must be measured separately.

## 2. Candidate 1 — delta redG congener partition

Primary source:

```text
Sydor et al. 2011, Nature Chemistry
PMID 21505498
DOI 10.1038/nchem.1024
```

The published biochemical result is unusually clean:

```text
parental pathway -> undecylprodigiosin + streptorubin B
delta redG       -> undecylprodigiosin retained; streptorubin B absent
```

RedG catalyzes oxidative carbocyclization of undecylprodigiosin to streptorubin B. Deleting `redG` therefore changes congener composition without shutting off undecylprodigiosin biosynthesis.

This is enough for:

```text
DELTA_redG_BIOCHEMICAL_CONGENER_PROBE_READY = TRUE
```

It is not enough for:

```text
ANTIBACTERIAL_TASK_PRESERVED = FALSE / NOT YET MEASURED
GENOTOXICITY_DIFFERENCE_MEASURED = FALSE
DIRECT_MU_DIFFERENCE_MEASURED = FALSE
SEPARATION_OF_FUNCTION_CERTIFIED = FALSE
```

The programme must not infer task preservation merely because undecylprodigiosin is still present. Prodiginine structure can alter biological activity, so the relevant task must be measured directly in the same ecological/assay context.

## 3. Candidate 2 — delta redG plus mcpG cyclic-congener swap

The same 2011 study provides a second, more synthetic congener perturbation.

Expression of the RedG orthologue `mcpG` in the `redG` mutant redirects oxidative carbocyclization toward **metacycloprodigiosin** rather than streptorubin B.

Thus the candidate comparison can alter cyclic-congener identity while leaving the upstream undecylprodigiosin route active.

Status:

```text
DELTA_redG_PLUS_mcpG_BIOCHEMICAL_CONGENER_PROBE_READY = TRUE
SEPARATION_OF_FUNCTION_CERTIFIED = FALSE
```

Again, the missing data are not biochemical identity. They are the two biological branches that matter for PAYOFF architecture semantics:

```text
task branch:
    same-context antibacterial / competitor-suppression performance;

genotoxic branch:
    DNA damage or equivalent genotoxic readout + direct deletion-generation mu.
```

## 4. Why delta redK is only a reserve

Stanley et al. 2008 (`10.1016/j.chembiol.2007.11.015`) showed that a `redK` mutant loses the normal undecylprodigiosin/streptorubin-B products and accumulates a hydroxylated shunt derivative.

That derivative was unstable and could not be isolated for full structural characterization. Because the canonical output is effectively lost rather than cleanly partitioned, this route does not pass the current biochemical-congener-probe gate.

```text
DELTA_redK_BIOCHEMICAL_CONGENER_PROBE_READY = FALSE
```

It remains a reserve chemistry probe, not a primary architecture route.

## 5. The predeclared certification ladder

The congener programme now has four distinct levels.

### C0 — biochemical congener probe

Requires:

```text
matched background;
congener profile changed;
prodiginine output not fully abolished;
candidate frozen before direct-mu outcome.
```

Current result:

```text
C0 count = 2
```

### C1 — task preservation

Requires direct evidence that the focal antibacterial/competitive task remains matched in the same context and that gross developmental state is sufficiently comparable.

Current result:

```text
C1 count = 0
```

### C2 — genotoxic branch

Requires a measured change in DNA-damaging/genotoxic activity plus a direct-mu measurement under the registered deletion-generation contract.

Current result:

```text
C2 count = 0
```

### C3 — separation of function

Requires both C1 and C2 on a C0-qualified probe.

Current result:

```text
C3 count = 0
```

## 6. No automatic architecture promotion

Even C3 would mean only that a prodiginine congener perturbation separates the focal task from the candidate genotoxic/differentiation branch.

It would still not automatically establish:

```text
matched generalist/shared architecture
matched S:D strategic units
full architecture mapping
frequency-dependent architecture fitness
eta
E1
```

Those remain governed by the independent matched-comparator and mechanism-to-architecture promotion gates.

## 7. Current status

```text
PRODIGININE_CONGENER_CANDIDATES_FROZEN_PREOUTCOME = TRUE
BIOCHEMICAL_CONGENER_PROBE_READY_COUNT = 2
TASK_PRESERVATION_SUPPORTED_COUNT = 0
GENOTOXIC_BRANCH_SUPPORTED_COUNT = 0
SEPARATION_OF_FUNCTION_CERTIFIED_COUNT = 0
MATCHED_GENERALIST_SHARED_ARCHITECTURE_RECOVERED = FALSE
MATCHED_S_CERTIFIED = FALSE
ARCHITECTURE_MAPPING_CERTIFIED = FALSE
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_IDENTIFIED = FALSE
```

This is the intended next positive handoff: move from full RED knockout probes toward congener-level perturbations that may eventually separate the mediator from the ecological task, without claiming that the separation has already been demonstrated.
