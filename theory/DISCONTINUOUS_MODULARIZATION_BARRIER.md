# Discontinuous modularization barrier — global release can pay before small release can invade

The edgewise model reveals a distinction analogous to PAYOFF's static-versus-invasion distinction, but now inside architecture construction itself.

Even before population frequency dependence is introduced, a fully decoupled architecture can have higher net payoff while every sufficiently small decoupling step is locally selected against.

The mechanism is convex recovery from edge release.

---

## 1. One-edge setup

Take one coupling edge with reference strength

```text
c0>0.
```

Let

```text
d in [0,c0]
```

be decoupling amount, so current coupling is

```text
c=c0-d.
```

Let recovery relative to the reference architecture be

```text
R(d)
=D*(c0)-D*(c0-d).
```

Then

```text
R(0)=0
```

and, from `EDGEWISE_MODULARIZATION.md`,

```text
R'(d)
=(x_i*(d)-x_j*(d))^2
>=0,
```

with

```text
R''(d)>=0.
```

Thus `R` is convex.

Assume linear architecture cost

```text
K(d)=k d,
```

where `k>=0` is cost per unit decoupling.

Net gain is

```text
Phi(d)=R(d)-kd.
```

---

## Theorem DMB1 — local and global decoupling thresholds are different

Define

```text
k_local
=R'(0),
```

and

```text
k_global
=R(c0)/c0.
```

Then

```text
k_global>=k_local.
```

### Proof

For any differentiable convex function with `R(0)=0`, the secant slope from zero to `c0` is at least the right derivative at zero:

```text
[R(c0)-R(0)]/c0 >= R'(0).
```

QED.

---

## Theorem DMB2 — exact three-regime accessibility classification

### Regime A — locally accessible release

If

```text
k<k_local,
```

then

```text
Phi'(0)>0.
```

Small decoupling mutations are favored.

Since `k_global>=k_local`, one also has

```text
R(c0)-kc0>0,
```

so full release is globally higher payoff than the reference architecture.

### Regime B — finite-jump modularization barrier

If

```text
k_local<k<k_global,
```

then

```text
Phi'(0)<0
```

but

```text
Phi(c0)>Phi(0)=0.
```

Thus infinitesimal decoupling is selected against even though the fully released endpoint has higher net payoff.

### Regime C — retained coupling

If

```text
k>k_global,
```

then

```text
Phi(c0)<0.
```

Because `k_global>=k_local`, one also has `Phi'(0)<0`. The reference coupling is favored both locally and against the fully released endpoint.

Boundary equalities give neutral local or endpoint comparisons.

---

## Interpretation

The barrier region

```text
k_local<k<k_global
```

is a genuine accessibility-versus-payoff mismatch:

```text
large architecture change would pay
but
small architecture change cannot start moving in that direction.
```

This is distinct from:

```text
frequency-dependent coordination,
finite-population stochastic barriers,
switching-cost hysteresis,
or developmental mutation limitation.
```

It is generated purely by the increasing-returns geometry of optimized conflict recovery.

A biological transition across this region would require a sufficiently large architectural mutation, correlated multi-edge change, drift, recombination, developmental reorganization, or another process capable of crossing the local loss valley.

---

## 2. Exact two-function quadratic thresholds

For the original two-function residual-coupling model,

```text
D_c(x,y)
=a(x-theta1)^2
+b(y-theta2)^2
+c(x-y)^2.
```

Let

```text
Delta=theta1-theta2,
Q0=ab+c0(a+b).
```

The realized separation fraction at the reference coupling is

```text
s0=ab/Q0.
```

The optimized trait difference is

```text
x*-y*=s0 Delta.
```

Therefore the local marginal decoupling threshold is

```text
k_local
=(x*-y*)^2
=s0^2 Delta^2.
```

The optimized loss at reference coupling is

```text
D_c0*
=ab c0 Delta^2/Q0.
```

Full release to `c=0` has zero pre-cost loss, so

```text
R(c0)=D_c0*.
```

Hence

```text
k_global
=R(c0)/c0
=ab Delta^2/Q0
=s0 Delta^2.
```

---

## Theorem DMB3 — exact jump-barrier width in the two-function model

For nonzero conflict and finite positive reference coupling,

```text
0<s0<1.
```

The thresholds are

```text
k_local=s0^2 Delta^2,
k_global=s0 Delta^2.
```

Therefore

```text
k_global/k_local
=1/s0>1
```

and the finite-jump barrier width is

```text
W_k
=k_global-k_local
=s0(1-s0)Delta^2.
```

### Consequences

The width is zero at the release extremes:

```text
s0->0
or
s0->1.
```

For fixed optimum separation `Delta`, it is maximal at

```text
s0=1/2,
```

with

```text
W_k,max=Delta^2/4.
```

Thus the largest accessibility gap occurs at intermediate residual integration.

---

## Corollary DMB3.1 — static architecture advantage does not imply local evolvability

Full release is statically favored whenever

```text
k<k_global.
```

But small decoupling can invade only when

```text
k<k_local.
```

Since

```text
k_local<k_global
```

for every finite partially coupled reference architecture with active conflict,

```text
static release advantage
!=
local accessibility of release.
```

This is the architecture-construction analogue of PAYOFF's broader rule that static architecture quality is not the same estimand as rare population invasion.

---

## 3. Multi-edge implication

With many edges and additive linear decoupling costs, net recovery is convex over the decoupling box. Consequently:

```text
small one-edge changes can all be locally unfavorable
```

while

```text
a coordinated multi-edge vertex topology can still have the largest global payoff.
```

The nonadditive coupling among edge pressures means the relevant finite jump may involve a set of edges rather than one edge.

This creates a direct mathematical rationale for comparing:

```text
single-edge mutant accessibility
versus
multi-edge topology payoff.
```

---

# Experimental receipt

For a candidate edge `e`, estimate or reconstruct at the current architecture:

```text
z_e^2=(x_i*-x_j*)^2.
```

This predicts

```text
k_local=z_e^2.
```

Independently compare the current and fully released edge architectures on the same fitness scale to estimate

```text
k_global=R_full/c0.
```

Then test whether the biological system lies in:

```text
accessible release,
finite-jump barrier,
or retained coupling.
```

---

# Prior-art / claim boundary

Convex value-function geometry, secant-versus-tangent inequalities, and discontinuous transitions in optimization are standard mathematics. Evolutionary accessibility barriers are also not new in general.

PAYOFF's specific claim is:

> In the registered quadratic coupling model, optimized recovery from edge decoupling is convex, so the marginal cost ceiling for an infinitesimal release is below the average cost ceiling for complete release; in the two-function case these thresholds are exactly `s0^2 Delta^2` and `s0 Delta^2`.

Do not interpret this as a universal proof that biological modularity must evolve by saltational mutations.
