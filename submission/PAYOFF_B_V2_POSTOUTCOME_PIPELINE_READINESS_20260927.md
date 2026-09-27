# PAYOFF-B V2 postoutcome pipeline readiness

Audited: **2026-09-27**

Status: **PASS — V2 postoutcome pipeline ready; real Aikens outcome still unopened**

## Canonical publication state

```text
PAPER_2_CANONICAL_SOURCE =
    manuscript/PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md

V1_STATUS =
    FROZEN_PROVENANCE_ONLY

REAL_AIKENS_LAMBDA_OUTCOME =
    UNOPENED
```

This receipt certifies only that the canonical V2 package can safely receive
the preregistered Aikens result. It is not an Aikens scientific result.

## Outcome-class coverage

The pipeline was tested against all four preregistered completion classes:

- PASS;
- FAIL_WRONG_DIRECTION;
- FAIL_INSUFFICIENT_SUPPORT;
- NOT_ESTIMABLE.

Synthetic payloads are test fixtures only.

## Outcome-invariance result

Across all four classes, CI verifies:

- identical blinded V2 main-manuscript hash;
- identical seven-figure manifest hash;
- unchanged title;
- unchanged structured abstract;
- unchanged main information-deadline / recovery-failure claim hierarchy;
- Aikens-specific wording confined to Supporting Information and claim-state
  receipts.

The Supporting Information differs across result classes as intended.

For NOT_ESTIMABLE, the gate is resolved but no lambda estimate is treated as
opened.

## Active authenticated workflow

The active workflow is:

`.github/workflows/payoff-b-aikens-appeears-full-extraction.yml`

After registered result classification it now executes only:

```text
registered result JSON
-> V2 Supporting Information renderer
-> V2 postoutcome GEB package
```

It no longer generates V1 rendered manuscripts or V1-derived outcome packages.

## Verified CI

Fast routing / outcome-invariance check:

```text
workflow = PAYOFF-B V2 postoutcome fastcheck
run = 36311298413
head = 9e6a44736a3828398aafc292c8d848129a8e9544
status = SUCCESS
```

Package invariance check:

```text
workflow = PAYOFF-B V2 GEB postoutcome pipeline
run = 36311298440
head = 9e6a44736a3828398aafc292c8d848129a8e9544
status = SUCCESS
```

## Remaining external blocker

The real Aikens result remains blocked by AppEEARS/Earthdata authentication.

No environmental values or lambda outcome are opened by this readiness work.

## Post-result state

After one valid authenticated run, the science package can become
`POSTOUTCOME_INTERNAL_READY` under any of the four registered result classes.

Journal upload will still require:

1. an anonymized stable reviewer archive link;
2. author-controlled title-page / declaration metadata.

No result class is permitted to retune the V2 title, abstract spine, main
figures or primary information-coordination conclusion.
