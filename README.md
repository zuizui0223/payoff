# PAYOFF — evolutionary game of compromise, persistence, and trait differentiation

PAYOFF is a game-theoretic bridge across three sister repositories:

- [SCH](https://github.com/zuizui0223/sch): where a shared-coordinate compromise settles.
- [BALANCE](https://github.com/zuizui0223/balance): why the shared architecture can persist despite real conflict.
- [BITA](https://github.com/zuizui0223/bita): when extra trait dimensions become worth their cost.

The central move is deliberately conservative:

> **SCH supplies the within-organism payoff geometry; the evolutionary game is played between alternative heritable trait architectures in a population.**

Biological functions are payoff components, not literal strategic agents.

## 1. Payoff generator: the shared-trait problem

Two fitness-relevant functions prefer different trait values `theta1` and `theta2`:

```text
loss_shared(z)
  = a (z-theta1)^2 + b (z-theta2)^2,
  a,b > 0.
```

The unique shared optimum and unavoidable compromise load are

```text
zS* = (a theta1 + b theta2)/(a+b)
L   = [ab/(a+b)] (theta1-theta2)^2.
```

Thus `L>0` exactly when the two function-specific optima differ.

For `n` functions the same quantity becomes

```text
L_n
= sum_i a_i(theta_i-theta_bar)^2
= [1/(sum_i a_i)] sum_{i<j} a_i a_j(theta_i-theta_j)^2,
```

so shared-coordinate conflict is exactly weighted pairwise disagreement among function-specific optima.

## 2. Exact dimensional-release bridge

Let a differentiated phenotype use coordinates `x` and `y`, but retain residual coupling `c >= 0`:

```text
loss_diff(x,y)
  = a (x-theta1)^2
  + b (y-theta2)^2
  + c (x-y)^2.
```

Optimizing gives

```text
s = |x*-y*|/|theta1-theta2|
  = ab/[ab+c(a+b)]
```

and residual differentiated loss

```text
LD = [abc/(ab+c(a+b))](theta1-theta2)^2.
```

The recovered shared-compromise loss satisfies the exact identity

```text
R = L-LD = sL.
```

This turns the SCH/BALANCE/BITA bridge into an algebraic theorem for the declared quadratic model.

If the extra architecture costs `K >= 0`,

```text
phi = WD* - WS* = sL-K.
```

Therefore

```text
L = 0                 no shared-axis conflict
L > 0, phi < 0        BALANCE: conflict exists, shared architecture still wins
phi = 0               architecture critical surface
phi > 0               BITA: differentiated architecture wins.
```

When `0<K<L`, residual integration has an explicit critical value

```text
c_crit = ab(L-K)/[K(a+b)].
```

## 3. The actual evolutionary game

Let `p` be the population frequency of differentiated architecture `D`. The frequency-independent baseline is `phi=sL-K`.

Add the minimal ecological frequency-feedback term

```text
Delta(p) = payoff_D(p)-payoff_S(p)
         = phi + eta(2p-1).
```

A symmetric payoff-matrix representation is

```text
          S          D
S         0       phi-eta
D      phi-eta      2phi.
```

Population dynamics follow

```text
dp/dt = p(1-p) Delta(p).
```

This yields four qualitative outcomes.

### `eta = 0` — static architecture selection

```text
phi < 0  -> S fixes
phi > 0  -> D fixes
phi = 0  -> static architecture boundary.
```

### `eta < 0` — negative frequency dependence

If `|phi| < |eta|`, there is a unique stable mixed equilibrium

```text
p* = (1-phi/eta)/2.
```

Shared and differentiated architectures coexist.

### `eta > 0` — positive frequency dependence

If `|phi| < eta`, the same interior point exists but is unstable. Both `p=0` and `p=1` are locally stable, giving a coordination threshold / bistability.

Outside `|phi| < |eta|`, one architecture dominates.

## 4. Switching costs and hysteresis

If switching `S -> D` costs `C_SD`, switching `D -> S` costs `C_DS`, amortized over horizon `T`, either inherited state can persist whenever

```text
-C_DS/T <= Delta(p) <= C_SD/T.
```

The hysteresis width on the payoff-gap scale is

```text
(C_SD + C_DS)/T.
```

Frequency-dependent coordination and structural switching costs are separate mechanisms and can be tested independently.

## 5. Many functions: coupling networks and modularization

PAYOFF generalizes the two-coordinate model to a network of functional trait coordinates:

```text
D_lambda(x)
= (x-theta)^T A(x-theta)
+ lambda x^T L_G x.
```

`L_G` is a coupling-graph Laplacian. For a connected graph:

```text
x_lambda*=(A+lambda L_G)^(-1)A theta.
```

As integration strength `lambda` rises, optimized differentiated loss rises monotonically. With non-identical optima it rises strictly, from

```text
D_0*=0
```

toward the fully shared conflict load

```text
D_infinity*=L_n.
```

Thus partial modularization can be modeled as weakening or deleting coupling edges. If `0<K<L_n`, there is a unique critical integration strength at which recovered conflict loss exactly equals architecture cost.

See [`theory/NETWORK_EXTENSION.md`](theory/NETWORK_EXTENSION.md).

## 6. Multiple architectures form a potential game

Let candidate modular architectures have optimized intrinsic payoffs `b_i` and symmetric pairwise ecological feedback `H=H^T`. Define

```text
A_ij=b_i+b_j+H_ij.
```

Under the multi-strategy replicator equation,

```text
dp_i/dt=p_i[pi_i-pi_bar],
```

the mean game payoff obeys

```text
d/dt(p^T A p)
=2 sum_i p_i(pi_i-pi_bar)^2
>=0.
```

So the symmetric many-architecture extension is a potential-like evolutionary game with a Lyapunov function.

See [`theory/MULTI_ARCHITECTURE_GAME.md`](theory/MULTI_ARCHITECTURE_GAME.md).

## 7. What is proved here

Current analytic results include:

1. unique two-function shared compromise;
2. exact shared conflict load;
3. `n`-function conflict load as weighted pairwise disagreement;
4. exact partial-decoupling solution with residual coupling;
5. exact identity `R=sL` for the quadratic bridge;
6. monotone loss recovery as coupling weakens;
7. explicit critical residual coupling `c_crit`;
8. three-world partition by `L` and `phi=sL-K`;
9. full two-strategy replicator phase classification under linear frequency feedback;
10. ESS classification of pure and mixed architecture states;
11. switching-cost hysteresis band;
12. positive-affine payoff invariance up to time rescaling;
13. many-function network-coupling monotonicity and unique crossing;
14. multi-architecture symmetric potential-game Lyapunov theorem.

## 8. Repository map

```text
theory/THEOREMS.md                  core statements and proofs
theory/NETWORK_EXTENSION.md         n-function coupling graph / modularization theory
theory/MULTI_ARCHITECTURE_GAME.md   many-architecture potential game
docs/SCH_BALANCE_BITA_BRIDGE.md     exact mapping to sister repositories
docs/CLAIM_BOUNDARY.md              scientific claim ceiling
src/payoff_game.py                  dependency-free reference implementation
scripts/self_check.py               deterministic/random numerical identity audits
scripts/phase_sweep.py              phase-grid generator
tests/test_payoff_game.py           algebraic / game-phase regression tests
.github/workflows/test.yml          automated verification
```

## 9. Main interpretation

The general question is now:

> **When does evolution resolve functional conflict by accepting a one-coordinate compromise, when does that compromise remain the best architecture, when does evolution change phenotype dimensionality, and when can multiple architectures coexist or become history-dependent because their payoffs depend on population state?**

PAYOFF adds that population-game layer without changing the empirical estimands owned by SCH, BALANCE, or BITA.
