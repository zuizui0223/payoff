# PAYOFF-B: standalone MODIS-only geographic spring-coherence test — frozen exploratory design

Date: 2026-11-17. **OUTCOME-NOT-INDEPENDENT:** The eBird-conditioned 28-species V8 primary was already opened and found a positive change. This is a **post-open source-policy repair and robustness study**, not a new confirmatory directional hypothesis. Do not use the sign or magnitude as preregistered strengthening, or equate this with migratory bird information use.

## Source wall: no eBird fields or bird-specific range masks

Original geographic and vegetation source **only**: `br-amaral/BirdMigrationSpeed` commit `62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`, file `data/for_green-up_dl.rds`, which the original author describes as satellite-derived MODIS MCD12Q2 mid-greenup days and original `gr_ncell` forest-pixel count, on predetermined eastern North American hexagonal cells.

**Do not read** `data/final.rds`, `birdgreen.rds`, `data_arr.rds`, `species_Grid.RData`, species, arrival date, migration speed, `mig_cell`, `breed_cell`, or data derived from eBird. The original grid's **geographic domain** was chosen for an eastern North America bird paper and is not a random global plant sample; report this selection history.

Source row keys: `year`, `cell`, `cell_lat`, `cell_lng`, `gr_mn`, `gr_ncell`. Require source year in 2002–2017, unambiguous cell ID and coordinates, finite 1–366 calendar greenup, and original author's source quality standard `gr_ncell>10000` usable forest pixels. Duplicated cell-year or conflicting coordinates fail closed, not averaged.

## Single fixed pair selection (not bird-conditioned)

- From **all** source geographical cells with at least 6 usable annual midgreenup observations in each of the two windows, classify each cell as possible target.
- For target, choose the nearest *other* southern cell (`candidate latitude < target latitude`) in haversine distance, with maximum distance **800 km** and ties by original numeric `cell` identifier. Every eligible target gets one source, or no pair if there is no candidate.
- Targets and sources are selected **before computing any time series correlations**, using site geometry and source completeness only. Do not select pairs based on their correlation direction or prior V8 positive result.
- Pair is unique source-cell→target-cell and includes **no species label**. Require >=30 geographic pairs, >=15 distinct source cells, >=6 annual observations per pair in each window. If any fail, NO_GO. No substitute eBird-based bird-range information.

## Environmental estimand and uncertainty

Window EARLY 2002–2009, LATE 2010–2017, no overlap. Regress `gr_mn` separately on calendar year at source and target within each window; signed Pearson r of residuals is the independent environmental forecast coordinate. Report r_late−r_early at each geographic pair, unweighted mean across pairs, mean early and late correlation, number positive/negative.

The sole preregistered sensitivity coordinates for this new **exploratory** test are:
- same all-year geographic pairs under exactly 8/8 valid annual source-target records;
- alternative 7-year windows 2002–2008 vs 2011–2017, with >=6 paired years;
- source-pixel `gr_ncell` sampling-support change across windows, and negative-control raw (undetrended) correlation.
- 10,000 bootstrap draws of complete **source-cell blocks**, seed 20261117, carrying every target pair of a source together (to avoid treating shared environmental source as independent). Also show unclustered pair CI as diagnostic, not primary uncertainty.

No dynamic adjustment of spatial distance cap, pixel quality threshold, included years, or source selection to obtain a desired direction. No p-hacking by allowing long-range links when the gate fails.

## Biological and prior-art claim ceiling

A positive mean is only **rising environmental synchrony among selected nearby Eastern North American forest MODIS cells**. A negative mean is only decreasing synchrony. Either direction is exploratory and does not establish birds' available or used forecast cues, route-stage behavior, climate-change causality or trophic payoff. The eBird-conditioned V8 result is quarantined as not acceptable under the user's no-eBird research policy; this satellite-only output must not be presented as its independent replication (same MODIS source).

Source provenance and DOI: Amaral et al., `10.1111/ddi.70033`, associated Dryad `10.5061/dryad.ttdz08m6w`. Satellite original MODIS MCD12Q2, not measured biomass or GDD jerk. Separate potential ecological relevance from empirical support.
