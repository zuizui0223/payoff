# PAYOFF-B parallel-control prior-consistency receipt

Frozen: **2026-09-25**

Machine source:

`data/payoff_b_amaral_parallel_control_prior_consistency_20260925.json`

## Why this receipt exists

The registered bird holdout rejected the prediction that stronger historical
timing responsiveness should flatten later mismatch dependence on movement
speed. That result is not rescued by fitting a different model.

Instead, we ask whether the **published source analysis itself** is at least
consistent with a phase–velocity division of labor.

This is prior-consistency evidence, not a new confirmatory test.

## Published bird-speed responses

From Amaral et al. (2025), fixed source commit
`62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`, Table 1:

### Model 2 — bird migration speed

```text
green-up date anomaly   = -0.549  (95% CI -0.770 to -0.327)
green-up speed anomaly  = +0.088  (95% CI +0.041 to +0.134)
migratory cell          = +0.130  (95% CI +0.055 to +0.205)
```

Thus migration speed itself responds to environmental timing and propagation.

### Model 3 — species traits and bird migration speed

```text
species sensitivity     = +0.119  (95% CI -0.034 to +0.203)
species first arrival   = +0.203  (95% CI +0.110 to +0.295)
```

The source-study definition of `xi_mean` is the posterior mean
species-specific sensitivity of arrival timing to green-up.

The sensitivity coefficient is uncertain, but importantly it is **not
negative**. The published source analysis therefore supplies no evidence for a
simple cross-species tradeoff in which stronger timing response implies slower
or less important migration speed.

## Connection to the fresh holdout

Fresh registered holdout:

```text
q² × timing responsiveness = +0.0351 ± 0.0289
p = 0.2249
registered direction = negative
classification = FAIL_WRONG_DIRECTION
```

The two evidence layers support only the conservative synthesis:

> **Timing and movement speed can respond in parallel to environmental forcing;
> stronger timing responsiveness does not make movement-speed matching
> dispensable.**

This does not license a positive complementarity claim. The holdout interaction
is unsupported, and the published species-sensitivity coefficient overlaps
zero.

## Mechanistic interpretation

For a moving environmental wave, a timing shift primarily changes **phase**,
whereas the difference between animal and environmental front speeds controls
how mismatch accumulates through time.

Hence a species can improve alignment through timing while still needing speed
adjustment to keep pace spatially.

This is the proposed explanation for why the timing-responsiveness main effect
is negative in the holdout while the registered flattening interaction fails.
