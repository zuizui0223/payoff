# PAYOFF-B: prospective decision-time forecast gate (2026-10-08)

**Status:** source-only methodological guard and toy demonstration. Stacked on PR #314 / PR #311. No V7R or V8 outcome reopened or reinterpreted. No evidence of active updating is claimed.

## Why this gate is necessary

PR #314 separated a checkpoint cue's **standalone** destination correlation from its **incremental** predictive value conditional on origin knowledge. Before using that update to explain migration, another identification risk must be removed:

> A climate variable reconstructed years later must not be treated as information the organism possessed before making the focal migration decision.

For example, Kölzsch et al. (2015) use a spring-onset date based on the historical peak of a GDD-jerk process. That can be an environmental response *target*, but the retrospectively completed peak is not automatically a cue available to a bird at an earlier stopover. Local weather, cumulative temperature measured up to the actual decision, and photoperiod are different quantities and require their own dated data provenance.

A second problem is that **within-period environmental correlation is not transferable forecast skill**. Two windows can have stronger signed correlation even when a predictor calibrated in the first window badly predicts the second, owing to mean/slope shifts.

## Step 1: temporal observability (mandatory)

Each unique source-defined spatial pair and seasonal year requires:
- the origin cue's numeric value **and date it could first have been known**;
- the checkpoint cue's numeric value and availability date;
- the focal action-decision date, not the arrival timestamp selected after route completion;
- the downstream phenological target and the date it could first have been known;
- provenance for how each cue could have been observed or delivered.

Require, using offset-aware timestamps:

    origin_available_at <= checkpoint_available_at <= action_decision_at
                        < downstream_onset_available_at

Reject missing cue provenance, a cue only inferable after action, missing timezone, repeated spatial-pair/year records, and absent registered years. Source timestamps in a modern climate archive do **not** themselves establish that the bird sensed the archived variable. Pass means only *environmental availability*, not neural information, behavior, or fitness.

Pair-year data shared by several migratory species must not be counted as independent evidence multiple times (the V8 dependency correction identified precisely this issue).

## Step 2: forecast rather than hindcast (environment-only gate)

Using only *past years*:
1. fit a climatology-only predictor of downstream onset;
2. fit an origin-cue model;
3. fit the **same origin-cue model plus the checkpoint cue**.
4. hold the models, scale/center, and predeclared predictors fixed; score an untouched later set of years.

The frozen primary descriptive contrast is

    Delta_MSE_holdout = MSE_origin - MSE_origin_plus_checkpoint.

Positive values mean the checkpoint helped out-of-sample **environmental** forecasts beyond the origin cue on this heldout split. This is not the animal's information gain until cue observability and sensing are defended. Report mean prediction bias and performance of the climatology benchmark; improve-on-training alone is not sufficient.

Implementation: `src/decision_time_forecast_gate.py`, which uses standard-library ridge regression, training-only feature scaling, fixed year blocking, duplicate source-pair/year rejection, and paired test-year MSE. It returns **no** behavior or fitness effect.

This prototype is *not* a final statistical inference method: it has no uncertainty estimate, flyway random effects, measurement-error correction, or cross-year multi-source bootstrap. Positive point estimates must not be called a discovery; a real confirmation requires independent environmental records, enough independent years and pairs, and predeclared year/pair-block uncertainty.

**Fail closed:** if the available checkpoint cue does not improve properly held-out prediction, stop the refresh explanation for that route. Do not rescue by choosing a different checkpoint after seeing response data.

## Step 3: actions must respond to forecast innovation

If Step 2 passes, use the model-derived **predecision forecast innovation**

    innovation_m = checkpoint_cue_m
                   - E_train[checkpoint_cue_m | origin_history]

and pre-registered destination forecast coefficient K_m.

The behavioral predictor is the signed *forecast update* K_m * innovation_m, not raw local spring warmth or a posteriori onset error. The primary response must be an actual, prospectively defined downstream choice (departure, stopover release, flight speed, route, breeding date) that was still reversible after information became available.

