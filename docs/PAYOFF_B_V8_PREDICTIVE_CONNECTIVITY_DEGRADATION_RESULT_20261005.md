# PAYOFF-B V8 predictive-connectivity degradation — frozen primary result

Date: **2026-10-05**  
Status: **NOT SUPPORTED — OPPOSITE DIRECTION**

Contract:
`docs/PAYOFF_B_V8_PREDICTIVE_CONNECTIVITY_DEGRADATION_CONTRACT_20261005.md`

Workflow:
- run: `37281018588`
- artifact: `11332196684`
- source data commit: `62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`

## Admission gate

The preregistered gate passed without relaxation:

```text
ELIGIBLE_SOURCE_TARGET_PAIRS = 393
ELIGIBLE_SPECIES = 28
SPECIES_WITH_AT_LEAST_3_PAIRS = 26
GATE = PASS
```

## Primary result

The registered estimand was

[
\Delta\rho
=
\rho_{2010-2017}
-
\rho_{2002-2009},
]

with the directional prediction (E(\Delta\rho)<0).

Observed:

```text
PAIR_MEAN_DELTA_RHO = +0.352915
SPECIES_CLUSTER_BOOTSTRAP_95 = [+0.283176, +0.414277]

MIXED_INTERCEPT_DELTA_RHO = +0.350608
MIXED_95 = [+0.268369, +0.432848]

SPECIES_EQUAL_WEIGHT_MEAN_DELTA_RHO = +0.336355
SPECIES_NEGATIVE = 2
SPECIES_POSITIVE = 26
REGISTERED_ONE_SIDED_NEGATIVE_SIGN_TEST_P = 0.999999892
```

The preregistered broad-degradation hypothesis is therefore:

```text
V8_BROAD_DEGRADATION = NOT_SUPPORTED
```

and the observed direction is strongly opposite to the registered prediction.

For scale only, the eligible pair-level signed detrended correlation averaged:

```text
EARLY_PAIR_MEAN_RHO = 0.427708
LATE_PAIR_MEAN_RHO  = 0.780623
```

The equal-weight species means were approximately 0.405 early and 0.741 late.

## Biological interpretation

The result rejects the simple broad story:

> climate change has generally made earlier route locations worse predictors of
> later breeding-site spring across this sample.

Under the frozen Amaral source-target geometry, the interannual source-to-target
green-up relationship was instead substantially **stronger** in the later
window for most species.

This is useful because it rules out the most direct version of the original
"climate change broke the forecast system" hypothesis at this scale.

It does **not** imply that:
- climate change caused the strengthening;
- all flyways or stopover sequences became more predictable;
- migrants perceive or use the correlation;
- stronger correlation improved fitness;
- route-level sign reversals such as Schreven et al. 2026 are unimportant.

The V8 result concerns the broad distribution under one frozen cell-mapping
definition. Route-specific predictability can still degrade even when the
multi-species mean increases.

## Transparency

No window, mapping, detrending method, minimum-pair threshold or species gate
was changed after outcome access.

The opposite-direction outcome is not reclassified as support for a new theory.
Mandatory prespecified sensitivities may now be run, but they may only assess
robustness of this frozen primary result.
