# Topology uncertainty — support for mechanism, endpoint topology, and accessibility

A single modular-topology prediction is not enough when the upstream SCH/BITA/BALANCE quantities are estimated with uncertainty.

PAYOFF therefore transports uncertainty through the topology calculation rather than collapsing

```text
theta_i,
a_i,
c_e,
k_e
```

to one point estimate first.

The registered ensemble runner is

```text
scripts/topology_uncertainty_ensemble.py.
```

It accepts bootstrap/posterior draws under schema

```text
PAYOFF_TOPOLOGY_ENSEMBLE_V1.
```

---

## 1. One draw produces several different topology receipts

For draw `b`, let

```text
S_b^*
```

be the globally best enumerated vertex topology.

PAYOFF also records:

```text
e_pressure,b
    edge with largest reference pressure (x_i*-x_j*)^2;

e_favorable,b
    first edge selected by the registered positive-marginal release rule;

G_b
    final topology reached by the greedy sequential release path;

rho_global,b
    best-minus-runner-up intrinsic topology payoff;

rho_local,b
    smallest local edge-boundary stability margin at S_b^*.
```

These are deliberately not merged into one "topology support" number.

---

## 2. Ensemble support definitions

For `B` draws, define

```text
P_hat_best(S)
= #{b:S_b*=S}/B.
```

This is **global topology support**.

For edge `e`,

```text
P_hat_pressure(e)
= #{b:e_pressure,b=e}/B
```

is **reference conflict-edge support**.

Similarly,

```text
P_hat_favorable(e)
= #{b:e_favorable,b=e}/B
```

is **first accessible edge-release support**.

For the greedy endpoint,

```text
P_hat_greedy(S)
= #{b:G_b=S}/B.
```

Finally,

```text
P_hat_access
= #{b:G_b=S_b*}/B
```

is the fraction of uncertainty draws in which the registered local release path reaches the global vertex optimum.

---

## 3. Mechanism support can exceed final-topology support

There is no theorem requiring

```text
P_hat_pressure
=
P_hat_best.
```

Indeed they answer different questions.

A high

```text
P_hat_pressure(e)
```

means the upstream conflict geometry consistently identifies one coupling edge as carrying the largest marginal constraint.

A lower

```text
P_hat_best(S)
```

means uncertainty in costs, secondary edge pressures, or later conflict rerouting changes the final module partition.

Therefore the scientifically correct conclusion can be:

> The first modularization pressure is robust, while the terminal topology remains uncertain.

This is stronger and more informative than either forcing one final topology or declaring the entire mechanism unsupported.

---

## 4. Global and local reserve summarize different robustness

For each draw,

```text
rho_global
=b_best-b_second.
```

This measures how close the best enumerated topology is to losing its global rank.

At the best vertex, each retained edge has local margin

```text
k_e-pressure_e,
```

and each released edge has local margin

```text
pressure_e-k_e.
```

Define

```text
rho_local
=min_e local edge margin.
```

Then:

```text
rho_global small, rho_local large
```

means a topology is strongly resistant to infinitesimal edge changes once formed, yet has a close distant competitor in global payoff.

Conversely,

```text
rho_local small
```

means the predicted architecture lies close to an edge-release/recoupling boundary even if no distant topology is globally competitive.

The ensemble reports mean and minimum global reserve plus mean local reserve so support frequency is not interpreted without payoff depth.

---

## 5. Registered synthetic three-function receipt

The file

```text
examples/three_function/ensemble.json
```

contains five deliberately perturbed draws around the worked example.

The registered regression result is

```text
first pressure edge F1-F3:       5/5
first favorable edge F1-F3:      5/5
best topology 011:                4/5
best topology 111:                1/5
greedy final topology 011:        5/5
greedy path reaches global best:  4/5.
```

So the synthetic conclusion is:

```text
mechanistic first-edge prediction   very robust
sequential local endpoint           very robust
unique global endpoint              less robust.
```

In the one draw where full release `111` is globally best, the registered greedy local path still stops at `011`. This is a direct example of uncertainty exposing an accessibility/global-optimum mismatch rather than hiding it.

The fixture is a software/theory regression only, not an empirical biological result.

---

## 6. No universal support cutoff is imposed

PAYOFF does not define

```text
0.8 = supported
```

or any other universal probability cutoff.

Interpretation should report the receipts directly, for example:

```text
first-edge support = 0.94,
best-topology support = 0.71,
greedy/global agreement = 0.66,
minimum global reserve = ...
```

and combine them with preregistered scientific decision rules when a binary decision is required.

This avoids converting continuous uncertainty into an arbitrary significance-style topology label.

---

## 7. Preferred empirical workflow

For each bootstrap/posterior draw on the same locked context and fitness scale:

```text
SCH
-> theta_i^(b), a_i^(b)

BITA / architecture assay
-> c_e^(b)

BALANCE / BITA cost assay
-> k_e^(b)

PAYOFF
-> pressure edge
-> first favorable edge
-> global vertex topology
-> greedy path
-> local/global reserves.
```

The ordering of functions and edges must remain identical across draws so topology bits retain one meaning.

---

## 8. What uncertainty propagation does not fix

Bootstrap support cannot rescue an unidentified estimand.

In particular:

```text
state-specific SCH optima
!= automatically function-specific theta_i;

total architecture cost K
!= automatically edge-specific k_e;

normalized coupling c_e
!= measured integration strength.
```

If these inputs are scenario assumptions rather than identified quantities, the ensemble is a **scenario uncertainty analysis**, not an empirical posterior over true biological topologies.

See

```text
docs/SCH_BITA_BALANCE_TOPOLOGY_HANDOFF.md.
```

---

## 9. Claim boundary

Appropriate:

> Across the registered parameter draws, the F1-F3 edge was the first predicted conflict-release target in all draws, whereas the final global topology was 011 in four of five draws.

Avoid:

> The organism has an 80% probability of possessing topology 011.

The ensemble support is conditional on the declared model, input-identification lane, and uncertainty distribution supplied to PAYOFF.
