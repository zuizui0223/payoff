# Recurrent mutation and the stationary architecture distribution

This note extends PAYOFF from absorbing fixation dynamics to long-run mutation-selection-drift balance.

The state is

```text
i = number of differentiated-architecture individuals D,
i=0,...,N.
```

The finite-population PAYOFF game retains

```text
phi = sL-K,
```

and symmetric architecture payoff matrix

```text
          S          D
S         0       phi-eta
D      phi-eta      2phi.
```

With `i` differentiated individuals and self-interaction excluded,

```text
Delta_N(i)
= pi_D(i)-pi_S(i)
= [phi(N-2)+eta(2i-N)]/(N-1).
```

Fitness is mapped exponentially,

```text
f_D(i)=exp(beta*pi_D(i)),
f_S(i)=exp(beta*pi_S(i)).
```

Offspring mutate

```text
S -> D with probability u_SD,
D -> S with probability u_DS,
```

before one uniformly random individual dies.

For

```text
0<u_SD<1,
0<u_DS<1,
```

the state chain is irreducible and therefore has a unique stationary distribution.

---

## Theorem 1 — exact recurrent-mutation transition probabilities

Let

```text
q_D(i)
= i f_D(i) / [i f_D(i)+(N-i)f_S(i)]
```

be the probability that the selected parent is `D` for `0<i<N`.

After mutation, the offspring is `D` with probability

```text
b_D(i)
= q_D(i)(1-u_DS) + [1-q_D(i)]u_SD.
```

Hence

```text
T_i^+
= b_D(i)(N-i)/N,

T_i^-
= [1-b_D(i)]i/N.
```

At the monomorphic boundaries,

```text
T_0^+ = u_SD,
T_N^- = u_DS.
```

### Proof

The parent is sampled in proportion to reproductive fitness. Conditional on parent identity, the offspring either retains or mutates its architecture. A state increase requires a `D` offspring and death of an `S` individual; a state decrease requires an `S` offspring and death of a `D` individual. At `i=0` and `i=N`, only mutation can generate the absent type. QED.

---

## Theorem 2 — exact stationary distribution and reversibility

For any finite irreducible birth-death chain,

```text
Pi_i T_i^+ = Pi_{i+1} T_{i+1}^-
```

under the stationary distribution. Therefore

```text
Pi_i/Pi_{i-1}
= T_{i-1}^+/T_i^-,
```

and

```text
Pi_i
= Pi_0 prod_{j=1}^i [T_{j-1}^+/T_j^-].
```

Normalization gives

```text
Pi_0
= {1 + sum_{i=1}^N prod_{j=1}^i [T_{j-1}^+/T_j^-]}^(-1).
```

Thus the recurrent-mutation PAYOFF process is reversible and has an exact stationary distribution over all architecture counts.

### Proof

A finite irreducible birth-death chain has zero stationary probability current because the only edge connecting the sets `{0,...,i}` and `{i+1,...,N}` is the edge `i <-> i+1`. Stationarity therefore forces equal left-to-right and right-to-left flux across every such edge. Recursion yields the product formula; normalization determines `Pi_0`. QED.

### Immediate consequence

The stationary shape is locally diagnosed by

```text
Pi_i/Pi_{i-1}=T_{i-1}^+/T_i^-.
```

A stationary mode occurs where this ratio crosses from above one to below one, with the obvious boundary cases.

This is the mutation-selection-drift analogue of the deterministic sign change in `Delta(p)`, but the two should not be conflated.

---

## Theorem 3 — rare-mutation reduction to reciprocal fixation

Let

```text
u_SD = epsilon*r_SD,
u_DS = epsilon*r_DS,
```

with fixed positive `r_SD,r_DS`, and take `epsilon -> 0` at fixed `N,phi,eta,beta`.

The stationary distribution concentrates on the two monomorphic states. The long-run boundary occupancy ratio satisfies

```text
Pi_N/Pi_0
-> (r_SD/r_DS)(rho_D/rho_S),
```

where

```text
rho_D = fixation probability of one D in an S population,
rho_S = fixation probability of one S in a D population.
```

For the exponential PAYOFF Moran model, the previously derived exact reciprocal-fixation theorem is

```text
rho_D/rho_S
= exp[beta*phi*(N-2)].
```

Hence

```text
Pi_N/Pi_0
-> (r_SD/r_DS) exp[beta*phi*(N-2)].
```

Equivalently,

```text
log(Pi_N/Pi_0)
-> log(r_SD/r_DS) + beta*phi*(N-2).
```

### Proof

From Theorem 2,

```text
Pi_N/Pi_0
= (T_0^+/T_N^-)
  prod_{i=1}^{N-1}(T_i^+/T_i^-).
```

As `epsilon -> 0`,

```text
T_0^+/T_N^- -> r_SD/r_DS.
```

For every interior state, mutation disappears and the ordinary Moran transition ratio is

```text
T_i^+/T_i^-
-> f_D(i)/f_S(i)
= exp[beta Delta_N(i)].
```

Therefore

```text
Pi_N/Pi_0
-> (r_SD/r_DS)
   exp[beta sum_{i=1}^{N-1} Delta_N(i)].
```

The finite-population PAYOFF identity

```text
sum_{i=1}^{N-1} Delta_N(i)=phi(N-2)
```

gives the result. QED.

---

## Corollary 3.1 — frequency feedback cancels from rare-mutation boundary odds

