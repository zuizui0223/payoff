# PAYOFF-B V8 environment-to-bird transfer contract — 2026-10-05

Status: **POSTPRIMARY PROSPECTIVE SECONDARY; WRITTEN BEFORE THIS LONGITUDINAL BIRD-OUTCOME ANALYSIS IS OPENED**

The V8 environmental primary is already frozen and opened. It showed a robust
positive change in source-destination green-up coupling, not the preregistered
degradation. This contract does not redefine V8 and cannot alter
`V8_BROAD_DEGRADATION = NOT_SUPPORTED`.

The new question is narrower:

> When source-destination environmental predictability increased, did bird
> timing become better matched to destination spring along the same sampled
> mappings?

This is a secondary environment-to-bird transfer test motivated by the opened
environmental result.

## Frozen inputs

Use the same Amaral source commit:

`62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`

Use the exact V8 source-target mapping and the exact finite primary
source-target-pair `delta_rho` values.

Windows remain:
- EARLY: 2002–2009;
- LATE: 2010–2017.

No alternative route mapping, window, green-up definition, or V8 predictor is
selected after outcome access.

## Biological unit and outcome eligibility

The biological row is one frozen species × breeding-target-cell mapping.

A row is eligible only if:
1. its environmental spatial pair is in the finite V8 primary sample;
2. at least 6 years in EARLY have finite `arr_GAM_mean` and `gr_mn`;
3. at least 6 years in LATE have finite `arr_GAM_mean` and `gr_mn`.

Eligibility uses only missingness/counts, not the size or sign of mismatch.

## Mismatch outcome

For each eligible species-target-year define:

`mismatch = log1p(abs(arr_GAM_mean - gr_mn))`.

For each species-target row compute:
- `mismatch_early`: mean mismatch in EARLY;
- `mismatch_late`: mean mismatch in LATE;
- `delta_mismatch = mismatch_late - mismatch_early`.

Thus:
- negative delta-mismatch = improved phenological matching;
- positive delta-mismatch = worsened phenological matching.

Also calculate the target's secular shift magnitude:

`target_shift_abs = abs(mean(gr_mn_late) - mean(gr_mn_early))`.

This is a control for how far the destination seasonal target moved between
periods. Bird migration speed is not controlled because it can be a downstream
recourse mechanism rather than a baseline confounder.

## T1 — system-level mismatch change

Report:
1. the unweighted species-target mean `delta_mismatch`;
2. the equal-species mean `delta_mismatch`.

Uncertainty is obtained by 10,000 resamples of unique V8 spatial pairs with
seed 20261005, carrying all species-target incidences of each sampled pair into
the replicate.

A **strong predictability-without-matching paradox** is licensed only if:
- the already-frozen V8 environmental change remains positive; and
- the equal-species mean `delta_mismatch > 0`; and
- its 95% dependency-aware pair-bootstrap interval is entirely above zero.

If the interval crosses zero, the result is described as no clear system-level
mismatch improvement/worsening, not as proof of no biological response.

## T2 — transfer gradient

Primary secondary model:

`delta_mismatch ~ z_delta_rho + z_target_shift_abs + factor(species)`.

Here `z_delta_rho` and `z_target_shift_abs` are standardized over eligible
species-target rows.

Inference for the `z_delta_rho` coefficient uses a two-way cluster-robust
covariance with clusters:
- species;
- unique spatial source-target pair.

The 95% interval uses df = min(number of species clusters,
number of pair clusters) - 1.

**TRANSFER_SUPPORTED** requires:
- coefficient on `z_delta_rho < 0`; and
- its two-way cluster-robust 95% interval lies entirely below zero.

Otherwise:
`TRANSFER_NOT_SUPPORTED`.

A non-significant coefficient is not interpreted as proof of zero transfer.

## T2 sensitivity — ANCOVA form

Fit:

`mismatch_late ~ mismatch_early + z_delta_rho + z_target_shift_abs + factor(species)`

with the same two-way cluster-robust covariance.

This is a robustness coordinate against change-score regression-to-the-mean.
It does not replace T2. Report whether the `z_delta_rho` sign agrees with T2
and its interval.

## T3 — leave-one-species-out

Repeat the T1 equal-species point estimate and the T2 ordinary coefficient
after omitting each species in turn. Report the ranges and sign stability.

This is a stability diagnostic, not a route for rescuing a failed T1 or T2.

## Interpretation matrix

- T1 worsens + T2 not supported:
  licensed wording is that environmental predictability increased while
  phenological matching worsened at the sampled system level, with no evidence
  that routes gaining more predictability improved more. This supports a
  predictability-is-not-sufficient framing, not a claim that birds ignored
  available cues.

- T1 worsens + T2 supported:
  predictability gains are associated with local improvement, but other
  contemporaneous forces dominate the aggregate mismatch trend.

- T1 improves + T2 supported:
  increased predictive connectivity is consistent with successful transfer
  into improved matching.

- T1 improves + T2 not supported:
  mismatch improved, but the improvement cannot be attributed to the measured
  connectivity gain.

## Claim boundary

No result from this analysis alone establishes:
- that birds directly perceive source-site green-up;
- that the V8 correlation is the cue birds actually use;
- causal effects of climate change;
- fitness consequences;
- population decline;
- a universal result for migratory taxa.

The already-frozen pooled 2010–2017 predictive-connectivity analysis remains a
separate piece of evidence and is not used to choose or modify this contract.
