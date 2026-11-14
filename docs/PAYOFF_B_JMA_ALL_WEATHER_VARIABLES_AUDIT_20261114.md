# JMA complete meteorological candidate screen for Japanese multi-taxon phenology

**2026-11-14 | source-verified menu and executable feature gate; no weather effect fitted**

The official JMA [historical weather CSV interface](https://www.data.jma.go.jp/risk/obsdl/) and [download guide](https://www.data.jma.go.jp/risk/obsdl/top/help1.html) were directly inspected. They support hourly/daily/5-day/10-day/monthly aggregates and station-/year-specific availability. The official menu contains:

- **Thermal:** mean/max/min temperature; heat/frost day counts, degree-days, short-term thresholds.
- **Hydrological:** daily rainfall, precipitation frequency, dry spells; snowfall and snow depth, thaw and snow-free duration.
- **Radiative:** sunshine duration, daily global solar radiation (primarily weather offices), cloud cover.
- **Atmospheric water:** relative humidity, vapour pressure, derived vapour-pressure deficit if source variables co-occur.
- **Mechanical/storm:** mean/max/gust wind, wind direction; pressure, fog, thunder, daytime/nighttime weather summaries.
- **Background:** climatological normals and departures (1991–2020), and observed time-of-extreme where supported.

**Critical measurement discontinuity:** JMA's [historical update log](https://www.data.jma.go.jp/risk/obsdl/top/whatsnew.html) documents AMeDAS sunshine hours switching from instrument observations to satellite-derived estimated sunshine hours on **2021-03-02**. It is a protocol break and cannot be interpreted as a sudden biological change. Weather station moves, historical data revisions, instrument changes and JMA quality flags must also be handled explicitly.

**Do not pretend all stations measure all variables.** The official guide distinguishes weather offices from AMeDAS stations and notes varying historical coverage; cloud, pressure, vapour pressure, solar radiation and some humidity observations are less widespread than temperature/precipitation.

## Registered modeling hierarchy

1. **M0:** seasonality, latitude/elevation, station and year structure, observation-process changes; no climate predictors.
2. **M1:** thermal (Tmean/Tmin/Tmax, growing-degree days, frost, 7/30/60/90-day antecedent windows).
3. **M2:** M1 + hydrology (precipitation sum/frequency/dry spells, snow depth and snowmelt).
4. **M3:** M2 + radiative and moisture stress (sunshine, global radiation where available, relative humidity, vapour pressure/VPD).
5. **M4:** M3 + wind/storm/pressure and separately sourced QA-masked NDVI.
6. **M5:** M4 + **independently measured resource biomass**, retaining biomass guild, dry/fresh basis, effort and demand-window support.

**Important:** Compare M1–M5 on *identical* station-event-years when evaluating incremental predictive scores; otherwise coverage differences masquerade as effects. Where variables are only measured at a small subset of stations, fit nested **availability-stratified** comparisons and report geographic/temporal selection. Use grouped feature blocks, not uncontrolled 100s of independent variable searches. Lag windows must end before first-call/first-sighting for forecasting; concurrent/post-event biomass is only a separate realized association.

## Biology-specific hypotheses, not confirmed results

- Frog first calls / spawning: accumulated heat **and** rainfall, relative humidity, snowmelt.
- Birds first call / arrival: temperature, wind and pressure/weather fronts, and green-up as an indirect cue/resource proxy.
- Insects emergence: degree-days, frost events, rainfall, moisture stress and wind-dependent detectability.
- Plants flowering/leafout: chilling, forcing GDD, winter snow and solar radiation.
- Resource production: sunshine/radiation and moisture influence NDVI and carbon flux; measured plant/seed/prey mass is a distinct response. Multi-taxon mismatches can arise when thermal forcing, rainfall, snowmelt and prey biomass change on different clocks.

## Code and evidence

- Original JMA phenology 65 event tables, 160,367 calendar-valid cells: `docs/PAYOFF_B_JMA_MULTITAXON_PANEL_FIRST_RESULT_20261114.md`.
- Station metadata ZIP `smaster.index` already fetched and checksum-verified, but its ID crosswalk is not yet certified.
- Machine-readable official menu: `data/payoff_b_jma_meteorological_covariate_registry_20261114.json`.
- Leakage-safe, quality-code-preserving feature extractor: `src/japan_phenology_jma_multivariate.py`.
- Tests: `tests/test_japan_phenology_jma_multivariate.py`.

**No measured temperature/rainfall/humidity/snow/wind/NDVI/biomass coefficient has been fitted.** Official JMA CSV download is interactive and warns against excessive automation. The present task records its available fields and prepares the join without scraping the interface at scale.
