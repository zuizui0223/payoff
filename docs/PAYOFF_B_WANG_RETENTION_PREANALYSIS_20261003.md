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
- Schmaljohann 2019: species-specific departure→arrival slopes and their
  heterogeneity are already known in 17 spring and 21 autumn songbird species.
- Franklin et al. 2022: within-stage timing repeatability varies across annual
  cycle stages in 47 species; this measures across-year consistency, not
  within-migration propagation of a departure anomaly.
- Ralston et al. 2025: explicitly identify individual migration distance as a
  candidate determinant of the ability to compensate delayed spring departure
  en route.
- Stopover studies show stronger time constraints and different departure
  decisions in long-distance migrants, but do not establish the sign of the
  distance effect on whole-journey departure→arrival retention.

Thus PAYOFF-B must not call "carry-over", "flexibility", "departure affects
arrival", or species-specific retention heterogeneity new.

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

The primary candidate novelty is now restricted to the **migration-distance
moderation of timing retention**.

The route remains open only if:
- species-level retention is estimable in >=20 species; and
- the predeclared relationship between log migration distance and spring
  retention is estimable and its declared uncertainty interval excludes zero.

Two competing biological predictions are retained:
- **recourse-opportunity:** longer routes provide more stages for acceleration,
  stopover shortening or route adjustment, so retention should be lower;
- **time-constraint:** longer routes impose tighter schedules, so departure
  deviations should be retained more strongly.

The spring–autumn contrast and body mass are secondary context only and cannot
rescue a null distance result. Species-level heterogeneity by itself is not
publishable PAYOFF-B novelty because Schmaljohann (2019) already established it.

No post-result taxonomic subgroup search is allowed to rescue this lane.


## Transparent revision note

This preanalysis document was narrowed on 2026-10-03 **before numerical Wang
migration-timing values were inspected**. The trigger was a literature result,
not an outcome: Schmaljohann (2019) already estimated the species-specific
start-to-arrival slopes that the first version proposed as a candidate novelty.
The revised route therefore tests only a proposed ecological driver of those
slopes, principally migration distance.
