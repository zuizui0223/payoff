# PAYOFF-B Scotland: measured caterpillar mass versus counts — incremental resource exposure gate

**Frozen on 2026-11-16 after opening the source-level count-based LOYO/LOSO fit. Exploratory analysis, NOT a prospectively independent confirmation.** Do not reword a result as confirmation because raw bird outcomes are already known. 

## Existing results (not being altered)

Source EIDC 10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3; direct official OGL ZIP, originally observed ZIP SHA e5e7fa4f2fe60420c11675a1d21fdc69b7b8d8fa5565f67b268e1ae070cd0d7d. The package wrapper may be repacked, so this and downstream code require exact pinned **CSV content hashes** instead. On 2026-11-16, count-only source-prespecified analysis admitted 448 unmanipulated blue-tit nests across 143 site-years / 44 sites / 5 distinct years (2014 and 2018–21). In both leave-one-year-out and leave-one-site-out prediction, a 14-day hatch-window caterpillar **count** rate added to climate, hatch timing, peak count, and peak lag **worsened** MSE; gate HOLD. This null must stay published as a null regardless of future sensitivity results.

## Narrow test

Can a directly observed source-weighted **caterpillar mass rate (g per standardized 30-hit branch beating)** during an observed blue-tit hatch window predict site-year mean fledglings per clutch better than **counts** on the **same admitted site-years**, or do they disagree? These prey traits proxy availability, not actual diet or energy intake. Local within-year resource use is not migrant information availability or game-theoretic coordination.

## Original-data source and measurement firewall

Original branch_beating.csv SHA256 38f5c34cf656bab33c5d5b3516648306549049deebfbe693e4b4cad09ac4004c. Original EIDC documentation says branch beating was standardized at 30 strikes, caterpillars counted if >1 mm diameter; samples were weighed from 2017, detection below 0.02g represented as `<0.02g`, and `mass.uncertain = 1` flags unreliable mass. Do NOT substitute the source's 2024/2026 Zenodo records as independent samples.

- Numeric recorded `caterpillar.mass` in original grams is accepted if finite nonnegative and `mass.uncertain` not 1.
- Exact `<0.02` (source file) or `<0.02g` (unit-annotated form) with positive caterpillar count is interval-censored; use **lower=0g, upper=0.02g** per sampled branch, with both reported, never silently set to 0.01.
- Blank mass and **zero source caterpillars** is accepted as a *structural zero* (explicit assumption), not a measured weight; count this separately and provide a sensitivity excluding those inferred zeros if sample permits.
- Blank mass with positive counts and uncertain mass flags are **unmeasured** and excluded from observed mass sums; never silently turn blanks into 0.
- For each site-year-date: all source branches with valid original caterpillar counts define denominator; require measured/censored/structural mass in at least **80% of those branch observations**. Calculate mass rate as total accepted mass g / number accepted standardized branch beatings. Restrict to dates satisfying coverage. Zero mass is meaningful; no invented g/m2 conversion or caterpillar nutritional calories.
- From each site-year date curve compute the source-year **observed peak mass rate** and peak DOY (earliest tie). Nest window: original `hatching_first_recorded` through +13 inclusive, uniform hypothetical demand, linear interpolation within adjacent observations at most **8 calendar days** apart, **100% day support**, no extrapolation. Report both upper and lower bounds of interpolated mass contact.
- The EIDC source code `bluti` is blue tit. Exclude blank and `coati` species; exclude manipulated or treatment-unknown nests in 2017–2019, exclude original `-999` fledgling sentinel, invalid hatch and clutch. Exact same nest and siteyear outcome as count model, from byte-verified EIDC ZIP. 
- Temperature: pre-fixed March 1–April 15 original site loggers, >=80% hourly sample coverage. Keep original source climate, hatch, site covariates unchanged.

## Frozen comparators and full holdout

All models must use **identical mass-and-count-complete source siteyears**; no stacking multiple nests as independent environmental replicates.

Outcome Y: site-year arithmetic mean of unmanipulated nests' `fledged / clutch`, equal siteyear weight.

Baseline A: `year + latitude + elevation + mean hatch ordinal day + mean clutch size + original site-year March1–Apr15 mean temperature + log1p(peak caterpillar count/beat) + signed peak count date - mean hatch`. (The prior count-only M2.) 
B: A + log1p(mean *count* per beating during hatch+0:13).
C0/C1: A + log1p(mean original mass g per beating during same hatch window), lower or upper censor bounds separately.
D0/D1: B + mass lower or upper bound separately (mass-specific extra prediction conditional on count).
Use train-only feature standardization, unpenalized intercept, fixed ridge lambda=1; no tuning after opening outputs. Preserve original count-only result without modifying it.

Admission before fit: >=60 source siteyears, >=20 distinct sites, >=3 distinct years and >=150 original qualifying nests, otherwise **NO_GO** with no coefficient. For real prediction record equal heldout-year folds (LOYO), heldout-site folds (LOSO), out-of-sample MSE for all; use siteyear and fold as unit, not branch or nest. Primary comparison: A vs B, A vs both C bounds, B vs both D bounds. Require C and D to improve in **both LOYO and LOSO, both upper/lower bounds**, and at least ceil(0.8 * years) heldout years for **D over B** before describing an exploratory biomass-specific incremental finding. Else HOLD. Also record 2020-excluded descriptive sensitivity only if still >=3 years and >=60 siteyears, otherwise NOT ADMITTED. Do not select whichever bound gives a favorable sign.

## Null interpretation and novelty boundary

A negative test means source-available count/mass temporal contact proxies did not improve an out-of-sample reproduction predictor under this specification. It does not show true food supply, trophic interaction, biomass or mismatch are ecologically irrelevant, because food ingested, diet substitution and individual energetic demand remain unobserved. Preexisting 2025 Oikos tree-specific biomass phenology and 2026 blue tit resource-size/duration study already occupy naive biomass–fitness findings. No causal/gene/game payoff claims.

## Failure protocol

Any source content hash drift, code-linked site-year ambiguity, unknown censor syntax, sample effort ambiguity, or missing high-coverage mass source must stop analysis instead of imputing results. Source provenance, exclusion table, and unchanged earlier negative baseline must be recorded regardless of the outcome.

### Source-literal correction before new mass outcome fit (2026-11-16)

The first dedicated mass workflow stopped at source-admission parsing (Actions run 43883245272) with literal `ValueError: Unknown source censor threshold <0.02`. The original EIDC CSV stores censored values as `<0.02` without a trailing `g`; source documentation identifies the same 0.02 g detection threshold. This is a source-format correction made **before any mass-specific fitness prediction was opened**, not a redefinition of the fixed [0,0.02] g interval. Accept the two exact strings `<0.02` and `<0.02g`; other censor codes remain rejected.
