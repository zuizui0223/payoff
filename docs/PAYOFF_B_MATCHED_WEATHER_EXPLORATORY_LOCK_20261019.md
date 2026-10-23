# PAYOFF-B matched predeparture weather: exploratory prereading lock

Date 2026-10-19. Previous V7R/V8 and original stork 53-season timing
hypotheses are NOT SUPPORTED and remain unchanged.

## Frozen source sample selection

Use original CC0 GPS stork, white-fronted goose and curlew sources. Original
stationary to northward movement candidate counts are 145, 106, and 59.
A separate, preweather source audit matched 38, 41 and 36 distinct
individual-years to a prior stationary nondeparture opportunity at
a similar source location, 5-21 days earlier. Original hourly GPS bracketing
within <=24h was admitted for 32, 32, and 25 source pairs.

Before opening any paired weather, select up to **12 distinct individual
years per source**, using the locked SHA256 of original source identity
and date, with exactly one case/control pair per identity-year, from the
24h-bracket-passing source universe. Require >=10 complete weather pairs for
each source separately. Do NOT choose favorable response signs, extend the
bracket width, widen the spatial matching radius or alter calendar-gap
restrictions if an estimate is non-significant.

## Physical reanalysis variables available before the decision

For each source location, coarsen to half-degree grid *before* external
request. Use historical NASA POWER T2M and WS10M hourly values in UTC for
the inclusive 8-day window from **eight calendar days before** the reference
stationary source date to **one day before** it. All 8 days must have at least
18 valid hourly records per variable. The day before is the "recent" value;
the seven earlier days are the "preceding baseline". No weather observed
after the stationary reference day can enter any covariate.

For both the eventual movement case and same-individual prior stationary
control calculate:
- mean prior-day temperature and 10m wind speed;
- anomaly: prior-day mean minus previous 7 days mean;
- pair differences = case minus stationary control for both raw physical
  weather and the seven-day anomalies.

Report per species n, signs, mean, median, 3,000 paired bootstrap draws'
95% descriptive intervals, missingness, and case-control calendar gap. No
cross-species pooled effect, no one-sided p-values and no selection by sign.
Bootstrap intervals are descriptive rather than a calibrated test of causal
cue use because of selection and differing reference dates.

## Identification limits (mandatory in any ecological discussion)

Historical NASA POWER weather is a physical reanalysis, **not** a forecast
issued to the bird. An event detector that uses the next two days to label
cases conditions on the outcome. Controls occur 5-21 days earlier in the
same stopover, so an approaching seasonal front, ongoing phenology,
migratory readiness, fat stores or diel scheduling can confound the weather
contrast. Wind speed alone cannot establish tailwind assistance.

The output can support only an exploratory *association* between
pre-movement weather and later-detected departure versus staying at the
same stopover. It cannot establish forecast learning, species-general
actionability, voluntary recourse, active phase correction or fitness.
No original GPS IDs, exact observation dates, source locations or
individual weather responses are uploaded.
