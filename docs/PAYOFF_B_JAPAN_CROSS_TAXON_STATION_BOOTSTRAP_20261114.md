# Station-resampled uncertainty: original JMA cross-taxon timing

**2026-11-14 | PR #350 | original-data GitHub Actions https://github.com/zuizui0223/payoff/actions/runs/43604357483 | 69 tests passed**

Recompute exact JMA event-pair correlations within each station on at least 10 shared years. Aggregate event-pair correlations within each station, weight stations equally, then resample **station units** 1,000 times (fixed seed 20261114). This avoids treating reused event-pair-year cells as independent replicates, but is conditional on the observed network and does not correct source quality or observer effort.

| Groups | Stations | Mean station r | 1,000 station-resample percentile 95% interval |
|---|---:|---:|---:|
| Amphibian–insect | 73 | 0.156474 | 0.121383–0.188081 |
| Amphibian–plant/unclassified | 75 | 0.135725 | 0.109016–0.162769 |
| Insect–plant/unclassified | 101 | 0.119561 | 0.101385–0.138287 |
| Amphibian–bird | 74 | 0.112540 | 0.078799–0.145387 |
| Bird–plant/unclassified | 101 | 0.095377 | 0.080861–0.109490 |
| Bird–insect | 100 | 0.085007 | 0.069467–0.101029 |

All resampled intervals are above zero; this is descriptive stability across the observed stations, **not** evidence of ecological synchrony significance under observation selection, phylogenetic dependence or weather confounding. In particular, all source `rm` codes remain uninterpreted, source phenology event types are heterogeneous, the plant/unclassified grouping is provisional, leap years are not harmonized, and no actual daily meteorological/NDVI/biomass predictors have been fitted.

**Next empirical gate:** verify source `rm` quality meanings and observation event types; obtain actual JMA weather time series for the temporally valid station IDs; compare thermal, rainfall, snow, radiation, moisture and wind blocks on identical station-event-years, then separate NDVI and measured biomass.
