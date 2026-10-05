# PAYOFF-B V8 information-value transfer diagnostic result — 2026-10-06

Status: **POSTHOC TRANSFER NOT SUPPORTED; APPARENT POSITIVE SLOPE STRUCTURALLY EXPLAINED**

## Question

After the metric-scale reanalysis replaced delta-rho with a decision-scale
environmental forecast-value proxy,

    delta G_CV
      =
    delta [MSE(target-history only) - MSE(source informed)],

does a larger increase in G_CV predict a larger reduction in realized bird
arrival-green-up mismatch?

This diagnostic was designed after both the frozen V8 rho outcome and the
metric-scale information-value result were known. It is not preregistered.

## Sample

The analysis uses the same bird sample admitted to the frozen transfer lane:

- 150 species-target rows;
- 72 unique source-target spatial pairs;
- 22 species.

Across all environmental pairs used to standardize exposure:

- mean delta G_CV = **+32.082 d^2**;
- SD = **85.652 d^2**.

The fitted coefficient is per 1 SD increase in delta G_CV.

## Observed transfer

### Frozen log-mismatch scale

Equal-species weighted model:

    delta log mismatch ~ z(delta G_CV)

Result:

- beta = **+0.2450**;
- 95% unique-pair bootstrap CI = **-0.0145 to +0.4192**.

A negative information-to-tracking transfer is not supported.

### Absolute day scale

Equal-species weighted model:

    delta absolute mismatch days ~ z(delta G_CV)

Result:

- beta = **+2.428 d**;
- 95% unique-pair bootstrap CI = **+0.351 to +3.646 d**.

The positive raw slope must not be interpreted as a biological worsening
response because the exposure and mismatch outcome share target green-up
geometry.

## Fixed-arrival structural null

Holding every species-target cell at its 2002-2017 mean arrival date while
allowing target green-up to vary gives:

- fixed-arrival log coefficient = **+0.3867**;
- fixed-arrival day coefficient = **+2.985 d**.

Observed minus fixed-arrival null:

Log scale:
- bird increment = **-0.1417**;
- 95% CI = **-0.4285 to +0.0583**.

Day scale:
- bird increment = **-0.5568 d**;
- 95% CI = **-2.390 to +0.550 d**.

Neither scale detects a bird-specific increment relative to the fixed-arrival
environmental geometry.

## Within-window arrival permutation

Annual arrival dates were permuted within each species-target row and within
EARLY/LATE periods, preserving the window-specific arrival distribution while
destroying year-specific alignment to green-up.

Across 2,000 permutations:

Log scale:
- null median beta = **+0.2166**;
- null 2.5-97.5% interval = **+0.1305 to +0.3105**;
- observed beta = **+0.2450**;
- fraction null <= observed = **0.7125**.

Day scale:
- null median beta = **+2.373 d**;
- null 2.5-97.5% interval = **+1.972 to +2.810 d**;
- observed beta = **+2.428 d**;
- fraction null <= observed = **0.6005**.

The observed positive slopes are therefore ordinary under null datasets in
which year-specific bird-environment alignment has been destroyed.

## Conclusion

The posthoc decision-scale environmental exposure does not create the missing
bridge from environmental information to bird timing.

Licensed:

> Marginal cross-site forecast value increased strongly between periods, but
> routes with larger increases did not show a bird-specific improvement in
> arrival-green-up mismatch after accounting for shared environmental geometry.

Also licensed:

> The apparent positive association between delta G_CV and mismatch change is
> reproduced by fixed-arrival and within-window-permutation nulls and is not
> interpreted biologically.

Not licensed:
- increasing information value worsened bird mismatch;
- birds ignored the source signal;
- actionability loss blocked use of the source signal;
- downstream correction caused population-level mismatch stability.

## Consequence for V4.3

The evidence must remain layered:

1. bird environmental data establish a robust temporal increase in the
   marginal forecast value of the frozen nonlocal source signal;
2. bird mismatch shows no corresponding overall deterioration, but route-level
   transfer from G_CV is not detected;
3. mule deer independently establish that signed downstream phase correction is
   biologically real;
4. theory links forecast value and correction opportunity without claiming the
   mule-deer mechanism caused the bird pattern.

This null strengthens the argument for separating environmental forecast
availability from realized biological use rather than treating them as one
predictability variable.

## Provenance

Workflow:
- run: 37390812861
- artifact: 11381312202
- artifact SHA256:
  bb04e1d5acf7583be730e6fe06f910f201c8de448add5861aafda6fdd8e9c01a

Script:
analysis/movement_phenology/payoff_b_v8_information_value_transfer_diagnostic.R
