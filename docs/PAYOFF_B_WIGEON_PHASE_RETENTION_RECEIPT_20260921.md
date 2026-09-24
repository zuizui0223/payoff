# PAYOFF-B Eurasian wigeon phase-retention receipt — superseded

Frozen originally: 2026-09-21  
Superseded: **2026-09-22**

Status: **SUPERSEDED BY SOURCE-FAITHFUL TGS REVALIDATION**.

The numerical result formerly frozen in this file used the correct published
5 C cumulative-minimum TGS rule but applied it to a full-calendar-year NASA
POWER series.

A source audit on 2026-09-22 recovered the missing published preprocessing
contract:

```r
days <- days[month(days)<8]
```

so the environmental series must be restricted to January--July before TGS is
computed. The full-year reconstruction produced artificial day-365/366 TGS
onsets in cold northern cell-years and phase values near -200 d.

The old values

```text
lambda_hat = 0.85994
stopover slope = -0.000140
stopover p = 0.972
```

must not be used.

The source-faithful corrected result is frozen in:

```text
docs/PAYOFF_B_WIGEON_PHASE_RETENTION_REVALIDATED_20260922.md
data/wigeon_phase_retention_observation_20260921.json
data/wigeon_stopover_actuator_observation_20260921.json
data/wigeon_tgs_source_window_revalidation_20260922.json
```

Corrected summary:

```text
transitions = 224
individuals = 28

lambda_hat = 0.749768021
SE = 0.049905667
naive p versus lambda_hat=1 = 5.328e-07

primary lambda<1 gate:
    PASS

strong |lambda_hat|<0.75 point gate:
    PASS, narrowly

W2 stopover slope:
    -0.0628626 d/d
cluster SE:
    0.0277386
conventional clustered p:
    0.03166

formal preregistered directional W2 gate:
    PASS

fixed p threshold preregistered:
    NO

secondary 0.3<g_S<0.8 band:
    FAIL

travel-speed diagnostic:
    NOT SUPPORTED
```

The corrected lambda remains a naive errors-in-variables estimator. Biological
interpretation of latent lambda and cross-system lambda magnitude differences
remains conditional on the separately frozen measurement-error validation layer.

Do not cite the superseded 0.85994 result as the current wigeon estimate.