The weak-mutation monomorphic occupancy ratio depends on

```text
phi, beta, N, r_SD/r_DS
```

but not on `eta`.

This does **not** imply that `eta` is irrelevant to the stationary process. At finite mutation it changes interior transitions and therefore the full stationary distribution. Even in the weak-mutation limit, `eta` changes absolute fixation times and absolute fixation probabilities. The cancellation is specific to reciprocal boundary odds.

---

## Corollary 3.2 — symmetric mutation preserves the static architecture crossing

If

```text
r_SD=r_DS,
```

then

```text
Pi_N>Pi_0 iff phi>0,
Pi_N=Pi_0 iff phi=0,
Pi_N<Pi_0 iff phi<0
```

in the rare-mutation limit for `N>2` and `beta>0`.

Since

```text
phi=sL-K,
```

the static SCH/BALANCE/BITA crossing

```text
K=sL
```

is exactly the equal long-run monomorphic occupancy boundary under symmetric rare mutation.

Thus `phi=0` now has four related but distinct roles across PAYOFF:

```text
frequency-independent deterministic game:
    architecture selection boundary

negative frequency dependence:
    50:50 coexistence-composition boundary

positive frequency dependence:
    deterministic risk-dominance boundary

finite recurrent mutation, rare symmetric mutation:
    equal all-S / all-D stationary occupancy boundary.
```

---

## Corollary 3.3 — mutation bias shifts the long-run architecture crossing

With asymmetric rare mutation, equal boundary occupancy requires

```text
log(r_SD/r_DS) + beta*phi*(N-2)=0.
```

Therefore

```text
phi_mut
= -log(r_SD/r_DS)/[beta(N-2)].
```

Using

```text
phi=R-K,
R=sL,
```

the corresponding architecture-cost crossing is

```text
K_mut
= R + log(r_SD/r_DS)/[beta(N-2)].
```

Hence a mutation bias toward differentiated architecture (`r_SD>r_DS`) shifts equal long-run occupancy toward larger architecture costs; a bias toward shared architecture shifts it toward smaller costs.

The shift shrinks as

```text
beta(N-2)
```

increases, because stronger selection or larger population size makes a fixed mutation bias less important relative to cumulative selection.

---

## Corollary 3.4 — rare-mutation boundary occupancy has logistic form

Conditional on the population being in one of the two monomorphic states in the rare-mutation limit,

```text
P(all D)
= 1 / {1 + exp[-Z]},
```

where

```text
Z
= log(r_SD/r_DS) + beta*phi*(N-2).
```

Substituting the architecture bridge,

```text
Z
= log(r_SD/r_DS)
  + beta(N-2)(sL-K).
```

This gives a compact long-run prediction from the same ecological quantities used by SCH, BALANCE, and BITA.

---

## 4. Stationary statistics beyond fixation

Unlike the absorbing no-mutation Moran process, recurrent mutation assigns positive long-run probability to every state. Useful estimands are therefore

```text
mean D frequency
E[i/N],

boundary mass
Pi_0+Pi_N,

interior polymorphism mass
1-Pi_0-Pi_N,

mean two-type heterozygosity
E[2(i/N)(1-i/N)].
```

These distinguish at least three biologically different long-run situations:

```text
1. boundary-dominated switching
   most time is spent near all-S or all-D;

2. interior mutation-selection balance
   substantial stationary mass lies at intermediate architecture frequencies;

3. biased long-run occupancy
   one architecture dominates the stationary mean even though recurrent mutation continuously regenerates the other.
```

The exact stationary product formula should be used when mutation is not demonstrably rare; the two-state fixation approximation should not be extrapolated into moderate or high mutation regimes.

---

## 5. Connection to the earlier stochastic critical-mass result

The no-mutation PAYOFF model asks

```text
rho_i
= probability that D eventually fixes from initial count i.
```

The recurrent-mutation model asks

```text
Pi_i
= fraction of long-run time spent at count i.
```

These are different objects.

The first quantifies one release event before absorption. The second quantifies persistent mutation-selection-drift balance when neither monomorphic state remains absorbing.

In the rare-mutation limit they reconnect through

```text
Pi_N/Pi_0
-> (r_SD/r_DS)(rho_D/rho_S).
```

That limiting identity is the formal bridge between the two layers.

---

## 6. Empirical handoff

A recurrent-mutation PAYOFF analysis needs

```text
SCH/BALANCE/BITA:
    L, s or R, K

PAYOFF frequency game:
    eta

finite population:
    N, beta

mutation layer:
    u_SD, u_DS or at minimum their rare-mutation ratio.
```

Then the framework predicts either

```text
full stationary distribution Pi_0,...,Pi_N
```

or, when mutation is independently shown to be rare,

```text
log(Pi_N/Pi_0)
≈ log(u_SD/u_DS)+beta(N-2)(sL-K).
```

A strong test would estimate the architecture payoffs and mutation bias independently, freeze them prospectively, and compare the predicted stationary architecture-frequency distribution with long-run replicated populations.

---

## 7. Claim boundary

Recurrent-mutation Moran processes, stationary birth-death distributions, mutation-selection balance, and rare-mutation reductions to transitions among monomorphic states are established population-genetic and evolutionary-game ideas.

PAYOFF should claim only that it carries the measurable ecological architecture quantities

```text
L -> R=sL -> phi=R-K
```

into those established stochastic objects and derives the resulting architecture-specific occupancy predictions under the declared model.
