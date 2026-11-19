# PAYOFF-B GWFG original 2024 data — within-year weather assignment permutation

**Design locked 2026-11-19 AFTER opening stage3→stage4 and heldout results.** This is a **post-open exploratory negative-control diagnostic**, not a prospective preregistration, randomization experiment, or a biological causal test.

## Why

The source-verified Schindler et al. (2024) stage3 earlier freezing → stage4 later feeding model yielded almost zero conditional linear effect (β=-0.001373 per 10 percentage points, 95% CI crossing zero, p=0.824) but modest improvement under fixed ridge α=1 in leave-one-bird and leave-one-year-out prediction. Because `prop_days_below_freezing(stage3)` is strongly calendar-year-dependent, that predictive gain may reflect **year climate structure** and/or source differences, rather than the true bird-year association.

## Frozen null and diagnostics

Use the **exact source CSV Git blob SHA1 `ca3736a281dfd2465921efc940dd985499c71a4f`** and the same 107 bird-year table and frozen predictors from `docs/PAYOFF_B_GWFG_STAGE3_TO_STAGE4_FREEZE_20261119.md`.

- Construct exactly **99** permutations with deterministic NumPy Generator seed **20261119**.
- For each original breeding year **separately**, randomly reassign only the original `freeze3_10pp` values among the observed bird-years from that **same year**, preserving **all per-year weather distributions and the original group sizes exactly**. Hold the true `feed3`, stage4 `feed4`, stage3/4 precipitation/storm, date, calendar year and bird identity fixed.
- Do not permute outcome labels, look ahead to breeding outcomes, move the weather values across years, change frozen ridge regularization α=1, alter grouping units, change the baseline/updated models, add covariates or pick a favorable permutation after results.
- Evaluate the exact original fixed-ridge with train-only scaling and two blocked cross-validation schemes: **leave-one-entire-bird-out (49 folds)** and **leave-one-entire-year-out (5 folds)**. Gain = baseline heldout MSE minus augmented heldout MSE, so positive means inclusion of stage3 freezing reduces error.
- Compare the *already observed* original gain to its 99 same-year permutations, reporting the fraction of null gains at least as large as original with +1 correction **(1+count≥)/(99+1)**, median, 5th/95th percentiles, and number of permutations with gain ≥0. A low tail frequency only shows a temporal association under a **nonexchangeable observational permutation design**; it does not demonstrate animal cue use.
- This permutation does **not** preserve detailed associations of freezing with each individual's movement date or habitat; stage3 first_day is included as a control, but unobserved source-site or cohort confounding remains. The randomized `freeze3` is not a real experimental manipulation.
- There is **no new breeding-success effect** in this permutation; the previous late behavior→breeding predictive comparison remains separate and mixed.

### Claim interpretation limits

If source gain is ordinary under within-year permutations, the observed retrospective prediction improvement need **not** arise from a special bird-year-specific freeze–feeding alignment. If source gain exceeds most permutations, that supports only **row-level assignment relevance within the original observational 2024 source**, not a measured information quality `q`, predecision belief acquisition, causal behavioral adjustment or theoretical `q_wait(D_eff)`.

Always report all 99 null values only in aggregate JSON summaries, never raw bird IDs/weather rows; test both grouping units regardless of relative advantage; keep original negative primary β and original mixed breeding-success CV visible. No eBird or raw GPS downloaded; no original V7 source admission or manuscript change.
