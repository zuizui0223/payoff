# PAYOFF-B: decision-time observability gate for upstream seasonal cues

Freeze date: **2026-11-17**. Created after seeing PR #396 environmental correlation change and PR #397 real out-of-year forecast skill; this is a **post-open exploratory availability diagnostic**, not preregistered confirmation and not ecological evidence that an actual migrant sensed a cue.

## Research question

PR #397 shows positive forecast skill when a same-year southern site's **complete** MODIS mid-greenup day is supplied to a model predicting a northern site's mid-greenup day. This is only an oracle forecast if the southern site has not yet completed green-up when a decision must be made. A bird or any real-time decision-maker cannot use observations that occur in the future. Testing the information×recourse theory therefore requires an independent *availability gate* before turning environmental covariation into potential decision-time information.

## Frozen data, geometry and forecast models

- Same official satellite-only 106 forest MODIS grid cells, original BirdMigrationSpeed source commit \`62c58d77c2028bd863dfe3697b0d9cf29ceaeab0\`, file \`data/for_green-up_dl.rds\`, SHA256 \`8989bf98752cf23a6be237332e35c44abff5a39d2a00d5bd1f65cce732cf6199\`.
- Same **104** nearest southern geographic source→target pairs and **88** unique source cells as PRs #396–397. No bird, migratory range, eBird source or species data. No geographic re-selection, outlier removal, year/window change or retrospective source timing threshold changes.
- Same fixed non-overlapping 8-year windows: EARLY 2002–2009, LATE 2010–2017.
- In each period, for test year 6,7,8, fit on only preceding 5,6,7 years, respectively. Target-only M0: target midgreenup day ~ year; source oracle M1: target ~ year + same-year source midgreenup day. The same held-out year target never enters either fit.
- Retain the exact **PR #397 oracle and baseline squared error** as an immutable reproduction checksum: forward forecast skill EARLY 0.7454488, LATE 0.5993736 (tolerance 1e-6). This new test is only an availability restriction, not a refit/search of the oracle.

## Prespecified hypothetical decision-time policy — not animal behavior

A *hypothetical observer* must make a decision **7 calendar days before the target's predicted green-up date**. The target predicted date is \`predict(M0, test_year)\`, using **training years only**. Define:

\`decision_day_y = predicted_target_day(M0) − 7\`

This is not a measured goose departure or breeding deadline and may occur after the target's *actual* green-up in some years; report that retrospectively, but do **not** use observed target day to choose the forecast model.

**Primary delayed observation scenario:** the same-year southern midgreenup completion can be used only if

\`observed_source_day + 7 <= decision_day_y\`.

The second seven-day interval is a deliberately hypothetical reporting/processing latency, **not** a known MODIS real-time latency. MODIS MCD12Q2 midgreenup is a retrospectively processed phenology statistic, so even seven days may be over-optimistic for actual operational availability. The condition depends only on known source-event timing and a target-only model fitted to earlier years; it never uses held-out target onset in model selection.

When the condition is true: forecast target with M1. Otherwise: fallback **unchanged** to M0. The fallback intentionally discards the potentially useful *negative information* that southern spring has not yet occurred; the specified rule estimates the performance of a simple observed-event-only policy, **not an optimal Bayesian stopping rule or strict lower/upper bound on achievable information value**.

**One fixed sensitivity:** zero observation latency with the same 7-day lead, allowing source event if \`source_day <= decision_day\`. No trial of multiple buffer lengths to find support. The original unrestricted M1 remains an explicitly clairvoyant upper-information comparator, not a mathematically guaranteed upper bound on forecast accuracy because adding a feature can overfit.

## Outcome and dependence

For each of 104 pairs × 2 periods × 3 strictly future test years, record:
- source day, target *actual* day (for error/validation only), training-based target-only predicted day, decision day;
- whether source data were available at the assumed decision time (lag 7 or 0);
- whether the hypothetical decision time actually preceded true target event, as an **audit only** (never a condition for using M1);
- squared error for M0, M1 oracle, delayed-event policy, instant-event policy.

Compute \`skill=1−SSE(policy)/SSE(M0)\` pooled with equal pair-year weight; compare EARLY and LATE. For each period, report coverage rate of observed source events by hypothetical decision time and source-value utility conditional on choosing the forecast.

Use 10,000 bootstrap resamples **by original source environmental cell**, seed **20261117**, keeping all its target pairs and both periods (paired change). Report delay-policy skill early/late, change, and 95% interval. No day or pair pseudoindependent p-values. Report source-domain sampling limitations and that nearby cells can share weather beyond source-cell clustering. Pairwise error distribution and adverse results must be preserved.

**Gate:** fail closed if (i) original 104 pairs, 88 source cells, original SHA and previous two oracle skills not reproduced; (ii) full 8-year calendar support is missing; (iii) model rank/slope or forecast nonfinite; (iv) heldout source dates leak into training, target actual onset influences a gate, or a year is used both for fit and evaluation.

## Claims and limits

Even when a source event is available before the hypothetical decision day, the analysis **does not measure bird perception, animal arrival at that cell, dynamic feedback, irreversible commitment, food intake, migration success or fitness**. The model is an environmental hypothetical decision exercise, not a natural experiment. Any change in the gated skill is *post-open exploratory* using exactly the same years and source archive; it cannot independently confirm the original game-theory claim.

Frozen barnacle-goose V7 \`q×U\` interaction remains **NOT_ESTIMABLE**: the original Kölzsch et al. 2015 1982–2011 GDD-jerk regional anomalies Tables S2–S7 and 16-region crosswalk have not been downloaded and source-verified. Do not substitute the North American MODIS correlation for those Arctic goose route coefficients or relax the V7 admission gate.

Primary milestone: diagnose how much apparent upstream forecaster skill is lost once an explicit **predecision information availability** rule is applied.
