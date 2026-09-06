# SCH -> BALANCE -> BITA -> PAYOFF finite-population handoff

This note freezes the minimum inputs required to carry the sister-repository programme from ecological compromise to finite-population stochastic predictions.

## 1. Input ownership

### SCH supplies ecological conflict

Required receipt:

```text
L >= 0
```

on a common reproductive-fitness scale, with the underlying compromise geometry and identification level stated explicitly.

PAYOFF does not relax SCH's distinction between state-specific and stricter pure-function optima.

### BITA supplies dimensional release

Required receipt:

```text
s in [0,1]
```

or an independently measured recovery

```text
R.
```

Under the declared quadratic bridge,

```text
R=sL.
```

### BALANCE/BITA supply architecture comparison

Required receipt:

```text
K >= 0
```

when a structural architecture cost can be identified, or a direct optimized worldline gap

```text
phi=WD*-WS*.
```

Under the bridge,

```text
phi=R-K=sL-K.
```

### PAYOFF supplies population feedback

Required population-game receipt:

```text
eta
```

from frequency-dependent relative fitness. Preferred direct identification uses reciprocal endpoint contrasts

```text
Delta0=Delta(0)
Delta1=Delta(1)
```

with

```text
phi=(Delta0+Delta1)/2
eta=(Delta1-Delta0)/2.
```

This creates an internal bridge check against the independently reconstructed `phi=sL-K`.

---

## 2. Deterministic prediction layer

Given `phi` and `eta`, PAYOFF predicts

```text
shared dominance
stable coexistence
coordination bistability
differentiated dominance
```

from the sign geometry of

```text
Delta(p)=phi+eta(2p-1).
```

The reciprocal rare-type boundaries are

```text
phi=eta
phi=-eta.
```

In architecture-cost form,

```text
K=R-eta
K=R+eta.
```

---

## 3. Finite-population input layer

To move beyond deterministic dynamics, PAYOFF additionally requires:

```text
N      effective population size for the modeled architecture competition
beta   payoff-to-fitness selection intensity
```

The current exact implementation assumes:

```text
well-mixed fixed N
pairwise random interaction
no self-interaction
Moran birth-death updating
exponential fitness f=exp(beta*pi)
```

These assumptions must be stated with every finite-population receipt.

---

## 4. Finite-population predictions

Given

```text
L,s,K,eta,N,beta,
```

compute

```text
R=sL
phi=R-K.
```

Then PAYOFF predicts:

```text
rho_D     fixation probability of one D mutant
rho_S     fixation probability of one S mutant
rho_i     fixation probability from i initial D individuals
m50       minimum initial D count for >=50% fixation
m90       minimum initial D count for >=90% fixation
i0        finite-population zero-drift count when eta!=0.
```

The exact reciprocal fixation ordering under the declared exponential Moran process is

```text
rho_D/rho_S=exp[beta phi(N-2)].
```

Thus

```text
phi>0 -> rho_D>rho_S
phi<0 -> rho_D<rho_S
```

for `N>2`, `beta>0`.

---

## 5. Four non-equivalent empirical questions

The programme should report these separately.

### Q1 — Is there functional conflict?

```text
L>0 ?
```

Owned by SCH.

### Q2 — Which architecture has higher optimized frequency-independent fitness?

```text
phi=sL-K
```

Owned by the SCH/BALANCE/BITA bridge.

### Q3 — Can an architecture invade when rare?

```text
D rare: phi>eta
S rare: -phi>eta.
```

Owned by PAYOFF's deterministic population layer.

### Q4 — Is a single mutant favored above neutral drift?

Under weak selection in the declared finite game:

```text
D: 3phi>eta
S: -3phi>eta.
```

This is a stochastic fixation criterion, not the same estimand as rare deterministic growth.

---

## 6. Three-barrier architecture experiment

For `eta>0`, a particularly informative experiment varies effective architecture cost or another axis that monotonically changes `phi=R-K` while holding the frequency-feedback regime approximately fixed.

The D-side thresholds are

```text
K=R          reciprocal fixation ordering changes
K=R-eta/3    single-D fixation crosses neutral 1/N under weak selection
K=R-eta      single-D local growth changes sign.
```

The mirror S-side thresholds are

```text
K=R
K=R+eta/3
K=R+eta.
```

Recovering even two of these layers would distinguish static advantage, stochastic advantage, and local invasion.

---

## 7. Release-curve validation

The strongest finite-population validation is not one fixation comparison but a release curve.

Manipulate or initialize multiple D counts

```text
i=1,2,...
```

and estimate

```text
Pr(D fixes | initial D=i).
```

Compare to the predicted

```text
rho_i
= [sum_{k=0}^{i-1} exp(-beta C_k)]
  /[sum_{k=0}^{N-1} exp(-beta C_k)].
```

A successful out-of-sample test would use `L,s,K,eta,N,beta` estimated from separate components, then predict the entire `i -> rho_i` curve without refitting each initial condition.

That would be a much stronger cross-scale receipt than merely observing one architecture replace the other.

---

## 8. Current empirical ceiling

At present, the sister repositories can motivate or estimate parts of

```text
L,s,K,phi.
```

The following PAYOFF-specific quantities are not yet established empirically in the programme:

```text
eta
beta
a matched effective N for architecture competition
rho_i release curves.
```

Therefore current finite-population results are theory and experimental-design predictions, not empirical demonstrations in the focal biological systems.
