# PAYOFF-B shared-cue information recovery failure

Frozen: **2026-09-27**

## Result

The information-deadline model and the interaction-network model have now been
joined in one finite game.

The canonical system begins with all three players using a shared environmental
cue:

    follow | follow | follow

at cue accuracy q=1.

Cue reliability is then reduced to 0.5 in steps of 0.01 and restored to 1 in
the same steps.

Across complete, chain and migrant-star topologies, the result is identical for
this symmetric all-informed/all-old comparison.

### Degradation

The exact player-specific lower stability thresholds of the fully informed
profile are:

    flower            0.58333
    local pollinator  0.66667
    migrant           0.80000.

The migrant therefore sets the network boundary.

At q=0.80 the current informed policy is exactly tied and is retained by the
declared path-preserving rule.

At q=0.79 the informed convention collapses to:

    late | late | late.

### Recovery

Cue quality is then restored all the way to:

    q=1.

The network remains:

    late | late | late.

There is no recovery on the declared 0.01 path.

## Why this is not because information remains poor

At q=1, the environment is perfectly classified.

The obsolete profile has joint payoff:

    -0.60.

The fully informed profile has joint payoff:

    -0.45.

So coordinated information use would improve joint payoff by:

    +0.15.

Yet the unilateral gains from being the first species to begin using the cue
are:

    flower            -0.15
    local pollinator  -0.20
    migrant           -0.10.

No species wants to move first.

Both the obsolete and informed profiles are strict Nash equilibria at q=1.

Thus:

> **Environmental information can recover completely before ecological
> information use recovers.**

## Exact condition

For player i, let:

- R_i = prior mismatch risk under the old timing convention;
- D_i = information / waiting cost;
- I_i = interaction strength;
- p = probability of the state in which the informed action differs from the
  old action.

The obsolete profile is stable when:

    D_i + p I_i >= R_i.

The informed profile is stable when:

    D_i <= R_i + p I_i.

Both are strict when:

    |D_i - R_i| < p I_i.

The fully informed profile is jointly better when:

    sum D_i < sum R_i.

The canonical parameterization satisfies all four statements.

## Ecological interpretation

The sequence is:

    cue is reliable
    -> all species use it

    cue deteriorates
    -> using information becomes too costly / unreliable
    -> the information-using convention collapses

    cue recovers
    -> unilateral re-adoption creates partner mismatch
    -> nobody moves first

    q = 1
    -> perfect environmental information
    -> obsolete ecological convention persists.

This separates two recovery processes:

    environmental recovery
    !=
    behavioural / interaction-network recovery.

## Relation to the topology result

This canonical shared-cue trap is not topology-specific across the three tested
connected graphs. A lone adopter disagrees with all of its own connected
neighbours, so normalized first-mover interaction cost is the same.

The earlier heterogeneous private-cue result addresses a different layer:
whether a displaced mixed timing state is stored by network geometry. There,
strict inefficient hysteresis occurs in complete and chain networks but not in
the migrant-star.

So PAYOFF-B now has two memory mechanisms:

1. **acquisition memory** — a whole information-using convention can fail to
   restart even at perfect cue recovery;
2. **topological memory** — heterogeneous displaced timing states can be stored
   or erased depending on who interacts with whom.

## Provenance

Workflow run: **36286708314**

Artifact: **10920975444**

Artifact SHA256:

    e8f4b0e8839e55d6bd5ed176a00c02120383f6e778ec71fb82c0cef1d2ebdc78

The trace and analytic theorem agree.

## Claim ceiling

This is an exact synthetic game result.

It is not evidence that a natural plant–pollinator–migrant community has
already undergone recovery hysteresis.

The natural hysteresis prediction remains prospective.
