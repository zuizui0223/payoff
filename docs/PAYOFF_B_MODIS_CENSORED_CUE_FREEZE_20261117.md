# PAYOFF-B: event-nonoccurrence as censored source information — exploratory freeze

Date: 2026-11-17. **Design frozen after observing all PR #396–398 outcomes.** This study is not an independent prediction of an ecological mechanism. It diagnoses one additional hypothetical information channel absent from PR #398: at a decision deadline, a monitored phenological event may *not yet have occurred*. That absence is a current, right-censored observation and must not be confused with the unknown completed event date.

## Literature and novelty ceiling

- Bauer, McNamara & Barta (2020), DOI 10.1098/rspb.2020.0622, already analyze information, stopovers, predictability, migration decisions and fitness in a dynamic model. We **do not** claim the first information-based migration model.
- Time-to-event and interval/right-censored forecasting are established tools. See Taggart, Loveday & Louis (2026) \`arxiv:2603.14835\` for scoring event-time forecasts under censoring. We do **not** claim new survival-analysis methodology.
- This MODIS-only demonstration measures no real goose, bird information uptake, actual forecast-delivery latency, migration strategy, resource transfer or fitness. It can at most reveal a **modeling/observation failure mode**, not PAYOFF-B's ecological mechanism.

## Exact external data, QA and fixed comparison

- Satellite-only \`br-amaral/BirdMigrationSpeed\` pinned commit \`62c58d77c2028bd863dfe3697b0d9cf29ceaeab0\`, original \`data/for_green-up_dl.rds\`, byte length 15,579, SHA256 \`8989bf98752cf23a6be237332e35c44abff5a39d2a00d5bd1f65cce732cf6199\`.
- **NO eBird**, bird-species range mask or arrival data: neither \`final.rds\` nor \`species_Grid.RData\`, nor any tracking file. Preserve PR #396 fixed **104 nearest-southern geographical pairs and 88 environmental source cells** among 106 Eastern North American forest sites, same original \`gr_ncell>10000\` pixels and 2002–2017 complete 16 years.
- Exact original PR #397 rolling forecast skill early=0.7454488, late=0.5993736; exact PR #398 7+7d simple event-only gate early=0.001605643 and late=0.220805535. Fail closed if these source or score invariants drift. Keep same **624 heldout year-pair predictions**, each with 5,6 or 7 previous **training-only years** in each 8-year window.
- Previously frozen hypothetical decision day \`d = predicted_target_onset(M0) − 7\`, and hypothetical event-processing lag \`7 days\`. Neither is empirical observed bird behavior nor operational MODIS latency. A zero-day lag is the **only** additional sensitivity and also appears in PR #398.
- Observed data at a hypothetical decision may include \`C(d)=1{source_greenup_day + 7 <= d}\` (source event occurred and is available), **or** \`C(d)=0\` (the monitored event has not yet been reported). In this scenario, both states are assumed observable, including negative reports. Actual satellite midgreenup is reconstructed retrospectively so these assumptions remain hypothetical.

## Frozen model and estimation

Per 8-year period, for test year 6/7/8:
1. Fit \`M0: target_greenup ~ calendar_year\` using only earlier 5/6/7 training years.
2. For *each training year*, define its historical decision date from the M0-fitted training prediction for that year, minus seven days. Use source-day + lag <= its training-year deadline to compute \`C_train\`. This is legitimate for train-only modeling and never uses heldout target onset. It reconstructs a hypothetical historical rule rather than an actual observed policy.
3. For heldout year, compute \`C_test\` from the train-only M0 heldout prediction − seven days and the original measured source day + seven-day assumed reporting lag. Heldout **true target date must never enter C_test**, the decision time, or model fit.
4. If \`C_train\` contains both 0 and 1 and \`lm(target ~ year + C_train)\` has rank 3, predict heldout target from its observed \`C_test\`. This is the **censored binary cue** model \`M_C\`. If all training cues are identical or rank-deficient, fail safe to M0 **without changing folds or selecting years**. Report number of training variation/fallback folds.
5. Compare \`M_C\` to the identical heldout target-only M0, and the **already frozen** PR #398 event-only M1 gate (uses exact source date only when reported, otherwise M0). Do not choose between models based on target outcome. Binary event status may be informative even if \`C_test=0\`.
6. Preserve both overall and retrospective true-timing partitions; true target day is allowed **only after predicting** for error and audit whether fixed hypothetical decision occurred before actual target event. No target-truth-based selection of a future predictor.
7. All improvements expressed \`1-SSE(M_C)/SSE(M0)\` across original **104 pairs × 3 next-year predictions per period**; per-period RMSE days, source-event incidence, binary-cue variable training support, error contributions of C_test=0 vs 1 and before vs after actual target greenup.
8. **10,000 complete source-cell cluster bootstrap** replicates seed \`20261117\`, sampling the same 88 original source cells and carrying all paired endpoints (early and late). Report early, late, change and 95% intervals. Regional climate dependence across adjacent source and target cells remains unhandled; intervals are conditional on the spatial sample and these assumptions.
9. Zero-day processing lag sensitivity repeats *only the same binary-cue model*, unmodified M0 horizon and all 104 pairs. No other horizons, penalization, weather covariates, pair selection, model family or calendar breakpoints may be searched to force a favorable result.

## Main inference / stop conditions

The ideal event-time forecaster with right censoring is not necessarily linear in \`C(d)\`, so this binomial indicator is only one fixed illustrative restricted model, **not** a general maximum or minimum possible information benefit. An observed absence could be valuable even if the fully realized event value is late; however **actual negative reporting** may not be available from remote-sensing midgreenup products.

If the positive result arises predominantly from hypothetical decision dates after *true* target onset, reject its interpretation as valid prior forecast. If the binary predictor is uninformative or harms prediction under rolling validation, preserve that failure. This study cannot establish that birds have negative observations, strategically wait, migrate, correct, gain energetic rewards or reproduce more successfully.

**V7 remains frozen and NOT_ESTIMABLE** because Kölzsch et al. 2015 1982–2011 GDD-jerk historical stopover supplemental anomaly tables S2–S7 and the source-verified 16-region crosswalk are still unavailable; do not substitute same MODIS eastern North American grid for the Arctic goose population.
