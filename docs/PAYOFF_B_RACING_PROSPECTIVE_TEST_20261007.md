# PAYOFF-B racing prospective mechanism-separation test

Date: **2026-10-07**  
Status: **prospective design frozen before JRA-VAN racing outcome access in this branch**

## 1. Purpose

This is **not** a preregistration for a novel betting-market mechanism.

The purpose is to use Japanese central horse racing as an external
mechanism-separation system for the PAYOFF-B information-value framework.

The target distinction is:

    value loss from physical / biological irreversibility

versus

    value loss because a collective forecast absorbs the same information.

The racing system is attractive because, until the wagering cutoff, physical
actionability can be approximately held fixed while market beliefs evolve
repeatedly.

## 2. Source boundary

Planned source:

- JRA-VAN Data Lab time-series win odds and race/result records;
- JRA-VAN head-to-head data-mining forecast records (TM), using
  **data category 1 = previous-day forecast** as the primary fixed public
  information source.

Public JRA-VAN documentation states that time-series odds are recorded at
roughly 5–10 minute intervals and that win/place, bracket quinella and quinella
time series are supported.

Primary analysis uses **win odds only**.

No claim is made here that the present branch has downloaded or inspected the
race outcomes.

## 3. Unit and eligibility

Primary unit:

    race × horse × pre-race time slice

Primary race set:

- JRA races with a valid official result;
- complete win-odds history for all required primary time slices;
- no horse retained in the active field with missing final result linkage.

Primary analysis excludes races in which the active runner set changes after
the earliest included time slice (for example, a late scratch), because that
changes the feasible action set and confounds the pure information-diffusion
comparison.

Late-field-change races may be analysed separately as an actionability-change
case after the primary test is frozen.

## 4. Fixed time slices

Use the last available odds snapshot at or before each target time:

- T-60 min
- T-30 min
- T-15 min
- T-10 min
- T-5 min
- LAST = final available pre-close snapshot

Never use a snapshot after the target time to fill an earlier slice.

If the feed cadence prevents a required slice from being reconstructed under
the predeclared tolerance, the race is excluded from the complete-case primary
analysis and retained for a secondary available-case analysis.

## 5. Market probability

For horse i in race r at time t, let decimal win odds be O_irt.

Define the raw reciprocal-odds score

    u_irt = 1 / O_irt.

Normalize within the active field:

    m_irt = u_irt / sum_j u_jrt.

This removes the common pool scaling and gives a within-race probability vector
for proper-score comparison.

The market probability is treated as a collective forecast, not as a guaranteed
fair probability.

## 6. Frozen public forecast

The **primary** fixed information source is not a newly trained horse model.

Use the JRA-VAN head-to-head data-mining forecast record:

    record type: TM
    data category: 1 = previous-day forecast
    field: predicted score, 000.0--100.0

JRA-VAN describes the head-to-head model as predicting pairwise win/loss and
constructing a per-horse score such that higher scores correspond to stronger
predicted performance.

For each race, standardize the previous-day scores within race and convert them
to probabilities with one global training-only softmax scale lambda:

    z_ir
      =
    (score_ir - race_mean_r) / race_sd_r

    f_ir(lambda)
      proportional to
    exp(lambda z_ir).

Fit lambda on training races only by multinomial log loss, then freeze it.

This gives a probability vector from a **public forecast released before the
within-day odds path** without building a bespoke predictor whose feature
engineering could itself create leakage or post hoc flexibility.

The same f_ir is used at every within-race time slice.

If the previous-day TM record cannot be recovered historically with its data
category intact, the primary route is blocked. A self-built pre-market form
model may then be developed only as a separately frozen secondary route; it is
not silently substituted into the primary analysis.

## 7. Market-absorption combiner

At each time slice t, combine the frozen form forecast f_ir with the
contemporaneous market forecast m_irt through a logarithmic opinion pool:

    h_irt(w_t)
      proportional to
    f_ir ^ w_t * m_irt ^ (1-w_t),

with

    0 <= w_t <= 1.

Choose w_t **only on the training period** by minimizing race-level
multinomial log loss.

Interpretation:

- w_t near 1: the non-market model still carries substantial independent
  predictive content;
- w_t near 0: the contemporaneous market dominates the optimal combination.

w_t is not itself declared to be the PAYOFF exclusivity parameter e(t), but its
time trajectory is a directly estimable proxy for remaining incremental value
of the fixed public-information forecast.

## 8. Primary endpoints

For each time slice t compute on held-out races:

### Market log loss

    L_market(t)
      =
    - mean_r log m_w(r),r,t

### Frozen form-model log loss

    L_form
      =
    - mean_r log f_w(r),r

