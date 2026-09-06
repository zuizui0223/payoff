# SCH -> BALANCE -> BITA -> PAYOFF topology handoff

This document defines the narrow interface required to turn function-level compromise geometry into a predicted modular coupling topology.

The purpose is to prevent silent relabeling of quantities across repositories.

---

## 1. Input file schema

`PAYOFF/scripts/predict_modular_topology.py` accepts two CSV files.

### `functions.csv`

```text
function_id,optimum,weight
```

Meaning:

```text
function_id
    stable label for one fitness-relevant function;

optimum
    function-specific optimum theta_i on the declared shared coordinate;

weight
    local quadratic fitness curvature a_i>0 on the common fitness scale.
```

### `edges.csv`

```text
source,target,coupling,release_cost
```

Meaning:

```text
source,target
    function ids connected by one reference integration edge;

coupling
    reference quadratic coupling coefficient c_e>=0;

release_cost
    marginal architecture cost k_e>=0 per unit of decoupling d_e.
```

The declared model is

```text
D(x;c)
=sum_i a_i(x_i-theta_i)^2
+sum_e c_e(x_i-x_j)^2.
```

For decoupling `d_e`, current coupling is

```text
c_e=c_e^0-d_e.
```

---

## 2. SCH ownership: function-specific conflict geometry

SCH owns the left-hand functional-conflict geometry.

For topology prediction, the required SCH-side quantities are

```text
theta_i
```

and, when using the local quadratic model,

```text
a_i.
```

### Critical identification rule

SCH's default state-specific optima

```text
z_P*, z_G*, z_C*
```

must **not** automatically be entered as pure function-specific `theta_i`.

The SCH README explicitly distinguishes

```text
state-specific reproductive optima
```

from

```text
pure / component function optima.
```

The topology pipeline may use a SCH optimum as `theta_i` only when one of the following is true:

1. the stricter SCH component-contrast lane identifies a context-stable function-specific optimum;
2. an equivalent independent experiment identifies the function-specific optimum on the same shared coordinate;
3. the analysis is explicitly labeled as a state-specific scenario rather than a pure-function architecture inference.

The same rule applies for more than two functions.

### `weight=a_i`

`weight` is not an arbitrary statistical weight.

It represents the local fitness curvature in

```text
a_i(z-theta_i)^2.
```

If those curvatures are not identified, a sensitivity analysis over plausible weights is valid; a point estimate should not be reported as empirically identified.

---

## 3. BITA ownership: reference differentiated architecture and recoverability

BITA owns the differentiated-coordinate geometry and the idea that relaxing shared constraints can recover compromise loss.

For the edgewise topology layer, BITA-facing inputs are

```text
reference coupling graph E,
reference coupling strengths c_e.
```

These are a finer decomposition of the scalar residual-coupling / recoverability idea used in the two-function bridge.

### Claim boundary

Current BITA theory establishes nested architecture recovery and coupling monotonicity, but a real system does not automatically supply empirically identified edge-specific `c_e` values.

Therefore:

```text
identified c_e
-> empirical topology prediction;

hypothesized / normalized c_e
-> registered mechanistic scenario analysis.
```

Do not describe normalized unit couplings as measured biological coupling strengths.

---

## 4. BALANCE / BITA ownership: architecture cost

The scalar programme uses

```text
K
```

for the extra cost of a differentiated architecture.

The edgewise model requires the finer object

```text
K(d)=sum_e k_e d_e
```

under its linear-cost specialization.

Thus `release_cost=k_e` is **not automatically identified** by a measured total `K`.

Possible lanes are:

### Structural edge-cost lane

Directly manipulate or construct architectures differing by one coupling edge and estimate the matched reproductive/performance cost on the same fitness scale.

### Decomposed-cost lane

Use independently justified architecture accounting to partition a total cost into edge-specific marginal costs.

### Scenario lane

If only total `K` is known, freeze a family of edge-cost allocations satisfying the total cost constraint and report topology sensitivity across that family.

Do not infer a unique `k_e` from total `K` without an additional decomposition assumption.

---

