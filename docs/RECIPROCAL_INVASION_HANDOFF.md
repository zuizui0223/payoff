# PAYOFF reciprocal-invasion handoff

The canonical game now has a direct population-level identification route.
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

This is the PAYOFF-owned evidence route requested by the sister-program separation
contract. It remains a mathematical/measurement contract until actual reciprocal
population evidence is supplied. It is not a substitute for SCH, BALANCE or BITA
empirical gates and does not establish fixation or mutation-limited accessibility.
