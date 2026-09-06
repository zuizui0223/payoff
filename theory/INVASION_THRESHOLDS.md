# Invasion thresholds — the static architecture boundary splits in two

The static SCH/BALANCE/BITA bridge uses

```text
phi = sL-K = WD*-WS*.
```

Without frequency dependence, `phi=0` is the single architecture crossing.

In the evolutionary game,

```text
Delta(p)=pi_D(p)-pi_S(p)=phi+eta(2p-1),
```

that one static boundary splits into two biologically distinct invasion boundaries.

---

## Theorem I1 — invasion criteria

A rare differentiated architecture `D` can invade a resident shared population `S` iff

```text
Delta(0)=phi-eta > 0,
```

or equivalently

```text
phi > eta.
```

A rare shared architecture `S` can invade a resident differentiated population `D` iff

```text
-Delta(1)=-(phi+eta) > 0,
```

or equivalently

```text
phi < -eta.
```

### Proof

When `D` is rare, `p -> 0`, and the sign of its initial growth under

```text
dp/dt=p(1-p)Delta(p)
```

is the sign of `Delta(0)`. Thus D invades iff `phi-eta>0`.

When `S` is rare, write `q=1-p`. Near `p=1`, S increases iff D decreases, which requires `Delta(1)<0`. Hence S invades iff `phi+eta<0`.

QED.

---

## Corollary I1.1 — four invasion regimes

The two inequalities produce four qualitative regimes.

### 1. D invades, S does not

```text
phi > eta
and
phi >= -eta.
```

Selection points toward differentiated architecture.

### 2. S invades, D does not

```text
phi <= eta
and
phi < -eta.
```

Selection points toward shared architecture.

### 3. Mutual invasion

```text
phi > eta
and
phi < -eta.
```

This is possible only if

```text
eta < 0.
```

Then

```text
eta < phi < -eta
```

or equivalently

```text
|phi|<|eta|.
```

This is the stable-coexistence wedge.

### 4. Mutual non-invasion

```text
phi <= eta
and
phi >= -eta.
```

This is possible only if

```text
eta > 0.
```

Then

```text
-eta <= phi <= eta.
```

This is the coordination / bistability wedge: whichever architecture is resident can resist invasion by the other.

Strict inequalities give the hyperbolic interior regimes; equalities are invasion boundaries.

---

## Theorem I2 — frequency dependence can reverse the static inference

### Negative frequency dependence can rescue D inside static BALANCE

Suppose

```text
phi < 0,
```

so the frequency-independent architecture comparison favors `S`. If

```text
eta < phi < 0
```

with `eta<0`, then

```text
phi-eta>0,
```

so rare `D` nevertheless invades the shared resident population.

If also `phi<-eta`, both strategies invade when rare and stable coexistence follows.

### Positive frequency dependence can block D inside static BITA

Suppose

```text
phi > 0,
```

so the frequency-independent comparison favors `D`. If

```text
0 < phi < eta
```

with `eta>0`, then

```text
phi-eta<0,
```

so rare `D` cannot invade a shared resident population despite its positive intrinsic architecture gap.

The shared state is protected by a coordination barrier.

### Proof

Both statements are direct substitutions into Theorem I1.

QED.

---

## Main consequence for SCH -> BALANCE -> BITA

The static boundary

```text
phi=0
```

is still the correct frequency-independent architecture comparison, but it is not generally the invasion threshold once ecological frequency dependence exists.

Instead the two invasion boundaries are

```text
D invades S:  phi= eta
S invades D:  phi=-eta.
```

Their separation is

```text
2|eta|.
```

For `eta<0`, the interval between them is a **mutual-invasion / coexistence region**.

For `eta>0`, the interval between them is a **mutual-non-invasion / bistability region**.

This is the cleanest new result created by adding the evolutionary game layer.

---

## Empirical interpretation

A direct PAYOFF experiment does not need to estimate the entire frequency-response curve first. The two edge experiments are already highly informative:

```text
Experiment A
rare D introduced into mostly-S population
-> estimate Delta(0)

Experiment B
rare S introduced into mostly-D population
-> estimate Delta(1).
```

Then

```text
phi = [Delta(0)+Delta(1)]/2
eta = [Delta(1)-Delta(0)]/2.
```

So the static architecture gap and frequency-feedback coefficient are separately identifiable from the two reciprocal invasion contrasts under the linear game.

This gives a minimal empirical design for PAYOFF:

```text
resident S + rare D
resident D + rare S
same reproductive fitness scale
matched environment
```

before attempting a dense frequency series.

---

## Corollary I2.1 — two-edge identification

Under the linear frequency game,

```text
Delta0 = Delta(0)=phi-eta
Delta1 = Delta(1)=phi+eta.
```

Therefore

```text
phi = (Delta0+Delta1)/2
eta = (Delta1-Delta0)/2.
```

The mapping between `(Delta0,Delta1)` and `(phi,eta)` is one-to-one.

QED.
