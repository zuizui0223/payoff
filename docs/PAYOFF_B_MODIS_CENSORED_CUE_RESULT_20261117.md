# PAYOFF-B right-censored source event as potential predecision information — original result

Date 2026-11-17. **POST-OPEN EXPLORATORY.** This result is not an independent confirmatory ecological hypothesis, does not measure actual bird information or fitness, and reuses exactly the same MODIS years and 104 geographical environmental pairs as prior PRs #396–398.

## Pre-result frozen contract and original data

- Contract committed before these predictions: \`docs/PAYOFF_B_MODIS_CENSORED_CUE_FREEZE_20261117.md\`.
- Pin: \`br-amaral/BirdMigrationSpeed\` source commit \`62c58d77c2028bd863dfe3697b0d9cf29ceaeab0\`, **only** satellite \`data/for_green-up_dl.rds\`, SHA256 \`8989bf98752cf23a6be237332e35c44abff5a39d2a00d5bd1f65cce732cf6199\`; no eBird arrival, species range or migration data.
- 106 original Eastern North American forest sites; same **104 nearest-southern geographical source→target pairs**, **88 unique source cells**, 2002–2017, two 8-year intervals and exactly 624 heldout forecasts (each period predicts year 6, 7, 8 using preceding 5, 6, 7 historical years).
- Existing PR #397 oracle forecast skill (+0.7454488, +0.5993736) and PR #398 7-day-delay positive-source-only gate skill (+0.001605643, +0.220805535) reproduced, along with 624 exact source pair/year baseline squared errors.
- New explicitly **hypothetical decision** = target-only historical forecast \`M0\` − 7 days. Original MODIS midgreenup is retrospectively processed and has NO confirmed real-time delivery latency. The primary hypothetical event-processing lag of +7 days and secondary zero-lag case are NOT measured telemetry. No actual bird or person decision is observed.

## How absent information was used

The previous PR #398 assumed that the completed exact source midgreenup day can be supplied only if already observed by the hypothetical deadline, otherwise the observer falls back to M0. This neglects the possible information in an **observed *absence* of the source event**.

The new fixed analysis uses only the binary record \`event_seen=1{source_midgreenup+report_delay<=decision_day}\`, with both \`event_seen=0\` and \`event_seen=1\` assumed observable from a hypothetical monitoring network. For each heldout year:
1. Estimate training-only \`M0 = lm(target ~ year)\` and derive source-event status for each training year from its train-only fitted decision day.
2. Fit \`M_C = lm(target ~ year + event_seen)\` with **training years only**. If binary status does not vary in training, use M0 unchanged rather than dropping the heldout observation or optimizing penalties.
3. Derive test-year event status using original source onset and only the M0 test prediction. Test-year target onset is used only **after** prediction to score and audit whether the hypothetical decision was already too late.
4. Each environmental source cell is the resampling block; 10,000 draws seed 20261117. All apparent gains must be interpreted as within-source exploratory forecast fits, not information value to a migrant.

## Primary original-data result: 7-day lead + 7-day assumed report lag

| Quantity | Early 2002–09 | Late 2010–17 |
|---|---:|---:|
| Original baseline RMSE (days) | 10.929665 | 6.771467 |
| **Censored binary model RMSE (days)** | **10.513034** | **6.890137** |
| **Censored binary model skill, 1−SSE(M_C)/SSE(M0)** | **+0.07478549** | **−0.03535724** |
| 95% source-cell bootstrap interval | **[+0.00219958,+0.1469409]** | **[−0.145504,+0.0643791]** |
| Source event positive at hypothetical deadline | 5 / 312 | 43 / 312 |
| Source event negative at hypothetical deadline | 307 / 312 | 269 / 312 |
| Training folds with both binary states / fitted M_C | **57 / 312** | **113 / 312** |
| Training folds falling back to M0 | **255 / 312** | **199 / 312** |
| Hypothetical decision actually before target event | 306 / 312 | 219 / 312 |

The early-to-late skill change was **−0.1101427**, 95% source-cell bootstrap **[−0.2596293,+0.02295365]**, which includes zero. A positive mean early binary effect is therefore not a general, independent new ecological result; the year-to-year change does **not** pass an exclusive/confirmatory evidential threshold. Late heldout forecast accuracy was worse with the binary cue.

### Crucial retrospective deadline validity check

The true target onset day was examined **only after** the train-only decision and forecasts. Partitioned contributions relative to total baseline squared error:
- Early: genuinely pretarget hypothetical decisions **+0.1021412** vs already-posttarget **−0.0273557**, total +0.0747855.
- Late: genuinely pretarget hypothetical decisions **−0.1140923** vs already-posttarget **+0.0787351**, total −0.0353572.

Because the classification uses heldout truth, it is an *audit*, not a valid policy known at decision time; importantly, **the late negative overall effect is not rescued by a positive true-pretarget subset**. No outcome-driven exclusion changes the actual forecast results.

## Frozen zero-reporting-delay sensitivity (hypothetical, not real-time availability)

| Quantity | Early | Late |
|---|---:|---:|
| Positive source event at hypothetical deadline | 32 / 312 | 198 / 312 |
| Training folds with variable event status | 207 / 312 | 245 / 312 |
| Censored binary cue skill | **+0.24919627** | **−0.03332977** |
| Source-cell bootstrap 95% interval | [+0.15435899,+0.3401636] | [−0.2052364,+0.1129478] |

Late–early binary-skill difference **−0.2825260**, source-cell bootstrap 95% interval **[−0.4745266,−0.10470264]**. **This remains exploratory and heavily depends on an unrealistic assumption that retrospective satellite midgreenup is instantly available.** The before/after true-target audit shows early +0.2503107/−0.0011145 and late −0.2154334/+0.1821036 (contribution fractions), again underscoring that in the late window some apparent forecaster benefit is from predictions at a hypothetical decision already after true spring.

## What this resolves in PAYOFF and what it does NOT

Three concepts must stay distinct:
1. \`q\` environmental covariation (retrospectively observed and population/site conditioned);
2. **Potential** out-of-year ability to forecast another environment from a known source onset;
3. **Predecision observable filtration** (a time-indexed information set), which may include the event not having occurred yet, not just already completed onset; and a subsequent fourth element, **actionable control / recourse**, is measured in none of these MODIS-only panels.

The result shows that treating absence of a completed seasonal event as a binary observed covariate **can change the prediction relative to an event-positive-only policy**, but it **does not reliably improve it**. Training only 5–7 calendar years creates frequent degenerate all-zero/all-one binaries and fallback folds. Neither this nor PR #398 proves the PAYOFF-B biological game or new survival-analysis theory. Bauer et al. (2020, DOI 10.1098/rspb.2020.0622) already addressed migration information under uncertainty, and censored time-to-event information has existing proper forecast and survival theory (e.g. arXiv 2603.14835, 2026).

**Main V7 remains NOT_ESTIMABLE:** 2015 Kölzsch 3 flyway GPS original 52,443 source fixes are independently verified, but 1982–2011 historical GDD spring-onset stopover anomaly tables S2–S7 and exact region crosswalk were not obtained. This MODIS East North America forest sample does not replace the Arctic barnacle goose environment nor establish real observed animal action.

## Reproducibility

Original source script: \`analysis/movement_phenology/payoff_b_modis_censored_cue_20261117.R\`.
Dedicated original run: https://github.com/zuizui0223/payoff/actions/runs/44061630915, SUCCESS; synthetic no-heldout-target-leakage tests also PASS. Artifact ID 14318012952 with three inspectable CSVs:
- \`payoff_b_modis_censored_cue_folds.csv\`
- \`payoff_b_modis_censored_cue_periods.csv\`
- \`payoff_b_modis_censored_cue_bootstrap.csv\`

Status: **EXPLORATORY_METHOD_CHECK_ONLY**. Keep the code/results as a separate stacked DRAFT and do not merge or promote the early binary signal to a bird/migration/fitness discovery.
