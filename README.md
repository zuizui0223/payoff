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
loss_shared(z)=a(z-theta1)^2+b(z-theta2)^2.
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
= [1/(sum_i a_i)] sum_{i<j} a_i a_j(theta_i-theta_j)^2.
```

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

For `0<K<L`,

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

At `phi=0`, negative frequency dependence gives `p*=1/2`; positive frequency dependence gives equal deterministic basin widths.

## 4. Environmental phase diagram: one crossing becomes two invasion surfaces

Write `R=sL`. Rare-architecture invasion margins are

```text
I_D=Delta(0)=R-K-eta
I_S=-Delta(1)=K-R-eta.
```

Neutral invasion surfaces are

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

## 5. Finite populations: stochastic fixation and critical mass

For population size `N`, self-excluding interactions give

```text
Delta_N(i)
=[phi(N-2)+eta(2i-N)]/(N-1).
```

Using `f=exp(beta*pi)`, reciprocal single-mutant fixation obeys the exact ratio

```text
rho_D/rho_S=exp[beta phi(N-2)].
```

Thus, for `N>2`, `beta>0`,

```text
rho_D>rho_S iff phi>0 iff sL>K.
```

Under weak selection,

```text
rho_D>1/N iff 3phi>eta
rho_S>1/N iff -3phi>eta.
```

Equivalently,

```text
D single mutant favored: K<R-eta/3
S single mutant favored: K>R+eta/3.
```

The deterministic interaction band has width `2|eta|`; the weak-selection stochastic core has width `2|eta|/3`.

For arbitrary starting count `i`, the exact D-fixation probability is

```text
rho_i
= [sum_{k=0}^{i-1} exp(-beta C_k)]
  /[sum_{k=0}^{N-1} exp(-beta C_k)],
```

with

```text
C_k=k[phi(N-2)+eta(k+1-N)]/(N-1).
```

This defines a stochastic critical mass

```text
m_q=min{i: rho_i>=q},
```

such as `m_0.5`, the minimum starting number of differentiated individuals required for at least 50% fixation probability.

See [`theory/FINITE_POPULATION_MORAN.md`](theory/FINITE_POPULATION_MORAN.md) and [`theory/STOCHASTIC_ARCHITECTURE_BARRIER.md`](theory/STOCHASTIC_ARCHITECTURE_BARRIER.md).

## 6. Recurrent mutation: long-run stationary architecture occupancy

With offspring mutation

```text
S -> D at rate u_SD
D -> S at rate u_DS,
```

both positive, the finite Moran chain is irreducible. Its exact stationary distribution satisfies detailed balance:

```text
Pi_i/Pi_{i-1}
= T_{i-1}^+/T_i^-,
```

so

```text
Pi_i
= Pi_0 prod_{j=1}^i T_{j-1}^+/T_j^-.
```

This predicts the full long-run architecture-frequency profile, including mean `D` frequency, boundary mass, interior polymorphism mass, and stationary modes.

In the rare-mutation limit,

```text
log(Pi_N/Pi_0)
-> log(u_SD/u_DS)+beta*phi*(N-2)
```

up to the fixed mutation-rate ratio used in the limit. Substituting `phi=sL-K`,

```text
log(Pi_N/Pi_0)
-> log(u_SD/u_DS)+beta(N-2)(sL-K).
```

Hence mutation bias and architecture quality combine additively on the long-run monomorphic log-odds scale.

For symmetric rare mutation,

```text
Pi_N=Pi_0 iff phi=0 iff K=sL.
```

For asymmetric rare mutation the equal-occupancy crossing shifts to

```text
phi_mut=-log(u_SD/u_DS)/[beta(N-2)]
```

or

```text
K_mut=R+log(u_SD/u_DS)/[beta(N-2)].
```

Thus mutation bias toward `D` can sustain greater long-run differentiated occupancy at architecture costs that would lie on the static shared-favored side, while mutation bias toward `S` shifts the crossing in the opposite direction.

See [`theory/RECURRENT_MUTATION_STATIONARY.md`](theory/RECURRENT_MUTATION_STATIONARY.md).

## 7. Switching costs and hysteresis

If switching `S -> D` costs `C_SD`, switching `D -> S` costs `C_DS`, amortized over horizon `T`, either inherited state can persist whenever

```text
-C_DS/T <= Delta(p) <= C_SD/T.
```

The hysteresis width is

```text
(C_SD+C_DS)/T.
```

Frequency-dependent coordination and structural switching costs are separate mechanisms.

## 8. Many functions: coupling networks and modularization

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

## 9. Multiple architectures form a potential game

For candidate architectures with symmetric interaction matrix `A`, the multi-strategy replicator equation satisfies

```text
d/dt(p^T A p)
=2 sum_i p_i(pi_i-pi_bar)^2
>=0.
```

The two-strategy game has explicit potential

```text
V(p)=2(phi-eta)p+2eta p^2
```

with

```text
dV/dt=2p(1-p)Delta(p)^2>=0.
```

See [`theory/MULTI_ARCHITECTURE_GAME.md`](theory/MULTI_ARCHITECTURE_GAME.md) and [`theory/POTENTIAL_AND_RISK_DOMINANCE.md`](theory/POTENTIAL_AND_RISK_DOMINANCE.md).

## 10. Current theorem-level results

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
16. stochastic-core width `2|eta|/3`;
17. exact arbitrary-initial-count fixation curve `rho_i` and stochastic critical mass `m_q`;
18. exact recurrent-mutation stationary distribution by detailed balance;
19. rare-mutation monomorphic occupancy odds;
20. mutation-bias-shifted long-run architecture crossing.

## 11. Repository map

```text
theory/THEOREMS.md                    core deterministic proofs
theory/ENVIRONMENTAL_PHASE_DIAGRAM.md L-K-eta invasion surfaces
theory/FINITE_POPULATION_MORAN.md     stochastic finite-population fixation
theory/STOCHASTIC_ARCHITECTURE_BARRIER.md arbitrary-count fixation / critical mass
theory/RECURRENT_MUTATION_STATIONARY.md recurrent-mutation stationary theory
theory/NETWORK_EXTENSION.md           n-function coupling graph theory
theory/MULTI_ARCHITECTURE_GAME.md     many-architecture potential game
theory/POTENTIAL_AND_RISK_DOMINANCE.md two-strategy potential and basin results
docs/SCH_BALANCE_BITA_BRIDGE.md       cross-repository interface
docs/FINITE_POPULATION_HANDOFF.md     empirical finite-population handoff
docs/CLAIM_BOUNDARY.md                scientific claim ceiling
docs/PRIOR_ART_BOUNDARY.md            novelty/prior-art boundary
src/payoff_game.py                    deterministic reference implementation
src/finite_population.py              Moran fixation implementation
src/mutation_stationary.py            recurrent-mutation stationary implementation
scripts/release_curve.py              fixation probability vs starting count
scripts/stationary_profile.py         long-run stationary frequency profile
tests/                                algebraic and stochastic regressions
.github/workflows/test.yml            automated verification
```

## 12. Main interpretation

The hierarchy is now

```text
functional conflict
-> shared compromise load L
-> dimensional recovery R=sL
-> static architecture gap phi=R-K
-> reciprocal invasion under eta
-> deterministic ESS/coexistence/coordination
-> finite-population fixation under N and beta
-> recurrent-mutation stationary occupancy under u_SD,u_DS.
```

The general question is therefore:

> **When does evolution tolerate a shared-trait compromise, when does dimensional release become worthwhile, when can the alternative architecture invade, when will a finite population cross the architecture barrier, and which architectures dominate long-run occupancy when mutation keeps reintroducing both states?**
