# Grid-refinement certificate for kernel accessibility barriers

Finite-grid PAYOFF accessibility can show a critical jump larger than one bin
for two very different reasons:

1. a genuine positive architecture-distance bottleneck survives refinement, or
2. the only obstruction is numerical resolution and the physical critical
   distance shrinks with the grid step.

The kernel barrier audit now separates these cases by repeating the same shared
resident calculation over increasingly fine regular grids.

Implementation:

```text
src/kernel_barrier_resolution.py
tests/test_kernel_barrier_resolution.py
```

## Positive-barrier witnesses

Using the registered smooth-kernel examples and grids with 321, 641 and 1281
bins on `[0,1]`, the critical strict-uphill jump distances stabilize at positive
values:

```text
triangular: gamma=-2,  epsilon=0.3
  delta_c -> about 0.059

cosine:     gamma=-3,  epsilon=0.3
  delta_c -> about 0.066-0.069

gaussian:   gamma=-20, epsilon=0.05
  delta_c -> about 0.044-0.047
```

The registered certificate requires the refinement tail spread to be below
`0.005` and the lower edge to exceed two cells of the finest grid.

These witnesses therefore do not disappear when the numerical grid is refined.
They support a positive continuum-scale accessibility bottleneck for the
registered resident payoff profiles, subject to the declared kernel family and
strict-uphill path definition.

## Adverse control

For

```text
alpha=0.5
kappa=1
gamma=-1
epsilon=0.1
```

with triangular, cosine or Gaussian smoothing, the critical radius is exactly
one bin at every audited resolution.  Hence

```text
delta_c(h) = h -> 0.
```

The apparent finite-grid jump therefore vanishes in physical architecture
distance under refinement.  This is the correct negative control for claiming
a positive continuum barrier.

## Consequence

The stronger distinction is now

```text
critical jump bins > 1 on one grid
!=
positive continuum-scale accessibility barrier.
```

A biological evolvability claim should be supported by a grid-refinement
certificate in addition to a kernel-family sensitivity audit.

## Claim boundary

This remains deterministic resident-landscape accessibility.  It is not a
fixation probability, first-passage time, or statement that stochastic mutation
can never cross a valley.  The refinement certificate addresses numerical
resolution only; kernel misspecification remains a separate uncertainty axis.
