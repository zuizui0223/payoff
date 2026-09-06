# Potential structure, coexistence composition, and risk dominance

This note analyzes what remains of the static architecture gap

```text
phi=R-K=sL-K
```

inside the frequency-dependent middle game region.

The key result is that `phi=0` does not disappear when `eta != 0`. It changes role.

---

## 1. Exact potential for the two-architecture game

Use the symmetric payoff matrix

```text
          S          D
S         0       phi-eta
D      phi-eta      2phi.
```

Let `p` be the frequency of `D`, so population state is

```text
q=(1-p,p).
```

The mean game payoff is

```text
V(p)=q^T A q
    =2(phi-eta)p(1-p)+2phi p^2
    =2(phi-eta)p+2eta p^2.
```

Its derivative is

```text
dV/dp
=2(phi-eta)+4eta p
=2[phi+eta(2p-1)]
=2Delta(p).
```

Under replicator dynamics

```text
dp/dt=p(1-p)Delta(p),
```

therefore

```text
dV/dt
=(dV/dp)(dp/dt)
=2p(1-p)Delta(p)^2
>=0.
```

Thus `V` is a Lyapunov function for the two-architecture game. Equality holds at pure states and at interior equilibria.

This is the two-strategy specialization of the symmetric potential-game result used in the multi-architecture extension.

---

## 2. Negative frequency dependence: the static gap controls coexistence composition

Suppose

```text
eta<0
and
|phi|<|eta|.
```

The unique stable equilibrium is

```text
p*=(1-phi/eta)/2.
```

Writing `eta=-h`, `h>0`, gives

```text
p*=1/2 + phi/(2h).
```

Therefore

```text
phi<0  -> p*<1/2 -> D persists as the minority architecture,
phi=0  -> p*=1/2 -> equal architecture frequencies,
phi>0  -> p*>1/2 -> D persists as the majority architecture.
```

Because

```text
d2V/dp2=4eta<0,
```

`V` is strictly concave and this interior equilibrium is the unique potential maximum.

### Interpretation

Inside the coexistence wedge, the static BALANCE/BITA crossing `phi=0` is no longer a phase boundary. It is a **composition boundary**:

```text
static BALANCE side  -> differentiated minority at coexistence,
static BITA side     -> differentiated majority at coexistence.
```

So the frequency-independent architecture comparison still determines the direction of population composition even though negative frequency dependence prevents fixation.

---

## 3. Positive frequency dependence: the static gap controls risk dominance

Suppose

```text
eta>0
and
|phi|<eta.
```

The interior equilibrium

```text
p*=(1-phi/eta)/2
```

is unstable. Initial conditions satisfy

```text
p(0)<p* -> S fixation,
p(0)>p* -> D fixation.
```

Hence the basin lengths on the unit interval are

```text
B_S=p*,
B_D=1-p*.
```

`D` is risk dominant in the deterministic basin-size sense iff

```text
B_D>B_S
<=>
1-p*>p*
<=>
p*<1/2
<=>
phi>0.
```

Similarly,

```text
phi<0 -> S has the larger basin,
phi=0 -> equal basin sizes.
```

Because

```text
d2V/dp2=4eta>0,
```

the interior threshold is the potential minimum, while the pure states occupy the two attraction basins.

### Interpretation

Inside the coordination wedge, `phi=0` is again not an invasion boundary. It is a **risk-dominance boundary**:

```text
phi<0 -> S has the larger basin,
phi>0 -> D has the larger basin.
```

This resolves the apparent paradox that a differentiated architecture may have `phi>0` but still fail to invade when rare. Positive `phi` does not guarantee rare invasion under positive frequency dependence; it instead shifts the coordination threshold in favor of `D`.

---

## 4. Unified role of the static crossing

The same quantity

```text
phi=sL-K
```

has three different dynamical meanings depending on frequency feedback.

```text
eta=0
    phi=0 is the architecture selection boundary.

eta<0
    phi=0 is the 50:50 coexistence-composition boundary.

eta>0
    phi=0 is the equal-basin / risk-dominance boundary.
```

The invasion phase boundaries themselves are instead

```text
phi=-|eta|
and
phi=+|eta|.
```

Thus frequency dependence does not invalidate the SCH/BALANCE/BITA static payoff gap. It changes which population-level question that gap answers.

---

## 5. Quantitative predictions

### Coexistence composition slope

For fixed `eta<0`,

```text
dp*/dphi = -1/(2eta) = 1/(2|eta|) > 0.
```

So equilibrium differentiated frequency changes linearly with the static architecture gap.

Since `phi=R-K`,

```text
dp*/dK = -1/(2|eta|),
dp*/dR =  1/(2|eta|).
```

### Coordination threshold slope

For fixed `eta>0`, the unstable threshold obeys

```text
dp*/dphi = -1/(2eta) < 0.
```

Increasing differentiated architecture advantage lowers the initial frequency required for `D` to cross the coordination barrier.

Since `phi=R-K`,

```text
dp*/dK =  1/(2eta),
dp*/dR = -1/(2eta).
```

Thus higher architecture cost raises the critical starting frequency for differentiation, while greater recovered compromise loss lowers it.

---

## 6. Empirical consequence

The three quantities

```text
rare-invasion thresholds,
interior coexistence frequency or coordination threshold,
static optimized worldline gap phi
```

are not redundant.

They test different layers of the same model:

```text
phi
-> frequency-independent architecture comparison

eta
-> inferred from reciprocal invasion splitting

p*
-> predicted from phi/eta
```

Therefore a measured `phi` and reciprocal-invasion estimate of `eta` generate an out-of-sample quantitative prediction

```text
p*=(1-phi/eta)/2.
```

Agreement would connect the SCH/BALANCE/BITA payoff bridge to actual population dynamics; disagreement would diagnose missing frequency dependence, nonlinear feedback, context mismatch, or a failure of the linear two-strategy game.