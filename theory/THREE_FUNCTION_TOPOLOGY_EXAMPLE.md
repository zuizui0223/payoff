# Three-function topology example — conflict rerouting produces an accessible two-module optimum

This note turns the edgewise modularization theorems into one complete three-function calculation.

The goal is not to claim that every biological three-function system has this topology. The purpose is to show how upstream function-specific optima generate an **edge-by-edge modularization prediction** that can be checked without fitting the topology after the fact.

---

## 1. Reference architecture

Take three functions with equal fitness weights

```text
a_0=a_1=a_2=1
```

and preferred coordinates

```text
theta=(0,1,3).
```

Start from the fully connected triangle

```text
E={(0,1),(0,2),(1,2)}
```

with reference coupling

```text
c_e=1
```

on every edge.

The optimized phenotype solves

```text
(I+L_K3)x=theta
```

and is exactly

```text
x_full=(1,5/4,7/4).
```

The optimized reference loss is

```text
D_full*=7/2.
```

This `7/2` is the recoverable conflict budget relative to complete edge release in this example.

---

## 2. Exact initial edge-release pressures

By `EDGEWISE_MODULARIZATION.md`, the marginal recovery from weakening edge `(i,j)` is

```text
partial R/partial d_ij=(x_i*-x_j*)^2.
```

At the fully connected reference:

```text
edge (0,1): pressure = (1-5/4)^2     = 1/16
edge (0,2): pressure = (1-7/4)^2     = 9/16
edge (1,2): pressure = (5/4-7/4)^2   = 1/4.
```

Thus the initial release ranking is

```text
(0,2) > (1,2) > (0,1).
```

Now assign one common linear cost per unit of edge release:

```text
k=2/5=0.4.
```

The initial marginal net-release receipts are

```text
(0,1): 1/16-2/5 = -27/80
(0,2): 9/16-2/5 =  13/80
(1,2): 1/4 -2/5 =  -3/20.
```

Therefore only edge

```text
(0,2)
```

is locally selected to weaken from the reference architecture.

Because recovery is convex along an edge and cost is linear, a positive current marginal receipt implies that full release of that edge improves net architecture payoff relative to the current state.

---

## 3. First release reroutes conflict

Fully release edge `(0,2)` while retaining `(0,1)` and `(1,2)`.

The new optimized phenotype is

```text
x=(5/8,5/4,17/8).
```

Its optimized loss is

```text
D*=19/8,
```

so recovery relative to the fully connected reference is

```text
R_02
=7/2-19/8
=9/8.
```

The architecture cost is

```text
2/5,
```

and the net gain is

```text
Phi_02
=9/8-2/5
=29/40
=0.725.
```

But the key result is not just the gain. Re-optimizing the phenotype changes the strain on the surviving edges:

```text
pressure_01=(5/8-5/4)^2   =25/64
pressure_12=(5/4-17/8)^2  =49/64.
```

Against cost `2/5`:

```text
25/64-2/5 = -3/320,
49/64-2/5 =117/320.
```

Thus edge `(1,2)`, which was initially selected **against** release,

```text
1/4 < 2/5,
```

becomes strongly selected **for** release after `(0,2)` is removed:

```text
49/64 > 2/5.
```

This is an exact conflict-rerouting effect.

---

## 4. Second release creates the predicted module partition

Release `(1,2)` next.

Only edge `(0,1)` remains coupled. The optimized phenotype becomes

```text
x=(1/3,2/3,3).
```

The optimized loss is

```text
D*=1/3.
```

Hence total recovery is

```text
R_02,12
=7/2-1/3
=19/6.
```

Two released edges cost

```text
4/5,
```

so

```text
Phi_02,12
=19/6-4/5
=71/30
~=2.3666667.
```

The remaining edge pressure is

```text
pressure_01=(1/3-2/3)^2=1/9<2/5.
```

Therefore the sequential local-release rule stops at

```text
retained edge: (0,1)
released edges: (0,2),(1,2)
```

which is the two-module architecture

```text
{0,1} | {2}.
```

---

## 5. This local path reaches the global vertex optimum

All `2^3=8` retain/release topologies can be enumerated exactly.

