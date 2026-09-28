# PAYOFF-B E7 source-screen result: local thermal-response ordering is heterogeneous

Date: **2026-09-28**  
Status: **screen complete; E7 not promoted; E6 remains the canonical empirical ceiling**

## What the screen found

Four independent plant–pollinator systems can be written on one descriptive scale:

```text
delta_abs_beta = |pollinator temperature slope| - |plant temperature slope|
unit = days / °C
negative = plant responds more strongly
positive = pollinator responds more strongly
```

The published point estimates are:

| system | delta_abs_beta (d/°C) | direction |
|---|---:|---|
| Freimuth 2022, bee–plant | -3.2 | plant stronger |
| Kehrberger & Holzschuh 2019, Osmia–Pulsatilla | -9.0 | plant stronger |
| Xie 2022, Andrena–Claytonia | +0.5 | pollinator stronger |
| Kharouba & Vellend 2015, butterfly–plant | -5.70 | plant stronger |

This is already an ecological result: **local partners do not have a universal ordering of thermal phenological responsiveness**. Xie et al. strengthens that conclusion within one interaction system by showing geographic reversal: flowering is more temperature-sensitive in warmer regions, whereas bee phenology is more responsive in colder regions.

## Why the four numbers are not promoted as a meta-analysis

Only Kharouba & Vellend directly report the exact cross-partner magnitude contrast and its SE under a model that accounts for repeated butterfly and plant identities.

For the other systems:

- **Freimuth:** the descriptive B_abs contrast combines separately summarized bee and plant group means. The paper also reports a valid direct interaction-asynchrony effect, but that is a different Tier-A estimand.
- **Kehrberger:** the mean bee and plant slopes come from models sharing sites, so their cross-model covariance is not published. A direct first-bee/first-flower lag model has uncertainty, but it measures first-event rather than mean phenology.
- **Xie:** the plant and bee fixed effects come from separate mixed models; Table 1 labels uncertainty as coefficient ± SD, and the covariance required for a cross-model difference is unavailable.

The forced diagnostic is intentionally noninferential. Treating all four uncertainty approximations as if they were valid SEs yields:

```text
Q = 34.31 on 3 df
diagnostic I² = 91.3%
DL tau² = 13.03
random mean = -3.50 d/°C
normal 95% CI = -7.47 to +0.48
```

The interval crosses zero and the heterogeneity is extreme. More importantly, the variance contract itself is invalid for three of four rows, so the pooled estimate is not a Paper 2 result.

## Paper 2 decision

**Do not add an E7 pooled coefficient.**

The stronger and cleaner story is now:

1. E6: within migratory birds, temperature responsiveness weakens with migration distance.
2. E6 local benchmark: local plant–pollinator partners can all respond strongly while differing in magnitude.
3. E7 source screen: across independent local interaction systems, even the **identity of the more temperature-responsive partner is not universal and can reverse geographically**.

This strengthens the information interpretation without creating a pseudo-meta-analysis:

> Local access removes part of the remote-information problem, but it does not force interacting species to share the same climatic response function.

That statement is descriptive synthesis, not a pooled causal effect.

## Promotion boundary

E7 can reopen only if at least three independent systems yield the same direct relative-timing or partner-disparity estimand with defensible uncertainty that does not depend on unreported cross-model covariance.

Until then, the canonical Paper 2 manuscript remains unchanged.
