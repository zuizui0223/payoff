# PAYOFF-B: randomized disjoint flowering-reference sensitivity

**2026-11-15 | PR #362 | original-data CI https://github.com/zuizui0223/payoff/actions/runs/43674757504 | 99 tests passed**

The previous single deterministic split gave 2001–2020 independent plant-reference lag correlation r=+0.031927. To test reference-selection sensitivity, randomly partition original flowering event files into disjoint source-file sets 200 times per 20-year fixed-composition window (seed 20261115), evaluate both B−Pa versus I−Pb and swapped orientations, and require all four event groups at identical stations in all 20 years.

| Fixed 20-year window | Plant source files | Valid orientations | Median r | 5th–95th percentile of split outcomes | Positive fraction | Detrended median r | Matched station range |
|---|---:|---:|---:|---|---:|---:|---|
| 1961–1980 | 20 | 400 | −0.083315 | −0.450336 to +0.209944 | 0.3475 | −0.014862 | 20–34 |
| 1981–2000 | 28 | 400 | +0.352399 | −0.035875 to +0.577086 | 0.8950 | +0.309342 | 47–53 |
| 2001–2020 | 26 | 400 | +0.356747 | −0.184808 to +0.670260 | 0.8700 | +0.374708 | 28–33 |

**Interpretation:** One arbitrary source-file split cannot support a categorical claim that independent-reference co-fluctuation disappears. Across randomized disjoint splits, recent periods are predominantly positive but reference selection materially affects estimates; negative results are possible. The originally shared-reference r=+0.877 is still inflated relative to randomized disjoint-reference medians, and must not be interpreted as independent trophic mismatch synchrony.

**Uncertainty:** These 400 draws are not independent observations, confidence intervals or a climate null; 200 randomized splits are reused with reversed orientation. Station sets vary between splits, potentially confounding reference identity with station coverage. The fixed 20-year source-event completeness criterion selects a restricted observation network. JMA biological rm semantics and observation effort are not certified. Climate, NDVI, biomass, food overlap and fitness are not measured in this analysis.

**Next:** hold the *same* eligible stations across every reference partition (common support), repeat with disjoint plant source sets, and independently measure climate covariates and resource availability. The central biological question remains whether annual timing co-fluctuation reflects common climatic cues or realized resource mismatch.
