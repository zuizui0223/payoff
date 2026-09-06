# Finite-population PAYOFF game

This note extends the deterministic PAYOFF architecture game to a finite, well-mixed population under a frequency-dependent Moran process.

The deterministic game has shared architecture `S`, differentiated architecture `D`, and symmetric payoff matrix

```text
          S          D
S         0       phi-eta
D      phi-eta      2phi
```

with

```text
phi = sL-K.
```

`eta` is the frequency-feedback coefficient. In an infinite population with differentiated frequency `p`,

```text
Delta(p)=pi_D-pi_S=phi+eta(2p-1).
```

The finite-population layer asks a different question:

> Starting from a small number of architecture mutants, what is the probability that drift plus selection carries them to fixation?

The finite-population results below do not replace the deterministic phase diagram. They quantify stochastic invasion and fixation around it.

---

## 1. Self-excluding finite-population payoff gap

Let population size be `N>=2` and let `i` be the number of `D` individuals, `1<=i<=N-1`. Random pairwise interactions exclude self-interaction.

The expected payoffs are

```text
pi_D(i)
= [2phi(i-1) + (phi-eta)(N-i)]/(N-1),

pi_S(i)
= [(phi-eta)i]/(N-1).
```

Therefore

```text
Delta_N(i)
= pi_D(i)-pi_S(i)
= [phi(N-2)+eta(2i-N)]/(N-1).
```

For `i/N -> p` and `N -> infinity`,

```text
Delta_N(i) -> phi+eta(2p-1)=Delta(p).
```

Thus the finite game converges to the deterministic PAYOFF game, with an explicit self-interaction correction at finite `N`.

---

## 2. Moran process with exponential payoff-to-fitness mapping

Use positive Malthusian fitness

```text
f_D(i)=exp(beta pi_D(i)),
f_S(i)=exp(beta pi_S(i)),
```

where `beta>=0` is selection intensity.

For the birth-death Moran process,

```text
T_i^+
= [i f_D /(i f_D+(N-i)f_S)] [(N-i)/N],

T_i^-
= [(N-i) f_S /(i f_D+(N-i)f_S)] [i/N].
```

The transition ratio simplifies exactly to

```text
T_i^-/T_i^+
= f_S/f_D
= exp[-beta Delta_N(i)].
```

This exponential mapping is used because it remains positive for arbitrary payoff values and yields an exact algebraic fixation expression.

---

## 3. Exact fixation probability of one differentiated mutant

Let `rho_D` be the probability that one `D` mutant introduced into `N-1` residents of type `S` reaches fixation.

For any birth-death chain,

```text
rho_D
= [1 + sum_{k=1}^{N-1} prod_{j=1}^k (T_j^-/T_j^+)]^(-1).
```

Using the exponential transition ratio,

```text
rho_D
= [sum_{k=0}^{N-1} exp(-beta C_k)]^(-1),
```

where

```text
C_0=0,
C_k=sum_{j=1}^k Delta_N(j).
```

Because `Delta_N(j)` is affine in `j`, the cumulative payoff difference has the closed form

```text
C_k
= k[phi(N-2)+eta(k+1-N)]/(N-1).
```

Hence

```text
rho_D
= {sum_{k=0}^{N-1}
    exp[-beta k{phi(N-2)+eta(k+1-N)}/(N-1)]}^(-1).
```

This is exact for the declared finite-population model.

By swapping the labels `S` and `D`, the same parameterization becomes `phi -> -phi` with unchanged `eta`. Therefore

```text
rho_S(N,phi,eta,beta)
= rho_D(N,-phi,eta,beta).
```

---

## 4. Exact relative-fixation theorem

The ratio of reciprocal single-mutant fixation probabilities is

```text
rho_D/rho_S
= prod_{i=1}^{N-1} (T_i^+/T_i^-)
= exp[beta sum_{i=1}^{N-1} Delta_N(i)].
```

The frequency-feedback term cancels in the full sum:

```text
sum_{i=1}^{N-1} Delta_N(i)
= phi(N-2).
```

Therefore

```text
rho_D/rho_S
= exp[beta phi(N-2)].
```

For `N>2` and `beta>0`,

```text
rho_D > rho_S  iff  phi>0,
rho_D = rho_S  iff  phi=0,
rho_D < rho_S  iff  phi<0.
```

Substituting the ecological architecture bridge,

```text
phi=sL-K,
```

we obtain

```text
rho_D > rho_S  iff  sL>K.
```

Thus the static SCH/BALANCE/BITA crossing `phi=0` survives finite-population stochasticity as the exact reciprocal-fixation ordering boundary under the declared exponential Moran model, even though absolute fixation probabilities depend on `eta`, `N`, and `beta`.

This does **not** mean that `eta` is irrelevant. `eta` strongly changes whether either mutant is more likely than neutral to fix. It cancels only from the ratio `rho_D/rho_S`.

---