Include as rival accounts:
- a fixed photoperiod/calendar departure schedule;
- immediate physical temperature effects independent of future forecasting;
- local forage/fuel intake, wind, travel constraint, and reproductive urgency;
- selection of the *last* local stop as apparent stage origin;
- repeated individuals and common-year climatic effects.

**Crucial caution:** even a signed innovation/behavior association is not unique evidence of cognitive forecasting. A direct local thermal mechanism can remain observationally equivalent; an intervention or exogenous cue separation is required for causal assignment.

Do not use a slope of `stopover duration ~ arrival phase` as an individual-scale actionability capacity: fixed departures generate negative slopes without reactive feedback, as PR #313 showed.

## Step 4: independent recourse and fitness

- Define each individual's feasible action set using independent biomechanics, fuel, actual flight constraints, weather, and explicit decision dates. A population-level schedule envelope does not identify this set.
- Test whether *forecast innovation × independently measured individual recourse* predicts the **next behavioral correction**, before analyzing outcomes.
- Only then test reproductive success or survival, if available. Phenological alignment alone is not demographic fitness.

If behavior is not identified, stop at environmental forecasting. If reproductive outcomes are absent, do not assert fitness rescue.

## Nontrivial calibration counterexample (exact model, not natural evidence)

Let an early standardized cue X and spring target H have correlation 0.3 with zero mean. A forecast trained then is 0.3X and has MSE 0.91.

Later, suppose the cue-target **correlation strengthens to 0.8**, but the target mean increases by one standardized unit:

    H_late = 1 + 0.8X + sqrt(1 - 0.8^2) * epsilon.

The historically calibrated 0.3X policy now has MSE:

    1^2 + (0.8 - 0.3)^2 + (1 - 0.8^2)
    = 1.61.

The newly calibrated late-era optimum would have MSE 0.36. Thus historical policy predictive accuracy can **deteriorate despite stronger within-period environmental correlation**. This standard distribution-shift identity is not a novel ecological theorem, and does not imply fixed calendars necessarily outperform the historical cue policy. It shows exactly why V8's increase in correlations cannot be read as an increase in usable information at the decision time.

## Synthetic smoke check (not a biological result)

With 48 synthetic training pair-years, 24 later held-out pair-years, and six spatial pairs:
- checkpoint genuinely predicts downstream target: origin-only MSE ~10.47, refreshed MSE ~0.037, incremental MSE gain ~10.44;
- checkpoint is irrelevant: origin-only MSE ~0.03736, refreshed ~0.03749, incremental gain slightly negative.

These are seeded illustrative fixtures only. In a real result the year-pair bootstrap, source selection, holdout structure, and effect uncertainty must all be locked before biological outcomes are opened.

## Gate hierarchy and editorial consequence

| Layer | Required evidence | What it **does not** establish |
|---|---|---|
| A. Environmental source | time-valid predecision cue | bird sensed the cue |
| B. Prospective forecast | heldout incremental value and calibration | cue changed behavior |
| C. Behavior | action revision with fixed-calendar controls | causality without an intervention |
| D. Fitness | reproduction/survival consequences | community-level coordination by itself |

The original V7R Q×R effect was **not supported**: 10 transitions; one-sided within-flyway permutation p=0.56994. V8's broad correlation-degradation hypothesis was **not supported**; its positive correlation change did not produce the pre-registered bird-mismatch improvement. These are preserved falsifications, not recast as positive support for this new route.

Novelty boundary: Bayesian filtering, signal innovation, decision theory, climate forecast verification, and blocked-year evaluation are known tools. A potentially new ecological result requires actual evidence that *information acquired after departure changes a future, still-reversible ecological decision and thereby alters interaction synchrony or fitness*, beyond fixed-schedule and direct local forcing mechanisms.

References: Kölzsch et al. (2015), doi:10.1111/1365-2656.12281; PAYOFF-B PRs #306, #313 and #314.
