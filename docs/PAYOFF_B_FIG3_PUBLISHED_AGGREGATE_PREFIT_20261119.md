# PAYOFF-B: published Fig. 3 RMSD × historical q — exploratory source-only prefit plan

Date: **2026-11-19**. Branch: `analysis/payoff-b-fig3-rmsd-ordinal-screen-20261119`.
Status: **post-publication exploratory source-aggregate diagnostic**. Published article's timing/RMSD results are already known; this is NOT prospective preregistration, not a new independent replication, not registered V7 `q × U`, not a claim of biological information use.

## New source-only opportunity

The original article [Kölzsch et al. (2015), JAE, DOI:10.1111/1365-2656.12281](https://doi.org/10.1111/1365-2656.12281) prints **13 regional pooled individual-site RMSDs in Fig. 3 (a–i,k–n)**. All 13 can be paired by their *destination* region labels with the **13 consecutive original published historical q correlations** already independently recovered from the supplied author supplementary document in PR #400. The published q is region-to-region GDD-jerk correlation (1982–2011); Fig. 3 RMSD is a 2006–2011 **site-level timing aggregate** assigned to the destination region. This is a mixed-grain, published **aggregate analog**; unlike the frozen V7 primary outcome it needs neither author-original 480 annual onset rows nor original individual GPS region assignments to describe published values. Its precision and role are more limited.

## Fixed input mapping before any re-fit

Use published Fig. 3 values exactly as printed with two decimal places, no digitizing point clouds:
- Greenland: Southern Iceland 21.21, Northern Iceland 11.31, Southern Greenland 25.60, Northern Greenland 24.93.
- Svalbard: Southern Norway 16.76, Northern Norway 24.36, Svalbard 18.16.
- Barents: Sweden 27.04, Baltic States 26.96, White Sea 5.87, Kanin Peninsula 15.96, Pechora/Kolguyev 7.94, Novaya Zemlya 10.52.

The values are published **regional RMSD in days**, and the original paper has already reported its overall q–RMSD association and additional influences of flyway, distance and spring-peak width. Reconstructing these numbers is a different unit of analysis, not an original inferential finding.

Match each to the corresponding **incoming consecutive source→destination q** from the original SUPPINFO 23-row file and source-fixed route order (Greenland 4, Svalbard 3, Barents 6). Preclude all 10 nonconsecutive source q rows. Flag Barents NLDK→SWE and PEKO→NSE as **original-code/S1-label unresolved** and report 11 remaining pairs as the primary sensitivity. Excluding uncertain source-code associations is a source-provenance screen, not outcome-selected exclusion.

## Frozen analysis and guardrails

1. Descriptive all-13 and alias-clean-11 statistics: Pearson and Spearman signed-q–Fig3-RMSD; averages by flyway; and raw q×ordinal-stage association.
2. Explicitly coding-dependent **structural exploratory OLS** models at source region transition scale:
   - A: `RMSD ~ intercept + two flyway dummies + q + ordinal_stage + incoming_ecological_barrier` (6 predictors);
   - B: `A + q * ordinal_stage` (7 predictors).
   Ordinal stage is a normalised published route index, **not the frozen geographic remaining-distance urgency U**.
3. Report B's q×ordinal coefficient and in-sample residual reduction, but **do not use t-tests, p-values, confidence intervals, or independent-visit interpretation**: n=13 (nominal residual df 6) or n=11 (df 4), with shared climate regions and only 3 flyways. Make no publication-grade significance claim.
4. Overfit diagnostics: leave-one-destination-transition-out refits of B to report interaction coefficient signs and maximum absolute fitted coefficient, not pseudo-independent validation. Optionally report leave-one-flyway-out predictive MSE for A vs B on a **pooled (no flyway intercept) ridge model**, with fixed ridge penalty `alpha = 1` on train-standardized `q` and ordinal stage features and the corresponding product, and unpenalized intercept. Do not tune penalty or choose best subsets.
5. Preserve absolute q sign; no squaring, dropping negative q, changing barrier class or arbitrary site rebinning. Original q×ordinal null/positive/negative all count.
6. If results disagree with original published higher-q / lower-RMSD association, label them sensitivity/partial aggregation—not a falsification of the published individual models or of registered V7. If strong agreement appears, it remains source-level circular prior art, **not** independent field confirmation.
7. The direct V7 biological `q × U` stays `NOT_ESTIMABLE` because site-year climate, original geographic U and original 40-migration assignments are still absent.

## Source-specific prior art

The original 2015 paper itself reports region-level RMSD related to q (*P*=0.03) and breeding distance (*P*=0.004) with additional effects of flyway and spring-peak width. It also reports individual arrival deviation analyses, different from regional RMSD, and nontrivial fixed migration schedules. PAYOFF-B does not claim discovery of q–RMSD associations.

## Audit commands once code is committed

```bash
python -m scripts.payoff_b_v7_fig3_published_aggregate_screen \
  --output outputs/payoff_b_fig3_published_aggregate_20261119.json
python -m pytest -q tests/test_payoff_b_v7_fig3_published_aggregate_screen.py
```

No original individual goose GPS is opened by this exploratory analysis; no author supplement or original GPS is redistributed. The original published 13 figure labels are retyped as numeric values with paper figure traceability, not a screenshot.
