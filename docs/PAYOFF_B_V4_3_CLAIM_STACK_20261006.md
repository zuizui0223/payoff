# PAYOFF-B V4.3 claim stack — 2026-10-06

Status: **JOURNAL-FACING CLAIM BOUNDARY**

## Central ecological question

How can seasonal tracking be maintained as the local seasonal environment
becomes more variable?

## Central synthesis

Seasonal tracking has two sequential control problems:

1. reduce uncertainty about a future seasonal target before or during
   commitment;
2. correct residual timing error afterward while useful response opportunities
   remain.

The paper distinguishes:
- standardized environmental coupling;
- decision-scale environmental forecast value;
- retained correction opportunity;
- realized phase correction.

These quantities are not interchangeable.

## Claim 1 — standardized source-destination coupling strengthened

Evidence class:
**preregistered environmental primary result**

Licensed:

> In the sampled eastern North American bird system, detrended
> source-destination spring correlation increased from 0.284 to 0.653 between
> 2002–2009 and 2010–2017.

Robustness:
- source-cell clustering;
- target-cell clustering;
- two-way source-target dependence;
- 5-degree and 10-degree spatial blocks;
- leave-one-calendar-year-out;
- remote-sensing support diagnostic.

Not licensed:
- climate change caused the increase;
- spatial synchrony increase is novel in itself;
- higher rho alone means lower absolute prediction error.

## Claim 2 — destination seasonal variability increased

Evidence class:
**posthoc metric-scale diagnostic**

Licensed:

> Detrended destination green-up SD increased from 2.41 to 4.66 d.

Not licensed:
- a long-term monotonic trend;
- anthropogenic attribution.

## Claim 3 — marginal forecast value of nonlocal information increased

Evidence class:
**posthoc cross-validated diagnostic**

Definition:

    G_CV = MSE(target-history baseline) - MSE(source-informed forecast).

Primary target-history baseline:
linear trend fitted without the held-out year.

Current result:
- pair mean: -16.1 -> +16.0 d^2;
- delta: +32.1 d^2;
- median delta: +15.84 d^2;
- 10% trimmed mean: +20.87 d^2;
- 139/166 pairs positive;
- equal-species delta: +20.87 d^2;
- 25/28 species positive;
- exact 8/8-year subset delta: +28.30 d^2;
- 16/16 calendar-year omissions positive with intervals above zero.

Licensed:

> The marginal out-of-sample forecast value of adding the frozen nonlocal
> source signal increased strongly between periods.

Not licensed:
- organismal fitness value of information;
- birds perceived or used this source signal;
- source information caused realized tracking.

Pending robustness:
- alternative climatological-mean baseline.

## Claim 4 — source-informed absolute forecast error did not deteriorate

Evidence class:
**posthoc cross-validation**

Licensed:

> Source-informed leave-one-year-out RMSE was approximately unchanged
> (4.11 -> 4.17 d) while the target-history-only RMSE increased strongly
> (3.18 -> 5.86 d).

Interpretation:

> Increased nonlocal forecast value offset much of the increased difficulty
> created by rising destination variability in this environmental prediction
> problem.

Not licensed:
- a bird behavioral buffering response.

## Claim 5 — realized bird mismatch did not show corresponding deterioration

Evidence class:
**frozen transfer sample + posthoc day-scale sensitivity**

Current result:
- unweighted absolute mismatch: 8.42 -> 8.07 d; interval spans zero;
- equal-species absolute change: -0.63 d; posthoc interval below zero;
- frozen log-mismatch change: unresolved around zero.

Licensed:

> Arrival-green-up mismatch showed no corresponding deterioration in the
> admitted bird sample.

Prefer this wording over:
> mismatch improved.

Not licensed:
- stable mismatch was caused by nonlocal information;
- actionability or downstream correction buffered the birds.

Pending diagnostic:
- posthoc delta-G_CV to mismatch-change transfer with structural nulls.

## Claim 6 — downstream signed correction exists in a natural seasonal trajectory

Evidence class:
**published prior art + source-data reanalysis in mule deer**

Licensed:
- signed start phase predicts movement speed and stopover use;
- early and late individuals adjust in opposite directions;
- phase variance contracts strongly from migration start to end;
- mean absolute phase error declines.

Not licensed:
- PAYOFF-B discovered mule-deer resynchronization;
- the mule-deer system identifies bird mechanisms;
- internal belief, r(t), G(t), or control gain are directly measured.

## Claim 7 — information value and actionability can peak at different stages

Evidence class:
**exact reduced-model result**

General reduced form:

    N(t) = r(t) G(t) - C(t).

Interior balance:

    r G' = -r' G + C'.

The multiplicative form is a scalar specialization, not a theorem for arbitrary
action sets.

Existing exponential special case:

    t* = log(1 + alpha/beta) / alpha.

Licensed:

> In the declared reduced model, increasing decision-scale information value
> and declining actionability can produce an intermediate stage of maximal
> usable information.

Not licensed:
- natural estimates of t*;
- a new general theorem of value of information or optimal stopping.

## Claim 8 — forecast and correction are distinct routes to seasonal precision

Evidence class:
**mechanistic synthesis + exact phase-state model + independent natural anchors**

Licensed:

> Upstream forecasting can reduce the error entering a seasonal trajectory,
> whereas downstream feedback can alter residual error after commitment and
> respond to new error generated later.

This is a seasonal specialization of established feedforward/feedback logic,
not a claim that the distinction itself is new.

## Submission headline

Preferred:

> **Seasonal tracking depends on information value and opportunities for
> correction.**

The paper should not be sold as:
- discovery of increasing spatial synchrony;
- discovery that variability changes information value;
- discovery of feedforward versus feedback;
- proof that birds use the reconstructed nonlocal cue.

Its contribution is the empirically anchored separation of forecast value,
residual uncertainty and correction opportunity within one seasonal-tracking
framework.
