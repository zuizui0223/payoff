# PAYOFF-B V8 source-stage migration-front access result — 2026-10-06

Status: **POSTHOC POPULATION-FRONT STAGE AUDIT; FROZEN V8 PRIMARY UNCHANGED**

## Question

The frozen source cell was selected from a lower-latitude migratory-range
environmental mapping. A stronger biological interpretation requires asking
whether the same species' estimated migration front also reaches the source cell
before the paired target cell.

This audit is restricted to source-target-species units with at least six
finite annual arrival estimates in both source and target cells in both
2002–2009 and 2010–2017.

It does not establish that the same individuals traversed both cells.

## Admitted sample

- **56 species-source-target units**;
- **31 unique source-target pairs**;
- **14 species**.

This is a substantially smaller subset than the environmental V8 network and
must not be generalized mechanically to all 166 pairs.

## Population migration front is usually earlier at the source

Define:

    front lead = target-cell arrival - source-cell arrival.

Positive values mean the estimated population migration front reaches the
source cell first.

Pair means:
- early = **7.20 d**;
- late = **5.69 d**.

Pairs with source front earlier in a majority of observed years:
- early = **28/31**;
- late = **30/31**.

Mean fraction of years with the expected front order:
- early = **0.883**;
- late = **0.917**.

Thus, in this restricted subset, the frozen environmental source is also
usually an earlier stage of the same species' population migration front.

Licensed wording:

> In the subset with arrival estimates at both mapped cells, the same species'
> estimated migration front generally reached the source cell before the target
> cell.

Do not write:
> tracked individuals passed through the source cell before reaching the target.

## Front lead narrowed between periods

Late-minus-early pair-mean front lead change:
- **-1.51 d**;
- pair-bootstrap 95% CI **-2.32 to -0.70 d**.

Equal-species:
- early = **5.99 d**;
- late = **3.97 d**;
- change = **-2.02 d**;
- 95% pair-incidence bootstrap CI **-2.95 to -0.53 d**.

Direction:
- 22/31 pairs have a more negative late-minus-early change;
- 12/14 species have a more negative change.

Therefore the population-front interval from source to target shortened.

## Local phase at the source shifted toward local green-up

Define source local phase:

    source arrival - source green-up.

Pair means:
- early = **-4.56 d**;
- late = **-1.06 d**;
- change = **+3.50 d**;
- 95% CI **+2.99 to +3.95 d**.

The population front was, on average, earlier than source mid-green-up in both
periods, but substantially less early in the late period.

This is a signed relative-timing statement, not evidence that zero phase is a
fitness optimum.

## Source-green-up to target-arrival interval widened

Define:

    target arrival - source green-up.

Pair means:
- early = **2.64 d**;
- late = **4.64 d**;
- change = **+2.00 d**;
- 95% CI **+1.21 to +2.75 d**.

Thus the reconstructed source environmental event was, on average, earlier
relative to target arrival in the late period even though the population-front
travel interval between source and target shortened.

## Arrival-date uncertainty changed markedly

Mean posterior SD of arrival estimates:

Source cells:
- early = **3.22 d**;
- late = **0.87 d**.

Target cells:
- early = **2.84 d**;
- late = **1.01 d**.

This large change in posterior precision is an important measurement boundary.
The period comparison uses posterior means and does not by itself imply that
observation quality was constant through time.

The manuscript should acknowledge this explicitly. It does not mechanically
explain the direction of the mean timing shifts, but it means that later-period
arrival dates are estimated more precisely.

## Interpretation

This audit strengthens the ecological interpretation of the range-based source
mapping in a restricted subset:

> the frozen environmental source often corresponds to an earlier stage of the
> same species' estimated population migration front.

At the same time, it does not establish individual route exposure or cue use.

Combined with the broader temporal-order results:
- the source environmental signal is temporally leading;
- its lead relative to target arrival increased;
- the same-species population front generally passes the source cell first.

These results make simple "the signal was unavailable in calendar time"
explanations less plausible, while leaving individual access, perception,
learning and actuator capacity unidentified.

## Provenance

Workflow:
- run: 37394027536
- artifact: 11381999716
- artifact SHA256:
  0c320ec46b593d21ba383de69d02e232ba2752ec9e192e80347fddb53961e7d4

Script:
analysis/movement_phenology/payoff_b_v8_source_stage_access_diagnostic.R
