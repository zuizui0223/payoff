# PAYOFF-B V8 downstream transfer contract — 2026-10-05

Status: **POSTPRIMARY, PREOUTCOME FOR THE V8 CHANGE-TO-BIRD-CHANGE TEST**

The V8 environmental primary result and mandatory sensitivities are already
open and frozen. They show a robust positive change in source-destination
spring predictive connectivity. This contract defines a new secondary test
before inspecting any bird-outcome change as a function of V8 delta-rho.

The specific outcome below — late-minus-early change in bird arrival–green-up
mismatch on the V8 mapped species-target cells — has not been used to choose
the model, sign, filters, weights, benchmark or support rule.

## 1. Biological question

> When source-destination spring predictability increased, did migratory bird
> timing capitalize on that increase?

This is a transfer test from changing environmental predictability to changing
realized phenological mismatch. It is not a test that birds literally perceive
the fitted correlation.

## 2. Frozen environmental exposure

Use the already-opened V8 primary unique-pair result without modification:

`delta_rho_p = rho_late_p - rho_early_p`

from:
- EARLY = 2002–2009;
- LATE = 2010–2017;
- separately detrended source and target mid-green-up series;
- the frozen Amaral source-target mapping;
- the 166 finite V8 unique spatial pairs.

No V8 pair, window, detrending rule or mapping is changed using bird outcomes.

## 3. Bird outcome

For every frozen V8 species-target-cell mapping row, define annual mismatch on
the same scale used by the frozen 2026-09-26 broad-bird analysis:

`mismatch_y = log1p(abs(gr_mn - arr_GAM_mean))`.

For a species-target-cell row to enter the transfer test, require at least
6 finite annual bird-mismatch observations in EACH window:

- 2002–2009;
- 2010–2017.

Then calculate:

`mean_mismatch_early` = arithmetic mean of annual `mismatch_y` in EARLY;

`mean_mismatch_late` = arithmetic mean of annual `mismatch_y` in LATE;

`delta_mismatch = mean_mismatch_late - mean_mismatch_early`.

Interpretation:
- delta_mismatch < 0 = mismatch improved;
- delta_mismatch = 0 = no change;
- delta_mismatch > 0 = mismatch worsened.

Eligibility is determined only by counts of finite annual mismatch values, not
by their sign or magnitude.

## 4. Primary transfer estimand

Rows are species × target-cell exposures. Several species can share the same
environmental pair, so the exposure is not independent across all rows.

Standardize `delta_rho` across the eligible UNIQUE environmental pairs:

`z_delta_rho = (delta_rho - mean_pair_delta_rho) / sd_pair_delta_rho`.

Fit the weighted linear model:

`delta_mismatch ~ z_delta_rho`

with each species receiving equal total weight. A row for species j receives
weight:

`w_jp = 1 / n_j`

where `n_j` is that species' number of eligible target-cell rows.

Thus the coefficient is an equal-species exposure estimand rather than a
cell-count-weighted estimand.

Registered direction:

`beta_transfer < 0`.

A negative coefficient means that species-route exposures with larger gains in
environmental predictive connectivity show larger reductions in realized
arrival–green-up mismatch.

## 5. Dependency-aware uncertainty

Use exactly:

`BOOTSTRAP_UNIT = UNIQUE_SPATIAL_PAIR`

`BOOTSTRAP_REPLICATES = 10000`

`BOOTSTRAP_SEED = 20261005`

Each sampled spatial pair carries all eligible species-target rows mapped to
that pair. Refit the same equal-species-weighted model in each replicate.

This preserves the exact reuse of environmental exposure across species.
Species dependence is additionally assessed by leave-one-species-out
sensitivity; the bootstrap is not claimed to solve phylogenetic dependence.

## 6. Primary support rule

`INFORMATION_TO_TIMING_TRANSFER = SUPPORTED`

only if:
1. the fitted `beta_transfer` is negative; and
2. the 95% unique-pair bootstrap interval has upper bound < 0.

Otherwise:

`INFORMATION_TO_TIMING_TRANSFER = NOT_SUPPORTED`.

No alternative weighting, transform or covariate model replaces the primary
test.

## 7. Frozen benchmark for a possible disconnect

The already-frozen 2026-09-26 pooled broad-bird result estimated:

`beta_prior = -0.0461786181`

for log mismatch per 1 SD of pre-outcome predictive connectivity.

This coefficient is dependence-sensitive and is NOT treated as a universal
causal effect. It is used only as a preregistered empirical reference magnitude.

After fitting the primary transfer model, report whether its 95% bootstrap
interval excludes effects at least as negative as `beta_prior`.

Define:

`PRIOR_MAGNITUDE_TRANSFER_EXCLUDED = YES`

only if the lower 95% bootstrap bound for `beta_transfer` is greater than
`-0.0461786181`.

This does NOT establish equivalence to zero or prove that birds failed to use
information. It only says that a change-effect as negative as the earlier
pooled cross-sectional coefficient is not compatible with this transfer
estimate at the stated interval.

## 8. Mandatory sensitivities

After the primary coefficient is frozen:

1. unweighted species-target-cell regression;
2. equal-species collapse: regress each species' mean delta-mismatch on its
   mean V8 delta-rho;
3. add early-window mismatch as a baseline covariate;
4. add target-cell mean green-up date change
   (late mean gr_mn - early mean gr_mn) as a climate-shift covariate;
5. add both baseline mismatch and target green-up change;
6. leave-one-species-out primary weighted model;
7. exact-complete bird windows: require 8/8 finite mismatch years in both
   periods.

All sensitivities retain the frozen V8 environmental exposure.

## 9. Secondary actuator bridge

Only after the mismatch-transfer result is frozen, a separate descriptive lane
may ask whether V8 delta-rho is associated with late-minus-early change in mean
bird migration speed (`log(vArrMag)`) on rows with sufficient data.

That speed lane is not part of the present primary support rule and is not
opened by the primary transfer script.

## 10. Interpretation ceiling

If transfer is supported, the licensed conclusion is:

> In the sampled Amaral bird system, route exposures with larger increases in
> source-destination spring predictive connectivity also tended to show larger
> reductions in arrival–green-up mismatch.

If transfer is not supported, the licensed conclusion is only:

> The frozen analysis did not detect the preregistered negative relationship
> between increasing environmental predictive connectivity and improving bird
> mismatch.

Even if the prior-magnitude benchmark is excluded, do NOT claim:
- birds ignored information;
- information was biologically unavailable;
- an information deadline caused the disconnect;
- climate change caused the connectivity increase;
- improved predictability should necessarily improve fitness.

Those stronger mechanisms require additional evidence.

## 11. Outcome-access rule

Before this contract is committed:
- do not calculate delta_mismatch for the V8 exposure set;
- do not fit the transfer coefficient;
- do not inspect its sign;
- do not run leave-one-species-out transfer models;
- do not calculate speed-change associations.

`V8_TRANSFER_CONTRACT = FROZEN_PREOUTCOME`
`V8_TRANSFER_PRIMARY_OUTCOME = UNOPENED`
