# PAYOFF-B quantitative Results/Discussion audit V1

## Purpose

This audit states exactly what the active theorem paper may claim numerically in Results and Discussion. It separates exact model predictions from implementation checks, prior-art placement, and real-world quantities not estimated by the paper.

| Qualitative claim | Quantitative claim licensed | Ceiling / not licensed |
|---|---|---|
| Every nonzero environmental contrast has one finite migration optimum in the declared model. | For every `v>0`, `F(u,v)` has exactly one stationary point on `u>0`, and it is the unique global maximum. | Exact only for the symmetric two-patch, two-season anti-phase model with the declared assumptions. |
| The weak-contrast optimum approaches a fixed dimensionless constant. | `u_*(v) -> 1.60611529880277...` as `v -> 0`. | This is a **model prediction**, not an empirical distribution of natural migration rates. |
| The weak-contrast growth premium has an explicit leading-order magnitude. | `P_max = 0.13248753945 x^2 tau + O(x^4 tau^3)`. | The coefficient is a theorem-level asymptotic result inside the model; it is not a cross-system effect size. |
| At strong contrast, the optimum approaches the environmental switching timescale. | `u_*(v)=1+\frac1v+O(v^{-2})` and `m_*\tau\to1`. | The timescale statement is conditional on the declared symmetric anti-phase dynamics and is not a universal dispersal rule. |
| Numerical comparisons support implementation correctness. | The exact-formula verification grid agrees with the general two-season Floquet implementation to numerical precision. | Numerical agreement audits code/formula consistency; it is not the proof of the uniqueness theorem. |
| The paper is a mathematical benchmark rather than a field calibration. | **Biological observations analyzed: none** in the active PAYOFF-B paper. | `FIELD_OPTIMUM_DISTRIBUTION = NOT_ESTIMATED` and `CROSS_SYSTEM_EFFECT_SIZE = NOT_ESTIMATED`. |
| Deviations in richer systems identify candidate missing mechanisms. | Asymmetry, partial phase lags, stochastic switching, density dependence, or larger networks can be tested against the single-optimum benchmark. | A deviation is not a contradiction unless the benchmark assumptions are approximately satisfied. |

## Discussion ceiling

```text
FIELD_OPTIMUM_DISTRIBUTION = NOT_ESTIMATED
CROSS_SYSTEM_EFFECT_SIZE = NOT_ESTIMATED
REAL_WORLD_MIGRATION_RATE_DISTRIBUTION = NOT_ESTIMATED
REAL_WORLD_CONTRAST_DISTRIBUTION = NOT_ESTIMATED
ASYMMETRIC_SYSTEM_OPTIMUM = NOT_ESTIMATED
STOCHASTIC_SYSTEM_OPTIMUM = NOT_ESTIMATED
DENSITY_DEPENDENT_SYSTEM_OPTIMUM = NOT_ESTIMATED
```

Results may therefore report exact uniqueness, scaling, and asymptotics. Discussion may present these quantities as a canonical benchmark and generate comparative predictions, but must not present them as measured natural optima or calibrated management prescriptions without an explicit mapping from field observables to `m`, `tau`, and `x`.
