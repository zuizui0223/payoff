# PAYOFF-B V8 source-signal to arrival temporal-window result — 2026-10-06

Status: **POSTHOC TEMPORAL-AVAILABILITY DIAGNOSTIC; FROZEN V8 PRIMARY UNCHANGED**

## Question

The earlier temporal-order audit established that the frozen lower-latitude
source green-up generally occurs before target green-up.

For the source signal to be even potentially useful for target arrival timing,
a stricter necessary condition is that it also occurs before the estimated bird
arrival date.

Define:

    source-to-arrival lead = target arrival date - source green-up date.

Positive values mean source green-up occurred before target arrival.

This is not a measure of cue perception, route exposure, retained actionability,
or actuator capacity. It is only a temporal-order condition.

## Admitted sample

Applying the same >=6 annual bird observations per window requirement yields:

- **140 species-target rows**;
- **69 unique source-target pairs**;
- **22 species**.

## Source-to-arrival lead widened

Pair-level means:

- early source-to-arrival lead = **5.47 d**;
- late source-to-arrival lead = **7.95 d**;
- late-minus-early change = **+2.48 d**;
- median pair change = **+2.49 d**;
- **56/69 pairs** have positive change.

Pair-bootstrap 95% CI:
- **+1.91 to +3.05 d**.

Dependence-aware intervals:
- source-cell cluster: **+1.75 to +3.48 d**;
- target-cell cluster: **+1.65 to +3.38 d**;
- 5-degree blocks: **+1.75 to +3.45 d**;
- 10-degree blocks: **+1.66 to +3.44 d**.

Equal-species weighting:
- early lead = **1.38 d**;
- late lead = **3.75 d**;
- change = **+2.37 d**;
- pair-incidence bootstrap 95% CI = **+1.60 to +3.40 d**.

Species direction:
- 21/22 species show a positive late-minus-early change in mean lead.

## Fraction of years in which the source precedes arrival

Pair-mean fraction:
- early = **0.711**;
- late = **0.777**.

Pairs with source before arrival in a majority of admitted years:
- early = **50/69**;
- late = **51/69**.

At the raw admitted species-target-year level:
- early source-before-arrival fraction = **0.603**;
- late = **0.705**.

Thus the source is not universally earlier than arrival, but temporal
availability increased between periods.

## What generated the wider lead window?

Pair-level calendar dates:

Bird arrival:
- early mean = **124.03**;
- late mean = **123.65**;
- shift = **-0.38 d**.

Source green-up:
- early mean = **118.56**;
- late mean = **115.70**;
- shift = **-2.86 d**.

Equal-species shifts:
- arrival = **-0.33 d**;
- source green-up = **-2.70 d**.

Therefore the lead window widened primarily because source green-up advanced
more than bird arrival, not because birds arrived later.

## Interpretation

The bird system does not support a simple temporal-expiry account in which the
frozen nonlocal environmental signal became more informative but arrived too
late relative to target arrival.

Instead, between periods:
- the source signal gained marginal out-of-sample forecast value;
- the source signal generally remained temporally leading;
- its mean lead relative to arrival **increased**.

Yet the posthoc delta-G_CV transfer test still detected no bird-specific
route-level improvement beyond fixed-arrival and permutation structural nulls.

This sharpens the missing layer:

> **Environmental forecast value and temporal availability are not equivalent
> to biological information use.**

Possible unmeasured layers include:
- whether individuals actually pass through or observe the reconstructed source
  location;
- which cue or cue combination they use;
- perception/learning;
- movement or stopover actuators available after cue acquisition;
- physiological readiness;
- other route-level constraints.

## Licensed manuscript wording

> In the admitted bird sample, the reconstructed nonlocal environmental signal
> occurred before target arrival more often in the late period and its mean
> source-to-arrival lead widened by about 2.5 d. Thus the absence of a
> route-level forecast-value-to-mismatch transfer cannot be attributed simply
> to the environmental signal becoming temporally later relative to arrival.

## Not licensed

Do not state:
- birds observed the source signal;
- the source-to-arrival interval is direct actionability r(t);
- birds had 5-8 d available for behavioral correction;
- increased lead caused stable mismatch;
- perception or actuator limitation is identified as the missing mechanism.

## Provenance

Workflow:
- run: 37392749991
- artifact: 11381428971
- artifact SHA256:
  fa10e7426b238b37624afd35f959b1c9e22fa8b628b65ced364b924b28c30fcb

Script:
analysis/movement_phenology/payoff_b_v8_signal_arrival_window_diagnostic.R
