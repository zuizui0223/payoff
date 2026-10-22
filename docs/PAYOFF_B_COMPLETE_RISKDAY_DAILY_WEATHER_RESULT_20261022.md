# PAYOFF-B complete all-stationary-day weather: verified source ecological observations

Date: **2026-10-22**. Original data: 3 published public CC0 Movebank GPS datasets. Original checked source and source-riskday counts are unchanged. This is **exploratory descriptive source evidence, not confirmatory migratory behavior causal inference**.

## Full daily NASA source coverage

Original fixed risk set: 5,509 eligible observed three-day stationary source opportunities, of which 333 are unthinned two-day northward GPS-labelled, 4,029 are continuing stationary, 727 are other movement, and 420 are right-censored. Original source animal/date/position are never exported.

NASA POWER UTC daily API fetched original historical T2M, WS10M, V10M and ALLSKY_SFC_SW_DWN for all 809 unique 0.5-degree grid × calendar year × month batches (343 stork, 334 goose, 132 curlew). All **809/809 public batches** succeeded, and all **5,509/5,509 original source riskday windows** had complete physical environment histories from 1 to 8 days prior to the source anchor. No weather after the three-day stationary anchor enters a predictor. This daily API source product is not numerically identical to the prior hourly 144-riskday pilot.

## Results under stronger coarse space-time comparison

For every 0.5-degree grid × calendar year × calendar month with both later-departing and staying original stationary days, compute the difference in mean lagged weather anomaly for cases vs stays, and average over those cells weighted by original source number of case-days in each cell.

| Species | Cases with an observed matched stay grid-month | Overlap source strata | Mean temperature anomaly contrast °C | Northward 10m wind anomaly contrast m/s | Solar input anomaly contrast W/m² |
|---|---:|---:|---:|---:|---:|
| Ciconia ciconia | 75 | 61 | -0.5143 | -0.2613 | -17.0988 |
| Anser albifrons | 89 | 84 | +1.0368 | +0.0741 | +2.2703 |
| Numenius arquata | 51 | 31 | +0.3396 | -0.6147 | -0.9746 |

This is an **observational restricted-overlap descriptive comparison**. Repeated animal-day risk opportunities and adjacent weather-grid space/time autocorrelation make the 176 grid-month strata NONindependent. Without animal/study/flyway/year robust uncertainty, no sign or magnitude is confirmed as a population effect.

## What changed relative to the first 144-day sample?

The first, small, deliberately outcome-stratified sample had apparent 10m northward-wind anomaly differences of -2.2963 (stork), +2.0213 (goose), and +0.4856 (curlew). In the COMPLETE all-riskday panel after coarse place/season matching those differences became -0.2613, +0.0741 and -0.6147. Thus the apparently striking source wind separation was **not stable** to fuller sampling and space-time standardization.

The physical temperature anomaly contrasts remain of opposite signs between stork and two other original taxon sources in this restricted overlap set, but do not establish a mechanism, flight strategy effect or seasonally transferable rule. Additional source-independent replication, sensor and habitat controls, real route-stopover decision timestamps, signed wind vector along a pre-specified route, independent correction feasibility and a fitness endpoint remain necessary.

The historical precommitted V7R/V8 and original stork 53-season negative results are not revised. **No ecological cue-uptake or game-theoretic coordination theorem is empirically proven** by the present source weather results.

Original CI source execution: https://github.com/zuizui0223/payoff/actions/runs/39725093549

All machine-readable original source receipts:
`data/payoff_b_complete_riskday_daily_weather_20261022.json`.
