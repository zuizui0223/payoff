# PAYOFF-B satellite-only prospective forecasting-value diagnostic — frozen exploratory contract

**Date:** 2026-11-17, **frozen after** original MODIS-only +0.08057016 correlation result and after historical eBird-conditioned V8 +0.369 result were already known. This is a strictly **post-open exploratory measurement-quality test**, NOT independent preregistration, not evidence that any bird perceives a cue.

## Why this is the next necessary link

Within-year detrended correlation of two sites' green-up days, q, is a **property of environmental covariation**, not yet evidence that a migrant with an observation at one site gains out-of-sample forecast skill about the next. Since the paper's hypothesized mechanism depends on information *available before the next commitment*, distinguish a geographic covariation result from independently held-out target prediction.

No eBird, bird species, migratory range, bird arrival, behavior or fitness records are accessed. Use exactly the same verified 106-cell forest MODIS file `data/for_green-up_dl.rds`, original Amaral commit `62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`, pinned SHA256 `8989bf98752cf23a6be237332e35c44abff5a39d2a00d5bd1f65cce732cf6199`, and **the same 104 nearest-southern geographic pairs** from the frozen `docs/PAYOFF_B_MODIS_ONLY_SPRING_COHERENCE_FREEZE_20261117.md`: distance ≤800 km, 10,000+ original good forest pixels, numeric cell tie-break, ≥6 paired annual records in each interval. Expected support: 106 cells, 104 physical pairs, 88 distinct source cells; 2002–2009 and 2010–2017. Fail-closed if this differs, without reranking pair candidates.

## Primary forecast skill — rolling forward without future-year training

For source and target annual mid-greenup calendar days (S_y,T_y), compare two fixed models trained on the *first 5, 6 and 7 years* within each eight-year window, then predicting the strictly next year 6, 7, 8 respectively:

- M0 (no source observation): OLS `target ~ year`, using only training years.
- M1 (source observation available): OLS `target ~ year + source`, using only the same training years. The held-out source date is supplied, but the held-out target date is never supplied to the fit. This is a linear proxy for **potential environmental information**, not actual bird observation.
- Source-day chronological availability is **not assumed** from lower latitude alone. Report separately how frequently source green-up precedes target green-up, and a strict subset of pairs where `S_y < T_y` in *all 16 original years*. Only this strict subset can be discussed as a physically prior seasonal event; even then whether any migrant is present and can sense the event is unobserved.
- For each physical pair × period, aggregate squared prediction error across the 3 held-out years; store `sse_baseline`, `sse_source`. Pair-balanced means and pooled squared errors (days²) reported.
- Define `forecast_skill = 1 - Σsse_source/Σsse_baseline` for each period, aggregating all 104 pairs at equal weight, with 3 prediction years each. `skill_change = skill_late - skill_early`. A negative value means the additional source cue **harms** forecast prediction compared with just knowing historical target trend.
- Do not decide an all-pairs "information benefit" based solely on in-sample Pearson correlation: M1 has one extra parameter with only 5–7 training years and can overfit.

## Frozen sensitivity / uncertainty rules

1. Leave-one-year-out (train 7 other years) compared with strict rolling-forward. Label LOYO **retrospective**, never true prospective training.
2. Strict-source-before-target subset: only if ≥30 eligible links and ≥15 unique source cells; otherwise `NOT_ESTIMABLE_CHRONOLOGICAL_SOURCE`, retaining counts but no adapted cutoff.
3. Report the number of valid chronological source→target orders over all original 16 annual observations per pair; do not post-select favorable years.
4. Cluster bootstrap with `B=10000`, seed `20261117`, sampling whole **source environmental cell** groups and carrying all associated pairs, separately for early/late skill and their contrast. This accounts for reuse of same source cells, not for shared destination targets, broad-area climate shocks or historical temporal dependence. No random pair-as-independent claim.
5. Guard unusual source and target values: exact SHA256, complete 8-year paired support, no missing/nonfinite source, target, or fitted forecast. A failed fit, reused annual target row, or new key drift gives NO_GO, never imputed.

## Hard interpretive ceiling

Whatever direction occurs, it is evidence only about **satellite forest green-up predictability in the selected eastern North American grid**. The same MODIS years were inspected in the previous exploratory correlation result, so this cannot provide an independent discovery or trial. It is **not** biological cue uptake, selected migratory routes, crop/leaf food biomass, nestling intake, movement correction, a game equilibrium, or a breeding outcome. A physically prior green-up difference is still not proof of arrival/departure access; a migrant may leave before the southern event. Preserve the user's no-eBird data rule.

Do not search multiple model penalties/lag lengths, remove exceptional source cells after opening predictions, alter 800 km selection, or call prediction R² a causal information-value parameter.

**Prior source:** <https://github.com/zuizui0223/payoff/pull/396>. **Related frozen V7:** `docs/PAYOFF_B_V7_PREDICTABILITY_URGENCY_CONTRACT_20261005.md`, still NOT_ESTIMABLE without archived Kölzsch 1982–2011 spring-onset and original route region crosswalk.
