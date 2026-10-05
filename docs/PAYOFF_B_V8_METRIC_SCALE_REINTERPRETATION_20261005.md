# PAYOFF-B V8 metric-scale reinterpretation — 2026-10-05

Status: POSTHOC, OUTCOME-INFORMED DIAGNOSTIC; DOES NOT ALTER THE FROZEN V8 PRIMARY ESTIMAND

## Why this note exists

The frozen V8 primary estimand is the change in detrended Pearson correlation
between source and destination green-up. That estimand remains valid and must be
reported as registered.

A subsequent independent reproduction identified a scale issue: a larger
correlation need not imply a smaller forecast error in days when destination
phenological variance changes between periods.

The manuscript must therefore distinguish:
1. standardized source-destination coupling;
2. absolute forecast error on the day scale;
3. biological actionability after information is available.

## Statistical point

For a detrended destination anomaly Y and source anomaly X, the population
linear-prediction decomposition under squared loss is

    Var(Y) = explained variance + residual variance

with

    explained variance = Var(Y) * rho^2
    residual variance  = Var(Y) * (1 - rho^2).

Therefore an increase in rho can coexist with an increase in absolute residual
error if Var(Y) increases enough.

Importantly, increased destination variance does not itself cause rho to rise:
correlation is scale invariant. The correct interpretation is that total
destination variability increased, the fraction shared with the source also
increased, and the unshared absolute residual may still have increased.

## Provisional reproduced pattern supplied after the primary outcome

The independent reproduction reports, across the same 166 unique pairs:

- mean rho: about 0.28 -> 0.65;
- mean destination anomaly SD: about 2.4 d -> 4.7 d;
- mean source-based in-window forecast RMSE: about 2.2 d -> 2.9 d;
- mean RMSE change: about +0.71 d;
- only about 36% of pairs show lower RMSE in the late period.

These numbers are treated as provisional until the repository diagnostic
independently reproduces them. The dedicated script is
analysis/movement_phenology/payoff_b_v8_metric_scale_diagnostic.R.

That script also computes leave-one-year-out forecast RMSE, source-only versus
no-source forecast error, spatial/dependence-aware intervals, and absolute
arrival-green-up mismatch in days.

## Consequence for the current manuscript

The phrase "environmental predictability improved" is no longer licensed from
rho alone.

Safe language before the diagnostic is finalized:

> Standardized source-destination spring coupling strengthened between periods.

If the day-scale diagnostic reproduces the reported result, the stronger
posthoc statement becomes:

> Standardized source-destination coupling strengthened while absolute
> source-based forecast error in destination green-up increased.

This is not a contradiction. It is a scale decomposition.

## Consequence for the title

Retire, unless redefined very carefully:

    Improved environmental predictability need not improve seasonal tracking

Candidate replacements:

1. Stronger seasonal coupling can coexist with larger forecast errors
2. Environmental coupling and forecast error can move in opposite directions
3. Seasonal tracking depends on usable forecasts, not correlation alone

The final choice should wait for the leave-one-year-out diagnostic.

## Consequence for the theory

The cleanest generalization is to define G(t) as decision-relevant expected-loss
reduction from the information available at stage t.

The actionability model becomes

    N(t) = r(t) G(t) - C(t).

The existing binary-cue model is one special case:

    G(t) = S q(t) - B.

For a Gaussian continuous timing target under optimal linear prediction and
squared loss, another special case is

    G(t) = sigma_Y(t)^2 rho(t)^2,

while the residual forecast risk is

    R(t) = sigma_Y(t)^2 [1 - rho(t)^2].

Thus relative information gain G can rise at the same time as residual
day-scale uncertainty R rises. Retained actionability r is a third quantity,
not a synonym for either.

This gives a three-layer ecological distinction:

    standardized coupling
        -> decision-scale forecast error/value
        -> retained actionability and downstream correction.

## Consequence for the bird result

Do not use V8 to say that an information-loss explanation was generally
falsified. The correct statement is narrower:

> The registered hypothesis that standardized cross-site correlation degraded
> was not supported.

If absolute day-scale forecast error increased, an environmental uncertainty
route remains viable in a different metric.

If bird mismatch nevertheless remained stable on the same absolute day scale,
that becomes an interesting descriptive resilience pattern, but it does not by
itself identify downstream correction as the cause. Alternative explanations
include use of other cues, metric insensitivity, changing arrival variance,
selection, and unmeasured route-level behavior.

## Evidence hierarchy after this correction

Primary, confirmatory:
- frozen V8 delta-rho result and its dependence audit.

Posthoc diagnostic:
- target anomaly SD;
- in-window day-scale forecast RMSE;
- leave-one-year-out day-scale RMSE;
- explained versus residual variance;
- raw absolute bird mismatch in days.

Independent mechanism anchor:
- mule-deer signed phase convergence and speed/stopover correction.

No posthoc day-scale result may be relabeled as preregistered.
