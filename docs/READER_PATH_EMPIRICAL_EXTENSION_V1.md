# Reader-path empirical extension v1

Read this extension immediately after **Part II — well-mixed evolutionary game** in `docs/CANONICAL_READER_PATH.md`, before moving to finite-population fixation.

The purpose is to separate three questions that the theory alone cannot answer:

```text
Can reciprocal invasion be measured in real systems?
Can incomplete sign evidence still exclude phases without overcalling a result?
Over what time horizon can the same two-type game be treated as fixed?
```

## E1. Direct reciprocal-invasion measurement contract

Read:

```text
docs/RECIPROCAL_INVASION_HANDOFF.md
theory/RECIPROCAL_INVASION_IDENTIFICATION.md
src/reciprocal_invasion_identification.py
```

Use this route when both oriented rare-type margins can be bounded numerically.

Strict signs alone identify the deterministic phase. A common numerical scale is additionally required for `phi,eta` reconstruction.

## E2. Partial sign identification

Read:

```text
src/reciprocal_sign_partial_identification.py
```

Use this when published or experimental evidence certifies one oriented sign but leaves the other unresolved.

Important rule:

```text
non-significant != negative
non-significant != exact zero
```

The output is a set of compatible strict phases plus whether a boundary remains compatible.

This prevents weak evidence from being forced into a false four-phase classification.

## E3. Published real-data receipt

Read:

```text
docs/PSTUTZERI_PUBLISHED_RECIPROCAL_INVASION_RECEIPT_V1.md
validation/pstutzeri_published_reciprocal_sign_v1.json
```

The *Pseudomonas stutzeri* receipt supplies the first repository-frozen published-data application of the reciprocal sign logic.

```text
pH 6.5:
    both rare types increase
    -> generic reciprocal invasion / protected coexistence

pH 7.5:
    rare generalist increase certified
    rare specialist response unresolved
    -> generic coexistence or generalist dominance remain possible,
       plus a boundary
```

This is Lane A generic game-layer recovery only.

## E4. Time-horizon gate

Read:

```text
docs/EMPIRICAL_GAME_TIME_HORIZON_GATE_V1.md
```

The P. stutzeri series shows that a short pre-evolution window and a longer evolutionary trajectory are different estimands.

```text
~20 generations:
    type definitions intentionally kept approximately frozen
    -> reciprocal-invasion sign inference licensed

~80 generations:
    generalist phenotypes evolve
    -> unchanged fixed-game extrapolation not licensed
```

Every empirical PAYOFF frequency analysis should therefore freeze a time horizon before interpreting a phase.

## E5. Generic evidence versus architecture evidence

Read:

```text
docs/EMPIRICAL_GAME_LAYER_STATUS_V1.md
docs/LANE_P_INTERSECTION_OBSTRUCTION_V1.md
docs/MICROBIAL_NEAR_LANE_P_LEDGER_V1.md
```

Do not collapse the following:

```text
generic two-type frequency game works in reality
        !=
frequency feedback has been identified between a PAYOFF
shared/integrated and differentiated/released architecture pair
```

The first statement now has direct published support. The second remains open.

## E6. Then continue the original canonical path

After this empirical extension, continue with

```text
Part III — finite populations
Part IV  — recurrent mutation and occupancy
Part V   — spatial structure
Part VI  — temporal structure
```

Those later layers remain model-specific transports. A generic reciprocal-invasion receipt does not automatically validate their finite-population, mutation, spatial or temporal assumptions.
