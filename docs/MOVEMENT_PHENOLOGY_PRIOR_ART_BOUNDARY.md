# Movement–phenology controller prior-art boundary

Status: literature boundary for the PAYOFF-B macro extension. This file is intentionally conservative.

## Established ideas that are not new

### Green-wave surfing / forage maturation

A substantial literature already shows that migratory herbivores and birds can track spatially propagating seasonal resources.

PAYOFF-B should not claim that animals can follow green-up, that migration can extend access to high-quality forage, or that phenology can shape movement as new concepts.

### Surfing versus jumping

Bischof et al. (2012) already distinguish continuous green-wave surfing from rapid relocation ("jumping") in red deer.

PAYOFF-B should not claim the SURF/JUMP distinction itself as novel.

### Greenscape controls surfing performance

Aikens et al. (2017) show that the order, rate, and duration of green-up along routes explain individual variation in mule-deer surfing better than simple individual traits.

PAYOFF-B should not claim that route-scale phenology geometry influences tracking as new.

### Predictability and stopover timing

Kölzsch et al. (2015) show that barnacle-goose arrival relative to spring is associated with environmental predictability among stopover sites.

PAYOFF-B should not claim that predictable phenology permits closer migration timing as new.

### Migration-distance effects on phenological tracking

van Toor et al. (2021) show that Eurasian wigeons migrating farther east/north arrive progressively closer to local spring phenology.

PAYOFF-B should not claim that migration distance alters tracking strategy as new.

### Compensatory plasticity during migration

Ortega et al. (2023) show that mule deer starting migration mismatched with green-up adjust movement rate and stopover behavior and arrive much closer to peak forage timing.

PAYOFF-B should not claim discovery of en-route compensation itself.

### Behavioral reaction norms

Laforge et al. (2025) quantify consistent individual differences and plasticity in spring migration timing across three North American ungulate species. Arrival timing, but not departure timing, is plastic to green-up timing, and the authors infer that herbivores can synchronize migration by adjusting migration pace.

PAYOFF-B should not claim migration-timing plasticity, among-individual reaction-norm variation, or pace adjustment as new.

### Anthropogenic decoupling

Aikens et al. (2022) show that energy development can cause mule deer to hold up and become decoupled from the green wave.

PAYOFF-B should not claim that infrastructure can disrupt green-wave surfing as new.

### Resource engineering

Geremia et al. (2019) show that Yellowstone bison can modify vegetation phenology through grazing.

PAYOFF-B should not claim that the resource wave is always exogenous or that animal feedback on vegetation is newly recognized.

### Control theory in migration broadly

Control-theoretic and optimal-control formulations exist for migration, movement, and conservation. Generic statements that a monotone negative-feedback law stabilizes a target state are elementary control/dynamical-systems facts.

Therefore theorem PF1,

\[
u(E)\text{ strictly increasing},\quad u(E_*)=1
\Rightarrow E_*\text{ stable},
\]

should currently be treated as an organizing derivation, **not** as a literature-novel control theorem.

## Candidate contribution of the PAYOFF-B macro programme

The potential novelty is the explicit bridge among three literatures that are usually analyzed with different response variables.

### 1. Common dimensionless movement/environment coordinate

For matched spatial support,

\[
u_{\rm macro}
=
\frac{c_{\rm animal}}
{c_{\rm environment}}.
\]

This puts animal movement and environmental-wave propagation on the same dimensionless timescale axis.

The ratio itself is simple; the contribution would be its systematic use across heterogeneous movement systems rather than its algebra.

### 2. Phase rather than zero-lag matching

The framework separates

~~~text
phase target:
  E*

controller gain:
  kappa

correction scale:
  ell = c_e/kappa
~~~

instead of defining successful tracking as zero phenological lag.

This matters because published systems already show persistent leads/lags and route-stage changes in phase.

### 3. Controller coordinates extracted from existing data

The proposed empirical object is

\[
\log u = \alpha+\kappa E,
\]

with

\[
E_*=-\alpha/\kappa,
\qquad
\ell=c_e/\kappa.
\]

The candidate contribution is to estimate comparable \(\kappa\), \(E_*\), and \(\ell\) across taxa/populations and explain their variation.

The current mule-deer reanalysis is the first registered example in this programme.

### 4. Separation of controller limitations

The programme distinguishes:

~~~text
information limitation:
  downstream phenology is unpredictable

actuation limitation:
  the animal cannot express corrective movement

environmental endogeneity:
  the animal changes the resource wave itself
~~~

These are represented by the proposed axes

\[
(P,G,\chi).
\]

A weak tracking signal has different biological meaning depending on which axis limits the system.

### 5. Strategy-aware synthesis

The framework does not force all systems into continuous surfing.

It treats

~~~text
SURF
STEP
JUMP
OVERTAKE
ENGINEER
~~~

as distinct movement architectures whose controller coordinates may not be directly interchangeable.

## Publication-level novelty gate

A standalone macroecological paper should not be framed as:

> "animals adjust migration to phenology."

That is established.

A stronger candidate framing is:

> **Phenological migration is a phase-control problem whose gain, target phase, and correction scale depend on environmental predictability, movement permeability, and whether the resource wave is exogenous.**

To justify this as a broad empirical contribution, the programme still needs:

1. at least two, preferably three, independent systems with directly estimable controller coordinates;
2. one independent predictability or barrier contrast;
3. one interpretable failure/boundary case;
4. an explicit literature search showing that this exact cross-system controller parameterization has not already been proposed.

Until those gates are met, use "framework", "reanalysis", and "comparative prediction", not "new general law".
