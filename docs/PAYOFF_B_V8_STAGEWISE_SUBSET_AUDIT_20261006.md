# PAYOFF-B V8 stagewise subset representativeness audit — 2026-10-06

Status: **POSTHOC SUBSET-SELECTION AUDIT**

## Purpose

The stagewise population-front analysis is restricted to source-target-species
units with at least six same-year arrival and green-up observations at both
mapped stages in both periods.

This yields:
- 56 species-source-target units;
- 31 unique environmental pairs;
- 14 species.

The full environmental network contains 166 unique pairs.

This audit asks how the 31-pair stagewise subset differs from the 135 excluded
environmental pairs.

## Selection differences

### Source-target distance

Stagewise subset:
- mean = **495 km**;
- median = **469 km**.

Excluded pairs:
- mean = **911 km**;
- median = **757 km**.

Standardized mean difference:
- **-0.79**.

The stagewise subset is therefore substantially shorter-distance.

### Standardized source-destination coupling

Early rho:
- stage subset = **0.357**;
- excluded = **0.267**;
- SMD = **+0.20**.

Late rho:
- stage subset = **0.847**;
- excluded = **0.608**;
- SMD = **+0.64**.

Delta rho:
- stage subset = **+0.490**;
- excluded = **+0.341**;
- SMD = **+0.33**.

The stagewise subset is more strongly coupled, especially in the late period.

### Destination variability

Target SD increase:
- stage subset = **+1.50 d**;
- excluded = **+2.42 d**;
- SMD = **-0.47**.

Thus destination variability increased less strongly in the stagewise subset.

## Forecast-value change

Cross-validated squared-loss forecast-value proxy:

Early:
- stage subset = **-2.22 d^2**;
- excluded = **-19.28 d^2**.

Late:
- stage subset = **+24.40 d^2**;
- excluded = **+14.06 d^2**.

Late-minus-early delta G_CV:
- stage subset = **+26.61 d^2**;
- excluded = **+33.34 d^2**.

Standardized mean difference in delta G_CV:
- **-0.078**.

Therefore the stagewise subset is not an extreme subset with respect to the
temporal increase in marginal forecast value, despite being clearly selected
toward shorter distances and stronger late source-target coupling.

## Interpretation

Licensed:

> The stagewise subset is selected toward shorter source-target distances and
> stronger late environmental coupling, so its population-front results should
> not be generalized mechanically to the full 166-pair network.

Also licensed:

> The increase in cross-validated forecast value is of similar magnitude in the
> stagewise subset and the excluded environmental pairs.

Not licensed:
- the 31-pair subset is representative of all migration routes;
- subset selection is ignorable;
- stagewise population dynamics can be extrapolated to the full network.

Role in V4.4:
**generalization boundary for the same-system stagewise bridge.**

## Provenance

Workflow:
- run: 37401696411
- artifact: 11385109112
- artifact SHA256:
  598b8a936f45068296d1772d3ea4a29baf6f2d345b0bfe9a221f78e74d14240c

Script:
analysis/movement_phenology/payoff_b_v8_stagewise_subset_representativeness.R
