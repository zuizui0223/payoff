# Three-function topology example — transport from modular architecture to population dynamics

This note continues `THREE_FUNCTION_TOPOLOGY_EXAMPLE.md` into the population layer.

The topology calculation itself produced eight discrete vertex architectures. Here those topology payoffs are inserted into the canonical PAYOFF game without refitting the intrinsic architecture geometry.

---

## 1. Intrinsic topology payoffs at edge cost `k=0.4`

The globally best topology is

```text
M = 011
```

in release-bit order `(01,02,12)`, meaning

```text
retained edge 01,
released edges 02 and 12,
module partition {0,1}|{2}.
```

Its intrinsic payoff relative to the fully coupled reference is

```text
b_M=71/30.
```

The fully released topology is

```text
F = 111
```

with

```text
b_F=23/10.
```

Therefore

```text
b_F-b_M
=23/10-71/30
=-1/15.
```

So full differentiation is intrinsically slightly worse than the two-module architecture.

---

## 2. Add topology-distance frequency feedback

Use the topology-game kernel

```text
H(S,T)=-gamma q(S,T),
```

where `q` is unweighted Hamming distance between release vectors.

Take

```text
gamma=-1/4.
```

Negative `gamma` rewards unlike topologies and therefore acts as negative frequency dependence.

The module and full-release states differ at only edge `01`, so

```text
q(M,F)=1.
```

By `TOPOLOGY_PAYOFF_GAME.md`, the pair reduces exactly to canonical PAYOFF coordinates

```text
phi_MF
=b_F-b_M
=-1/15,

eta_MF
=gamma q
=-1/4.
```

Because

```text
|phi_MF|=1/15 < 1/4=|eta_MF|
```

and `eta<0`, the pair lies in the stable-coexistence wedge.

---

## Theorem P1 — exact module/full-release coexistence frequency

Let `p_F` be full-release frequency in the `M` versus `F` subgame.

The canonical interior equilibrium is

```text
p_F*
=(1-phi/eta)/2.
```

Substituting

```text
phi=-1/15,
eta=-1/4
```

gives

```text
phi/eta=4/15
```

and therefore

```text
p_F*
=(1-4/15)/2
=11/30.
```

Thus the predicted deterministic composition is

```text
full release F: 11/30,
two-module M:  19/30.
```

The intrinsic optimum remains the majority architecture, but negative topology-frequency feedback maintains the nearby fully differentiated state.

---

## 3. Reciprocal invasion margins

Rare full release invading the module population has margin

```text
I_F
=phi-eta
=-1/15+1/4
=11/60>0.
```

Rare module architecture invading full release has margin

```text
I_M
=-phi-eta
=1/15+1/4
=19/60>0.
```

Both invade when rare, but the module state has the stronger reciprocal invasion margin.

---

## 4. The other six topology states are excluded by the best module

At `gamma=-1/4`, compare every other vertex topology against `M=011`.

Only `F=111` satisfies reciprocal invasion.

All other six states have intrinsic payoff deficits too large for the topology-distance reward to overcome. Against each of them,

```text
M invades,
competitor does not invade M.
```

Thus the eight-state topology landscape simplifies dynamically to one dominant two-state polymorphism around the top of the intrinsic architecture landscape:

```text
M=011  <---->  F=111.
```

This is a concrete example of population ecology maintaining an architecture that is not the intrinsic optimum, but only when it lies sufficiently close in intrinsic payoff and sufficiently far in frequency-dependent interaction space.

---

## 5. Finite-population transport

Take

```text
N=20,
beta=0.4
```

with the registered exponential-fitness Moran process.

The reciprocal fixation ratio is exact:

```text
rho_F/rho_M
=exp[beta(N-2)phi]
=exp[-0.48]
~=0.618783.
```

So the module architecture is still favored in reciprocal fixation ordering.

However, the weak-selection single-mutant scores are

```text
3phi-eta
=-1/5+1/4
=1/20>0,

-3phi-eta
=1/5+1/4
=9/20>0.
```

Thus both mutant directions are above the weak-selection neutral criterion.

The exact Moran calculation at `N=20,beta=0.4` also gives both single-mutant fixation probabilities above `1/N`, while retaining

```text
rho_M>rho_F.
```

This separates three statements:

```text
both architectures can invade when rare,
both single mutants can be favored above neutrality,
but the module architecture still has larger reciprocal fixation probability.
```

---

## 6. Symmetric rare topology mutation

Now allow symmetric rare single-edge topology mutation among all eight vertex states.

For the registered exponential Moran substitution process,

```text
Pi(S)
propto exp[beta(N-2)b_S].
```

The topology-distance interaction does not enter these monomorphic stationary weights under the symmetric rare-mutation theorem.

At

```text
N=20,
beta=0.4,
```

the two top states carry essentially all stationary mass:

```text
Pi(M) ~= 0.61746,
Pi(F) ~= 0.38207,
Pi(M)+Pi(F) > 0.999.
```

Their ratio is exact:

```text
Pi(M)/Pi(F)
=exp[beta(N-2)(b_M-b_F)]
=exp(0.48).
```

Thus negative topology-frequency feedback strongly changes deterministic coexistence and substitution kinetics, but symmetric weak-mutation monomorphic occupancy is still ordered by intrinsic topology payoff.

---

## 7. Accessibility and stationary abundance are different

At `k=0.4`, the intrinsic optimum `M=011` is reachable from the reference `000` by the monotonic single-edge path

```text
000 -> 010 -> 011.
```

So this specific example has no intrinsic single-edge fitness valley at the registered cost.

But `THREE_FUNCTION_ACCESSIBILITY_REGIMES.md` shows that increasing the same edge cost into

```text
9/8 < k < 19/12
```

leaves `M=011` as the global intrinsic optimum while making the reference a strict one-edge local optimum.

Therefore the same final topology can have:

```text
high stationary weight
```

but very different

```text
evolutionary accessibility
```

depending on edge cost and mutation step size.

---

## 8. Full end-to-end transport

The worked example now closes the entire chain:

```text
function optima
    theta=(0,1,3)
        |
        v
reference optimized phenotype
    x=(1,5/4,7/4)
        |
        v
edge pressures
    1/16, 9/16, 1/4
        |
        v
sequential release
    02 then 12
        |
        v
intrinsic module topology
    M=011={0,1}|{2}
    b_M=71/30
        |
        v
topology game
    phi=-1/15
    eta=-1/4 against F=111
        |
        v
stable coexistence
    p_F*=11/30
        |
        v
finite Moran / rare mutation
    reciprocal fixation ordering
    + long-run topology occupancy.
```

No population parameter is used to choose the intrinsic module topology. The architecture is generated first from function-level conflict and edge costs, then transported into the population game.

---

## 9. Biological interpretation

The example demonstrates three distinct biological filters:

```text
within-organism optimization
-> which couplings carry conflict;

architecture cost
-> which modular topology is intrinsically best;

ecology and population process
-> whether nearby alternative topologies coexist, fix, or persist long-term.
```

That separation is the main purpose of the PAYOFF transport architecture.

---

## 10. Claim boundary

The numerical values in this note belong to one deliberately transparent three-function example. They are not empirical estimates and are not universal constants.

The theorem-level claim is narrower:

> Once a modular topology is generated from explicit function-level conflict and architecture costs, its intrinsic payoff and graph distance can be transported without refitting into the same canonical invasion, fixation, and rare-mutation machinery used for the original shared-versus-differentiated PAYOFF game.
