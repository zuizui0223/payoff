# PAYOFF — evolutionary game of compromise, persistence, and trait differentiation

PAYOFF is a game-theoretic bridge across three sister repositories:

- [SCH](https://github.com/zuizui0223/sch): where a shared-coordinate compromise settles.
- [BALANCE](https://github.com/zuizui0223/balance): why the shared architecture can persist despite real conflict.
- [BITA](https://github.com/zuizui0223/bita): when extra trait dimensions become worth their cost.

The central move is deliberately conservative:

> **SCH supplies the within-organism payoff geometry; the evolutionary game is played between alternative trait architectures in a population.**

This avoids pretending that biological functions are literally strategic agents.

## 1. Payoff generator: the shared-trait problem

Two fitness-relevant functions prefer different trait values `theta1` and `theta2`:

```text
loss_shared(z)
  = a (z-theta1)^2 + b (z-theta2)^2,
  a,b > 0.
```

The unique shared optimum is

```text
zS* = (a theta1 + b theta2)/(a+b)
```

and the unavoidable compromise load is

```text
L = [ab/(a+b)] (theta1-theta2)^2.
```

Thus `L>0` exactly when the two function-specific optima differ.

## 2. Exact dimensional-release bridge

Let a differentiated phenotype use coordinates `x` and `y`, but retain residual coupling `c >= 0`:

```text
loss_diff(x,y)
  = a (x-theta1)^2
  + b (y-theta2)^2
  + c (x-y)^2.
```

Optimizing gives residual differentiated loss

```text
LD = [abc/(ab+c(a+b))] (theta1-theta2)^2.
```

Define the realized separation fraction

```text
s = |x*-y*| / |theta1-theta2|
  = ab/[ab+c(a+b)].
```

Then, exactly,

```text
R = L-LD = sL.
```

This is the algebraic bridge used qualitatively by SCH/BALANCE/BITA: in this quadratic model, the fraction of function-specific optimum separation actually released by differentiation equals the fraction of shared compromise load recovered.

If the extra architecture costs `K >= 0`, the optimized architecture payoff gap is

```text
phi = WD* - WS* = sL-K.
```

So:

```text
L = 0                 no shared-axis conflict
L > 0, phi < 0        BALANCE: conflict exists, shared architecture still wins
phi = 0               architecture critical surface
phi > 0               BITA: differentiated architecture wins
```

## 3. The actual evolutionary game

Let `p` be the population frequency of the differentiated architecture `D`. The frequency-independent baseline is `phi=sL-K`.

Add the minimal ecological frequency-feedback term

```text
Delta(p) = payoff_D(p)-payoff_S(p)
         = phi + eta(2p-1).
```

`eta` measures whether differentiation becomes more or less favorable as differentiated phenotypes become common.

Population dynamics follow the two-strategy replicator equation

```text
dp/dt = p(1-p) Delta(p).
```

This yields a complete phase classification.

### eta = 0 — architecture dominance

```text
phi < 0  -> S fixes
phi > 0  -> D fixes
phi = 0  -> static architecture boundary
```

### eta < 0 — negative frequency dependence

If `|phi| < |eta|`, there is a unique stable mixed equilibrium

```text
p* = (1-phi/eta)/2.
```

Shared and differentiated architectures coexist.

### eta > 0 — positive frequency dependence

If `|phi| < eta`, the same interior point exists but is unstable. Both `p=0` and `p=1` are locally stable, producing a coordination threshold / history-dependent architecture state.

Outside `|phi| < |eta|`, one architecture dominates.

## 4. Switching costs and hysteresis

If switching `S -> D` costs `C_SD`, switching `D -> S` costs `C_DS`, amortized over horizon `T`, then history dependence is possible whenever

```text
-C_DS/T <= Delta(p) <= C_SD/T.
```

The hysteresis width on the payoff-gap scale is

```text
(C_SD + C_DS)/T.
```

This recovers BALANCE's switching-cost result as a state-dependent architecture game and lets it interact with ecological frequency dependence.

## 5. What is proved here

Current analytic results:

1. unique two-function shared compromise;
2. exact shared conflict load;
3. `n`-function conflict load as weighted pairwise disagreement;
4. exact partial-decoupling solution with residual coupling;
5. exact identity `R=sL` for the quadratic bridge;
6. monotone loss recovery as coupling weakens;
7. three-world partition by `L` and `phi=sL-K`;
8. full two-strategy replicator phase classification under linear frequency feedback;
9. ESS classification of pure and mixed architecture states;
10. switching-cost hysteresis band;
11. positive-affine payoff invariance up to time rescaling.

See [`theory/THEOREMS.md`](theory/THEOREMS.md).

## 6. Repository map

```text
theory/THEOREMS.md                  formal statements and proofs
docs/SCH_BALANCE_BITA_BRIDGE.md     exact mapping to the sister repositories
docs/CLAIM_BOUNDARY.md              what is and is not being claimed
src/payoff_game.py                  reference implementation
scripts/phase_sweep.py              phase-grid generator
tests/test_payoff_game.py           algebraic / phase regression tests
```

## 7. Interpretation

The general evolutionary question is:

> **When does evolution resolve functional conflict by accepting a one-coordinate compromise, when does that compromise remain the best architecture, and when does evolution instead change the dimensionality of phenotype space?**

PAYOFF turns that question into an evolutionary game without changing the empirical estimands owned by SCH, BALANCE, or BITA.
