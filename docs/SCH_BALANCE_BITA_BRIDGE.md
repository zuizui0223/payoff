# SCH -> BALANCE -> SLK/PAYOFF, with BITA as an orthogonal mechanism layer

This note updates the cross-repository interface to the current scientific ownership. The filename retains its historical BITA label for existing links; it must not be read as granting BITA ownership of the `Phi=R-K` value boundary. This handoff distinguishes **architecture value**, **ecological mechanism**, **evolutionary realization**, and **historical evolutionary origin**.

## 1. Ownership of quantities

### SCH

SCH owns the one-coordinate functional-conflict problem.

```text
function 1 prefers theta1
function 2 prefers theta2
both must use shared coordinate z
```

The quadratic bridge identifies

```text
zS* = (a theta1+b theta2)/(a+b)
L   = [ab/(a+b)](theta1-theta2)^2.
```

Empirically, SCH should continue to distinguish state-specific optima from stricter pure-function optima. PAYOFF does not relax that identification rule.

### BALANCE

BALANCE owns the middle world in which conflict exists but the shared architecture still has higher optimized frequency-independent payoff.

```text
L > 0
phi = sL-K < 0.
```

PAYOFF preserves BALANCE's reserve

```text
rho = K-sL = -phi > 0
```

on the static common fitness scale.

Frequency-dependent persistence or invasion beyond that static domain must be labeled as PAYOFF game dynamics rather than silently back-projected into BALANCE.

### SLK/PAYOFF architecture-value handoff; BITA ecological-mechanism handoff

SLK owns recovery `R`, added architecture cost `K`, and architecture-value difference `Phi=R-K`. PAYOFF supplies mathematical realizations and transports the admissible value contrasts to population dynamics. BITA instead owns mechanism identification for an `A x D` trait interaction after multiple axes exist. It does **not** own the `Phi=0` architecture-value boundary.

A trait interaction on reproductive fitness cannot be equated with the architecture benefit `R-K`. The former may admit several ecological-channel decompositions; the latter requires matched optimized **alternative architectures** on a common fitness scale.

For the residual-coupling loss

```text
LD(x,y)=a(x-theta1)^2+b(y-theta2)^2+c(x-y)^2,
```

PAYOFF gives the exact quadratic realization

```text
s = |x*-y*|/|theta1-theta2|
  = ab/[ab+c(a+b)]
```

and

```text
R=sL.
```

Therefore

```text
phi = WD*-WS* = R-K = sL-K.
```

This is the exact algebraic bridge from SCH's one-coordinate conflict loss to the BALANCE/SLK architecture-value comparison, under this quadratic model. It is not a universal identity or a BITA mechanism-allocation estimand.

---

## 2. PAYOFF adds a population level without overriding scientific ownership

SCH qualifies conflict, BALANCE quantifies persistent compromise, and SLK owns architecture value and realization. PAYOFF develops explicit continuous and population-frequency models; BITA remains a separate causal-channel identification layer. For the two-architecture game:

```text
p = frequency of differentiated architecture D
Delta(p)=pi_D(p)-pi_S(p)=phi+eta(2p-1)
dp/dt=p(1-p)Delta(p).
```

The architecture-value and population hierarchy is

```text
SCH: identify genuine shared-coordinate functional conflict (L, if admissible)
        |
        v
BALANCE: shared world still outranks the differentiated-accessible world?
        |
        v
SLK: architecture recovery R, construction cost K, static Phi=R-K
        |
        v
PAYOFF: accessibility, topology, invasion, coexistence, fixation, occupancy
```

The orthogonal BITA question is whether an observed joint trait effect can be causally allocated to pollination, antagonism, and independently measured remaining channels. These allocations must not be substituted for `R`, `K`, or the history of new structure formation.

---

## 3. Static three-world diagram

For `L>0`:

```text
                    phi = sL-K

shared favored <--------- 0 ---------> differentiated favored
   BALANCE                                  SLK/PAYOFF
```

The static architecture boundary is

```text
K=sL=R.
```

In the exact residual-coupling model,

```text
s(c)=ab/[ab+c(a+b)].
```

When `0<K<L`, the critical coupling is

```text
c_crit = ab(L-K)/[K(a+b)].
```

Thus

```text
c > c_crit  -> too much residual integration; shared wins
c = c_crit  -> static architecture crossing
c < c_crit  -> sufficient release; differentiated wins.
```

If `K>=L`, even full decoupling (`s=1`) cannot pay in the static model. If `K=0` and `L>0`, any finite positive release favors differentiation.

---

## 4. PAYOFF splits the static crossing into reciprocal invasion surfaces

Rare `D` in an `S` resident population has margin

```text
I_D = Delta(0)=phi-eta=R-K-eta.
```

Rare `S` in a `D` resident population has margin

```text
I_S = -Delta(1)=-phi-eta=K-R-eta.
```

Therefore the neutral invasion surfaces are

```text
Sigma_D: K=R-eta
Sigma_S: K=R+eta.
```

For fixed `s`, in `(L,K,eta)` coordinates:

```text
Sigma_D: K=sL-eta
Sigma_S: K=sL+eta.
```

They collapse onto the sister-repository static crossing only at

```text
eta=0,
K=sL.
```

The strict population-game partition is

```text
K > R+|eta|                -> shared dominance
K < R-|eta|                -> differentiated dominance
|K-R|<|eta| and eta<0      -> stable coexistence
|K-R|<|eta| and eta>0      -> coordination bistability.
```

The width of the game-generated middle region on the architecture-cost axis is

```text
2|eta|.
```

This distinction is essential:

```text
BALANCE/SLK boundary  = static optimized worldline comparison
PAYOFF boundaries     = reciprocal population invasion conditions.
```

