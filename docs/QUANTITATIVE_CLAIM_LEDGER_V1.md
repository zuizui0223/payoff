# PAYOFF-B quantitative claim ledger V1

## Purpose

This ledger distinguishes exact model predictions from implementation checks, prior-art placement, empirical measurements, and quantities that the present short paper does not estimate in real metapopulations. It does not alter the theorem or its scope.

## Claim classes

- `EMPIRICAL` — estimated from a biological field/lab dataset.
- `LITERATURE-AUDIT` — a literature/prior-art placement statement; not a new effect estimate.
- `THEORETICAL-WITNESS` — a constructive or numerical verification object used to audit the mathematics/implementation; not empirical evidence.
- `MODEL-PREDICTION` — an exact theorem, scaling law, or asymptotic consequence conditional on the declared dynamical model.
- `NOT-ESTIMATED` — a real-world quantity not inferred by the present paper.

## Registered quantitative objects

| Object | Class | Frozen quantitative statement | Interpretation ceiling |
|---|---|---|---|
| global optimum theorem | `MODEL-PREDICTION` | for every `v>0`, `F(u,v)` has exactly one stationary point on `u>0`, and it is the `unique global maximum` | exact only for the symmetric two-patch, two-season anti-phase model |
| weak-contrast optimum | `MODEL-PREDICTION` | `u_*(v) -> 1.60611529880277...` as `v -> 0` | dimensionless optimum within the declared model |
| weak-contrast premium | `MODEL-PREDICTION` | `P_max = 0.13248753945 x^2 tau + O(x^4 tau^3)` | leading-order dimensional temporal premium for weak contrast |
| strong-contrast optimum | `MODEL-PREDICTION` | `u_*(v)=1+\frac1v+O(v^{-2})` | asymptotic optimum for large `v` |
| seasonal-timescale limit | `MODEL-PREDICTION` | `m_*\tau\to1` | strong-contrast limit in the declared model |
| exact-formula verification grid | `THEORETICAL-WITNESS` | numerical comparisons against the general two-season Floquet implementation are an implementation audit, not proof | supports code/formula agreement only |
| prior-art boundary | `LITERATURE-AUDIT` | the closed-form periodic/Floquet growth exponent is treated as prior art; novelty is the uniqueness theorem, scaling curve, and endpoint asymptotics | prevents the explicit growth formula from being claimed as new |
| biological observations analyzed | `EMPIRICAL` | none in the active PAYOFF-B paper | the paper is a mathematical benchmark, not a field calibration |

## Quantities explicitly not estimated

```text
FIELD_OPTIMUM_DISTRIBUTION = NOT_ESTIMATED
CROSS_SYSTEM_EFFECT_SIZE = NOT_ESTIMATED
REAL_WORLD_MIGRATION_RATE_DISTRIBUTION = NOT_ESTIMATED
REAL_WORLD_CONTRAST_DISTRIBUTION = NOT_ESTIMATED
ASYMMETRIC_SYSTEM_OPTIMUM = NOT_ESTIMATED
STOCHASTIC_SYSTEM_OPTIMUM = NOT_ESTIMATED
DENSITY_DEPENDENT_SYSTEM_OPTIMUM = NOT_ESTIMATED
```

The statement that optimal movement lies on the seasonal timescale is therefore a **model prediction**, not a survey of natural dispersal rates. The exact result applies to the **symmetric two-patch, two-season anti-phase model** with equal season duration, constant symmetric migration, and linear rare-population dynamics.

## Promotion rule

A field comparison to `m_* tau` requires a defensible mapping from observed movement and environmental switching to the model parameters. Deviations from the single-optimum scaling curve are not treated as contradictions unless the declared assumptions are approximately satisfied; they instead identify candidate mechanisms absent from the benchmark, such as asymmetry, partial phase lags, stochastic switching, density dependence, or larger networks.

## Asymptotic approximation error audit

The fixed **nine-point** audit in `docs/PAYOFF_B_ASYMPTOTIC_ERROR_TABLE_V1.md` is registered as a `MODEL-PREDICTION` diagnostic, not as empirical evidence and not as proof of the theorem.

- At `v=0.1`, the weak approximation has `0.0226%` relative error for `u_*` and `0.0144%` for the maximum `F`.
- At `v=10`, the strong approximation has `0.933%` relative error for `u_*` and `0.736%` for the maximum `F`.
- At `v=100`, the strong approximation has `0.00995%` relative error for `u_*` and `0.00530%` for the maximum `F`.

These checkpoints report approximation error only. There is **no validity cutoff** inferred from the grid, no empirical calibration, and no change to the exact all-`v>0` uniqueness theorem.
