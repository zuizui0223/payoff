# Dactylorhiza generic frequency-game reanalysis readiness v1

Status: prospective observed-range reanalysis handoff for a clean multi-frequency plant reproductive-success analogue.

This system is deliberately treated as a **generic two-morph game-layer test**, not as evidence for the upstream SCH/BALANCE/BITA shared-versus-differentiated architecture mechanism.

## Primary source

Gigord, Macnair & Smithson (2001), PNAS 98:6253–6255, DOI `10.1073/pnas.111162598`, experimentally manipulated the yellow-versus-purple flower-colour frequency of the rewardless orchid *Dactylorhiza sambucina* in synthetic field arrays while maintaining constant plant density.

The design used:

```text
10 arrays
50 plants per array
2 replicate arrays at each yellow-morph frequency
p_yellow in {0.1,0.3,0.5,0.7,0.9}.
```

The reported male and female reproductive-success measures were:

```text
relative pollinia removal
relative pollinia deposition
fruit set.
```

All three relative-success measures declined significantly with the focal morph's frequency. The identity of the fitter morph reversed across the frequency gradient, and the rare morph had higher reproductive success at both extreme observed frequencies.

The authors reported predicted yellow equilibrium frequencies of approximately 0.69 from pollinia removal, 0.72 from pollinia deposition, and 0.61 from fruit set.

A 2004 PNAS correction states that the Fig. 3b symbol labels for fruit set and pollinia deposition were switched in the original graph. Any figure extraction must therefore use the corrected labeling.

## Why this is a particularly useful PAYOFF analogue

Unlike a two-context or natural-frequency correlation, this experiment contains five preplanned frequency settings spanning most of the unit interval at fixed density.

That makes it naturally compatible with PAYOFF's no-refit frequency-response logic:

```text
outer observed frequencies -> freeze an observed-range affine prediction
interior observed frequencies -> independent holdouts.
```

However, `p=0.1` and `p=0.9` are not true rare-invasion endpoints. They must not be relabeled as `p=0` and `p=1`, and no reciprocal-invasion `u,v` claim is licensed from this design alone.

## Frozen observed-range reanalysis

Let

```text
p = yellow-morph frequency
Delta(p) = reproductive_success_yellow(p)-reproductive_success_purple(p)
```

on a common reproductive-success scale where the source data permit reconstruction.

For each outcome separately:

```text
pollinia removal
pollinia deposition
fruit set
```

use the outer observed support

```text
p=0.1 and p=0.9
```

to freeze the unique secant prediction over the observed range. Then evaluate

```text
p=0.3,0.5,0.7
```

as no-refit holdouts.

This is an observed-range affine transportability test. It is not endpoint identification of canonical PAYOFF `phi,eta` on `[0,1]` unless actual endpoint data or an independently justified extrapolation model becomes available.

## Alternative parameterization

If individual- or array-level data support direct estimation, an affine model may be written over the observed support as

```text
Delta(p)=alpha+beta p.
```

The PAYOFF-form coordinates are algebraically related by

```text
eta=beta/2,
phi=alpha+beta/2,
```

but these should be reported as **generic two-morph game coordinates** only. They do not equal architecture `phi=sL-K` or architecture `eta` without an independent architecture mapping.

The stricter no-refit analysis remains preferable for testing transportability because it separates fitting frequencies from validation frequencies.

## Exact claim ladder for this system

If only the published qualitative pattern is used:

```text
A_MANIPULATED_MULTIFREQUENCY_FREQUENCY_FEEDBACK_RECOVERED
```

If numerical array-level outcomes are recovered:

```text
A_MULTIFREQUENCY_RELATIVE_MARGIN_RECONSTRUCTABLE
```

If the outer-frequency secant survives all three interior holdouts for a declared outcome:

```text
A_OBSERVED_RANGE_AFFINE_FREQUENCY_RESPONSE_COMPATIBLE
```

If one or more holdouts reject:

```text
A_OBSERVED_RANGE_AFFINE_FREQUENCY_RESPONSE_REJECTED
```

Both compatibility and rejection are informative outcomes.

None of these promote the study to PAYOFF Lane P.

## Frozen extraction requirements

Prefer, in descending order:

```text
individual-level raw data
array-level morph-specific means and denominators
array-level relative reproductive-success values with uncertainty
figure-derived values only as an explicitly approximate exploratory fallback.
```

Required fields are:

```text
array_id
p_yellow
yellow_n
purple_n
yellow_pollinia_removed
purple_pollinia_removed
yellow_pollinia_deposited
purple_pollinia_deposited
yellow_fruit_set
purple_fruit_set
or directly reported comparable relative-success quantities
```

Do not merge male and female reproductive components into a single fitness score without a preregistered biological aggregation rule.

## What this system can and cannot validate

A successful reanalysis can show that the **minimal affine two-strategy frequency-response layer** used by PAYOFF is compatible with a manipulated real plant polymorphism over a broad observed frequency range.

It cannot show:

```text
shared-versus-differentiated architecture competition;
SCH conflict load L;
BITA recovery R;
architecture cost K;
phi=sL-K;
PAYOFF architecture eta;
mutualist-antagonist trade-off;
historical architecture splitting.
```

The frequency dependence here is pollinator-mediated rare-colour advantage in a rewardless orchid. Its value for PAYOFF is as a clean game-layer reality check and falsification dataset, not as upstream mechanism validation.

## Current readiness labels

```text
DACTYLORHIZA_MANIPULATED_FIVE_FREQUENCY_DESIGN_RECOVERED
DACTYLORHIZA_RARE_MORPH_REVERSAL_RECOVERED
DACTYLORHIZA_THREE_REPRODUCTIVE_COMPONENTS_RECOVERED
DACTYLORHIZA_FIGURE_LABEL_CORRECTION_RECORDED
DACTYLORHIZA_NUMERIC_ARRAY_DATA_NOT_YET_RECOVERED
DACTYLORHIZA_OBSERVED_RANGE_NO_REFIT_TEST_PREDECLARED
DACTYLORHIZA_ARCHITECTURE_MAPPING_NOT_ESTABLISHED
```