| Released edges | Recovery `R` | Release cost | Net gain `Phi` |
|---|---:|---:|---:|
| none | `0` | `0` | `0` |
| `(0,1)` | `1/8` | `2/5` | `-11/40` |
| `(0,2)` | `9/8` | `2/5` | `29/40` |
| `(1,2)` | `1/2` | `2/5` | `1/10` |
| `(0,1),(0,2)` | `13/6` | `4/5` | `41/30` |
| `(0,1),(1,2)` | `1/2` | `4/5` | `-3/10` |
| `(0,2),(1,2)` | `19/6` | `4/5` | **`71/30`** |
| all three | `7/2` | `6/5` | `23/10` |

Thus

```text
{0,1}|{2}
```

is not only a local stopping point. It is the unique maximum-net-gain vertex architecture in this example.

Full differentiation recovers an additional

```text
7/2-19/6=1/3
```

but requires paying one more edge-release cost

```text
2/5.
```

Since

```text
1/3<2/5,
```

the last within-module edge should remain coupled.

The net advantage of the two-module architecture over full release is

```text
71/30-23/10
=1/15.
```

---

## 6. Recovery is strongly nonadditive across edges

Single-edge recoveries are

```text
R_02=9/8,
R_12=1/2.
```

If edge benefits were additive, releasing both would recover

```text
9/8+1/2=13/8.
```

Instead the exact joint recovery is

```text
R_02,12=19/6.
```

The interaction/synergy receipt is therefore

```text
R_02,12-R_02-R_12
=19/6-9/8-1/2
=37/24
~=1.54167.
```

This large positive nonadditivity is the mechanistic reason independent initial edge ranking is insufficient.

Releasing `(0,2)` changes the optimized phenotype, which reallocates conflict onto `(1,2)` and makes the second release much more valuable.

---

## 7. The exact accessible path

With the declared common release cost `k=0.4`, the pressure-driven path is

```text
complete triangle
{01,02,12}
    |
    | only pressure_02 > k
    v
release 02
{01,12}
    |
    | pressure_12 rises from 1/4 to 49/64 > k
    v
release 12
{01}
    |
    | pressure_01=1/9 < k
    v
stop

module partition = {0,1}|{2}.
```

So this example predicts not only the final topology but also the order of accessible edge changes.

---

## 8. Biological interpretation

The example has three useful messages.

### 8.1 The widest functional disagreement is the first release target here

At the fully symmetric triangle, the optimized edge pressures inherit the ordering of function-specific optimum separation, so `(0,2)` is the first target.

This ordering is specific to the declared symmetric reference architecture. It is not a general theorem that the largest raw optimum difference always releases first.

### 8.2 Modularity can emerge by conflict rerouting

The second edge release is not profitable in the original architecture. It becomes profitable only after the first release changes the optimized phenotype.

Thus modularization can be a sequential endogenous cascade rather than a set of independent edge decisions.

### 8.3 Full differentiation need not be optimal

The final retained `(0,1)` edge defines a functional module because its remaining conflict recovery is smaller than the cost of breaking that connection.

This is the graph-level analogue of BALANCE:

```text
conflict remains inside a module,
but eliminating the last coupling is not worth its architecture cost.
```

---

## 9. Empirical handoff

A real three-function application would replace the toy optima and equal couplings by independently estimated quantities:

```text
function-specific optima theta_i,
fitness curvatures a_i,
reference coupling strengths c_e,
edge-specific release costs k_e.
```

Then the prospective pipeline is

```text
1. optimize the reference phenotype;
2. compute edge pressures (x_i*-x_j*)^2;
3. predict the first release candidate;
4. experimentally weaken/remove that edge;
5. re-estimate the optimized phenotype;
6. predict the next edge;
7. compare the observed module partition with the frozen topology prediction.
```

The point is to predict the sequence from upstream conflict geometry, not to infer the edge sequence from the final observed modules.

---

## 10. Claim boundary

This is an exact worked example under a quadratic trait-loss model, unit reference couplings, and linear release cost.

It does not establish that real modularity universally evolves by this exact sequence. Its value is that the PAYOFF framework now produces a falsifiable graph-topology prediction from function-level optima and costs.
