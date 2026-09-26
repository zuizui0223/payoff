# PAYOFF-B Tomotani information-history contract

Frozen: **2026-09-26**  
Status: **PREOUTCOME — source archive requires owner-approved access**

## Why this lane matters

The 1980–2015 Dutch pied-flycatcher series is currently the strongest
within-species candidate for testing whether seasonal timing follows different
paths while an information relationship deteriorates and later recovers.

The published paper already reports a nonlinear male arrival-to-breeding
interval: it shortened until roughly 2008 and increased afterwards. That
published reversal is precisely why PAYOFF-B must **not** choose 2008 as its
breakpoint.

The information history has to define the regimes independently.

## Order of operations

1. Reconstruct the annual African pre-/en-route temperature cue and Dutch spring
   temperature state using the archived, source-defined variables.
2. For each focal year, estimate signed predictive connectivity from the
   preceding eight years only.
3. Detect at most one information breakpoint using **only** this connectivity
   series.
4. Require a real reversal: segmented fit must improve AICc by at least 4,
   pre- and post-break slopes must have opposite signs, and at least half of the
   connectivity decline must be recovered by the end of the series.
5. Only after these gates pass, open the annual arrival-to-breeding interval.

The published 2008 timing reversal is an external comparison, never an input to
steps 1–4.

## Primary path-dependence test

If an information reversal exists, classify years as the degradation arm or the
recovery arm based only on the connectivity breakpoint.

Fit:

    arrival_to_breeding_interval
      ~ connectivity
      + regime_direction
      + connectivity:regime_direction.

The primary hysteresis estimand is the interaction. A path-dependence claim
requires its 95% interval to exclude zero and the two arms to predict different
timing intervals over their overlapping connectivity support.

A stronger ecological-memory claim additionally requires at least a 2-day
difference at matched connectivity with a 95% interval excluding zero.

If the information series does not pass the reversal gate, the result is
`NO_INFORMATION_REVERSAL`. We do not search for another breakpoint.

## Data-access boundary

The official Marine Data Archive landing page identifies the archived file as
`Tomotani et al.zip`, but anonymous download is not permitted; access requires a
project login or owner-approved request.

Therefore this contract is frozen **before archive bytes are available**.

No result is currently claimed from this lane.
