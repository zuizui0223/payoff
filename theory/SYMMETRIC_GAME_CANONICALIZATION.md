# Symmetric architecture games have canonical PAYOFF coordinates

PAYOFF began with the symmetric two-architecture matrix

```text
          S          D
S         0       phi-eta
D      phi-eta      2phi.
```

That form is more general than it first appears.

Every symmetric two-strategy game is equivalent, up to a common additive payoff shift, to exactly one pair of PAYOFF coordinates `(phi,eta)`.

This is standard two-strategy game algebra; the useful PAYOFF contribution is the architecture interpretation of those coordinates and the ability to transport them into the already developed invasion/fixation machinery.

---

## 1. Arbitrary symmetric pair

Take any symmetric payoff matrix

```text
          S      T
S         a      b
T         b      d.
```

Subtract the common constant `a` from every entry:

```text
          S        T
S         0      b-a
T       b-a      d-a.
```

Define

```text
phi
=(d-a)/2,

eta
=(a+d-2b)/2.
```

Then

```text
b-a=phi-eta
```

and

```text
d-a=2phi.
```

Therefore the shifted matrix is exactly

```text
          S          T
S         0       phi-eta
T      phi-eta      2phi.
```

---

## Theorem SGC1 — unique canonical PAYOFF coordinates for a symmetric pair

Every real symmetric 2x2 game has the unique canonical coordinates

```text
phi=(d-a)/2,
eta=(a+d-2b)/2
```

modulo a common additive payoff shift.

### Proof

The canonical shifted matrix requires

```text
2phi=d-a
```

and

```text
phi-eta=b-a.
```

These equations have the unique solution above. QED.

---

## Theorem SGC2 — canonical frequency gap

Let `p` be frequency of `T`. Then

```text
pi_T-pi_S
=phi+eta(2p-1).
```

Thus the entire deterministic PAYOFF phase classification applies to every symmetric pair once `(phi,eta)` are computed from its matrix.

### Endpoint meanings

```text
Delta(0)=phi-eta=b-a
```

is rare-T advantage in resident S.

```text
Delta(1)=phi+eta=d-b
```

is T advantage when resident T.

Their midpoint and half-difference recover

```text
phi=[Delta(0)+Delta(1)]/2,
eta=[Delta(1)-Delta(0)]/2.
```

---

## 2. Interpretation of the two canonical coordinates

### `phi`: endpoint-centered architecture advantage

```text
phi=(d-a)/2.
```

It compares the two like-with-like endpoint payoffs.

### `eta`: interaction curvature

```text
eta=(a+d-2b)/2.
```

It compares average like-with-like payoff against unlike-pair payoff.

Hence:

```text
eta>0
-> unlike pairs underperform the average of like pairs
-> coordination / positive-frequency tendency;

eta<0
-> unlike pairs outperform the average of like pairs
-> coexistence / negative-frequency tendency.
```

This provides an interpretation of `eta` that does not require a Hamming-distance model.

---

## 3. Architecture payoff decomposition

In `MULTI_ARCHITECTURE_GAME.md`, candidate architectures have

```text
A_ij=b_i+b_j+H_ij,
```

where `b_i` is intrinsic optimized architecture payoff and `H` is symmetric ecological feedback.

For a pair `S,T`:

```text
A_SS=2b_S+H_SS,
A_ST=b_S+b_T+H_ST,
A_TT=2b_T+H_TT.
```

Canonicalization gives

```text
phi_ST
=
b_T-b_S
+(H_TT-H_SS)/2,
```

and

```text
eta_ST
=
(H_SS+H_TT-2H_ST)/2.
```

---

## Corollary SGC3.1 — equal same-type feedback preserves the intrinsic gap

If

```text
H_SS=H_TT,
```

then

```text
phi_ST=b_T-b_S.
```

Frequency interaction modifies `eta` but does not shift the endpoint-centered architecture gap.

---

## Corollary SGC3.2 — zero-diagonal distance kernels give the topology mapping

For

```text
H_SS=H_TT=0,
H_ST=-gamma q_ST,
```

one obtains

```text
phi_ST=b_T-b_S,
eta_ST=gamma q_ST.
```

Thus `TOPOLOGY_PAYOFF_GAME.md` is a special case of the general symmetric-pair canonicalization.

---

## Corollary SGC3.3 — self-environment asymmetry shifts phi

If architecture types receive different same-type ecological feedback,

```text
H_TT != H_SS,
```

then the population-level canonical `phi_ST` is not identical to the pre-interaction intrinsic difference `b_T-b_S`.

The shift is exactly

```text
(H_TT-H_SS)/2.
```

This supplies a clear claim boundary:

```text
intrinsic architecture gap
and
canonical population-game phi
coincide only under equal diagonal feedback.
```

---

## 4. Finite-population transport

Once any symmetric architecture pair is canonicalized, the existing exponential Moran formulas apply with the resulting `(phi,eta)`.

In particular,

```text
rho_T/rho_S
=exp[beta(N-2)phi].
```

Therefore reciprocal fixation ordering depends only on the canonical endpoint-centered coordinate `phi`, while absolute fixation probabilities also depend on interaction curvature `eta`.

For the zero-diagonal topology-distance model this reduces to dependence on `b_T-b_S` alone.

---

## 5. Why this matters for the many-architecture programme

For an `m`-strategy symmetric architecture game, every edge of the strategy-comparison graph has its own pairwise canonical coordinates:

```text
(S,T)
-> (phi_ST,eta_ST).
```

This creates a common local language across:

```text
continuous recovery states,
vertex coupling topologies,
modular partitions,
spatially or developmentally distinct architectures.
```

It does **not** mean that the full many-strategy dynamics can be reconstructed from independent pairwise classifications; higher-dimensional coexistence and invasion must still be checked in the full game.

---

# Claim boundary

Representing a symmetric 2x2 game by two independent payoff contrasts is elementary game theory, not a new theorem of evolutionary biology.

PAYOFF should claim only:

> The architecture interpretation of the canonical coordinates lets any symmetric pair of optimized architectures enter the same registered invasion, fixation, and threshold machinery, while explicitly separating endpoint-centered advantage `phi` from interaction curvature `eta`.
