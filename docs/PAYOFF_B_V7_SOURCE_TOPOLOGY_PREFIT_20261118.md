# PAYOFF-B V7 published-q route topology: source-only prefit screen

Date: **2026-11-18**. Status: **source-only original aggregate diagnostic, frozen V7 focal test NOT_ESTIMABLE**.

## Question

The registered V7 model tests whether independently estimated historical route predictability q interacts with **geometry-only** route urgency U to explain individual goose timing error. Before estimating any bird outcome, ask two more limited questions using the recovered, published Kölzsch et al. 2015 data:

1. Do the original consecutive regional q values vary within routes, or does published route order trivially determine them?
2. Is incoming ecological-barrier classification related to q, requiring the original mandatory barrier adjustment and flyway-aware uncertainty?

This is a **postinspection design diagnostic** using already published original environmental aggregates, not a newly preregistered macro inference, q×U test, or evidence that geese read the same q.

## Original sources and invariant data

- Published study: Kölzsch et al. (2015), *Journal of Animal Ecology*, DOI [10.1111/1365-2656.12281](https://doi.org/10.1111/1365-2656.12281).
- Original user-supplied supporting DOCX: SHA256 `925e1e5921a4f005b55c5ffb60fa2958bcb29be8c56f4252cd00f66effe91e19`; source derivatives in `data/payoff_b_v7_kolzsch_2015_suppinfo_q_20261117.csv`.
- Original source table: **23** reported pairs, only **13 adjacent** consecutive route transitions.
- Remove adjacent links with original code→Table S1 name aliases marked unresolved (**NLDK, NSE**) → **11** candidates. This does **not** validate their actual geographic GPS membership or map boundaries.
- Original published incoming barrier classification: southern Iceland (SIC), southern Greenland (SGR), southern Norway (SNO), Svalbard (SVA) and White Sea (WS). This is a prior published geographical designation, not fitted from goose outcome.
- The ordinal position measure is `(target_region_index - 1) / (n_route_regions - 2)`, hence runs 0 to 1 along the *source table route order*. **This is not the V7 geographic urgency** `U=1−d(region, breeding)/d(winter, breeding)`. All numerics below are exploratory descriptive environmental-source screens.

## Source-only numerical results

| Published q diagnostic | All 13 adjacent q | 11 without unresolved source-label aliases |
|---|---:|---:|
| Sampled flyways | 3 | 3 |
| Signed q mean | 0.545385 | 0.515455 |
| Negative q transitions | 2 | 2 |
| Pearson q × ordinal route position | **−0.056225** | **+0.050275** |
| Within-flyway centered Pearson q × ordinal position | **−0.069172** | **+0.061396** |
| Source incoming ecological-barrier links (count) | 5 | 5 |
| Mean q: barrier links | +0.178000 | +0.178000 |
| Mean q: non-barrier links | +0.775000 | +0.796667 |
| Barrier−nonbarrier signed-q difference | −0.597000 | −0.618667 |

Per-flyway signed q mean/range for *all 13* original consecutive pairs:

| Route | n | mean q | min–max q |
|---|---:|---:|---:|
| Greenland | 4 | 0.2175 | −0.38 to +0.85 |
| Svalbard | 3 | 0.5967 | +0.45 to +0.81 |
| Barents Sea | 6 | 0.7383 | +0.39 to +0.97 |

After removing unverified aliases, Barents retains n=4, mean q=0.7525.

These figures show descriptive variation in source q within the fixed published route order. In particular, strong q differences are not simply a monotone function of **ordinal stage** in this set. However, there are only 11–13 source transitions, concentrated in 3 flyways: avoid independent-transition p-values, frequentist biological confidence intervals or mislabeling these regional pairs as 11–13 distinct sampled animals. The barrier difference is consistent with the **original paper's already-reported ecological-barrier result**, not a new effect.

## Additional structural q × ordinal-stage predictor check

To make the *design support* problem explicit, a **predictor-only** diagnostic regresses the constructed q×ordinal-rank column on an additive source-only set: intercept, 2 flyway indicator columns, q, ordinal rank, and the paper's incoming-barrier indicator. This fits **no goose outcome**. The product is full rank beyond these six columns, but the residual signal and transition-level degrees of freedom are limited.

| Predictor-only quantity | 13 adjacent links | 11 alias-unresolved-free links |
|---|---:|---:|
| Full model predictor columns including interaction | 7 | 7 |
| Remaining row-level df **if** transitions were independent | 6 | 4 |
| Proportion of product-column variance not predicted by additive columns | 0.18906 | 0.17887 |
| Auxiliary VIF of q×ordinal-rank column | **5.2894** | **5.5906** |

This descriptive VIF is **dependent on the original 0–1 ordinal coding**, is **not** a measured q×geographic-U VIF, and is not evidence for an animal response. Interregional environmental q share climate sources and are not necessarily statistically independent. The diagnostic warns that even a *fully ranked* model can have weak transition-level identification after flyway and barrier adjustment. A large number of GPS fixes cannot manufacture independent regional q variation.

## Source reproduction opportunity and blocker

The original **paper Methods** describes actual stopovers as radius 30 km for over 48 h, allowing at most one outlier; larger regions are composed of geographically separated stops used by **at least 3 birds**; regional climate positions use a circular mean, with **one Iceland glacier mean position shifted to an original goose stop**. Initial sites have incomplete tagging-based arrival time and were excluded from the original arrival-date analysis. The 40 complete migrations span 2006–2011 and are distinct from the 44 birds with DOI-source GPS records.

The paper's methods provide **rules**, but **not** the authoritative 16-region GPS membership polygons, the precise randomly adjusted Iceland representative point, or a machine-readable 1982–2011 region-year onset matrix. Source climate was ECA gridded temperatures plus NOAA station data; using a different reanalysis product and guessed coordinates would **change the V7 measurement**, not reproduce its frozen primary endpoint.

Therefore reconstructing 30-km stopovers from GPS is a **potential source-audit sensitivity**, but is **not enough** to declare original 16-region membership or an original spring-onset series recovered. A possible author/source-data request should seek original 16 region site or fix assignments, centroids/coordinates (including the Iceland exception), 1982–2011 GDD-jerk region-year Julian days, code/version/temperature inputs, and the exact 40 complete spring migration identities.

## What this prefit screen DOES / DOES NOT settle

**Supported source-only design observations:**

- Nominal source q candidate count ≥10 has 11 aliases-unresolved-free consecutive regional links.
- q varies within each of the three published route orders and is almost uncorrelated with *ordinal* route position in the whole set.
- Published ecological barriers are clearly aligned with lower q in this small descriptive dataset, so they remain a mandatory competing explanatory variable.
- Without genuine independent regions and geographies, route/stage/observation biases remain serious identification risks.

**Still NOT estimable:**

- Registered `corr(q,U)` using genuine geographic U, including its fail threshold `|r|<0.90`.
- Genuine ≥30 individual stopover visits, two flyway inclusion and original 40 complete-migration cohort.
- The individual response `|arrival_{ij} − S_{j,year}|` because source-year GDD onset is absent.
- Registered `q×U` biological interaction, actual animal cue usage, fitness, direct actionability or a new natural information-deadline theorem.
- Original `s` sensitivity because published SMATR table has a documented discrepancy with S1 SD ratios; leave the already frozen hold in place.

**Required next artifact:** source-verified original region-year onset and 16-region GPS geometry/membership with provenance. Keep the frozen V7 preregistration, outcome-access rule and threshold unchanged. If those source artifacts remain unavailable, report **NOT_ESTIMABLE** rather than substitute S1 means or ordinal stage.

## Reproduction

```bash
python -m scripts.payoff_b_v7_q_topology_prefit_audit \
    --output outputs/payoff_b_v7_q_topology_prefit_20261118.json
python -m pytest -q tests/test_payoff_b_v7_q_topology_prefit_audit.py
```

The script imports and calls the **existing source-DOCX aggregate validator**, reads only published q/S1 aggregate CSVs and published route order, and explicitly forces `V7_REGISTERED_PRIMARY_GATE=HOLD_NOT_ESTIMABLE`. No GPS animal outcome or new weather data are loaded; no original copyrighted DOCX is redistributed.
