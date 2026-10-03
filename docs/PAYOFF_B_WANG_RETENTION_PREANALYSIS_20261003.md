# PAYOFF-B comparative timing-retention route — preanalysis contract

Date: **2026-10-03**  
Status: **PREOUTCOME; numerical Wang timing values not yet inspected in PAYOFF-B**

## Why this route exists

The direct fitness-rescue novelty screen closed the broad V4 question: individual
studies already show that timing deviations can dissipate, persist, or carry
fitness costs.

A narrower comparative question may remain:

> **How much of an individual's departure-time deviation survives to arrival,
> and does that retention differ systematically among migratory bird species?**

This is not the same as asking whether departure predicts arrival on average.
Wang et al. (2024) already show a strong pooled carry-over path using 1,708
full-annual-cycle records from 186 species. The candidate contribution is the
**heterogeneity of that path among species**, not its existence.

## Prior-art boundary

- Wang et al. 2024: pooled global departure→arrival carry-over is already known.
- Franklin et al. 2022: within-stage timing repeatability varies across annual
  cycle stages in 47 species; this measures across-year consistency, not
  within-migration propagation of a departure anomaly.
- Morbey & Schmaljohann 2020: comparative spring migration speed and departure
  traits for 25 songbirds; no species-specific departure→arrival retention.
- Linssen et al. 2025: fuelling-time flexibility across five Arctic-breeding
  waterfowl; a related but narrower metric.

Thus PAYOFF-B must not call "carry-over", "flexibility", or "departure affects
arrival" new.

## Primary estimand

For species (s), define within-study-year departure and arrival anomalies

[
d'_{i}=d_i-ar d_{s,j,y},
qquad
a'_{i}=a_i-ar a_{s,j,y}.
]

The species-specific retention coordinate is

[
a'_i=eta_s d'_i+epsilon_i.
]

Interpretation:

- (eta_s=1): departure deviations persist fully to arrival;
- (0<eta_s<1): partial temporal compression;
- (eta_s=0): complete reset by arrival;
- (eta_s<0): over-correction / reversal.

This is descriptive. It is **not** an estimate of cognitive information use,
feedback gain, actionability, or fitness.

## Data gate

Use only individual-level Wang records. Population means are excluded.

The comparative route opens only if at least **20 species** have at least
**8 informative paired individual records** in a season after centering within
species × study/paper × year, with nonzero within-stratum departure variation.

If that gate fails, the macro-comparative route closes without relaxing the
threshold after inspecting outcomes.

## Primary analyses

1. Estimate (eta_s) separately for spring and autumn.
2. Quantify among-species heterogeneity with a random-effects meta-analysis.
3. For species eligible in both seasons, compare
   (eta_{m spring}-eta_{m autumn}) with a paired species bootstrap.
4. Secondary, predeclared moderators for spring retention:
   log migration distance and log body mass.

Moderator signs are two-sided. Longer routes could offer more recourse, lowering
retention, or impose stronger time constraints, increasing retention.

## Novelty decision

A publishable comparative result requires more than a pooled carry-over effect.

The route is biologically informative if:
- species-level heterogeneity is estimable in >=20 species; and
- either the paired seasonal contrast or a predeclared ecological moderator is
  supported with its declared uncertainty.

Otherwise the result remains a bounded comparative null.

No post-result taxonomic subgroup search is allowed to rescue this lane.
