# PAYOFF-B: Greenland goose prior-freezing forecast against year-preserving permutations

Date: **2026-11-19**. **Post-open exploratory robustness**, fixed in `docs/PAYOFF_B_GWFG_WITHIN_YEAR_FREEZE_PERMUTATION_FREEZE_20261119.md` **after** observing the original stage3→stage4 regression and blocked-CV gains. It is not an independent preregistration, animal cue experiment, information-threshold estimate or hypothesis test with valid biological exchangeability.

## Exact original-source and analysis contract

- Schindler et al. (2024), *Proc R Soc B* DOI [10.1098/rspb.2023.2016](https://doi.org/10.1098/rspb.2023.2016), original public [author GitHub source](https://github.com/aschindler23/Schindler_etal_2024_ProcB), original CSV SHA256 `5d31ef41867d7f591f5a3fc5f2936df6e01dd91951c006e35b607a1e542e8972`, original Git blob SHA1 `ca3736a281dfd2465921efc940dd985499c71a4f`.
- Same **107 original bird-years, 49 original birds, five seasons 2018–2022**; no independently observed cue beliefs, fitness-to-age-one, route correction budget or interacting partner signals.
- Fixed **99** shuffles, NumPy seed **20261119**; permute only the *assignment* of source stage-3 freezing fractions **within the same calendar year** while preserving all original per-year freezing values, stage-3 feeding, stage-4 weather/feeding, bird and year structure and observed breeding outcomes. No selection by fitted effect signs or outcome.
- Repeat original train-only-standardized Ridge **α=1** on the same source sub-season weather/feeding controls, comparing original early freezing variable's fixed-ridge incremental prediction for stage-4 feeding against the shuffled frozen weather variable. Evaluate **leave-entire-bird-out 49 folds** and **leave-entire-year-out 5 folds**.
- All original fixed-ridge augmented CV values were independently re-computed from the source before the shuffled experiment and matched the already-frozen previous results within 1e−11.

## Original source prediction versus within-year-assignment null

Define `gain = baseline heldout MSE − baseline+freeze3 heldout MSE` (positive is better). The baseline has the same stage-3 feeding, weather/time, stage-4 precipitation/storm and year index as the prior analysis; source stage-3 freezing is the sole extra predictor.

| Frozen metric | Bird-heldout (49) | Year-heldout (5) |
|---|---:|---:|
| Original no-early-freeze baseline MSE | 0.004734244 | 0.012608862 |
| Original +early-freeze MSE | **0.004399626** | **0.010500354** |
| Original added-freeze gain | **+0.000334617** | **+0.002108508** |
| 99 within-year shuffled gain median | −0.000061006 | −0.000066713 |
| Shuffled 5–95% gain interval (descriptive quantiles, NOT CI) | [−0.000145256, +0.000216563] | [−0.001017034, +0.001222234] |
| Permutations whose gain was ≥ observed original | **1 of 99** | **1 of 99** |
| (1 + null count ≥ observed) / (99 + 1) | **0.02** | **0.02** |

**Exploratory signal:** the original matching of an earlier weather condition to its bird-year is more predictively informative than almost all 99 within-calendar-year reassignments in *both* group-heldout measures. Therefore simple differences in year-level freezing marginal distributions are not enough to reproduce the full observed ridge prediction gain **under this particular shuffle design**.

**Important caution:** The 0.02 is a **post-outcome, nonexchangeable permutation-tail diagnostic**, NOT a valid causal p-value. Individual stage windows vary in dates and potentially route/habitat; shuffling weather among bird-years within the same year also disturbs the alignment to those dates, not solely a hypothetical bird's access to forecasts. Correlated site weather and shared bird/year effects may explain the source alignment. Also, the source *full OLS* stage-3 freezing coefficient **remains nonsignificant** (β=−0.001373 feeding fraction per +10pp frozen days; bird-cluster CI [−0.013697,+0.010952], p=0.824); regularized heldout prediction is a **different descriptive estimand**.

## No supported direct payoff or compensatory mechanism

- The original Schindler et al. paper already showed associations of spring weather/habitat with feeding and expenditure, and those of feeding expenditure with breeding. A retrospective stage-lag predictive gain does not establish new ecology beyond that prior art without an independently tested system.
- The previous secondary breeding-success prediction remains **mixed**: after adding stage4 feeding+ODBA, bird-heldout logloss **worsens 0.650239→0.652046**, while year-heldout improves 0.654137→0.642096 with a worsening 2020 fold. There is no stable transfer across the two grouping schemes.
- The frozen source has measured weather fractions, **not** a timestamped assessment of what future-state information each individual had **before its irreversible decision**; actual informational reliability `q`, remaining feasible control `r_t`, waiting cost `D_eff`, pairwise partner asynchrony and their effects on reproductive success are **not identified**.
- The earlier out-of-year full frozen-controls OLS had to mark 2018 omission **NOT_ESTIMABLE** because storm4 was exactly zero after removal; this remains retained, not silently recoded.

## Reproduction

- Dedicated original-source [GitHub Actions run 44530687896](https://github.com/zuizui0223/payoff/actions/runs/44530687896) **SUCCESS**, archive artifact **14533148638**. The original publicly accessible stage-3 weather/data were downloaded with exact Git blob and SHA256 verification.
- Artifact ZIP SHA256 **`1ac4f690f4c3edaae5da963aa8b3e0b0117f52b1952bcaa531ac4d974fca52cc`**; aggregate `within_year_permutation.json` SHA256 **`e69bd4857a11dfd97ee664f1f6bfc8c36af4a81fcfccf352b80918b109c42bfa`**. Both the original `result.json` and permutation receipt are included.
- `scripts/payoff_b_gwfg_within_year_freeze_permutation.py`; `tests/test_payoff_b_gwfg_within_year_freeze_permutation.py`; dedicated original source setup in `.github/workflows/payoff-b-gwfg-lagged-weather.yml`. Dedicated job **10 tests passed**.
- Raw bird IDs, source CSV and GPS coordinates are **not** committed or exported.

**Conclusion:** physical source weather has modest, bird-year-aligned *retrospective predictive content* for later spring-stage feeding in this already-studied goose system. Actual information uptake and downstream breeding payoff remain **unverified**. No changes to frozen V2/V7 manuscript, original 2024 source study, or `main`; keep [Draft PR #409](https://github.com/zuizui0223/payoff/pull/409).
