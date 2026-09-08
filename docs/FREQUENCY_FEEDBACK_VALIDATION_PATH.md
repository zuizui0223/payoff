# PAYOFF frequency-feedback validation path

Status: canonical measurement and falsification path for the PAYOFF frequency-feedback layer.

This document consolidates the results added after the static architecture bridge. It is a measurement-design path, not an empirical claim that any biological system already satisfies the full PAYOFF game.

## 1. Start from reciprocal invasion, not from static architecture quantities

For the canonical pairwise gap

```text
Delta(p)=phi+eta(2p-1),
```

define the two rare-invasion margins

```text
u = Delta(0)      # rare D in an S resident population
v = -Delta(1)     # rare S in a D resident population.
```

Then

```text
u = phi-eta,
v = -phi-eta.
```

The strict phase is identified from the signs alone:

```text
u>0, v>0   -> stable coexistence
u<0, v<0   -> coordination bistability
u>0, v<0   -> D dominance
u<0, v>0   -> S dominance.
```

This phase classification survives unknown positive assay-specific scale factors because only signs are used.

If the two margins are on one common positive payoff/fitness scale, then

```text
phi=(u-v)/2,
eta=-(u+v)/2.
```

Thus numerical identification of `phi` and `eta` is stronger than phase identification and has a stronger scale requirement.

## 2. Interior frequencies are independent holdouts, not refit points

Once endpoint margins are frozen, the canonical affine model predicts every interior frequency without further fitting:

```text
Delta_hat(p)=(1-p)u-pv.
```

Interior observations must therefore be used as holdouts. Re-estimating `phi` or `eta` using the same holdouts would destroy the falsification role.

With endpoint intervals

```text
u in [uL,uH],
v in [vL,vH],
```

the exact predicted interval is

```text
[(1-p)uL-pvH,
 (1-p)uH-pvL].
```

A measured interior interval that is disjoint from this prediction rejects the declared affine PAYOFF frequency law. Closed-band contact is compatible and is not rejection.

Passing all declared holdouts means only that the affine law remains compatible at those frequencies. It does not prove that all nonlinear alternatives are absent.

## 3. Where should the holdouts be placed?

### Zero-error or pure covering problem

For an `L`-Lipschitz residual

```text
r(p)=Delta_true(p)-Delta_PAYOFF(p),
r(0)=r(1)=0,
```

the minimax `m`-point zero-error placement is

```text
p_i=i/(m+1).
```

Examples:

```text
m=1 -> 1/2
m=2 -> 1/3,2/3
m=3 -> 1/4,1/2,3/4.
```

For a signed-curvature alternative with `|r''|>=kappa` and fixed curvature sign, the single most sensitive point is exactly `p=1/2`, where the guaranteed departure is `kappa/8`.

## 4. Bounded measurement error changes the minimax design

Let reported centres have deterministic half-width errors

```text
endpoint u: e_u
endpoint v: e_v
interior:   e_h.
```

At frequency `p`, a true nonlinear residual is guaranteed to force rejection only if

```text
|r(p)| > 2[e_h+(1-p)e_u+p e_v].
```

The factor two is exact for the declared centre-error plus closed-band comparison model. Equality is excluded because bands may touch.

For arbitrary declared holdouts with nondetection thresholds `b_i`, the exact largest `L`-Lipschitz residual amplitude that can still evade guaranteed rejection is

```text
U = max_p min_j [b_j+L|p-p_j|],
```

with `(0,0)` and `(1,0)` included as endpoint anchors.

Any alternative with

```text
||r||_infinity > U
```

must reject at least one holdout. The bound is sharp under the declared deterministic-error class.

## 5. Equal endpoint precision: closed-form noisy design

If

```text
e_u=e_v=e_E,
B=2(e_E+e_h),
```

and `B<L/2`, the unique minimax design is

```text
p_i=[iL+(m+1-2i)B]/[(m+1)L]
```

with exact minimax ceiling

```text
U_m=B+(L/2-B)/(m+1).
```

Nonzero error therefore pulls the optimal points inward relative to equal spacing.

If

```text
B>=L/2,
```

no finite interior design improves the endpoint-only ceiling `L/2`.

## 6. Unequal reciprocal endpoint precision

Define

```text
B=2e_h+e_u+e_v,
delta=2|e_v-e_u|,
q=(L-delta)/(L+delta).
```

