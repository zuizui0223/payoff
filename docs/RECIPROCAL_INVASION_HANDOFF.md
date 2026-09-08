# PAYOFF reciprocal-invasion handoff

The canonical game has a direct population-level identification route.
Measure or bound the oriented rare-D advantage in an S resident (`u`) and the
oriented rare-S advantage in a D resident (`v`) under matched external contexts.

```python
from src.reciprocal_invasion_identification import identify_from_reciprocal_invasion

receipt = identify_from_reciprocal_invasion(
    differentiated_into_shared_band=(u_lo, u_hi),
    shared_into_differentiated_band=(v_lo, v_hi),
    support_reference="declared_population_assay_provenance",
    resident_contexts_matched_declared=True,
    common_scale_declared=True,
)
```

If both bands have strict signs, `certified_strict_phase` reports coexistence,
coordination, or one of the two dominance phases. This phase call needs oriented
signs only. If the two assays have separate unknown positive scale multipliers,
set `common_scale_declared=False`: the phase may still be certified, but the code
will refuse to return numerical `phi` or `eta` bands.

With a common scale, the receipt also returns exact `(phi,eta)` corner vertices,
coordinate bands, and whether `eta != 0` is certified. Closed intervals touching
zero are treated as boundary/ambiguity, never as strict evidence.

## Partial identification when one sign is unresolved

Published studies often certify one rare-type direction while the reciprocal
assay remains unresolved. Do not convert a non-significant result into a negative
sign or an exact zero.

Use:

```python
from src.reciprocal_sign_partial_identification import identify_phase_from_sign_evidence

receipt = identify_phase_from_sign_evidence(
    "unresolved",   # D in S
    "positive",     # S in D
    support_reference="declared_published_or_experimental_provenance",
)
```

The receipt returns all compatible strict phases, excluded strict phases, and
whether a boundary remains compatible. Numerical `phi` and `eta` are never
claimed from sign categories alone.

## Real published-data recovery now exists

The route is no longer synthetic-only at the **generic game-layer** level.

`docs/PSTUTZERI_PUBLISHED_RECIPROCAL_INVASION_RECEIPT_V1.md` freezes a published
application to *Pseudomonas stutzeri* competition data:

```text
pH 6.5:
    both rare types increase over the declared short pre-evolution window
    -> strict generic reciprocal invasion / protected coexistence

pH 7.5:
    rare generalist increase certified
    rare specialist response unresolved
    -> only generic coexistence or generalist dominance remain as strict phases,
       plus a boundary
```

The associated machine-readable receipt is

```text
validation/pstutzeri_published_reciprocal_sign_v1.json
```

This validates transportability of the reciprocal-sign measurement logic. It
does **not** identify PAYOFF's shared-versus-differentiated architecture `eta`.
The strain labels are algebraic orientation labels, not SCH/BALANCE/BITA
architecture semantics.

## Time horizon must be declared

Read `docs/EMPIRICAL_GAME_TIME_HORIZON_GATE_V1.md` before extending a frequency
game across many generations.

The same *P. stutzeri* system shows why: the short reciprocal tests were chosen
to minimize genetic/phenotypic change, whereas longer propagation produced
altered generalist phenotypes and a different trajectory. The later observations
therefore belong to an evolving-game regime rather than an unchanged fixed
`(phi,eta)` extrapolation.

## Claim boundary

This is the PAYOFF-owned evidence route requested by the sister-program separation
contract. Generic reciprocal-invasion measurement logic is now empirically
recovered, but it remains separate from direct architecture-frequency
identification.

It is not a substitute for SCH, BALANCE or BITA empirical gates and does not
establish fixation, mutation-limited accessibility, historical causation, or
PAYOFF architecture `eta`.
