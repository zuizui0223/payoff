# PAYOFF-B wigeon ERA5-calibrated SIMEX v2

Frozen: **2026-09-24**  
Workflow: **35942135223**  
Status: **canonical GitHub Actions reproduction complete**.

This is the primary current SIMEX sensitivity for the source-faithful wigeon
phase-retention result. Unlike the earlier SIMEX lane, its error scales come
from the complete 256/256 POWER-versus-ERA5 calibration.

The simulation preserves the actual 224-transition event structure. One
measurement error is assigned to each unique staging event and reused when that
event is the destination of one transition and the origin of the next.
Within individual-year sequences the errors follow the frozen AR(1) process.

Frozen settings:

```text
zeta:                    0.5, 1.0, 1.5, 2.0
replicates per zeta:     1000
seed:                     20260924
extrapolation:            quadratic to zeta=-1
naive POWER lambda_hat:   0.749768
```

## Results

| complete-ERA5 calibration scenario | error SD (d) | rho | SIMEX lambda |
| --- | ---: | ---: | ---: |
| equal independent replicates | 5.010 | 0 | 0.8412 |
| discrepancy-correlation proxy | 5.010 | 0.367 | 0.7979 |
| conservative full disagreement | 7.086 | 0 | 0.9354 |

All three frozen extrapolations move lambda upward relative to the naive
estimate, as expected under predictor-error attenuation.

The resulting range is:

```text
0.7979 .. 0.9354
```

and every frozen scenario remains below one.

## Interpretation

The complete calibration changes the emphasis compared with the naive estimate.

The wigeon coefficient should not be described as a precisely known
approximately-0.75 biological retention coefficient. Reasonable frozen
measurement-error assumptions move it appreciably upward, and the deliberately
conservative full-disagreement scenario approaches complete retention.

At the same time, the phase-retention signal is not eliminated by any of the
three predeclared event-structure SIMEX scenarios.

The appropriate statement is therefore:

> measurement error materially affects the estimated strength of wigeon phase
> correction, but the source-faithful phase-retention signal remains below
> complete retention across the frozen SIMEX sensitivity set.

This remains a sensitivity statement. POWER-versus-ERA5 disagreement does not
uniquely identify the latent error distribution, so none of the extrapolated
values is promoted as the true biological lambda.

## Relationship to the earlier SIMEX lane

The previous SIMEX used error scales from the registered ERA5-Land calibration
that failed its 90% event-coverage gate. It remains a historical sensitivity
receipt.

This v2 lane supersedes it as the primary observation-error sensitivity because
the source-faithful ERA5 calibration has complete 256/256 event coverage and
passes the frozen validation gates.

## Claim ceiling

Licensed:

- complete-calibration event-structure SIMEX;
- measurement error attenuates the naive wigeon lambda estimate;
- correction magnitude is materially uncertainty-sensitive;
- all three frozen SIMEX extrapolations remain below one.

Not licensed:

- a uniquely identified latent lambda;
- describing 0.841, 0.798 or 0.935 as the corrected truth;
- universal contraction strength;
- using this sensitivity to alter the still-unopened Aikens preregistration.
