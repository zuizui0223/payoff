# PAYOFF-B V7: published Fig. 3 q × ordinal-stage aggregate result

**Date:** 2026-11-19  
**Status:** **post-publication exploratory ecological-aggregate diagnostic**, **NOT V7 biological preregistered q×geographic U**, **NOT an independent new macro confirmation**.  
**Protocol committed before fitting:** `docs/PAYOFF_B_FIG3_PUBLISHED_AGGREGATE_PREFIT_20261119.md`.

## 1. What was actually observed and analyzed

The [original Kölzsch et al. (2015) paper](https://doi.org/10.1111/1365-2656.12281) printed **13 regional destination RMSD values in its Fig. 3**. The author-supplied 2015 supporting DOCX printed historical, 1982–2011 GDD-jerk spring-onset correlations **q** between 23 region pairs, of which **13** are consecutive on the original three flyway routes and **11** avoid two code-to-S1 alias uncertainties. We paired published historical q for the **incoming** link with the original figure's **destination-region site-aggregate RMSD**.

This is a **source-grain mismatch by construction**: q is a broad-region environmental statistic, whereas Fig. 3 RMSD aggregates local site-year goose arrivals to their region. It is a legitimate descriptive crosswalk of published statistics but does **not** reconstruct the original year-specific region-level Y or individually observed bird decisions.

All 13 printed figure RMSDs and their panels are pinned verbatim in `data/payoff_b_v7_fig3_printed_rmsd_20261119.csv`; no point-cloud digitization, GPS microdata, invented regional centroids, or surrogate phenology outcomes were used.

## 2. Main descriptive results

| Source-published aggregate q → Fig. 3 RMSD | All 13 destination links | 11 without uncertain S1 aliases |
|---|---:|---:|
| Original flyways | 3 | 3 |
| Raw signed-q vs RMSD Pearson r | **−0.1402** | **−0.2650** |
| Raw signed-q vs RMSD Spearman ρ | **+0.0743** | **−0.0909** |
| Additive OLS SSE, days² | 387.08 | 246.95 |
| + q×**ordinal** stage OLS SSE, days² | 287.08 | 205.27 |
| In-sample SSE decrease with product | **25.83%** | **16.88%** |
| q×ordinal-stage coefficient, model B | **−23.81** | **−17.14** |
| Full B model *nominal* residual df, under independent-link fiction | 6 | 4 |
| Leave-one-link-out product coefficient sign | 13/13 negative | 10/11 negative |
| Leave-one-**flyway**-out fixed-ridge baseline MSE, days² | **138.45** | **119.59** |
| Leave-one-**flyway**-out with product MSE, days² | **183.29** | **182.57** |
| Heldout MSE increase after adding product | **+32.4%** | **+52.7%** |

The additive model includes intercept, two flyway indicators, q, source-table ordinal route stage and the original paper's incoming ecological barrier. The product model adds q×ordinal stage. The secondary out-of-flyway comparison instead uses **fixed α=1 ridge, no flyway dummy, training-only q/stage standardization, unpenalized intercept**, because the held-out flyway cannot have a learned dummy coefficient. No model family or penalty was tuned to outcomes. These are only 3 flyway holdouts, not a large-sample generalization estimate.

### Important heterogeneity obscured by pooling

The original source-level q–RMSD Pearson signs vary among the three flyways:

- Greenland n=4: **−0.709**;
- Svalbard n=3: **+0.926**;
- Barents Sea n=6: **+0.664**.

These signs are **descriptive with tiny within-route sample sizes**, and the site-aggregate RMSD is not a shared individual causal response. A strong global monotone relationship cannot be inferred from pooling these very different source units. Note the conspicuous original published contrasts: Sweden (incoming q=0.89, RMSD=27.04 d) and Baltic States (q=0.97, RMSD=26.96 d), versus White Sea (incoming q=0.39, RMSD=5.87 d). Those are **published site-level aggregation facts**, not newly discovered inverse causal effects.

## 3. Interpretation for PAYOFF-B

**Negative but discriminating:** An apparent in-sample q×ordinal-stage association has no supported **out-of-flyway predictive gain** at this ecological-aggregate grain. The directional B interaction is negative here, but its transfer MSE is worse, clean-alias destination omission changes sign once, and the analysis has only 3 flyways / 11–13 linked region pairs. It should **not** be promoted as support for either the urgency-weakens-information or last-step-information-wins theory.

This result also does **not** contradict the original paper's source-confirmed analysis: Kölzsch et al. (2015) already reported a multivariable q–RMSD effect (Table 1b, P=0.03), with flyway, distance to breeding and spring peak width among the important covariates, plus an individual-arrival deviation model of a **different response**. Our aggregate model lacks their exact geographical distance, q's original climate series, and year/individual data and is therefore **not** a re-fit/falsification of their original reported model.

The strongest supported ecological statement remains: **regional potential environmental predictability is not interchangeable with individual-level, decision-time, remaining-actionability or local timing response; broad-region q alone does not robustly transport a novel stage interaction between these three studied flyways.** This agrees with PAYOFF-B's distinction between information, controller opportunity and realized seasonal tracking, but it does not identify the underlying feedback mechanism.

## 4. Frozen main-result and source boundaries

- Registered V7 primary response is `|A_ij - S_jy|` using original **region-year** spring onset and geospatial urgency `U=1−d_region,breed/d_winter,breed`. Both **original 480 annual region-year onset values and region GPS geographic mapping are missing**. No actor fitness, cue use, individual information gain, or biological q×U coefficient was estimated.
- Fig. 3 values are **published site-level RMSDs**, which differ from the original year-specific regional response and do not identify an individual transfer function.
- Ordinal route stage (0→1 in the source published list) is **not** registered geometric U. The new product coefficient therefore cannot satisfy V7's `|corr(q,U)|<0.90` gate or theoretical actionability.
- The 13 candidate transitions **share flyways and weather regions**, so coefficient p-values/CIs and nominal residual df would grossly overstate independence. None are reported.
- No objective environmental information-time variable, observation chronology, stopover actuator budget, or target-individual fitness exists in this figure.
- This analysis reuses known 2015 published findings and **cannot count as a new independent taxon, route system, or prospective confirmation**.

## 5. Reproduction

```bash
python -m scripts.payoff_b_v7_fig3_published_aggregate_screen \
  --output outputs/payoff_b_v7_fig3_aggregate_20261119.json

python -m pytest -q tests/test_payoff_b_v7_fig3_published_aggregate_screen.py
```

The source CSV and regression tests lock all 13 printed values, original route orders, signed-q flags, and the negative out-of-flyway result. No alteration to the frozen original V7 outcome-access rule or main GEB Paper-2 manuscript.
