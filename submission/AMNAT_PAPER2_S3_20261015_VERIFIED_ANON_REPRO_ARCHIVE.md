# PAYOFF-B Paper 2: 41-page S3-included anonymous scientific archive, 2026-10-15

**Status:** S3 numerical/data-source replay **PASS**; full editorial PDF all-page mechanical QC **PASS**; external anonymous reviewer deposit and formal journal submission **HOLD**.

## Executed immutable scientific CI

- Run: https://github.com/zuizui0223/payoff/actions/runs/38699554487 — **SUCCESS**.
- Full CI ZIP/PDF/figure/source artifact: https://github.com/zuizui0223/payoff/actions/runs/38699554487/artifacts/11955491813.
- GitHub Actions outer artifact SHA256: `444db4613302bbb865758dd19e923d9a0eec26dcacc36c145b799f5a472c15fe`.
- Deterministic **inner reviewer candidate ZIP SHA256:** `8a72991d3cc93390ced829444f065f3069e4c511e55c0cea3ce70d12a0b6354a`.
- Inner ZIP: **75 files**, **5,645,743 bytes**.
- Automated review tests: **21 passed** before building the archive.
- Rebuilt anonymous mathematical manuscript: **41 pages**, 4 embedded figures, source-verified 166 actual environmental pairs and 150 actual bird species-target plotted observations, remaining figure 1 theoretical and figure 4 original source-frozen mule-deer descriptive summary.
- Whole-PDF mechanical audit: no blank page, off-page text, missing glyph or known internal owner token. All pages rasterized and contact sheets included; **human final page-by-page approval NOT performed**.

## Source-data and scientific reproduction

The ZIP retains the original byte-pinned Amaral environmental/bird source RDS, the independently reconstructed V8 pair/target and 10,000-bootstrap/2,000-permutation records, original Ortega et al. Source Data workbook (and previously checked 32 source-data fields), previously reproduced S2 day-unit measures, and the corrected theorem's mathematical companion source.

**New in this run:**

1. Six **outcome-informed exploratory** day-metric-to-bird mismatch regressions (2 predictors: LOYO source RMSE change and incremental source MSE forecast value; 3 outcomes: observed mismatch, fixed-arrival null and their bird-specific difference).
2. Original 150 species-target joined rows from 72 distinct environmental pairs and 22 species, 10,000 unique-pair bootstrap coefficient draws.
3. Source/target cell + 5°/10° geographical block sensitivity results: all 24 reported groupings, 40,000 attempted bootstrap draws with the 10° scheme marked **NOT_ESTIMABLE** because it has only 4 independent groups.
4. **564** complete original leave-one-species/leave-one-environmental-pair-out slope outputs.
5. Reproducible anonymized R scripts for the six slopes and the secondary geographical sensitivity, an independent output CSV validator, Supplementary Table S3 and a revised 41-page PDF containing its explicitly qualified discussion.

**Exact replay gate:** the anonymized R scripts were actually executed with the bundled original scientific source records, and *all* six first-stage model source files and all eight spatial/deletion sensitivity source files matched their original immutable run output numerically. Receipt status:
`S3_ORIGINAL_POSTOUTCOME_TRANSFER_AND_SPATIAL_REPLAY_MATCH`.

## Ecological conclusion and epistemic boundary

| Exploratory day-unit predictor | Observed bird mismatch β | Fixed-arrival null β | Bird-only increment β |
|---|---:|---:|---:|
| Source-informed LOYO RMSE change | +0.00947 [−0.08942, +0.09886] | +0.07392 [−0.00981, +0.15961] | −0.06446 [−0.13837, +0.00766] |
| Source squared-loss forecast-value change | +0.09530 [−0.00258, +0.16230] | **+0.15040 [+0.09407, +0.23158]** | −0.05510 [−0.16754, +0.02120] |

Coefficients per 1 SD of the 72-pair environmental predictor. At **20 source-cell, 19 target-cell, and 9 target 5°-block** resampling levels, both bird-specific increments' CIs include zero, while the positive **fixed-arrival** forecast-value association remains interval-positive. At target 10° scale (4 independent blocks), no CI is estimated; it is not an absence-of-effect result.

All 22 species-omission and 72 pair-omission coefficients for the two bird-specific increments remain negative; this is descriptive sign stability **without** spatial-bootstrap exclusion of zero. No animal actual cue reception, action opportunity, optimal fitness or species demographic response has been measured. The fixed-bird-arrival null is a structural/synthetic benchmark holding bird arrival unchanged, not an intervention.

**Original registered V8 results and negative hypothesis support decisions are unchanged**: stronger signed environmental rho (+0.3690), registered negative correlation→matching transfer NOT_SUPPORTED, fixed-arrival null accounts for a positive association. These S3 tests were chosen **after** the original and day-unit outcomes were known and are neither confirmatory nor multiplicity-adjusted. The complete source-code and original-model comparison remains in separate Draft PR #333 stacked on the Paper 2 branch.

## Remaining external submission blockers

Human full-resolution proofreading of every PDF page/figure/equation; software reuse and source-licence review; author approval, contribution/funding/COI/AI-use statements; journal-specific citation/format check; and deposition of the internally content-anonymous ZIP to an externally anonymous reviewer-accessible location. **GitHub Actions URLs themselves identify the repository and are NOT a double-blind sharing method.**

No journal submission, code licence issuance, PR merge or causal ecological claim upgrade occurred.
