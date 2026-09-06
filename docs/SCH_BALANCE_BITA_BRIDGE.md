# SCH -> BALANCE -> BITA -> PAYOFF

This note freezes the cross-repository interface.

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

BALANCE owns the middle world in which conflict exists but the shared architecture still has higher optimized payoff.

```text
L > 0
phi = sL-K < 0.
```

PAYOFF preserves BALANCE's reserve

```text
rho = K-sL = -phi > 0
```

in the frequency-independent case.

When population feedback is added, BALANCE-like persistence can extend beyond the static sign of `phi` because the realized invasion payoff is

```text
Delta(p)=phi+eta(2p-1).
```

This extension must be labeled as PAYOFF game dynamics rather than silently back-projected into BALANCE.

### BITA

BITA owns the differentiated-coordinate world and mechanism identification after multiple axes exist.

PAYOFF gives an exact quadratic realization of BITA's partial differentiation parameter:

```text
s = |x*-y*|/|theta1-theta2|
  = ab/[ab+c(a+b)].
```

For the residual-coupling loss

```text
LD(x,y)=a(x-theta1)^2+b(y-theta2)^2+c(x-y)^2,
```

recovered conflict loss satisfies exactly

```text
R=sL.
```

Therefore

```text
phi = WD*-WS* = R-K = sL-K.
```

This is the exact algebraic bridge from the one-coordinate loss to the architecture comparison.

## 2. PAYOFF adds a new level rather than replacing the three chapters

The sister repositories stop at optimized fitness geometry and persistence across environments/history. PAYOFF adds population-frequency dependence:

```text
p = frequency of differentiated architecture D
Delta(p)=pi_D(p)-pi_S(p)=phi+eta(2p-1)
dp/dt=p(1-p)Delta(p).
```

This creates three new evolutionary outcomes unavailable from `phi` alone:

```text
eta < 0, |phi|<|eta| -> stable architecture polymorphism
eta > 0, |phi|<eta   -> coordination threshold / bistability
|phi|>|eta|          -> architecture dominance
```

Thus the full hierarchy is

```text
SCH
Does one shared coordinate create conflict, and where is its compromise?
        |
        v
BALANCE
Does shared architecture still outrank differentiated-accessible architecture?
        |
        v
BITA
How much conflict loss can extra dimensionality recover, at what cost, and by which mechanism?
        |
        v
PAYOFF
Given those architecture payoffs, what population state is evolutionarily stable when payoffs depend on architecture frequency and switching history?
```

## 3. Static three-world diagram

For `L>0`:

```text
                    phi = sL-K

shared favored <--------- 0 ---------> differentiated favored
   BALANCE                                  BITA
```

The architecture boundary is

```text
K=sL.
```

In the exact residual-coupling model,

```text
s(c)=ab/[ab+c(a+b)].
```

Hence the critical coupling is obtained from

```text
K = L ab/[ab+c_crit(a+b)].
```

When `0<K<L`, solving gives

```text
c_crit = ab(L-K)/[K(a+b)].
```

Interpretation:

```text
c > c_crit  -> too much residual integration; shared wins
c = c_crit  -> architecture crossing
c < c_crit  -> sufficient release; differentiated wins.
```

If `K>=L`, even full decoupling (`s=1`) cannot pay. If `K=0` and `L>0`, any finite release with `s>0` favors differentiation.

## 4. Game-theoretic phase diagram

Define

```text
Delta(0)=phi-eta
Delta(1)=phi+eta.
```

### Negative feedback (`eta<0`)

When `|phi|<|eta|`, neither pure architecture can exclude the other and the population converges to

```text
p*=(1-phi/eta)/2.
```

This is a stable mixed architecture state.

### Positive feedback (`eta>0`)

When `|phi|<eta`, both pure architectures are locally stable and

```text
p*=(1-phi/eta)/2
```

is an unstable invasion threshold. Initial architecture frequency determines the final state.

This is a genuine coordination game layered on top of the SCH/BALANCE/BITA payoff generator.

## 5. Hysteresis is not the same as positive frequency dependence

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

## 6. Empirical handoff contract

A future empirical PAYOFF test should not estimate everything from one uncontrolled dataset. Preferred handoff:

```text
SCH receipt
- common fitness scale
- conflict-active context
- z_P*, z_G*, z_C* or stricter component optima when justified
- conflict budget L

BITA/BALANCE receipt
- matched optimized shared and differentiated-accessible worldlines
- dimensional separation s or direct recovery R
- architecture cost K when structurally identified
- direct gap WD*-WS*

PAYOFF-specific receipt
- architecture frequency p manipulated or naturally replicated
- invasion/growth/reproductive payoff of S and D across p
- estimate eta from frequency dependence
- transition-history manipulation for C_SD, C_DS when possible.
```

The key new empirical test is therefore not merely whether `D` has higher fitness than `S`, but whether

```text
[pi_D(p)-pi_S(p)] - [pi_D(p')-pi_S(p')]
```

changes systematically with architecture frequency.

## 7. New predictions generated by the bridge

1. **Conflict does not imply differentiation.** `L>0` can coexist with `phi<0`.
2. **Full release has a hard ceiling.** Since `s<=1`, differentiation is impossible in the static model when `K>=L`.
3. **Residual integration has a critical value.** For `0<K<L`, `c_crit=ab(L-K)/[K(a+b)]` separates shared and differentiated optima.
4. **Architecture polymorphism is possible without environmental heterogeneity.** Negative frequency dependence can stabilize `0<p*<1` in a single environment.
5. **The static BITA boundary need not predict population outcome.** Positive frequency feedback can let either architecture persist near the crossing.
6. **Switching hysteresis and coordination bistability are experimentally distinguishable.** One depends on transition history/cost; the other on current population frequency.

These predictions are PAYOFF's main added value over a purely static trait-optimization account.
