# PAYOFF-B: spring northward-progress source-only stage-gate

Date: 2026-10-19. Study: Rotics et al. 2018, DOI 10.5441/001/1.v8d24552.

## Reason for a second pre-fit admission test

Original 273MB GPS file passed its checksum and linked all 1,207,130 GPS
fixes to 91 annual reproductive source rows. But at least 7 May-June
GPS dates were present in only 8 animal-years and those with numeric fledgling
outcomes in just 2. This is a **data-availability result** and does not
license narrowing a confirmatory outcome to 2 observations.

January-April location coverage is much wider. Instead of quietly relaxing
the frozen May-June completeness thresholds after observing the counts, this
separate **source-only, exploratory geometry audit** checks whether a
lower-latitude-to-higher-latitude trajectory can be measured during spring.
No fitted effect or reproductive outcome may be opened in this diagnostic.

## Locked procedure

- One original archived GPS file with strict original checksum validation.
- For the already verified breeding-deployment annual keys, collect daily
  mean latitudes from timestamps in January-April. No daily location may leave
  the CI runner.
- Require at least 5 distinct Jan-Feb dates and 10 Mar-Apr dates.
- Winter reference: median daily mean latitude over Jan-Feb.
- Spring northern range: 90th percentile of March-April daily latitude.
- Require at least +10° net spring northing versus the winter reference.
- First 20% and 80% of this latitudinal range are the only fixed checkpoints.
  If March 1's first observed spring day already exceeds 20%, classify the
  trajectory as left-censored rather than assigning a fictional onset.
- Report first crossing day-of-year and elapsed interval, aggregate quantiles
  and exact exclusion counts; never upload animal IDs, coordinates or daily
  positions.
- No individual fecundity slope or temperature/NDVI analysis is run.
- All findings are *northward progress proxies*; neither 80%-northing nor
  the end of a GPS track proves breeding arrival, stopover, real recourse,
  cue availability, or fitness rescue.

## Scientific use

A sufficient number of strictly classified within-route trajectories may
support a **future independently preregistered stagewise decision test**, once
a genuinely predecision cue, independent correction-opportunity measure, and
an appropriate independent field cohort are available.

Failure to admit enough data is a valid result and must not be 'rescued'
by tuning latitude thresholds against fledgling counts.

Workflow: .github/workflows/payoff-b-stork-spring-northward-progress.yml.
