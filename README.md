# PAYOFF — evolutionary game of compromise, persistence, and trait differentiation

PAYOFF is a game-theoretic bridge across three sister repositories:

- [SCH](https://github.com/zuizui0223/sch): where a shared-coordinate compromise settles.
- [BALANCE](https://github.com/zuizui0223/balance): why the shared architecture can persist despite real conflict.
- [BITA](https://github.com/zuizui0223/bita): when extra trait dimensions become worth their cost.

The central move is deliberately conservative:

> **SCH supplies the within-organism payoff geometry; the evolutionary game is played between alternative heritable trait architectures in a population.**

Biological functions are payoff components, not literal strategic agents.

## 1. Payoff generator: shared-trait conflict

For two functions with preferred trait values `theta1`, `theta2` and weights `a,b>0`,

```text
loss_shared(z)
= a(z-theta1)^2+b(z-theta2)^2.
```

The unique compromise and conflict load are

```text
zS*=(a theta1+b theta2)/(a+b)
L=[ab/(a+b)](theta1-theta2)^2.
```

For `n` functions,

```text
L_n
= sum_i a_i(theta_i-theta_bar)^2
= [1/(sum_i a_i)] sum_{i<j} a_i a_j(theta_i-theta_j)^2,
```

so one-coordinate conflict is weighted pairwise disagreement among function-specific optima.

## 2. Exact dimensional-release bridge

For differentiated coordinates `x,y` with residual coupling `c>=0`,

```text
loss_diff(x,y)
= a(x-theta1)^2+b(y-theta2)^2+c(x-y)^2.
```

Optimization gives

```text
s=|x*-y*|/|theta1-theta2|
 =ab/[ab+c(a+b)]
```

and the exact recovered compromise loss

```text
R=L-LD=sL.
```

With added architecture cost `K>=0`,

```text
phi=WD*-WS*=R-K=sL-K.
```

Thus

```text
L=0                 no shared-axis conflict
L>0, phi<0          BALANCE: conflict exists, shared architecture still wins
phi=0               architecture critical surface
phi>0               BITA: differentiated architecture wins.
```

For `0<K<L`, the critical residual coupling is

```text
c_crit=ab(L-K)/[K(a+b)].
```

## 3. Population evolutionary game

Let `p` be the frequency of differentiated architecture `D`. Add minimal ecological frequency feedback:

```text
Delta(p)=payoff_D-payoff_S
        =phi+eta(2p-1).
```

One symmetric payoff matrix is

```text
          S          D
S         0       phi-eta
D      phi-eta      2phi.
```

Replicator dynamics are

```text
dp/dt=p(1-p)Delta(p).
```

The strict deterministic phases are

```text
phi<-|eta|                  shared dominance
phi>|eta|                   differentiated dominance
|phi|<|eta|, eta<0          stable architecture coexistence
|phi|<|eta|, eta>0          coordination bistability.
```

The interior equilibrium/threshold is

```text
p*=(1-phi/eta)/2.
```

The static crossing `phi=0` remains meaningful: under `eta<0` it is the point `p*=1/2`; under `eta>0` it is the risk-dominance switch where the two deterministic basins have equal width.

## 4. Environmental phase diagram: one crossing becomes two invasion surfaces

Write `R=sL`. Rare-architecture invasion margins are

```text
I_D=Delta(0)=R-K-eta
I_S=-Delta(1)=K-R-eta.
```

Neutral invasion surfaces are therefore

```text
K_D=R-eta
K_S=R+eta.
```

For fixed `s` these are two planes in `(L,K,eta)` space:

```text
K=sL-eta
K=sL+eta.
```

The game-generated middle region has exact cost width

```text
W_K=2|eta|.
```

Hence static architecture advantage and rare-type invasion are distinct:

```text
static BALANCE (phi<0) can admit rare D invasion when eta<0,
static BITA advantage (phi>0) can fail to invade when eta>0.
```

Reciprocal neutral-cost thresholds identify

```text
R=(K_D+K_S)/2
eta=(K_S-K_D)/2.
```

Along a linear environmental gradient `phi(e)=alpha(e-e0)`, the two invasion transitions are separated by

```text
W_e=2|eta|/|alpha|.
```

See [`theory/ENVIRONMENTAL_PHASE_DIAGRAM.md`](theory/ENVIRONMENTAL_PHASE_DIAGRAM.md).

## 5. Finite populations: stochastic fixation

PAYOFF now also has an exact finite-population Moran layer. For population size `N`, self-excluding interactions give

```text
Delta_N(i)
=[phi(N-2)+eta(2i-N)]/(N-1),
```

where `i` is the number of `D` individuals.

Using exponential payoff-to-fitness mapping `f=exp(beta*pi)`, the exact fixation probability of one `D` mutant is

```text
rho_D
= {sum_{k=0}^{N-1}
   exp[-beta k{phi(N-2)+eta(k+1-N)}/(N-1)]}^(-1).
```

The reciprocal fixation ratio simplifies to

```text
rho_D/rho_S
=exp[beta phi(N-2)].
```

Therefore, for `N>2` and `beta>0`,

```text
rho_D>rho_S iff phi>0 iff sL>K.
```

So frequency feedback changes the absolute fixation probabilities but cancels from their relative ordering under the declared exponential Moran model. The static architecture crossing survives as an exact reciprocal-fixation boundary.

Under weak selection, comparison with the neutral fixation probability `1/N` gives

```text
rho_D>1/N iff 3phi>eta
rho_S>1/N iff -3phi>eta.
```

Equivalently,

```text
D single mutant favored: K<R-eta/3
S single mutant favored: K>R+eta/3.
```

Thus the deterministic frequency-feedback band has width

```text
2|eta|
```

while the weak-selection stochastic core has width

```text
2|eta|/3.
```

For strong positive frequency dependence (`eta>3|phi|`), neither reciprocal single mutant is favored above neutral drift. For strong negative frequency dependence (`eta<-3|phi|`), both are.

In the coordination regime `eta>0`,

```text
rho_D>1/N iff p*<1/3,
```

recovering the established one-third law in architecture variables:

```text
3(sL-K)>eta.
```

PAYOFF does not claim the one-third law as new; its contribution is the explicit ecological-to-architecture substitution chain `L -> sL -> phi -> fixation`.

See [`theory/FINITE_POPULATION_MORAN.md`](theory/FINITE_POPULATION_MORAN.md).

## 6. Switching costs and hysteresis

If switching `S -> D` costs `C_SD`, switching `D -> S` costs `C_DS`, amortized over horizon `T`, either inherited state can persist whenever

```text
-C_DS/T <= Delta(p) <= C_SD/T.
```

The hysteresis width is

```text
(C_SD+C_DS)/T.
```

Frequency-dependent coordination and structural switching costs are separate mechanisms.

## 7. Many functions: coupling networks and modularization

For a network of functional trait coordinates,

```text
D_lambda(x)
=(x-theta)^T A(x-theta)+lambda x^T L_G x.
```

For a connected coupling graph,

```text
x_lambda*=(A+lambda L_G)^(-1)A theta.
```

Increasing integration `lambda` increases optimized loss monotonically, strictly when function-specific optima differ, from `D_0*=0` toward the fully shared load `L_n`. If `0<K<L_n`, one critical integration strength separates profitable from unprofitable release.

See [`theory/NETWORK_EXTENSION.md`](theory/NETWORK_EXTENSION.md).

## 8. Multiple architectures form a potential game

For candidate architectures with symmetric interaction matrix `A`, the multi-strategy replicator equation

```text
dp_i/dt=p_i[pi_i-pi_bar]
```

satisfies

```text
d/dt(p^T A p)
=2 sum_i p_i(pi_i-pi_bar)^2
>=0.
```

The two-strategy game also has explicit potential

```text
V(p)=2(phi-eta)p+2eta p^2
```

with

```text
dV/dt=2p(1-p)Delta(p)^2>=0.
```

See [`theory/MULTI_ARCHITECTURE_GAME.md`](theory/MULTI_ARCHITECTURE_GAME.md) and [`theory/POTENTIAL_AND_RISK_DOMINANCE.md`](theory/POTENTIAL_AND_RISK_DOMINANCE.md).

## 9. Current theorem-level results

Current analytic results include:

1. unique shared compromise and exact conflict load;
2. `n`-function conflict as weighted pairwise disagreement;
3. exact partial release `R=sL` in the quadratic residual-coupling model;
4. explicit critical residual coupling;
5. static SCH/BALANCE/BITA partition by `phi=sL-K`;
6. complete deterministic two-strategy phase classification;
7. reciprocal invasion surfaces `K=R+-eta` and game-middle width `2|eta|`;
8. reciprocal-threshold identification of `R` and `eta`;
9. linear environmental transition width `2|eta|/|alpha|`;
10. switching-cost hysteresis;
11. potential/risk-dominance results;
12. many-function network-coupling monotonicity;
13. exact finite-population Moran fixation formula;
14. exact reciprocal fixation ratio `rho_D/rho_S=exp[beta phi(N-2)]`;
15. weak-selection architecture one-third criterion `3phi>eta`;
16. stochastic-core width `2|eta|/3`.

## 10. Repository map

```text
theory/THEOREMS.md                    core deterministic proofs
theory/ENVIRONMENTAL_PHASE_DIAGRAM.md L-K-eta invasion surfaces
theory/FINITE_POPULATION_MORAN.md     stochastic finite-population fixation
theory/NETWORK_EXTENSION.md           n-function coupling graph theory
theory/MULTI_ARCHITECTURE_GAME.md     many-architecture potential game
theory/POTENTIAL_AND_RISK_DOMINANCE.md two-strategy potential and basin results
docs/SCH_BALANCE_BITA_BRIDGE.md       cross-repository interface
docs/CLAIM_BOUNDARY.md                scientific claim ceiling
src/payoff_game.py                    deterministic reference implementation
src/finite_population.py              Moran fixation implementation
scripts/phase_sweep.py                phi-eta phase grid
scripts/lke_phase_sweep.py            L-K-eta phase grid
scripts/finite_population_sweep.py    fixation-probability grid
tests/                                algebraic and stochastic regressions
.github/workflows/test.yml            automated verification
```

## 11. Main interpretation

The hierarchy is now

```text
functional conflict
-> shared compromise load L
-> dimensional recovery R=sL
-> static architecture gap phi=R-K
-> reciprocal invasion under eta
-> deterministic ESS/coexistence/coordination
-> finite-population fixation under N and beta.
```

The general question is therefore:

> **When does evolution tolerate a shared-trait compromise, when does dimensional release become worthwhile, when can the alternative architecture invade, and when will a finite population actually cross the architecture barrier despite drift and frequency dependence?**
