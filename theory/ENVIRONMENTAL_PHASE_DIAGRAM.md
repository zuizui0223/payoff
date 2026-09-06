# Environmental architecture-game phase diagram

This note extends the static SCH -> BALANCE -> BITA bridge into an environmental evolutionary game.

The purpose is not to rename the sister-repository domains. `BALANCE` and `BITA` remain defined by the frequency-independent architecture payoff gap

```text
phi(e) = s(e)L(e)-K(e).
```

PAYOFF asks the additional population question: after ecological frequency feedback is admitted, can an architecture invade, resist invasion, coexist, or become history dependent?

---

## 1. Environmental payoff generator

At environment `e`, define

```text
L(e)   >= 0     shared-coordinate conflict load supplied by SCH
s(e) in [0,1]  recoverable fraction supplied by the dimensional-release model
R(e)=s(e)L(e)  recoverable conflict loss
K(e)   >= 0     additional differentiated-architecture cost
phi(e)=R(e)-K(e).
```

Add frequency feedback `eta(e)` and let `p` be the population frequency of differentiated architecture `D`:

```text
Delta(p,e)
= pi_D(p,e)-pi_S(p,e)
= phi(e)+eta(e)(2p-1).
```

The replicator equation is

```text
dp/dt = p(1-p)Delta(p,e).
```

For any fixed `e`, this is the two-strategy PAYOFF game already proved in `THEOREMS.md`.

---

## 2. Two invasion surfaces replace one static crossing

The frequency-independent architecture crossing is

```text
phi=0
<=>
K=R.
```

But rare-architecture invasion is controlled by the endpoint payoff differences.

### Rare differentiated architecture in a shared resident population

At `p=0`,

```text
I_D = Delta(0)=phi-eta=R-K-eta.
```

Therefore

```text
D invades S  <=>  I_D>0
             <=>  K<R-eta.
```

The neutral invasion surface is

```text
Sigma_D: K=R-eta.
```

### Rare shared architecture in a differentiated resident population

At `p=1`, the invasion fitness of rare `S` is

```text
I_S = pi_S-pi_D
    = -Delta(1)
    = -phi-eta
    = K-R-eta.
```

Therefore

```text
S invades D  <=>  I_S>0
             <=>  K>R+eta.
```

The neutral invasion surface is

```text
Sigma_S: K=R+eta.
```

Thus frequency feedback splits the single static plane `K=R` into two invasion planes.

For fixed `s`, in `(L,K,eta)` coordinates:

```text
Sigma_D: K=sL-eta
Sigma_S: K=sL+eta.
```

They intersect exactly on

```text
eta=0,
K=sL,
```

which is the static BALANCE/BITA architecture crossing.

---

## 3. Four-phase theorem in `(R,K,eta)` space

Because

```text
phi=R-K,
```

the two dominance boundaries are

```text
K=R-|eta|
K=R+|eta|.
```

Away from equality surfaces:

```text
K > R+|eta|
    -> shared dominance

K < R-|eta|
    -> differentiated dominance

|K-R| < |eta| and eta<0
    -> reciprocal invasion
    -> stable architecture coexistence

|K-R| < |eta| and eta>0
    -> neither architecture invades when rare
    -> coordination bistability.
```

The middle game region therefore has exact width

```text
W_K = 2|eta|
```

on the architecture-cost axis.

Its center is always the static crossing `K=R`.

The sign of `eta` does not change the width; it changes the topology:

```text
eta<0  -> coexistence wedge
eta>0  -> bistability wedge.
```

This is a key distinction from the static SCH/BALANCE/BITA partition.

---

## 4. Static domain does not determine invasibility

Two consequences follow immediately.

### Static BALANCE can admit differentiated invasion

Suppose

```text
phi<0
```

so the shared architecture has the higher frequency-independent optimized payoff. If `eta<0` and

```text
|phi|<|eta|,
```

then

```text
I_D=phi-eta>0.
```

A rare differentiated architecture can invade even though the static state lies on the BALANCE side of `phi=0`.

The eventual result is stable coexistence, not differentiated dominance.

### Static BITA advantage can fail to invade

Suppose

```text
phi>0.
```

If `eta>0` and

```text
phi<eta,
```

