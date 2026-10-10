# PAYOFF-B goose: staging duration, energetic allocation, breeding outcome forecast test

Date: 2026-10-08
Status: **post-published-outcome exploratory source-specific plan; frozen before opening the new numeric test result**. Neither publication nor published original model outcomes are blinded in any clinical/preregistration sense. This is a *new cross-validated model contrast*, not a confirmatory causal finding.

## Why this is a different and limited question

The external stage-calendar audit on the unchanged author spring data (Schindler et al. 2024; source commit 2171bcd36bf37022c8716e15c0f75412103b0f3f) gave year-centered stage5-exit on stage3-arrival slope -0.0134 (bird bootstrap -0.153 to +0.120), versus staging duration slope -1.0134. That can arise without adaptive feedback, from synchronized exit dates. The follow-on test asks only:

> After stage timing and the original authors' feeding/energetic correlates are accounted for, does realized Iceland staging duration provide **additional out-of-year predictive information** about breeding success?

This is a **prediction question**. Calendar scheduling, compensatory learning, animal condition and physiological causation remain unidentifiable from stage dates alone.

## Exact frozen source and eligibility

Use pinned public author spring_data.csv (not the moving GitHub branch) and Dryad version-5 SHA256 after CRLF normalization:

    9ef98e6b5e979e93476ed076a018db13bdf03aab6dcc5ca728b5fd866e79c1bd

Require exactly 642 rows, 107 complete bird-years in 49 birds, exactly stages 1–6 and strict monotonic first_day. Bird-year is the outcome unit, not stage row. Every stage row within a bird-year must have the same binary breeding_success value (0 or 1) and same categorical breeding_outcome. If any inconsistency, missingness or implausible feed fraction occurs, **fail closed**; do not drop birds selectively. The published paper reports 108 breeding observations, so 107 versus 108 stays a source discrepancy and no missing record is manufactured.

## Definitions

- Stage3_start = first_day sub_season 3 (start of Iceland staging).
- Stage5_start = first_day sub_season 5 (start of second migration flight).
- Stage6_start = first_day sub_season 6 (start of early breeding).
- Iceland staging duration = stage5_start - stage3_start. This does not equal flight speed or physical maximum route recourse.
- Staging feeding fraction = (num_feed_fixes_stage3+num_feed_fixes_stage4)/(num_ACC_fixes_stage3+num_ACC_fixes_stage4), bounded 0–1. This is an observation-weighted **feeding propensity**, not total energy intake or food quality.
- Staging activity = average (log_ODBA_stage3, log_ODBA_stage4), a movement/energy expenditure proxy, not a calibrated metabolic or fitness cost.
- Year code: 1–5 (2018–2022), represented as a numeric trend for held-out predictions. Year one-hot effects would fail to extrapolate to a left-out year.
- Staging-start and breeding-start dates enter baseline, so duration cannot simply substitute for these obvious calendar covariates.

## Prospective models, matched cross-validation

All covariate scaling is fitted from each training fold only.
Ridge-penalized logistic regression with fixed penalty strength lambda=2 on standardized slopes, unpenalized intercept; no hyperparameter search, no post-outcome feature selection.
Hold out *each calendar year in turn* (five folds) to avoid leakage through common-year climate (many individuals repeat in other years; this does not eliminate individual effects).

Models, **the only focal comparisons**:
- M0 calendar only: numeric year code + stage3_start + stage6_start.
- M1 calendar + resource allocation: M0 + staging feeding fraction + staging log_ODBA.
- M2 add putative schedule compression: M1 + staging duration.

Focal descriptive contrast: mean held-out log loss(M1) - log loss(M2), positive if duration improves predictions *after* stage dates and energy proxies. Context contrast: mean log loss(M0) - log loss(M1), positive if energy information adds forecasts.
Report raw log losses, paired Brier scores, all five held-out year score differences, probability extrema, sample support, and 4000 bird-cluster resamples of already-made out-of-fold paired errors (note: refit and year uncertainty NOT included). No fit coefficient significance tests or causal mediation estimates are pre-authorized.

Do not recode unsuccessful attempt vs deferral after seeing results; binary success is one endpoint fixed here. Do not claim independent causal cost from feeding fraction, ODBA or stage duration. Original Schindler model already included breeding arrival timing alongside environmental, feeding and activity effects.

## Competing outcomes and stop rules

- M2 out-of-fold improvement stable across years: staging duration adds prediction conditional on available covariates, *but* fixed calendar could also predict it; not evidence of information-driven adaptive compensation.
- No improvement or deterioration: no incremental support for staging duration beyond M1 in this declared predictive test; does not prove no timing cost.
- Mixed sign / wide cluster interval: insufficient support to interpret a general effect; do not retune a different target or treatment.
- Structural collinearity: if design ill-conditioned despite ridge, mark unidentifiable.
- The source has no independent actual resource-wave phase optimum, pre-decision cue perception, or physical maximum remaining correction, so a biological fitness-optimal strategy still cannot be identified.

## Prior-art and publication boundary

Schindler et al. (2024) themselves analyzed stage-wise feeding, activity, breeding onset and subsequent reproduction in this exact cohort. This new contrast is an exploratory **added predictive-value audit**, not a discovery that goose energetic condition influences breeding. The paper's main theorems, V7R/V8 results and prior natural evidence remain frozen and unchanged. Include this result as supplementary only if it clarifies source identifiability, not as a posthoc rescue headline.
