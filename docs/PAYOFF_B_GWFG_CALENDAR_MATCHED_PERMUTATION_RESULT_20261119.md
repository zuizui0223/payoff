# PAYOFF-B — Calendar-aligned weather assignment null changes the interpretation

**Verified:** 2026-11-19. **Scope:** post-open exploratory sensitivity on the **same** original Schindler et al. (2024) Greenland white-fronted goose dataset, not new source-independent ecological evidence. Earlier protocol: `docs/PAYOFF_B_GWFG_CALENDAR_MATCHED_PERMUTATION_FREEZE_20261119.md`; previous less-constrained null: `docs/PAYOFF_B_GWFG_WITHIN_YEAR_FREEZE_PERMUTATION_RESULT_20261119.md`.

## Original source and fixed target

Original author `spring_data.csv` in [aschindler23/Schindler_etal_2024_ProcB](https://github.com/aschindler23/Schindler_etal_2024_ProcB), original Git blob SHA1 `ca3736a281dfd2465921efc940dd985499c71a4f`, original source-byte SHA256 `5d31ef41867d7f591f5a3fc5f2936df6e01dd91951c006e35b607a1e542e8972`. **107 original bird-years / 49 individual geese / 5 years 2018–2022**. Outcome: second-half spring staging feeding-fix fraction. Source first-half freezing-day fraction is added to an otherwise identical fixed weather/feeding predictor, with train-only-standardized Ridge **alpha=1** and blocked bird- or year-holdout. No original GPS fixes, bird IDs or individual weather rows are exported.

## Earlier preexisting results, not modified

The original bird-clustered year-FE conditional linear **early freezing → later feeding** estimate was near zero: **β = −0.0013725 feeding fraction per +10pp frozen days** (95%CI [−0.013697,+0.010952], **p=0.8238**). Early freezing added modest retrospective prediction in fixed Ridge:

- **Leave-bird-out** MSE: 0.00473424 → 0.00439963 (original improvement **+0.000334617**).
- **Leave-year-out** MSE: 0.01260886 → 0.01050035 (original improvement **+0.002108508**), but the five years were heterogeneous.

The previous within-year-only reallocation of source freeze values returned an exploratory corrected upper-tail **0.02 in both splits** (99 permutations; 1 null assignment as good as original). The original bird-year weather exposure dates and duration were **not** matched in that earlier null.

## What is genuinely new in this diagnostic

After inspecting **only original source design support**, before executing the tighter nulls, a second **post-open** design fixed both matching rules and low-support stop conditions:

| Calendar-matched exposure null | Swappable bird-years / 107 | Nonconstant source strata | Eligible years | Decision |
|---|---:|---:|---:|---|
| **Exact year + stage-3 start day** | **48** | **14** | **5** | **RUN** |
| **Exact year + fixed 7-day start bin + fixed 3-day exposure-duration bin** | **52** | **11** | **5** | **RUN** |
| **Exact year + exact start day + exact stage-3 duration** | **17** | **7** | **4** | **HOLD — NOT ESTIMABLE** |

Frozen admission: at least 40 swappable bird-years, 8 nonconstant multirecord blocks, 3 eligible original years. For each runnable null, **99** shuffles of the *freeze assignment only within each prespecified block*; seed **20261119** (exact start) or **20261120** (week × 3-day duration); leave original bird/year/outcome/feeding/date/weather regressors otherwise unchanged. Each source block's original freeze-value multiset is preserved exactly.

### Result: exact-date and duration-aware alternatives are ordinary under the matched null

| Exploratory corrected tail fraction for original heldout gain | Bird-heldout (49 folds) | Year-heldout (5 folds) |
|---|---:|---:|
| Previous **year-only** null (all 107 rows potentially reassigned) | **0.02** | **0.02** |
| **Exact same original year + start Julian day** | **0.48** (47/99 shuffled gains ≥ observed) | **0.58** (57/99) |
| **Same year + 7-day start bin + 3-day duration bin** | **0.35** (34/99) | **0.47** (46/99) |
| **Exact start day + exact duration** | **NOT ESTIMABLE** | **NOT ESTIMABLE** |

The original observed gains are unchanged because **no predictor or outcome model was refit or retuned**. The exact-day null gain medians are **+0.000328353** (bird holdout) and **+0.002216021** (year holdout), nearly the original +0.000334617 and +0.002108508. The week×duration null medians are **+0.000307099** and **+0.001890907**, also of a similar scale. All 99 permutations in each run yielded some positive augmented-model gain.

**Interpretation:** the prior 0.02 weather-assignment contrast is **not robust to calendar alignment**. Original forecasts do not outperform most shuffles after constraining assignment to geese with the same first staging date or approximately similar date and exposure duration. Hence the previous "within-year bird-specific environmental information" suggestion **must be downgraded**. This does *not* imply that climate exposure has no predictive content, or that exact exposure matching has disproven an individual mechanism.

### Critical identification limits

1. The exact-day null changes **only 48 of 107 potentially swappable records**, leaving 59 source bird-years fixed by stratum support. The week×duration null changes at most 52, leaving 55 fixed. The resulting tail fractions are **post-open, nonexchangeable observational diagnostics**, not calibrated causal hypothesis-test p-values. They are also not directly comparable to the original 107-row permutation tail under a common randomization distribution.
2. The exact-day match does **not control observed stage-3 duration**. The week×duration match bins both quantities and leaves within-bin date/duration variation. The strongest exact same-day **and** duration stratum has only 17 original potentially swappable records and fails predeclared support. No fully calendar/duration matched bird-year effect was estimated.
3. Weather measurements at a particular spring staging window can be associated with geography, individual habitat, conditions or migratory tactics; matching observed timing does not establish what information a goose perceived before committing to the next flight.
4. Original Schindler et al. (2024) already reported spring weather and energetic/feeding predictors and breeding links. This analysis is **same-source model criticism**, not a new independent macroecological replication or evidence of the exact theoretical information waiting threshold.
5. The older observed later feeding/energy-cost variables did **not consistently improve future breeding-success prediction** across individual and year holdouts. No `q`, `D_eff`, `r_t`, pairwise asynchronous cue uptake, natural hysteresis, or causally identified fitness mediation is estimated.

## Reproduction / independent output verification

- Source SHA-pinned [GitHub Actions run 44537189557](https://github.com/zuizui0223/payoff/actions/runs/44537189557) **SUCCESS**, **15 dedicated source tests passed** (with dependency warnings), aggregate-only artifact ID **14537265791**.
- Original downloaded artifact ZIP SHA256 **`b59bb249f87fe549f3897d3e1594c4548c928bdbdce54253034bd48b60bb570a`**; extracted aggregate `calendar_matched_freeze.json` SHA256 **`2962e8353364278a387561604406489f72baae97d11a33948933fea2acf63348`**. These were re-downloaded and checked separately after the GitHub workflow.
- Executable: `scripts/payoff_b_gwfg_calendar_matched_freeze_permutation.py`, tests `tests/test_payoff_b_gwfg_calendar_matched_freeze_permutation.py`, workflow `.github/workflows/payoff-b-gwfg-lagged-weather.yml`.

**Scientific decision:** classify the stage-3 freezing / stage-4 feeding predictive improvement as **calendar-associated observational structure, not a robust same-day bird-year-specific information-uptake signal**. Retain both prior positive predictive associations and the new negative matched-source control. Do **not** add more post hoc model variants to chase significance within the same 107 bird-years; prioritize truly independent, timestamped decision-environment data before further claims. Original PAYOFF-B theorem and frozen V7/source manuscripts unchanged; keep [Draft PR #409](https://github.com/zuizui0223/payoff/pull/409) unmerged.
