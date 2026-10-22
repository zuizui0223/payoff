# PAYOFF-B complete GPS risk-day weather: clustered sensitivity verdict

Date: **2026-10-22**. Post-outcome sensitivity, NOT an independent confirmatory test.

## Provenance and sample

All three public original CC0 tracking sources and daily NASA POWER reanalysis were reread: 5,509 original stationary-at-risk opportunities, 333 raw later northward labels, 4,029 stable two-day continuations, 727 other movements, 420 right-censored followups. 809 unique 0.5° grid/year/month meteorology requests all succeeded. Strict prior-weather-only T2M, WS10M, V10M and incoming solar irradiance input dates (source anchor day -1 through -8) were preserved.

The original within-grid×year×month observational case-weighted contrast was audited with 1,000 **whole-individual-history bootstrap draws** (fixed seed 20261022), preserving all calendar years of each sampled identity. All 1,000 draws per source were estimable. Entire observation years were then removed one at a time without changing the weather estimand. No original identities, routes, GPS points or source weather cell identifiers are exported.

## Most informative descriptive patterns

| Source taxon | Environmental anomaly contrast | Case-weighted estimate | Descriptive animal-bootstrap 95% interval | Leave-one-year-out sign |
| --- | --- | ---: | --- | --- |
| Ciconia ciconia | Solar shortwave irradiance W/m² | -17.10 | [-27.63, -2.06] | Negative in all five omitted-year checks |
| Ciconia ciconia | Temperature °C | -0.51 | [-1.10, +0.09] | Negative in all five |
| Anser albifrons | Temperature °C | +1.04 | [+0.22, +2.00] | Positive in all five |
| Anser albifrons | 10m wind speed m/s | -0.47 | [-0.89, -0.16] | Negative in all five |
| Numenius arquata | Temperature °C | +0.34 | [-0.36, +0.92] | 2019 omission changes the sign |
| Numenius arquata | 10m northward wind component m/s | -0.61 | [-1.58, +0.23] | Negative in all years, but interval crosses zero |

These values represent **physical weather associated with retrospective northward GPS labels**, not proof of meteorological trigger, optimized behavior, available information, information-theoretic value, game-theoretic strategy or evolutionary fitness. Shared atmospheric variability among different birds/cells is not covered by whole-individual bootstrap; time-varying seasonal readiness, stopover stage, site quality and censoring may bias the contrasts.

The stork shortwave observation is counter to a simplistic claim that higher predeparture solar radiation must accompany all soaring migrants. However cloud cover, thermal-lift conditions, flight timing, route, and internal state are not measured. No physical reduction in solar energy is shown to cause departure. The goose physical warming / slower surface wind signal is a stronger observational candidate for preregistered testing in a genuinely untouched cohort, but the historical goose may overlap previously analysed PAYOFF data. Curlew environmental effects were not robustly distinguishable from zero with this descriptive sensitivity.

The previously opened V7R/V8 and registered stork 53-season non-support conclusions remain unchanged. The next independent ecological test must validate physical cues in real stage-specific context, route-relative winds at flight altitude, independent recourse, fate/fitness endpoints, and genuinely independent species/cohorts.

Actual source execution: https://github.com/zuizui0223/payoff/actions/runs/39725832808

Machine readable audit: `data/payoff_b_fullrisk_weather_robustness_20261022.json`.
