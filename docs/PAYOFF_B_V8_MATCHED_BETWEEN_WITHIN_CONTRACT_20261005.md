# PAYOFF-B V8 matched between-within information contract — 2026-10-05

Status: **POSTTRANSFER, PREOUTCOME FOR MATCHED BETWEEN-WITHIN DECOMPOSITION**

Known before this analysis:
- V8 source-destination spring predictive connectivity increased strongly;
- the preregistered negative change-on-change transfer is not supported;
- the apparent positive transfer slope is structurally explained;
- an earlier, differently constructed pooled 2026-09-26 analysis associated
  higher pre-outcome predictive connectivity with smaller mismatch.

The exact matched-panel between/within coefficients below have not been opened.

## Question

> Is predictive connectivity associated with lower mismatch as a persistent
> property of routes, even though increases in predictive connectivity do not
> produce corresponding within-route mismatch improvement?

This separates:
- **between-route information structure**; and
- **within-route information gain through time**.

## Matched panel

Use exactly the 150 eligible species-target rows and 72 unique spatial pairs
from the frozen V8 downstream-transfer primary analysis.

Create two observations per eligible species-target row:
- EARLY: rho = rho_early, mismatch = mean_mismatch_early;
- LATE: rho = rho_late, mismatch = mean_mismatch_late.

No row is added or dropped based on rho or mismatch magnitude.

## Predictor decomposition

For each unique spatial pair p:

`rho_bar_p = (rho_early_p + rho_late_p) / 2`.

For each period t:

`rho_within_pt = rho_pt - rho_bar_p`.

Standardize both coordinates using unique-pair information only:
- z_between = standardized rho_bar across the 72 unique pairs;
- z_within = standardized rho_within across the 144 pair-period values.

## Primary model

Fit the species-equal-weighted model:

`mismatch ~ period_late + z_between + z_within`.

Each species receives equal total weight across all its target cells and both
periods.

Interpretation:
- beta_between < 0: routes with persistently higher predictive connectivity
  have lower mismatch;
- beta_within < 0: increases in predictive connectivity within a route are
  associated with lower mismatch;
- beta_within >= 0 with beta_between < 0: static association without dynamic
  transfer.

## Dependency-aware uncertainty

Use exactly:
- bootstrap unit = UNIQUE_SPATIAL_PAIR;
- 10,000 replicates;
- seed = 20261005.

Each sampled pair carries all of its species-target rows in both periods.

## Registered tests

### Between-route support

`BETWEEN_INFORMATION_ASSOCIATION = SUPPORTED`
only if beta_between < 0 and its 95% pair-bootstrap upper bound < 0.

### Within-route support

`WITHIN_INFORMATION_TRANSFER = SUPPORTED`
only if beta_within < 0 and its 95% pair-bootstrap upper bound < 0.

### Between-within dissociation

Define:

`contrast = beta_within - beta_between`.

`BETWEEN_WITHIN_DISSOCIATION = SUPPORTED`
only if:
1. BETWEEN_INFORMATION_ASSOCIATION = SUPPORTED;
2. WITHIN_INFORMATION_TRANSFER = NOT_SUPPORTED; and
3. the 95% pair-bootstrap lower bound for contrast is > 0.

This is deliberately stricter than merely observing different point estimates.

## Matched-period simple summaries

After the primary decomposition is frozen, report:
- EARLY: equal-species-weighted slope of mean_mismatch_early on standardized
  rho_early;
- LATE: equal-species-weighted slope of mean_mismatch_late on standardized
  rho_late.

These are descriptive checks and do not replace the decomposition.

## Claim ceiling

If dissociation is supported, licensed:

> Higher predictive connectivity is associated with lower mismatch across
> routes, but gains in predictive connectivity within routes do not translate
> into comparable mismatch improvement over time.

Not licensed:
- persistent route differences are causal effects of information;
- birds perceive the fitted green-up correlation;
- evolutionary adaptation causes the between-route association;
- information deadlines or recourse cause the absent within-route transfer.

The mechanism remains supplied by the independent theory and separate
individual-level evidence, not identified by this panel alone.
