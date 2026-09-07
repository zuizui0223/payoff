# Precision before acquisition budget: PAYOFF continuation, 2026-09-07

## Checked baseline

The inspected main commit was `73df815cd24a657994c36d75e9ff14ac2c82c9ef`
(2026-09-07 13:46 JST). Its `test` workflow run 321, ID `34084323639`, completed
successfully. The latest additions were the adaptive routing audit and the
intermediate budget window, with two adaptive versus three fixed acquisitions
in the registered four-world example. These are finite-panel synthetic results.

The pre-existing PR #1 (`scope/sister-program-separation-v1`) was still open and
reported nonmergeable during this inspection. This continuation starts from the
current main and does not force-merge or overwrite that branch.

## New result

The outstanding precision condition is now an exact certificate, not an assertion
that more budget or adaptive routing always resolves the phase. For each
opposite-phase pair, compute the largest query-specific separation/error ratio;
the smallest of those pairwise maxima is the common error-scale ceiling. At a
finite ceiling, a concrete opposite-phase pair and a shared response vector prove
why BOTH adaptive and fixed designs fail.

See [`../theory/FINITE_PANEL_PRECISION_LIMIT.md`](../theory/FINITE_PANEL_PRECISION_LIMIT.md)
for the general proof, the three separate precision thresholds of the actual
PAYOFF witness, and its weighted acquisition-cost theorem.

## Use with the existing workflow

```python
from src.phase_precision_certificate import certify_phase_precision

precision = certify_phase_precision(
    worlds, queries,
    support_reference="declared_finite_panel_provenance",
    matched_contrasts_declared=True,
)
```

`identifiable_at_declared_errors` tests the supplied error bounds, at multiplier
one. `critical_error_scale_exact=None` means no finite ceiling, NOT a failed or
unknown calculation. A finite ceiling is excluded because the response bands
are closed. Use `identifiable_at_error_scale(scale)` to check other multipliers.

If precision is sufficient, use `plan_adaptive_phase_budget` or
`phase_adaptivity_budget_profile` for costs. If not, inspect `blocking_pair` and
`common_response_at_critical`; increasing acquisition budget within the same
vocabulary cannot remove that ambiguity. Better calibrated precision or a
new supported matched contrast is needed. These are theoretical diagnostics,
not a proposed field experiment or sample-size calculation.

## Interpretation

In the registered panel the intrinsic response routes between two contexts;
the relevant interaction scale differs between them. Measuring that context
first avoids acquiring both branch-specific interaction contrasts. This explains
why adaptivity can save resource without changing the biological payoff model
or increasing instrument precision. The benefit is conditional on the existence
of separable response bands and branch-dependent query needs.

Do not promote this synthetic measurement result to an ecological observation.
Theory first, independently recoverable real-world patterns next, and empirical
design only after those layers have been established remain separate stages.
