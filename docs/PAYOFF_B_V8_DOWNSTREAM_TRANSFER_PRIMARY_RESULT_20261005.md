# PAYOFF-B V8 downstream transfer primary result — 2026-10-05

Status: **PRIMARY INFORMATION-TO-TIMING TRANSFER NOT SUPPORTED**

This receipt freezes the post-V8 downstream transfer result defined in
`docs/PAYOFF_B_V8_DOWNSTREAM_TRANSFER_CONTRACT_20261005.md`.

No post-primary transfer sensitivity and no migration-speed-change analysis had
been opened when this primary result was obtained.

## Frozen sample

- source dataset: Amaral et al. BirdMigrationSpeed;
- environmental V8 exposure: already-opened detrended source-destination
  `delta_rho`, 2002–2009 versus 2010–2017;
- bird outcome:
  `log1p(abs(gr_mn - arr_GAM_mean))`;
- required finite bird years per window: >=6;
- eligible species-target-cell rows: **150**;
- eligible unique spatial source-target pairs: **72**;
- eligible species: **22**;
- mean V8 delta-rho among the eligible unique pairs: **+0.4845476**;
- SD of V8 delta-rho among the eligible unique pairs: **0.3667078**.

## Primary result

Equal-species-weighted model:

`delta_mismatch ~ z_delta_rho`

where negative was the preregistered transfer direction.

Observed coefficient:

`beta_transfer = +0.06243969`

Dependency-aware unique-pair bootstrap:

- 10,000 / 10,000 finite replicates;
- seed = 20261005;
- 95% interval = **-0.01411178 to +0.1363489**.

Frozen status:

`INFORMATION_TO_TIMING_TRANSFER = NOT_SUPPORTED`

The point estimate is opposite to the registered negative direction, and the
interval includes zero.

## Frozen prior-magnitude benchmark

The preregistered empirical reference from the 2026-09-26 broad-bird pooled
analysis was:

`beta_prior = -0.0461786181`.

The lower 95% bootstrap bound of the transfer coefficient is -0.01411178,
which is greater than -0.0461786181.

Therefore:

`PRIOR_MAGNITUDE_TRANSFER_EXCLUDED = YES`

Interpretation is deliberately narrow: the present change-on-change estimate is
not compatible, at this interval, with a negative effect as large as the
earlier pooled cross-sectional coefficient. This is not a formal equivalence
test and does not prove zero information use.

## Joint reading with V8 environmental result

The frozen V8 environmental result showed robustly positive change in
source-destination spring predictive connectivity:

- unique-pair mean delta-rho = +0.3690;
- equal-species mean delta-rho = +0.3364;
- 26/28 species means positive.

The downstream primary result does not show the predicted corresponding
reduction in bird arrival–green-up mismatch.

The combined observation is therefore:

> environmental predictive connectivity strengthened strongly, but the
> preregistered route-level transfer from larger connectivity gains to larger
> mismatch reductions was not detected.

This is compatible with, but does not by itself prove, a distinction between
information quality and biological actionability.

## Claim ceiling

Licensed:
- stronger V8 connectivity gains were not associated with larger mismatch
  improvements under the frozen transfer test;
- the point estimate was positive rather than negative;
- a negative change-effect as large as the earlier pooled reference coefficient
  lies outside the primary 95% bootstrap interval.

Not licensed:
- birds ignored the improved information;
- the improved environmental correlation was perceptible as a cue;
- an information deadline caused the lack of transfer;
- downstream control or recourse is the causal bottleneck;
- fitness failed to improve;
- the result generalizes beyond the sampled Amaral system.

## Provenance

Workflow:
- run: 37289801143
- job: 111697274044
- artifact: 11336345852
- artifact SHA256: 046b3221feef75f77be63fcf37ef887101f801c8b1f62e32b41d6bc454466327
