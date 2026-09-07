# Optimal placement of interior-frequency PAYOFF holdouts

Status: exact design result for two explicitly declared nonlinear alternative classes.
This is not an optimal-design theorem over arbitrary nonlinear functions and is not
an empirical sample-size recommendation.

## 1. Setup

The endpoint-derived canonical line is fixed before any interior observations:

```text
Delta_lin(p) = (1-p)u - p v.
```

Write the nonlinear residual as

```text
r(p) = Delta_true(p) - Delta_lin(p).
```

Because the endpoint line uses the same two endpoints, `r(0)=r(1)=0`. Interior
holdout frequencies must be chosen without seeing interior outcomes.

## 2. Minimax theorem for a Lipschitz residual class

Assume only

```text
|r(x)-r(y)| <= L |x-y|.
```

Choose `m >= 1` strict interior frequencies `0<p1<...<pm<1`. Together with the
fixed endpoint anchors 0 and 1, these split the unit interval into `m+1` gaps.
Let `g_max` be the largest gap.

If residuals were exactly zero at all sampled frequencies, every unsampled point
lies within distance at most `g_max/2` of some sampled anchor, hence

```text
|r(p)| <= L * g_max / 2.
```

Every `m`-point design has `g_max >= 1/(m+1)` because the `m+1` gaps sum to one.
Equality is possible only when all gaps are equal. Therefore the global minimax
design is

```text
p_i = i/(m+1),  i=1,...,m,
```

with

```text
g_max* = 1/(m+1)
covering_radius* = 1/[2(m+1)]
worst unsampled residual envelope = L/[2(m+1)].
```

Small cases are therefore:

```text
m=1 -> 1/2
m=2 -> 1/3, 2/3
m=3 -> 1/4, 1/2, 3/4
```

This formalizes when quarter/mid/three-quarter sampling is justified: it is the
exact three-holdout minimax coverage design for a Lipschitz-bounded residual,
not a universal rule for every nonlinear alternative.

## 3. One-point theorem for uniformly signed curvature

Consider a stronger alternative class. Suppose throughout `[0,1]` either

```text
r''(p) >= kappa > 0
```

or

```text
r''(p) <= -kappa < 0,
```

with the sign fixed across the interval and `r(0)=r(1)=0`.

For the first case, compare `r` with `q(p)=kappa*p*(p-1)/2`. Then
`(r-q)'' >= 0` and `(r-q)` is zero at both endpoints. Convexity implies
`r-q <= 0`, hence

```text
r(p) <= -kappa*p*(1-p)/2.
```

The opposite curvature sign gives the symmetric lower bound. Thus in either case

```text
|r(p)| >= kappa*p*(1-p)/2.
```

The factor `p(1-p)` is uniquely maximized at `p=1/2`. Therefore the optimal
single holdout is

```text
p*=1/2
```

and its guaranteed departure from the endpoint line is

```text
kappa/8.
```

So the midpoint has a second, distinct justification: it is the most sensitive
single point against a frequency response whose curvature keeps one sign and has
a known minimum magnitude.

## 4. Why the two results should not be mixed

The Lipschitz result controls how much deviation can hide between sampled points.
It makes no curvature-sign assumption and naturally favors equal coverage as the
number of holdouts increases.

The signed-curvature result gives a lower bound on the deviation at a sampled
point. It is stronger but applies to a narrower alternative class. A function
whose curvature changes sign can evade that theorem even if it is strongly
nonlinear.

Therefore PAYOFF should report the declared alternative class together with the
design. Calling midpoint or equal spacing universally optimal would exceed the
proof.

## 5. Relation to the existing no-refit holdout gate

`src/frequency_response_holdout.py` evaluates observed interior bands after the
frequencies have been registered. `src/frequency_holdout_design.py` chooses the
frequencies before those outcomes exist. The design layer never refits `u`, `v`,
`phi`, or `eta` and never sees holdout responses.

Passing the resulting holdouts still means only compatibility with the canonical
line under the registered checks. It does not prove uniqueness among arbitrary
nonlinear frequency-response families, finite-population fixation, historical
causation, or an ecological mechanism in a natural population.
