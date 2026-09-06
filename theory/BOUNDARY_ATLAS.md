# PAYOFF boundary atlas

PAYOFF contains several mathematically distinct transition surfaces. They answer different biological questions and must not be reported as interchangeable thresholds.

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

## 9. Common temporal forcing boundary

Question:

> Does a time-varying environment alter invasion if every patch receives the same additive shift?

For

```text
A(t)=A0+q(t)I,
```

the temporal invasion exponent is exactly

```text
Lambda_temporal
= lambda_max(A0)+mean(q).
```

Neutrality is therefore

```text
lambda_max(A0)+mean(q)=0.
```

Zero-mean common fluctuations do not create a new boundary: they leave the baseline spectral invasion condition unchanged.

---

## 10. Two-season Floquet invasion boundary

Question:

> Can periodic switching of relative patch quality change rare-architecture invasion relative to the time-averaged landscape?

For exactly two seasons in the symmetric two-patch model, the exact periodic invasion boundary is

```text
Lambda_F=0,
```

where `Lambda_F` is given by the scalar closed form in

```text
theory/TWO_SEASON_TEMPORAL_PREMIUM.md.
```

Let

```text
Lambda_avg
= lambda_max(A_bar)
```

for the time-averaged operator. In this registered model,

```text
Lambda_F>=Lambda_avg.
```

Thus a temporal-rescue region exists whenever

```text
Lambda_avg<0<Lambda_F.
```

The temporal-structure gate is the commutator condition

```text
m[(r_1,1-r_2,1)-(r_1,2-r_2,2)] != 0.
```

At the commuting gates the periodic and averaged boundaries coincide.

Under rapid switching, the boundary displacement begins at order `T^2`, with temporal premium proportional to

```text
m^2 * (seasonal patch-contrast change)^2.
```

---

## 11. Anti-phase temporal coordination boundaries

Question:

> Can seasonal source switching overcome a positive-frequency coordination barrier between shared and differentiated architectures?

For the symmetric anti-phase special case, both reciprocal invasion problems receive the same temporal premium

```text
P=P(m,x,tau).
```

Their exact edge exponents are

```text
Lambda_D
= phi_bar-eta+P,

Lambda_S
= -phi_bar-eta+P.
```

Therefore the two temporal reciprocal-neutral boundaries are

```text
phi_bar
= +(eta-P)
```

and

```text
phi_bar
= -(eta-P).
```

Equivalently define

```text
eta_eff=eta-P.
```

The central static point remains

```text
phi_bar=0,
```

but the biological type of the middle region depends on the sign of `eta_eff`.

### Coordination side

```text
P<eta
-> eta_eff>0
-> central mutual non-invasion.
```

### Temporal inversion surface

```text
P=eta
-> eta_eff=0
-> reciprocal boundaries collapse at phi_bar=0.
```

### Reciprocal-invasion side

```text
P>eta
-> eta_eff<0
-> central reciprocal invasion.
```

For nonzero `phi_bar`, both architectures invade iff

```text
P>eta+|phi_bar|.
```

Neither invades iff

```text
P<eta-|phi_bar|.
```

Between those conditions, only the statically favored architecture invades.

---

## 12. Weak-contrast temporal inversion boundary

Question:

> At weak seasonal contrast, is temporal source switching strong enough to invert coordination for any migration rate?

For

```text
|x|tau << 1,
```

the temporal premium is

```text
P
~= x^2 tau H(m tau),
```

where

```text
H(u)=[u-tanh u]/(2u^2).
```

`H` has one maximum

```text
H*=0.132487539446827...
```

at

```text
u*=m tau
=1.60611529880277....
```

At `phi_bar=0`, a temporal reciprocal-invasion island exists approximately iff

```text
x^2 tau/eta
> 1/H*
=7.547879628343014....
```

At equality the two migration boundaries merge at `u*`. Above threshold there are two positive migration crossings and the reciprocal-invasion state lies between them.

This is an asymptotic anti-phase boundary, not a universal migration threshold.

---

## 13. The hierarchy of questions

The boundaries correspond to increasingly population- and context-dependent estimands:

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
    heterogeneous spatial invasion
        |
        v
Lambda_F=0
    periodic spatiotemporal invasion
        |
        v
P=eta (+/- phi_bar adjustment)
    temporal inversion of reciprocal architecture coordination.
```

Graph, migration, mutation, and temporal models add separate transformations around this chain.

The central rule is:

```text
same biological architectures
!=
same mathematical boundary.
```

Each threshold must be named by the estimand it answers.
