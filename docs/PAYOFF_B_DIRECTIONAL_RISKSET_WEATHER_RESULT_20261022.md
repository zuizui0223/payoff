# PAYOFF-B: northward surface wind and shortwave before potential migration

Date: 2026-10-22. This is the directional physical-environment source follow-up on exactly the original 144 fixed sampled GPS at-risk days. The selection rule was frozen before V10M and solar outcomes, but the test was introduced *after* the first temperature/wind-speed results and must remain exploratory.

NASA POWER hourly `V10M` is the meridional northward wind component (m/s), positive toward north, negative toward south. `ALLSKY_SFC_SW_DWN` is surface incoming shortwave radiation (W/m²). Both are aggregated for one UTC day BEFORE the end of the observed 3-day stationary window, minus the previous 7-day average; all 144 original cases/stays had valid weather. No individual GPS, exact source coordinate or event date is output.

| Taxon | Sampled northward/stay source days | Northward 10m wind anomaly contrast (m/s) | Prior-day northward 10m wind contrast (m/s) | Shortwave anomaly contrast (W/m²) |
|---|---:|---:|---:|---:|
| Ciconia ciconia | 16/32 | **-2.2963** | -2.0152 | -0.7782 |
| Anser albifrons | 16/32 | **+2.0213** | +1.0268 | +1.4019 |
| Numenius arquata | 16/32 | +0.4856 | +0.4964 | +8.5440 |

The northward wind-anomaly sign differs strongly in this exploratory small source sample, and within-month sample means retain the negative stork and positive goose/curlew signs across months with adequate weather samples. These are descriptive class-wise contrasts, not estimates with valid animal-year/flyway-cluster uncertainty. Source samples were outcome-stratified and geography/year/week/individual differ between cases and nonmovement days. No taxon-pooled biological effect is fitted.

Potential next ecological hypothesis: soaring migration and flapping migrants may differ in reliance on seasonal meteorological cues. However this source comparison does **NOT** establish migratory flight strategy as the cause. For storks, true thermal support depends on convective conditions and actual flight height; 10m surface wind and shortwave do not measure that. For all taxa, the route bearing, sensor location accuracy, actual moment of departure, local risk-set stage, and source study/cohort replication remain unresolved.

The non-support of earlier V7R/V8 and originally registered 53-stork-timing claims remains intact. A new confirmatory comparison should prospectively define stage-specific local observed cues, wind projections along a route bearing pre-estimated from independent training animals (NOT the same bird's future route), true at-risk panel hazard with site/season/year/animal clustering, and lagged physiological/fitness endpoints where observed.

Machine-readable source receipt: `data/payoff_b_directional_riskset_weather_result_20261022.json`.
NASA source documentation: https://power.larc.nasa.gov/docs/services/api/temporal/hourly/
