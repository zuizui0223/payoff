# PAYOFF-B Japan: station-balanced coupling robustness — actual data

**2026-11-14 | PR #349 | original-data run https://github.com/zuizui0223/payoff/actions/runs/43601308504 | 68 tests passed**

The original 65 JMA phenology event CSVs yielded 160,367 calendar-valid event-date cells. We recomputed correlations on exact source-event pairs within the same station and overlapping years (>=10 years). Each station is weighted equally in nationwide summaries, unlike the earlier pooled event-pair-year estimate. We also remove a separate linear year trend within each event pair to test whether results are entirely driven by a shared monotonic trend.

| Groups | Stations | Equal-station mean r | Fraction stations positive | Detrended equal-station mean r |
|---|---:|---:|---:|---:|
| Amphibian–insect | 73 | +0.156474 | 0.917808 | +0.131329 |
| Amphibian–plant/unclassified | 75 | +0.135725 | 0.933333 | +0.154118 |
| Insect–plant/unclassified | 101 | +0.119561 | 0.960396 | +0.138017 |
| Amphibian–bird | 74 | +0.112540 | 0.743243 | +0.118187 |
| Bird–plant/unclassified | 101 | +0.095377 | 0.910891 | +0.100196 |
| Bird–insect | 100 | +0.085007 | 0.930000 | +0.078439 |

**Interpretation:** The earlier pooled r values were sensitive to event-pair-year weighting. Equal station weights yield consistently positive but small average associations. Positive station-level correlations are common across the observed network. Linear detrending does not remove the positive average. This is an exploratory descriptive result, **not** a statistical test of nationwide ecological synchrony, and does not establish a causal climate mechanism.

**Unresolved methodological risks:** Original `rm` codes remain uninterpreted; event types are heterogeneous (first calls, first sightings, flowering, etc.); plant/unclassified label is provisional; calendar-year DOY includes leap-year differences; station observations are not independent across pairs; observer effort, site/year missingness, observation discontinuities and event-season mismatches are not controlled. The detrending is linear only and does not adjust for nonlinear shared environmental effects. No inferential p-values or CIs are reported.

**Next empirical step:** Source-certify `rm` codes, separate event types and seasons, perform a matched station-year clustered/bootstrap sensitivity, then join actual daily temperature, rainfall, snow, sunshine, humidity and wind. Independently measured biomass and QA-screened NDVI must remain separate; no effects have been fitted yet.
