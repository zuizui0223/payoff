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
G > alpha/epsilon - kappa,
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

For

```text
alpha=0.5
kappa=1
epsilon=0.3
```

the registered cases are:

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

Thus stronger negative frequency feedback can first create an accessibility
bottleneck and later remove the **global-better-across-barrier** condition by
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
