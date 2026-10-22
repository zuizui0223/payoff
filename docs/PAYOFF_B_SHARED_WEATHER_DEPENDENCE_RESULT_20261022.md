# PAYOFF-B complete GPS risk-set meteorology: shared-weather dependence result

**2026-10-22 | source-backed exploratory sensitivity | Not confirmatory.**

## Reproduced source

Three original Movebank public CC0 GPS datasets were MD5 verified again. All
5,509 observed stationary-day risk entries and original labels, 809 daily
NASA POWER prior-weather batches, and the original within-0.5-degree
grid×calendar-year×month means/weights reproduced exactly.

The source outcome is a **retrospectively detected northward two-day GPS
movement**, not a bird's directly observed decision. Meteorology is
retrospectively reconstructed physical weather for source day -1, compared
with -2 through -8. No animal identities, GPS points, calendar dates or
meteorological grid-cell keys have been exported.

## Why the previous animal-bootstrap results were not sufficient

Different individuals can be exposed to the same meteorological field.
Sampling complete individual histories only does not account for that
additional shared exposure. This audit resampled **three progressively
broader weather blocks**, keeping every contributing bird-day in each
block together:

1. Original 0.5-degree weather grid × year × month.
2. Coarse 2-degree geographic weather supercell × year × month.
3. Entire year-month weather episode across the source's recorded locations.

Each resampling scale used **3,000 fixed-seed draws**. These are
descriptive bootstrap percentiles and leave-one-weather-block sensitivity
results, not evidence of independent atmospheric episodes or causal
confidence intervals.

## Observed source patterns

All contrasts are source case (later northward movement) minus source
two-day stay, for prior-day minus preceding-seven-days environmental anomaly,
computed within fine grid×year×month and averaged weighted by case-day count.

| Taxon / source variable | Original difference | 0.5° block 95% | 2° block 95% | entire year-month block 95% |
| --- | ---: | --- | --- | --- |
| Ciconia ciconia: incoming shortwave W/m² | -17.10 | [-31.19,-2.26] | [-31.31,-2.63] | **[-25.13,-7.47]** |
| Anser albifrons: T2M °C | +1.04 | [+0.15,+1.95] | [+0.12,+1.95] | **[-0.38,+2.28]** |
| Anser albifrons: WS10M m/s | -0.47 | [-0.86,-0.09] | [-0.88,-0.05] | **[-0.95,-0.01]** |
| Numenius arquata: T2M °C | +0.34 | [-0.57,+1.13] | [-0.70,+1.27] | **[-0.63,+1.34]** |

At the broadest year-month level, there are only **14 stork,
13 goose and 11 curlew distinct block labels**. The corresponding
case-weight effective block counts are about **9.03, 6.64 and 6.45**.
Even an interval narrowly excluding zero is not enough for a
species-general inference under such few shared weather episodes.

The full source also permits more restrictive within-*individual* and
within-*same 0.5° grid, year and month* comparison:

| Source | Animal identities with this overlap | Original matched case days | Same-animal temperature anomaly contrast °C | Solar contrast W/m² |
|---|---:|---:|---:|---:|
| Ciconia ciconia | 30 | 63 | -0.494 | -10.332 |
| Anser albifrons | 43 | 86 | +1.217 | +3.954 |
| Numenius arquata | 23 | 49 | +0.269 | -4.049 |

The within-individual filter is a *different observational subset* and
does not control elapsed time, readiness, weather autocorrelation or
weather-driven detectability. These estimates cannot be used to
retroactively redefine the original effect.

## Ecological interpretation and stop boundary

**Remaining robust descriptive pattern:** in this observed stork
cohort, the northern GPS movement source labels tend to be preceded by
*lower* shortwave radiation relative to recent local conditions than
source labels of continued stay. This survives several weather-block
sensitivity definitions but does NOT mean low sunshine causes soaring
flight. Solar radiation at a 0.5-degree source surface cell is not
measured convective lift or conditions at departure hour/flight height.
Cloud cover, route/site, season, delayed response and bird readiness
are plausible alternatives.

**Weakening evidence:** the earlier goose temperature range excluding
zero under whole-animal resampling now crosses zero when calendar
year-month is treated as a common weather episode. Goose wind-speed
source difference remains negative within this resampling scheme,
but few effective weather episodes, prior PAYOFF goose cohort overlap
and missing route-relative wind direction block strong generalization.
Curlew associations remain uncertain.

**No biological mechanism confirmed:** neither birds receiving
forecasts, climate predictability, information constraints,
irreversible departure choice, remaining feasible correction,
destination phenology, reproductive fitness nor evolutionary
coordination is identified by these source weather comparisons.

Prior registered V7R/V8 and stork 53-season non-support outcomes
are untouched. A genuinely independent cohort and independently
measured true migration stages/weather exposures are necessary.

Reproducibility:
- Source workflow: https://github.com/zuizui0223/payoff/actions/runs/39771294911
- Frozen original full weather: https://github.com/zuizui0223/payoff/actions/runs/39725093549
- Original whole-animal bootstrap: https://github.com/zuizui0223/payoff/actions/runs/39725832808
- Machine-readable receipt: `data/payoff_b_shared_weather_dependence_result_20261022.json`
