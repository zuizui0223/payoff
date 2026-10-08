# PAYOFF-B: time-of-availability correction to goose breeding prediction

Date: 2026-10-08
Status: **post-publication and post-previous-provisional-result exploratory sensitivity; exact predictors registered here BEFORE opening its new numeric result**.
Previous frozen/previously recorded analyses are unchanged.

## Defect in the preceding exploratory model

The initial M0/M1/M2 five-fold held-year prediction used first_day(stage6), the beginning of early breeding, as a calendar predictor, while discussion framed stage3-stage5 time allocation as if it were evaluated when the goose decides to leave the Iceland staging area at stage5. Stage6 happens **after stage5**, so it is not information available at the staging-exit decision.

This is **not necessarily target leakage relative to an outcome defined after early breeding**. It IS a chronology/estimand mismatch for explaining decisions at stage5. The existing model remains as a *retrospective post-arrival breeding-outcome prediction*, not as a prospective stage5 decision forecast. Do not erase its numbers when CI reproduces them.

## Fixed new as-of-stage5 contrast

Evaluate breeding success as a later outcome of variables that would be chronologically observed by an analyst at the **start of stage5**:
- A0_calendar_at_exit: year code and stage3 first-day (start of Iceland staging).
- A1_resource_at_exit: A0 plus stages 3–4 ACC-weighted feeding fraction and mean log_ODBA; these are stage-aggregated observed measurements only available by the end of stage4. Do not claim geese sensed those exact numeric summaries.
- A2_duration_at_exit: A1 plus **realized stage5 first_day - stage3 first_day**.

**Do NOT use stage6 first_day** nor later autumn variables in any model. The timing at stage5 is the time of the comparison, not a counterfactual for a potential stage5 action; the new result is predictive, not an identifiable causal cost.

Source, grain, year folds, model, outcome and stop rules:
- Original public author commit 2171bcd36bf37022c8716e15c0f75412103b0f3f; exact Dryad v5 CRLF-normalized spring SHA256 9ef98e6b5e979e93476ed076a018db13bdf03aab6dcc5ca728b5fd866e79c1bd.
- Exactly 107 complete individual-years, 49 individual birds, five years and only source success binary 0/1, no synthetic missing 108th breeding attempt.
- All features calibrated in training years only. Leave one source year out across all five years; fixed ridge penalty 2.0, intercept unpenalized; NO hyperparameter search or dropping years based on outcomes.
- Compare mean out-of-year logloss(A0)-logloss(A1) and logloss(A1)-logloss(A2), matched Brier gains, all five held-year differences, 4000 bird-cluster resamples of fixed held-year *errors* (validation uncertainty only; not model refit uncertainty).
- Primary question: Does **staging duration** add held-year predictive information beyond genuinely pre-exit calendar and energetic/feeding measurements?
- Original Schindler et al. already modeled arrival date and energetic covariates in breeding success, so new stage duration forecasting ability is not automatically biological novelty even if its measured cross-validation score improves.

## Explicit causal limits

Duration and observed feeding/activity may be affected by common weather, physiological state, social group and stage detection; conditioning on them may block pathways or introduce collider bias. A predictive improvement does not measure a cost or benefit of actively choosing one more day at the stopover. No independently dated distant forage phenology, knowledge updating, exogenous feasible adjustment set, or downstream individual offspring fitness optimum is present.

A credible mechanism test must identify (i) predecision cues, (ii) feasible actions, (iii) exogenous or well-supported variation in chosen actions and their cost, (iv) independent energetic and demographic outcomes. This as-of-stage5 audit can only rule in/out *incremental observable forecasting information* in this one dataset.

## Interpretation rule

- A2 no better than A1: duration not incrementally predictive under chosen features and five-year transport; does not prove zero fitness cost.
- A2 better than A1: observational association that warrants separate causal design; does not show the bird deliberately compensated or that delay causes breeding success.
- Mixed heldout years, wide intervals, or training/CI failure: no generalizable directional effect.
- All results classified **POST_OUTCOME_EXPLORATORY**, irrespective of sign.

The preceding negative-calendar-control dataset stage5_exit ~ stage3_start, 95% bird-bootstrap and exact accounting identity remain archived unchanged in docs/PAYOFF_B_GOOSE_CALENDAR_VS_FITNESS_RESULT_20261008.md.