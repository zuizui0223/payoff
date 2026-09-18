# PAYOFF-B asymptotic error table V1

## Purpose

This receipt compares the exact registered scaling curve with the weak- and strong-contrast asymptotes on a small fixed grid. It is a `MODEL-PREDICTION` diagnostic and implementation audit. The theorem does not depend on this table.

```text
REGISTERED_V_POINTS = 9
MODEL_ROLE = MODEL-PREDICTION
VALIDITY_CUTOFF_DECLARED = false
WEAK_U_RELATIVE_ERROR_AT_V_0.1_PCT = 0.022602927
STRONG_U_RELATIVE_ERROR_AT_V_10_PCT = 0.932774563
STRONG_U_RELATIVE_ERROR_AT_V_100_PCT = 0.009948479
WEAK_MAX_F_RELATIVE_ERROR_AT_V_0.1_PCT = 0.014425130
STRONG_MAX_F_RELATIVE_ERROR_AT_V_10_PCT = 0.735930758
STRONG_MAX_F_RELATIVE_ERROR_AT_V_100_PCT = 0.005296305
```

| v | exact u* | weak u approx | weak u rel. err. % | strong u approx | strong u rel. err. % | exact max F | weak max F rel. err. % | strong max F rel. err. % |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.01 | 1.606111668 | 1.606115299 | 0.000226 | 101.000000000 | 6188.479315 | 1.32487348e-05 | 0.000144 | 27286808.760094 |
| 0.03 | 1.606082619 | 1.606115299 | 0.002035 | 34.333333333 | 2037.706549 | 0.000119237238 | 0.001298 | 2127220.247896 |
| 0.1 | 1.605752352 | 1.606115299 | 0.022603 | 11.000000000 | 585.037141 | 0.00132468431 | 0.014425 | 105780.705731 |
| 0.3 | 1.602861201 | 1.606115299 | 0.203018 | 4.333333333 | 170.349880 | 0.0119084137 | 0.129865 | 4132.073375 |
| 1 | 1.571482172 | 1.606115299 | 2.203851 | 2.000000000 | 27.268386 | 0.130597785 | 1.447004 | 100.000000 |
| 3 | 1.385588717 | 1.606115299 | 15.915732 | 1.333333333 | 3.771349 | 1.05601798 | 12.913594 | 14.642769 |
| 10 | 1.110357129 | 1.606115299 | 44.648533 | 1.100000000 | 0.932775 | 6.74706866 | 96.363111 | 0.735931 |
| 30 | 1.034461571 | 1.606115299 | 55.260992 | 1.033333333 | 0.109065 | 25.6154578 | 365.495429 | 0.065020 |
| 100 | 1.010100490 | 1.606115299 | 59.005497 | 1.010000000 | 0.009948 | 94.3998295 | 1303.472232 | 0.005296 |

## Interpretation boundary

The endpoints converge as the analysis predicts: the weak approximation is extremely close at small `v`, while `1+1/v` and `v-log(v)-1` become accurate at large `v`. The table deliberately declares **no validity cutoff**; it reports error rather than inventing a threshold for when an asymptotic formula is 'valid'.

There is **no empirical calibration** in this audit. The nine `v` values are registered numerical checkpoints, not biological observations and not evidence for the uniqueness theorem. The exact theorem covers every `v>0`; the grid only makes the endpoint approximations quantitatively inspectable.