In the informative regime `B<L/2`, automatically `delta<L`, and the unique minimax design has

```text
U_m = L [B(1-q^m)+(delta/2)(1+q^m)]
      /[(L+delta)(1-q^(m+1))].
```

Swapping `e_u` and `e_v` reflects the optimal frequencies through `p=1/2` but leaves `U_m` unchanged.

Consequences:

```text
m=1: p=1/2 regardless of endpoint asymmetry;
m>=2: the design centroid shifts toward the noisier endpoint.
```

The dense-design deterministic floor is

```text
U_inf = 2L[e_h+max(e_u,e_v)]/[L+2|e_v-e_u|].
```

Thus adding more frequency settings cannot beat the declared precision floor.

## 7. Precision allocation across reciprocal invasion assays

Hold the total endpoint error

```text
S=e_u+e_v
```

fixed.

In the informative regime:

```text
m=1   -> minimax performance is invariant to endpoint imbalance;
m>=2  -> U_m is strictly minimized by e_u=e_v=S/2.
```

The dense-design error floor is also uniquely minimized by balanced achieved endpoint precision.

This is a statement about achieved deterministic error half-widths. It does not imply equal biological replicate numbers when the two assays have different variance or cost functions.

## 8. Two exact ex-ante inversions

### A. Fixed precision -> minimum number of distinct frequency settings

For asymmetric endpoint precision and target nonlinear amplitude `A`, let

```text
U_inf = L(B+delta/2)/(L+delta).
```

If

```text
U_inf < A <= L/2,
```

then

```text
q^m < T(A)
```

is exactly equivalent to guaranteed detection, where

```text
T(A)= [A(L+delta)-L(B+delta/2)]
      /[A(L-delta)+L(delta/2-B)].
```

The minimum count is

```text
min {m>=1 : q^m<T(A)}.
```

Exact equality `q^m=T(A)` is insufficient and requires one additional setting.

### B. Fixed count -> maximum admissible common interior error

For fixed `m`, endpoint errors and target `A`, solve the same minimax law for `B=2e_h+e_u+e_v`.

For `delta>0`, the excluded boundary is

```text
B_crit = [A(L+delta)(1-q^(m+1))/L
          -(delta/2)(1+q^m)]
         /(1-q^m),
```

so guaranteed detection requires

```text
e_h < [B_crit-(e_u+e_v)]/2.
```

For `delta=0`,

```text
B_crit=[(m+1)A-L/2]/m.
```

Again, the boundary itself is excluded.

## 9. What this path establishes and what it does not

This path establishes exact deterministic measurement-design results under the declared affine PAYOFF model, Lipschitz/curvature alternative classes, and bounded-error semantics.

It does not establish:

```text
that a biological S/D architecture pair has frequency-dependent fitness;
that eta is nonzero in any empirical system;
that the affine Delta(p) law passes real interior-frequency holdouts;
statistical power or biological replicate counts;
finite-population fixation in an empirical system;
recurrent-mutation occupancy in an empirical system;
historical causation of architecture evolution.
```

The empirical sequence should therefore be

```text
static architecture bridge
-> reciprocal frequency evidence
-> common-scale phi/eta identification when possible
-> frozen interior-frequency holdouts
-> only then finite-population / recurrent-mutation tests.
```

## 10. Canonical implementation map

```text
src/reciprocal_invasion_identification.py
src/frequency_response_holdout.py
src/frequency_holdout_design.py
src/frequency_holdout_detection.py
src/asymmetric_frequency_holdout_detection.py
src/asymmetric_holdout_count.py
src/endpoint_precision_allocation.py
src/interior_precision_frontier.py
```

Key theory documents:

```text
theory/OPTIMAL_FREQUENCY_HOLDOUT_PLACEMENT.md
theory/FINITE_PANEL_PRECISION_LIMIT.md
theory/ASYMMETRIC_ENDPOINT_PRECISION_HOLDOUT_DESIGN.md
theory/ASYMMETRIC_HOLDOUT_COUNT_INVERSION.md
theory/BALANCED_ENDPOINT_PRECISION_ALLOCATION.md
theory/INTERIOR_PRECISION_FRONTIER.md
```

The claim ceiling remains mathematical/measurement-design infrastructure until empirical architecture-frequency evidence is supplied.
