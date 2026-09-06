# Universal triangular-kernel barrier phase curve

The exact triangular-kernel barrier theorem can be reduced to a dimensionless
interaction-range curve.

Assume the unconstrained intrinsic optimum

```text
r* = alpha/kappa
```

lies inside the architecture interval, and define

```text
E = epsilon/r* = kappa epsilon/alpha in (0,1)
g = G/kappa = -gamma/kappa > 0.
```

The global-better-across-barrier phase depends only on `(E,g)`.

## Lower boundary: ridge onset

The local ridge appears when

```text
g > g_on(E)
```

with

```text
g_on(E)=1/E-1.
```

## Upper boundary: local ridge catches the outside optimum

At the upper boundary, let

```text
x = r_m/r*.
```

Stationarity of the local ridge together with equal payoff to the outside
intrinsic optimum eliminates `g` and gives

```text
x^2 - 3x + 2E = 0.
```

The admissible branch is

```text
x(E)=[3-sqrt(9-8E)]/2.
```

Since the same equation implies

```text
E=x(3-x)/2,
```

the upper feedback curve simplifies to

```text
g_hi(E)
=(1-x)(3-x)/(2x^2).
```

Therefore the exact dimensionless barrier phase is

```text
g_on(E) < g < g_hi(E),
0<E<1.
```

The width is strictly positive throughout `(0,1)`.  Using the `x` parameter,

```text
g_hi-g_on
=(1-x)(9-10x+3x^2)
 /(2x^2(3-x)),
```

and the quadratic `9-10x+3x^2` is positive for real `x` because its
discriminant is negative.

## Interaction range near the intrinsic optimum

Let

```text
delta=1-E -> 0+.
```

Then

```text
g_on ~ delta
g_hi ~ 2 delta
g_hi-g_on ~ delta.
```

So as the interaction support reaches the intrinsic optimum, the entire
barrier window collapses linearly to zero feedback strength.

## Very narrow interaction range

As

```text
E -> 0+,
```

```text
g_on ~ 1/E,
g_hi ~ 27/(8E^2),
g_hi-g_on ~ 27/(8E^2).
```

Thus a very narrow interaction neighbourhood requires diverging negative
feedback before a ridge can form, while the upper boundary diverges even faster.
The barrier window is therefore not controlled by feedback strength alone: the
physical interaction range is an equally essential estimand index.

## Registered example

For

```text
alpha=0.5
kappa=1
epsilon=0.3
```

```text
r*=0.5
E=0.6
```

and the universal curve returns

```text
g_on=2/3
g_hi=2.93184698670244...
```

which recovers the dimensional result

```text
-2.93184698670244... < gamma < -2/3.
```

Implementation:

```text
src/triangular_kernel_phase_curve.py
tests/test_triangular_kernel_phase_curve.py
```

## Claim boundary

This universal curve is universal only within the declared one-dimensional
quadratic intrinsic payoff and triangular interaction kernel after the stated
non-dimensionalization.  Other interaction kernels have separate accessibility
geometry, as shown by the kernel-robustness and adverse-control results.
