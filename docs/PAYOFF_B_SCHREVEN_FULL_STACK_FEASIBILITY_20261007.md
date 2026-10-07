# PAYOFF-B Schreven full-stack feasibility audit

Date: **2026-10-07**
Status: **PROSPECTIVE FEASIBILITY; V4.5 CLAIMS FROZEN**

## Why this branch exists

The frozen V4.5 manuscript ends with one decisive empirical requirement:
measure environmental forecastability, organismal information access, retained
actionability, behavioral response and phase outcome in the same natural
seasonal trajectory.

The current V4.5 bird system identifies environmental forecastability and some
population-level timing geometry, but it does not directly identify the cue
encountered by an individual, organismal information value G_O, retained
actionability r, or individual downstream correction.

The Schreven et al. pink-footed-goose system is screened here as a candidate
for narrowing that same-system gap.

## Already-known outcomes

Published aggregate outcomes are known before any row-level reanalysis here.

Known results include:

- route-stage spring predictability differs among migration steps;
- the recent Trondelag to Svalbard GDD relationship is significantly negative;
- mainland steps generally retain positive predictability;
- Novaya Zemlya arrival is associated with local GDD spring;
- GPS-tracked breeding populations differ in stopover duration, especially in
  Jutland;
- route-specific timing differences occur at Jutland, Orebro and Oulu.

Therefore this branch does not claim discovery of sign reversal, route
differences, or cue unreliability. It asks whether multiple PAYOFF interfaces
can be reconstructed on one individual route-stage coordinate.

## Candidate same-system layers

### External forecastability G_E

For a declared route step s to s+1, estimate the signed source-to-target spring
relationship and, if replication permits, held-out reduction in prediction
loss.

Negative slopes remain negative. They are not folded into unsigned cue quality.

### Individual exposure opportunity

For individual i, year y and source stage s, let source residence be

    [arrival_isy, departure_isy].

For source environmental event date E_sy define

    O_isy = 1{arrival_isy <= E_sy <= departure_isy}.

O=1 means only that the event occurred while the tracked individual was
present. It does not prove perception or use.

This is a direct improvement over the V4.5 population-front observability
audit, which cannot establish individual passage through the reconstructed
source stage.

### Enacted timing response

For stages with sufficient replication, evaluate departure or progression
timing against local seasonal state while accounting for arrival timing,
individual identity, route/stage and year structure.

A departure response is enacted behavior, not G_O itself. Local spring can
affect local foraging directly, so a response cannot automatically be called
forecast use.

### Temporal-flexibility proxy

Observed stopover duration is

    T_isy = departure_isy - arrival_isy.

Published GPS summaries show strong stage-specific variation, including a
large Svalbard-versus-Novaya-Zemlya difference in Jutland and almost no
difference in Oulu.

But:

    T_isy != r_isy.

Observed duration is realized behavior, not the counterfactual feasible action
set. The branch therefore uses temporal-slack / compressibility-proxy language
only.

### Downstream signed phase

At each stage define

    e_isy = arrival_isy - spring_sy.

For consecutive stages:

    Delta e_isy = e_i,s+1,y - e_isy.

This is individual-level phase geometry. It does not alone prove feedback
correction.

## Source feasibility already established

Schreven et al. report public data at DataverseNL DOI 10.34894/KLPQG9 and use
tracking from 83 individuals together with long-term environmental monitoring.

Automated Dataverse retrieval is currently blocked by its Anubis proof-of-work
page, so no raw Schreven Dataverse rows have been opened in this repository.

The related Kölzsch barnacle-goose archives confirm that this research system
has route-resolved public tracking suitable for stage reconstruction:

- Greenland: 6,853 GPS fixes, 7 IDs;
- Svalbard: 24,488 fixes, 22 IDs;
- Barents Sea: 21,102 fixes, 15 IDs.

Barents Sea includes populated ground-speed and heading fields throughout;
speed can be reconstructed from timestamped locations for the other archives.

These older archives demonstrate technical feasibility but do not substitute
for the Schreven dataset.

## Strongest biological contrast

The most useful contrast is not positive cue versus no cue. It is route steps
with different signed environmental mappings.

Generic negative cue relationships and negative adaptive reaction norms are
prior art. The candidate PAYOFF question is narrower:

> When the signed mapping between current and future seasonal state differs
> among route stages, do tracked migrants show corresponding differences in
> enacted timing response, and how much downstream temporal flexibility remains
> after that response?

## Promotion ladder

Level 0: source failure.
Ordered individual route stages cannot be reconstructed.

Level 1: exposure bridge.
External mapping + individual exposure opportunity + downstream phase are
identified.

Level 2: behavioral bridge.
Level 1 plus within-stage timing response is estimable.

Level 3: flexibility bridge.
Level 2 plus an independently defensible temporal-flexibility coordinate exists.

Level 4: structural actionability.
Requires a counterfactual or mechanistic model identifying the feasible
response set rather than realized behavior alone.

Only Level 4 can claim direct natural r(t).

## Current decision

SCHREVEN_FULL_STACK = PROMISING_BUT_NOT_YET_IDENTIFIED

RAW_DATAVERSE_ROWS = NOT_MATERIALIZED

PUBLISHED_AGGREGATE_OUTCOMES = KNOWN

EXTERNAL_FORECASTABILITY = SUPPORTED_PUBLISHED

INDIVIDUAL_EXPOSURE = PLAUSIBLY_RECONSTRUCTABLE

BEHAVIORAL_RESPONSE = PLAUSIBLY_RECONSTRUCTABLE

STRUCTURAL_ACTIONABILITY_r = NOT_IDENTIFIED

TEMPORAL_SLACK_PROXY = AVAILABLE_PUBLISHED

DOWNSTREAM_PHASE = PLAUSIBLY_RECONSTRUCTABLE

The next step is source materialization and a field audit, not a new theory.
