# Universal triangular-kernel barrier phase curve

The exact triangular-kernel barrier theorem reduces to a dimensionless phase
curve.

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

## Feedback window at fixed interaction range

The local ridge onset is

```text
g_on(E)=1/E-1.
```

At the upper boundary, let `x=r_m/r*`. Stationarity of the local ridge together
with equal payoff to the outside intrinsic optimum gives

```text
x^2 - 3x + 2E = 0,
```

with admissible root

```text
x(E)=[3-sqrt(9-8E)]/2.
```

Since

```text
E=x(3-x)/2,
```

the upper feedback curve is

```text
g_hi(E)=(1-x)(3-x)/(2x^2).
```

Therefore

```text
g_on(E) < g < g_hi(E),
0<E<1.
```

The width is strictly positive throughout `(0,1)`:

```text
g_hi-g_on
=(1-x)(9-10x+3x^2)/(2x^2(3-x)) > 0.
```

## Interaction-range window at fixed feedback

The same phase can be inverted.  For a fixed `g>0`, ridge onset requires

```text
E > E_lo(g)=1/(1+g).
```

The upper boundary solves `g=g_hi`. In the contact coordinate this becomes

```text
(2g-1)x^2 + 4x - 3 = 0.
```

For `g != 1/2`,

```text
x_hi(g)
=[sqrt(1+6g)-2]/(2g-1),
```

while at `g=1/2` the regular limiting solution is

```text
x_hi=3/4.
```

Then

```text
E_hi(g)=x_hi(3-x_hi)/2.
```

So the same barrier exists exactly for

```text
E_lo(g) < E < E_hi(g).
```

This gives a non-monotone locality result: at fixed feedback, an interaction
range that is too narrow cannot form the local ridge, while a range that is too
broad raises the ridge enough that the outside intrinsic architecture is no
longer better.  A global-better accessibility barrier occurs only at
**intermediate interaction range**.

Example:

```text
g=2
-> E_lo=1/3
-> E_hi=0.6595648100573256...
```

Thus the registered `E=0.6` case lies in the barrier phase, while `E=0.3` is too
narrow and `E=0.7` is too broad.

## Interaction range near the intrinsic optimum

Let `delta=1-E -> 0+`. Then

```text
g_on ~ delta
g_hi ~ 2 delta
g_hi-g_on ~ delta.
```

As interaction support reaches the intrinsic optimum, the feedback window
collapses linearly to zero.

## Very narrow interaction range

As `E -> 0+`,

```text
g_on ~ 1/E,
g_hi ~ 27/(8E^2),
g_hi-g_on ~ 27/(8E^2).
```

A very narrow interaction neighbourhood therefore requires diverging negative
feedback before a ridge can form, with an even faster-diverging upper boundary.

## Registered dimensional example

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

and

```text
g_on=2/3
g_hi=2.93184698670244...
```

so

```text
-2.93184698670244... < gamma < -2/3.
```

Implementation:

```text
src/triangular_kernel_phase_curve.py
tests/test_triangular_kernel_phase_curve.py
```

## Claim boundary

The curve is universal only within the declared one-dimensional quadratic
intrinsic payoff and triangular interaction kernel after this
non-dimensionalization. Other interaction kernels have separate accessibility
geometry, as shown by the kernel-robustness and adverse-control results.