## 5. Weak-selection single-mutant advantage

A neutral single mutant fixes with probability

```text
rho_neutral=1/N.
```

Expand `rho_D` around `beta=0`. Write

```text
rho_D(beta)
= [sum_{k=0}^{N-1} exp(-beta C_k)]^(-1).
```

At neutrality,

```text
rho_D(0)=1/N.
```

The first derivative has the sign of

```text
sum_{k=1}^{N-1} C_k
= sum_{j=1}^{N-1}(N-j)Delta_N(j).
```

Direct summation gives, for `N>2`,

```text
sum_{j=1}^{N-1}(N-j)Delta_N(j)
= N(N-2)(3phi-eta)/6.
```

Therefore, to first order in weak selection,

```text
rho_D > 1/N  iff  3phi>eta.
```

Using `phi=sL-K`,

```text
rho_D > 1/N  iff  3(sL-K)>eta,
```

or equivalently

```text
K < sL-eta/3.
```

For a single `S` mutant in a `D` population, swap `phi -> -phi`:

```text
rho_S > 1/N  iff  -3phi>eta,
```

or

```text
K > sL+eta/3.
```

These are weak-selection fixation-advantage boundaries. They lie between the deterministic reciprocal invasion boundaries

```text
K=sL-eta
and
K=sL+eta
```

when `eta>0`, and reverse ordering when `eta<0`.

---

## 6. One-third law as an architecture threshold

The one-third law is established prior theory in finite-population evolutionary games. PAYOFF does not claim it as new.

In the coordination regime `eta>0`, the deterministic unstable threshold is

```text
p*=(1-phi/eta)/2.
```

Then

```text
3phi>eta
iff
p*<1/3.
```

So the standard one-third law becomes, for this architecture game,

```text
single D is favored over neutral drift
iff
p*<1/3
iff
3(sL-K)>eta.
```

The contribution of PAYOFF is the substitution chain

```text
measured compromise load L
-> dimensional recovery sL
-> architecture gap phi=sL-K
-> finite-population fixation criterion.
```

The law itself is not novel.

Prior-art anchor:

- Ohtsuki, Bordalo & Nowak (2007), *The one-third law of evolutionary dynamics*, Journal of Theoretical Biology 249:289-295, PMID 17826798.

---

## 7. Finite-population refinement of the four deterministic phases

Define the weak-selection mutant-advantage tests

```text
D_adv: 3phi>eta,
S_adv: -3phi>eta.
```

Then:

### Strong negative frequency dependence

If

```text
eta < -3|phi|,
```

both single mutants are favored relative to neutrality:

```text
rho_D>1/N
and
rho_S>1/N
```

under weak selection.

This is the strongest stochastic signature of a coexistence-promoting game.

### Strong positive frequency dependence

If

```text
eta > 3|phi|,
```

neither single mutant is favored relative to neutrality:

```text
rho_D<1/N
and
rho_S<1/N.
```

This defines a stochastic coordination core: either pure state can be locally stable in deterministic dynamics, while a lone mutant of either architecture is selected against strongly enough that fixation probability falls below neutral drift.

### Intermediate region

For

```text
-3|phi| < eta < 3|phi|,
```

exactly one reciprocal single mutant is favored under weak selection, with the favored direction determined by the sign of `phi` away from equality surfaces.

---

## 8. Nested cost surfaces

Let

```text
R=sL.
```

The deterministic reciprocal invasion surfaces are

```text
K_D,invasion = R-eta,
K_S,invasion = R+eta.
```

The weak-selection fixation-advantage surfaces are

```text
K_D,fix = R-eta/3,
K_S,fix = R+eta/3.
```

Thus frequency feedback creates two nested scales:

```text
full deterministic interaction band width = 2|eta|,
weak-selection stochastic core width      = 2|eta|/3.
```

For `eta>0`, the central interval

```text
R-eta/3 < K < R+eta/3
```

has neither single mutant favored above neutral drift.

For `eta<0`, the same ordered interval

```text
R-|eta|/3 < K < R+|eta|/3
```

has both reciprocal single mutants favored above neutral drift.

---

## 9. Interpretation

The finite-population extension separates three increasingly strict questions:

```text
1. Static architecture advantage
   phi=sL-K.

2. Deterministic rare-type invasion
   Delta(0)=phi-eta,
   -Delta(1)=-phi-eta.

3. Stochastic single-mutant advantage
   rho_D>1/N or rho_S>1/N.
```

They are not equivalent.

In particular, a differentiated architecture can have `phi>0` and therefore a larger reciprocal fixation probability than `S`, while still having `rho_D<1/N` if positive frequency dependence is sufficiently strong. Conversely, under sufficiently negative frequency dependence, both architecture mutants can have fixation probabilities above neutrality even though only one can have the larger reciprocal fixation probability.

This is the finite-population version of PAYOFF's central distinction:

> architecture quality, invasion when rare, and stochastic fixation are different estimands.
