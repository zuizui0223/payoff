# PAYOFF -> TTF spatial-projection bridge

Status: empirical/mechanistic bridge. This file links the individual-system interpretation developed for *Campanula microdonta* to the cross-species spatial-transfer target in TTF (Transferable Turnover Fields). It does **not** change the canonical PAYOFF theorems, and it does **not** turn a TTF transfer result into proof of a shared causal mechanism.

## 1. Position in the programme

The intended hierarchy is:

```text
functional conflict / module-specific ecology
                |
                v
             PAYOFF
      local architecture payoff
                |
                v
individual-system anchor
Campanula microdonta / Izu islands
                |
                v
       spatial projection
x -> ecological context -> local payoff margin
                |
                v
              TTF
cross-species transfer of within-species turnover
```

The *Campanula* system supplies biological semantics, direction, history and eventual direct payoff assays for one well-resolved system. TTF asks a different question: whether a transition structure learned from some species predicts strong within-species trait transitions in entirely unseen species.

The two layers should therefore be connected by a **projection contract**, not collapsed into one inference.

---

## 2. Local PAYOFF object

For a species `s`, ecological context `e`, architecture pair `S,D`, and local frequency `p`, define the canonical local margin

```text
M_s(e,p)
= pi_D - pi_S
= phi_s(e) + eta_s(e)(2p-1).
```

With an upstream SCH/BALANCE/BITA receipt,

```text
phi_s(e)=R_s(e)-K_s(e)
        =s_s(e)L_s(e)-K_s(e).
```

Interpretation:

```text
M_s>0   D is locally favored against the specified resident context;
M_s=0   local architecture boundary;
M_s<0   S is locally favored.
```

When frequency dependence has not been identified, use the weaker static object

```text
M_s^0(e)=phi_s(e)
```

and label the projection explicitly as static/pre-game.

---

## 3. Projecting the local margin into geographic space

Let location `x` determine a species-specific ecological context

```text
e_s(x)
```

through pollinator environment, mating environment, resources, climate, connectivity, or another prospectively declared driver set.

The latent spatial payoff field is

```text
m_s(x)
= M_s(e_s(x),p_s(x)).
```

or, before frequency dependence is identified,

```text
m_s^0(x)=phi_s(e_s(x)).
```

Define the species-specific latent payoff-transition set

```text
B_s^P={x : m_s(x)=0}.
```

This is a **mechanism-side boundary**. It is not the same object as the empirical TTF boundary field learned from observed trait turnover.

A trait can show little turnover across `B_s^P` if architecture cannot respond, if history prevents the transition, if gene flow overwhelms local sorting, or if the proposed trait is not the relevant architecture coordinate.

Conversely, observed turnover can occur away from `B_s^P` for neutral history, unmeasured ecology, or another mechanism.

---

## 4. From a payoff field to an edge-level TTF predictor

TTF scores within-species edges. For an edge `e` with geographic path length `L_e`, a prospectively fixed mechanism-exposure feature can be constructed from the payoff field, for example

```text
P_se
= (1/L_e) integral_e g[m_s(x)] dl,
```

where `g` is fixed before evaluation-trait inspection.

Examples include

```text
g(m)=exp(-|m|/tau)
```

or

```text
g(m)=1{|m|<=epsilon}.
```

The exact transform is not theoretically privileged. It is a measurement choice that must be calibrated and frozen.

The crucial rule is:

> Evaluation-species trait outcomes may not be used to tune `m_s`, `tau`, `epsilon`, the driver weights, or any other PAYOFF-derived predictor that is later scored on those same species.

Mechanism predictors can be fixed from prior biology, fitted only on training species, or cross-fitted prospectively.

---

## 5. TTF does two different jobs

### 5.1 Core TTF sharedness

The canonical TTF statistic remains

```text
C_s=Spearman(b_hat_se,u_se),
T=mean_s C_s,
```

where the boundary field is learned from training-species trait turnover and evaluated on species-disjoint held-out species.

This asks:

> Is turnover geometry transferable across species?

### 5.2 PAYOFF-informed predictor competition

TTF's generic held-out predictor-space layer can additionally compare a PAYOFF-derived mechanism space `P` against geography/environment baselines on the same held-out species.

Recommended spaces include

```text
G      geography / intrinsic spatial structure
E      environmental contrast
GE     geography + environment
P      PAYOFF-derived mechanism exposure
GEP    geography + environment + PAYOFF exposure
```

with paired increments such as

```text
Delta_P|GE = T_GEP - T_GE
Delta_GE|P = T_GEP - T_P.
```

A positive `Delta_P|GE` means the preregistered PAYOFF projection adds held-out turnover prediction beyond the declared geography/environment baseline.

It does not by itself prove that all held-out species share the same biological mechanism.

---

## 6. Campanula as the individual-system anchor

The Izu-island *Campanula microdonta* system is assigned the **individual-system anchor** role.

It is useful because one species can be resolved deeply across populations, modules and evolutionary history:

```text
visual-information module
    floral-tube purple spots / candidate nectar guide

mechanical-access module
    flower size, throat and opening geometry

reproductive-interface module
    reproductive-organ geometry / mating-assurance traits
```

The current project can test whether these modules share one size/investment trajectory or partially disassemble, and whether repeated low-spot states occur on distinct neutral genetic backgrounds.

The later direct-PAYOFF stage can estimate reproductive payoff for guide-rich versus guide-reduced architectures and, with frequency manipulation, identify

