# First original-data cross-taxon timing screen: JMA nationwide

**2026-11-14 | PR #348 | original source run https://github.com/zuizui0223/payoff/actions/runs/43600128749**

## Data and method

- JMA all-species archive: 65 source event CSV files; 160,367 calendar-valid station-year event-date cells. Original source event labels classify 3 amphibian, 6 bird, 15 insect, 41 plant-or-unclassified files; labels are provisional and the plant group requires a manual audit.
- For each event × station series with >=8 observations, subtract its observed mean day of year; within the same station and year, pair centered events from different provisional groups.
- Calculate pooled Pearson r across all such event-pair-year cells. These cells **reuse the same station-year repeatedly**, so they are *not independent observations*. Report stations and event-series pairs as coverage, not a pseudo-replicated sample size for inference.
- Original JMA `rm` codes have not been independently interpreted or quality-screened; cross-taxon event definitions, effort and changes in detection may differ. No climate, NDVI or biomass variable was fitted.

## Exploratory observed correlations

| Event groups | Station IDs with paired years | Event-series pairs | Reused pair-year cells (NOT N independent) | Pooled anomaly Pearson r |
|---|---:|---:|---:|---:|
| Amphibian–insect | 78 | 1,462 | 40,668 | +0.154759 |
| Amphibian–bird | 77 | 561 | 15,382 | +0.119125 |
| Bird–insect | 100 | 3,647 | 148,730 | +0.071471 |
| Amphibian–plant or unclassified | 77 | 2,848 | 77,211 | +0.036813 |
| Bird–plant or unclassified | 101 | 7,452 | 299,497 | +0.018433 |
| Insect–plant or unclassified | 101 | 19,508 | 762,678 | +0.017763 |

## Interpretation boundary

The pooled r values are all small, and the present screen does **not** establish strong nationwide cross-taxon synchrony. However, the pooled event-pair weighting, different phenological seasons, leap-year DOY offsets, non-overlapping observation periods, mixed event types, and source-quality codes prevent interpreting these as estimates of true community mismatch or species interactions. These are descriptive **observed-event** statistics only. The current correlations do not test biomass, food supply, migration payoff, or climate cue selection.

## Required next validation

1. Source-certify `rm` meanings and event definitions; separate first call, first sighting, flowering, leafout and other source events. Avoid treating all plant events as the same biological stage.
2. Recalculate by exact event pair and overlapping station-year periods, with one equal-weight estimate per station/event pair and clustered uncertainty by station and year.
3. Correct leap-day DOY comparison using a common non-leap seasonal scale or explicit calendar-date model.
4. Fit weather predictor blocks (thermal, hydrological, radiative, moisture and wind) on the same matched station-event-years; then add NDVI and **independently measured** biomass, avoiding interpretation of greenness as prey mass.

**No ecological mechanism or statistical significance has been established by this screen.**
