# Spatial aggregation and identification

The patch-network PAYOFF model has local field

```text
f(p)=p(1-p)[phi+eta(2p-1)].
```

Under symmetric conservative migration, migration cancels from the global mean. The remaining mean-selection term admits an exact two-coefficient form that is useful for identification.

## Theorem 1 — exact `phi A + eta B` decomposition

For patch frequencies `p_j`, define

```text
A = E[p(1-p)],
B = E[p(1-p)(2p-1)].
```

Then

```text
d p_bar/dt
= phi A + eta B.
```

### Proof

Average the local selection field directly:

```text
E[f(p)]
= E[p(1-p){phi+eta(2p-1)}]
= phi E[p(1-p)]
+ eta E[p(1-p)(2p-1)].
```

Symmetric migration contributes zero to the mean. QED.

## Corollary 1.1 — moment representation

Let

```text
mu = E[p],
V  = E[(p-mu)^2],
T  = E[(p-mu)^3].
```

Then

```text
A = mu(1-mu)-V,
```

and

```text
B
= mu(1-mu)(2mu-1)
+ V(3-6mu)
- 2T.
```

Thus

```text
dmu/dt
= phi[mu(1-mu)-V]
+ eta[mu(1-mu)(2mu-1)+V(3-6mu)-2T].
```

This is algebraically equivalent to the spatial-moment correction in `SPATIAL_METAPOPULATION.md`.

## Corollary 1.2 — `A` is an exact selection-active mass

Because

```text
p(1-p)>=0
```

for every patch,

```text
A>=0.
```

Moreover,

```text
A=0
```

iff every patch is locally monomorphic (`p_j` is 0 or 1).

When `A=0`, local selection is instantaneously zero in every patch for every `phi,eta`; conservative migration can move patch frequencies but cannot change the global mean instantaneously.

---

## Theorem 2 — instantaneous spatial zero-growth value of `phi`

If

```text
A>0,
```

the architecture gap that gives zero instantaneous metapopulation mean change is uniquely

```text
phi_sp
= -eta B/A.
```

This is a configuration-specific aggregated zero-growth condition, not a replacement for the upstream static architecture quantity

```text
phi=sL-K.
```

### Special case: no spatial heterogeneity

If every patch has the same frequency `mu`, then

```text
A=mu(1-mu),
B=mu(1-mu)(2mu-1),
```

and

```text
phi_sp=-eta(2mu-1),
```

which is exactly the well-mixed condition

```text
Delta(mu)=0.
```

### Special case: symmetric midpoint configuration

If

```text
mu=1/2,
T=0,
A>0,
```

then

```text
B=0
```

and therefore

```text
phi_sp=0
```

for any variance `V<1/4`.

Spatial segregation changes the magnitude of mean selection but not the sign boundary at a symmetric midpoint.

---

## Theorem 3 — algebraic identification from short-term spatial change

Suppose patch frequencies are measured at one instant and the short-term metapopulation mean change

```text
g = d p_bar/dt
```

is measured over a sufficiently short interval that the deterministic patch configuration can be treated as fixed for the contrast.

If `eta` is independently known and `A>0`, then

```text
phi
= (g-eta B)/A.
```

If `phi` is independently known and `B!=0`, then

```text
eta
= (g-phi A)/B.
```

These identities provide a spatial cross-check rather than a recommendation to estimate both unknowns from one aggregate change.

### Preferred cross-repository test

Use sister repositories to register

```text
phi_bridge=sL-K.
```

Use a well-mixed or controlled frequency experiment to estimate

```text
eta.
```

Then use patch moments to predict

```text
g_pred
= phi_bridge A + eta B.
```

and compare it with the observed short-term global mean change.

This is stronger than fitting `phi` and `eta` to the same spatial trajectory.

---

## Corollary 3.1 — why aggregated well-mixed fits can be biased

A naive well-mixed analysis at mean frequency `mu` assumes

```text
g
= mu(1-mu)[phi+eta(2mu-1)].
```

The spatial truth is

```text
g
= phi A + eta B.
```

Because

```text
A != mu(1-mu)
```

and generally

```text
B != mu(1-mu)(2mu-1),
```

spatial variance and skewness can be misinterpreted as changes in `phi` or `eta`.

Therefore an apparent architecture-frequency interaction in pooled spatial data is not by itself an identified PAYOFF `eta`.

---

## Claim boundary

The decomposition is an algebraic consequence of the declared cubic PAYOFF field plus conservative migration. It is not a universal aggregation theorem for arbitrary spatial evolutionary games.

Directed migration, unequal patch sizes, density-dependent weighting, nonlinear frequency feedback, or patch-specific payoff parameters require a different aggregation formula.
