# PAYOFF-B calendar-duration phase-retention sensitivity

Created: **2026-09-25**

Status: **retrospective diagnostic; not prospective evidence**.

## Question

The direct GEB systems estimate

```text
E_next = a + lambda E_current + ...
```

over ecological intervals of very different duration.

The primary interval-standardization amendment therefore reports descriptive
`k_eq=-ln|lambda|/Delta t_ref` and cumulative retained memory. This diagnostic
asks a stricter question:

> Does the original observation-level data actually support a single monotone
> calendar-time decay law, `lambda_i = exp(-k Delta t_i)`?

If yes, per-day `k` would have a stronger interpretation. If no, `lambda`
should remain a segment/correction-opportunity estimand and the descriptive
`k_eq` must not be promoted as a biological rate.

## Competing models

The frozen primary form is reproduced as

```text
E_next = Z gamma + lambda E_current + error
```

and compared with

```text
E_next = Z gamma + exp(-k Delta t) E_current + error.
```

Both models have the same number of fitted parameters.

Two nuisance specifications are evaluated:

1. the exact nuisance structure of the original segment model;
2. the same structure plus standardized log interval duration in both models.

The comparison statistic is the Gaussian AIC difference with equal parameter
counts,

```text
Delta AIC = n log(SSE_duration / SSE_segment).
```

Positive values favour segment retention; negative values favour calendar-time
decay.

The classification rule is deliberately conservative:

```text
both Delta AIC >= +2  -> SEGMENT_RETENTION_PREFERRED
both Delta AIC <= -2  -> CALENDAR_DURATION_DECAY_SUPPORTED
otherwise             -> SPECIFICATION_SENSITIVE_OR_INCONCLUSIVE
```

## Declared boundary

Svalbard's negative lambda is a sign-reversal/overshoot result. A monotone
`exp(-k Delta t)` coefficient is always positive, so Svalbard is declared
**not representable by this model** rather than forced into an absolute-value
fit.

## Evidence status

This diagnostic was designed after the direct lambda results were already
known and after interval scale was raised as a manuscript concern. It can
therefore narrow or block a cross-system interpretation, but it cannot be
counted as a new prospective confirmation.

The Aikens fixed-24 h outcome remains unopened and is not modified by this
analysis.
