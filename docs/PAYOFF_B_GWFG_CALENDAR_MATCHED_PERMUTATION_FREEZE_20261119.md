# PAYOFF-B GWFG: calendar-aligned weather-assignment controls

**Design and interpretation freeze, 2026-11-19.** This is a **post-open sensitivity analysis**, added after seeing the original stage3→stage4 coefficient and the first 99 within-year weather permutations. It is **not** independent preregistration, randomization, or causal proof of a bird information-use mechanism.

## Question

The earlier same-year freeze permutation showed that original source bird-year assignment gave better retrospective prediction of later feeding than almost all shuffled assignments (exploratory upper tail 0.02 for both bird and year holdouts). However, that permutation also destroyed the linkage of historical exposure to each individual's **actual start day and length of stage-3 staging**. Determine whether the original predictive gain is unusual after conditioning *more tightly* on exposure timing.

## Original source and immutable sample

Source is the original `spring_data.csv` in [aschindler23/Schindler_etal_2024_ProcB](https://github.com/aschindler23/Schindler_etal_2024_ProcB), Git blob SHA1 `ca3736a281dfd2465921efc940dd985499c71a4f`, published Schindler et al. 2024 *Proc R Soc B*, DOI `10.1098/rspb.2023.2016`. **107 bird-years, 49 original birds, five years 2018–2022**; stage3 = first half spring staging, stage4 = second half. `first_day3` and `first_day4` are observed start dates. Approximate stage3 exposure length is **`first_day4 - first_day3`**, which measures sub-season time between starts, not exact hourly weather coverage.

### Pre-effect source-only support (inspected before this new permutation)

| Blocking rule | Calendar×block groups with ≥2 different freeze fractions | Bird-year rows eligible to change | Years with eligible blocks | Gate |
|---|---:|---:|---:|---|
| **Primary**: same year + **exact stage3 start Julian day** | 14 | **48/107** | 5/5 | PASS |
| **Secondary**: same year + fixed 7-day Julian calendar bin (floor((DOY−1)/7)) + fixed 3-day stage3-duration band (floor((duration−1)/3)) | 11 | **52/107** | 5/5 | PASS |
| **Strict diagnostic**: same year + exact start day + exact stage3 duration | 7 | **17/107** | 4/5 | **FAIL / DO NOT RUN FORECAST** |

Minimum support fixed **before observing the new shuffled outcome**: **≥40 eligible bird-years across ≥8 nonconstant, ≥2-record blocks in ≥3 original years**. A block is eligible only with at least two original bird-years and at least two distinct observed `freeze3_10pp` values; all other rows remain untouched. The strict fully matched design fails and its effect must not be inferred, and no thresholds may be reduced post-outcome.

**Important non-nested controls:** the 7-day×3-day blocks are not a subset of the exact-start-day blocks. They trade calendar precision against matched approximate stage3 duration. Their two results must not be selected as a single best or a new independent replication.

## Frozen permutation procedure

- Use **99** within-block permutations per passing design; fixed seeds **20261119** (exact start day), **20261120** (7-day start bin × 3-day duration bin). For each repetition, reassign **only `freeze3_10pp` among bird-years within the same predeclared block**.
- The original per-block freezing-value multiset must remain **identical** after every shuffle. Hold `feed3`, `feed4`, `first_day3`, `first_day4`, precipitation, storm fractions, bird ID, year, breeding outcome all unchanged.
- Reproduce **the earlier exact original heldout augmented Ridge α=1** before shuffling. Use identical feature matrix, train-only scaling, leave-one-bird-out and leave-one-year-out folds. Do not tune Ridge or select covariates after seeing effects.
- Primary descriptive statistic in each split: **observed original gain** `MSE(base) - MSE(base + real freeze3)` compared to **99 matched-block shuffled gains**, with median, q05/q95, number of shuffles meeting/exceeding original and corrected empirical upper-tail fraction `(1 + count≥) / 100`. This is a **post-open exchangeability-suspect diagnostic, NOT an inferential p-value**.
- Report the fraction of bird-year records whose freezing assignment could vary in each blocked design; show the **exact-day+exact-duration failure** transparently. No person-level IDs or weather rows will be exposed.
- The *unchanged full primary linear coefficient* remains β **−0.001373**, 95%CI [−0.013697,+0.010952], p=0.824 and must stay in any discussion as **NOT SUPPORTED**. The previous breeding-success prediction split is also mixed and may not be relabelled as fitness causation.

## Decision/interpretation

- If exact-start-day null frequently produces the original gain, the previous within-year permutation signal is not robust to **calendar-day alignment**.
- If the original still exceeds most exact-day shuffles, it demonstrates at most **original observation-specific predictive value conditional on start day**, but **different exposure durations and unsampled habitat remain confounders**.
- The secondary fixed-calendar-week×duration-bin test is a partial check on both; even if it exceeds null, within-bin dates and route/habitat differences remain uncontrolled.
- **The strict same-start+same-duration comparison is NOT ESTIMABLE** with 17 potential rows: do not claim the strongest matching was confirmed.
- None of the tests measures the organism's forecast beliefs, actually available future green-up information, a decision deadline, remaining actuator capacity `r(t)`, net fitness cost `D_eff`, or interaction-partner synchrony. The original Schindler 2024 weather/behavior/reproduction relationships remain prior art. Source year-level climate response is not an independent five-system replication.

## Reproduction

```bash
python -m scripts.payoff_b_gwfg_calendar_matched_freeze_permutation \
  --source /path/to/original_public_spring_data.csv \
  --output outputs/payoff_b_gwfg_calendar_matched_20261119.json

python -m pytest -q tests/test_payoff_b_gwfg_calendar_matched_freeze_permutation.py
```

The public GitHub Actions runner downloads the SHA-pinned original, runs the tests and writes **aggregated-only** results. No eBird, original bird IDs, trajectories or unpublished data are redistributed; original theory, V7 and journal manuscript remain frozen.
