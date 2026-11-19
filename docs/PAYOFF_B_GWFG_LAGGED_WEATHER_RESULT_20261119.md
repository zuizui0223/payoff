# PAYOFF-B 2026-11-19: Original Greenland white-fronted goose lagged weather → feeding / breeding diagnostic

**Result grade:** **post-publication, exploratory reanalysis of original Schindler et al. (2024) data**. Not an independent replication, direct information-uptake assay, causal compensation demonstration, or fitness-to-age-one measurement. Original paper: [Schindler et al. 2024, Proc R Soc B, DOI 10.1098/rspb.2023.2016](https://doi.org/10.1098/rspb.2023.2016); original author's public [GitHub repository](https://github.com/aschindler23/Schindler_etal_2024_ProcB) (MIT) and Dryad [DOI 10.5061/dryad.2547d7wzn](https://doi.org/10.5061/dryad.2547d7wzn).

## Provenance / pre-fit source contract

- Pre-result frozen **2026-11-19** methodology in `docs/PAYOFF_B_GWFG_STAGE3_TO_STAGE4_FREEZE_20261119.md`. The published source itself and its original migration–energetic–reproduction findings were known before the present fit. The protocol is **not prospective research preregistration**.
- Original exact `spring_data.csv` Git blob SHA1 **`ca3736a281dfd2465921efc940dd985499c71a4f`** and original file-byte SHA256 **`5d31ef41867d7f591f5a3fc5f2936df6e01dd91951c006e35b607a1e542e8972`**, size **50,918 bytes**, verified byte-for-byte from author's original GitHub repo in public-source GitHub Actions.
- Complete source: **642 stage rows = 49 distinct birds, 107 bird-years, exactly six spring stages and five years (2018–2022)**; **30 birds repeated ≥2 years, 18 ≥3 years**. Source breed success: **28 successful attempts, 72 failed attempts, 7 deferrals**. Source original first-day chronology strictly increases through stages 1–6, with no missing source fields. Stage 3 = first half of Iceland spring staging; stage 4 = second half. Categorical success is defined from the original published 0/1 `breeding_success` flag.
- Weather fractions and ACC-based feeding are *within-stage observational summaries*. Millions of raw fixes are **not independent samples**; all models use **107 bird-year units**, bird clusters or group-heldout evaluations. No original individual bird ID, GPS coordinate, raw source data, or sensitive location is uploaded in derived artifacts.

## 1. Primary stage-lagged weather → next-stage feeding

Frozen primary conditional OLS: **feeding fix fraction in stage 4** ~ feeding fraction in stage 3 + **stage-3 freezing-day fraction (per 10 percentage points)** + original stage-3 precipitation/storm + first stage-3 day + stage-4 precipitation/storm + full fixed effects for the 5 study years. Bird-cluster-robust variance with t(48) inference.

| Estimate | Original-source result |
|---|---:|
| n independent bird-year units | **107** |
| n original birds / years | **49 / 5** |
| Original covariate design rank / columns | **12 / 12** |
| β freeze3, feeding *fraction* per +10 pp frozen days | **−0.00137253** |
| Bird-cluster-robust SE | 0.00612968 |
| **95% CI** | **[−0.01369707, +0.01095202]** |
| **p**, two-sided t(48) | **0.823774** |
| Incremental in-sample residual sum-of-squares reduction | **0.000449 (0.045%)** |
| Full model ordinary R² | 0.367838 |

**Focal result: NOT SUPPORTED.** The data do not support a distinctive positive compensatory rebound or negative persistent limitation in stage-4 feeding as a linear response to measured earlier freezing after these controls. In particular, this is *not* a null test of a real animal information belief or a universal biological effect.

### Year-omission source-support stress

The original source stage-4 storm fraction has **zero variance across the remaining 2019–2022 birds if 2018 is omitted**. Thus the frozen full-controls 2018-omitted model is **rank deficient**. After its initial CI error, the implementation was corrected to **return NOT_ESTIMABLE rather than change covariates or invent a coefficient**. The other four unmodified year-omission fits are:

| Omitted source year | β freeze3 | 95% CI |
|---|---:|---|
| **2018** | **NOT_ESTIMABLE** | stage-4 storm fraction identically zero in 2019–2022 |
| 2019 | −0.001120 | [−0.013327, +0.011088] |
| 2020 | −0.004134 | [−0.018048, +0.009780] |
| 2021 | +0.000212 | [−0.018052, +0.018475] |
| 2022 | −0.001015 | [−0.015097, +0.013067] |

All four estimable intervals include zero and the sign is not stable. This is not a pooled meta-analysis of independent years.

## 2. Heldout prediction of stage-4 feeding by earlier freezing history

Predeclared ridge **α=1**, original stage-3 feeding and stage-3/4 weather/time baseline, fixed train-only standardization. The alternate model adds **prior stage-3 freezing fraction** without re-tuning penalty. The target is stage-4 observed feeding, so prediction at **end of stage 4**, *not* a pre-stage-3 environmental forecast.

| Group-heldout unit | Baseline pooled MSE (feeding fraction²) | + stage-3 freezing MSE | Improvement |
|---|---:|---:|---:|
| Leave one **bird** out (49 folds) | 0.00473424 | **0.00439963** | **7.07%** |
| Leave one **year** out (5 folds) | 0.01260886 | **0.01050035** | **16.72%** |

This same-source forecast gain is **heterogeneous**: leave-out years **2019, 2020 and 2021** improve; **2018 and 2022** worsen. There is **no independent estimate of the gain's confidence interval or reliable transfer to unrepresented years or populations**. Ridge/heldout and the full-year-fixed-effects OLS are different estimands; modest predictive gain with an OLS β near zero is *not* evidence that birds actively interpreted early freezing information as a climate forecast.

## 3. Secondary breeding-success prediction from observing late staging behavior

At the **end of stage 4**, with the same available stage-3 history, stage-4 weather and original stage-4 date, a frozen L2 logistic model (C=1) adds **stage-4 feeding fraction and log ODBA**. Original breeding success is observed later, during breeding. Published Schindler et al. already reported spring feeding and energy-cost links to reproduction.

| Group-heldout | Baseline log loss | + stage-4 behavior log loss | Baseline Brier | + behavior Brier |
|---|---:|---:|---:|---:|
| Leave one bird out (49 folds) | **0.650239** | 0.652046 (**worse**) | **0.221184** | 0.221277 (**worse**) |
| Leave one year out (5 folds) | 0.654137 | **0.642096** (better) | 0.229157 | **0.221081** (better) |

Among leave-year-out folds, **2020 clearly worsens** (log loss 0.626355→0.731106), whereas the other four years improve; pooled metrics alone conceal this instability. **There is no consistently transferable independent predictive value of late staging behavior across both birds and years in this chosen fixed model**. No novel causal feeding-to-breeding effect is established; the published original is prior art.

## Ecological interpretation and novelty ceiling

**What can be said:** Original stage-ordered weather has a small *same-study heldout predictive contribution* to later feeding under a fixed ridge model, but its explicitly controlled linear β is essentially zero with wide CI and year-specific changes. Later behavior does **not** consistently improve breeding-success prediction in both withheld-bird and withheld-year tests. This separates **weather-associated forecastability**, **observed behavioral response**, and **downstream reproduction**, which cannot be collapsed into one path.

**What cannot be said:** precommitment birds receive or use a forecast of Greenland spring from measured Iceland weather; earlier freezing causally triggers compensation; stage-4 ACC feeding determines the fitness cost of a wait; the observed parameters identify the exact PAYOFF-B information gate `q_wait(D_eff)`, effective control `r(t)`, pairwise cooperation or natural hysteresis. The frozen V7 goose (q×U) remains **NOT_ESTIMABLE** and no eBird data were used.

## Reproducibility

Dedicated source-hashed [GitHub Actions run 44529079285](https://github.com/zuizui0223/payoff/actions/runs/44529079285) **SUCCESS**. Original source CSV was re-downloaded and Git blob verified before fitting; the CI archive is artifact **14532508038**. Original downloaded article-derived input was not committed.

- GitHub Actions artifact ZIP SHA256: **`21b1010b0fb8932cf95b8979b006c9132cd9cd0a4e2a9287a9dd63fa21de3c75`**.
- Original computed aggregate-only `result.json` SHA256: **`d19031a08343558fd26b5b6db33846222af9aca0033a40dd7c7964726396fcf6`**.
- `scripts/payoff_b_gwfg_lagged_weather_to_feeding.py`; `tests/test_payoff_b_gwfg_lagged_weather_to_feeding.py`; `.github/workflows/payoff-b-gwfg-lagged-weather.yml`.
- Five source-integrity/negative tests plus one full original-hash/fit audit **passed in dedicated CI**. Global `test` and `test-environments` workflows also **SUCCESS** at original tested PR head.

No full source rows, bird identifiers, sensitive GPS coordinates, or original commercial data were distributed. Keep analysis in [Draft PR #409](https://github.com/zuizui0223/payoff/pull/409), do not silently merge to `main` or reframe the frozen 2026 manuscripts.
