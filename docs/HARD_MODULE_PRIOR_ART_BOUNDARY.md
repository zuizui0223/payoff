# Hard-module partition prior-art boundary

The hard-module extension uses standard mathematical and algorithmic ingredients. The manuscript must keep those ingredients separate from the PAYOFF-specific architecture interpretation.

## Established prior art

Optimal one-dimensional k-means / weighted univariate clustering can be solved exactly by dynamic programming after sorting the scalar observations.

A direct reference is:

- Wang H, Song M. 2011. **Ckmeans.1d.dp: Optimal k-means clustering in one dimension by dynamic programming.** The R Journal 3(2):29-33. DOI `10.32614/RJ-2011-015`.

Penalized segmentation and changepoint dynamic programming are also established algorithmic families.

Therefore PAYOFF does **not** claim to invent:

```text
one-dimensional clustering,
contiguous optimal blocks,
dynamic programming for squared-error segmentation,
penalized module-count selection,
or weighted variance decomposition.
```

## PAYOFF-specific derivation

The candidate contribution is the architecture interpretation on the same fitness scale used by SCH/BALANCE/BITA:

```text
function-specific optima theta_i
+ fitness curvatures a_i
        |
        v
one hard module
= one shared coordinate
        |
        v
within-module compromise loss
        |
        v
module split A|B recovers
[A_A A_B/(A_A+A_B)](mu_A-mu_B)^2
        |
        v
compare directly with per-extra-module architecture cost kappa.
```

The split receipt is exactly the same weighted quadratic conflict form used by SCH, now applied recursively to daughter-module centroids.

## Claim ceiling

Use:

```text
we derive an architecture interpretation of the weighted partition loss;
we show that hard-module recovery is exactly between-module conflict;
we map an explicit module cost onto the established optimal 1-D partition problem;
we provide an executable cross-repository handoff.
```

Avoid:

```text
new clustering algorithm;
first dynamic programme for modularity;
first theory that optimal clusters are contiguous;
new changepoint method.
```
