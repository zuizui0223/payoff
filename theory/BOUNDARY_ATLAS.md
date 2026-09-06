# PAYOFF boundary atlas

PAYOFF now contains several mathematically distinct transition surfaces. They answer different biological questions and must not be reported as interchangeable thresholds.

The upstream architecture bridge is

```text
R=sL,
phi=R-K=sL-K.
```

`phi` is the optimized frequency-independent differentiated-minus-shared architecture gap on the common fitness scale.

---

## 1. Static architecture boundary

Question:

> Which optimized architecture has higher frequency-independent fitness?

Boundary:

```text
phi=0
<=>
K=sL.
```

Ownership:

```text
SCH -> L
BITA -> s or R
BALANCE -> static middle-world comparison
PAYOFF -> carries the gap forward.
```

---

## 2. Well-mixed deterministic invasion boundaries

Question:

> Can a rare architecture increase in a resident population?

With

```text
Delta(p)=phi+eta(2p-1),
```

rare-D neutrality is

```text
phi=eta
```

and rare-S neutrality is

```text
phi=-eta.
```

Equivalently on the cost axis,

```text
K=R-eta,
K=R+eta.
```

The region between them is stable coexistence for `eta<0` and coordination bistability for `eta>0`.

---

## 3. Weak-selection finite-population fixation boundaries

Question:

> Is a single architecture mutant more likely to fix than a neutral mutant?

Under the declared exponential-fitness Moran model and weak selection:

```text
rho_D>1/N iff 3phi>eta,
rho_S>1/N iff -3phi>eta.
```

Neutral fixation boundaries are

```text
phi=eta/3,
phi=-eta/3.
```

or

```text
K=R-eta/3,
K=R+eta/3.
```

These are not the deterministic invasion boundaries.

---

## 4. Reciprocal fixation-order boundary

Question:

> Which single architecture mutant has the larger fixation probability?

For the declared finite exponential Moran process,

```text
rho_D/rho_S
= exp[beta phi(N-2)].
```

Therefore

```text
rho_D=rho_S
iff
phi=0.
```

The static boundary survives here as a reciprocal stochastic ordering boundary even though the absolute fixation probabilities depend on `eta`.

---

## 5. Rare-mutation stationary occupancy boundary

Question:

> Which monomorphic architecture occupies more long-run time when mutation repeatedly reintroduces both states?

In the rare-mutation limit,

```text
log(Pi_N/Pi_0)
= log(u_SD/u_DS)+beta phi(N-2).
```

Equal all-D/all-S occupancy occurs at

```text
phi_occ
= -log(u_SD/u_DS)/[beta(N-2)].
```

or

```text
K_occ
= R + log(u_SD/u_DS)/[beta(N-2)].
```

Symmetric mutation restores `phi_occ=0`.

---

## 6. Regular-graph weak-selection boundaries

Question:

> How does local graph competition alter the frequency-dependent middle region?

Under the declared Ohtsuki-Nowak regular-graph pair approximation,

```text
phi_k=k phi/(k-2),
eta_k=eta.
```

The graph middle region satisfies

```text
|phi|<|eta|(k-2)/k.
```

Thus its boundaries are

```text
phi=+-|eta|(k-2)/k
```

and the cost interval is centered at the same static crossing

```text
K=R
```

with width

```text
2|eta|(k-2)/k.
```

This is a weak-selection large-regular-graph approximation, not the patch-migration model below.

---

## 7. Homogeneous-patch migration thresholds

Question:

> Can migration synchronize or destroy a spatial architecture mosaic when every patch has the same local game?

For a synchronous equilibrium `p*`, graph mode `k` has rate

```text
r_k=f'(p*)-m lambda_k.
```

The transverse synchronization threshold is

```text
m_sync=f'(p*)/lambda_2
```

when `f'(p*)>0`.

For the exact symmetric two-patch coordination special case at `phi=0`:

```text
m=eta/6
```

is the polarized-state stability boundary, while

```text
m=eta/4
```

is the polarized-branch existence boundary.

These migration thresholds are not architecture-cost boundaries.

---

## 8. Heterogeneous environment-mosaic invasion boundary

Question:

> Can a rare architecture grow across patches with different local architecture payoffs?

Patch-specific quantities are

```text
phi_j=s_jL_j-K_j.
```

Rare-D local margins are

```text
r_j^D=phi_j-eta_j,
```

and rare-S local margins are

```text
r_j^S=-phi_j-eta_j.
```

The spatial invasion boundaries are spectral:

```text
lambda_max[diag(r^D)-mL_G]=0
```

and

```text
lambda_max[diag(r^S)-mL_G]=0.
```

In general there is no single scalar `phi` threshold that replaces these eigenvalue conditions.

### Two-patch source-sink special case

For margins

```text
r_1>0>r_2,
r_1+r_2<0,
```

the exact critical migration rate is

```text
m_c=r_1r_2/(r_1+r_2).
```

At `eta=0`, this means a local BITA source patch can rescue differentiated architecture in a landscape with negative average static `phi`, but only below `m_c`.

---

## 9. The hierarchy of questions

The boundaries correspond to increasingly population-dependent estimands:

```text
phi=0
    static architecture quality
        |
        v
phi=+-eta
    deterministic rare invasion
        |
        v
phi=+-eta/3
    weak-selection single-mutant fixation advantage
        |
        v
mutation-shifted phi_occ
    long-run monomorphic occupancy
        |
        v
principal-eigenvalue boundary
    heterogeneous spatial invasion.
```

Graph and migration models add separate transformations around this chain.

The central rule is:

```text
same biological architectures
!=
same mathematical boundary.
```

Each threshold must be named by the estimand it answers.
