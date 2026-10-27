# PAYOFF-B: weather descriptives from all stationary-source risk days

2026-10-22; exploratory source outcome after registered risk-set extraction, NOT a confirmatory ecological mechanism.

## Source population and weather sample

The complete observational risk set from original CC0 GPS contains **5,509** eligible
three-day stationary source opportunities, including **333** raw northward
source labels, **4,029** continuing stays, **727** other movements and **420**
right-censored future intervals. The original source 7-day-deduplicated
145/106/59 case counts remain reproducible.

A weather-blind, original source-ID/year/day SHA256 round-robin across
February-May chose **16 future northward-labelled days and 32 stable
nonmovement-labelled days per taxon**, one opportunity per animal-year and
status. This is **outcome-stratified case/control sampling**, not population
hazard sampling; do NOT interpret sampled 16/(16+32) as an individual
departure probability.

All **144/144** sampled source-day NASA POWER queries returned sufficient
T2M and WS10M hourly conditions strictly before the stationary reference
day (last UTC day minus the previous 7-day mean). Request points were
rounded to 0.5°; event IDs, real coordinates and individual observed
dates never leave the worker.

## Preliminary taxon-specific environmental patterns

Contrast = mean (prior-day minus previous 7-day mean) on northward-labelled
stationary days minus the same lagged weather anomaly on continuing-stay
stationary days.

| Taxon | Cases / stays | Mean temperature anomaly case (°C) | Stay (°C) | Case-minus-stay difference (°C) | Case-minus-stay wind speed anomaly (m/s) |
| --- | --- | ---: | ---: | ---: | ---: |
| Ciconia ciconia | 16/32 | -1.3275 | +0.6902 | -2.0178 | +0.7596 |
| Anser albifrons | 16/32 | +1.7945 | +1.2357 | +0.5588 | +0.3192 |
| Numenius arquata | 16/32 | +0.4569 | -0.2518 | +0.7087 | +0.0165 |

These are **SOURCE DESCRIPTIONS**, not covariate-adjusted case/control
effects. Month-specific differences are also retained in full source
receipts. In storks, the negative temperature pattern appears in March
and April in the selected small sample; in white-fronted geese, signs
differ between months. The source is neither representative of annual
departure rates nor independent of individuals/years/habitat.

## Biological conclusion ceiling

No universal positive warming trigger is apparent in this small subset,
but neither a general absence of thermal triggering nor a taxon-specific
actionability mechanism follows. Source timing, location, stage, season,
individual readiness, wind direction and species movement strategy remain
confounders. All source samples use retrospective future-GPS labels and
all environmental values are historical physical reanalysis, **not**
bird-observed forecast information. Wind speed without direction is not
a route-relevant tailwind. The true ecological information×deadline model
and reproductive/survival benefit are NOT tested.

Next design must validate stage-identified departure and route context,
add directionally meaningful predecision winds and date/site climatology,
use clustered risk-set inference with source-specific held-out cohorts,
and estimate feasible recourse without using focal future action.

Results: https://github.com/zuizui0223/payoff/actions/runs/39722927455
Raw source denominators: https://github.com/zuizui0223/payoff/actions/runs/39721821673
Machine-readable aggregate receipt:
`data/payoff_b_complete_riskday_weather_20261022.json`.
