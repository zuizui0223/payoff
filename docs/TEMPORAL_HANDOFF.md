# Temporal empirical handoff for PAYOFF

This document specifies what must be measured before applying the temporal PAYOFF layer.

The core rule is:

> do not fit seasonal architecture payoffs and temporal rescue from the same response curve if the goal is to test the theory.

The preferred design freezes upstream quantities first and predicts temporal invasion out of sample.

---

## 1. Seasonal architecture receipts

For each patch `j` and season `l`, estimate or register

```text
L_jl   shared-coordinate conflict load
s_jl   recoverable fraction under extra dimensionality
K_jl   architecture cost
eta_jl local frequency-feedback coefficient, if supported.
```

Then construct

```text
phi_jl=s_jl L_jl-K_jl.
```

Rare differentiated architecture has local linear margin

```text
r_jl^D=phi_jl-eta_jl,
```

while rare shared architecture has

```text
r_jl^S=-phi_jl-eta_jl.
```

These should be treated as upstream inputs to temporal dynamics.

---

## 2. Temporal and movement receipts

Independently record

```text
season durations tau_l,
season ordering,
migration/connectivity rate m,
patch graph or explicit two-patch connection.
```

If migration itself varies by season, the current symmetric fixed-migration theorems do not apply directly; use a more general Floquet operator and lower the claim ceiling accordingly.

---

## 3. Mandatory temporal null

First test whether seasonality is only a common additive shift:

```text
r_jl = r_j0 + q_l
```

for every patch `j`.

If so,

```text
A(t)=A0+q(t)I
```

and the exact long-run invasion exponent depends only on the time mean:

```text
Lambda_temporal=Lambda0+mean(q).
```

Zero-mean common seasonality has no additional Floquet effect.

Do not fit a temporal-rescue term in this commuting case.

---

## 4. Two-season relative-contrast test

If relative patch quality changes across two seasons, compute

```text
c_l=r_1l-r_2l.
```

The noncommutativity gate is

```text
m(c_1-c_2) != 0.
```

For the declared symmetric two-patch model, compute both

```text
Lambda_avg
```

from the time-averaged invasion operator and

```text
Lambda_F
```

from the exact two-season Floquet formula.

Registered prediction:

```text
Lambda_F>=Lambda_avg.
```

The temporal premium is

```text
Delta_temp=Lambda_F-Lambda_avg.
```

A direct temporal rescue occurs when

```text
Lambda_avg<0<Lambda_F.
```

---

## 5. Rapid-switching prediction

For total period `T`, first-season fraction `w`, migration `m`, seasonal patch contrasts `c_1,c_2`, and

```text
delta_bar
= sqrt(
    [w c_1+(1-w)c_2]^2/4
    + m^2
  ),
```

the declared two-season model predicts

```text
Delta_temp
=
T^2 w^2(1-w)^2 m^2(c_1-c_2)^2
/[24 delta_bar]
+O(T^4).
```

A strong experiment varies the period while keeping the seasonal margins and season fraction fixed, then tests

```text
Delta_temp/T^2
-> registered coefficient.
```

---

## 6. Anti-phase source-switching design

The cleanest temporal experiment is the symmetric anti-phase case:

```text
season A: (r_bar+x, r_bar-x)
season B: (r_bar-x, r_bar+x)
```

with equal season duration `tau`.

The exact prediction is

```text
Lambda_F
=
r_bar-m
+(1/tau)
asinh[
  m/sqrt(m^2+x^2)
  *sinh(tau sqrt(m^2+x^2))
].
```

The time-average prediction is simply

```text
Lambda_avg=r_bar.
```

Thus the temporal premium is identified without any additional fitted temporal parameter.

---

## 7. Intermediate-migration falsification test

For `x!=0`, the anti-phase premium satisfies

```text
P(0)=0,
P(m)>0 for finite m>0,
P(m)->0 as m->infinity.
```

Therefore temporal rescue should peak at intermediate migration.

A prospective test should:

```text
1. estimate r_bar and x before the migration manipulation;
2. choose several migration treatments spanning low to high connectivity;
3. predict Lambda_F(m) from the exact formula;
4. compare observed rare-architecture growth with the frozen curve.
```

The model is challenged if the peak occurs at an incompatible migration scale or if the observed curve is monotone despite the registered anti-phase conditions.

---

## 8. Weak-contrast quantitative prediction

If

```text
|x|tau << 1,
```

then

```text
m_opt tau
~= 1.6061152988
```

and

```text
P_max
~= 0.13248753945 x^2 tau.
```

Thus a negative mean margin is approximately rescuable when

```text
-r_bar
< 0.13248753945 x^2 tau.
```

This creates two especially clean prospective predictions:

```text
optimal migration scale
and
maximum rescue budget.
```

Neither needs to be fitted from the migration-response curve itself.

---

## 9. Recommended response variables

Depending on the biological system, rare-architecture growth can be represented by a common-fitness-scale quantity such as

```text
per-capita population growth,
relative lifetime reproductive output,
seed/offspring production per introduced genotype,
or another architecture-comparable Malthusian proxy.
```

The same fitness definition should be used when constructing the upstream `L,s,K` receipts and when evaluating temporal invasion whenever possible.

---

## 10. Claim ceiling

A temporal PAYOFF experiment can support statements such as

> Seasonal changes in the ecology-derived architecture margins predicted a nonzero Floquet premium and an intermediate migration range in which the differentiated architecture could invade despite a negative time-averaged margin.

It does not by itself establish

```text
historical origin of modularity,
universal benefits of temporal heterogeneity,
or a general law that dispersal favors differentiation.
```

The decisive test remains the cross-scale prediction:

```text
seasonal L,s,K,eta
        |
        v
seasonal r_jl
        |
        v
frozen Floquet/migration prediction
        |
        v
independent observed rare-architecture dynamics.
```
