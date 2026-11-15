# PAYOFF-B interannual observed phenology lag synchrony: first real 60-year screen

**2026-11-15 | PR #358 | original JMA source run https://github.com/zuizui0223/payoff/actions/runs/43668459528 | 95 tests passed**

## Definition

For each station and exact original event-file pair with >=10 overlapping years (1961–2020), calculate `lag(s,p,y) = DOY_A(s,p,y) - DOY_B(s,p,y)`. Then subtract the *pair's own* mean observed lag across its shared years, yielding `lag_anomaly(s,p,y)`. Average all eligible event-pair lag anomalies **within each station-year** before national year summaries. Do not pool event-pair-year cells as independent units. Leap day removed; dates normalized to a common 365-day DOY.

Positive anomalies mean the first group's event occurred relatively later than the second group's event *compared with the same station/event pair's observed average*, not necessarily a biologically harmful mismatch. The reported mean of absolute station anomalies is not food-resource mismatch or fitness loss.

## Real national annual series

Each of the three comparisons has 60 years meeting >=10 stations per year:

| Contrast | Event pairs | 1961 stations / mean anomaly days | 2020 stations / mean anomaly days | Highest observed mean year | Lowest observed mean year |
|---|---:|---|---|---|---|
| Bird first sighting – plant flowering | 1,201 | 80 / +2.873 | 49 / +2.816 | 2011 +9.193 (49 stations) | 1981 −8.599 (84 stations) |
| Insect first sighting – plant flowering | 4,649 | 84 / −7.152 | 52 / +5.591 | 1996 +9.941 (91 stations) | 2016 −9.331 (54 stations) |
| Bird first sighting – insect first sighting | 331 | 75 / +8.979 | 45 / −2.907 | 1961 +8.979 (75 stations) | 1981 −6.279 (78 stations) |

**Critical comparability limitation:** the source event-pair means are calculated over different observation windows and stations; the composition of contributing stations and event pairs changes annually. The 1961–2020 difference is not an identified trend or a causal climate effect. Changes in source observation effort, 2020 event termination, and original JMA `rm` code meanings are unverified.

## Next identification steps

1. Freeze a common set of source event pairs and stations across fixed year windows, then recompute annual anomalies and geographic concordance; compare to this changing-composition series.
2. Model annual `lag_anomaly` with independent observed **temperature, precipitation, snow, radiation, humidity and wind** anomalies for the *same station-year* and season; preserve pre-event-only climate windows, historical station metadata and quality/homogeneity regimes.
3. Separate environmental cue synchrony (shared weather response) from **resource mismatch** (independently measured food biomass/availability and demand overlap). NDVI is greenness, not food mass.
4. Examine cross-group synchrony of annual national anomalies, spatial covariance, station-block uncertainty, and prospective out-of-year prediction. Do not interpret year extremes as ecological causal events without measured climate.