---

## 5. What happens to `phi=0` after frequency dependence is added?

The static gap remains meaningful but changes role.

### `eta=0`

```text
phi=0
```

is the architecture selection boundary.

### `eta<0`

Within the coexistence wedge,

```text
p*=(1-phi/eta)/2.
```

Hence

```text
phi<0 -> D minority
phi=0 -> p*=1/2
phi>0 -> D majority.
```

So the static architecture-value crossing becomes a coexistence-composition boundary.

### `eta>0`

Within the coordination wedge, the same `p*` is the unstable basin threshold. The deterministic basin lengths are

```text
B_S=p*
B_D=1-p*.
```

Therefore

```text
phi<0 -> S has the larger basin
phi=0 -> equal basin sizes
phi>0 -> D has the larger basin.
```

So the static crossing becomes a risk-dominance boundary, not an invasion boundary.

This is why

```text
static architecture advantage != invasion success
```

without making the static gap irrelevant.

---

## 6. Reciprocal invasion is an empirical identification layer

If `R` and `eta` are fixed while an architecture-cost axis can be varied, the neutral thresholds are

```text
K_D=R-eta
K_S=R+eta.
```

Therefore

```text
R   = (K_D+K_S)/2
eta = (K_S-K_D)/2.
```

Equivalently, if endpoint payoff differences are measured directly,

```text
Delta0=Delta(0)=phi-eta
Delta1=Delta(1)=phi+eta,
```

then

```text
phi=(Delta0+Delta1)/2
eta=(Delta1-Delta0)/2.
```

These are algebraic identification statements under the declared linear game. They require matched context and common fitness scale; they do not guarantee that all experimental thresholds are biologically reachable.

---

## 7. Environmental handoff

Let environment `e` change the static architecture gap:

```text
phi(e)=s(e)L(e)-K(e).
```

For constant `eta`, a continuous monotone `phi(e)` crosses at most two population-game boundaries:

```text
phi=-|eta|
phi=+|eta|.
```

If

```text
phi(e)=alpha(e-e0),
```

the static sister-repository crossing is at `e0`, while the two PAYOFF transitions are separated by

```text
2|eta|/|alpha|.
```

Thus PAYOFF predicts a measurable widening of the architecture transition zone relative to a one-threshold static account.

---

## 8. Hysteresis is not the same as positive frequency dependence

Two mechanisms can independently generate history dependence.

### Ecological coordination

```text
eta>0
```

makes common architectures increasingly favorable and creates an unstable frequency threshold.

### Structural switching costs

```text
-C_DS/T <= Delta(p) <= C_SD/T
```

allow either inherited architecture to persist because transitions themselves are costly.

The two should be estimated and tested separately. Their joint presence enlarges path dependence but does not make them the same mechanism.

---

## 9. Empirical handoff contract

A future empirical PAYOFF test should not estimate everything from one uncontrolled dataset.

```text
SCH receipt
- common fitness scale
- conflict-active context
- z_P*, z_G*, z_C* or stricter component optima when justified
- conflict budget L

BALANCE/SLK value receipt
- matched and optimized shared versus differentiated-accessible worldlines
- common reproductive-fitness scale, matching ecological context and joint uncertainty
- dimensional separation s or recovery R only when legitimately identified
- independently measured structural cost K, not an unallocated statistical residual
- direct gap WD*-WS* and decomposed R-K, with mismatch retained as an audit result

BITA mechanism receipt (orthogonal)
- factorial trait x trait interaction and selective consumer intervention, if available
- explicit mutualist, antagonist and independently supported remaining channels
- no conversion of unidentified interaction residual into architecture construction cost

PAYOFF-specific receipt
- architecture frequency p manipulated or naturally replicated
- invasion/growth/reproductive payoff of S and D across p
- reciprocal endpoint contrasts Delta(0), Delta(1)
- estimate eta from frequency dependence
- independent prediction of p* when an interior equilibrium/threshold exists
- transition-history manipulation for C_SD, C_DS when possible.
```

A particularly strong test is

```text
SCH/BALANCE/SLK estimate an admissible phi
+
reciprocal invasion estimate eta
        |
        v
predict p*=(1-phi/eta)/2
```

and then test that population prediction out of sample.

---

## 10. New predictions generated by the bridge

1. **Conflict does not imply differentiation.** `L>0` can coexist with `phi<0`.
2. **Full release has a hard static ceiling.** Since `s<=1`, differentiation cannot win on the static bridge when `K>=L`.
3. **Residual integration has a critical value.** For `0<K<L`, `c_crit=ab(L-K)/[K(a+b)]` separates shared and differentiated static optima.
4. **One static crossing becomes two invasion surfaces.** Their signed separation is `2eta` and absolute width is `2|eta|`.
5. **Static BALANCE can admit rare D invasion.** Negative frequency dependence can stabilize D at low frequency despite `phi<0`.
6. **Static differentiated-architecture advantage can face a coordination barrier.** Positive `phi` need not permit D invasion from rarity when `eta>0`.
7. **The static crossing changes role rather than disappearing.** It becomes a 50:50 composition boundary under `eta<0` and a risk-dominance boundary under `eta>0`.
8. **Architecture polymorphism is possible without environmental heterogeneity.** Negative frequency dependence can stabilize `0<p*<1` in one environment.
9. **Environmental transition width is quantitative.** Under a linear path it is `2|eta|/|alpha|`.
10. **Switching hysteresis and coordination bistability are experimentally distinguishable.** One depends on transition history/cost; the other on current population frequency.

These predictions are PAYOFF's main added value over a purely static trait-optimization account.