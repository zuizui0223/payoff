# PAYOFF-B V8 environment-to-bird transfer result — 2026-10-05

Status: **TRANSFER OF ENVIRONMENTAL PREDICTABILITY GAINS INTO IMPROVED MATCHING NOT SUPPORTED**

This receipt records the prospectively locked postprimary secondary analysis in
`docs/PAYOFF_B_V8_ENVIRONMENT_TO_BIRD_TRANSFER_CONTRACT_20261005.md`.

It does not alter the already frozen V8 primary status:
`V8_BROAD_DEGRADATION = NOT_SUPPORTED`.

## Frozen environmental premise

The V8 environmental analysis showed that source-destination green-up
connectivity strengthened between 2002–2009 and 2010–2017:

- unique-spatial-pair mean delta-rho = **+0.3690**,
  95% bootstrap CI **+0.2984 to +0.4365**;
- equal-species exposure mean delta-rho = **+0.3364**,
  95% dependency-aware bootstrap CI **+0.2628 to +0.4312**.

The mandatory sensitivities kept this change positive under Fisher-z,
complete-window, raw-correlation, alternative-window and leave-one-species-out
coordinates.

## Transfer sample

After applying the prospectively locked bird-outcome eligibility rule:

- species x breeding-target rows: **150**;
- unique environmental spatial pairs: **72**;
- species: **22**.

Mismatch is
`log1p(abs(arrival date - destination green-up date))`.

`delta_mismatch = mismatch_late - mismatch_early`, so negative values denote
improved matching and positive values denote worsened matching.

## T1 — did matching improve at the system level?

Unweighted species-target mean:

- delta-mismatch = **-0.00020**;
- 95% dependency-aware pair-bootstrap CI =
  **-0.07031 to +0.07176**.

Equal-species mean:

- delta-mismatch = **-0.02031**;
- 95% dependency-aware pair-bootstrap CI =
  **-0.09260 to +0.05279**.

Frozen status:

`T1_STRONG_PREDICTABILITY_WITHOUT_MATCHING_PARADOX = NOT_SUPPORTED`

The strong predeclared paradox required a significant *worsening* of mismatch.
That condition is not met. The data instead show no clear system-level change
in mismatch despite the large increase in environmental predictive
connectivity.

Leave-one-species-out stability is directionally consistent with a small
improvement but remains non-conclusive:
- all leave-one-species-out equal-species point estimates are negative;
- range = **-0.03657 to -0.00183**.

This does not license a claim of improved matching because the registered
dependency-aware interval for T1 includes zero.

## T2 — did routes gaining more predictability improve more?

Prospectively locked change-score model:

`delta_mismatch ~ z_delta_rho + z_target_shift_abs + factor(species)`

with two-way cluster-robust uncertainty by species and unique spatial pair.

Coefficient for `z_delta_rho`:

- beta = **+0.06161**;
- cluster-robust SE = **0.03123**;
- 95% CI = **-0.00333 to +0.12655**;
- df = **21**.

Frozen status:

`TRANSFER_NOT_SUPPORTED`

The estimated sign is opposite to the beneficial-transfer prediction:
larger gains in predictive connectivity are estimated to accompany slightly
more positive delta-mismatch, but the cluster-robust interval narrowly includes
zero. Therefore this result must be described as **no evidence that larger
predictability gains produced larger improvements in matching**, not as
evidence that predictability gains causally worsened mismatch.

Leave-one-species-out ordinary point estimates are directionally stable:
- beta range = **+0.05032 to +0.07716**;
- 0 leave-one-species-out coefficients are negative.

This strengthens the statement that the point-estimate direction is not driven
by one species, but it does not override the registered cluster-robust
uncertainty.

## T2 sensitivity — ANCOVA

Prospectively locked ANCOVA:

`mismatch_late ~ mismatch_early + z_delta_rho + z_target_shift_abs + factor(species)`

Coefficient for `z_delta_rho`:

- beta = **+0.03576**;
- cluster-robust SE = **0.02454**;
- 95% CI = **-0.01528 to +0.08679**.

The ANCOVA agrees in sign with the primary change-score transfer model and is
also non-conclusive.

## Joint ecological interpretation

The combined V8 result is:

1. cross-site spring predictive connectivity **increased strongly**;
2. phenological mismatch showed **no clear aggregate improvement or worsening**;
3. the amount by which connectivity increased did **not** predict improved
   matching.

The strongest licensed wording is therefore:

> **Environmental predictability increased without a detectable corresponding
> improvement in migratory phenological matching, and routes gaining more
> predictability did not show greater matching gains.**

This is evidence that **environmental predictive information is not by itself
sufficient to guarantee improved seasonal matching**.

It is not evidence that birds ignored information, failed to perceive cues, or
were physiologically incapable of adjustment. Those stronger mechanisms require
direct measures of cue use and actionability/recourse.

## Relation to the existing cross-sectional result

The existing preregistered pooled 2010–2017 analysis found that higher
pre-outcome predictive connectivity was associated with smaller realized
arrival-green-up mismatch, although conservative dependence-aware intervals
crossed zero.

The two findings answer different questions:

- cross-sectional level: places/times with higher connectivity tend to show
  smaller mismatch in the pooled model;
- longitudinal change: increasing connectivity did not produce detectable
  improvement in matching.

This distinction is compatible with the PAYOFF-B separation between
information availability and the ability to convert information into action.

## Manuscript consequence

The pre-V8 headline

> climate change is degrading the information organisms use to anticipate
> seasonal environments

must be abandoned.

A stronger and better-supported Paper-2 framing is now:

> **Prediction and actionability are distinct constraints on seasonal
> adaptation: environmental predictability can improve without a corresponding
> improvement in phenological matching.**

The V8 result should be used as the macroecological environmental-to-biological
bridge, while the individual mule-deer result supplies the mechanistic
separation between entry timing and downstream recourse.

## Provenance

Environment-to-bird transfer workflow:
- run: **37289823336**
- job: **111697346006**
- artifact: **11336141826**
- artifact SHA256:
  **f3136644fe77f3d35e4a0c41506e7203d905154cc901248b9ad872392e903984**

The analysis was specified in a committed postprimary contract before the
longitudinal bird outcome was opened.
