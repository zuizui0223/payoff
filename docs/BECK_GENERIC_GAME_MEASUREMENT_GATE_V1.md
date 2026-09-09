# Beck generic game measurement gate v1

Lane: **G only**.

This document starts only after the public workbook has independently passed the R3 raw-reconstruction gate. It does not use or strengthen Lane A architecture mapping.

Primary source:

```text
Beck et al. 2022
Environment Constrains Fitness Advantages of Division of Labor in Microbial Consortia Engineered for Metabolite Push or Pull Interactions
mSystems 7(4):e00051-22
DOI 10.1128/msystems.00051-22
```

## 1. Why a scalar PAYOFF gap is not pre-existing in this study

The paper compares WT and synthetic consortia using six distinct performance metrics:

```text
1. final biomass titer
2. total glucose catabolized
3. biomass produced per glucose consumed
4. biomass produced per H+ accumulated
5. by-product accumulation
6. specific growth rate
```

These metrics do not all rank the alternatives in the same direction.

Accordingly, the phrase `fitness advantage` in the paper cannot be imported into PAYOFF as a unique scalar `Delta` without declaring how these biological objectives are scalarized.

## 2. Frozen metric orientation

For the architecture-neutral candidate label `LAE consortium` versus comparator `WT`, orient the metrics as:

```text
higher final biomass titer          -> better
higher total glucose catabolized   -> better
higher biomass / glucose           -> better
higher biomass / H+ accumulated    -> better
lower by-product accumulation      -> better
higher specific growth rate        -> better
```

These directions are frozen before scalarization.

No `shared`, `differentiated`, `integrated`, or `released` semantics are used in this gate.

## 3. Weak-buffer context

The primary paper reports that the LAE consortium, relative to WT under weak buffering, has:

```text
final biomass titer:          better
substrate/glucose conversion: better
biomass per H+:               better
by-product accumulation:      better (less accumulation)
specific growth rate:         worse
biomass per glucose:          comparable / no directional claim frozen here
```

The last metric is deliberately registered as `unresolved`, not `zero`. A reported comparable/non-significant difference is not an exact equality statement.

Thus the direction-normalized vector contains both positive and negative components.

For any scalar aggregate

```text
Delta_w = sum_j w_j d_j,
```

with all `w_j > 0`, sufficiently different positive weight choices can emphasize either a metric favoring LAE or the growth-rate metric favoring WT.

Therefore:

```text
WEAK_BUFFER_WEIGHT_INVARIANT_SCALAR_SIGN = NOT IDENTIFIED
```

The result is a real performance trade-off, not a failure of the experiment.

## 4. Strong-buffer context

When conventional/high buffering is used, the paper reports WT as superior in five of the six considered performance metrics, while the LAE consortium retains the advantage of no measurable stationary-phase by-product accumulation.

The oriented vector is therefore again mixed:

```text
five metrics: favor WT
by-product accumulation: favors LAE
```

Hence:

```text
STRONG_BUFFER_WEIGHT_INVARIANT_SCALAR_SIGN = NOT IDENTIFIED
```

This is an environment-dependent change in the performance vector, but still not a unique scalar PAYOFF gap without a declared scalarization.

## 5. What would be required for a scalar generic-game estimand

A subsequent G-lane analysis may proceed in one of three ways, but must choose before inspecting the desired result:

```text
G-scalar route 1:
    predeclare one biologically justified primary performance metric;

G-scalar route 2:
    predeclare an external utility/fitness weighting w over the six metrics;

G-vector route:
    retain the Pareto/multimetric object and do not call it canonical scalar PAYOFF.
```

Post hoc selection of the metric on which the preferred strategy wins is prohibited.

## 6. Frequency limitation

The Beck study compares WT and consortium performance across environmental conditions, but it does not supply the required WT:consortium resident-frequency series for identifying `eta`.

Therefore even after a future scalar metric is chosen:

```text
frequency_support = false
eta = not identified
reciprocal invasion phase = not identified
canonical affine Delta(p) = not validated
```

At most, a separately justified scalar metric could provide an environment-specific **static generic performance gap**.

## 7. Relationship to R and A lanes

Lane R currently establishes:

```text
Beck workbook R3 reconstructed
```

That only guarantees an auditable data substrate.

Lane A currently remains:

```text
BECK_ARCHITECTURE_MAPPING_NOT_CERTIFIED
```

because the pathway-partitioned state is a multi-strain consortium and its strategic-unit equivalence to a single WT lineage has not been independently established.

Neither result changes because of this G-lane multimetric audit.

## 8. Current labels

```text
BECK_MULTIMETRIC_PERFORMANCE_VECTOR_RECOVERED_FROM_PRIMARY_SOURCE
BECK_WEIGHT_INVARIANT_SCALAR_PAYOFF_SIGN_NOT_IDENTIFIED
BECK_GENERIC_STATIC_SCALAR_GAP_NOT_YET_REGISTERED
BECK_FREQUENCY_GAME_NOT_IDENTIFIED
BECK_ETA_NOT_IDENTIFIED
BECK_ARCHITECTURE_MAPPING_NOT_PROMOTED_FROM_GAME_LAYER
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
```

## 9. Manuscript wording

Allowed:

> The Beck synthetic consortium data provide an independently reconstructed multimetric performance substrate and demonstrate an environment-dependent trade-off between consortium yield/resource-use benefits and growth-rate cost. Because the reported metrics do not induce a weight-invariant ordering, we do not collapse them post hoc into a scalar game payoff.

Avoid:

> The Beck data show that the differentiated architecture has positive PAYOFF fitness.

Avoid:

> The public raw data identify PAYOFF eta.
