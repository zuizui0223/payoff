# PAYOFF-B: original 2023 climate-adjusted timing-gap fitness prediction (2026-11-15)

Reproducible GitHub Actions: https://github.com/zuizui0223/payoff/actions/runs/43707053421

Original 2023 Dryad data, byte-identical Zenodo mirror, source SHA256 verified. Include=1, site/species/year means, minimum 5 broods per year; leave-one-year-out cross-validation within six population-species strata. Temperature proxy: March-April mean daily (TN+TX)/2 from KNMI deBilt or deKooy. Same 3-4 month temperature window chosen before examining the results.

## MSE reduction when adding caterpillar peak minus mean first egg day to temperature

Positive means incremental prediction improvement; units are squared outcome units, not regression coefficients.

| Population/species | Years | Corrected fledglings | All-brood recruits |
|---|---:|---:|---:|
| Hoge Veluwe Blue Tit | 43 | -0.1249937 | -0.0035484 |
| Hoge Veluwe Great Tit | 47 | -0.1114509 | -0.0050760 |
| Oosterhout Blue Tit | 25 | -0.0804503 | +0.0010197 |
| Oosterhout Great Tit | 28 | +0.1203661 | -0.0081757 |
| Vlieland Blue Tit | 19 | -0.4665060 | -0.0063477 |
| Vlieland Great Tit | 19 | -0.1549926 | -0.0157176 |

**Result:** only 2/12 endpoint × population/species comparisons improved. In each endpoint, 1/6 population/species strata improved. Peak biomass added to temperature alone worsened prediction in all 12 comparisons.

**Critical caveat:** For corrected fledglings, temperature-only was worse than intercept-only in *all six* strata (intercept minus temperature MSE was positive in all six). For recruits, temperature-only beat intercept in some but not all. Thus an improvement over temperature-only does not establish predictive value beyond a strong intercept-only baseline. The temperature covariate was much more effective for *phenological dates* than for fitness.

**Other limitations:** Observed bird date is first egg; resource date is peak caterpillar biomass; their difference is not chick-demand food overlap. Year-aggregated mean fitness is not individual selection. Original recruitment counts include all broods. Fixed calendar temperature window may be suboptimal for different sites/species, but optimizing it post hoc would require nested CV. Climate station-to-site crosswalk is a proxy. Exploratory multiple comparisons, no confirmatory significance, causal effects, or independent taxon validation.

**Next:** compare both temperature+gap and intercept-only on identical held-out years, inspect source code's chick demand definition and obtain daily caterpillar biomass curves if available. No mechanism claim before these checks.
