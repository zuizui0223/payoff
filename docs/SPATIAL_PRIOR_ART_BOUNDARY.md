# Spatial prior-art boundary for PAYOFF

PAYOFF does not claim that spatial evolutionary games, graph-structured selection, migration-coupled populations, source-sink metapopulations, principal-eigenvalue persistence criteria, dispersal reduction principles, synchronization, or bistable patch mosaics are new.

## 1. Evolutionary games on graphs are established

Ohtsuki, Hauert, Lieberman & Nowak (2006), *A simple rule for the evolution of cooperation on graphs and social networks*, Nature 441:502-505, established influential graph-structured evolutionary-game results.

Ohtsuki & Nowak (2006) and related work derived weak-selection graph analogues of replicator dynamics under several update rules.

PAYOFF's regular-graph layer therefore only substitutes the architecture payoff matrix into established pair-approximation formulas. The special simplification

```text
phi_k=k phi/(k-2),
eta_k=eta
```

is model-specific algebra, not a new general theory of evolutionary graphs.

## 2. Source-sink persistence and explicit movement are established

Arino, Bajeux & Kirkland (2019), **Number of Source Patches Required for Population Persistence in a Source-Sink Metapopulation with Explicit Movement**, Bulletin of Mathematical Biology 81:1916-1942, DOI `10.1007/s11538-019-00593-1`, studies explicit movement among source and sink patches and uses applied linear algebra to characterize persistence.

PAYOFF therefore does not claim that source patches, sink patches, explicit movement, or movement-dependent persistence thresholds are new.

## 3. Principal-eigenvalue growth criteria are established

Linear source-sink and metapopulation models routinely identify long-run growth or persistence from a dominant/principal eigenvalue of a matrix combining local demography and movement.

Bansaye & Lambert (2013), **New approaches to source-sink metapopulations decoupling demography and dispersal**, develops this spectral perspective for source-sink systems.

PAYOFF therefore does not claim to invent the criterion

```text
principal eigenvalue > 0
-> rare population can grow.
```

## 4. Spectral monotonicity and the reduction principle are established

Chen, Shi, Shuai & Wu, **Two Novel Proofs of Spectral Monotonicity of Perturbed Essentially Nonnegative Matrices with Applications in Population Dynamics**, SIAM Journal on Applied Mathematics, DOI `10.1137/20M1345220`, reviews and extends monotonicity results for spectral bounds of matrices combining dispersal and heterogeneous local dynamics, tracing the idea to Karlin's reduction principle and later generalizations.

PAYOFF therefore does not claim that increasing conservative mixing can reduce a heterogeneous system's principal growth rate as a new general theorem.

## 5. Migration-coupled bistability and synchronization are established

Coupled-patch systems with local bistability, migration-driven synchronization, critical coupling, and spatially heterogeneous states are mature dynamical-systems and metapopulation topics.

PAYOFF therefore does not claim to invent migration thresholds, synchronization, or polarized patch states as general phenomena.

## 6. PAYOFF-specific spatial bridge

The defensible contribution is the architecture parameter chain:

```text
patch ecological conflict
L_j
  |
  v
patch recoverable dimensional release
R_j=s_jL_j
  |
  v
patch static architecture gap
phi_j=s_jL_j-K_j
  |
  v
patch reciprocal rare-architecture margins
r_j^D=phi_j-eta_j
r_j^S=-phi_j-eta_j
  |
  v
migration-coupled operators
A_D=diag(r^D)-mL_G
A_S=diag(r^S)-mL_G
  |
  v
architecture-specific principal invasion exponents.
```

The spatial contribution is therefore a cross-scale parameterization: ecological trait-conflict measurements are carried into established source-sink/spectral machinery.

## 7. Current model-specific consequences

Under the declared symmetric time-independent patch model, PAYOFF derives:

```text
Lambda_D(0)=max_j(s_jL_j-K_j-eta_j),
Lambda_D(infinity)=mean_j(s_jL_j-K_j-eta_j),
```

with monotone interpolation in migration on a connected graph;

an exact two-patch source-sink rescue threshold

```text
m_c=r_1r_2/(r_1+r_2)
```

for one source and one stronger sink;

low-migration topology sensitivity

```text
dLambda/dm|_0=-weighted_degree_of_unique_best_source;
```

and, under a common environmental slope,

```text
Lambda_D(e,m)=Lambda_D(e0,m)+alpha(e-e0),
Lambda_S(e,m)=Lambda_S(e0,m)-alpha(e-e0).
```

In the common-eta two-patch special case, patch architecture contrast can oppose positive frequency-dependent coordination. If

```text
|phi_1-phi_2|>2eta,
```

low migration permits reciprocal spatial invasion, which switches to mutual non-invasion at

```text
m_switch=[(phi_1-phi_2)^2-4eta^2]/(8eta).
```

These are consequences for the PAYOFF parameterization. The underlying spectral and spatial tools remain prior art.

## 8. Claim ceiling

Preferred:

> We map patch-specific compromise recovery and architecture costs onto a source-sink invasion operator and derive the resulting migration and environmental thresholds under a symmetric patch model.

Avoid:

> We introduce a new theory showing that dispersal can reduce persistence.

Preferred:

> The local source strength is `s_jL_j-K_j-eta_j`, linking the principal invasion eigenvalue to independently measurable architecture quantities.

Avoid:

> Principal-eigenvalue source-sink theory is unique to PAYOFF.

Preferred:

> In the two-patch PAYOFF special case, environmental architecture contrast can overcome positive frequency-dependent coordination at low migration, with a closed-form migration switch.

Avoid:

> Habitat heterogeneity universally converts coordination games into coexistence.

## 9. Why PAYOFF keeps two spatial models separate

The conservative patch-migration model and the microscopic regular-graph model are different theories.

The patch model keeps the upstream ecological parameters `phi_j,eta_j` explicit and gives exact deterministic source-sink and migration results.

The regular-graph model requires an explicit update rule and weak-selection pair approximation. Its graph transform should not be treated as a correction to the patch model, nor vice versa.
