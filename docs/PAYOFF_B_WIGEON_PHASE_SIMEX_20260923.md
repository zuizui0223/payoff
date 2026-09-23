# PAYOFF-B wigeon event-structure SIMEX sensitivity

Frozen contract: **2026-09-23**  
Local exact-contract reproduction: **2026-09-23**

Status: **provisional numerical result pending GitHub Actions confirmation**.

This sensitivity uses the real 224 source-faithful wigeon transitions rather
than an IID pair generator. Measurement error is attached to unique staging
events, so the same event error is shared when one staging event is the
destination of a transition and the origin of the next. Errors follow the
frozen individual-year AR(1) process.

Frozen SIMEX settings:

```text
zeta = 0.5, 1.0, 1.5, 2.0
replicates per zeta = 1000
seed = 20260923
quadratic extrapolation -> zeta = -1
```

Observed source-faithful naive estimate:

```text
lambda_hat = 0.749768
```

Provisional exact-contract reproduction:

| sensitivity scenario | error SD (d) | rho | SIMEX lambda |
| --- | ---: | ---: | ---: |
| equal independent replicates | 3.842 | 0 | 0.8070 |
| equal replicates + discrepancy-correlation proxy | 3.842 | 0.288 | 0.7827 |
| conservative full disagreement | 5.434 | 0 | 0.8602 |

Thus the observation-error correction moves lambda upward, as expected, but all
three frozen scenarios remain below one.

The result is deliberately not called a recovered true lambda. Error scales
come from an incomplete POWER-versus-ERA5-Land calibration whose registered
coverage gate failed. SIMEX therefore functions as a robustness/claim audit.

The dedicated GitHub Actions workflow must reproduce the same deterministic
numbers before this receipt is promoted from provisional to canonical.
