# Spring stage-matched JMA original-data timing comparisons

**2026-11-15 | PR #353 | source run https://github.com/zuizui0223/payoff/actions/runs/43660299570 | 79 tests passed**

The previous all-year taxon-pair association pooled unrelated event types and phenological seasons. This analysis predeclares an original-event median DOY 45–160 spring window, restricts source stages to first call, first sighting and flowering, and compares exact event pairs on >=10 overlapping station-years. Station means are equally weighted; station-unit bootstrap percentile intervals use 300 resamples. The selection is based on **event-wide median timing**, not on whether every individual observation falls in the spring interval.

| Contrast | Stations | Equal-station mean r | Station-resample percentile 95% interval |
|---|---:|---:|---:|
| Amphibian first call × plant flowering | 41 | 0.158582 | 0.107637–0.202473 |
| Insect first sighting × plant flowering | 97 | 0.155866 | 0.130183–0.184296 |
| Amphibian first sighting × plant flowering | 67 | 0.143741 | 0.106058–0.183956 |
| Bird first call × plant flowering | 100 | 0.134708 | 0.113825–0.152444 |
| Bird first sighting × plant flowering | 89 | 0.126097 | 0.098930–0.149828 |
| Bird first sighting × insect first sighting | 84 | 0.121112 | 0.089456–0.147782 |

The insect first-sighting group includes モンシロチョウ, キアゲハ, シオカラトンボ and ホタル; bird first sighting includes ツバメ. First calls include source-labelled birds and ニホンアマガエル. These are **not** established food-web links: same-season observational timing is not evidence of direct consumption, pollination, fitness, biomass or migration payoff.

**Unresolved:** original `rm` semantics, observation effort, calendar-year event definitions, stage-specific observation process, weather/NDVI/biomass data joins and effect estimates. The positive descriptive correlations must not be promoted to a climate-driven mechanism until actual JMA daily weather covariates are joined on temporally valid station records.
