# PAYOFF-B racing bridge — status ledger

Date: **2026-10-07**  
Branch: \`analysis/payoff-b-competitive-information-value-20261007\`  
Draft PR: **#307**

## Decision

### Standalone horse-racing novelty route: CLOSED

Do not write a horse-racing paper whose main claim is any of the following:

- public information is incorporated into betting odds;
- useful forecast information loses value as the market learns it;
- odds paths contain information not captured by a final price;
- late informed wagering changes final pari-mutuel odds;
- a fundamental forecast can be combined with market probabilities.

These are occupied by established betting-market / forecasting literature.

The strongest direct collision is Green et al. (2019), who use horse-racing
market prices over eighteen years to quantify the value and diffusion of novel
forecast information. Benter-style work already occupies the basic
fundamental-model + public-odds combination architecture. Recent Japanese work
also occupies last-minute pari-mutuel information dynamics.

## PAYOFF result that survives

The useful conceptual extension is the distinction between:

- \(r(t)\): retained biological / physical actionability;
- \(e(t)\): retained differential-information value.

The declared reduced form is

\[
N(t)=r(t)e(t)V_A(q(t))-C(t).
\]

Define

\[
u(t)=r(t)e(t).
\]

Then

\[
N(t)=u(t)V_A(q(t))-C(t).
\]

Therefore the value trajectory identifies only \(u(t)\), not \(r(t)\) and
\(e(t)\) separately.

This is the main payoff of the racing comparison:

> **an information-value hump does not by itself identify biological recourse
> loss.**

The ecological interpretation now requires an independent measurement of
actionability / recourse rather than inferring it from the timing of information
use.

Under exponential decay,

\[
r(t)=e^{-\beta t},
\qquad
e(t)=e^{-\gamma t},
\]

only \(\beta+\gamma\) enters the timing optimum.

## Racing role that remains

Horse racing is retained only as an **optional external mechanism-separation
boundary case**:

- physical actionability remains approximately available until a sharp cutoff;
- collective market information changes through time;
- usable relative information can therefore decay mainly through diffusion.

This is useful for explanation, teaching, a negative control, or a cross-system
demonstration. It is not required for the biological PAYOFF claim.

## Optional empirical pipeline completed

The branch contains a source-to-result retrospective JRA-VAN/JV-Link pipeline:

1. normalized JV-Link four-table source contract;
2. source-faithful handoff validator;
3. outcome-blind 70/30 chronological date split;
4. retrospective fixed TM category-7 forecast;
5. T-30, T-15, T-10, T-5, LAST time-slice selection;
6. 10-minute snapshot freshness rule, including LAST;
7. explicit exclusion of dead heats / non-single-winner races;
8. valid support for decimal odds down to 1.0;
9. training-only TM-score probability calibration;
10. contemporaneous market probability normalization;
11. training-only log-opinion-pool weights;
12. untouched test proper-score comparisons;
13. paired race-level bootstrap for held-out P1/P3 contrasts;
14. one-command end-to-end primary runner.

No betting-profit optimization is included.

## External source boundary

Retrospective primary:

- MING/TM accumulated category 7 = stored final pre-race mining forecast;
- time-series win odds from the O1 / time-series feed;
- use the officially guaranteed provision window as the primary source window.

Realtime category 1/2/3 mining forecasts can only form a cleaner prospective
extension if archived at receipt time before later versions overwrite earlier
ones.

## Current blocker

The repository does not contain a user's local JRA-VAN Data Lab / JV-Link
subscription or extracted records.

Issue **#308** is therefore an **optional validation issue**, not a priority
blocker for PAYOFF-B.

## Priority recommendation

Do **not** spend additional research effort on racing before the biological
identification problem advances.

The next higher-value PAYOFF-B task is to find or derive a natural ecological
system in which the following can be measured separately:

\[
q(t)
=
\text{predictive quality of information available at stage }t,
\]

and

\[
r(t)
=
\text{retained capacity to alter the fitness-relevant action at stage }t.
\]

That direct \(q(t)\)–\(r(t)\) identification would test the biological mechanism
that racing cannot establish.

## Merge recommendation

Keep PR #307 as a draft until deciding whether the **mechanism-aliasing warning**
belongs in the general prospective theory layer.

If merged later, merge it for that identification warning and reusable
validation code — **not** as a horse-racing empirical claim.
