# PAYOFF-B Paper 2 V4 — actionability peak scope correction and natural-evidence boundary

Date: 2026-10-10
Status: **POST-FREEZE MANUSCRIPT ERRATUM AND GENERALIZATION, NOT A NEW EMPIRICAL FINDING**.
The science-frozen V3 text and the original canonical code/theorem on main are unchanged. The revised V4 on draft PR #320 corrects a statement that omitted the canonical boundary condition.

## Problem identified in the V4 integrated manuscript

V4 section 2.1 originally displayed

    q(t)=q0+Delta_q*(1-exp(-alpha*t)),
    r(t)=exp(-beta*t),
    t*=log(1+alpha/beta)/alpha

as though the optimal time were independent of *q0*, Delta_q, loss scale S and threshold B. That general reading is **false**. The main original source, theory/ACTIONABILITY_BALANCE_THEOREM.md, already specifies q0=B/S, so its theorem remains exactly correct. The V4 restatement omitted this critical hypothesis; it should not be used to extrapolate timing optima across taxa with different prior cues.

## Correct general zero-direct-cost derivation

Assume t >= 0, alpha,beta,S,Delta_q > 0,
0.5<=q_start, q_start+Delta_q<=1, S/2<=B<=S.
Here q is the accuracy of an invertible symmetric binary cue; q<0.5
would be better handled by flipping cue labels, NOT automatically
called low information value. In the Paper-2 canonical loss,
B=max(A,L) and S=A+L, which guarantees B/S>=0.5.
Let q_c=B/S, and let nonnegative incremental information value
be [S*q(t)-B]_+ (zero if that signal is unusable).

    N(t)=exp(-beta*t)*[S*(q_start+Delta_q*(1-exp(-alpha*t)))-B]_+.

In the positive-valued region write

    A = S*(q_start+Delta_q) - B,
    H = S*Delta_q.

Then N(t)=exp(-beta*t)*(A-H*exp(-alpha*t)), and

    N'(t) = exp(-beta*t) *
            ((alpha+beta)*H*exp(-alpha*t) - beta*A).

If A<=0, even the asymptotic cue fails to cross the threshold;
there is no positive-valued information-using decision. With a
zero-payoff abstain option, classify as NEVER_ACTIONABLE; do not
invent a negative biological fitness optimum.

If A>0, the stationary candidate is

    tcrit = [log(H/A)+log(1+alpha/beta)]/alpha,

and the maximizing action time is

    tstar = max(0, tcrit).

The canonical formula follows **only if** q_start=B/S, since
A=H. The limiting case q_start>B/S can yield a strictly earlier
interior optimum or immediate commitment.

If the cue starts below threshold and eventually crosses it, the
threshold-crossing time is

    t_cross = log(H/A)/alpha > 0,

and

    tstar = t_cross + log(1+alpha/beta)/alpha.

This is the biologically pertinent result: an uninformative cue
must first become useful and *then* face the information/optionality
trade-off. Two migrants with different initial cue usefulness can
choose different commitment times even under the same alpha/beta.

## Deterministic illustrative witnesses, not fitted biological parameters

All examples set S=1.6, B=1.2 (q_c=0.75), alpha=beta=1 and are exact zero-cost
source-free toy calculations.

| Initial q | Delta q | Limiting q | Expected result |
|---:|---:|---:|---|
| 0.75 | 0.20 | 0.95 | canonical t*=ln2=0.6931 |
| 0.60 | 0.35 | 0.95 | threshold t_c=ln1.75=0.5596; optimum t*=ln3.5=1.2528 |
| 0.80 | 0.15 | 0.95 | cue already useful: t*=ln1.5=0.4055 |
| 0.95 | 0.025 | 0.975 | t*=0 (immediate use), rather than ln2 |
| 0.55 | 0.15 | 0.70 | never useful, despite cue improvement |

The original symmetric special case q_start=q_c=0.5,
Delta_q=0.5, S=2, B=1 gives q(tstar)=0.75 at tstar=ln2,
unchanged; the non-symmetric-prior table instead uses q_c=0.75.
This explicit separation prevents labeling an accuracy below 50%
(which is invertible) as insufficient environmental information.

## Source code and tests

- New source-only decision calculus: src/general_exponential_actionability.py.
- New ten-test regression suite:
  tests/test_general_exponential_actionability.py.
- Tests cover the canonical result, crossing-time shift, already useful
  cues, immediate action, never-usable cues, dense numerical
  maximization, faster expiry, invalid parameters, and regression
  checks preventing the canonical formula being incorrectly used in
  noncanonical settings.
- This is **new software to validate a manuscript's generalization**,
  not a new theorem, empirical payoff fit or taxa-level claim.
- General dynamic information acquisition and optimal stopping theory
  predate PAYOFF-B (e.g., Zhong 2022, Econometrica,
  doi:10.3982/ECTA17787). A familiar analytic optimum should not be
  advertised as independent high-impact novelty.

## Ecological claim boundary

q_start, S, B, beta and Delta_q are **theoretical decision quantities**.
Neither Amaral V8 environmental correlations (166 pairs) nor the
Schindler goose, Burnside houbara or Rüppel radio-telemetry panels
measure all these parameters at the individual's true information
decision point. The threshold crossing t_c is not empirically
identified by correlation shifts or start/end weather.

The result strengthens a **falsifiable modeling distinction**—initial
information distance to actionability matters, separately from the
speed of information accumulation and the speed of losing recourse.
It does not show that a particular migrant waits until t_c, learns
the destination spring, or rationally fails to respond.

## Other V4 source-integrity corrections accompanying this erratum

- Original Rüppel telemetry has **178 uniquely paired bird flights**
  and **178 status=1 departure events**. The exact event/flight date
  difference is zero in 175 records and one day in 3 records;
  the earlier V4 description 'three unmatched' was incomplete.
- The variance-funnel identification statement is now restricted
  to the declared Gaussian cue/action assumptions, independently
  known passive retention and process variance, and nonzero
  correction×information product. The source-only goose calendar
  example demonstrates that variance contraction is not uniquely
  identifiable as feedback.

## No retroactive outcome changes

The registered V8 correlation-change→bird mismatch test remains
NOT_SUPPORTED. Existing frozen V3 and earlier evidence receipts are
unmodified. This erratum is a transparent post-freeze refinement of
the candidate V4 integrative manuscript, not a new preregistration
or an attempt to rescue previously negative natural tests.
