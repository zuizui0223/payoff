# Weak-selection PAYOFF on regular graphs

This note connects the PAYOFF architecture game to the established Ohtsuki-Nowak pair-approximation replicator equation on large regular graphs.

It is intentionally a **prior-theory substitution result**, not a claim to invent evolutionary graph theory.

## 1. Starting PAYOFF matrix

Rows and columns are ordered `(S,D)`:

```text
          S          D
S         0       phi-eta
D      phi-eta      2phi.
```

Write

```text
q=phi-eta.
```

Then

```text
A=[[0,q],[q,2phi]].
```

The well-mixed payoff gap at differentiated frequency `p` is

```text
Delta(p)=phi+eta(2p-1).
```

---

## 2. Established regular-graph transform

For a large degree-`k` regular graph (`k>=3`) under weak selection, the Ohtsuki-Nowak pair approximation transforms a two-strategy matrix

```text
[[a11,a12],
 [a21,a22]]
```

into

```text
[[a11,   a12+H],
 [a21-H, a22  ]].
```

The correction `H` depends on update rule.

For birth-death / pairwise-comparison updating,

```text
H_BD
= (a11+a12-a21-a22)/(k-2).
```

For death-birth updating,

```text
H_DB
= [(k+1)a11+a12-a21-(k+1)a22]
  /[(k+1)(k-2)].
```

For imitation updating,

```text
H_IM
= [(k+3)a11+3a12-3a21-(k+3)a22]
  /[(k+3)(k-2)].
```

These formulas are established prior theory; see Ohtsuki & Nowak (2006), *The replicator equation on graphs*, Journal of Theoretical Biology 243:86-97, DOI `10.1016/j.jtbi.2006.06.004`.

---

## Theorem 1 — all three update-rule corrections coincide for the PAYOFF matrix

For

```text
a11=0,
a12=a21=phi-eta,
a22=2phi,
```

all three formulas reduce to

```text
H
= -2phi/(k-2).
```

### Proof

For BD / pairwise comparison,

```text
H_BD
= [0+(phi-eta)-(phi-eta)-2phi]/(k-2)
= -2phi/(k-2).
```

For DB, the off-diagonal terms cancel and

```text
H_DB
= -2phi(k+1)/[(k+1)(k-2)]
= -2phi/(k-2).
```

For imitation, the off-diagonal terms again cancel and

```text
H_IM
= -2phi(k+3)/[(k+3)(k-2)]
= -2phi/(k-2).
```

QED.

### Interpretation

Update-rule independence here is **not** a general property of graph evolutionary games. It is a consequence of the special PAYOFF symmetry

```text
a12=a21
```

and diagonal structure

```text
a11=0,
a22=2phi.
```

---

## Theorem 2 — the graph transform rescales `phi` but leaves `eta` unchanged

The transformed matrix is

```text
A_k
=
[[0,
  phi-eta-2phi/(k-2)],
 [phi-eta+2phi/(k-2),
  2phi]].
```

The transformed payoff gap is

```text
Delta_k(p)
= [k/(k-2)]phi + eta(2p-1).
```

Hence define

```text
phi_k = [k/(k-2)]phi,
eta_k = eta.
```

### Proof

At D frequency `p`,

```text
pi_D-pi_S
= (a21-H-a11)(1-p)
  +(a22-a12-H)p.
```

Substituting the PAYOFF entries and `H=-2phi/(k-2)` gives

```text
Delta_k(0)
= phi-eta+2phi/(k-2),

Delta_k(1)
= phi+eta+2phi/(k-2).
```

Their midpoint is

```text
phi+2phi/(k-2)
= [k/(k-2)]phi,
```

while half their difference remains `eta`. QED.

---

## Corollary 2.1 — graph structure preserves the static architecture crossing

For every finite `k>=3`,

```text
sign(phi_k)=sign(phi).
```

Therefore

```text
phi=0
```

remains the static shared-versus-differentiated sign boundary under this weak-selection regular-graph approximation.

Substituting

```text
phi=sL-K,
```

the crossing remains

```text
K=sL.
```

The graph changes the **magnitude** of the static gap relative to frequency feedback, not its sign.

---

## Corollary 2.2 — sparse regular graphs amplify the static architecture gap

The amplification factor is

```text
A_k = k/(k-2)>1.
```

It decreases monotonically toward one:

```text
k=3 -> A_k=3,
k=4 -> A_k=2,
k=6 -> A_k=1.5,
k->infinity -> A_k->1.
```

Thus the pair approximation recovers the well-mixed PAYOFF game as degree increases.

---

## Theorem 3 — the coexistence/coordination wedge shrinks on the `phi` scale

The transformed graph game has an interior equilibrium/threshold iff

```text
|phi_k|<|eta|.
```

Using Theorem 2,

```text
|phi|
< |eta|(k-2)/k.
```

Therefore the width of the graph middle region on the original `phi` scale is

```text
W_phi,graph
= 2|eta|(k-2)/k.
```

Compared with the well-mixed width

```text
W_phi,wellmixed=2|eta|,
```

regular-graph local competition shrinks this wedge by factor

```text
(k-2)/k.
```

The sign of `eta` still determines its type:

```text
eta<0 -> stable coexistence wedge,
eta>0 -> coordination wedge.
```

---

## Corollary 3.1 — graph-shifted invasion surfaces in architecture cost

Since

```text
phi=R-K,
R=sL,
```

the graph middle region is

```text
|R-K|<|eta|(k-2)/k.
```

Its two cost boundaries are

```text
K_-=R-|eta|(k-2)/k,
K_+=R+|eta|(k-2)/k.
```

The midpoint remains exactly

```text
R=sL,
```

while the width becomes

```text
W_K,graph
=2|eta|(k-2)/k.
```

Thus the graph transform leaves the upstream static architecture crossing centered at the same cost but changes how wide a frequency-dependent coexistence/coordination region surrounds it.

---

## Corollary 3.2 — graph interior equilibrium / coordination threshold

When `eta!=0` and the interior condition holds,

```text
p*_k
= 1/2[1-phi_k/eta]
= 1/2[1-k phi/((k-2)eta)].
```

At

```text
phi=0,
```

one still has

```text
p*_k=1/2
```

for every degree.

Away from the static crossing, sparse graphs move the interior equilibrium farther from `1/2` because they amplify `phi` relative to `eta`.

---

## 4. What this result does and does not mean

The result applies to the established Ohtsuki-Nowak weak-selection pair approximation on large regular graphs. It does **not** say that arbitrary spatial population structure universally rescales `phi` by `k/(k-2)`.

It does not cover, without further derivation:

```text
finite small graphs,
strong selection,
irregular degree distributions,
clustering beyond pair approximation,
directed graphs,
different interaction and replacement graphs,
mutation,
or arbitrary update rules.
```

The deterministic conservative-patch model in `SPATIAL_METAPOPULATION.md` is also a different spatial model and should not be conflated with this microscopic regular-graph approximation.

---

## 5. Prior-art and novelty boundary

Ohtsuki & Nowak already showed that regular graph structure under weak selection can be represented by a transformed payoff matrix, with update-rule-specific corrections. That is prior art (DOI `10.1016/j.jtbi.2006.06.004`).

PAYOFF contributes only the substitution and simplification for its ecology-calibrated matrix:

```text
phi=sL-K
        |
        v
PAYOFF matrix
        |
        v
Ohtsuki-Nowak graph transform
        |
        v
phi_k=k phi/(k-2)
eta_k=eta.
```

The resulting graph-degree predictions are therefore a bridge from measured compromise/architecture quantities into established graph-game machinery, not a new theory of evolutionary graphs.
