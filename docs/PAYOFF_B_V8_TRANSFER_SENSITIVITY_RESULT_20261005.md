# PAYOFF-B V8 downstream transfer sensitivity result — 2026-10-05

Status: **PRIMARY NEGATIVE TRANSFER PREDICTION NOT SUPPORTED; POSITIVE DIRECTION ROBUST ACROSS SENSITIVITIES**

This receipt records the postprimary sensitivities fixed in
`docs/PAYOFF_B_V8_TRANSFER_SENSITIVITY_LOCK_20261005.md`.

## Descriptive mismatch change

Across the frozen transfer sample:
- unweighted mean late-minus-early log mismatch = **-0.00020**,
  95% unique-pair bootstrap CI **-0.07014 to +0.07195**;
- equal-species mean late-minus-early log mismatch = **-0.02031**,
  95% CI **-0.09002 to +0.05123**.

Thus the sample does not show a clear overall reduction in arrival–green-up
mismatch between the two windows.

## Transfer sensitivities

Primary transfer result for reference:
- equal-species weighted beta = **+0.06244**;
- 95% CI **-0.01411 to +0.13635**;
- preregistered direction was negative.

Mandatory sensitivities:

1. **Unweighted species-target rows**
   - beta = **+0.07543**
   - 95% CI = **+0.00094 to +0.13627**

2. **Equal-species collapse**
   - beta = **+0.03857**
   - 95% CI = **-0.07138 to +0.21239**

3. **Adjust early-window mismatch**
   - beta = **+0.04857**
   - 95% CI = **-0.02291 to +0.10665**

4. **Adjust target green-up mean shift**
   - beta = **+0.06473**
   - 95% CI = **+0.00342 to +0.13931**

5. **Adjust both baseline mismatch and target green-up shift**
   - beta = **+0.04958**
   - 95% CI = **-0.01670 to +0.11164**

6. **Leave one species out**
   - 22/22 coefficients positive;
   - coefficient range **+0.05158 to +0.07959**.

7. **Exact complete bird windows**
   - retained 53 species-target rows, 32 unique spatial pairs, 14 species;
   - beta = **+0.11947**
   - 95% CI = **-0.00916 to +0.22691**.

## Current interpretation

The registered negative transfer prediction is not supported. The point
estimate is positive in the primary model and remains positive across every
mandatory sensitivity, including every leave-one-species-out fit.

The result therefore robustly rejects the simple expectation:

> larger gains in source-destination spring predictability should produce
> larger reductions in bird arrival–green-up mismatch over the same period.

However, the positive coefficient itself is **not yet interpreted
biologically**.

Both the environmental exposure and the bird mismatch outcome contain target
green-up. A positive transfer coefficient could therefore arise partly or
entirely from shared environmental geometry or the nonlinear mismatch
transformation, even if bird timing did not respond to connectivity.

Before promoting an information-versus-actionability interpretation, a
structural-null audit is required.

## Provenance

Sensitivity workflow:
- run: 37290339930
- job: 111699001476
- artifact: 11336178282
- artifact SHA256: bb4a2c81b906322efef18fe84a48e056da5d315a80e36201e36da850fc1a352c
