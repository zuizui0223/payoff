# PAYOFF interior-frequency validation handoff — 2026-09-07

The reciprocal-invasion route now has an explicit out-of-endpoint falsification
step. Rare-D-in-S and rare-S-in-D margins determine the canonical endpoint line;
strict interior observations are held out and are never used for fitting.

Use `validate_frequency_response_holdouts(...)` with:

- the two reciprocal endpoint bands,
- one or more unique strict interior frequencies,
- an observed `D-minus-S` gap band at each frequency,
- matched resident/external context declaration,
- a common positive oriented payoff/growth-gap scale declaration.

Any disjoint interior band returns
`canonical_linear_frequency_response_rejected_by_holdout`. Passing every
registered holdout returns `canonical_linear_frequency_response_holdout_supported`.
Closed-band contact counts as compatible.

This closes a specific logical gap: reciprocal invasion identifies endpoint phase
geometry, but does not by itself prove that frequency dependence is linear between
those endpoints. The new holdout check can reject that interpolation without
changing or refitting the endpoint result.

This remains theory/measurement infrastructure. No natural population has been
run through this gate in this commit.
