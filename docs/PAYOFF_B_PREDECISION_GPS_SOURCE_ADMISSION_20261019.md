# PAYOFF-B: source-only departure / stopover checkpoint admission contract

Date: 2026-10-19. Implemented **after prior northward-source
geometry and exploratory stage-slope results were opened**. This is
therefore source eligibility exploration, NOT confirmation of a
pre-registered PAYOFF-B information/recourse mechanism.

## Original high-frequency source sets

Only independently archived CC0 **GPS** sources with known original
checksums are included: Ciconia ciconia (Rotics 2018), Numenius arquata
(Schwemmer 2021) and Anser albifrons (Kölzsch 2016). The latter's cohort
may overlap prior PAYOFF goose tracks. Woodcock Argos is excluded from
the GPS event algorithm because its geolocation uncertainty differs:
this is a sensor-eligibility decision, not absence of real stopovers.

## Frozen five-day candidate detector (before opening these event counts)

- Use February-May original timestamped WGS84 locations, grouped by source
  taxon, animal identity and calendar year. UTC daily position = arithmetic
  mean latitude and circular mean longitude.
- A day is eligible if at least **two distinct recorded UTC hour bins**
  are present, avoiding duplicate/rapid repeated fixes being mistaken for
  two independent time samples.
- Require five consecutive eligible calendar days without interpolation.
- The first 3 daily positions must all fall within 30 km of their
  3-day center (candidate stationary period).
- Day 4 must lie >=30 km from the stationary center; day 5 must lie
  >=120 km from that center and >=0.8° farther north.
- Collapse multiple potential events within 7 days, preserving the first
  one. Report all five-day windows and event yields, even when zero.
- These are **stationary→northward movement candidates**, not verified
  stopovers, *actual departures*, or observation of the instantaneous
  information available to the animal.

No individual ID, exact track coordinate or specific event date is
written to output. Original checksums, source season and invalid-record
counts remain inspectable. No environmental variable, route-feasible
counterfactual, causal inference, fitness measure, or timing-response slope
is computed by this gate.

## Next biological information gate (not yet claimed)

An external hourly or daily meteorological source must be linked only
to local conditions recorded *strictly before the last stationary
observation*, rather than using observed departure-day or future weather
as if available at commitment. A candidate must then have actual
timestamped fixes bracketing the transition. Feasible advancement and
delay options should be estimated from **different individual histories**
and sensor biases separately. Reanalysis of previously published
weather effects from original papers is prior art.

External candidate sources:
- NASA POWER hourly API, time-standard=UTC:
  https://power.larc.nasa.gov/docs/services/api/temporal/hourly/
- Open-Meteo historical ERA5 reanalysis:
  https://open-meteo.com/en/docs/historical-weather-api

Reanalysis describes historical local physical conditions, not what a
migrant actually perceived or what a forecasting model issued then.
No information-actionability gain is identifiable until that distinction
and an independent decision/outcome panel are resolved.
