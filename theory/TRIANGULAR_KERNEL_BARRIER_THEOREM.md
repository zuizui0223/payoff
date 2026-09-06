# Exact triangular-kernel barrier geometry

For a shared resident at architecture `r=0`, negative frequency feedback
`gamma<0`, and triangular interaction weight

```text
w(r)=max(0,1-r/epsilon),
```

write

```text
G=-gamma>0.
```

Inside the interaction support,

```text
p(r)
= alpha r - (kappa/2)r^2
  + G r^2(1-r/epsilon),
```

so

```text
p'(r)
= alpha + (2G-kappa)r - (3G/epsilon)r^2.
```

Outside the support,

```text
p(r)=alpha r-(kappa/2)r^2,
p'(r)=alpha-kappa r.
```

## Exact ridge/dip onset

At the kernel boundary,

```text
p'(epsilon^-)=alpha-(G+kappa)epsilon
p'(epsilon^+)=alpha-kappa epsilon.
```

Therefore, if

```text
epsilon < alpha/kappa
```

and

```text
G > G_on = alpha/epsilon - kappa,
```

then

```text
p'(0)>0,
p'(epsilon^-)<0,
p'(epsilon^+)>0.
```

There is exactly one local maximum inside `(0,epsilon)` and the kernel boundary
is a local minimum. The local maximum is

```text
r_m
= epsilon [(2G-kappa)
  + sqrt((2G-kappa)^2 + 12G alpha/epsilon)]/(6G).
```

This is an exact continuous architecture result; it does not depend on a finite
grid.

## A ridge/dip is not yet an accessibility barrier to a better global state

The outside intrinsic optimum is

```text
r*=alpha/kappa
```

when it lies inside the feasible architecture interval. A biologically relevant
across-valley barrier additionally requires

```text
p(r*) > p(r_m).
```

The distinction matters because feedback strength is not monotone in the final
accessibility statement.

## The global-better barrier exists on one finite feedback window

Once the interior local maximizer exists, the envelope theorem gives

```text
d p(r_m;G) / dG
= r_m^2(1-r_m/epsilon)
> 0.
```

So the optimized local-ridge payoff rises strictly with `G`. The outside
intrinsic optimum `p(r*)` does not depend on `G`. At ridge onset the local ridge
coincides with the kernel boundary and lies below `p(r*)` whenever
`epsilon<r*`; for sufficiently large `G` the ridge payoff diverges upward.
Therefore there is a unique upper feedback strength `G_hi` satisfying

```text
p(r_m(G_hi);G_hi)=p(r*).
```

The **global-better-across-barrier** phase is exactly

```text
G_on < G < G_hi.
```

In the original signed feedback coordinate this is

```text
-G_hi < gamma < -G_on.
```

For the registered parameters

```text
alpha=0.5
kappa=1
epsilon=0.3
```

the executable receipt gives

```text
G_on = 2/3
G_hi = 2.93184698670244...
```

so

```text
-2.93184698670244... < gamma < -0.66666666666667...
```

is the finite feedback window in which a local ridge/dip exists **and** a better
outside intrinsic architecture remains across the valley.

Representative points are:

```text
G=0.5
-> no ridge/dip before epsilon

G=2
-> ridge/dip exists
-> r_m=0.25
-> p(r_m)=0.1145833...
-> p(epsilon)=0.105
-> p(r*)=0.125
-> a better outside state lies across the valley

G=5
-> ridge/dip still exists
-> but the local ridge itself exceeds p(r*)
-> there is no longer a globally better outside state to be reached.
```

Thus stronger negative frequency feedback first creates an accessibility
bottleneck and later removes the **global-better-across-barrier** condition by
making the near-resident ridge itself globally superior.

Implementation:

```text
src/triangular_kernel_barrier.py
tests/test_triangular_kernel_barrier.py
```

## Relation to the grid-refinement certificate

The earlier finite-grid triangular witness

```text
gamma=-2, epsilon=0.3
```

has a positive critical jump distance under grid refinement. The exact theorem
here explains the continuous payoff geometry responsible for that numerical
certificate.

## Claim boundary

The theorem is specific to the quadratic intrinsic payoff, shared resident at
`0`, triangular distance kernel, negative feedback, and one-dimensional
architecture coordinate. The existence of a local ridge/dip does not by itself
specify stochastic crossing times or fixation probabilities.
