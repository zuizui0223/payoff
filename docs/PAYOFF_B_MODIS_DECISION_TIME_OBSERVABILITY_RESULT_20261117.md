# PAYOFF-B: can source spring information arrive before a decision? Observed event-time falsification

Date 2026-11-17. **Status: POST-OPEN EXPLORATORY SCENARIO + RETROSPECTIVE TIMING AUDIT. Not a bird behavior/fitness result, not a new preregistered ecological confirmation.**

## The exact scientific problem

The prior eBird-free MODIS study (PR #396) showed modest spatial spring synchrony change in 104 geographically selected eastern North American forest source–target links; the next-year forecast study (PR #397) found very strong apparent forecast skill when allowed to use the **complete** same-year southern satellite midgreenup date (2002–09 skill +0.74545, 2010–17 skill +0.59937) compared with the target's train-only calendar trend. This supplied cue may be unavailable at the moment a decision must be made and the target may have already begun spring even if a model predicts its onset in the future.

A new availability rule was frozen in \`docs/PAYOFF_B_MODIS_DECISION_TIME_OBSERVABILITY_FREEZE_20261117.md\` before calculating the following new outcomes. **This rule and the same MODIS years were chosen after observing earlier analyses and can never be described as independent confirmatory evidence.**

## Source and exact matched sample

Original source **only** satellite \`br-amaral/BirdMigrationSpeed\` pinned commit \`62c58d77c2028bd863dfe3697b0d9cf29ceaeab0\`, \`data/for_green-up_dl.rds\`, SHA256 \`8989bf98752cf23a6be237332e35c44abff5a39d2a00d5bd1f65cce732cf6199\`. The existing R scripts rechecked the same 106 satellite forest cells, **104** original nearest-south latitude links, **88** source-cell bootstrap blocks and the original mean correlation change +0.08057016. No eBird occurrence, bird species, bird distribution mask, GPS, livestock, bird arrival or fitness information was used.

Exactly **624 original-satellite heldout predictions** = 104 physical pairs × 2 separate eight-year periods × 3 forward heldout years (5 previous training years→next, then 6→next, then 7→next). Models and previous oracle result reproduced to within 1e-6.

### Frozen hypothetical (NOT measured) information deadline

- Training-only M0 = \`target_midgreenup_day ~ year\`.
- Oracle M1 = \`target_midgreenup_day ~ year + same_year_source_midgreenup_day\`.
- Fixed hypothetical action deadline = **M0 predicted target greenup − 7 calendar days**. This is NOT a real bird departure, real breeding deadline or measured observer choice.
- For the primary scenario, assume **7 additional calendar days** between source midgreenup and completed availability of its observation, then apply M1 only when \`source_onset + 7 <= deadline\`; otherwise fall back *exactly* to M0. A zero-day observation-lag sensitivity was fixed but is even less realistic.
- **Critically**, MODIS MCD12Q2 midgreenup is reconstructed after the growing season from a remotely sensed curve. Seven days is an arbitrary, potentially over-optimistic reporting delay and **not measured real-time information availability**. Nor do we know that any migrant was at or near the source cell or could sense the cue.

## Results before checking whether the decision was too late

| Metric | 2002–09 (312 next-year tests) | 2010–17 (312 next-year tests) |
|---|---:|---:|
| M0 baseline RMSE, days | 10.929665 | 6.771467 |
| M1 unrestricted same-year source RMSE, days | 5.514351 | 4.286004 |
| M1 unrestricted source *squared-error saving fraction* | **0.7454488** | **0.5993736** |
| 7d deadline + 7d latency gate RMSE, days | 10.920887 | 5.977309 |
| **7d deadline + 7d latency gate squared-error saving fraction** | **0.001605643** | **0.220805535** |
| Source event met the 7d + 7d eligibility gate | **5 / 312 (1.60%)** | **43 / 312 (13.78%)** |
| Hypothetical decision date preceded *true* target event | 306/312 (98.08%) | 219/312 (70.19%) |
| Zero-latency sensitivity, squared-error saving | 0.01282361 | 0.57631553 |

The naive overall gate change was **+0.2191999** of baseline squared error, source-cell block bootstrap 95% interval **[+0.1387521,+0.3014302]**, 10,000 draws seed 20261117. The numbers are reproducible, **but this interval does not make late decisions biologically meaningful**.

## Decisive post-scoring timing audit: late apparent signal is nearly entirely invalid as an advance forecast

The actual target phenology was inspected only *after* determining the hypothetical decision and forecast, **never** for model fitting or choosing the available-cue policy. We partitioned the pre-existing squared-error improvement by whether its fixed decision date truly occurred before or after target spring onset:

| 7d-lag policy event use | Early | Late |
|---|---:|---:|
| Eligible source event AND decision precedes target onset | **4** | **12** |
| Eligible source event BUT decision occurs after target onset | **1** | **31** |
| Percentage-point contribution to full-sample baseline-error savings from genuinely pretarget decision rows | **+0.0502 pp** | **+0.0896 pp** |
| Percentage-point contribution from already-post-target rows | **+0.1103 pp** | **+21.9909 pp** |
| Total apparent gate saving (both kinds) | **+0.1606 pp** | **+22.0806 pp** |

These parts add to the already reported 0.001605643 / 0.220805535 in fractional units. Among late-period **43** source-available events, **31** occurred at a hypothetical decision time after target spring actually started. Therefore **almost the entire apparent 22.1% saved squared error is unfit to represent forecasting a still-unobserved target event.** The valid-order contribution is tiny under this particular hypothetical deadline (0.0896 percentage points relative to the all-predictions M0 SSE). Because the partition uses future observed target timing, it is *post-scoring validity decomposition*, not an executable decision rule and not an identified future benefit.

**This is the principal supported methodological finding**, not the tempting naive late-gate +22.1%. Never elevate positive bootstrap significance from an invalid temporal interpretation. The appropriate inference is that claimed information availability must be verified relative to the decision deadline **and** the actual future outcome timeline. It remains possible to know useful *negative information* from not observing source spring, or to use other earlier climate cues, but this simplistic observed-completed-greenup policy does not test those alternatives.

## PAYOFF theoretical meaning / claim ceiling

This case separates three very different objects:
1. **Correlation:** sources and targets show shared seasonal variation;
2. **Clairvoyant cross-site forecast skill:** knowledge of the current year's **complete** source midgreenup improves next target predictions;
3. **Information available before a particular action:** far fewer completed source events qualify; some candidate decisions are already past the real target event.

That ordering motivates, but **does not prove**, PAYOFF's hypothesis that the ecological value of information depends jointly on predictive reliability and finite opportunity to act. We have **no individual decision-time cue, actual goose departure, stopover recourse, energetic return, reproductive fitness or game-theoretic payoff in the satellite dataset**. Neither a real bird nor an operational MODIS forecasting system was simulated with measured observation latency.

The pre-frozen 2015 three-flyway V7 goose \`q×U\` interaction remains **NOT_ESTIMABLE** because the original independent 1982–2011 stopover GDD-jerk anomalies Tables S2–S7 and exact region crosswalk are still not accessible/verified. Wiley lists the supplement \`jane12281-sup-0001-SuppInfo.docx\` but publisher access returned 403; KNAW provides manuscript text, not original numeric supplement. Do not substitute the eastern North American forest system as a goose environmental source.

## Code, tests and data rights

- Freeze: \`docs/PAYOFF_B_MODIS_DECISION_TIME_OBSERVABILITY_FREEZE_20261117.md\`.
- Original source runner: \`analysis/movement_phenology/payoff_b_modis_observable_cue_gate_20261117.R\`.
- Dedicated original-data and synthetic target-nonleakage test: **https://github.com/zuizui0223/payoff/actions/runs/44055773083**, SUCCESS. Its artifact contains 3 CSVs: \`payoff_b_modis_decision_time_gate_result.csv\`, \`payoff_b_modis_decision_time_period_scores.csv\`, \`payoff_b_modis_decision_time_year_scores.csv\`.
- The branch does not redistribute private tracking or licensed noncommercial bird GPS. It uses satellite-only source already downloaded in the eBird-free upstream PR #396, not \`final.rds\` or species mask artifacts.
- **Remain DRAFT / not merged to main**. The scientifically useful contribution is a failure mode in treating an observed environment relation as *predecision information*, not new evidence of ecological fitness consequences.
