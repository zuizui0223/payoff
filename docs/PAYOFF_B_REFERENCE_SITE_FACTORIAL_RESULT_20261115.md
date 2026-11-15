# PAYOFF-B plant reference × station support factorial sensitivity

**2026-11-15 | PR #364 | original JMA run https://github.com/zuizui0223/payoff/actions/runs/43677047531 | 101 tests passed**

To separate the two changing dimensions in prior independent flowering-reference sensitivity, enumerate up to 500 lexicographically ordered sets of four original flowering event files in each 20-year block. Require >=10 stations with bird, insect and all four plants continuously observed. For each admitted four-file set, evaluate all six oriented disjoint 2-vs-2 references twice: (1) strictly identical stations with all four plants; (2) variable station set requiring only one plant from each reference half. The same plant files and orientation are held fixed within each paired comparison.

| Window | Four-file sets examined | Admitted >=10 strict stations | Range of subset median r at strict support | Median across subsets of paired (variable−strict) r | Fraction of strict subset median r > 0 |
|---|---:|---:|---|---:|---:|
| 1961–1980 | 500 | 22 | −0.373631 to +0.308708 | +0.020321 | 0.681818 |
| 1981–2000 | 500 | 53 | −0.375333 to +0.675559 | −0.054765 | 0.584906 |
| 2001–2020 | 500 | 24 | **−0.277954 to +0.522248** | **+0.076288** | **0.416667** |

**Inference:** Both plant-source choice and site support affect the observed sign and magnitude of national annual lag co-fluctuation. The prior 2001–2020 all-negative result for a single coverage-maximized four-plant set is not representative of every eligible four-plant set. A positive national ecological mismatch synchrony effect is **not established**.

**Limitations:** the 500 combinations are the first 500 in source filename order, not a random sample or exhaustive universe; strict site sets still differ between plant-file subsets, so the across-subset r range is not a pure plant identity effect. The within-subset station comparison does hold source files fixed but changes station coverage and, on variable sites, available plant observations per reference half. Six orientations are not independent replicates; no formal confidence interval, independent climate, resource biomass, NDVI, pollinator/food-web match or fitness effects. Biological phenology rm codes and observer effort remain uncertified.

Next: obtain source-verified multi-year station meteorology and estimate annual timing response to climate with site/event fixed effects, temporal blocking and held-out years. Before any claims about food-resource mismatch, independently observe resource timing and availability.
