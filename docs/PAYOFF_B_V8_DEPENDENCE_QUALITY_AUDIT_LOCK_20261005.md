# PAYOFF-B V8 dependence and measurement-quality audit — 2026-10-05

Status: **POSTOUTCOME DIAGNOSTIC LOCK; WRITTEN BEFORE THE DIAGNOSTICS BELOW ARE OPENED**

Known before this audit:
- the frozen V8 degradation hypothesis is NOT_SUPPORTED;
- mean detrended source–destination correlation change is strongly positive;
- mandatory scale/window/LOO-species sensitivities retain the positive direction;
- larger connectivity gains do not predict the registered reduction in bird mismatch;
- the apparent opposite-sign transfer slope is structurally explained.

This audit does not redefine any V8 hypothesis. It asks whether the strong
positive environmental change is robust enough to serve as a falsification
layer in the V4 manuscript.

## A0 — range-column semantic audit

The Amaral repository data dictionary describes `mig_cell` and
`breed_cell` in a way that appears reversed relative to their names.
Before interpreting V8 geography, record how the original analysis code
actually uses these columns.

The V8 mapping is semantically accepted only if original source code uses:
- `mig_cell == TRUE` as migratory-range cells;
- `breed_cell == TRUE` as breeding-range cells.

Also verify numerically that every frozen V8 source latitude is strictly below
its paired target latitude.

No V8 result is recalculated under a reversed mapping unless this audit fails.

## A1 — absolute early and late connectivity

On the 166 primary finite unique spatial pairs, report:
- unweighted mean and median rho in 2002–2009;
- unweighted mean and median rho in 2010–2017;
- mean delta-rho.

Use the existing unique-pair bootstrap only to report 95% intervals for the
two means. This is descriptive context.

## A2 — cell-reuse dependence

Report:
- number of unique source cells;
- number of unique target cells;
- maximum number of V8 pairs sharing one source;
- maximum number sharing one target;
- number and size distribution of connected components in the undirected
  source–target cell graph.

For the mean delta-rho, compute three dependence diagnostics:
1. source-cell cluster bootstrap, 10,000 replicates;
2. target-cell cluster bootstrap, 10,000 replicates;
3. two-way source × target cluster-robust CR0 standard error for an intercept-only
   model, with the usual inclusion–exclusion form
   `V_source + V_target - V_pair`.

Cluster bootstrap seed = 20261005.
These are diagnostics, not replacements for the frozen primary interval.

## A3 — coarse spatial-block dependence

Join source and target coordinates from the frozen Amaral cell table. Define
pair midpoint coordinates by the arithmetic mean of source and target latitude
and longitude.

Before opening results, fix two block grids:
- 5-degree latitude × 5-degree longitude;
- 10-degree latitude × 10-degree longitude.

For each grid, resample spatial blocks with replacement 10,000 times, carrying
all pairs within a sampled block, and report the bootstrap interval for mean
delta-rho.

Seed = 20261005.

The two resolutions are both reported; neither is selected after inspection.

## A4 — leave-one-calendar-year-out stability

Use only the 58 exact-complete pairs that have all 8 green-up years in both
primary windows.

For each of the 16 calendar years from 2002 through 2017:
- omit that year globally;
- recompute the affected-window detrended correlation from the remaining
  7 years;
- leave the other 8-year window unchanged;
- calculate mean delta-rho across the same 58 pairs.

Report all 16 means, their range, and the number retaining positive direction.

No significance test is attached.

## A5 — green-up measurement-support audit

Use `gr_ncell`, the number of green-up pixels meeting the source filtering
criteria, as a measurement-support diagnostic.

For each primary V8 pair and each window, calculate separately for source and
target:
- mean `log1p(gr_ncell)` across available years.

Then define:
- source support change = late - early;
- target support change = late - early;
- mean pair support change = average of source and target changes.

Report:
- overall early and late support means for source and target cells;
- Pearson correlation between delta-rho and mean pair support change;
- slope from `delta_rho ~ z_support_change`;
- mean delta-rho separately in quartiles of support change.

This diagnoses whether improved remote-sensing support is aligned with the
positive V8 change. It is not interpreted as a causal correction.

## A6 — interpretation rule

The strong positive V8 environmental result is considered **DEPENDENCE-ROBUST
FOR FALSIFICATION USE** only if:
- source-cluster, target-cluster, 5-degree block and 10-degree block 95%
  intervals for mean delta-rho all remain entirely above zero; and
- all 16 leave-one-year-out complete-pair means remain positive.

Measurement-support results are reported independently. A correlation with
`gr_ncell` change lowers confidence in interpreting the positive change as a
pure environmental synchronization signal, but it does not retrospectively
change the frozen V8 outcome.

If any dependence criterion fails, V4 must describe V8 as a positive point
pattern with dependence-sensitive uncertainty rather than as a strong broad
increase.

## Claim boundary

This audit cannot establish that climate change caused any connectivity change,
that birds perceive the fitted correlations, or that spatial correlation is
equivalent to biological information.

It only determines whether the V8 positive environmental contrast is robust
enough to reject the simpler broad-degradation narrative in this sampled
system.