This is constant across t by construction.

### Hybrid log loss

    L_hybrid(t)
      =
    - mean_r log h_w(r),r,t

### Incremental form value over market

    Delta_form(t)
      =
    L_market(t) - L_hybrid(t).

Positive Delta_form means the frozen form model improves proper-score
prediction beyond the contemporaneous market.

Primary time-structure quantities:

1. w_t;
2. Delta_form(t);
3. L_market(t).

## 9. Prospective predictions

### P1 — collective forecast improves toward post

The market's multinomial log loss will tend to be lower at later pre-race time
slices than at early slices.

This is a directional prediction, not a required monotonicity claim at every
adjacent pair.

### P2 — fixed public-form information is progressively absorbed

The optimally trained combination weight on the fixed form model will tend to
decline as the race approaches:

    w_60 > w_LAST

as the primary contrast.

### P3 — incremental form value shrinks

On held-out races,

    Delta_form(60 min) > Delta_form(LAST)

is the primary PAYOFF competitive-information contrast.

Failure of P2/P3 is informative: it would mean that the market does not simply
absorb the focal model's public information on the assumed schedule, or that
the focal model captures stable complementarity rather than a transient edge.

### P4 — accuracy and incremental value can decouple

The strongest PAYOFF pattern would be:

    market / hybrid prediction accuracy improves toward post,

while

    the incremental contribution of the fixed form model declines.

This is the empirical analogue of

    q(t) rising while e(t) falls.

It is not claimed to be a new result in market microstructure.

## 10. Positive-control path test

Because Japanese interim-odds literature already reports predictive content in
last-minute odds trajectories conditional on final odds, include one
**positive-control replication**, not a novelty endpoint.

Define a predeclared last-5-minute log-odds movement and test whether adding
that path feature to a final/current-odds model improves held-out proper score
or reproduces the published directional relation.

If this positive control fails badly, treat the dynamic feed or time alignment
as suspect before interpreting P1–P4.

## 11. Secondary event-study candidate: race-day body weight

JRA reports race-day horse weight roughly around one hour before post and
updates it promptly after release.

This creates a potential public-information event around the first primary time
slice.

A later secondary analysis may test how rapidly odds incorporate a predeclared
body-weight surprise measure, but this is **not** part of the primary frozen
test until:

1. the exact release timestamp is available in the source records;
2. the surprise measure is fixed without inspecting outcome-conditioned odds
   responses.

## 12. Split and leakage control

Use chronological splits.

The exact calendar boundaries must be fixed immediately after confirming which
historical JRA-VAN time-series period is actually retrievable, and before
opening the corresponding outcome table.

Minimum structure:

- training period: fit the previous-day-score softmax scale lambda and the
  time-specific log-pool weights w_t;
- untouched test period: all reported primary endpoints.

The public-score calibration and market-combination weights are therefore both
estimated without using the test outcomes.

No random horse-level split is allowed because horses recur across races and
would leak identity/history across folds.

Bootstrap and uncertainty calculations resample by race.

## 13. Secondary scores

Secondary predictive diagnostics:

- multiclass Brier score;
- calibration intercept / slope where estimable;
- reliability plots by probability bin;
- top-1 winner accuracy only as a descriptive statistic.

Primary inference remains proper-score based. Top-1 accuracy is not an
appropriate sole target for a probabilistic racing model.

## 14. Betting-profit boundary

Primary test does not optimize or report a betting strategy.

A profitability analysis requires a separate frozen protocol covering:

- takeout;
- final settlement odds;
- uncertainty in final odds at decision time;
- stake sizing;
- pool impact;
- late execution / cutoff risk;
- multiple testing across bet types.

Prediction quality and betting profitability are not interchangeable.

## 15. PAYOFF mapping

Racing variables:

    q(t)
      -> predictive quality of focal information

    e(t)
      -> remaining incremental predictive value relative to the crowd

    r(t)
      -> approximately constant until the hard wagering cutoff in the primary
         mechanism-separation design

Ecological variables:

    q(t)
      -> improving seasonal-state information

    r(t)
      -> declining biological recourse / retained actionability

    e(t)
      -> not required for the canonical ecological model

The same hump-shaped usable-value trajectory can therefore arise from different
mechanisms.

## 16. Decision rule for the branch

Promote racing from analogy to empirical PAYOFF evidence only if:

1. the time-series feed is obtained without post hoc selection of races;
2. the chronology and leakage controls are frozen;
3. the positive-control dynamic-odds test behaves plausibly;
4. P2/P3 are estimated on untouched races;
5. conclusions are stated as mechanism comparison, not market-microstructure
   novelty.

Otherwise retain racing as an explanatory analogy only.