```text
phi and eta.
```

Thus *Campanula* contributes what TTF intentionally does not provide on its own:

```text
biological direction;
module identity;
functional interpretation;
colonization / population-history control;
and eventually direct payoff identification.
```

The eight Izu populations are **not eight held-out species** for the canonical TTF superpopulation claim. They are repeated populations inside one mechanistic anchor species.

---

## 7. TTF as the spatial-projection layer

TTF is assigned the **cross-species spatial projection** role.

Once a trait-agnostic transition measure is available across many species, TTF can ask whether the location/structure of strong within-species change is reproducible in unseen species.

The projection chain is

```text
individual-system mechanism
        |
        v
local payoff margin M_s
        |
        v
spatial payoff field m_s(x)
        |
        v
predicted transition exposure P_se
        |
        +--------------------------+
        |                          |
        v                          v
PAYOFF-informed TTF          canonical TTF field
predictor competition       cross-species sharedness
        |                          |
        +------------+-------------+
                     v
       cross-species spatial support
```

The two TTF lanes answer complementary questions:

```text
canonical field:
    does turnover transfer at all?

PAYOFF-informed P space:
    does the mechanistic projection add transfer skill?
```

---

## 8. Mapping TTF synthetic axes to PAYOFF language

TTF qualification separates

```text
shared fraction pi
```

from

```text
within-species turnover amplitude A.
```

The PAYOFF bridge gives these axes a useful but deliberately non-identical interpretation.

### Shared fraction `pi`

A high synthetic `pi` is analogous to a high fraction of species whose latent transition sets `B_s^P` are spatially aligned closely enough to create transferable turnover geometry.

It is **not** automatically the fraction of species sharing the same causal mechanism.

### Amplitude `A`

A high synthetic `A` is analogous to strong observable trait turnover conditional on crossing the relevant transition region.

It is **not** equal to `|phi|`, `|eta|`, or the gradient of the payoff field. Observable amplitude can also depend on developmental response, standing variation, history and measurement scale.

This distinction preserves the original TTF adversarial null:

```text
pi=0, A>0
```

which corresponds to strong private within-species transitions with no transferable boundary geometry.

---

## 9. Four-stage empirical programme

### Stage A — individual-system anchor

Use *C. microdonta* to establish whether syndrome disassembly is real rather than a one-axis size reduction or neutral-lineage artifact.

### Stage B — mechanism projection

Construct a prospectively frozen spatial payoff proxy from ecological drivers and, when available, directly identified PAYOFF parameters.

### Stage C — TTF transfer

Use species-disjoint TTF to test both generic turnover sharedness and incremental prediction from the PAYOFF-derived space.

### Stage D — syndrome synthesis

Only after A-C are separately supported ask whether pollination, selfing or island syndromes are better described as recurrent assembly/disassembly around shared payoff transitions.

---

## 10. Direction is a separate layer

Canonical TTF uses within-species dissimilarity rank and therefore identifies **where strong turnover occurs**, not which side evolves which phenotype.

For example, the same TTF boundary can be compatible with

```text
species A: guide-rich -> guide-reduced
species B: guide-reduced -> guide-rich.
```

A syndrome-direction claim therefore requires a separate signed layer tied to a declared trait orientation or architecture endpoint.

The recommended hierarchy is

```text
TTF: where does turnover recur?
        |
        v
signed endpoint layer: which direction does it move?
        |
        v
PAYOFF / individual anchors: why is that direction favored?
```

Do not infer syndrome direction from unsigned TTF sharedness alone.

---

## 11. Falsification cases

The bridge is challenged if any of the following occurs:

```text
Campanula modules reduce to one common allometric axis;

an independently constructed payoff field does not predict turnover even in the anchor system;

canonical TTF sharedness is positive but PAYOFF-informed P adds no held-out skill beyond GE;

PAYOFF-informed P appears predictive only after evaluation-trait tuning;

held-out species show transferable turnover but inconsistent signed direction where a common syndrome direction was claimed;

or a direct payoff assay contradicts the sign of the projected margin.
```

These failures distinguish different possibilities rather than being pooled into one negative result.

---

## 12. Claim ceiling

A strong combined result could support:

> A mechanism-derived architecture-payoff projection, biologically anchored in a deeply resolved individual system, predicts where entirely unseen species undergo strong within-species trait turnover beyond declared geographic/environmental baselines.

It would still not by itself prove:

```text
a universal island-syndrome mechanism;
identical causal pathways in all species;
trait-direction agreement;
or direct estimation of PAYOFF phi/eta in species without payoff data.
```

Those require their own receipts.

---

## 13. Repository handoff

Individual-system anchor:

- [`CAMPANULA_SYNDROME_DISASSEMBLY_HANDOFF.md`](CAMPANULA_SYNDROME_DISASSEMBLY_HANDOFF.md)

PAYOFF spatial layer:

- [`ENVIRONMENT_MOSAIC_HANDOFF.md`](ENVIRONMENT_MOSAIC_HANDOFF.md)
- [`../theory/ENVIRONMENT_MOSAIC_SOURCE_SINK.md`](../theory/ENVIRONMENT_MOSAIC_SOURCE_SINK.md)

TTF cross-species implementation:

- `zuizui0223/TTF/docs/PAYOFF_SPATIAL_PROJECTION_HANDOFF.md`
- `zuizui0223/TTF/docs/METHOD_SPEC.md`

This bridge is part of the empirical handoff layer, not the canonical theorem spine.