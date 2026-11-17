# PAYOFF-B MODIS-only out-of-year forecasting skill — original data result, 2026-11-17

**Result status: POST-OPEN EXPLORATORY.** Original satellite data are source SHA256 verified and all new source-year forecasts were successfully computed. This is not a new preregistered confirmation, because the same MODIS historical years and the previous eBird-conditioned V8 change were already inspected. No bird-specific data or eBird were used.

## Main mechanistic distinction

A pairwise *correlation* between two environmental time series does not directly measure the **marginal accuracy gain** of an observable upstream source over what could already be forecast from the target's own history. To connect PAYOFF's information-recourse theory to ecology, avoid treating static environment-to-environment covariance `q` as if it proves a bird's value of information.

The previous eBird-free MODIS geographic analysis (PR #396) selected **104** nearest-southern physical links, **88** unique source cells, from 106 eastern North American forest grid cells. Its source-only midgreenup correlation rose from r=0.7985937 (2002–2009) to r=0.8791639 (2010–2017), Δr=+0.08057016, source-cell bootstrap 95% interval [+0.02409762,+0.1391265]. The present analysis keeps **exactly those 104 pairs, same original source `data/for_green-up_dl.rds`, SHA256 `8989bf98752cf23a6be237332e35c44abff5a39d2a00d5bd1f65cce732cf6199`, and the same calendar years**. Source commit `62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`. No bird range, migration, eBird, fitted bird outcome, or resource fitness input.

## Frozen test (before these new forecast scores were opened)

Registered implementation/spec: `docs/PAYOFF_B_MODIS_OOS_FORECAST_SKILL_FREEZE_20261117.md`, committed before CI fit. Train only within each 8-year period: 5 historical years → year 6, 6 historical → year 7, 7 historical → year 8; three truly forward heldout target years per period/pair. Compare:
- **M0** no upstream source: train-only ordinary least squares target greenup DOY ~ calendar year.
- **M1** with upstream source: train-only ordinary least squares target greenup DOY ~ calendar year + source midgreenup DOY. The heldout source event is observed, heldout target never enters that fit.
- Period-specific `forecast_skill = 1 - SSE(M1)/SSE(M0)` across pairs, using each pair equally (3 test years each), expressed in fraction of **squared error saved**; not an RMSE difference. Negative is harmful, zero no marginal benefit. Cluster 10,000 bootstrap draws by complete source environmental cell, seed 20261117, preserving links using the same source.
- Same pair comparison under retrospective 8-fold leave-one-year-out (LOYO) only as a sensitivity; LOYO includes future-year training relative to leftout years.
- Strict temporal subset was specified in advance as sites where source midgreenup preceded target midgreenup in **all sixteen observed years**. This uses target calendar observations over all 16 years to *classify* the subset retrospectively; it is not a decision-time selection rule and cannot by itself establish future-available cues. Minimum strict gate ≥30 physical pairs and ≥15 unique source cells, met here.

## Source-record result

### Forward rolling-year holdouts (source forecast potential, not animal forecasting)

| Metric | Early 2002–2009 | Late 2010–2017 |
|---|---:|---:|
| Baseline target-only RMSE (days) | **10.929665** | **6.771467** |
| Added-source prediction RMSE (days) | **5.514351** | **4.286004** |
| Forecast skill: share of baseline squared error removed by observed source | **+0.7454488** | **+0.5993736** |
| 95% source-cell-block interval on skill | [+0.6434433,+0.8200721] | [+0.4537885,+0.7255434] |
| Fraction pairs whose holdout SSE decreases with source | **81.73%** | **90.38%** |

**Change in relative extra skill = −0.1460751, 95% clustered bootstrap [−0.3145864,+0.0257183].** Zero is within the interval, so a decline in *additional information value* is NOT statistically established. Both target-only and source-added absolute RMSE improved; the M0 baseline improved more proportionately. The data show a reproducible distinction between a large positive cross-site `r` and the *incremental* value of that source over an existing baseline.

### Chronological event-order gate

Across all 104×16 observed source-target-year records, source greenup was earlier in **81.73%** of pairs/years. Source was strictly earlier in all sixteen years for **50 pairs from 42 unique source cells**, passing the predefined minimum. This is *environmental event ordering*, not actual goose departure timing.

For the stringent 50-pair subset:
- forward skill early **+0.7718442**;
- forward skill late **+0.7374045**;
- skill difference **−0.03443975**, source-block bootstrap 95% interval **[−0.1569102,+0.106258]**.

No evidence for a reliable decline in skill even in the strict-time subset. The strict subset was defined with full 16-year information and is not a prospective or causal migrant sampling protocol.

### Retrospective LOYO sensitivity

LOYO skill early **+0.8277850**, late **+0.7266135**, change **−0.1011715**. LOYO shares the direction of the forward contrast but is not a prospective forecast protocol.

## Biological implications and claims that must NOT be made

**Allowed (narrow):** Eastern North American forest midgreenup among the fixed geographically paired MODIS cells is forecastable from a southern neighbor's observed seasonal timing beyond a year-only baseline in both separate 8-year intervals. Stronger mean environmental correlation does not automatically translate into a larger *incremental* improvement in heldout forecasts. The point estimate of incremental advantage is smaller in the later window, but the difference is uncertain.

**Not supported / not allowed:** migratory birds accessed this cue at the departure decision, that southern greenup was observable before bird migration, that correlation/skill trend was caused by climate change, that fewer birds became maladapted, that source cue has direct energetic/fitness value, that information×remaining opportunity interaction was detected, or that the current study is an independent replication of earlier V8 (it is the **same MODIS historical series**). The 104 pairs' geographic sample domain was originally assembled for an eastern North American bird-phenology analysis, so **no claim of independent random global environmental sampling**.

**Remaining main-line blocker:** Frozen V7 barnacle goose 3-flyway GPS files (52,443 fixes) are source-verified but original independent 1982–2011 GDD-jerk regional spring-onset anomalies Tables S2–S7 and the sixteen-stopover regional crosswalk are not yet available for q×route-stage-urgency on bird timing. The Kölzsch 2015 original Wiley DOCX was identified as `jane12281-sup-0001-SuppInfo.docx` but publisher fetch denied HTTP 403; alternate institutional manuscript is not a substitute for its tables. No q×U coefficient is fitted.

## Reproducibility

- New script `analysis/movement_phenology/payoff_b_modis_oos_forecast_skill_20261117.R`.
- Original source / analyses in upstream PR #396 (do not duplicate or overwrite the previous fixed correlation).
- Dedicated original-data run: **https://github.com/zuizui0223/payoff/actions/runs/44035822839**, status SUCCESS, synthetic contract PASS, original source and 10,000 block bootstraps complete. The attached artifact contains `payoff_b_modis_oos_forecast_summary.csv`, `payoff_b_modis_oos_forecast_protocol_scores.csv`, `payoff_b_modis_oos_forecast_pair_scores.csv`.
- Artifact source has environment-only cell IDs; no private individual animal GPS or bird records included.

**Outcome decision: keep as exploratory satellite environmental forecast calibration. Do not promote it to evidence that PAYOFF-B's game-theoretic behavioral mechanism has been empirically verified.**
