# Japan multi-taxon phenology × resource biomass: admission and testable contrasts

**2026-11-14 | biomass resource extension of PR #344; NO new biomass effect estimated**

## Existing real-data foundation

The JMA original 65 event CSVs yielded 160,367 calendar-valid station-year-event cells. This is phenology, **not** biomass. The station history source `smaster.index` was downloaded, hash-verified, and CP932-decoded, but the exact JMA phenology station-ID to meteorological station history crosswalk remains unverified. Temperature and NDVI have not yet been fitted.

## Separate three biologically different quantities

1. **Vegetation activity (NDVI):** green-up, seasonal greenness and vegetation condition. Useful for plants and herbivorous birds, but **not** measured plant biomass without calibration and not caterpillar biomass.
2. **Measured resource biomass:** independently sampled mass/area over time, e.g. forest litter/seed fall, above-ground vegetation, insect prey, or benthic prey. Keep dry/fresh basis, units, trap area, observation effort and resource guild. These are *different resources*; forest litterfall is not necessarily edible food.
3. **Consumer response:** frog first call/first egg mass, bird first call/first arrival/breeding output, insect first emergence/abundance, plant first bloom. A first-call observation alone cannot estimate population biomass, abundance or reproductive success.

## Real-data candidates and what they can identify

- **Monitoring Sites 1000 forest:** litterfall, seedfall, tree growth, bird counts; source inventory at https://www.biodic.go.jp/moni1000/findings/data/ . **Potential** vegetation production and consumer associations, but verify whether each downloadable table contains *measured mass*, date, area, and co-located bird outcomes. Do not equate litterfall with plant standing biomass.
- **Monitoring Sites 1000 satoyama:** frog egg-mass counts, bird counts, butterflies/fireflies. These provide consumer/reproductive indices, not measured biomass by default. Egg masses are count-based reproduction indices, not frog biomass.
- **JMA phenology:** first-call/first-sighting/flowering, matched to independent temperature and NDVI only after location history is verified.
- **Remote sensing:** MODIS/VIIRS NDVI, EVI, LAI/fPAR, NPP/GPP products. NPP/GPP are **carbon flux proxies/estimates** (mass carbon per area per time), not direct standing edible biomass. NDVI, NPP and measured biomass must be distinct model columns.
- **Trophic pair test:** in sites with verified repeated prey mass and brood outcomes, estimate resource-weighted demand-window biomass versus peak-date mismatch. Do not substitute resident bird records as migratory fitness.

## New executable measured-biomass bridge

`src/japan_phenology_biomass_bridge.py` requires repeated biomass density in g/m², sampling dates, sample area, mass basis, effort, source ID, and a resource guild. It integrates a declared demand window by piecewise-linear interpolation and **rejects extrapolation, sampling gaps over 14 days, mixed sites/guilds/dry-fresh mass and invalid data**. This is a measurement operator, not an empirical association.

Target contrasts, each on matched site-years with heldout-year/site validation:

- M0: biological event day ~ temperature + site + year;
- M1: M0 + NDVI green-up / peak / seasonal integral;
- M2: M0 + **measured guild-specific biomass magnitude or demand-window exposure**;
- M3: M0 + NDVI + measured biomass, testing whether measured food mass contributes beyond greenness.
- For frog first-call, bird first-song and first-sighting, avoid post-event demand windows as *predictive* features; demand-window exposure can be analysed as a separate **realized resource association** only.

A stronger hypothesis than generic warming response is **resource-dependent cross-guild decoupling**: climate and greenness may advance at different rates than insect prey or plant seed production, so amphibian/bird/insect phenology can shift without a corresponding increase in food quantity. This is falsifiable; not an established PAYOFF-B result.

## Hard stop

The current JMA event panel contains no source-verified biomass mass/area, no NDVI raster join and no matched reproductive fitness. **No M2/M3 effect, resource mediation, or biomass-driven migration adaptation is claimed.** Next required actual input: site-year original mass/area sampling table plus co-located consumer data and an independently verified coordinate crosswalk.
