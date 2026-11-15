# PAYOFF-B Tokyo March–April 2019–2021: first measured interannual weather comparison

**2026-11-15 | PR #365 | original JMA source CI https://github.com/zuizui0223/payoff/actions/runs/43678262836 | 102 tests passed**

Read six original JMA Tokyo daily observation HTML pages for March and April 2019, 2020, 2021 (61 days/year, 183 source days in total). Each page SHA-256 and variable-specific numeric coverage are in the workflow receipt `jma_tokyo_multiyear_weather_pilot.json`.

| Year | March mean daily temperature °C | April mean daily temperature °C | March–April mean °C | Sunshine hours sum | Mean RH % |
|---|---:|---:|---:|---:|---:|
| 2019 | 10.5613 | 13.6400 | 12.0754 | 363.2 (60/61 numeric days) | 61.3279 |
| 2020 | 10.7355 | 12.8033 | 11.7525 | 395.3 (61/61) | 65.2459 |
| 2021 | 12.7645 | 15.1067 | 13.9164 | 411.7 (61/61) | 61.0328 |

2021 March–April mean temperature minus 2020 = **+2.1639 °C** (descriptive difference of two source periods, not a climate trend). All three years have complete daily mean temperature display coverage.

**Not admitted to a weather–phenology effect model:** these are HTML display observations, not certified original CSV variable-specific quality/homogeneity numbers; weather station code `47662` is not independently crosswalked to original biological phenology station ID `662`; only one site and three years; no station-year climate anomaly baseline, resource biomass, NDVI, or event-date coefficient. The source pages can support measured interannual climate contrasts, but not causal mismatch inference.

Next: obtain original downloadable CSV quality/homogeneity and verified station metadata crosswalk, then extend to a fixed multi-station, multi-year panel and fit climate anomalies against biological event-date lag anomalies with held-out years.
