# Identifying architecture selection versus mutation bias from stationary occupancy

The rare-mutation recurrent PAYOFF model gives monomorphic stationary log odds

```text
Y
= log(Pi_N/Pi_0)
= m + beta(N-2)phi,
```

where

```text
m   = log(u_SD/u_DS)
phi = sL-K.
```

This compact formula creates both an identification problem and a simple experimental solution.

---

## Proposition 1 — one stationary occupancy contrast does not identify selection and mutation bias separately

Suppose `N` and `beta` are known and one observes the rare-mutation monomorphic log odds `Y`.

Then

```text
Y=m+beta(N-2)phi.
```

For any candidate `phi'`, choosing

```text
m'=Y-beta(N-2)phi'
```

produces the same observed `Y`.

Therefore a single stationary occupancy contrast identifies only the composite quantity

```text
m+beta(N-2)phi,
```

not `m` and `phi` separately.

### Interpretation

A long-run excess of differentiated architecture can arise from

```text
positive architecture selection phi>0,
mutation/conversion bias u_SD>u_DS,
or both.
```

Stationary abundance alone cannot distinguish these mechanisms.

This is an identification statement, not a limitation of numerical precision.

---

## Theorem 2 — two population sizes identify architecture selection and mutation bias

Assume two rare-mutation populations share the same

```text
phi,
beta,
u_SD/u_DS,
```

but have known different sizes

```text
N_1 != N_2.
```

Their stationary log odds are

```text
Y_1=m+beta(N_1-2)phi,
Y_2=m+beta(N_2-2)phi.
```

Subtracting gives

```text
Y_2-Y_1
= beta(N_2-N_1)phi.
```

Hence, for `beta>0`,

```text
phi
= (Y_2-Y_1)/[beta(N_2-N_1)].
```

Then

```text
m
= Y_1-beta(N_1-2)phi,
```

and therefore

```text
u_SD/u_DS=exp(m).
```

Thus two population sizes identify both the static architecture gap and the mutation bias ratio under the declared rare-mutation model.

### Cross-repository test

The stationary estimate

```text
phi_stationary
```

can be compared prospectively with the independent sister-repository prediction

```text
phi_bridge=sL-K.
```

Agreement is a cross-scale validation. Disagreement exposes at least one failed assumption: common fitness scale, constant mutation bias, constant `phi` across population-size treatments, rare mutation, the exponential Moran mapping, or the architecture bridge itself.

---

## Corollary 2.1 — symmetric mutation needs no intercept estimate

If independent biology establishes

```text
u_SD=u_DS,
```

then `m=0` and one population size already yields

```text
phi
= Y/[beta(N-2)]
```

for `N>2`, `beta>0`.

The two-size design remains useful as an over-identification check: the inferred `phi` should be the same at both sizes if the model is correct.

---

## Theorem 3 — two selection intensities also identify the two components

At fixed `N>2`, suppose two treatments have known

```text
beta_1 != beta_2
```

while `phi` and mutation bias remain unchanged.

Then

```text
Y_1=m+beta_1(N-2)phi,
Y_2=m+beta_2(N-2)phi.
```

Therefore

```text
phi
= (Y_2-Y_1)/[(beta_2-beta_1)(N-2)],
```

and

```text
m=Y_1-beta_1(N-2)phi.
```

This is mathematically equivalent to the population-size design. Its biological usefulness depends on whether a selection-intensity manipulation can be defined without simultaneously changing the ecological payoff geometry.

---

## Corollary 3.1 — multi-treatment regression form

For multiple rare-mutation populations indexed by `j`, if mutation bias is shared and `phi` is shared,

```text
Y_j
= m + X_j phi,
```

where

```text
X_j=beta_j(N_j-2).
```

Hence the stationary design reduces to a straight-line model:

```text
intercept = m = log(u_SD/u_DS)
slope     = phi = sL-K.
```

At least two distinct `X_j` values are needed for algebraic identification. More than two provide an over-identified test of linearity and common-parameter assumptions.

This suggests a particularly clean validation figure:

```text
x-axis: beta(N-2)
y-axis: log(Pi_N/Pi_0)
```

with sister-repository `sL-K` registered in advance as the predicted slope.

---

## Theorem 4 — environmental equal-occupancy crossing is mutation shifted

Suppose the static architecture gap varies linearly with environment:

```text
phi(e)=alpha(e-e0),
alpha != 0,
```

where `e0` is the static SCH/BALANCE/BITA crossing.

Rare-mutation equal monomorphic occupancy requires

```text
m+beta(N-2)phi(e_occ)=0.
```

Therefore

```text
e_occ
= e0 - m/[alpha beta(N-2)].
```

or

```text
e_occ-e0
= -log(u_SD/u_DS)/[alpha beta(N-2)].
```

Thus mutation bias shifts the observed long-run occupancy transition away from the static architecture transition by a predictable amount.

The shift approaches zero as population size or selection intensity increases, holding the mutation bias ratio fixed.

---

## Empirical hierarchy

A strong PAYOFF stationary test should therefore separate three layers:

```text
Layer A — ecological architecture geometry
SCH/BALANCE/BITA estimate L,s,K
-> predict phi_bridge=sL-K

Layer B — population game
reciprocal frequency manipulation estimates eta

Layer C — mutation-selection-drift occupancy
long-run populations estimate Y=log(Pi_N/Pi_0)
across at least two values of beta(N-2)
-> estimate phi_stationary and mutation-bias intercept m.
```

The decisive cross-scale comparison is

```text
phi_stationary ?= phi_bridge.
```

This avoids fitting the entire framework to one stationary distribution and calling agreement a test.

---

## Claim boundary

The idea of using multiple treatments to identify the slope and intercept of a linear relation is elementary, and weak-mutation stationary reductions are established theory. PAYOFF's contribution is the architecture-specific substitution

```text
phi=sL-K
```

which turns the stationary slope into a direct independent test of the SCH/BALANCE/BITA bridge.
