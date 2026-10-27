# PAYOFF-B 2026-10-19: observable northward transfers and prior-day weather gate

## Source-level result, not a new ecological causality claim

From three published public CC0 GPS sources, a fixed five-day algorithm
identified **310 candidate stationary→northward transitions**:

| Original published species source | Candidates | Individual-years with ≥1 candidate | Consecutive five-day windows |
|---|---:|---:|---:|
| Ciconia ciconia | 145 | 80 | 5,848 |
| Anser albifrons | 106 | 46 | 2,496 |
| Numenius arquata | 59 | 41 | 2,156 |

These represent candidate transitions from 3 days in a 30-km stationary
area to ≥120 km of 2-day northward displacement, with distinct hourly fix
coverage. Multiple events can be associated with the same animal. The
source collections are neither independent experimental replications
nor proof of stopover decisions; the goose cohort may overlap the
historical PAYOFF goose data.

GitHub source run:
https://github.com/zuizui0223/payoff/actions/runs/39225406150

## Pre-movement meteorology availability pilot

Before weather outcome access, 12 distinct animal-year candidates per
taxon were sampled using a fixed non-behavioral SHA256 order, totaling
36 candidate events. The location was coarsened to a 0.5° grid before
issuing requests to the public NASA POWER hourly source. The weather day
was *the UTC calendar day before the last stationary candidate day*, not
the day when onward movement became observed.

All **36/36 sampled candidate events** returned 24 valid hourly values
for both T2M (°C) and WS10M (m/s). The three descriptive averages were:

| Source species | N sampled | Temp °C | Wind speed (10m) m/s |
|---|---:|---:|---:|
| Ciconia ciconia | 12 | 12.0875 | 4.6191 |
| Anser albifrons | 12 | 5.8652 | 4.3343 |
| Numenius arquata | 12 | 5.2047 | 4.4861 |

Those temperature/wind contrasts are not comparable ecological preferences
or species-level forecast reliability: geographic and annual sampling
differ. NASA POWER is historical meteorological **reanalysis** and is
not proof that a bird perceived those specific conditions. A three-day
stationary centroid is not a known exact departure point, and the first
post-stationary movement day is not a precise commitment instant.

Weather source run:
https://github.com/zuizui0223/payoff/actions/runs/39226252405

## What remains before the central ecological claim

The signed environmental-information × remaining-recourse × action mechanism
is **not tested**. To move to a new prespecified biological hypothesis,
first validate stationary→move candidates against raw within-day GPS fixes
to bracket departure; measure independently available weather cues
without accessing after-departure weather as explanatory signals; define
route-independent physical opportunities to advance/delay; then test
downstream signed decisions with individual/study/flyway/year dependence.
All source-selected examples remain exploratory after the V7R/V8 nulls
were opened.

No raw bird identities or coordinates, including restricted sensitive
habitats, are included in the repository-derived result artifacts.
NASA POWER documentation:
https://power.larc.nasa.gov/docs/services/api/temporal/hourly/
