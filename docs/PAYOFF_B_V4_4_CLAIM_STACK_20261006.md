# PAYOFF-B V4.4 claim stack — 2026-10-06

Status: **CURRENT JOURNAL-FACING CLAIM BOUNDARY**

## Central ecological question

**What determines whether environmental forecast opportunity becomes
phenological adjustment?**

## Central synthesis

Seasonal tracking contains separable stages:

1. environmental conditions carry information about a future seasonal target;
2. that information has a decision-scale forecast value;
3. the signal must be temporally and biologically accessible;
4. the organism must retain actions capable of altering timing;
5. residual phase error can then be corrected or retained.

The paper distinguishes:
- standardized environmental coupling;
- marginal forecast value;
- temporal availability;
- organismal access and cue use;
- correction opportunity;
- realized timing adjustment.

These quantities are not interchangeable.

## Claim 1 — standardized source-destination coupling strengthened

Evidence class:
**preregistered environmental primary result**

Licensed:

> In the sampled eastern North American bird system, detrended
> source-destination spring correlation increased from 0.284 to 0.653 between
> 2002–2009 and 2010–2017.

Robustness:
- pair bootstrap;
- source-cell clustering;
- target-cell clustering;
- two-way source-target dependence;
- 5-degree and 10-degree spatial blocks;
- leave-one-calendar-year-out;
- remote-sensing support diagnostic.

Not licensed:
- climate change caused the increase;
- spatial synchrony increase is novel by itself;
- higher rho alone means lower absolute prediction error.

## Claim 2 — destination spring became more variable

Evidence class:
**posthoc metric-scale diagnostic**

Licensed:

> Detrended target green-up SD increased from 2.41 to 4.66 d.

Not licensed:
- a monotonic long-term climate trend;
- anthropogenic attribution.

## Claim 3 — the reconstructed nonlocal signal gained forecast value

Evidence class:
**posthoc cross-validated forecast diagnostic**

Primary definition:

    G_CV
      =
    MSE(target-history baseline)
      -
    MSE(source-informed forecast).

Current trend-baseline result:
- early pair mean = -16.1 d^2;
- late pair mean = +16.0 d^2;
- delta = +32.1 d^2;
- median delta = +15.84 d^2;
- 10% trimmed mean = +20.87 d^2;
- 139/166 pairs positive.

Equal-species:
- delta = +20.87 d^2;
- 25/28 species positive;
- 95% CI +16.37 to +32.48 d^2.

Exact 8/8-year subset:
- delta = +28.30 d^2;
- all dependence-aware intervals positive;
- 16/16 global calendar-year omissions positive with intervals above zero.

Alternative climatological-mean baseline:
- delta = +22.37 d^2;
- 136/166 pairs positive;
- equal-species delta = +21.30 d^2;
- 24/28 species positive.

Licensed:

> The marginal held-out predictive value of adding the reconstructed nonlocal
> environmental signal increased strongly between periods.

Preferred journal wording:
**forecast-value proxy** or **marginal predictive value**.

Not licensed:
- organismal fitness value of information;
- a baseline-free intrinsic cue value;
- bird perception or use of the source signal.

## Claim 4 — the environmental signal was temporally leading

Evidence class:
**posthoc temporal-order diagnostics**

Source versus target green-up:
- grand pair-mean source lead = about 13.4 d;
- 158/166 pairs positive in both windows;
- 127/166 source earlier in every observed paired year.

Source versus bird arrival in the admitted bird sample:
- 140 species-target rows;
- 69 unique pairs;
- 22 species;
- pair-mean lead = 5.47 -> 7.95 d;
- change = +2.48 d;
- 95% CI +1.91 to +3.05 d;
- all source/target/5-degree/10-degree intervals positive;
- equal-species change = +2.37 d;
- 21/22 species positive.

The wider source-to-arrival lead arose primarily because source green-up
advanced:
- source green-up shift = -2.86 d;
- arrival shift = -0.38 d in the temporal-window subset.

Licensed:

> The reconstructed signal was temporally leading and became earlier relative
> to target arrival on average.

Not licensed:
- birds actually passed through or observed the source cell;
- source-to-arrival lead is direct actionability r(t);
- the lead interval equals available correction time.

## Claim 5 — population arrival changed little while target green-up advanced

Evidence class:
**posthoc signed-timing diagnostic**

Frozen transfer sample:
- 150 species-target rows;
- 72 unique pairs;
- 22 species.

Target green-up:
- 130.98 -> 128.67;
- change = -2.31 d;
- 95% CI -2.58 to -2.08 d.

Estimated bird arrival:
- 123.17 -> 122.98;
- change = -0.19 d;
- 95% CI -0.95 to +0.52 d.

Signed lag = arrival - target green-up:
- -7.81 -> -5.69 d;
- change = +2.12 d;
- 95% CI +1.41 to +2.77 d.

Equal-species signed change:
- +2.14 d;
- 95% CI +1.32 to +2.92 d.

Direction:
- 20/22 species positive;
- 57/72 pairs positive.

Licensed:

