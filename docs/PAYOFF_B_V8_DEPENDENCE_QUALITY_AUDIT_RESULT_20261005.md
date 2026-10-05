# PAYOFF-B V8 dependence and measurement-quality audit result — 2026-10-05

Status: **DEPENDENCE-ROBUST FOR FALSIFICATION USE**

This receipt records the postoutcome diagnostic audit defined in
`docs/PAYOFF_B_V8_DEPENDENCE_QUALITY_AUDIT_LOCK_20261005.md`.

It does not change the frozen V8 hypothesis or support rule. The original
broad-degradation hypothesis remains NOT_SUPPORTED.

## A0 — range-column semantics

The Amaral data dictionary text appears to reverse the verbal descriptions of
`mig_cell` and `breed_cell`, but the original source analysis code resolves
the operational semantics:

- `mig_cell == TRUE` is used as the migratory-range state;
- `breed_cell == TRUE` is used to filter breeding-range cells.

The V8 mapping therefore follows the original code's operational semantics.

Numerical geometry also passes:
- all 166 V8 source cells are strictly lower in latitude than their paired
  target cells;
- no source/target coordinate is missing.

`A0_RANGE_SEMANTICS = PASS`

## A1 — absolute connectivity

Across the 166 primary unique spatial pairs:

Early window, 2002–2009:
- mean rho = **+0.2838**;
- median rho = **+0.3167**;
- pair-bootstrap 95% CI for mean = **+0.2145 to +0.3544**.

Late window, 2010–2017:
- mean rho = **+0.6528**;
- median rho = **+0.7812**;
- pair-bootstrap 95% CI for mean = **+0.5930 to +0.7085**.

Mean late-minus-early change:
- **+0.3690**.

The positive change therefore represents a shift from moderate to substantially
stronger positive source-destination coupling, not merely a sign change around
zero.

## A2 — cell-reuse dependence

The 166 unique spatial pairs use:
- 24 unique source cells;
- 30 unique target cells;
- as many as 23 pairs sharing one source cell;
- as many as 11 pairs sharing one target cell.

The source-target cell graph is highly connected:
- 1 connected component;
- 31 cell nodes in the component.

Despite this reuse, the positive mean survives dependence-aware diagnostics:

Source-cell cluster bootstrap:
- 95% CI = **+0.1794 to +0.5118**.

Target-cell cluster bootstrap:
- 95% CI = **+0.2799 to +0.4614**.

Two-way source × target CR0:
- SE = **0.0910**;
- 95% normal interval = **+0.1907 to +0.5473**.

## A3 — coarse spatial-block dependence

Using pair midpoints:

5-degree blocks:
- 19 blocks;
- bootstrap 95% CI = **+0.2506 to +0.4671**.

10-degree blocks:
- 8 blocks;
- bootstrap 95% CI = **+0.3039 to +0.4566**.

Thus the positive contrast is not removed by coarse regional clustering.

## A4 — leave-one-calendar-year-out

The exact-complete subset contains 58 pairs with all 8 years in both windows.

Each calendar year from 2002 through 2017 was omitted globally in turn,
recomputing the affected correlation from the remaining 7 years.

Result:
- **16/16** leave-one-year-out means remain positive;
- minimum mean delta-rho = **+0.3248**;
- maximum mean delta-rho = **+0.5012**.

No single calendar year drives the direction.

## A5 — green-up measurement support

`gr_ncell` was used as a diagnostic of the number of green-up pixels meeting
the source filtering criteria.

Mean log1p support is essentially unchanged between periods:

Source cells:
- early = **12.3972**;
- late = **12.3948**.

Target cells:
- early = **12.4665**;
- late = **12.4655**.

Mean pair support change:
- **-0.00164**.

Association with V8 delta-rho:
- cor(delta-rho, support change) = **-0.279**;
- slope on standardized support change = **-0.1267**.

Mean delta-rho by support-change quartile:
- Q1 = **+0.5115**;
- Q2 = **+0.3796**;
- Q3 = **+0.3815**;
- Q4 = **+0.2071**.

The positive V8 change is therefore not aligned with increasing
`gr_ncell` support. If anything, the largest increases in predictive
connectivity occur in the lowest support-change quartile.

This does not exclude every possible remote-sensing artifact, but it argues
against a simple increasing-measurement-support explanation.

## Frozen audit decision

All locked dependence criteria pass:

- source-cell cluster lower bound > 0;
- target-cell cluster lower bound > 0;
- 5-degree block lower bound > 0;
- 10-degree block lower bound > 0;
- 16/16 leave-one-year-out means > 0.

Therefore:

`V8_DEPENDENCE_ROBUST_FOR_FALSIFICATION_USE = YES`

## Licensed manuscript use

V4 may state:

> In this sampled eastern North American migratory-bird system,
> source-destination spring coupling strengthened between the two periods, and
> this contrast is robust to source/target cell reuse, coarse spatial blocking,
> calendar-year omission and a basic remote-sensing support diagnostic.

V4 may use the result to reject the simpler broad information-degradation
narrative for this sampled system.

V4 still may not state:
- climate change caused the strengthening;
- birds perceive the fitted correlations;
- stronger environmental correlation is necessarily more useful biological
  information;
- actionability loss caused the absence of mismatch improvement.

## Provenance

Workflow:
- run: 37300704756
- job: 111732473539
- artifact: 11341377429
- artifact SHA256: 273187c67cf5fbaa7f9bc91e55553356e61bf102afcfe4f0645009021fd284b7