then

```text
I_D=phi-eta<0.
```

A rare differentiated architecture cannot invade a shared resident population even though its frequency-independent optimized payoff is higher. The system lies in the coordination-bistable wedge.

Hence

```text
static architecture advantage != invasion success.
```

---

## 5. Reciprocal-invasion threshold inversion

If `R` and `eta` are held fixed while architecture cost `K` is varied experimentally, define the two neutral thresholds

```text
K_D = R-eta     # D is neutral when rare in S
K_S = R+eta     # S is neutral when rare in D.
```

Then

```text
R   = (K_D+K_S)/2
eta = (K_S-K_D)/2.
```

Thus reciprocal invasion identifies the frequency-independent recovery term and the frequency-feedback term separately.

The signed threshold split is

```text
K_S-K_D=2eta.
```

So threshold ordering itself diagnoses the sign of feedback:

```text
K_S<K_D  -> eta<0 -> reciprocal-invasion / coexistence geometry
K_S>K_D  -> eta>0 -> reciprocal-exclusion / coordination geometry.
```

If an independent SCH/BITA bridge supplies `R=sL`, the same experiment yields a direct consistency check between architecture optimization and population invasion.

---

## 6. Environmental path theorem

Let environment `e` move the frequency-independent payoff gap monotonically while `eta` remains constant:

```text
phi=phi(e).
```

If `phi(e)` is continuous and strictly increasing, each invasion boundary can be crossed at most once. If the environmental path spans both `-|eta|` and `+|eta|`, the phase sequence is exactly

```text
shared dominance
    -> middle game region
    -> differentiated dominance.
```

The middle region is

```text
stable coexistence     if eta<0
coordination bistability if eta>0.
```

Thus a monotone environmental driver does not imply a single architecture transition. With frequency feedback it generically produces two distinct invasion transitions.

### Linear environmental corollary

If

```text
phi(e)=alpha(e-e0),
alpha != 0,
```

where `e0` is the static `phi=0` crossing, then the two game boundaries occur at solutions of

```text
phi(e)=+-|eta|.
```

Their ordered locations are

```text
e_low  = min(e0-|eta|/alpha, e0+|eta|/alpha)
e_high = max(e0-|eta|/alpha, e0+|eta|/alpha),
```

with exact environmental width

```text
W_e = 2|eta|/|alpha|.
```

So stronger frequency feedback widens the observed transition zone, while a steeper environmental change in static architecture payoff compresses it.

---

## 7. Variable-feedback paths and re-entry

When both `phi(e)` and `eta(e)` vary, the relevant signed margins are

```text
I_D(e)=phi(e)-eta(e)
I_S(e)=-phi(e)-eta(e).
```

Every change in reciprocal-invasion status requires a zero crossing of at least one of these two margins.

Therefore apparent sequences such as

```text
shared dominance
-> coexistence/bistability
-> differentiated dominance
-> middle region again
```

require at least one invasion margin to be non-monotone or to cross zero repeatedly.

This gives a direct diagnostic: topology should be studied in the two margin functions, not inferred from `phi(e)` alone.

---

## 8. Relation to the sister repositories

The ownership rule remains strict.

```text
SCH
-> identifies shared-coordinate conflict and, when possible, L(e)

BALANCE
-> owns the static region L>0 and phi(e)<0

BITA
-> owns dimensional release, R=sL, K, and the static crossing phi=0

PAYOFF
-> takes those quantities as payoff inputs
-> adds eta and population frequency p
-> predicts invasion, coexistence, coordination barriers, ESSs, and environmental threshold splitting.
```

PAYOFF must not relabel a frequency-dependent coexistence state as empirical BALANCE or a coordination state as historical BITA differentiation without the corresponding sister-repository receipts.

---

## 9. Main quantitative prediction

The central new prediction of the environmental game is

```text
one static architecture crossing
K=R

becomes

two reciprocal-invasion crossings
K=R-eta
K=R+eta.
```

The separation of those crossings is itself an estimand:

```text
signed split = 2eta
absolute width = 2|eta|.
```

That split is zero in the frequency-independent theory, positive/negative in sign according to the direction of ecological feedback, and directly testable by reciprocal rare-architecture assays.