# Streptomyces mechanism-to-architecture promotion gate v1

Lane: **A only**.

This gate prevents a future positive RED/prodiginine mechanism result from being relabeled as recovery of the missing PAYOFF matched-S architecture.

## Current status

The required matched generalist/shared Streptomyces architecture is still not recovered.

```text
MATCHED_GENERALIST_SHARED_ARCHITECTURE_RECOVERED = FALSE
MATCHED_S_COMPARATOR_CERTIFIED = FALSE
ARCHITECTURE_MAPPING_CERTIFIED = FALSE
```

The RED/prodiginine two-probe triangulation is frozen before outcome data, but remains prospective:

```text
RED_TWO_PROBE_TRIANGULATION_FROZEN_PREOUTCOME = TRUE
RED_TWO_PROBE_TRIANGULATION_PROSPECTIVE = TRUE
DIRECT_MU_OUTCOME_AVAILABLE = FALSE
```

## Why a positive mechanism result would still be insufficient

The two RED-deficient primary probes are useful because they can test whether RED/prodiginine contributes to entry into a registered terminal-deletion state. But the perturbations also alter RED/prodiginine biosynthesis itself.

Therefore a hypothetical future result

```text
RED loss -> lower direct deletion-generation mu
```

would establish a narrower mediator-to-generation relationship, not automatically the architecture counterfactual

```text
same biological task
same strategic unit
same background
shared/generalist organization instead of differentiated organization.
```

The missing comparison is still a task-matched S:D pair.

## Promotion requirements

A mechanism result can contribute to a matched-S promotion only when both blocks pass independently.

### M block — mechanism support

```text
registered two-probe generation reduction is supported;
the pre-outcome primary-probe rule was respected.
```

### A-counterfactual block — matched architecture

```text
a concrete shared/generalist candidate unit exists;
S and D are the same strategic-unit level;
the relevant net biological task is preserved or independently rescued;
task matching is not achieved by reintroducing the same differentiation mechanism;
background is adequately matched;
the focal architecture difference is isolated;
S generalist-only state is verified;
D differentiated state is verified;
both units are stable over the assay horizon.
```

Only

```text
M block PASS + A-counterfactual block PASS
```

licenses promotion of the candidate into a matched-S architecture.

## Current Streptomyces adjudication

At present the mechanism block is unresolved because direct two-probe `mu` outcomes do not yet exist. More importantly, the A-counterfactual block also fails independently:

```text
matched shared unit not recovered;
strategic-unit level not matched;
net task not demonstrated as preserved/rescued;
background/isolation requirements not met;
shared generalist-only state not verified.
```

Hence even a simulated or hypothetical future positive mechanism result cannot be used to erase these blockers.

## What would count as a stronger next comparator

The cleanest future S candidate would suppress the differentiation-generating process while leaving the relevant colony-level task and strategic-unit definition matched to D. A separation-of-function perturbation or an independently validated task rescue could in principle satisfy this requirement, but neither is currently recovered.

This document does not nominate an unvalidated strain as S.

## Claim firewall

This gate never promotes Lane G. Even a fully certified matched-S architecture still requires a separate frequency-performance experiment before `eta` or E1 can be claimed.

```text
MECHANISM_SUPPORT != MATCHED_S
MATCHED_S != FREQUENCY_FEEDBACK
FREQUENCY_FEEDBACK != AUTOMATIC_HISTORICAL_CAUSATION
```

Current labels:

```text
STREPTOMYCES_RED_TRIANGULATION_PROSPECTIVE
STREPTOMYCES_MATCHED_GENERALIST_SHARED_ARCHITECTURE_NOT_RECOVERED
STREPTOMYCES_TASK_MATCHED_ARCHITECTURE_COUNTERFACTUAL_NOT_RECOVERED
STREPTOMYCES_MATCHED_S_PROMOTION_NOT_LICENSED
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
```
