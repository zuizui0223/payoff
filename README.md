# PAYOFF — from ecological compromise to evolving architecture and population dynamics

PAYOFF is the mathematical bridge across three sister repositories:

- [SCH](https://github.com/zuizui0223/sch): reconstructs conflict when multiple functions share one phenotypic coordinate.
- [BALANCE](https://github.com/zuizui0223/balance): identifies when that real conflict is still cheaper than changing architecture.
- [BITA](https://github.com/zuizui0223/bita): measures how much extra dimensionality recovers and when recovery can outweigh architecture cost.

PAYOFF asks what happens next:

> **How does a measurable within-organism functional conflict generate an architecture payoff landscape, and how is that landscape transported into architecture construction, evolutionary games, fixation, mutation-selection occupancy, space, and time?**

Biological functions are payoff components, not literal strategic agents. The strategic/evolutionary objects are heritable architectures.

Start with [`theory/PAYOFF_TRANSPORT_PRINCIPLE.md`](theory/PAYOFF_TRANSPORT_PRINCIPLE.md). For the full reading order use [`docs/CANONICAL_READER_PATH.md`](docs/CANONICAL_READER_PATH.md).

---

## 1. Upstream architecture payoff landscape

For two functions forced to share one trait,

```text
loss_S(z)=a(z-theta1)^2+b(z-theta2)^2.
```

The unique compromise has conflict load

```text
L=[ab/(a+b)](theta1-theta2)^2.
```

For the registered differentiated residual-coupling model,

```text
R=sL,
```

with

```text
s=ab/[ab+c(a+b)].
```

The original binary shared-versus-differentiated gap is

```text
phi=R-K=sL-K.
```

The more general architecture-level object is

```text
b(a)=R(a)-K(a),
```

where `a` can be a coupling strength, a partial modular architecture, or a discrete coupling topology.

So the original binary PAYOFF model is one pairwise contrast on a broader architecture payoff landscape.

---

## 2. Continuous architecture: shared, partial, full, then branching

Along a monotone release path use recovered conflict loss itself as architecture coordinate:

```text
r=R(lambda) in [0,L].
```

With smooth architecture cost `C(r)`, intrinsic payoff is

```text
b(r)=r-C(r).
```

An interior intrinsic optimum satisfies

```text
C'(r*)=1.
```

With symmetric architecture-distance feedback

```text
H(r,q)=-gamma(r-q)^2,
```

the monomorphic selection gradient is still

```text
1-C'(r).
```

but the mutant curvature at `r*` is

```text
-C''(r*)-2gamma.
```

Therefore the general local branching boundary is

```text
gamma_branch=-C''(r*)/2.
```

For quadratic cost

```text
C(r)=c1*r+(kappa/2)r^2,
alpha=1-c1,
```

one gets

```text
r0=clip(alpha/kappa,0,L)
```

and

```text
gamma_branch=-kappa/2.
```

Thus:

```text
alpha<=0              shared intrinsic optimum
0<alpha<kappa L       partial-modularity intrinsic optimum
alpha>=kappa L        full-differentiation intrinsic optimum.
```

For the declared quadratic potential game, crossing `gamma=-kappa/2` converts an interior partial architecture from a monomorphic ESS into a protected mixture of the two recovery endpoints.

See:

- [`theory/CONTINUOUS_ARCHITECTURE_ESS.md`](theory/CONTINUOUS_ARCHITECTURE_ESS.md)
- [`theory/GENERAL_CONVEX_ARCHITECTURE_BRANCHING.md`](theory/GENERAL_CONVEX_ARCHITECTURE_BRANCHING.md)
- [`theory/CONTINUOUS_ARCHITECTURE_GLOBAL_PHASE_DIAGRAM.md`](theory/CONTINUOUS_ARCHITECTURE_GLOBAL_PHASE_DIAGRAM.md)

---

## 3. Continuous branching closes back into the original two-strategy game

For endpoint architectures

```text
S: r=0,
D: r=L,
```

the continuous model gives

```text
phi_end
=alpha L-(kappa/2)L^2,
```

and

```text
eta_end=gamma L^2.
```

When

```text
0<alpha<kappa L,
gamma<-kappa/2,
```

one automatically has

```text
|phi_end|<|eta_end|,
eta_end<0.
```

So the post-branching endpoint game lies exactly inside PAYOFF's stable negative-frequency coexistence wedge.

The differentiated-endpoint frequency is

```text
p_D*
=(1-phi_end/eta_end)/2
```

and is identical to the endpoint frequency from the continuous potential solution.

Thus the binary PAYOFF game reappears endogenously as the post-branching endpoint phase.

See [`theory/CONTINUOUS_ENDPOINT_COEXISTENCE.md`](theory/CONTINUOUS_ENDPOINT_COEXISTENCE.md).

---

## 4. Edgewise modularization: which functional connection should weaken?

Give every functional coupling edge `e=(i,j)` its own strength `c_e`.

After phenotype optimization,

```text
partial D*/partial c_e
=(x_i*-x_j*)^2.
```

So squared optimized disagreement across an edge is exactly its marginal coupling penalty.

Using decoupling amount `d_e`,

```text
partial R/partial d_e
=(x_i*-x_j*)^2.
```

Recovery is convex in edgewise decoupling. Therefore with additive linear decoupling cost,

```text
Phi(d)=R(d)-sum_e k_e d_e
```

is convex on the coupling box, and at least one global optimizer is a vertex:

```text
d_e in {0,c_e^0}.
```

So under the declared geometry, continuously variable couplings can generate a discrete retain/release modular topology.

This does not mean graded coupling is universally impossible; sufficiently convex architecture cost can stabilize interior edge strengths.

See [`theory/EDGEWISE_MODULARIZATION.md`](theory/EDGEWISE_MODULARIZATION.md).

---

## 5. Global architecture value can differ from local accessibility

For one edge with linear decoupling cost `k d`, define

```text
k_local=R'(0),
k_global=R(dmax)/dmax.
```

Convex recovery gives

```text
k_local<=k_global.
```

Hence

```text
k_local<k<k_global
```

is a finite-jump modularization barrier:

```text
small release mutations are selected against,
complete release has higher payoff.
```

For the original two-function quadratic model, with reference separation fraction `s0`,

```text
k_local=s0^2 Delta^2,
k_global=s0 Delta^2,
```

and the exact gap is

```text
W_k=s0(1-s0)Delta^2.
```

At fixed functional optimum separation `Delta`, the gap is largest at

```text
s0=1/2,
```

where

```text
W_k,max=Delta^2/4.
```

So intermediate residual integration produces the largest mismatch between global payoff advantage and local evolvability in this model.

See [`theory/DISCONTINUOUS_MODULARIZATION_BARRIER.md`](theory/DISCONTINUOUS_MODULARIZATION_BARRIER.md).

---

## 6. Discrete topology game

Represent a vertex architecture by a binary edge-release vector `S` with intrinsic optimized payoff

```text
b_S=R(S)-K(S).
```

For weighted topology distance

```text
q(S,T)=sum_e w_e(s_e-t_e)^2
```

and symmetric feedback

```text
H(S,T)=-gamma q(S,T),
```

every topology pair is exactly a canonical PAYOFF game with

```text
phi_ST=b_T-b_S,
eta_ST=gamma q(S,T).
```

Therefore:

```text
gamma<0 and |Delta b|<|gamma|q
-> stable pairwise topology coexistence;

gamma>0 and |Delta b|<gamma q
-> pairwise topology coordination.
```

All deterministic and finite-population PAYOFF receipts can be reused pair by pair.

See [`theory/TOPOLOGY_PAYOFF_GAME.md`](theory/TOPOLOGY_PAYOFF_GAME.md).

---

## 7. Any symmetric architecture pair has canonical PAYOFF coordinates

The topology-distance kernel is only one special case.

For any symmetric pair

```text
[[a,b],
 [b,d]],
```

define

```text
phi=(d-a)/2,
eta=(a+d-2b)/2.
```

After a common additive shift, the pair is exactly

```text
[[0,phi-eta],
 [phi-eta,2phi]].
```

Thus `(phi,eta)` are canonical local coordinates for any symmetric architecture pair.

For a decomposition

```text
A_ij=b_i+b_j+H_ij,
```

```text
phi_ij
=b_j-b_i+(H_jj-H_ii)/2,
```

```text
eta_ij
=(H_ii+H_jj-2H_ij)/2.
```

So intrinsic architecture gap and population-game `phi` coincide only when same-type feedback is equal across the pair.

See [`theory/SYMMETRIC_GAME_CANONICALIZATION.md`](theory/SYMMETRIC_GAME_CANONICALIZATION.md).

---

## 8. Well-mixed invasion and finite-population fixation

For any canonical architecture pair,

```text
Delta(p)=phi+eta(2p-1),
```

with strict phases

```text
phi<-|eta|             first architecture dominance
phi>|eta|              second architecture dominance
|phi|<|eta|, eta<0     stable coexistence
|phi|<|eta|, eta>0     coordination bistability.
```

Rare-invasion boundaries are

```text
phi=+eta,
phi=-eta.
```

Under the declared exponential Moran process,

```text
rho_T/rho_S
=exp[beta(N-2)phi].
```

Under weak selection,

```text
rho_T>1/N iff 3phi>eta.
```

So deterministic rare invasion, reciprocal fixation ordering, and absolute mutant advantage remain separate estimands.

---

## 9. Rare topology mutation: stationary abundance is not accessibility

With connected symmetric rare mutation among architecture states and exponential Moran fixation, any finite symmetric architecture game has self-play scores

```text
u_i=A_ii/2.
```

The exact monomorphic stationary law is

```text
Pi_i
propto
exp[beta(N-2)u_i].
```

For zero-diagonal architecture feedback,

```text
u_i=b_i,
```

so

```text
Pi_i
propto
exp[beta(N-2)b_i].
```

Off-diagonal ecological interaction changes invasion, coexistence, fixation probabilities, substitution rates, and metastability, but cancels from these symmetric weak-mutation monomorphic weights.

Single-edge topology accessibility is tracked separately by the intrinsic path valley

```text
B(S->G)
=max[0,b_S-best_path_bottleneck].
```

Thus a globally favored topology can have high long-run stationary weight and still be difficult to reach through local edge mutations.

See:

- [`theory/TOPOLOGY_RARE_MUTATION.md`](theory/TOPOLOGY_RARE_MUTATION.md)
- [`theory/SYMMETRIC_RARE_MUTATION_GIBBS.md`](theory/SYMMETRIC_RARE_MUTATION_GIBBS.md)
- [`theory/ARCHITECTURE_STATE_ATLAS.md`](theory/ARCHITECTURE_STATE_ATLAS.md)

---

## 10. Space: local architecture gaps become spectral invasion

Patch-specific rare-type margins are transported through

```text
A=diag(r)-mL_G.
```

Metapopulation invasion is

```text
Lambda=lambda_max(A).
```

For connected conservative migration, the principal exponent falls from the best local source toward the landscape mean as migration strengthens.

A local architecture source can therefore rescue a type in a landscape whose average static payoff disfavors it, but only below a critical migration rate.

See [`theory/ENVIRONMENT_MOSAIC_SOURCE_SINK.md`](theory/ENVIRONMENT_MOSAIC_SOURCE_SINK.md).

---

## 11. Time: common forcing is a null, source switching creates a premium

If every patch receives the same additive temporal forcing,

```text
A(t)=A0+q(t)I,
```

then

```text
Lambda_temporal
=lambda_max(A0)+mean(q).
```

Zero-mean common fluctuations have no extra long-run effect.

When relative patch quality changes through time, seasonal operators need not commute. For the registered symmetric two-patch two-season model,

```text
Lambda_F
=lambda_max(A_bar)+P_temp,
```

with

```text
P_temp>=0.
```

For anti-phase source switching,

```text
season A: (r_bar+x,r_bar-x)
season B: (r_bar-x,r_bar+x),
```

```text
Lambda_F
=r_bar-m
+(1/tau)asinh[
  m/sqrt(m^2+x^2)
  *sinh(tau sqrt(m^2+x^2))
].
```

The temporal premium has one unique finite migration maximum for every nonzero contrast.

In weak contrast,

```text
m_opt tau -> 1.6061152988...
```

and

```text
P_max
~=0.13248753945 x^2 tau.
```

The exact critical seasonal contrast and two migration boundaries are implemented when temporal switching is strong enough to overcome a coordination barrier.

---

### 11b. Migration–phenology tracking under a moving environment

An exploratory PAYOFF-B extension now treats spatial movement and phenological
change as alternative heritable axes for closing the same moving environmental
mismatch. The interaction partner can track that demand through a different
mixture of the two axes, so a lineage can be abiotically successful yet fail
because partner overlap is lost.

The current implementation provides:

- a dependency-free deterministic tracking simulator;
- a global migration x phenology strategy-grid optimizer;
- a rare-mutation local adaptive walk;
- mutation-selection stationary occupancy on the 2D strategy lattice;
- two-species alternating rare-mutation coevolution;
- seed-explicit stochastic climate and partner forcing;
- phase classification into migration, phenology, mixed, stasis,
  interaction failure, and abiotic failure;
- reproducible sharded large sweeps with resume and dry-run workload counting.

A notable accessibility result already appears in the coevolution tests:
interaction matching can lock two species on a matched mixed strategy even when
both have the same intrinsic cost bias toward one tracking axis, because a
unilateral move first creates partner mismatch.

Run the deterministic phase sweep with:

    python scripts/migration_phenology_phase_sweep.py

Run or size the stochastic sweep with:

    python scripts/migration_phenology_stochastic_sweep.py --dry-run

The model and claim boundary are documented in
[theory/MIGRATION_PHENOLOGY_TRACKING.md](theory/MIGRATION_PHENOLOGY_TRACKING.md).

This lane is not another pollinator-community realization model: its focal
question is which adaptive axis tracks a moving environment, and when axis
mismatch between interactors breaks otherwise successful environmental
tracking.

The first frozen synthetic receipt is
[docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md](docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md).
Within the declared 75-cell ecological design, 44 cells contain a positive
coordination gap between the locally accessible coevolution endpoint and a
coordinated matched-pair optimum. Crossing that design with demographic stress
showed that the barrier is usually demographically cryptic: an independent
128-replicate rerun retained no cell with a >=0.10 persistence gain. Instead,
the replicated signal is a **demographic visibility window**: mean persistence
gain is largest when local persistence is intermediate and approaches zero
when both alternatives are almost certainly lost or almost certainly persist.

Finite-N weak-mutation evolution adds a second distinction. Small populations
can stochastically cross the deterministic coordination barrier, whereas large
populations remain locked at the local endpoint. In the first drift pilot this
barrier crossing did **not** raise long-run mean joint growth because broader
drift occupancy imposed a larger payoff load. The retained result is therefore
drift-assisted barrier crossing, not drift rescue.

The explicit spatial extension is frozen separately in
[docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md](docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md).
Here migration is actual conservative movement among patches and the climate
envelope moves across a finite landscape. The canonical low-density-fitness
runs give a monotone persistence frontier: increasing the allowed phenological
shift from 0 to 5 raises the sampled maximum persistent climate velocity from
0.030 to 0.065, with identical frontier brackets on 7 x 7 and 11 x 11 strategy
grids. Every frontier strategy remains migration-dominant, so phenology extends
the persistence envelope without replacing spatial range tracking near the
boundary.

Spatialization also makes the coordination problem demographically sharp. In
the coarse explicit-landscape design, 52/108 cells contain a coordination
barrier and 24/108 have local coevolutionary extinction but coordinated
persistence. With a finer unilateral mutation step, 57/81 positive-interaction
cells retain barriers and 21/81 retain persistence rescue. A direct one-step
audit shows the mechanism: moving both partners from (migration, phenology)
=(0.2,0.0) to (0.2,0.2) raises joint low-density payoff by about +1.115, while
either partner moving alone has payoff change about -1.427 because interaction
mismatch rises to about 3.189.

The two-dimensional connectivity extension is frozen in
[docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md](docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md).
The key added result is **temporal buffering of connectivity costs**. In the
7 x 7 zigzag-route resolution check, the mean open-to-zigzag low-density
growth penalty shrinks from about -0.0419 at phenology limit 0 to -0.0070 at
limit 4. With limit 4 the optimum is phenology-only at climate velocities
0.04-0.05, mixed at 0.06, and increasingly migration-dependent by 0.07.
This temporal-bypass transition is bracketed by an explicit finite-horizon
capacity diagnostic.

The 2D coevolutionary result is robust to route geometry and mutation
resolution. At mutation step 0.1, 22/24 positive-interaction cells contain
coordination barriers and 21/24 convert local extinction into coordinated
persistence. The canonical zigzag gate has resident growth about -0.840,
coordinated growth about +0.255, coordinated gain +1.095, and unilateral gain
about -5.946. Adding an explicit Bhattacharyya distribution-overlap penalty
does not remove the gate; it makes the unilateral step still more costly.

Partner-specific tracking costs expose a forcing-dependent role of
interaction. At moderate climate speed, interaction synchronizes quantitatively
different partner strategies while all sampled pairs persist. At stronger
forcing, the same synchronizing pressure locks the pair into a migration-only
local attractor and all sampled pairs go extinct. The retained interpretation
is therefore **synchronization can become maladaptive synchronization**.

The 2D buffering result is also robust to directional movement limitation.
Reducing transverse-to-longitudinal dispersal weight from 1 to 0.1 makes the
zigzag growth penalty somewhat larger when phenology is unavailable, but
raising the phenology limit from 0 to 4 still removes about 76% of the penalty
magnitude across the sampled anisotropy levels. No anisotropy-specific
persistence rescue is claimed.

The fixed-rate tracking layer now also has an exact closed-loop
controller extension in
[theory/CLOSED_LOOP_MOVEMENT_PHENOLOGY_TRACKING.md](theory/CLOSED_LOOP_MOVEMENT_PHENOLOGY_TRACKING.md),
with frozen results in
[docs/PAYOFF_B_CLOSED_LOOP_TRACKING_RESULTS_20260920.md](docs/PAYOFF_B_CLOSED_LOOP_TRACKING_RESULTS_20260920.md).
If q_m is mismatch-dependent movement feedback and q_h is timing feedback, the
local recurrence depends only on K=q_m+q_h. Stability requires 0<K<2; at fixed
K, quadratic costs allocate more restoring effort to the cheaper axis. Under
equal costs the unconstrained optimum becomes dynamically and phenologically
infeasible at sufficiently strong forcing, so stronger feedback is not
universally better.

The closed-loop null has also been returned to the explicit 2D landscape via
a mismatch-dependent movement-rate controller. In the sampled high-forcing
regime, movement feedback alone improves tracking but remains non-persistent,
whereas an independent timing response crosses the persistence boundary and
then substantially reduces the movement effort required by the controller.
The frozen result is
[docs/PAYOFF_B_MOVEMENT_FEEDBACK_LANDSCAPE_RESULTS_20260920.md](docs/PAYOFF_B_MOVEMENT_FEEDBACK_LANDSCAPE_RESULTS_20260920.md).
This is the current clearest demonstration that exact local space-time
substitutability can become complementarity once spatial mechanics and finite
capacities are restored.

The cross-system empirical architecture is now explicitly split into two
independent gates in
[docs/PAYOFF_B_PHASE_RETENTION_ACTUATOR_GATES_20260921.md](docs/PAYOFF_B_PHASE_RETENTION_ACTUATOR_GATES_20260921.md).

The common coordinate is phase retention

    e_out = r + lambda e_in.

Under the local closed-loop model,

    lambda = 1-K.

This is the quantity to compare across systems. Speed, stopover use, route
reset, directional movement, or other actuators are tested prospectively within
each system and are not required to generalize across taxa. Therefore
**lambda PASS / actuator FAIL is a valid and informative outcome**, not a
contradiction. The source-backed wigeon result now provides the prospective
`lambda PASS / actuator FAIL` example. Across 224 consecutive staging
transitions from 28 individuals,

    lambda = 0.85994
    SE = 0.04509
    p versus lambda=1 = 0.00190.

The primary preregistered `lambda<1` prediction passes, while the stronger
`|lambda|<0.75` forecast fails and neither stopover nor measured travel-speed
actuator is supported. The quantitative receipt is frozen in
[docs/PAYOFF_B_WIGEON_PHASE_RETENTION_RECEIPT_20260921.md](docs/PAYOFF_B_WIGEON_PHASE_RETENTION_RECEIPT_20260921.md).

The existing mule-deer, barnacle-goose, and wigeon direct results are frozen
separately in
[docs/PAYOFF_B_THREE_TAXON_PHASE_RETENTION_RECEIPT_20260921.md](docs/PAYOFF_B_THREE_TAXON_PHASE_RETENTION_RECEIPT_20260921.md).
That three-taxon receipt is descriptive: it establishes a portable response
coordinate, not one universal lambda or a pooled actuator rule.

The current empirical panel status is frozen in
[docs/PAYOFF_B_EMPIRICAL_PHASE_PANEL_STATUS_20260921.md](docs/PAYOFF_B_EMPIRICAL_PHASE_PANEL_STATUS_20260921.md).
The panel now has three direct taxa, with wigeon as the prospective third-taxon
extension. A fourth taxon remains **HOLD by default**.

The inclusion rule is now test-based rather than taxon-based. A candidate
lambda test must add a new prospectively registered lambda endpoint or boundary
test on the common coordinate and segment scale. A prospective actuator-only
test can also be included, but contributes zero additional lambda support.
Raw-data availability or a new forcing regime alone is not enough.

The source-backed industrial-development mule-deer analysis first entered as
an actuator-only forcing perturbation without increasing the direct-taxon
count. Its actuator receipt is
[docs/PAYOFF_B_INDUSTRIAL_MULE_DEER_ACTUATOR_RECEIPT_20260921.md](docs/PAYOFF_B_INDUSTRIAL_MULE_DEER_ACTUATOR_RECEIPT_20260921.md).

A stronger within-taxon test is now preregistered: large-development animals
are predicted to retain more phase mismatch than small-development animals on
a fixed 24-hour local peak-IRG coordinate. The offline peak-IRG reconstruction,
MODIS product-version firewall, GPS environmental join, and fixed-interval
phase-pair pipeline are implemented in
[docs/PAYOFF_B_AIKENS_IRG_RECONSTRUCTION_HANDOFF_20260921.md](docs/PAYOFF_B_AIKENS_IRG_RECONSTRUCTION_HANDOFF_20260921.md).
The lambda outcome remains unopened until the MODIS NDVI plus snow/quality
source layer is materialized.

Confirmatory evidence is now stricter than that verbal separation. Prediction
registration and observation files are separate. A prospective lambda receipt
must match its frozen system ID, independent-test ID, phase-coordinate ID and
segment-scale ID. A prospective actuator receipt must contain exactly the
registered actuator names: missing predictions and post-hoc added actuator
variables are both rejected.

Cross-system synthesis then counts **independent prospectively registered
lambda tests**, not taxa and not actuator successes. Retrospective lambda
analyses remain visible in a separate tier but do not increase prospective
support. Synthesis is refused if phase-coordinate or segment-scale definitions
differ across systems, and the API deliberately exposes no pooled actuator or
lambda-plus-actuator omnibus score.

Candidate evidence is screened before addition by
`src/taxon_inclusion_gate.py` with preferred CLI
`scripts/evaluate_evidence_inclusion.py`. The inference unit is an independent
test. Lambda tests require the common phase coordinate and segment scale;
actuator-only tests do not, because they contribute zero lambda support. A new
forcing regime by itself is not a registered endpoint and therefore does not
license inclusion.

The empirical bridge is now explicit in
[docs/PAYOFF_B_TRACKING_EMPIRICAL_PARAMETERIZATION.md](docs/PAYOFF_B_TRACKING_EMPIRICAL_PARAMETERIZATION.md).
Under the declared one-step movement family, projected fixed-interval component
second moments identify migration rate and x/y movement weights; adding mean
displacements identifies x/y directional biases. Environmental wave speed and
gradient identify climate velocity.

Phase-error compression is kept separate from the independent phenology rate:
the latter is licensed only when timing has been isolated from movement and
other tracking pathways. Fitness terms require separate matched growth
contrasts rather than being imputed from movement data.

The first named-system readiness receipt is
[docs/PAYOFF_B_MULE_DEER_PARAMETERIZATION_READINESS_20260920.md](docs/PAYOFF_B_MULE_DEER_PARAMETERIZATION_READINESS_20260920.md).
The public mule-deer system is biologically appropriate for tracking
calibration, and the interval pipeline can now fit a directional movement kernel
from raw projected GPS means and second moments. The published group summaries,
however, are not silently converted into per-step model rates: they do not
contain those interval movement moments, early/mid phase summaries cross zero,
and the late summary is a whole-route compression rather than one frozen
decision interval. Because the observed compensation also uses movement speed
and stopovers, the group-level Days-From-Peak compression is not treated as the
independent phenology rate h.

The current status is therefore **public system identified, direct tracking
calibration pending source-file ingestion**.

---



## 12. Main organizing principle

PAYOFF is now best read as one transport hierarchy:

```text
functional conflict
        L
        |
        v
architecture landscape
        a -> R(a)-K(a)=b(a)
        |
        +--> continuous ESS / branching
        +--> edgewise modularization / topology
        |
        v
symmetric architecture pair
        (phi,eta)
        |
        +--> deterministic invasion
        +--> finite fixation
        +--> rare-mutation occupancy
        +--> spatial spectral growth
        +--> temporal Floquet growth.
```

The same biological system can have different answers to:

```text
which architecture has highest intrinsic payoff?
which architecture is locally reachable?
which architecture can invade when rare?
which mutant fixes more often?
which topology dominates weak-mutation occupancy?
which architecture persists in space or periodic environments?
```

Those distinctions are the point of the framework, not nuisances to be collapsed.

---

## 13. Reading and claim boundaries

Start with:

- [`theory/PAYOFF_TRANSPORT_PRINCIPLE.md`](theory/PAYOFF_TRANSPORT_PRINCIPLE.md)
- [`theory/ARCHITECTURE_STATE_ATLAS.md`](theory/ARCHITECTURE_STATE_ATLAS.md)
- [`theory/BOUNDARY_ATLAS.md`](theory/BOUNDARY_ATLAS.md)
- [`docs/CANONICAL_READER_PATH.md`](docs/CANONICAL_READER_PATH.md)

Empirical handoffs:

- [`docs/SCH_BALANCE_BITA_BRIDGE.md`](docs/SCH_BALANCE_BITA_BRIDGE.md)
- [`docs/CONTINUOUS_ARCHITECTURE_HANDOFF.md`](docs/CONTINUOUS_ARCHITECTURE_HANDOFF.md)
- [`docs/TEMPORAL_HANDOFF.md`](docs/TEMPORAL_HANDOFF.md)
- [`docs/PAYOFF_B_PHASE_RETENTION_ACTUATOR_GATES_20260921.md`](docs/PAYOFF_B_PHASE_RETENTION_ACTUATOR_GATES_20260921.md)
- [`docs/PAYOFF_B_TRACKING_EMPIRICAL_PARAMETERIZATION.md`](docs/PAYOFF_B_TRACKING_EMPIRICAL_PARAMETERIZATION.md)

Claim ceilings:

- [`docs/CLAIM_BOUNDARY.md`](docs/CLAIM_BOUNDARY.md)
- [`docs/PRIOR_ART_BOUNDARY.md`](docs/PRIOR_ART_BOUNDARY.md)
- [`docs/CONTINUOUS_ARCHITECTURE_PRIOR_ART_BOUNDARY.md`](docs/CONTINUOUS_ARCHITECTURE_PRIOR_ART_BOUNDARY.md)
- [`docs/TOPOLOGY_CLAIM_BOUNDARY.md`](docs/TOPOLOGY_CLAIM_BOUNDARY.md)
- [`docs/SPATIAL_PRIOR_ART_BOUNDARY.md`](docs/SPATIAL_PRIOR_ART_BOUNDARY.md)
- [`docs/TEMPORAL_PRIOR_ART_BOUNDARY.md`](docs/TEMPORAL_PRIOR_ART_BOUNDARY.md)

PAYOFF does not claim to invent specialization, adaptive dynamics, branching, modularity, evolutionary games, Moran processes, source-sink theory, graph selection, or Floquet theory. The candidate contribution is the **explicit architecture payoff transport from measured functional compromise into those established population-theoretic objects, with exact receipts under declared models.**
