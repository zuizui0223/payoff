# PAYOFF-B V8 actuator bridge contract — 2026-10-05

Status: **POSTTRANSFER, PREOUTCOME FOR MIGRATION-SPEED CHANGE**

Known before this analysis:
- V8 source-destination spring predictive connectivity increased strongly;
- the preregistered negative connectivity-change -> mismatch-change transfer is
  not supported;
- the apparent positive transfer slope is structurally explained;
- the stricter matched between/within decomposition supports neither a
  persistent negative between-route association nor a negative within-route
  transfer.

The migration-speed change outcome below has not been opened as a function of
V8 delta-rho.

## Question

> Are gains in environmental predictive connectivity associated with a change
> in an available downstream timing actuator: migration speed?

This is a descriptive actuator bridge. It is not a causal mediation analysis
and does not claim that birds perceive the fitted environmental correlation.

## Frozen environmental exposure

Use the already-opened V8 exposure without modification:

`delta_rho = rho_late - rho_early`

from 2002–2009 versus 2010–2017 under the frozen detrended source-destination
green-up definition.

## Speed outcome

For every frozen V8 species-target-cell mapping row, use annual `vArrMag`
from the Amaral source dataset.

Keep only finite positive speed values and define:

`log_speed_y = log(vArrMag)`.

Require at least 6 finite speed years in each period:
- EARLY = 2002–2009;
- LATE = 2010–2017.

Then calculate:

`delta_log_speed = mean(log_speed_late) - mean(log_speed_early)`.

No row is retained or removed according to the sign or magnitude of speed
change.

## Primary descriptive model

Standardize `delta_rho` across eligible unique spatial pairs only.

Fit:

`delta_log_speed ~ z_delta_rho`

using species-target-cell rows with equal total weight per species.

Uncertainty:
- bootstrap unit = UNIQUE_SPATIAL_PAIR;
- 10,000 replicates;
- seed = 20261005.

Because theory does not require improved predictability to increase rather than
decrease mean migration speed, this is a **two-sided descriptive association**.
No directional support rule is imposed.

Report:
- coefficient;
- 95% pair-bootstrap interval;
- whether the interval excludes zero.

## Mandatory diagnostics

After the primary coefficient is frozen:
1. unweighted row model;
2. equal-species collapse;
3. adjust early-window mean log speed;
4. leave-one-species-out;
5. exact-complete speed windows (8/8 years in both periods).

## Interpretation

If the interval excludes zero, licensed only:

> Connectivity gains covary with changes in mean migration speed in this
> sampled system.

If it includes zero, licensed only:

> No clear association between connectivity gains and changes in mean migration
> speed was detected.

Neither outcome identifies cue uptake, information use, causal mediation,
fitness consequences, or recourse limitation.

`V8_ACTUATOR_BRIDGE = FROZEN_PREOUTCOME`