> Target green-up advanced by about 2.3 d while the estimated bird arrival
> front changed little, shifting signed relative arrival by about 2.1 d.

Interpretation:
birds became less early relative to mid-green-up.

Do not call this automatically:
- improvement;
- deterioration;
- fitness loss.

Zero arrival-minus-mid-green-up is not established as the fitness optimum.

## Claim 6 — absolute mismatch stability is not evidence of active tracking

Evidence class:
**posthoc signed decomposition + frozen structural null logic**

Absolute distance:
- unweighted 8.42 -> 8.07 d;
- change -0.35 d; CI spans zero;
- equal-species change -0.63 d; posthoc interval below zero.

But birds were several days earlier than mid-green-up in both periods.
The target advanced toward a largely unchanged arrival schedule.

Licensed:

> The modest stability or decline of the absolute arrival–green-up gap does not
> demonstrate active timing adjustment.

This replaces the older wording:
> tracking was maintained / mismatch did not deteriorate.

## Claim 7 — gains in forecast value did not transfer detectably to bird timing

Evidence class:
**posthoc transfer diagnostic + structural nulls**

Day-scale raw coefficient:
- +2.43 d mismatch change per SD delta G_CV;
- CI +0.35 to +3.65 d.

Fixed-arrival null:
- +2.98 d.

Observed-minus-null bird increment:
- -0.56 d;
- CI -2.39 to +0.55 d.

Within-window arrival permutation:
- observed positive slope ordinary under null.

Licensed:

> Larger route-level gains in environmental forecast value did not produce a
> detectable bird-specific improvement beyond shared environmental geometry.

Not licensed:
- forecast value worsened bird timing;
- birds ignored the signal;
- perception failure, actuator limitation or actionability loss is identified.

## Claim 8 — population timing is transformed across mapped migration stages

Evidence class:
**posthoc restricted-subset stagewise diagnostic**

Restricted sample:
- 31 unique source-target pairs;
- 14 species;
- source-target population-front lead: 7.20 -> 5.69 d;
- change = -1.51 d, 95% CI -2.32 to -0.70 d;
- source-target green-up interval changed little;
- phase transformation: -3.57 -> -4.95 d;
- change = -1.37 d, 95% CI -2.36 to -0.36 d;
- 23/31 pairs and 12/14 species became more negative.

Generalization boundary:
- stagewise subset mean source-target distance = 495 km versus 911 km outside;
- late rho = 0.847 versus 0.608 outside;
- delta G_CV = +26.61 d^2 versus +33.34 d^2 outside (SMD -0.08).

Measurement boundary:
- source arrival posterior SD: about 2.89 -> 0.91 d;
- target arrival posterior SD: about 2.85 -> 0.93 d;
- posterior-normal uncertainty propagation retained a negative mean change in
  all 5,000 simulations;
- inverse-variance reweighting retained a negative point estimate but the
  bootstrap interval crossed zero.

Licensed:

> In the restricted same-species stage subset, population-level relative timing
> changed between mapped source and target stages rather than being passively
> retained, but the magnitude is sensitive to observation-precision weighting.

Not licensed:
- individual feedback correction;
- controller gain or actionability;
- full-network generalization;
- measurement-error invariance.

Role:
**same-system supporting bridge**, not headline evidence.

## Claim 9 — downstream signed correction exists in a natural seasonal trajectory

Evidence class:
**published prior art + source-data reanalysis in mule deer**

Licensed:
- start phase predicts movement speed and stopover use;
- early and late individuals adjust in opposite directions;
- phase variance contracts strongly from migration start to end;
- mean absolute phase error declines.

Not licensed:
- discovery of mule-deer resynchronization;
- direct identification of G(t), r(t), internal belief or control gain;
- proof that the same mechanism explains the bird pattern.

## Claim 10 — usable information depends on forecast value and correction opportunity

Evidence class:
**exact reduced-model specialization**

General reduced form:

    N(t) = r(t) G(t) - C(t).

Interior condition:

    r G' = -r' G + C'.

The multiplicative rG term is a declared scalar specialization, not a universal
identity for arbitrary action sets.

Exponential special case:

    t* = log(1 + alpha/beta) / alpha.

Licensed:

> In the declared reduced model, increasing forecast value and declining
> correction opportunity can create an intermediate stage of maximal usable
> information.

Not licensed:
- a new general value-of-information theorem;
- a natural estimate of t* from the current systems.

## Submission headline

Preferred:

> **Seasonal tracking depends on information value and opportunities for
> correction.**

One-sentence contribution:

> **Environmental forecast opportunity increased while population arrival
> adjustment remained limited; seasonal tracking therefore requires converting
> environmental information into biological correction.**

## What the paper is not

Do not sell the paper as:
- discovery of increasing spatial synchrony;
- discovery that variability changes information value;
- discovery of feedforward versus feedback control;
- proof that birds use the reconstructed nonlocal signal;
- proof that actionability loss caused the bird pattern.

The contribution is the source-backed separation of environmental forecast
opportunity from realized phenological adjustment, embedded in a sequential
forecast-to-correction framework.
