# PAYOFF-B E6 — within-study migrant temperature-response contrast (13 original studies)

Date: **2026-11-19**. Status: **SOURCE-VERIFIED POST-OPEN ROBUSTNESS**. **Not** a new independent original species-level study, a complete eBird-free certification, or a directly identified migration information-deadline mechanism.

## Result and original statistical unit

An existing published association between migration distance and bird temperature responsiveness was reproduced in the Usui et al. (2017) source table by PAYOFF-B E6 (944 effects, adjusted pooled long-minus-short +0.421 d/°C). The E6 source inventory subsequently found that **264 original effects from Hurlbert & Liang 2012 were explicitly based on eBird**, incompatible with the source policy; they were excluded as one entire study. A further **4 effects from Zalakevicius 2002** cannot be tied to a unique original data custodian, leaving **676 source-described original effects from 26 studies**. Italian Rubolini (4) and Finnish Ahola (2) original local study contexts are documented but the raw field-log custodian remains uncertain.

Within the 676-row group, **only 13 of 26 studies contain both source-coded short- and long-distance migrant classes**; their original **444 effect-size rows span 269 bird species**. This subset was established before opening the new study-FE coefficient, as frozen in `docs/PAYOFF_B_E6_WITHIN_STUDY_FIXED_EFFECT_FREEZE_20261119.md`.

### Primary within-study association

Model `Slope(days/°C) ~ long_distance + C(Study)`, 13 crossed original study intercepts; original source inverse-SE² weights; Study × Species two-way robust covariance (frozen original E6 estimator). With only **13 independent study clusters**, inference uses Student-t **df=12**. Predictor design has full rank (14 columns).

| Study fixed effects, source-published E6 | Value |
|---|---:|
| Source studies containing both classes | **13** |
| Reported effects in crossed studies | **444** |
| Bird species | **269** |
| Adjusted within-study long−short difference | **+0.525253 days/°C** |
| Two-way clustered standard error | 0.138135 days/°C |
| 95% clustered confidence interval | **+0.224283 to +0.826223** days/°C |
| Two-sided p (df=12) | **0.00251849** |

This shows the already-published distance gradient is not explained **solely by differences in mean outcomes among studies** in this specific source subset and model. It does **not** identify causal geographic distance from information, actual organism-level cue exposure, or the ability to adjust later in the annual cycle.

### Preserved sensitivity results and heterogeneity

| Re-fit (same 13 study intercepts) | Estimate days/°C | 95% CI |
|---|---:|---|
| Original E6 inverse-variance weights | +0.525253 | [+0.224283,+0.826223] |
| Source weight 99th-percentile cap | +0.525438 | [+0.223069,+0.827806] |
| Unweighted original effect rows | +0.608607 | [+0.348285,+0.868928] |

Leave one **entire original study** out and refit the model **13 times**: estimates stay positive, range **+0.472793 to +0.623006**, and all their study-cluster CI lower bounds are positive. At the study-descriptive level, inverse-variance means are **positive for 11 studies and negative for 2**. Those study contrasts are reported individually in the generated source artifact; no per-study significance or independent-original-replication claim is made. They are not all biologically equivalent response definitions.

The more restrictive 670-row source-origin panel excludes two *only-long* source studies (Rubolini and Ahola), so it has **the same 13 crossed studies and identical 444 effects** for this particular within-study test. Thus the 13-study result is numerically unchanged by those two further source-origin exclusions—not an independent replication.

## Scientific claim ceiling

**Allowed:** source-verified, no-known-eBird-study E6 published temperature-response gradients remain positive under study-fixed-intercept comparisons, original weight sensitivity and one-study-at-a-time omission. This is a stronger *within-original-study* association audit than the broad pooled E6 summary.

**Not allowed:** proclaiming a novel migration-distance effect (already known from Usui); that the all-input dataset is fully eBird-free; identifying actual future environmental cue information from a researcher-specified `Temperature_location`; identifying information thresholds, coordinated phenological mismatch, downstream speed/stopover recourse, or fitness effects. The separate [temperature-location gate PR #403](https://github.com/zuizui0223/payoff/pull/403) failed source crossing (2 studies vs minimum 5); this result does not repair that.

The main [frozen barnacle-goose V7 q×geographic urgency](../docs/PAYOFF_B_V7_PREDICTABILITY_URGENCY_CONTRACT_20261005.md) remains `NOT_ESTIMABLE` because original region×year spring-onset and geospatial region membership are missing.

## Reproducibility and independent numerical verification

- Original paper Usui et al. 2017, *Journal of Animal Ecology*, DOI [10.1111/1365-2656.12612](https://doi.org/10.1111/1365-2656.12612).
- Original E6 derived GitHub Actions archive ID **10953792024**, ZIP SHA256 `443cab62531d9b633aa6ee67da010fa66b6c230ef87e919d697269e77a7373f0`, original source-derived 944-row CSV SHA256 `817a2d2d18931944103283c93e4d9bf80568906a21a92369ee168e4f8f203085`.
- Prefit source and model contract `docs/PAYOFF_B_E6_WITHIN_STUDY_FIXED_EFFECT_FREEZE_20261119.md`.
- Executable `scripts/payoff_b_e6_within_study_distance.py`, tests `tests/test_payoff_b_e6_within_study_distance.py`.
- Dedicated GitHub Actions [run 44484580314](https://github.com/zuizui0223/payoff/actions/runs/44484580314) **SUCCESS**, artifact ID **14509328403**, `result.json`. The artifact ZIP was downloaded again separately and numerical coefficients, intervals, study counts and source-status guardrails were independently checked against the fixed protocol.
- No raw eBird checklists or individual trackers were accessed. The already-summarized original E6 effect archive is used for source verification only, and the verified eBird study was excluded from any admitted subset model.

Freeze this result as a stacked Draft [PR #405](https://github.com/zuizui0223/payoff/pull/405) on top of [PR #404](https://github.com/zuizui0223/payoff/pull/404). Neither main nor the frozen V2/V7 manuscripts are changed.