## 5. PAYOFF ownership: topology prediction

Given frozen

```text
theta_i,
a_i,
E,
c_e,
k_e,
```

PAYOFF computes the reference optimized phenotype

```text
x*(c),
```

the exact edge pressures

```text
pressure_e
=(x_i*-x_j*)^2,
```

the local marginal release receipts

```text
pressure_e-k_e,
```

and, for small graphs, every vertex architecture

```text
d_e in {0,c_e^0}.
```

The CLI writes:

```text
edge_pressures.csv
greedy_release_path.csv
vertex_topologies.csv       # when edge count <= enumeration limit
summary.json.
```

---

## 6. What `greedy_release_path` means

The greedy path repeatedly chooses a currently retained edge with positive

```text
(x_i*-x_j*)^2-k_e
```

and fully releases it, then re-optimizes the phenotype.

Because recovery is convex along each release direction under the declared quadratic model, a positive current marginal receipt guarantees that full release of that edge improves the current net payoff.

But the greedy rule is an **accessibility diagnostic**, not a theorem that it always finds the global optimum for arbitrary graphs.

Therefore compare

```text
greedy final topology
```

with

```text
global vertex optimum
```

whenever full enumeration is computationally feasible.

A mismatch is biologically interesting: it identifies an architecture that is globally better but not reachable by the registered local edge-release sequence.

---

## 7. Interpretation of a predicted module

A predicted connected component of retained edges means only:

> Under the declared optima, curvatures, coupling penalties and release costs, retaining those couplings gives greater optimized net payoff than the competing enumerated edge-release topologies.

It does not by itself establish:

```text
genetic independence,
developmental independence,
historical sequence of edge losses,
or a literal anatomical module.
```

Those require separate evidence.

---

## 8. Population handoff after topology generation

For topology `S`, define intrinsic architecture payoff

```text
b_S=R(S)-K(S).
```

Then population ecology is added **after** topology generation.

For pair `S,T`, any symmetric two-strategy interaction can be represented by canonical

```text
phi_ST,
eta_ST.
```

Under the weighted-Hamming topology kernel registered in PAYOFF,

```text
phi_ST=b_T-b_S,
eta_ST=gamma q_ST.
```

This supplies deterministic invasion, finite-population fixation, and rare-mutation occupancy predictions without changing the upstream topology calculation.

---

## 9. Recommended empirical sequence

A strong prospective test is:

```text
SCH
-> identify function-specific theta_i and local curvature a_i

BITA architecture assay
-> identify / freeze reference edges and coupling strengths c_e

BALANCE/BITA cost assay
-> identify / freeze k_e or a preregistered cost-allocation scenario

PAYOFF prediction
-> freeze edge pressures
-> freeze predicted first edge change
-> freeze global topology and accessibility path

new intervention
-> weaken/remove predicted edge
-> re-optimize phenotype
-> test predicted conflict rerouting
-> continue to next edge without refitting earlier parameters.
```

This is stronger than explaining an observed module after seeing it.

---

## 10. Minimal command

The included worked example runs as

```text
python scripts/predict_modular_topology.py \
  --functions examples/three_function/functions.csv \
  --edges examples/three_function/edges.csv \
  --output-dir outputs/three_function_generic
```

Registered expected result:

```text
highest pressure edge: F1-F3
best vertex release bits: 011
module partition: {F1,F2}|{F3}
greedy path reaches the same vertex.
```

---

## 11. Current empirical ceiling

The repository now has an executable handoff, but the existence of the schema does not imply that SCH/BITA/BALANCE have already identified all required `n`-function edge-level inputs.

Current correct status is:

```text
TOPOLOGY_HANDOFF_SCHEMA_READY
N_FUNCTION_TOPOLOGY_PREDICTOR_READY
THREE_FUNCTION_END_TO_END_EXAMPLE_READY
EDGE_SPECIFIC_EMPIRICAL_COUPLINGS_NOT_YET_GENERALLY_IDENTIFIED
EDGE_SPECIFIC_ARCHITECTURE_COSTS_NOT_YET_GENERALLY_IDENTIFIED.
```
